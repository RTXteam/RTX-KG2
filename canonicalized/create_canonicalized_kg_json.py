#!/bin/env python3
import argparse
import gzip
import json
import os
import sys
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../ARAX/NodeSynonymizer/")
from node_synonymizer import NodeSynonymizer


def create_canonicalized_kg_json(input_slim_kg2_path, output_canonicalized_kg2_path):
    print(f"Starting to create {output_canonicalized_kg2_path}..")
    start = time.time()
    try:
        with gzip.open(input_slim_kg2_path, 'r') as input_file:
            input_kg2 = json.load(input_file)
    except Exception:
        print(f"ERROR: Could not find '{input_slim_kg2_path}' file.")
        return
    if not input_kg2.get('nodes') or not input_kg2.get('edges'):
        print(f"ERROR: Input KG json file is missing a nodes and/or edges property.")
        return
    print(f"  Input KG (non-canonicalized) contains {len(input_kg2['nodes'])} nodes and "
          f"{len(input_kg2['edges'])} edges.")

    # Grab canonical curies for every node in the input KG using NodeSynonymizer
    original_nodes = {node['id']: node for node in input_kg2.get('nodes') if node.get('id')}
    synonymizer = NodeSynonymizer()
    print(f"  Getting canonical curies from NodeSynonymizer..")
    canonical_curie_info = synonymizer.get_canonical_curies(curies=list(original_nodes.keys()))
    print(f"  Got results back from NodeSynonymizer.")
    # TODO: get equivalent curies and types for each synonym group to store on canonicalized nodes

    # Canonicalize the nodes
    print(f"  Canonicalizing nodes in the input KG..")
    nodes_canonicalized = dict()
    input_curie_to_canonical_curie = dict()
    for input_curie, canonical_info in canonical_curie_info.items():
        if canonical_info:
            canonicalized_node = {'id': canonical_info.get('preferred_curie', input_curie),
                                  'name': canonical_info.get('preferred_name'),
                                  'category label': canonical_info.get('preferred_type')}
            nodes_canonicalized[canonicalized_node['id']] = canonicalized_node
            input_curie_to_canonical_curie[input_curie] = canonicalized_node['id']
        else:
            # Just use the node's original info if we couldn't find canonical info for it
            input_curie_to_canonical_curie[input_curie] = input_curie
            original_node = original_nodes.get(input_curie)
            nodes_canonicalized[input_curie] = {'id': input_curie,
                                                'name': original_node.get('name'),
                                                'category label': original_node.get('category label')}
            input_curie_to_canonical_curie[input_curie] = input_curie
    print(f"  After canonicalization, there are {len(nodes_canonicalized)} nodes "
          f"({round((len(nodes_canonicalized) / len(original_nodes)) * 100)}% of input KG).")

    # Record info about this build in a node
    original_build_node = original_nodes.get('RTX:KG2')
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    if original_build_node:
        canonicalized_build_node = nodes_canonicalized.pop('RTX:KG2')
        canonicalized_build_node['id'] = 'RTX:KG2C'
        canonicalized_build_node['name'] = f"KG2C:Build - {now}, built from {original_build_node['update date']} KG2 build"
    else:
        canonicalized_build_node = {'id': 'RTX:KG2C',
                                    'name': f"KG2C:Build - {now}",
                                    'category label': None}
    nodes_canonicalized[canonicalized_build_node['id']] = canonicalized_build_node

    # Remap edges and merge them as appropriate
    print(f"  Remapping and merging edges..")
    edges_canonicalized = dict()
    for current_edge in input_kg2.get('edges', []):
        canonicalized_subject = current_edge['subject']
        canonicalized_object = current_edge['object']
        predicate = current_edge['simplified edge label']
        edge_key = f"{canonicalized_subject}--{predicate}--{canonicalized_object}"
        if edge_key in edges_canonicalized:
            existing_edge = edges_canonicalized.get(edge_key)
            existing_edge['provided by'] = list(set(existing_edge['provided by'] + current_edge['provided by']))
        else:
            remapped_edge = {'subject': canonicalized_subject,
                             'object': canonicalized_object,
                             'simplified edge label': predicate,
                             'provided by': current_edge['provided by']}
            edges_canonicalized[edge_key] = remapped_edge

    # Put together our final canonicalized KG
    canonicalized_kg = {'nodes': list(nodes_canonicalized.values()),
                        'edges': list(edges_canonicalized.values())}
    print(f"  Canonicalized KG contains {len(canonicalized_kg['nodes'])} nodes and {len(canonicalized_kg['edges'])} edges.")

    # Verify format is as expected
    print(f"  Verifying node/edge structure is as expected..")
    for node in canonicalized_kg['nodes']:
        assert set(node) == {'id', 'name', 'category label'}
    for edge in canonicalized_kg['edges']:
        assert set(edge) == {'subject', 'object', 'simplified edge label', 'provided by'}

    # Save the KG to our output file..
    print(f"  Saving canonicalized data to {output_canonicalized_kg2_path}..")
    with open(output_canonicalized_kg2_path, 'w+') as output_file:
        json.dump(canonicalized_kg, output_file)

    print(f"Done! Took {round((time.time() - start) / 60)} minutes.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help="Path to input file (e.g., kg2-slim.json.gz)")
    parser.add_argument('output_file', type=str, help="Path to output file (e.g., kg2-canonicalized.json)")
    args = parser.parse_args()
    create_canonicalized_kg_json(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
