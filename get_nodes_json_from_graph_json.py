#!/usr/bin/python3

'''Extracts the nodes from a knowledge graph that is in JSON format; saves the nodes in JSON format.

   Usage: get_nodes_json_from_graph_json.py <inputFile.json> <outputFile.json>
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import json
import tempfile
import argparse
import shutil


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='build-kg2: builds the KG2 knowledge graph for the RTX system')
    arg_parser.add_argument('inputFile', type=str, nargs=1)
    arg_parser.add_argument('outputFile', type=str, nargs=1)
    return arg_parser


if __name__ == "__main__":
    args = make_arg_parser().parse_args()
    temp_file = tempfile.mkstemp(prefix="kg2nodes")[1]
    graph = json.load(open(args.inputFile, 'r'))
    json.dump(graph['nodes'], open(temp_file, 'w'), indent=4, sort_keys=True)
    shutil.move(temp_file, args.outputFile)
