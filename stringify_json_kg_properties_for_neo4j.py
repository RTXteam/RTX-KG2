#!/usr/bin/env python3
'''stringify_json_kg_properties_for_neo4j.py: Convert list or dictionary fields of a JSON KG into string format, for neo4j import

   Usage: stringify_json_kg_properties_for_neo4j.py [--test] --inputFile <inputFile.json> --outputFile <outputFile.json>
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


def get_args():
    arg_parser = argparse.ArgumentParser(description='stringify_json_kg_properties_for_neo4j.py: Convert list or dictionary fields of a JSON KG into string format, for neo4j import')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('--inputFile', type=str, nargs=1)
    arg_parser.add_argument('--outputFile', type=str, nargs=1)
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    input_file_name = args.inputFile[0]
    output_file_name = args.outputFile[0]
    test_mode = args.test
    graph = kg2_util.load_json(input_file_name)
    # ------ SAR:  save for now ------
    # node_properties_to_convert = ['publications', 'synonym']
    # for node in graph['nodes']:
    #     for property_name in node_properties_to_convert:
    #         node[property_name] = json.dumps(node[property_name])
    # ------ SAR:  save for now ------
    edge_properties_to_convert = ['publications info']
    for edge in graph['edges']:
        for property_name in edge_properties_to_convert:
            edge[property_name] = json.dumps(edge[property_name])
    kg2_util.save_json(graph, output_file_name, test_mode)
