#!/usr/bin/env python3

'''Extracts the nodes from a knowledge graph that is in JSON format; saves the nodes in JSON format.

   Usage: get_nodes_json_from_graph_json.py <inputFile.json> <outputFile.json>
   Either the input file or the output file can optionally have a ".gz" extension.
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
import gzip
import json
import kg2_util
import tempfile


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='build-kg2: builds the KG2 knowledge graph for the RTX system')
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser


if __name__ == "__main__":
    args = make_arg_parser().parse_args()
    test_mode = args.test
    temp_file_name = tempfile.mkstemp(prefix="kg2-")[1]
    input_file_name = args.inputFile
    if not input_file_name.endswith('.gz'):
        input_file = open(input_file_name, 'r')
        graph = json.load(input_file)
    else:
        input_file = gzip.GzipFile(input_file_name, 'r')
        graph = json.loads(input_file.read().decode('utf-8'))
    del graph['edges']
    output_file_name = args.outputFile
    kg2_util.save_json(graph, output_file_name, test_mode)
