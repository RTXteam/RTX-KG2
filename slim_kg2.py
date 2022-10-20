#!/usr/bin/env python3
''' slim_kg2.py: reduce graph in KG2 JSON format to only bare-bones node and edge properties.
    Usage: slim_kg2.py <inputFile>
                         --outputFile <outputFile
'''
__author__ = 'Lindsey Kvarfordt'
__copyright__ = 'Oregon State University'
__credits__ = ['Lindsey Kvarfordt', 'Stephen Ramsey']
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


def tokenizer():
    # Write a tokenizer to handle chunks of a json stream
    pass


def stateMachine():
    # remember which part of the json object we're currently processing. 
    # Start of object -> Field Name -> Start of array -> start of object -> validate and save record
    pass


if __name__ == "__main__":
    node_set = set(["name", "id", "full_name", "category", "knowledge_source"])
    edge_set = set(["core_predicate", "subject", "object", "predicate_label", "knowledge_source"])

    args = make_arg_parser().parse_args()
    test_mode = args.test
    reduced = {"nodes": [], "edges": []}
    with open(args.inputFilepath, "r") as fp:
        
        # File is too big to use json.load()
        #all_data = json.load(fp)

        build = ijson.items(fp, 'build.item')
        print(f"{str(build)}")

    #     nodes = ijson.items(fp, 'nodes.item')


    #     reduced["build"] = all_data["build"]
    #     num_nodes = len(all_data["nodes"])
    #     node_ctr = 0
    #     for node in all_data["nodes"]:
    #         node_ctr += 1
    #         if node_ctr % 1000000 == 0:
    #             print(f"Processing node {str(node_ctr)} of {str(num_nodes)}")
    #         temp_node = {}
    #         for key, val in node.items():
    #             if key in node_set:
    #                 temp_node[key] = val
    #         reduced["nodes"].append(temp_node)
    #     print(f"Nodes completed")

    #     num_nodes = len(all_data["edges"])
    #     edge_ctr = 0
    #     num_edges = len(all_data["edges"])
    #     for edge in all_data["edges"]:
    #         edge_ctr += 0
    #         if edge_ctr % 1000000 ==0:
    #             print(f"Processing edge {str(edge_ctr)} of {str(num_edges)}")
    #         temp_edge = {}
    #         if edge_ctr < 5:
    #             print(f"Example edge: {edge}")
    #         for key, val in edge.items():
    #             if key in edge_set:
    #                 temp_edge[key] = val
    #             else:
    #                 print(f"Key {key} not in edge set")
    #         reduced["edges"].append(temp_edge)
    #     print(f"Edges completed")

    # kg2_util.save_json(reduced, args.outputFilepath, test_mode)
