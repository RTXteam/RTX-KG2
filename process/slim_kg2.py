#!/usr/bin/env python3
''' slim_kg2.py: reduce graph in KG2 JSON format to only bare-bones node and edge properties.
    Usage: slim_kg2.py <inputNodesFile> <inputEdgesFile> <outputNodesFile> <outputEdgesFile>
'''
__author__ = 'Liliana Acevedo'
__copyright__ = 'Oregon State University'
__credits__ = ['Liliana Acevedo', 'Lindsey Kvarfordt', 'Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import argparse
import kg2_util
import datetime

NODE_PROPERTIES = {"category", "id", "name", "synonym", "same_as"}

EDGE_PROPERTIES = {
    "object",
    "object_aspect_qualifier",
    "object_direction_qualifier",
    "predicate",
    "primary_knowledge_source",
    "qualified_predicate",
    "subject"
}


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description="slim_kg2.py: reduce graph in KG2 JSON format to only bare-bones node and edge properties.")
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument("inputNodesFile", type=str)
    arg_parser.add_argument("inputEdgesFile", type=str)
    arg_parser.add_argument("outputNodesFile", type=str)
    arg_parser.add_argument("outputEdgesFile", type=str)
    return arg_parser


if __name__ == "__main__":
    start = datetime.datetime.now()

    args = make_arg_parser().parse_args()
    input_nodes_file_name = args.inputNodesFile
    input_edges_file_name = args.inputEdgesFile
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile
    test_mode = args.test

    print("Start time:", kg2_util.date())
    
    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    input_nodes_jsonlines_info = kg2_util.start_read_jsonlines(input_nodes_file_name)
    input_nodes = input_nodes_jsonlines_info[0]

    node_ctr = 0
    for node in input_nodes:
        node_ctr += 1
        if node_ctr % 1000000 == 0:
            print(node_ctr, "nodes finished.")
        temp_node = dict()
        for key, val in node.items():
            if key in NODE_PROPERTIES:
                temp_node[key] = val
        nodes_output.write(temp_node)

    print("Nodes completed.")
    kg2_util.end_read_jsonlines(input_nodes_jsonlines_info)

    input_edges_jsonlines_info = kg2_util.start_read_jsonlines(input_edges_file_name)
    input_edges = input_edges_jsonlines_info[0]

    edge_ctr = 0
    for edge in input_edges:
        edge_ctr += 1
        if edge_ctr % 1000000 == 0:
            print(edge_ctr, "edges finished.")
        temp_edge = dict()
        for key, val in edge.items():
            if key in EDGE_PROPERTIES:
                temp_edge[key] = val
        edges_output.write(temp_edge)

    print("Edges completed.")
    kg2_util.end_read_jsonlines(input_edges_jsonlines_info)

    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)

    print("Finish time:", kg2_util.date())

    finish = datetime.datetime.now()

    print(f"Total time: {finish-start}")
