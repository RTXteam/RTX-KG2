#!/bin/env python3
"""
This script creates a canonicalized version of KG2 stored in TSV files, ready for import into neo4j. The TSVs are
created in the directory this script is in.
Usage: python3 create_kg2c_files.py [--test]
"""
import argparse
import csv
import gc
import json
import logging
import os
import pickle
import re
import sqlite3
import sys
import time
import traceback

from datetime import datetime
from multiprocessing import Pool
from typing import List, Dict, Tuple, Union, Optional
from neo4j import GraphDatabase

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import select_best_description
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../")  # code directory
from RTXConfiguration import RTXConfiguration
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../ARAX/NodeSynonymizer/")
from node_synonymizer import NodeSynonymizer

ARRAY_NODE_PROPERTIES = ["all_categories", "publications", "equivalent_curies", "all_names", "expanded_categories"]
ARRAY_EDGE_PROPERTIES = ["provided_by", "publications", "kg2_ids"]
DELIMITER_CHAR = "ǂ"  # Need to use a delimiter that does not appear in any list items (strings)
KG2C_DIR = f"{os.path.dirname(os.path.abspath(__file__))}"


def _run_kg2_cypher_query(cypher_query: str) -> List[Dict[str, any]]:
    # This function sends a cypher query to the KG2 neo4j specified in config.json and returns the results
    rtxc = RTXConfiguration()
    rtxc.live = "KG2"
    try:
        driver = GraphDatabase.driver(rtxc.neo4j_bolt, auth=(rtxc.neo4j_username, rtxc.neo4j_password))
        with driver.session() as session:
            logging.info(f"  Sending cypher query to KG2 neo4j ({rtxc.neo4j_bolt})..")
            query_results = session.run(cypher_query).data()
            logging.info(f"  Got {len(query_results)} results back from neo4j")
        driver.close()
    except Exception:
        tb = traceback.format_exc()
        error_type, error, _ = sys.exc_info()
        logging.error(f"Encountered a problem interacting with {rtxc.neo4j_bolt}. {tb}")
        return []
    else:
        return query_results


def _convert_list_to_string_encoded_format(input_list_or_str: Union[List[str], str]) -> Union[str, List[str]]:
    if isinstance(input_list_or_str, list):
        filtered_list = [item for item in input_list_or_str if item]  # Get rid of any None items
        str_items = [item for item in filtered_list if isinstance(item, str)]
        if len(str_items) < len(filtered_list):
            logging.warning(f"  List contains non-str items (this is unexpected; I'll exclude them)")
        return DELIMITER_CHAR.join(str_items)
    else:
        return input_list_or_str


def _merge_two_lists(list_a: List[any], list_b: List[any]) -> List[any]:
    unique_items = list(set(list_a + list_b))
    return [item for item in unique_items if item]


def _get_edge_key(subject: str, object: str, predicate: str) -> str:
    return f"{subject}--{predicate}--{object}"


def _clean_up_description(description: str) -> str:
    # Removes all of the "UMLS Semantic Type: UMLS_STY:XXXX;" bits from descriptions
    return re.sub("UMLS Semantic Type: UMLS_STY:[a-zA-Z][0-9]{3}[;]?", "", description).strip().strip(";")


def _get_best_description(descriptions_list: List[str]) -> Optional[str]:
    candidate_descriptions = [description for description in descriptions_list if description and len(description) < 10000]
    if len(candidate_descriptions) == 1:
        return candidate_descriptions[0]
    else:
        # Use Chunyu's NLP-based method to select the best description out of the coalesced nodes
        description_finder = select_best_description(candidate_descriptions)
        return description_finder.get_best_description


