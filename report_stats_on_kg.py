#!/usr/bin/env python3

'''Prints a JSON overview report of a JSON knowledge graph in Biolink format, to STDOUT.

   Usage: report_stats_on_kg.py <inputKGFile.json> <outputKGFile.json>
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
import collections
import json
import shutil
import tempfile


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='build-kg2: builds the KG2 knowledge graph for the RTX system')
    arg_parser.add_argument('inputFile', type=str, nargs=1)
    arg_parser.add_argument('outputFile', type=str, nargs=1)
    return arg_parser


def get_prefix_from_curie_id(curie_id: str):
    assert ':' in curie_id
    return curie_id.split(':')[0]


def get_nodes_with_none_category(nodes: list):
    return [node for node in nodes if
            node['category label'] is None or node['category label'] == 'unknown category']


def count_nodes_by_curie_prefix(nodes: list):
    return collections.Counter([get_prefix_from_curie_id(node['id']) for node in nodes])


def count_nodes_by_curie_prefix_given_no_category(nodes: list):
    return count_nodes_by_curie_prefix(get_nodes_with_none_category(nodes))


def count_nodes_by_category(nodes: list):
    return collections.Counter([node['category label'] for node in nodes])


def count_nodes_by_source(nodes: list):
    return collections.Counter([node['provided by'] for node in nodes])


def count_edges_by_source(edges: list):
    return collections.Counter([edge['provided by'] for edge in edges])


def count_edges_by_predicate_curie(edges: list):
    return collections.Counter([edge['relation curie'] for edge in edges])


def count_edges_by_predicate_type(edges: list):
    return collections.Counter([edge['type'] for edge in edges])


def count_edges_by_predicate_curie_prefix(edges: list):
    return collections.Counter([get_prefix_from_curie_id(edge['relation curie']) for edge in edges])


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    graph = json.load(open(args.inputFile[0], 'r'))
    stats = {'num_nodes': len(graph['nodes']),
             'num_edges': len(graph['edges']),
             'node_curie_prefixes': dict(count_nodes_by_curie_prefix(graph['nodes'])),
             'node_curie_prefixes_for_nodes_without_category': dict(count_nodes_by_curie_prefix_given_no_category(graph['nodes'])),
             'node_category_types': dict(count_nodes_by_category(graph['nodes'])),
             'node_source_types': dict(count_nodes_by_source(graph['nodes'])),
             'edge_predicate_curies': dict(count_edges_by_predicate_curie(graph['edges'])),
             'edge_predicate_types': dict(count_edges_by_predicate_type(graph['edges'])),
             'edge_predicate_curie_prefixes': dict(count_edges_by_predicate_curie_prefix(graph['edges'])),
             'edge_sources': dict(count_edges_by_source(graph['edges']))}
    temp_output_file = tempfile.mkstemp(prefix='kg2-')[1]
    with open(temp_output_file, 'w') as outfile:
        json.dump(stats, outfile, indent=4, sort_keys=True)
    shutil.move(temp_output_file, args.outputFile[0])
