#!/usr/bin/env python3
'''Filters the RTX "KG2" second-generation knowledge graph, simplifying predicates and removing redundant edges.
   Filter out negated edges, merge edges, remap predicates, remap source curies.

   Usage: filter_kg_and_remap_predicates.py <predicate-remap.yaml> <kg-input.json> <kg-output.json>
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
from datetime import datetime

# - check for any input relation_labels that occur twice in the predicate-remap.yaml file
# - rename script something like "filter_kg_and_remap_relation_labels.py"
# - need to detect the command "keep" in the YAML file
# - drop edges with 'NEGATION' ?
# - *don't* merge two edges if at least one of them has nonempty publication_info
# - change 'xref' to skos:closeMatch (skos)
# - drop any edge if it is in between two SnoMedCT nodes (optionally; use command-line option)
# - programmatically generate list of "keep" lines to add to the YAML file so all 1,100
#   distinct relation_labels are represented in the file
# - note (somehow) if a relationship has been inverted, in the "orig_relation_curie" field


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='filter_kg.py: filters and simplifies the KG2 knowledge grpah for the RTX system')
    arg_parser.add_argument('predicateRemapYaml', type=str, help="The YAML file describing how predicates should be remapped to simpler predicates")
    arg_parser.add_argument('inforesRemapYaml', type=str, help="The YAML file describing how provided_by fields should be remapped to Translator infores curies")
    arg_parser.add_argument('curiesToURIFile', type=str, help="The file mapping CURIE prefixes to URI fragments")
    arg_parser.add_argument('inputFileJson', type=str, help="The input KG2 graph, in JSON format")
    arg_parser.add_argument('outputFileJson', type=str, help="The output KG2 graph, in JSON format")
    arg_parser.add_argument('versionFile', type=str, help="The text file storing the KG2 version")
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('--dropSelfEdgesExcept', required=False, dest='drop_self_edges_except', default=None)
    arg_parser.add_argument('--dropNegated', dest='drop_negated', action='store_true', default=False)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    predicate_remap_file_name = args.predicateRemapYaml
    infores_remap_file_name = args.inforesRemapYaml
    curies_to_uri_file_name = args.curiesToURIFile
    input_file_name = args.inputFileJson
    output_file_name = args.outputFileJson
    test_mode = args.test
    drop_negated = args.drop_negated
    drop_self_edges_except = args.drop_self_edges_except
    if drop_self_edges_except is not None:
        assert type(drop_self_edges_except) == str
        drop_self_edges_except = set(drop_self_edges_except.split(','))
    # Config files
    predicate_remap_config = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(predicate_remap_file_name))
    infores_remap_config = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(infores_remap_file_name))
    map_dict = kg2_util.make_uri_curie_mappers(curies_to_uri_file_name)
    # ** Not sure about this notation ** 
    [curie_to_uri_expander, uri_to_curie_shortener] = [map_dict['expand'], map_dict['contract']]
    graph = kg2_util.load_json(input_file_name)
    new_edges = dict()
    # Create sets to handle knowledge sources
    original_predicate_curies_not_in_config = set()
    provided_by_curies_not_in_config_nodes = set()
    provided_by_curies_not_in_config_edges = set()
    # ** Double check meaning ** 
    record_of_original_predicate_curie_occurrences = {original_predicate_curie: False for original_predicate_curie in
                                            predicate_remap_config.keys()}
    # To Do: Update command set
    command_set = {'delete', 'keep', 'invert', 'rename'}
    for original_predicate_curie, command in predicate_remap_config.items():
        assert len(command) == 1
        assert next(iter(command.keys())) in command_set
    # Every predicate curie should get its own node. Otherwise add to this set to complain.
    original_predicate_curies_not_in_nodes = set()
    nodes_dict = dict()
    for node_dict in graph['nodes']:
        node_id = node_dict['id']
        provided_by = node_dict['knowledge_source']
        infores_curie_dict = infores_remap_config.get(provided_by, None)
        if infores_curie_dict is None:
            provided_by_curies_not_in_config_nodes.add(provided_by)
        else:
            infores_curie = infores_curie_dict['infores_curie']
        node_dict['knowledge_source'] = infores_curie
        nodes_dict[node_id] = node_dict
    edge_ctr = 0
    for edge_dict in graph['edges']:
        edge_ctr += 1
        if edge_ctr % 1000000 == 0:
            print('processing edge ' + str(edge_ctr) + ' out of ' + str(len(graph['edges'])))
        if drop_negated and edge_dict['negated']:
            continue
        original_predicate_label = edge_dict['relation_label']
        predicate_label = original_predicate_label
        original_predicate_curie = edge_dict['original_predicate']
        predicate_curie = original_predicate_curie
        if record_of_original_predicate_curie_occurrences.get(original_predicate_curie, None) is not None:
            record_of_original_predicate_curie_occurrences[original_predicate_curie] = True
            pred_remap_info = predicate_remap_config.get(original_predicate_curie, None)
        else:
            # there is a original predicate CURIE in the graph that is not in the config file
            original_predicate_curies_not_in_config.add(original_predicate_curie)
            pred_remap_info = {'keep': None}
        assert pred_remap_info is not None
        invert = False
        get_new_rel_info = False
        if pred_remap_info is None:
            assert original_predicate_curie in original_predicate_curies_not_in_config
        else:
            if 'delete' in pred_remap_info:
                continue
            remap_subinfo = pred_remap_info.get('invert', None)
            if remap_subinfo is not None:
                invert = True
                get_new_rel_info = True
            else:
                remap_subinfo = pred_remap_info.get('rename', None)
                if remap_subinfo is None:
                    assert 'keep' in pred_remap_info
                else:
                    get_new_rel_info = True
        if get_new_rel_info:
            predicate_label = remap_subinfo[0]
            predicate_curie = remap_subinfo[1]  # Gets the biolink predicate
        if invert:
            edge_dict['relation_label'] = 'INVERTED:' + original_predicate_label
            new_object = edge_dict['subject']
            edge_dict['subject'] = edge_dict['object']
            edge_dict['object'] = new_object
        edge_dict['predicate_label'] = predicate_label
        # Delete negated edges and self edges except interacts_with,positively_regulates,inhibits,increase
        # as defined in run-simplify.sh
        # To Do: verify exception list complies with updates from Biolink 3.0
        if drop_self_edges_except is not None and \
           edge_dict['subject'] == edge_dict['object'] and \
           predicate_label not in drop_self_edges_except:
            continue  # see issue 743
        edge_dict['predicate'] = predicate_curie
        # Sets biolink curie; remapping
        if predicate_curie not in nodes_dict:
            predicate_curie_prefix = predicate_curie.split(':')[0]
            predicate_uri_prefix = curie_to_uri_expander(predicate_curie_prefix + ':')
            # Create list of curies to complain about if not in biolink
            if predicate_uri_prefix == predicate_curie_prefix:
                original_predicate_curies_not_in_nodes.add(predicate_curie) 
        provided_by = edge_dict['knowledge_source']
        infores_curie_dict = infores_remap_config.get(provided_by, None)
        if infores_curie_dict is None:
            provided_by_curies_not_in_config_edges.add(provided_by)
        else:
            infores_curie = infores_curie_dict['infores_curie']
        edge_dict['knowledge_source'] = [infores_curie]
        # TODO: Update with additional properties
        edge_key = edge_dict['subject'] + ' /// ' + predicate_label + ' /// ' + edge_dict['object']
        existing_edge = new_edges.get(edge_key, None)
        # TODO: Update merging to handle semantic distinction between qualifiers
        if existing_edge is not None:
            existing_edge['knowledge_source'] = sorted(list(set(existing_edge['knowledge_source'] + edge_dict['knowledge_source'])))
            existing_edge['publications'] += edge_dict['publications']
            existing_edge['publications_info'].update(edge_dict['publications_info'])
        else:
            new_edges[edge_key] = edge_dict
    # Releasing some memory
    del graph['edges']
    del graph['nodes']
    graph['nodes'] = list(nodes_dict.values())
    del nodes_dict
    graph['edges'] = list(new_edges.values())
    del new_edges
    # Warnings for issues that came up
    for original_predicate_curie in record_of_original_predicate_curie_occurrences:
        if not record_of_original_predicate_curie_occurrences[original_predicate_curie]:
            print('original predicate curie is in the config file but was not used in any edge in the graph: ' + original_predicate_curie, file=sys.stderr)
    for original_predicate_curie in original_predicate_curies_not_in_nodes:
        print('could not find a node for original predicate curie: ' + original_predicate_curie)
    original_predicate_curies_not_in_config_for_iteration = list(original_predicate_curies_not_in_config)
    for original_predicate_curie_not_in_config in original_predicate_curies_not_in_config_for_iteration:
        if not original_predicate_curie_not_in_config.startswith(kg2_util.CURIE_PREFIX_BIOLINK + ':'):
            print('original predicate curie is missing from the YAML config file: ' + original_predicate_curie_not_in_config,
                  file=sys.stderr)
        else:
            original_predicate_curies_not_in_config.remove(original_predicate_curie_not_in_config)
    for provided_by_curies_not_in_config_node in provided_by_curies_not_in_config_nodes:
        print('knowledge_source node curie is missing from the YAML config file: ' + provided_by_curies_not_in_config_node,
               file=sys.stderr)
    for provided_by_curies_not_in_config_edge in provided_by_curies_not_in_config_edges:
        print('knowledge_source node curie is missing from the YAML config file: ' + provided_by_curies_not_in_config_edge,
               file=sys.stderr)
    if len(original_predicate_curies_not_in_config) > 0:
        print("There are original predicate curies missing from the yaml config file. Please add them and try again. Exiting.", file=sys.stderr)
        exit(1)
    if len(provided_by_curies_not_in_config_nodes) > 0:
        print("There are nodes provided_by curies missing from the yaml config file. Please add them and try again. Exiting.", file=sys.stderr)
        exit(1)
    if len(provided_by_curies_not_in_config_edges) > 0:
        print("There are edges provided_by curies missing from the yaml config file. Please add them and try again. Exiting.", file=sys.stderr)
        exit(1)
    update_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    version_file = open(args.versionFile, 'r')
    build_name = str
    # Add node to describe build
    for line in version_file:
        test_flag = ""
        if test_mode:
            test_flag = "-TEST"
        build_name = "RTX KG" + line.rstrip() + test_flag
        break
    build_node = kg2_util.make_node(kg2_util.CURIE_PREFIX_RTX + ':' + 'KG2',
                                    kg2_util.BASE_URL_RTX + 'KG2',
                                    build_name,
                                    kg2_util.BIOLINK_CATEGORY_INFORMATION_RESOURCE,
                                    update_date,
                                    kg2_util.CURIE_PREFIX_RTX + ':')
    build_info = {'version': build_node['name'], 'timestamp_utc': build_node['update_date']}
    pprint.pprint(build_info)
    graph["build"] = build_info
    graph["nodes"].append(build_node)
    kg2_util.save_json(graph, output_file_name, test_mode)
    del graph
