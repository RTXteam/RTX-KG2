#!/bin/env python3
"""
This script creates a canonicalized version of KG2 stored in TSV files, ready for import into neo4j. The TSVs are
created in the current working directory.
Usage: python3 create_canonicalized_kg_tsvs.py [--test]
"""
import argparse
import ast
import csv
import os
import sys
import time
import traceback

from datetime import datetime
from typing import List, Dict, Tuple, Union
from neo4j import GraphDatabase

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../")  # code directory
from RTXConfiguration import RTXConfiguration
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../ARAX/NodeSynonymizer/")
from node_synonymizer import NodeSynonymizer


def _run_cypher_query(cypher_query: str, kg="KG2") -> List[Dict[str, any]]:
    # This function sends a cypher query to neo4j (either KG1 or KG2) and returns results
    rtxc = RTXConfiguration()
    if kg == "KG2":
        rtxc.live = "KG2"
    try:
        driver = GraphDatabase.driver(rtxc.neo4j_bolt, auth=(rtxc.neo4j_username, rtxc.neo4j_password))
        with driver.session() as session:
            print(f"  Sending cypher query to {kg} neo4j..")
            query_results = session.run(cypher_query).data()
            print(f"  Got {len(query_results)} results back from neo4j")
        driver.close()
    except Exception:
        tb = traceback.format_exc()
        error_type, error, _ = sys.exc_info()
        print(f"ERROR: Encountered a problem interacting with {kg} neo4j. {tb}")
        return []
    else:
        return query_results


def _convert_list_to_neo4j_format(input_list: List[any]) -> str:
    return str(input_list).strip("[").strip("]").replace("'", "")


def _merge_two_lists(list_a: List[any], list_b: List[any]) -> List[any]:
    return list(set(list_a + list_b))


def _literal_eval_list(input_item: Union[str, List[any]]) -> List[any]:
    try:
        actual_list = ast.literal_eval(input_item)
    except Exception:
        return []
    else:
        return actual_list


def _convert_strange_provided_by_field_to_list(provided_by_field: List[any]) -> List[any]:
    # Needed temporarily until kg2-2+ is rolled out to production
    provided_by_list = []
    for item in provided_by_field:
        if "[" in item:
            item = item.replace("[", "")
        if "]" in item:
            item = item.replace("]", "")
        if "'" in item:
            item = item.replace("'", "")
        provided_by_list.append(item)
    return provided_by_list


def _get_curie_for_node_type(node_type: str) -> str:
    return f"biolink:{_convert_string_to_pascal_case(node_type)}"


def _get_edge_key(source: str, target: str, edge_type: str) -> str:
    return f"{source}--{edge_type}--{target}"


def _convert_string_to_pascal_case(input_string: str) -> str:
    # Converts a string like 'chemical_substance' or 'chemicalSubstance' to 'ChemicalSubstance'
    if not input_string:
        return ""
    elif "_" in input_string:
        words = input_string.split('_')
        return "".join([word.capitalize() for word in words])
    elif len(input_string) > 1:
        return input_string[0].upper() + input_string[1:]
    else:
        return input_string.capitalize()


