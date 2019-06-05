#!/usr/bin/env python3

'''Prints a JSON overview report of a JSON knowledge graph in Biolink format, to STDOUT.

   Usage: report_stats_on_kg.py <inputKGFile.json> <outputKGFile.json>
   The input file can be optionally gzipped (specify with the .gz extension).
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
import gzip
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

def count_predicates_by_predicate_curie_prefix(edges: list):
    unique_relation_curies = set([edge['relation curie'] for edge in edges])
    return collections.Counter([get_prefix_from_curie_id(curie) for curie in unique_relation_curies])

def count_types_of_pairs_of_curies_for_xrefs(edges: list):
    prefix_pairs_list = list()
    for edge in edges:
        if edge['type'] == 'xref':
            subject_curie = edge['subject']
            subject_prefix = get_prefix_from_curie_id(subject_curie)
            object_curie = edge['object']
            object_prefix = get_prefix_from_curie_id(object_curie)
            key = subject_prefix + '---' + object_prefix
            prefix_pairs_list.append(key)
    return collections.Counter(prefix_pairs_list)


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_file_name = args.inputFile[0]
    if not input_file_name.endswith('.gz'):
        input_file = open(input_file_name, 'r')
        graph = json.load(input_file)
    else:
        input_file = gzip.GzipFile(input_file_name, 'r')
        graph = json.loads(input_file.read().decode('utf-8'))
    stats = {'number_of_nodes': len(graph['nodes']),
             'number_of_edges': len(graph['edges']),
             'number_of_nodes_by_curie_prefix': dict(count_nodes_by_curie_prefix(graph['nodes'])),
             'number_of_nodes_without_category__by_curie_prefix': dict(count_nodes_by_curie_prefix_given_no_category(graph['nodes'])),
             'number_of_nodes_by_category_label': dict(count_nodes_by_category(graph['nodes'])),
             'number_of_nodes_by_source': dict(count_nodes_by_source(graph['nodes'])),
             'number_of_edges_by_predicate_curie': dict(count_edges_by_predicate_curie(graph['edges'])),
             'number_of_edges_by_predicate_type': dict(count_edges_by_predicate_type(graph['edges'])),
             'number_of_edges_by_predicate_curie_prefixes': dict(count_edges_by_predicate_curie_prefix(graph['edges'])),
             'number_of_predicates_by_predicate_curie_prefixes': dict(count_predicates_by_predicate_curie_prefix(graph['edges'])),
             'number_of_edges_by_source': dict(count_edges_by_source(graph['edges'])),
             'xref_node_curie_prefix_pair_counts': dict(count_types_of_pairs_of_curies_for_xrefs(graph['edges']))}
    temp_output_file = tempfile.mkstemp(prefix='kg2-')[1]
    with open(temp_output_file, 'w') as outfile:
        json.dump(stats, outfile, indent=4, sort_keys=True)
    shutil.move(temp_output_file, args.outputFile[0])
