#!/usr/bin/env python3

'''Provides a JSON overview report of a JSON knowledge graph in Biolink format.

   Usage: report_stats_on_json_kg.py [--useSimplifiedPredicates] <inputNodesFile.jsonl> <inputEdgesFile.jsonl> <outputFile.json>
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
import sys
import jsonlines


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='build-kg2: builds the KG2 knowledge graph for the RTX system')
    arg_parser.add_argument('inputNodesFile', type=str)
    arg_parser.add_argument('inputEdgesFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    arg_parser.add_argument('--useSimplifiedPredicates', dest='use_simplified_predicates', action='store_true', default=False)
    return arg_parser


def get_prefix_from_curie_id(curie_id: str):
    """
    :param curie_id: This parameter is the node id that we need to get the prefix from
    """
    assert ':' in curie_id
    
    return curie_id.split(':')[0]


def get_edge_stats(edges_file_name: list):
    """
    :param edges_file_name: This parameter refers to the edges file name that we can get all of the edges from
    """
    # Initialize edges reader
    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(edges_file_name)
    edges = edges_read_jsonlines_info[0]

    # Pick which edge keys we want to access now, especially with questions of simiplified predicates
    source_key = 'primary_knowledge_source'
    excluded_key = 'domain_range_exclusion'
    relation_label_key = 'relation_label'
    subject_key = 'subject'
    object_key = 'object'
    predicate_curie_key = 'source_predicate' if not args.use_simplified_predicates else 'predicate'
    label_key = 'relation_label' if not args.use_simplified_predicates else 'predicate_label'

    # Initialize our output data
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

    # We only have one pass through all of the edges, so we have to get all of the data we want in that one pass
    for edge in edges:
        # Formerly under _number_of_edges
        edge_count += 1

        # Gather all of the data we need from each edge at the start so it can be easily applied to multiple metrics
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

        # Formerly count_edges_by_source()
        if source not in edge_sources:
            edge_sources[source] = 0
        edge_sources[source] += 1

        # Formerly count_edges_by_predicate_curie()
        if predicate_curie not in edges_by_predicate_curie:
            edges_by_predicate_curie[predicate_curie] = 0
        edges_by_predicate_curie[predicate_curie] += 1

        # Formerly count_edges_by_predicate_type()
        if label not in edges_by_predicate_type:
            edges_by_predicate_type[label] = 0
        edges_by_predicate_type[label] += 1

        # Formerly count_edges_by_predicate_curie_prefix()
        if predicate_curie_prefix not in edges_by_predicate_curie_prefix:
            edges_by_predicate_curie_prefix[predicate_curie_prefix] = 0
        edges_by_predicate_curie_prefix[predicate_curie_prefix] += 1

        # Formerly part of count_predicates_by_predicate_curie_prefix()
        # The rest must be done after all edges have been processed
        unique_relation_curies.add(predicate_curie)

        # Formerly count_types_of_pairs_of_curies_for_xrefs()
        if edge['relation_label'] == 'xref' or edge['relation_label'] == 'close_match':
            key = subject_prefix + '---' + object_prefix
            if key not in prefix_pairs_dict_for_xrefs:
                prefix_pairs_dict_for_xrefs[key] = 0
            prefix_pairs_dict_for_xrefs[key] += 1

        # Formerly count_types_of_pairs_of_curies_for_equivs()
        if relation_label == kg2_util.EDGE_LABEL_OWL_SAME_AS:
            key = subject_prefix + '---' + object_prefix
            if key not in prefix_pairs_dict_for_equivs:
                prefix_pairs_dict_for_equivs[key] = 0
            prefix_pairs_dict_for_equivs[key] += 1

        # Formerly get_excluded_edges()
        if excluded:
            if source not in excluded_edges:
                excluded_edges[source] = 0
            excluded_edges[source] += 1

        # Formerly part of count_orphan_nodes(); needs to process nodes for second part
        nodes_on_edges.add(edge.get('subject', ""))
        nodes_on_edges.add(edge.get('object', ""))

    # Close our reader since we have finished
    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)

    # Formerly part of count_predicates_by_predicate_curie_prefix()
    predicate_by_predicate_curie_prefix = dict(collections.Counter([get_prefix_from_curie_id(curie) for curie in unique_relation_curies]))

    # Save the data in dictionary form
    edges_report = {'_number_of_edges': edge_count,
                    'number_of_edges_by_predicate_curie': edges_by_predicate_curie,
                    'number_of_edges_by_predicate_type': edges_by_predicate_type,
                    'number_of_edges_by_predicate_curie_prefixes': edges_by_predicate_curie_prefix,
                    'number_of_predicates_by_predicate_curie_prefixes': predicate_by_predicate_curie_prefix,
                    'number_of_edges_by_source': edge_sources,
                    'types_of_pairs_of_curies_for_xrefs': prefix_pairs_dict_for_xrefs,
                    'types_of_pairs_of_curies_for_equivs': prefix_pairs_dict_for_equivs,
                    'number_of_excluded_edges': excluded_edges}

    # Return the dictionary report and the set of all nodes on edges
    return edges_report, nodes_on_edges


def get_node_stats(nodes_file_name: list, nodes_on_edges: set):
    """
    :param nodes_file_name: This parameter refers to the nodes file name that we can get all of the nodes from
    :param nodes_on_edges: This parameter provides a set containing all of the node ids that are on edges
    """
    # Initialize nodes reader
    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]

    # Pick which node keys we want to access now
    category_label_key = 'category_label'
    id_key = 'id'
    source_key = 'provided_by'
    name_key = 'name'
    category_key = 'category'
    deprecated_key = 'deprecated'

    source_node_category = kg2_util.convert_biolink_category_to_curie(kg2_util.SOURCE_NODE_CATEGORY)

    # Initialize our output data
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

    # We only have one pass through all of the nodes, so we have to get all of the data we want in that one pass
    for node in nodes:
        # Formerly under _number_of_nodes
        node_count += 1

        # Gather all of the data we need from each node at the start so it can be easily applied to multiple metrics
        category_label = node[category_label_key]
        node_id = node[id_key]
        curie_prefix = get_prefix_from_curie_id(node_id)
        source = node[source_key][0]
        name = node[name_key]
        category = node[category_key]
        deprecated = node[deprecated_key]

        # Formerly _build_version and _build_time
        if node_id == kg2_util.CURIE_PREFIX_RTX + ':' + 'KG2':
            build_info = node
            continue

        # Formerly count_nodes_by_curie_prefix()
        if curie_prefix not in nodes_by_curie_prefix:
            nodes_by_curie_prefix[curie_prefix] = 0
        nodes_by_curie_prefix[curie_prefix] += 1

        # Formerly count_nodes_by_curie_prefix_given_no_category()
        if category_label is None or category_label == 'unknown category':
            if curie_prefix not in nodes_by_curie_prefix_given_no_category:
                nodes_by_curie_prefix_given_no_category[curie_prefix] = 0
            nodes_by_curie_prefix_given_no_category[curie_prefix] += 1

        # Formerly count_nodes_by_category()
        if category_label not in nodes_by_category:
            nodes_by_category[category_label] = 0
        nodes_by_category[category_label] += 1

        # Formerly count_nodes_by_source()
        for multi_source in node[source_key]:
            if multi_source not in nodes_by_source:
                nodes_by_source[multi_source] = 0
            nodes_by_source[multi_source] += 1

            if not args.use_simplified_predicates:
                break

        # Formerly count_number_of_nodes_by_source_and_category()
        if source not in nodes_by_source_and_category:
            nodes_by_source_and_category[source] = dict()
        if category_label not in nodes_by_source_and_category[source]:
            nodes_by_source_and_category[source][category_label] = 0
        nodes_by_source_and_category[source][category_label] += 1

        # Formerly get_sources()
        if category == source_node_category:
            sources.append(name)

        # Formerly get_deprecated_nodes()
        if deprecated:
            if source not in deprecated_nodes:
                deprecated_nodes[source] = 0
            deprecated_nodes[source] += 1

        # Formerly part of count_orphan_nodes()
        if node_id not in nodes_on_edges:
            if source not in orphan_nodes:
                orphan_nodes[source] = 0
            orphan_nodes[source] += 1

    # Close our reader since we have finished
    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    if len(build_info) == 0:
        print("WARNING: 'build' property is missing from the input JSON.", file=sys.stderr)

    # Save the data in dictionary form
    nodes_report = {'_number_of_nodes': node_count,
                    '_build_version': build_info.get('name', ""),
                    '_build_time': build_info.get('update_date', ""),
                    'number_of_nodes_by_curie_prefix': nodes_by_curie_prefix,
                    'number_of_nodes_without_category_by_curie_prefix': nodes_by_curie_prefix_given_no_category,
                    'number_of_nodes_by_category_label': nodes_by_category,
                    'number_of_nodes_by_source': nodes_by_source,
                    'number_of_nodes_by_source_and_category': nodes_by_source_and_category,
                    'sources': sources,
                    'number_of_deprecated_nodes': deprecated_nodes,
                    'number_of_orphan_nodes': orphan_nodes}

    # Return the dictionary report
    return nodes_report

if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_nodes_file_name = args.inputNodesFile
    input_edges_file_name = args.inputEdgesFile

    stats = {'_report_datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    # Get stats from the edges first (since we need the set of nodes on edges), then nodes
    edges_report, nodes_on_edges = get_edge_stats(input_edges_file_name)
    nodes_report = get_node_stats(input_nodes_file_name, nodes_on_edges)

    # Add the output of get_edge_stats() and get_node_stats() to the return dictionary
    stats.update(edges_report)
    stats.update(nodes_report)

    # Save our output dictionary to the output file
    kg2_util.save_json(stats, args.outputFile, True)