def _canonicalize_nodes(nodes: List[Dict[str, any]]) -> Tuple[Dict[str, Dict[str, any]], Dict[str, str]]:
    synonymizer = NodeSynonymizer()
    node_ids = [node.get('id') for node in nodes if node.get('id')]
    print(f"  Sending NodeSynonymizer.get_canonical_curies() {len(node_ids)} curies..")
    canonicalized_info = synonymizer.get_canonical_curies(curies=node_ids, return_all_types=True)
    print(f"  Sending NodeSynonymizer.get_equivalent_nodes() {len(node_ids)} curies..")
    equivalent_curies_info = synonymizer.get_equivalent_nodes(node_ids)
    recognized_curies = {curie for curie in equivalent_curies_info if equivalent_curies_info.get(curie)}
    equivalent_curies_dict = {curie: list(equivalent_curies_info.get(curie)) for curie in recognized_curies}
    print(f"  Creating canonicalized nodes..")
    curie_map = dict()
    canonicalized_nodes = dict()
    for node in nodes:
        canonical_info = canonicalized_info.get(node['id'])
        canonicalized_curie = canonical_info.get('preferred_curie', node['id']) if canonical_info else node['id']
        node['publications'] = _literal_eval_list(node['publications'])  # Only need to do this until kg2.2+ is rolled out
        if canonicalized_curie in canonicalized_nodes:
            existing_canonical_node = canonicalized_nodes[canonicalized_curie]
            existing_canonical_node['publications'] = _merge_two_lists(existing_canonical_node['publications'], node['publications'])
        else:
            if canonical_info:
                canonicalized_node = _create_node(node_id=canonicalized_curie,
                                                  name=canonical_info.get('preferred_name', node['name']),
                                                  types=list(canonical_info.get('all_types')),
                                                  preferred_type=canonical_info.get('preferred_type', node['category_label']),
                                                  publications=node['publications'],
                                                  equivalent_curies=equivalent_curies_dict.get(node['id'], []))
            else:
                canonicalized_node = _create_node(node_id=canonicalized_curie,
                                                  name=node['name'],
                                                  types=[node['category_label']],
                                                  preferred_type=node['category_label'],
                                                  publications=node['publications'],
                                                  equivalent_curies=equivalent_curies_dict.get(node['id'], []))
            canonicalized_nodes[canonicalized_node['id']] = canonicalized_node
        curie_map[node['id']] = canonicalized_curie  # Record this mapping for easy lookup later
    return canonicalized_nodes, curie_map


def _canonicalize_edges(edges: List[Dict[str, any]], curie_map: Dict[str, str], is_test: bool) -> Dict[str, Dict[str, any]]:
    allowed_self_edges = ['positively_regulates', 'interacts_with', 'increase']
    canonicalized_edges = dict()
    for edge in edges:
        original_source_id = edge['subject']
        original_target_id = edge['object']
        if not is_test:  # Make sure we have the mappings we expect
            assert original_source_id in curie_map
            assert original_target_id in curie_map
        canonicalized_source_id = curie_map.get(original_source_id, original_source_id)
        canonicalized_target_id = curie_map.get(original_target_id, original_target_id)
        edge_type = edge['simplified_edge_label']
        # Convert fields that should be lists to lists (only need to do this until kg2.2+ is rolled out to production)
        edge['provided_by'] = _convert_strange_provided_by_field_to_list(edge['provided_by'])
        edge['publications'] = _literal_eval_list(edge['publications'])
        if canonicalized_source_id != canonicalized_target_id or edge_type in allowed_self_edges:
            canonicalized_edge_key = _get_edge_key(canonicalized_source_id, canonicalized_target_id, edge_type)
            if canonicalized_edge_key in canonicalized_edges:
                canonicalized_edge = canonicalized_edges[canonicalized_edge_key]
                canonicalized_edge['provided_by'] = _merge_two_lists(canonicalized_edge['provided_by'], edge['provided_by'])
                canonicalized_edge['publications'] = _merge_two_lists(canonicalized_edge['publications'], edge['publications'])
            else:
                new_canonicalized_edge = _create_edge(source=canonicalized_source_id,
                                                      target=canonicalized_target_id,
                                                      simplified_edge_label=edge['simplified_edge_label'],
                                                      provided_by=edge['provided_by'],
                                                      publications=edge['publications'])
                canonicalized_edges[canonicalized_edge_key] = new_canonicalized_edge
    return canonicalized_edges


