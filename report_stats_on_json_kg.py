#!/usr/bin/env python3

'''Prints a JSON overview report of a JSON knowledge graph in Biolink format, to STDOUT.

   Usage: report_stats_on_json_kg.py [--useSimplifiedPredicates] <inputKGFile.json> <outputKGFile.json>
   The input file can be optionally gzipped (specify with the .gz extension).
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood', 'Veronica Flores']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


import argparse
import collections
import datetime
import gzip
import json
import kg2_util
import shutil
import sys
import tempfile


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='build-kg2: builds the KG2 knowledge graph for the RTX system')
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    arg_parser.add_argument('--useSimplifiedPredicates', dest='use_simplified_predicates', action='store_true', default=False)
    return arg_parser


def get_prefix_from_curie_id(curie_id: str):
    assert ':' in curie_id
    return curie_id.split(':')[0]


def get_nodes_with_none_category(nodes: list):
    return [node for node in nodes if
            node['category_label'] is None or node['category_label'] == 'unknown category']


def count_nodes_by_curie_prefix(nodes: list):
    return collections.Counter([get_prefix_from_curie_id(node['id']) for node in nodes])


def count_nodes_by_curie_prefix_given_no_category(nodes: list):
    return count_nodes_by_curie_prefix(get_nodes_with_none_category(nodes))


def count_nodes_by_category(nodes: list):
    return collections.Counter([node['category_label'] for node in nodes])


def count_nodes_by_source(nodes: list):
    return collections.Counter([node['provided_by'] for node in nodes])


def count_number_of_nodes_by_source_and_category(nodes: list):
    fulldict = {}
    sourcedict = collections.Counter([node['provided_by'] for node in nodes])
    sourcecatdict = {}
    categorylist = []
    for source in sourcedict:
        categorylist = []
        for node in nodes:
            if node['provided_by'] == source:
                categorylist.append(node['category_label'])
        sourcecatdict.update({source: categorylist})
    for defintion in sourcecatdict:
        sourcecount = collections.Counter(sourcecatdict.get(defintion))
        fulldict.update({defintion: sourcecount})
    return fulldict


def count_edges_by_source(edges: list):
    ret_data = None
    if type(edges[0]['provided_by']) == str:
        ret_data = collections.Counter([edge['provided_by'] for edge in edges])
    else:
        assert type(edges[0]['provided_by'] == list)
        provby_list = []
        for edge in edges:
            provby_list += edge['provided_by']
        ret_data = collections.Counter(provby_list)
    return ret_data


def count_edges_by_predicate_curie(edges: list):
    curie_field = 'relation' if not args.use_simplified_predicates else 'predicate'
    return collections.Counter([edge[curie_field] for edge in edges])


def count_edges_by_predicate_type(edges: list):
    label_field = 'relation_label' if not args.use_simplified_predicates else 'predicate_label'
    return collections.Counter([edge[label_field] for edge in edges])


def count_edges_by_predicate_curie_prefix(edges: list):
    curie_field = 'relation' if not args.use_simplified_predicates else 'predicate'
    return collections.Counter([get_prefix_from_curie_id(edge[curie_field]) for edge in edges])


def count_predicates_by_predicate_curie_prefix(edges: list):
    curie_field = 'relation' if not args.use_simplified_predicates else 'predicate'
    unique_relation_curies = set([edge[curie_field] for edge in edges])
    return collections.Counter([get_prefix_from_curie_id(curie) for curie in unique_relation_curies])


def count_types_of_pairs_of_curies_for_xrefs(edges: list):
    prefix_pairs_list = list()
    for edge in edges:
        if edge['relation_label'] == 'xref' or edge['relation_label'] == 'close_match':
            subject_curie = edge['subject']
            subject_prefix = get_prefix_from_curie_id(subject_curie)
            object_curie = edge['object']
            object_prefix = get_prefix_from_curie_id(object_curie)
            key = subject_prefix + '---' + object_prefix
            prefix_pairs_list.append(key)
    return collections.Counter(prefix_pairs_list)


def count_types_of_pairs_of_curies_for_equivs(edges: list):
    prefix_pairs_list = list()
    for edge in edges:
        if edge['relation_label'] == kg2_util.EDGE_LABEL_OWL_SAME_AS:
            subject_curie = edge['subject']
            subject_prefix = get_prefix_from_curie_id(subject_curie)
            object_curie = edge['object']
            object_prefix = get_prefix_from_curie_id(object_curie)
            key = subject_prefix + '---' + object_prefix
            prefix_pairs_list.append(key)
    return collections.Counter(prefix_pairs_list)


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_file_name = args.inputFile
    if not input_file_name.endswith('.gz'):
        input_file = open(input_file_name, 'r')
        graph = json.load(input_file)
    else:
        input_file = gzip.GzipFile(input_file_name, 'r')
        graph = json.loads(input_file.read().decode('utf-8'))

    if 'nodes' not in graph:
        print("WARNING: 'nodes' property is missing from the input JSON.", file=sys.stderr)
    nodes = graph.get('nodes', [])
    nodes = graph.get('nodes', [])
    for n in nodes[::-1]:  # search for build info node starting at end
        if n["name"] == "KG2:Build":  # should be the first node accessed
            nodes.remove(n) # remove it so stats aren't reported
            break
    if 'edges' not in graph:
        print("WARNING: 'edges' property is missing from the input JSON.", file=sys.stderr)
    edges = graph.get('edges', [])

    stats = {'_number_of_nodes': len(nodes),   # underscore is to make sure it sorts to the top of the report
             '_number_of_edges': len(edges),   # underscore is to make sure it sorts to the top of the report
             '_report_datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             'number_of_nodes_by_curie_prefix': dict(count_nodes_by_curie_prefix(nodes)),
             'number_of_nodes_without_category__by_curie_prefix': dict(count_nodes_by_curie_prefix_given_no_category(nodes)),
             'number_of_nodes_by_category_label': dict(count_nodes_by_category(nodes)),
             'number_of_nodes_by_source': dict(count_nodes_by_source(nodes)),
             'number_of_edges_by_predicate_curie': dict(count_edges_by_predicate_curie(edges)),
             'number_of_edges_by_predicate_type': dict(count_edges_by_predicate_type(edges)),
             'number_of_edges_by_predicate_curie_prefixes': dict(count_edges_by_predicate_curie_prefix(edges)),
             'number_of_predicates_by_predicate_curie_prefixes': dict(count_predicates_by_predicate_curie_prefix(edges)),
             'number_of_edges_by_source': dict(count_edges_by_source(edges)),
             'types_of_pairs_of_curies_for_xrefs': dict(count_types_of_pairs_of_curies_for_xrefs(edges)),
             'types_of_pairs_of_curies_for_equivs': dict(count_types_of_pairs_of_curies_for_equivs(edges)),
             'number_of_nodes_by_source_and_category': dict(count_number_of_nodes_by_source_and_category(nodes))}

    temp_output_file = tempfile.mkstemp(prefix='kg2-')[1]
    with open(temp_output_file, 'w') as outfile:
        json.dump(stats, outfile, indent=4, sort_keys=True)
    shutil.move(temp_output_file, args.outputFile)
