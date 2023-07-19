#!/usr/bin/env python3

'''Prints a JSON overview report of a JSON knowledge graph in Biolink format, to STDOUT.

   Usage: report_stats_on_json_kg.py [--useSimplifiedPredicates] <inputNodesFile.json> <inputEdgesFile.json> <outputKGFile.json>
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


def count_nodes_by_curie_prefix(nodes: list):
    return collections.Counter([get_prefix_from_curie_id(node['id']) for node in nodes])


def count_nodes_by_curie_prefix_given_no_category(nodes: list):
    return count_nodes_by_curie_prefix(get_nodes_with_none_category(nodes))


def count_nodes_by_category(nodes: list):
    return collections.Counter([node['category_label'] for node in nodes])


def count_nodes_by_source(nodes: list):
    label_field = 'provided_by' 
    if args.use_simplified_predicates:
      provided_by_list = []
      for node in nodes:
         provided_by_list += node['provided_by']
      ret_data = collections.Counter(provided_by_list)
      return ret_data
    else:
      return collections.Counter([node[label_field][0] for node in nodes])


def count_number_of_nodes_by_source_and_category(nodes: list):
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
    return fulldict


def count_edges_by_source(edges: list):
    ret_data = None
    if type(edges[0]['primary_knowledge_source']) == str:
        #print(f"{edges[0]}")
        ret_data = collections.Counter([edge.get('primary_knowledge_source') for edge in edges])
    else:
        # primary knowledge source should be a string, we should not get here
        assert type(edges[0].get('primary_knowledge_source') == str), f"Problem with edges source type"
    return ret_data


def count_edges_by_predicate_curie(edges: list):
    curie_field = 'source_predicate' if not args.use_simplified_predicates else 'predicate'
    # Every simplified edge should have a predicate. 
    return collections.Counter([edge.get(curie_field) for edge in edges])
   

def count_edges_by_predicate_type(edges: list):
    label_field = 'relation_label' if not args.use_simplified_predicates else 'predicate_label'
    return collections.Counter([edge[label_field] for edge in edges])


def count_edges_by_predicate_curie_prefix(edges: list):
    curie_field = 'source_predicate' if not args.use_simplified_predicates else 'predicate'
    return collections.Counter([get_prefix_from_curie_id(edge.get(curie_field)) for edge in edges])


def count_predicates_by_predicate_curie_prefix(edges: list):
    curie_field = 'source_predicate' if not args.use_simplified_predicates else 'predicate'
    unique_relation_curies = set([edge.get(curie_field) for edge in edges])
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

def get_sources(nodes: list):
    return [node.get('name') for node in nodes if node.get('category') == kg2_util.convert_biolink_category_to_curie(kg2_util.SOURCE_NODE_CATEGORY)]

def get_deprecated_nodes(nodes: list):
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

    return deprecated_nodes


def get_excluded_edges(edges: list):
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

    return excluded_edges


def count_orphan_nodes(nodes: list, edges: list):
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

    return orphan_nodes


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_nodes_file_name = args.inputNodesFile
    input_edges_file_name = args.inputEdgesFile
        
    input_nodes_file = open(input_nodes_file_name, 'r')
    input_edges_file = open(input_edges_file_name, 'r')

    nodes = jsonlines.Reader(input_nodes_file)
    edges = jsonlines.Reader(input_edges_file)

    build_info = dict()

    for n in nodes:  # search for build info node starting at end
        if n["id"] == kg2_util.CURIE_PREFIX_RTX + ':' + 'KG2':  # should be the first node accessed
            build_info = n
            nodes.remove(n) # remove it so stats aren't reported
            break

    if len(build_info) == 0:
        print("WARNING: 'build' property is missing from the input JSON.", file=sys.stderr)

    number_of_nodes = 0
    for node in nodes:
        number_of_nodes += 1

    number_of_edges = 0
    for edges in edges:
        number_of_edges += 1

    stats = {'_number_of_nodes': number_of_nodes,   # underscore is to make sure it sorts to the top of the report
             '_number_of_edges': number_of_edges,   # underscore is to make sure it sorts to the top of the report
             '_report_datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
             '_build_version': build_info.get('version', ""),
             '_build_time': build_info.get('timestamp_utc', ""),
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
             'number_of_nodes_by_source_and_category': dict(count_number_of_nodes_by_source_and_category(nodes)),
             'sources': get_sources(nodes),
             'number_of_deprecated_nodes': get_deprecated_nodes(nodes),
             'number_of_excluded_edges': get_excluded_edges(edges),
             'number_of_orphan_nodes': count_orphan_nodes(nodes, edges)}

    temp_output_file = tempfile.mkstemp(prefix='kg2-')[1]
    with open(temp_output_file, 'w') as outfile:
        json.dump(stats, outfile, indent=4)
    shutil.move(temp_output_file, args.outputFile)

    nodes.close()
    edges.close()

    input_nodes_file.close()
    input_edges_file.close()
