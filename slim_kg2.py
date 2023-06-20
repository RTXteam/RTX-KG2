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
import datetime


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description=" slim_kg2.py: reduce graph in KG2 JSON format to only bare-bones node and edge properties.")
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument("inputFilepath", type=str)
    arg_parser.add_argument("outputFilepath", type=str)
    return arg_parser


if __name__ == "__main__":
    node_set = set(["name", "id", "full_name", "category", "provided_by"])
    edge_set = set(["core_predicate", "subject", "object", "predicate_label", 
"primary_knowledge_source"])

    args = make_arg_parser().parse_args()
    test_mode = args.test
    reduced = {"nodes": [], "edges": []}
    start = datetime.datetime.now()
    print(f"Start time: {start}")
    
    with open(args.inputFilepath, "r") as fp:

        node_ctr = 0
        edge_ctr = 0
        generator = (row for row in ijson.kvitems(fp, ""))

        for row in generator:
            key = row[0]
            data = row[1]
            if key == "build":
                reduced["build"] = data
                print(data)
            elif key == "nodes":  # handling the list of all nodes
                for node in data:  # handling a single node dict
                    node_ctr += 1
                    if node_ctr % 1000000 == 0:
                        print(node_ctr)
                    temp_node = {}
                    for k, v in node.items():  # iterating over the node's items
                        if k in node_set:
                            temp_node[k] = v
                    reduced["nodes"].append(temp_node)
                print("Nodes completed")
            elif key == "edges":
                for edge in data:
                    edge_ctr += 1
                    if edge_ctr % 1000000 == 0:
                        print(edge_ctr)
                    temp_edge = {}
                    for k, v in edge.items():
                        if k in edge_set:
                            temp_edge[k] = v
                    reduced["edges"].append(temp_edge)
                print("Edges completed")

    finish = datetime.datetime.now()
    print(f"Finish time: {finish} \nTotal time: {finish-start}")

    kg2_util.save_json(reduced, args.outputFilepath, test_mode)
