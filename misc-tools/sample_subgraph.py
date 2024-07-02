#!/usr/bin/env python3
'''sample_subgraph.py: sample a random subgraph from a KG2 JSON graph, in JSON format

   Usage: run "sample_subgraph.py --help" to get usage information
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


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='sample_subgraph.py: sample a smaller subgraph of a KG in JSON format')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str, nargs=1)
    arg_parser.add_argument('outputFile', type=str, nargs=1)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_file_name = args.inputFile
    output_file_name = args.outputFile
    graph = kg2_util.load_json(input_file_name)
    nodes = [graph['nodes'][i] for i in range(0, len(graph['nodes']), 5)]
    nodes_id_set = set([node['id'] for node in nodes])
    edges = [edge for edge in graph['edges'] if edge['subject'] in nodes_id_set and edge['object'] in nodes_id_set]
    build = graph.get('build', None)
    out_graph = {'nodes': nodes, 'edges': edges}
    if build is not None:
        out_graph['build'] = build
    kg2_util.save_json(out_graph, output_file_name)
