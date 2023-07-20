#!/usr/bin/env python3

'''Prints a JSON overview report of a JSON knowledge graph in Biolink format, to STDOUT.

   Usage: report_stats_on_json_kg.py [--useSimplifiedPredicates] <inputNodesFile.json> <inputEdgesFile.json> <outputFile.json>
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
import jsonlines


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='build-kg2: builds the KG2 knowledge graph for the RTX system')
    arg_parser.add_argument('inputNodesFile', type=str)
    arg_parser.add_argument('inputEdgesFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    arg_parser.add_argument('--useSimplifiedPredicates', dest='use_simplified_predicates', action='store_true', default=False)
    return arg_parser


def get_prefix_from_curie_id(curie_id: str):
    assert ':' in curie_id
    
    return curie_id.split(':')[0]


def get_nodes_with_none_category(nodes: list):
    return [node for node in nodes if
            node['category_label'] is None or node['category_label'] == 'unknown category']


def count_nodes_by_curie_prefix(nodes_file_name: list):
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]

    nodes_by_curie_prefix = dict(collections.Counter([get_prefix_from_curie_id(node['id']) for node in nodes]))

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    return nodes_by_curie_prefix


def count_nodes_by_curie_prefix_given_no_category(nodes_file_name: list):
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]

    nodes_by_curie_prefix_given_no_category = dict(collections.Counter([get_prefix_from_curie_id(node['id']) for node in get_nodes_with_none_category(nodes)]))

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    return nodes_by_curie_prefix_given_no_category


def count_nodes_by_category(nodes_file_name: list):
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]

    nodes_by_category = dict(collections.Counter([node['category_label'] for node in nodes]))

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    return nodes_by_category


def count_nodes_by_source(nodes_file_name: list):
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]

    label_field = 'provided_by'

    ret_data = dict()
    if args.use_simplified_predicates:
        provided_by_list = []
        for node in nodes:
            provided_by_list += node['provided_by']
        ret_data = dict(collections.Counter(provided_by_list))
    else:
        ret_data = dict(collections.Counter([node[label_field][0] for node in nodes]))

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    return ret_data


def count_number_of_nodes_by_source_and_category(nodes_file_name: list):
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]

    fulldict = dict()
    provided_by_label = 'provided_by'
    category_label = 'category_label'

    for node in nodes:
        source = node[provided_by_label][0]
        category = node[category_label]
        if source not in fulldict:
            fulldict[source] = dict()
        if category not in fulldict[source]:
            fulldict[source][category] = 0
        fulldict[source][category] += 1

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    return fulldict


def count_edges_by_source(edges_file_name: list):
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    ret_data = None
    
    ret_data = dict(collections.Counter([edge.get('primary_knowledge_source') for edge in edges]))

    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    return ret_data


def count_edges_by_predicate_curie(edges_file_name: list):
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    curie_field = 'source_predicate' if not args.use_simplified_predicates else 'predicate'
    # Every simplified edge should have a predicate. 
    edges_by_predicate_curie = dict(collections.Counter([edge.get(curie_field) for edge in edges]))

    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    return edges_by_predicate_curie
   

def count_edges_by_predicate_type(edges_file_name: list):
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    label_field = 'relation_label' if not args.use_simplified_predicates else 'predicate_label'
    edges_by_predicate_type = dict(collections.Counter([edge[label_field] for edge in edges]))

    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    return edges_by_predicate_type


def count_edges_by_predicate_curie_prefix(edges_file_name: list):
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    curie_field = 'source_predicate' if not args.use_simplified_predicates else 'predicate'
    edges_by_predicate_curie_prefix = dict(collections.Counter([get_prefix_from_curie_id(edge.get(curie_field)) for edge in edges]))

    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    return edges_by_predicate_curie_prefix


def count_predicates_by_predicate_curie_prefix(edges_file_name: list):
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    curie_field = 'source_predicate' if not args.use_simplified_predicates else 'predicate'
    unique_relation_curies = set([edge.get(curie_field) for edge in edges])

    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    return dict(collections.Counter([get_prefix_from_curie_id(curie) for curie in unique_relation_curies]))


def count_types_of_pairs_of_curies_for_xrefs(edges_file_name: list):
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    prefix_pairs_list = list()
    for edge in edges:
        if edge['relation_label'] == 'xref' or edge['relation_label'] == 'close_match':
            subject_curie = edge['subject']
            subject_prefix = get_prefix_from_curie_id(subject_curie)
            object_curie = edge['object']
            object_prefix = get_prefix_from_curie_id(object_curie)
            key = subject_prefix + '---' + object_prefix
            prefix_pairs_list.append(key)

    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    return dict(collections.Counter(prefix_pairs_list))


def count_types_of_pairs_of_curies_for_equivs(edges_file_name: list):
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    prefix_pairs_list = list()
    for edge in edges:
        if edge['relation_label'] == kg2_util.EDGE_LABEL_OWL_SAME_AS:
            subject_curie = edge['subject']
            subject_prefix = get_prefix_from_curie_id(subject_curie)
            object_curie = edge['object']
            object_prefix = get_prefix_from_curie_id(object_curie)
            key = subject_prefix + '---' + object_prefix
            prefix_pairs_list.append(key)

    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    return dict(collections.Counter(prefix_pairs_list))

def get_sources(nodes_file_name: list):
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]

    sources = [node.get('name') for node in nodes if node.get('category') == kg2_util.convert_biolink_category_to_curie(kg2_util.SOURCE_NODE_CATEGORY)]

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    return sources

def get_deprecated_nodes(nodes_file_name: list):
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]

    deprecated_nodes = dict()
    provided_by_label = 'provided_by'
    deprecated_label = 'deprecated'

    for node in nodes:
        source = node[provided_by_label][0]
        deprecated = node[deprecated_label]

        if deprecated:
            if source not in deprecated_nodes:
                deprecated_nodes[source] = 0
            deprecated_nodes[source] += 1

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    return deprecated_nodes


def get_excluded_edges(edges_file_name: list):
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    excluded_edges = dict()
    provided_by_label = 'primary_knowledge_source'
    excluded_label = 'domain_range_exclusion'

    for edge in edges:
        source = edge[provided_by_label]
        excluded = edge[excluded_label]

        if excluded:
            if source not in excluded_edges:
                excluded_edges[source] = 0
            excluded_edges[source] += 1

    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    return excluded_edges


def count_orphan_nodes(nodes_file_name: list, edges_file_name: list):
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]

    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    orphan_nodes = dict()
    provided_by_label = 'provided_by'

    nodes_on_edges = set()

    for edge in edges:
        nodes_on_edges.add(edge.get('subject', ""))
        nodes_on_edges.add(edge.get('object', ""))

    for node in nodes:
        source = node[provided_by_label][0]
        if node.get('id', "") not in nodes_on_edges:
            if source not in orphan_nodes:
                orphan_nodes[source] = 0
            orphan_nodes[source] += 1

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)
    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    return orphan_nodes


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_nodes_file_name = args.inputNodesFile
    input_edges_file_name = args.inputEdgesFile
        
    build_info = dict()

    number_of_nodes = 0
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(input_nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]
    for node in nodes:
        number_of_nodes += 1
        if node["id"] == kg2_util.CURIE_PREFIX_RTX + ':' + 'KG2':
            build_info = node
    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    if len(build_info) == 0:
        print("WARNING: 'build' property is missing from the input JSON.", file=sys.stderr)

    number_of_edges = 0
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(input_edges_file_name)
    edges = edges_read_jsonlines_info[0]
    for edge in edges:
        number_of_edges += 1
    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    stats = {'_number_of_nodes': number_of_nodes,   # underscore is to make sure it sorts to the top of the report
             '_number_of_edges': number_of_edges,   # underscore is to make sure it sorts to the top of the report
             '_report_datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             '_build_version': build_info.get('version', ""),
             '_build_time': build_info.get('timestamp_utc', ""),
             'number_of_nodes_by_curie_prefix': count_nodes_by_curie_prefix(input_nodes_file_name),
             'number_of_nodes_without_category__by_curie_prefix': count_nodes_by_curie_prefix_given_no_category(input_nodes_file_name),
             'number_of_nodes_by_category_label': count_nodes_by_category(input_nodes_file_name),
             'number_of_nodes_by_source': count_nodes_by_source(input_nodes_file_name),
             'number_of_edges_by_predicate_curie': count_edges_by_predicate_curie(input_edges_file_name),
             'number_of_edges_by_predicate_type': count_edges_by_predicate_type(input_edges_file_name),
             'number_of_edges_by_predicate_curie_prefixes': count_edges_by_predicate_curie_prefix(input_edges_file_name),
             'number_of_predicates_by_predicate_curie_prefixes': count_predicates_by_predicate_curie_prefix(input_edges_file_name),
             'number_of_edges_by_source': count_edges_by_source(input_edges_file_name),
             'types_of_pairs_of_curies_for_xrefs': count_types_of_pairs_of_curies_for_xrefs(input_edges_file_name),
             'types_of_pairs_of_curies_for_equivs': count_types_of_pairs_of_curies_for_equivs(input_edges_file_name),
             'number_of_nodes_by_source_and_category': count_number_of_nodes_by_source_and_category(input_nodes_file_name),
             'sources': get_sources(input_nodes_file_name),
             'number_of_deprecated_nodes': get_deprecated_nodes(input_nodes_file_name),
             'number_of_excluded_edges': get_excluded_edges(input_edges_file_name),
             'number_of_orphan_nodes': count_orphan_nodes(input_nodes_file_name, input_edges_file_name)}

    temp_output_file = tempfile.mkstemp(prefix='kg2-')[1]
    with open(temp_output_file, 'w') as outfile:
        json.dump(stats, outfile, indent=4)
    shutil.move(temp_output_file, args.outputFile)