def _modify_column_headers_for_neo4j(plain_column_headers: List[str], file_name_root: str) -> List[str]:
    modified_headers = []
    all_array_column_names = ARRAY_NODE_PROPERTIES + ARRAY_EDGE_PROPERTIES
    for header in plain_column_headers:
        if header in all_array_column_names:
            header = f"{header}:string[]"
        elif header == 'id' and "node" in file_name_root:  # Skip setting ID for edges
            header = f"{header}:ID"
        elif header == 'node_labels':
            header = ":LABEL"
        elif header == 'subject_for_conversion':
            header = ":START_ID"
        elif header == 'object_for_conversion':
            header = ":END_ID"
        elif header == 'predicate_for_conversion':
            header = ":TYPE"
        modified_headers.append(header)
    return modified_headers


def _create_node(preferred_curie: str, name: Optional[str], category: str, all_categories: List[str],
                 expanded_categories: List[str], equivalent_curies: List[str], publications: List[str],
                 all_names: List[str], iri: Optional[str], description: Optional[str], descriptions_list: List[str]) -> Dict[str, any]:
    assert isinstance(preferred_curie, str)
    assert isinstance(name, str) or name is None
    assert isinstance(category, str)
    assert isinstance(all_names, list)
    assert isinstance(all_categories, list)
    assert isinstance(expanded_categories, list)
    assert isinstance(equivalent_curies, list)
    assert isinstance(publications, list)
    return {
        "id": preferred_curie,
        "name": name,
        "category": category,
        "all_names": all_names,
        "all_categories": all_categories,
        "expanded_categories": expanded_categories,
        "iri": iri,
        "description": description,
        "descriptions_list": descriptions_list,
        "equivalent_curies": equivalent_curies,
        "publications": publications
    }


def _create_edge(subject: str, object: str, predicate: str, provided_by: List[str], publications: List[str],
                 kg2_ids: List[str]) -> Dict[str, any]:
    assert isinstance(subject, str)
    assert isinstance(object, str)
    assert isinstance(predicate, str)
    assert isinstance(provided_by, list)
    assert isinstance(publications, list)
    assert isinstance(kg2_ids, list)
    return {
        "subject": subject,
        "object": object,
        "predicate": predicate,
        "provided_by": provided_by,
        "publications": publications,
        "kg2_ids": kg2_ids
    }


def _write_list_to_neo4j_ready_tsv(input_list: List[Dict[str, any]], file_name_root: str, is_test: bool):
    # Converts a list into the specific format Neo4j wants (string with delimiter)
    logging.info(f"  Creating {file_name_root} header file..")
    column_headers = list(input_list[0].keys())
    modified_headers = _modify_column_headers_for_neo4j(column_headers, file_name_root)
    with open(f"{KG2C_DIR}/{'test_' if is_test else ''}{file_name_root}_header.tsv", "w+") as header_file:
        dict_writer = csv.DictWriter(header_file, modified_headers, delimiter='\t')
        dict_writer.writeheader()
    logging.info(f"  Creating {file_name_root} file..")
    with open(f"{KG2C_DIR}/{'test_' if is_test else ''}{file_name_root}.tsv", "w+") as data_file:
        dict_writer = csv.DictWriter(data_file, column_headers, delimiter='\t')
        dict_writer.writerows(input_list)


def create_kg2c_json_file(canonicalized_nodes_dict: Dict[str, Dict[str, any]],
                          canonicalized_edges_dict: Dict[str, Dict[str, any]],
                          meta_info_dict: Dict[str, str], is_test: bool):
    logging.info(f" Creating KG2c JSON file..")
    kgx_format_json = {"nodes": list(canonicalized_nodes_dict.values()),
                       "edges": list(canonicalized_edges_dict.values())}
    kgx_format_json.update(meta_info_dict)
    with open(f"{KG2C_DIR}/kg2c{'_test' if is_test else ''}.json", "w+") as output_file:
        json.dump(kgx_format_json, output_file)


