#!/bin/env python3
"""
This script creates a canonicalized version of KG2 stored in TSV files, ready for import into neo4j. The TSVs are
created in the current working directory.
Usage: python3 create_canonicalized_kg_tsvs.py [--test]
"""
import argparse
import csv
import os
import sys
import time
import traceback

from datetime import datetime
from typing import List, Dict, Tuple
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


def canonicalize_nodes(nodes: List[Dict[str, any]]) -> Tuple[List[Dict[str, any]], Dict[str, str]]:
    synonymizer = NodeSynonymizer()
    node_ids = [node.get('id') for node in nodes if node.get('id')]
    print(f"  Sending NodeSynonymizer.get_canonical_curies() a list of {len(node_ids)} curies..")
    canonicalized_info = synonymizer.get_canonical_curies(curies=node_ids)
    print(f"  Editing nodes..")
    curie_map = dict()
    canonicalized_nodes = dict()
    for node in nodes:
        canonical_info = canonicalized_info.get(node['id'])
        if canonical_info:
            canonicalized_curie = canonical_info.get('preferred_curie', node['id'])
            curie_map[node['id']] = canonicalized_curie  # Store this mapping for easy access later
            node['id'] = canonicalized_curie
            node['category_label'] = canonical_info.get('preferred_type', node['category_label'])
            node['name'] = canonical_info.get('preferred_name', node['name'])
        else:
            curie_map[node['id']] = node['id']
        canonicalized_nodes[node['id']] = node

    # Create a node containing information about this KG2C build, and remove the original build node
    new_build_node = {'id': 'RTX:KG2C',
                      'name': f"KG2C:Build created on {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                      'category_label': 'data_file'}
    if 'RTX:KG2' in canonicalized_nodes:
        original_build_node = canonicalized_nodes.pop('RTX:KG2')
        new_build_node['name'] += f", from {original_build_node['update_date']} KG2 build"
    canonicalized_nodes[new_build_node['id']] = new_build_node

    # Add synonymization info to nodes
    print(f"  Sending NodeSynonymizer.get_equivalent_nodes() a list of {len(node_ids)} curies..")
    equivalent_curies_dict = synonymizer.get_equivalent_nodes(list(canonicalized_nodes.keys()))
    for canonicalized_node_id, canonicalized_node in canonicalized_nodes.items():
        canonicalized_node['equivalent_curies'] = equivalent_curies_dict.get(canonicalized_node_id)
        # TODO: also store list of node types (once added to NodeSynonymizer output)

    return list(canonicalized_nodes.values()), curie_map


def remap_edges(edges: List[Dict[str, any]], curie_map: Dict[str, str]) -> List[Dict[str, any]]:
    allowed_self_edges = ['positively_regulates', 'interacts_with', 'increase']
    merged_edges = dict()
    for edge in edges:
        original_source_id = edge['subject']
        original_target_id = edge['object']
        canonicalized_source_id = curie_map.get(original_source_id, original_source_id)
        canonicalized_target_id = curie_map.get(original_target_id, original_target_id)
        edge_type = edge['simplified_edge_label']
        if canonicalized_source_id != canonicalized_target_id or edge_type in allowed_self_edges:
            remapped_edge_key = f"{canonicalized_source_id}--{edge_type}--{canonicalized_target_id}"
            if remapped_edge_key in merged_edges:
                merged_edge = merged_edges[remapped_edge_key]
                merged_edge['provided_by'] = list(set(merged_edge['provided_by'] + edge['provided_by']))
            else:
                edge['subject'] = canonicalized_source_id
                edge['object'] = canonicalized_target_id
                merged_edges[remapped_edge_key] = edge
    return list(merged_edges.values())


def create_canonicalized_tsvs(test=False):
    # Grab the node data from KG2 neo4j and load it into TSVs
    print(f" Starting nodes..")
    nodes_query = f"match (n) return n.id as id, n.name as name, n.category_label as category_label{' limit 30000' if test else ''}"
    nodes = _run_cypher_query(nodes_query)
    if nodes:
        print(f"  Canonicalizing nodes..")
        canonicalized_nodes, curie_map = canonicalize_nodes(nodes)
        print(f"  Canonicalized KG contains {len(canonicalized_nodes)} nodes ({round((len(canonicalized_nodes) / len(nodes)) * 100)}%)")
        print(f"  Creating nodes header file..")
        column_headers = canonicalized_nodes[0].keys()
        with open(f"{'test_' if test else ''}nodes_c_header.tsv", "w+") as nodes_header_file:
            dict_writer = csv.DictWriter(nodes_header_file, column_headers, delimiter='\t')
            dict_writer.writeheader()
        print(f"  Creating nodes file..")
        with open(f"{'test_' if test else ''}nodes_c.tsv", "w+") as nodes_file:
            dict_writer = csv.DictWriter(nodes_file, column_headers, delimiter='\t')
            dict_writer.writerows(canonicalized_nodes)
    else:
        print(f"ERROR: Couldn't get node data from KG2 neo4j.")
        return

    # Grab the edge data from KG2 neo4j and load it into TSVs
    print(f" Starting edges..")
    edges_query = f"match (n)-[e]->(m) return n.id as subject, m.id as object, e.simplified_edge_label as " \
                  f"simplified_edge_label, e.provided_by as provided_by{' limit 30000' if test else ''}"
    edges = _run_cypher_query(edges_query)
    if edges:
        print(f"  Remapping edges..")
        remapped_edges = remap_edges(edges, curie_map)
        print(f"  Canonicalized KG contains {len(remapped_edges)} edges ({round((len(remapped_edges) / len(edges)) * 100)}%)")
        print(f"  Creating edges header file..")
        column_headers = remapped_edges[0].keys()
        with open(f"{'test_' if test else ''}edges_c_header.tsv", "w+") as edges_header_file:
            dict_writer = csv.DictWriter(edges_header_file, column_headers, delimiter='\t')
            dict_writer.writeheader()
        print(f"  Creating edges file..")
        with open(f"{'test_' if test else ''}edges_c.tsv", "w+") as edges_file:
            dict_writer = csv.DictWriter(edges_file, column_headers, delimiter='\t')
            dict_writer.writerows(remapped_edges)
    else:
        print(f"ERROR: Couldn't get edge data from KG2 neo4j.")
        return


def main():
    arg_parser = argparse.ArgumentParser(description="Creates a canonicalized KG2, stored in TSV files")
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    args = arg_parser.parse_args()

    print(f"Starting to create canonicalized KG TSV files..")
    start = time.time()
    create_canonicalized_tsvs(args.test)
    print(f"Done! Took {round((time.time() - start) / 60, 2)} minutes.")


if __name__ == "__main__":
    main()