def _add_edges_from_nodes_to_types(nodes_dict: Dict[str, Dict[str, any]], edges_dict: Dict[str, Dict[str, any]]):
    # This function adds edges mapping nodes to each of their types (e.g., (PR:123)-[has_type]->(biolink:Protein)
    all_node_ids = set(nodes_dict)
    for node_id in all_node_ids:
        node = nodes_dict[node_id]
        for node_type in node['types']:
            curie_for_node_type = _get_curie_for_node_type(node_type)
            if curie_for_node_type not in nodes_dict:
                node_type_node = _create_node(node_id=curie_for_node_type,
                                              name=node_type,
                                              types=["ontology_class"],
                                              preferred_type="ontology_class",
                                              equivalent_curies=[],
                                              publications=[])
                nodes_dict[node_type_node['id']] = node_type_node
            edge_to_node_type = _create_edge(source=node['id'],
                                             target=curie_for_node_type,
                                             simplified_edge_label="has_type",
                                             provided_by=["ARAX:NodeSynonymizer"],
                                             publications=[])
            edge_key = _get_edge_key(edge_to_node_type["subject"], edge_to_node_type["object"],
                                     edge_to_node_type["simplified_edge_label"])
            edges_dict[edge_key] = edge_to_node_type


def _modify_column_headers_for_neo4j(plain_column_headers: List[str]) -> List[str]:
    modified_headers = []
    array_columns = ['provided_by', 'types', 'equivalent_curies', 'publications']
    for header in plain_column_headers:
        if header in array_columns:
            header = f"{header}:string[]"
        elif header == 'id':
            header = f"{header}:ID"
        elif header == 'preferred_type_for_conversion':
            header = ":LABEL"
        elif header == 'subject_for_conversion':
            header = ":START_ID"
        elif header == 'object_for_conversion':
            header = ":END_ID"
        elif header == 'simplified_edge_label_for_conversion':
            header = ":TYPE"
        modified_headers.append(header)
    return modified_headers


def _create_node(node_id: str, name: str, types: List[str], preferred_type: str, equivalent_curies: List[str],
                 publications: List[str]) -> Dict[str, any]:
    assert isinstance(node_id, str)
    assert isinstance(name, str) or name is None
    assert isinstance(types, list)
    assert isinstance(preferred_type, str)
    assert isinstance(equivalent_curies, list)
    assert isinstance(publications, list)
    return {
        "id": node_id,
        "name": name,
        "types": types,
        "preferred_type": preferred_type,
        "equivalent_curies": equivalent_curies,
        "publications": publications
    }


def _create_edge(source: str, target: str, simplified_edge_label: str, provided_by: List[str], publications: List[str]) -> Dict[str, any]:
    assert isinstance(source, str)
    assert isinstance(target, str)
    assert isinstance(simplified_edge_label, str)
    assert isinstance(provided_by, list)
    assert isinstance(publications, list)
    return {
        "subject": source,
        "object": target,
        "simplified_edge_label": simplified_edge_label,
        "provided_by": provided_by,
        "publications": publications
    }


def _write_list_to_tsv(input_list: List[Dict[str, any]], file_name_root: str, is_test: bool):
    print(f"  Creating {file_name_root} header file..")
    column_headers = list(input_list[0].keys())
    modified_headers = _modify_column_headers_for_neo4j(column_headers)
    with open(f"{'test_' if is_test else ''}{file_name_root}_header.tsv", "w+") as header_file:
        dict_writer = csv.DictWriter(header_file, modified_headers, delimiter='\t')
        dict_writer.writeheader()
    print(f"  Creating {file_name_root} file..")
    with open(f"{'test_' if is_test else ''}{file_name_root}.tsv", "w+") as data_file:
        dict_writer = csv.DictWriter(data_file, column_headers, delimiter='\t')
        dict_writer.writerows(input_list)