def create_kg2c_lite_json_file(canonicalized_nodes_dict: Dict[str, Dict[str, any]],
                               canonicalized_edges_dict: Dict[str, Dict[str, any]],
                               meta_info_dict: Dict[str, str], is_test: bool):
    logging.info(f" Creating KG2c lite JSON file..")
    # Filter out all except these properties so we create a lightweight KG
    node_lite_properties = ["id", "name", "category", "expanded_categories"]
    edge_lite_properties = ["id", "predicate", "subject", "object", "provided_by", "publications"]
    lite_kg = {"nodes": [], "edges": []}
    for node in canonicalized_nodes_dict.values():
        lite_node = dict()
        for lite_property in node_lite_properties:
            lite_node[lite_property] = node[lite_property]
        lite_kg["nodes"].append(lite_node)
    for edge in canonicalized_edges_dict.values():
        lite_edge = dict()
        for lite_property in edge_lite_properties:
            lite_edge[lite_property] = edge[lite_property]
        lite_kg["edges"].append(lite_edge)
    lite_kg.update(meta_info_dict)

    # Save this lite KG to a JSON file
    logging.info(f"    Saving lite json...")
    with open(f"{KG2C_DIR}/kg2c_lite{'_test' if is_test else ''}.json", "w+") as output_file:
        json.dump(lite_kg, output_file)


def create_kg2c_sqlite_db(canonicalized_nodes_dict: Dict[str, Dict[str, any]], is_test: bool):
    logging.info(" Creating KG2c sqlite database..")
    db_name = f"kg2c{'_test' if is_test else ''}.sqlite"
    # Remove any preexisting version of this database
    if os.path.exists(db_name):
        os.remove(db_name)
    connection = sqlite3.connect(db_name)
    # Add all nodes (node object is dumped into a JSON string)
    connection.execute("CREATE TABLE nodes (id TEXT, node TEXT)")
    node_rows = [(node["id"], json.dumps(node)) for node in canonicalized_nodes_dict.values()]
    connection.executemany(f"INSERT INTO nodes (id, node) VALUES (?, ?)", node_rows)
    connection.execute("CREATE UNIQUE INDEX node_id_index ON nodes (id)")
    connection.commit()
    cursor = connection.execute(f"SELECT COUNT(*) FROM nodes")
    logging.info(f"  Done creating nodes table; contains {cursor.fetchone()[0]} rows.")
    cursor.close()
    connection.close()


def create_kg2c_tsv_files(canonicalized_nodes_dict: Dict[str, Dict[str, any]],
                          canonicalized_edges_dict: Dict[str, Dict[str, any]], is_test: bool):
    # Convert array fields into the format neo4j wants and do some final processing
    for canonicalized_node in canonicalized_nodes_dict.values():
        for list_node_property in ARRAY_NODE_PROPERTIES:
            canonicalized_node[list_node_property] = _convert_list_to_string_encoded_format(canonicalized_node[list_node_property])
        canonicalized_node['node_labels'] = canonicalized_node['expanded_categories']
    for canonicalized_edge in canonicalized_edges_dict.values():
        if not is_test:  # Make sure we don't have any orphan edges
            assert canonicalized_edge['subject'] in canonicalized_nodes_dict
            assert canonicalized_edge['object'] in canonicalized_nodes_dict
        for list_edge_property in ARRAY_EDGE_PROPERTIES:
            canonicalized_edge[list_edge_property] = _convert_list_to_string_encoded_format(canonicalized_edge[list_edge_property])
        canonicalized_edge['predicate_for_conversion'] = canonicalized_edge['predicate']
        canonicalized_edge['subject_for_conversion'] = canonicalized_edge['subject']
        canonicalized_edge['object_for_conversion'] = canonicalized_edge['object']

    # Finally dump all our nodes/edges into TSVs (formatted for neo4j)
    logging.info(f" Creating TSVs for Neo4j..")
    _write_list_to_neo4j_ready_tsv(list(canonicalized_nodes_dict.values()), "nodes_c", is_test)
    _write_list_to_neo4j_ready_tsv(list(canonicalized_edges_dict.values()), "edges_c", is_test)


