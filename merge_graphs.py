#!/usr/bin/env python3
'''merge_graphs.py: merge two KGs that are in the KG2 JSON format

   Usage: merge_graphs.py [--kgFileOrphanEdges <kgFileOrphanEdges>]
                           --outpufFile <outputFile.json>
                           <kgNodesFile1> ... <kgNodesFileN>
                           <kgEdgesFile1> ... <kgEdgesFileN>
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import argparse
import kg2_util
import json
import sys


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='merge_graphs.py: merge two or more JSON KG files')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('--kgFileOrphanEdges', type=str, nargs='?', default=None)
    arg_parser.add_argument('--outputFile', type=str, nargs='?', default=None)
    arg_parser.add_argument('--kgNodesFiles', type=str, nargs='+')
    arg_parser.add_argument('--kgEdgesFiles', type=str, nargs='+')
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    kg_nodes_file_names = args.kgNodesFiles
    kg_edges_file_names = args.kgEdgesFiles
    test_mode = args.test
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile
    orphan_edges_file_name = args.kgFileOrphanEdges

    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    orphan_info = kg2_util.create_single_jsonlines(test_mode)
    orphan_output = orphan_info[0]

    nodes = dict()

    for kg_nodes_file_name in kg_nodes_file_names:
        kg2_util.log_message("reading nodes from file",
                             ontology_name=kg_nodes_file_name,
                             output_stream=sys.stderr)
        num_nodes_added = 0
        for node in kg2_util.read_json_lines(kg_nodes_file_name):
            node_id = node['id']
            if node_id not in nodes:
                nodes[node_id] = node
                num_nodes_added += 1
            else:
                nodes[node_id] = kg2_util.merge_two_dicts(nodes[node_id], node)
        kg2_util.log_message("number of nodes added: " + num_nodes_added,
                             ontology_name=kg_nodes_file_name,
                             output_stream=sys.stderr)
    ctr_edges_added = 0
    last_edges_added = 0
    last_orphan_edges = 0
    kg_orphan_edges_count = 0
    edge_keys = set()
    for kg_edges_file_name in kg_edges_file_names:
        kg2_util.log_message("reading edges from file",
                             ontology_name=kg_edges_file_name,
                             output_stream=sys.stderr)
        for rel_dict in kg2_util.read_json_lines(kg_edges_file_name):
            subject_curie = rel_dict['subject']
            object_curie = rel_dict['object']
            if subject_curie in nodes and object_curie in nodes:
                ctr_edges_added += 1
                edge_key =rel_dict["id"]
                if edge_key not in edge_keys:
                    edge_keys.add(edge_key)
                    edges_output.write(rel_dict)
            else:
                orphan_output.write(rel_dict)
                kg_orphan_edges_count += 1

        kg2_util.log_message("number of edges added: " + str(ctr_edges_added - last_edges_added),
                             ontology_name=kg_edges_file_name,
                             output_stream=sys.stderr)
        last_edges_added = ctr_edges_added
        kg2_util.log_message("number of orphan edges: " + str(kg_orphan_edges_count -
                                                              last_orphan_edges),
                             ontology_name=kg_edges_file_name,
                             output_stream=sys.stderr)
        last_orphan_edges = kg_orphan_edges_count

    for node in nodes.values():
        nodes_output.write(node)
    del nodes

    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)
    kg2_util.close_single_jsonlines(orphan_info, orphan_edges_file_name)
