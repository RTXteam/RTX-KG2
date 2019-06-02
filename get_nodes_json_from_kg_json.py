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

import gzip
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
    temp_file_name = tempfile.mkstemp(prefix="kg2-")[1]
    input_file_name = args.inputFile[0]
    if not input_file_name.endswith('.gz'):
        input_file = open(input_file_name, 'r')
        graph = json.load(input_file)
    else:
        input_file = gzip.GzipFile(input_file_name, 'r')
        graph = json.loads(input_file.read().decode('utf-8'))
    output_file_name = args.outputFile[0]
    if not output_file_name.endswith('.gz'):
        temp_file = open(temp_file_name, 'w')
        json.dump(graph['nodes'], temp_file, indent=4, sort_keys=True)
    else:
        temp_file = gzip.GzipFile(temp_file_name, 'w')
        temp_file.write(json.dumps(graph['nodes'], indent=4, sort_keys=True).encode('utf-8'))
    shutil.move(temp_file_name, output_file_name)