def _canonicalize_nodes(neo4j_nodes: List[Dict[str, any]]) -> Tuple[Dict[str, Dict[str, any]], Dict[str, str]]:
    synonymizer = NodeSynonymizer()
    node_ids = [node.get('id') for node in neo4j_nodes if node.get('id')]
    logging.info(f"  Sending NodeSynonymizer.get_canonical_curies() {len(node_ids)} curies..")
    canonicalized_info = synonymizer.get_canonical_curies(curies=node_ids, return_all_categories=True)
    all_canonical_curies = {canonical_info['preferred_curie'] for canonical_info in canonicalized_info.values() if canonical_info}
    logging.info(f"  Sending NodeSynonymizer.get_equivalent_nodes() {len(all_canonical_curies)} curies..")
    equivalent_curies_info = synonymizer.get_equivalent_nodes(all_canonical_curies)
    recognized_curies = {curie for curie in equivalent_curies_info if equivalent_curies_info.get(curie)}
    equivalent_curies_dict = {curie: list(equivalent_curies_info.get(curie)) for curie in recognized_curies}
    with open(f"{KG2C_DIR}/equivalent_curies.pickle", "wb") as equiv_curies_dump:  # Save these for use by downstream script
        pickle.dump(equivalent_curies_dict, equiv_curies_dump, protocol=pickle.HIGHEST_PROTOCOL)
    logging.info(f"  Creating canonicalized nodes..")
    curie_map = dict()
    canonicalized_nodes = dict()
    for neo4j_node in neo4j_nodes:
        # Grab relevant info for this node and its canonical version
        canonical_info = canonicalized_info.get(neo4j_node['id'])
        canonicalized_curie = canonical_info.get('preferred_curie', neo4j_node['id']) if canonical_info else neo4j_node['id']
        publications = neo4j_node['publications'] if neo4j_node.get('publications') else []
        descriptions_list = [neo4j_node['description']] if neo4j_node.get('description') else []
        if canonicalized_curie in canonicalized_nodes:
            # Merge this node into its corresponding canonical node
            existing_canonical_node = canonicalized_nodes[canonicalized_curie]
            existing_canonical_node['publications'] = _merge_two_lists(existing_canonical_node['publications'], publications)
            existing_canonical_node['all_names'] = _merge_two_lists(existing_canonical_node['all_names'], [neo4j_node['name']])
            existing_canonical_node['descriptions_list'] = _merge_two_lists(existing_canonical_node['descriptions_list'], descriptions_list)
            # Make sure any nodes subject to #1074-like problems still appear in equivalent curies
            existing_canonical_node['equivalent_curies'] = _merge_two_lists(existing_canonical_node['equivalent_curies'], [neo4j_node['id']])
            # Add the IRI for the 'preferred' curie, if we've found that node
            if neo4j_node['id'] == canonicalized_curie:
                existing_canonical_node['iri'] = neo4j_node.get('iri')
        else:
            # Initiate the canonical node for this synonym group
            name = canonical_info['preferred_name'] if canonical_info else neo4j_node['name']
            category = canonical_info['preferred_category'] if canonical_info else neo4j_node['category']
            all_categories = list(canonical_info['all_categories']) if canonical_info else [neo4j_node['category']]
            expanded_categories = list(canonical_info['expanded_categories']) if canonical_info else [neo4j_node['category']]
            iri = neo4j_node['iri'] if neo4j_node['id'] == canonicalized_curie else None
            all_names = [neo4j_node['name']]
            canonicalized_node = _create_node(preferred_curie=canonicalized_curie,
                                              name=name,
                                              category=category,
                                              all_categories=all_categories,
                                              expanded_categories=expanded_categories,
                                              publications=publications,
                                              equivalent_curies=equivalent_curies_dict.get(canonicalized_curie, [canonicalized_curie]),
                                              iri=iri,
                                              description=None,
                                              descriptions_list=descriptions_list,
                                              all_names=all_names)
            canonicalized_nodes[canonicalized_node['id']] = canonicalized_node
        curie_map[neo4j_node['id']] = canonicalized_curie  # Record this mapping for easy lookup later
    return canonicalized_nodes, curie_map


