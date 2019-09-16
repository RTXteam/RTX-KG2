#!/usr/bin/env python3
'''Filters the RTX "KG2" second-generation knowledge graph, simplifying predicates and removing redundant edges.

   Usage: filter_kg.py <predicate-remap.yaml> <kg-input.json> <kg-output.json>
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
import pprint
import sys


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='filter_kg.py: filters and simplifies the KG2 knowledge grpah for the RTX system')
    arg_parser.add_argument('predicateRemapYaml', type=str, help="The YAML file describing how predicates should be remapped to simpler predicates")
    arg_parser.add_argument('inputFileJson', type=str, help="The input KG2 grah, in JSON format")
    arg_parser.add_argument('outputFileJson', type=str, help="The output KG2 graph, in JSON format")
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    predicate_remap_file_name = args.predicateRemapYaml
    input_file_name = args.inputFileJson
    output_file_name = args.outputFileJson
    test_mode = args.test
    predicate_remap_config = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(predicate_remap_file_name))
    graph = kg2_util.load_json(input_file_name)
    edge_keys = set()
    new_edges = dict()
    edge_labels_not_in_config = set()
    edge_labels_unknown_command = set()
    for edge_dict in graph['edges']:
        edge_label = edge_dict['edge label']
        pred_remap_info = predicate_remap_config.get(edge_label, None)
        new_edge_label = None
        invert = False
        if pred_remap_info is None:
            edge_labels_not_in_config.add(edge_label)
        else:
            if 'delete' in pred_remap_info:
                continue
            else:
                new_edge_label = pred_remap_info.get('rename')
                if new_edge_label is None:
                    new_edge_label = pred_remap_info.get('invert')
                    if new_edge_label is not None:
                        invert = True
                    else:
                        edge_labels_unknown_command.add(edge_label)
        if invert:
            new_object = edge_dict['subject']
            edge_dict['subject'] = edge_dict['object']
            edge_dict['object'] = new_object
        orig_relation_curie = edge_dict['relation curie']
        if new_edge_label is None:
            new_edge_label = edge_label
        new_relation_curie = 'KG2:' + new_edge_label
        new_relation_iri = 'http://rtx.ncats.io/api/rtx/v1/predicates/' + new_edge_label
        edge_dict['orig relation curie'] = orig_relation_curie
        edge_dict['relation curie'] = new_relation_curie
        edge_dict['relation'] = new_relation_iri
        edge_dict['edge label'] = new_edge_label
        edge_dict['provided by'] = [edge_dict['provided by']]
        edge_key = edge_dict['subject'] + ' /// ' + new_edge_label + ' /// ' + edge_dict['object']
        existing_edge = new_edges.get(edge_key, None)
        if existing_edge is not None:
            existing_edge['provided by'] += edge_dict['provided by']
            existing_edge['publications'] += edge_dict['publications']
            existing_edge['publications info'].update(edge_dict['publications info'])
        else:
            new_edges[edge_key] = edge_dict
    del graph['edges']
    graph['edges'] = [edge_dict for edge_dict in new_edges.values()]
    for edge_label_not_in_config in edge_labels_not_in_config:
        print('edge label is missing from the YAML config file: ' + edge_label_not_in_config, file=sys.stderr)
    for edge_label_unknown_command in edge_labels_unknown_command:
        print('edge label has unrecognized command in the YAML file: ' + edge_label_unknown_command, file=sys.stderr)
    kg2_util.save_json(graph, output_file_name, test_mode)

