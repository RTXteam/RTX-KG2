#!/usr/bin/env python3
''' slim_kg2.py: reduce graph in KG2 JSON format to only bare-bones node and edge properties.
    Usage: slim_kg2.py <inputFile>
                         --outputFile <outputFile
'''
__author__ = 'Liliana Acevedo'
__copyright__ = 'Oregon State University'
__credits__ = ['Liliana Acevedo', 'Lindsey Kvarfordt', 'Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import json
import ijson
import argparse
import kg2_util


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description=" slim_kg2.py: reduce graph in KG2 JSON format to only bare-bones node and edge properties.")
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument("inputFilepath", type=str)
    arg_parser.add_argument("outputFilepath", type=str)
    return arg_parser


if __name__ == "__main__":
    node_set = set(["name", "id", "full_name", "category", "knowledge_source"])
    edge_set = set(["core_predicate", "subject", "object", "predicate_label", "knowledge_source"])

    args = make_arg_parser().parse_args()
    test_mode = args.test
    reduced = {"nodes": [], "edges": []}
    # I think splitting this file into nodes and edges might be helpful in the future, 
    # but I'm leaving it as is for nwo
    # reduced_nodes = {"nodes": []}
    # reduced_edges = {"edges": []}
    with open(args.inputFilepath, "r") as fp:

        for item in ijson.items(fp, "build"):
            reduced["build"] = item

    with open(args.inputFilepath, "r") as fp:

        node_ctr = 0
        num_nodes = 11117653  # Snagging this number for kg2-report.json for debugging purposes
        
        for node_list in ijson.items(fp, "nodes"):
            for node in node_list:
                node_ctr += 1
                if node_ctr % 1000000 == 0:
                    print(f"Processing node {str(node_ctr)} of {str(num_nodes)}")
                temp_node = {}
                for key, val in node.items():
                    if key in node_set:
                        temp_node[key] = val
                reduced["nodes"].append(temp_node)
        print("Nodes completed")

    with open(args.inputFilepath, "r") as fp:

        edge_ctr = 0
        num_edges = 11117653  # Snagging this number for kg2-report.json for debugging purposes
        
        for edge_list in ijson.items(fp, "edges"):
            for edge in edge_list:
                edge_ctr += 1
                if edge_ctr % 1000000 == 0:
                    print(f"Processing edge {str(edge_ctr)} of {str(num_edges)}")
                temp_edge = {}
                for key, val in edge.items():
                    if key in edge_set:
                        temp_edge[key] = val
                reduced["edges"].append(temp_edge)
        print("Edges completed")

    kg2_util.save_json(reduced, args.outputFilepath, test_mode)