def _canonicalize_edges(neo4j_edges: List[Dict[str, any]], curie_map: Dict[str, str], is_test: bool) -> Dict[str, Dict[str, any]]:
    canonicalized_edges = dict()
    for neo4j_edge in neo4j_edges:
        kg2_edge_id = neo4j_edge['id']
        original_subject = neo4j_edge['subject']
        original_object = neo4j_edge['object']
        if not is_test:  # Make sure we have the mappings we expect
            assert original_subject in curie_map
            assert original_object in curie_map
        canonicalized_subject = curie_map.get(original_subject, original_subject)
        canonicalized_object = curie_map.get(original_object, original_object)
        edge_publications = neo4j_edge['publications'] if neo4j_edge.get('publications') else []
        edge_provided_by = neo4j_edge['provided_by'] if neo4j_edge.get('provided_by') else []
        if canonicalized_subject != canonicalized_object:  # Don't allow self-edges
            canonicalized_edge_key = _get_edge_key(canonicalized_subject, canonicalized_object, neo4j_edge['predicate'])
            if canonicalized_edge_key in canonicalized_edges:
                canonicalized_edge = canonicalized_edges[canonicalized_edge_key]
                canonicalized_edge['provided_by'] = _merge_two_lists(canonicalized_edge['provided_by'], edge_provided_by)
                canonicalized_edge['publications'] = _merge_two_lists(canonicalized_edge['publications'], edge_publications)
                canonicalized_edge['kg2_ids'].append(kg2_edge_id)
            else:
                new_canonicalized_edge = _create_edge(subject=canonicalized_subject,
                                                      object=canonicalized_object,
                                                      predicate=neo4j_edge['predicate'],
                                                      provided_by=edge_provided_by,
                                                      publications=edge_publications,
                                                      kg2_ids=[kg2_edge_id])
                canonicalized_edges[canonicalized_edge_key] = new_canonicalized_edge
    return canonicalized_edges


