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


def get_edge_stats(edges_file_name: list):
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    source_key = 'primary_knowledge_source'
    excluded_key = 'domain_range_exclusion'
    relation_label_key = 'relation_label'
    subject_key = 'subject'
    object_key = 'object'
    predicate_curie_key = 'source_predicate' if not args.use_simplified_predicates else 'predicate'
    label_key = 'relation_label' if not args.use_simplified_predicates else 'predicate'

    edge_count = 0
    edge_sources = dict()
    edges_by_predicate_curie = dict()
    edges_by_predicate_type = dict()
    edges_by_predicate_curie_prefix = dict()
    unique_relation_curies = set()
    prefix_pairs_dict_for_xrefs = dict()
    prefix_pairs_dict_for_equivs = dict()
    excluded_edges = dict()
    nodes_on_edges = set()

    for edge in edges:
        edge_count += 1

        source = edge[source_key]
        excluded = edge[excluded_key]
        relation_label = edge[relation_label_key]
        subject_curie = edge[subject_key]
        subject_prefix = get_prefix_from_curie_id(subject_curie)
        object_curie = edge[object_key]
        object_prefix = get_prefix_from_curie_id(object_curie)
        predicate_curie = edge[predicate_curie_key]
        predicate_curie_prefix = get_prefix_from_curie_id(predicate_curie)
        label = edge[label_key]

        if source not in edge_sources:
            edge_sources[source] = 0
        edge_sources[source] += 1

        if predicate_curie not in edges_by_predicate_curie:
            edges_by_predicate_curie[predicate_curie] = 0
        edges_by_predicate_curie[predicate_curie] += 1

        if label not in edges_by_predicate_type:
            edges_by_predicate_type[label] = 0
        edges_by_predicate_type[label] += 1

        if predicate_curie_prefix not in edges_by_predicate_curie_prefix:
            edges_by_predicate_curie_prefix[predicate_curie_prefix] = 0
        edges_by_predicate_curie_prefix[predicate_curie_prefix] += 1

        unique_relation_curies.add(predicate_curie)

        if edge['relation_label'] == 'xref' or edge['relation_label'] == 'close_match':
            key = subject_prefix + '---' + object_prefix
            if key not in prefix_pairs_dict_for_xrefs:
                prefix_pairs_dict_for_xrefs[key] = 0
            prefix_pairs_dict_for_xrefs[key] += 1

        if relation_label == kg2_util.EDGE_LABEL_OWL_SAME_AS:
            key = subject_prefix + '---' + object_prefix
            if key not in prefix_pairs_dict_for_equivs:
                prefix_pairs_dict_for_equivs[key] = 0
            prefix_pairs_dict_for_equivs[key] += 1

        if excluded:
            if source not in excluded_edges:
                excluded_edges[source] = 0
            excluded_edges[source] += 1

        nodes_on_edges.add(edge.get('subject', ""))
        nodes_on_edges.add(edge.get('object', ""))

    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    predicate_by_predicate_curie_prefix = dict(collections.Counter([get_prefix_from_curie_id(curie) for curie in unique_relation_curies]))

    edges_report = {'_number_of_edges': edge_count,
                    'number_of_edges_by_predicate_curie': edges_by_predicate_curie,
                    'number_of_edges_by_predicate_type': edges_by_predicate_type,
                    'number_of_edges_by_predicate_curie_prefixes': edges_by_predicate_curie_prefix,
                    'number_of_predicates_by_predicate_curie_prefixes': predicate_by_predicate_curie_prefix,
                    'number_of_edges_by_source': edge_sources,
                    'types_of_pairs_of_curies_for_xrefs': prefix_pairs_dict_for_xrefs,
                    'types_of_pairs_of_curies_for_equivs': prefix_pairs_dict_for_equivs,
                    'number_of_excluded_edges': excluded_edges}

    return edges_report, nodes_on_edges


def get_node_stats(nodes_file_name: list, nodes_on_edges: set):
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]

    category_label_key = 'category_label'
    id_key = 'id'
    source_key = 'provided_by'
    name_key = 'name'
    category_key = 'category'
    deprecated_key = 'deprecated'

    source_node_category = kg2_util.convert_biolink_category_to_curie(kg2_util.SOURCE_NODE_CATEGORY)

    node_count = 0
    build_info = dict()
    nodes_by_curie_prefix = dict()
    nodes_by_curie_prefix_given_no_category = dict()
    nodes_by_category = dict()
    nodes_by_source = dict()
    nodes_by_source_and_category = dict()
    sources = list()
    deprecated_nodes = dict()
    orphan_nodes = dict()

    for node in nodes:
        node_count += 1
        category_label = node[category_label_key]
        node_id = node[id_key]
        curie_prefix = get_prefix_from_curie_id(node_id)
        source = node[source_key][0]
        name = node[name_key]
        category = node[category_key]
        deprecated = node[deprecated_key]

        if curie_prefix not in nodes_by_curie_prefix:
            nodes_by_curie_prefix[curie_prefix] = 0
        nodes_by_curie_prefix[curie_prefix] += 1

        if category_label is None or category_label == 'unknown category':
            if curie_prefix not in nodes_by_curie_prefix_given_no_category:
                nodes_by_curie_prefix_given_no_category[curie_prefix] = 0
            nodes_by_curie_prefix_given_no_category[curie_prefix] += 1

        if category_label not in nodes_by_category:
            nodes_by_category[category_label] = 0
        nodes_by_category[category_label] += 1

        for multi_source in node[source_key]:
            if multi_source not in nodes_by_source:
                nodes_by_source[multi_source] = 0
            nodes_by_source[multi_source] += 1

            if not args.use_simplified_predicates:
                break

        if source not in nodes_by_source_and_category:
            nodes_by_source_and_category[source] = dict()
        if category_label not in nodes_by_source_and_category[source]:
            nodes_by_source_and_category[source][category_label] = 0
        nodes_by_source_and_category[source][category_label] += 1

        if category == source_node_category:
            sources.append(name)

        if deprecated:
            if source not in deprecated_nodes:
                deprecated_nodes[source] = 0
            deprecated_nodes[source] += 1

        if node_id not in nodes_on_edges:
            if source not in orphan_nodes:
                orphan_nodes[source] = 0
            orphan_nodes[source] += 1

        if node_id == kg2_util.CURIE_PREFIX_RTX + ':' + 'KG2':
            build_info = node

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    if len(build_info) == 0:
        print("WARNING: 'build' property is missing from the input JSON.", file=sys.stderr)

    nodes_report = {'_number_of_nodes': node_count,
                    '_build_version': build_info.get('version', ""),
                    '_build_time': build_info.get('timestamp_utc', ""),
                    'number_of_nodes_by_curie_prefix': nodes_by_curie_prefix,
                    'number_of_nodes_without_category_by_curie_prefix': nodes_by_curie_prefix_given_no_category,
                    'number_of_nodes_by_category_label': nodes_by_category,
                    'number_of_nodes_by_source': nodes_by_source,
                    'number_of_nodes_by_source_and_category': nodes_by_source_and_category,
                    'sources': sources,
                    'number_of_deprecated_nodes': deprecated_nodes,
                    'number_of_orphan_nodes': orphan_nodes}

    return nodes_report

if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_nodes_file_name = args.inputNodesFile
    input_edges_file_name = args.inputEdgesFile

    stats = {'_report_datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    edges_report, nodes_on_edges = get_edge_stats(input_edges_file_name)
    nodes_report = get_node_stats(input_nodes_file_name, nodes_on_edges)

    stats.update(edges_report)
    stats.update(nodes_report)

    kg2_util.save_json(stats, args.outputFile, True)