def create_canonicalized_tsvs(is_test=False):
    # Canonicalize nodes and edges from KG2
    print(f" Extracting nodes from KG2..")
    nodes_query = f"match (n) return n.id as id, n.name as name, n.category_label as category_label, " \
                  f"n.publications as publications{' limit 20000' if is_test else ''}"
    neo4j_nodes = _run_cypher_query(nodes_query)
    if neo4j_nodes:
        print(f" Canonicalizing nodes..")
        canonicalized_nodes_dict, curie_map = _canonicalize_nodes(neo4j_nodes)
        print(f"  Number of KG2 nodes was reduced to {len(canonicalized_nodes_dict)} ({round((len(canonicalized_nodes_dict) / len(neo4j_nodes)) * 100)}%)")
    else:
        print(f"ERROR: Couldn't get node data from KG2 neo4j.")
        return
    print(f" Extracting edges from KG2..")
    edges_query = f"match (n)-[e]->(m) return n.id as subject, m.id as object, e.simplified_edge_label as " \
                  f"simplified_edge_label, e.provided_by as provided_by, e.publications as publications" \
                  f"{' limit 20000' if is_test else ''}"
    neo4j_edges = _run_cypher_query(edges_query)
    if neo4j_edges:
        print(f" Canonicalizing edges..")
        canonicalized_edges_dict = _canonicalize_edges(neo4j_edges, curie_map, is_test)
        print(f"  Number of KG2 edges was reduced to {len(canonicalized_edges_dict)} ({round((len(canonicalized_edges_dict) / len(neo4j_edges)) * 100)}%)")
    else:
        print(f"ERROR: Couldn't get edge data from KG2 neo4j.")
        return

    # Add edges from nodes to their types (for faster querying vs. the 'types' property on nodes)
    print(f" Adding edges from nodes to their node types..")
    start_node_count = len(canonicalized_nodes_dict)
    start_edge_count = len(canonicalized_edges_dict)
    _add_edges_from_nodes_to_types(canonicalized_nodes_dict, canonicalized_edges_dict)
    print(f"  Added {len(canonicalized_nodes_dict) - start_node_count} nodes representing node types")
    print(f"  Added {len(canonicalized_edges_dict) - start_edge_count} edges from nodes to their node types")

    # Create a node containing information about this KG2C build
    kg2c_build_node = _create_node(node_id="RTX:KG2C",
                                   name=f"KG2C:Build created on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                                   types=["data_file"],
                                   preferred_type="data_file",
                                   equivalent_curies=[],
                                   publications=[])
    canonicalized_nodes_dict[kg2c_build_node['id']] = kg2c_build_node

    # Convert array fields into the format neo4j wants and do final processing
    for canonicalized_node in canonicalized_nodes_dict.values():
        canonicalized_node['types'] = _convert_list_to_neo4j_format(canonicalized_node['types'])
        canonicalized_node['publications'] = _convert_list_to_neo4j_format(canonicalized_node['publications'])
        canonicalized_node['equivalent_curies'] = _convert_list_to_neo4j_format(canonicalized_node['equivalent_curies'])
        canonicalized_node['preferred_type_for_conversion'] = canonicalized_node['preferred_type']
    for canonicalized_edge in canonicalized_edges_dict.values():
        if not is_test:  # Make sure we don't have any orphan edges
            assert canonicalized_edge['subject'] in canonicalized_nodes_dict
            assert canonicalized_edge['object'] in canonicalized_nodes_dict
        canonicalized_edge['provided_by'] = _convert_list_to_neo4j_format(canonicalized_edge['provided_by'])
        canonicalized_edge['publications'] = _convert_list_to_neo4j_format(canonicalized_edge['publications'])
        canonicalized_edge['simplified_edge_label_for_conversion'] = canonicalized_edge['simplified_edge_label']
        canonicalized_edge['subject_for_conversion'] = canonicalized_edge['subject']
        canonicalized_edge['object_for_conversion'] = canonicalized_edge['object']

    # Finally dump all our nodes/edges into TSVs (formatted for neo4j)
    print(f" Saving data to TSVs..")
    _write_list_to_tsv(list(canonicalized_nodes_dict.values()), "nodes_c", is_test)
    _write_list_to_tsv(list(canonicalized_edges_dict.values()), "edges_c", is_test)


def main():
    arg_parser = argparse.ArgumentParser(description="Creates a canonicalized KG2, stored in TSV files")
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    args = arg_parser.parse_args()

    print(f"Starting to create canonicalized KG..")
    start = time.time()
    create_canonicalized_tsvs(args.test)
    print(f"Done! Took {round((time.time() - start) / 60, 2)} minutes.")


if __name__ == "__main__":
    main()