def create_kg2c_files(is_test=False):
    """
    This function extracts all nodes/edges from the regular KG2 Neo4j endpoint (specified in your config.json),
    canonicalizes the nodes, merges edges (based on subject, object, predicate), and saves the resulting canonicalized
    graph in multiple file formats: JSON, sqlite, and TSV (ready for import into Neo4j).
    """
    logging.info(f" Extracting nodes from KG2..")
    nodes_query = f"match (n) return n.id as id, n.name as name, n.category as category, " \
                  f"n.publications as publications, n.iri as iri, n.description as description{' limit 5000' if is_test else ''}"
    neo4j_nodes = _run_kg2_cypher_query(nodes_query)
    if neo4j_nodes:
        logging.info(f" Canonicalizing nodes..")
        canonicalized_nodes_dict, curie_map = _canonicalize_nodes(neo4j_nodes)
        logging.info(f"  Number of KG2 nodes was reduced to {len(canonicalized_nodes_dict)} ({round((len(canonicalized_nodes_dict) / len(neo4j_nodes)) * 100)}%)")
    else:
        logging.error(f"Couldn't get node data from KG2 neo4j.")
        return
    logging.info(f" Extracting edges from KG2..")
    edges_query = f"match (n)-[e]->(m) return n.id as subject, m.id as object, e.predicate as " \
                  f"predicate, e.provided_by as provided_by, e.publications as publications, e.id as id" \
                  f"{' limit 20000' if is_test else ''}"
    neo4j_edges = _run_kg2_cypher_query(edges_query)
    if neo4j_edges:
        logging.info(f" Canonicalizing edges..")
        canonicalized_edges_dict = _canonicalize_edges(neo4j_edges, curie_map, is_test)
        logging.info(f"  Number of KG2 edges was reduced to {len(canonicalized_edges_dict)} ({round((len(canonicalized_edges_dict) / len(neo4j_edges)) * 100)}%)")
    else:
        logging.error(f"Couldn't get edge data from KG2 neo4j.")
        return

    # Create a node containing information about this KG2C build
    with open(f"{KG2C_DIR}/kg2c_config.json") as config_file:
        kg2c_config_info = json.load(config_file)
    kg2_version = kg2c_config_info.get("kg2_version")
    biolink_version = kg2c_config_info.get("biolink_version")
    description_dict = {"kg2_version": kg2_version,
                        "biolink_version": biolink_version,
                        "build_date": datetime.now().strftime('%Y-%m-%d %H:%M')}
    description = f"{description_dict}"
    name = f"RTX-KG{kg2_version}c"
    kg2c_build_node = _create_node(preferred_curie="RTX:KG2c",
                                   name=name,
                                   all_categories=["biolink:InformationContentEntity"],
                                   expanded_categories=["biolink:InformationContentEntity"],
                                   category="biolink:InformationContentEntity",
                                   equivalent_curies=[],
                                   publications=[],
                                   iri="http://rtx.ai/identifiers#KG2c",
                                   all_names=[name],
                                   description=description,
                                   descriptions_list=[description])
    canonicalized_nodes_dict[kg2c_build_node['id']] = kg2c_build_node

    # Choose best descriptions using Chunyu's NLP-based method
    node_ids = list(canonicalized_nodes_dict)
    description_lists = [canonicalized_nodes_dict[node_id]["descriptions_list"] for node_id in node_ids]
    num_cpus = os.cpu_count()
    logging.info(f" Detected {num_cpus} cpus; will use all of them to choose best descriptions")
    pool = Pool(num_cpus)
    logging.info(f" Starting to use Chunyu's NLP-based method to choose best descriptions (in parallel)..")
    start = time.time()
    best_descriptions = pool.map(_get_best_description, description_lists)
    logging.info(f" Choosing best descriptions took {round(((time.time() - start) / 60) / 60, 2)} hours")
    # Actually decorate nodes with their 'best' description
    for num in range(len(node_ids)):
        node_id = node_ids[num]
        best_description = best_descriptions[num]
        canonicalized_nodes_dict[node_id]["description"] = best_description
        del canonicalized_nodes_dict[node_id]["descriptions_list"]
    del description_lists
    del best_descriptions
    gc.collect()

    # Do some final clean-up/formatting of nodes, now that all merging is done
    logging.info(f" Doing final clean-up/formatting of nodes")
    for node_id, node in canonicalized_nodes_dict.items():
        node["publications"] = node["publications"][:10]  # We don't need a ton of publications, so truncate them
    logging.info(f" Doing final clean-up/formatting of edges")
    # Convert our edge IDs to integers (to save space downstream) and add them as actual properties on the edges
    edge_num = 1
    for edge_id, edge in canonicalized_edges_dict.items():
        edge["id"] = edge_num
        edge_num += 1
        edge["publications"] = edge["publications"][:20]  # We don't need a ton of publications, so truncate them

    # Actually create all of our output files (different formats for storing KG2c)
    meta_info_dict = {"kg2_version": kg2_version, "biolink_version": biolink_version}
    create_kg2c_lite_json_file(canonicalized_nodes_dict, canonicalized_edges_dict, meta_info_dict, is_test)
    create_kg2c_json_file(canonicalized_nodes_dict, canonicalized_edges_dict, meta_info_dict, is_test)
    create_kg2c_sqlite_db(canonicalized_nodes_dict, is_test)
    create_kg2c_tsv_files(canonicalized_nodes_dict, canonicalized_edges_dict, is_test)


def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        handlers=[logging.FileHandler("createkg2cfiles.log"),
                                  logging.StreamHandler()])
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    args = arg_parser.parse_args()

    logging.info(f"Starting to create KG2canonicalized..")
    start = time.time()
    create_kg2c_files(args.test)
    logging.info(f"Done! Took {round(((time.time() - start) / 60) / 60, 2)} hours.")


if __name__ == "__main__":
    main()
