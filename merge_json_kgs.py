#!/usr/bin/env python3
'''kg2_merge.py: merge two KGs that are in the KG2 JSON format

   Usage: kg2_merge.py [--test] --inputFiles <file1> <file2> ... <fileN> --outputFile <outputFile>
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
import json
import kg2_util


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='semmeddb_mysql_to_json.py: extracts all the predicate triples from SemMedDB, in the RTX KG2 JSON format')
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('--inputFiles', type=str, nargs='+')
    arg_parser.add_argument('--outputFile', type=str, nargs=1)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    nodes = {}
    edges = []
    for input_file_name in args.inputFiles:
        kg_file = open(input_file_name, 'r')
        input_kg = json.load(kg_file)
        for node in input_kg['nodes']:
            node_id = node['id']
            if node_id in nodes:
                nodes[node_id] = kg2_util.merge_two_dicts(nodes[node_id], node)
        edges += input_kg['edges']
    output_kg = {'nodes': [node for node in nodes.values()],
                 'edges': edges}
    output_file_name = args.outputFile[0]
    test_mode = args.test
    kg2_util.save_json(output_kg, output_file_name, test_mode)
