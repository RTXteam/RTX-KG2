#!/usr/bin/env python3
'''Filters the RTX "KG2" second-generation knowledge graph, simplifying predicates and removing redundant edges.
   Filter out negated edges, merge edges, remap predicates, remap source curies.

   Usage: filter_kg_and_remap_predicates.py <predicate-remap.yaml> <kg-input.json> <kg-output.json>
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import argparse
import kg2_util
import pprint
import sys
import json
from datetime import datetime

# 1. What is the indicator for negation?
# - It's a prefix in the relation property in the edge... possibly. 
# - Negated edges only come from SEMMEDDB, so we look in semmeddb_tuple_list_json_to_kg_json
# - A value on L209, the source relation checks and sets value
# 2. Instruction below "drop any edge if it is in between two SnoMedCT nodes" still needed? No

# - check for any input relation_labels that occur twice in the predicate-remap.yaml file
# - rename script something like "filter_kg_and_remap_relation_labels.py"
# - need to detect the command "keep" in the YAML file
# - drop edges with 'NEGATION'
# - *don't* merge two edges if at least one of them has nonempty publication_info
# - change 'xref' to skos:closeMatch (skos)
# - drop any edge if it is in between two SnoMedCT nodes (optionally; use command-line option)
# - programmatically generate list of "keep" lines to add to the YAML file so all 1,100
#   distinct relation_labels are represented in the file
# - note (somehow) if a relationship has been inverted, in the "orig_relation_curie" field


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='filter_kg.py: filters and simplifies the KG2 knowledge grpah for the RTX system')
    arg_parser.add_argument('predicateRemapYaml', type=str, help="The YAML file describing how predicates should be remapped to simpler predicates")
    arg_parser.add_argument('inforesRemapYaml', type=str, help="The YAML file describing how knowledge_source fields should be remapped to Translator infores curies")
    arg_parser.add_argument('curiesToURIFile', type=str, help="The file mapping CURIE prefixes to URI fragments")
    arg_parser.add_argument('knowledgeLevelAgentTypeFile', type=str, help="The file mapping infores curies to knowledge_level and agent_type source information")
    arg_parser.add_argument('edgeBlocklistFile', type=str, help="File containing blocked edges from KG2")
    arg_parser.add_argument('inputNodesFile', type=str, help="The input KG2 graph, in JSON format")
    arg_parser.add_argument('inputEdgesFile', type=str, help="The input KG2 graph, in JSON format")
    arg_parser.add_argument('outputNodesFile', type=str, help="The output KG2 graph, in JSON format")
    arg_parser.add_argument('outputEdgesFile', type=str, help="The output KG2 graph, in JSON format")
    arg_parser.add_argument('versionFile', type=str, help="The text file storing the KG2 version")
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('--dropSelfEdgesExcept', required=False, dest='drop_self_edges_except', default=None)
    arg_parser.add_argument('--dropNegated', dest='drop_negated', action='store_true', default=False)
    return arg_parser


def update_edge_id(edge_id: str, qualified_predicate=None, qualified_object_aspect=None,
                   qualified_object_direction=None):
    edge_id_keys = edge_id.split("---")
    subject = edge_id_keys[0]
    predicate = edge_id_keys[1]
    object = edge_id_keys[-2]
    knowledge_source = edge_id_keys[-1]
    new_edge_id = f"{subject}---{predicate}---{qualified_predicate}---{qualified_object_aspect}---{qualified_object_direction}---{object}---{knowledge_source}"
    return new_edge_id


def warning_knowledge_source_curies_not_in_config_edges(knowledge_source_curies_not_in_config_edges):
    for knowledge_source_curies_not_in_config_edge in knowledge_source_curies_not_in_config_edges:
        print('knowledge_source node curie is missing from the YAML config file: ' + knowledge_source_curies_not_in_config_edge,
               file=sys.stderr)
    
    if len(knowledge_source_curies_not_in_config_edges) > 0:
        print(
            "There are edges knowledge_source curies missing from the yaml config file. Please add them and try again. Exiting.",
            file=sys.stderr)
        exit(1)


def warning_knowledge_source_curies_not_in_config_nodes(knowledge_source_curies_not_in_config_nodes):
    for knowledge_source_curies_not_in_config_node in knowledge_source_curies_not_in_config_nodes:
        print('knowledge_source node curie is missing from the YAML config file: ' + knowledge_source_curies_not_in_config_node,
               file=sys.stderr)

    if len(knowledge_source_curies_not_in_config_nodes) > 0:
        print(
            "There are nodes knowledge_source curies missing from the yaml config file. Please add them and try again. Exiting.",
            file=sys.stderr)
        exit(1)

def warning_knowledge_level_agent_source_not_in_config_edges(knowledge_source_not_in_klat_map):
    for infores_curie in knowledge_source_not_in_klat_map:
        print('infores is missing from the YAML config file for knowledge_level and agent_type: ' + infores_curie,
               file=sys.stderr)
        # To terminate build in the future in case they are missing columns `knowledge_level` and `agent_type` mentioned issue number #441 to keep track
        exit(1)

    if len(knowledge_source_curies_not_in_config_nodes) > 0:
        print(
            "There are edges infores_curies missing from the yaml config file for knowledge_level and agent_type. Please add them and try again. Exiting.",
            file=sys.stderr)
        exit(1)


def warning_source_predicate_curies_not_in_config(source_predicate_curies_not_in_config):
    source_predicate_curies_not_in_config_for_iteration = list(source_predicate_curies_not_in_config)
    for source_predicate_curie_not_in_config in source_predicate_curies_not_in_config_for_iteration:
        if not source_predicate_curie_not_in_config.startswith(kg2_util.CURIE_PREFIX_BIOLINK + ':'):
            print('Source predicate curie is missing from the YAML config file: ' + source_predicate_curie_not_in_config,
                  file=sys.stderr)
        else:
            source_predicate_curies_not_in_config.remove(source_predicate_curie_not_in_config)
    
    if len(source_predicate_curies_not_in_config) > 0:
        print(
            "There are source predicate curies missing from the yaml config file. Please add them and try again. Exiting.",
            file=sys.stderr)
        exit(1)


def warning_source_predicate_curies_not_in_nodes(source_predicate_curies_not_in_nodes):
    for source_predicate_curie in source_predicate_curies_not_in_nodes:
        print('could not find a node for source predicate curie: ' + source_predicate_curie)


def warning_record_of_source_predicate_curie_occurrences(record_of_source_predicate_curie_occurrences):
    for source_predicate_curie in record_of_source_predicate_curie_occurrences:
        if not record_of_source_predicate_curie_occurrences[source_predicate_curie]:
            print(
                'Knowledge source predicate curie is in the config file but was not used in any edge in the graph: ' + source_predicate_curie,
                file=sys.stderr)


def process_nodes(input_nodes_file_name, infores_remap_config, nodes_output):
    knowledge_source_curies_not_in_config_nodes = set()

    node_ctr = 0

    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(input_nodes_file_name)
    nodes = nodes_read_jsonlines_info[0]
    nodes_set = set()

    for node_dict in nodes:
        node_ctr += 1
        if node_ctr % 1000000 == 0:
            print(f"Processing node {node_ctr}")
        node_id = node_dict["id"]
        if node_dict.get('provided_by') is None:
            node_dict['provided_by'] = node_dict.pop('knowledge_source')
        if isinstance(node_dict.get('provided_by'), str):
            node_dict['provided_by'] = [node_dict['provided_by']]
        knowledge_source = node_dict['provided_by']
        infores_curies = list()
        for source in knowledge_source:
            infores_curie_dict = infores_remap_config.get(source, None)
            if infores_curie_dict is None:
                knowledge_source_curies_not_in_config_nodes.add(source)
            else:
                infores_curie = infores_curie_dict['infores_curie']
                infores_curies.append(infores_curie)
        node_dict['provided_by'] = infores_curies
        nodes_output.write(node_dict)
        nodes_set.add(node_id)

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)
    print(f"Completed nodes {kg2_util.date()}")

    # Issue warnings for problems that came up
    warning_knowledge_source_curies_not_in_config_nodes(knowledge_source_curies_not_in_config_nodes)
   
    return nodes_set


def process_edges(input_edges_file_name, infores_remap_config, knowledge_level_agent_type_map, predicate_remap_file_name, curies_to_uri_file_name, edges_output, drop_self_edges_except, nodes, edge_blocklist):
    predicate_remap_config = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(predicate_remap_file_name))
    # map_dict = kg2_util.make_uri_curie_mappers(curies_to_uri_file_name)

    # curie_to_uri_expander = map_dict['expand']
    source_predicate_curies_not_in_config = set()
    source_predicate_curies_not_in_nodes = set()
    knowledge_source_curies_not_in_config_edges = set()
    record_of_source_predicate_curie_occurrences = {source_predicate_curie: False for source_predicate_curie in predicate_remap_config.keys()}

    command_set = {'delete', 'keep', 'invert'}
    # The length of the 'command' could be 1 if it just has the operation, such as with 'delete'
    # or up to 4 if there is the operation, core predicate, qualified predicate, and qualifiers
    # Verify that the operation is allowed
    for source_predicate_curie, command in predicate_remap_config.items():
        assert len(command) in range(1, 5)
        assert command["operation"] in command_set

    edge_ctr = 0

    edges_read_jsonlines_info = kg2_util.start_read_jsonlines(input_edges_file_name)
    edges = edges_read_jsonlines_info[0]

    print(f"Starting edges {kg2_util.date()}")
    for edge_dict in edges:
        edge_ctr += 1
        if edge_ctr == 1:
            print(edge_dict)
        if edge_ctr % 1000000 == 0:
            print(f"Processing edge {edge_ctr}")
        if drop_negated and edge_dict['negated']:
            continue
        source_predicate_label = edge_dict['relation_label']
        predicate_label = source_predicate_label
        if edge_dict.get('source_predicate') is None:
            edge_dict['source_predicate'] = edge_dict.pop('original_predicate')
        source_predicate_curie = edge_dict['source_predicate']
        predicate_curie = source_predicate_curie

        core_predicate_curie = None   # never reuse a core_predicate_curie from previous iteration through loop
        
        if record_of_source_predicate_curie_occurrences.get(source_predicate_curie, None) is not None:
            record_of_source_predicate_curie_occurrences[source_predicate_curie] = True 
            pred_remap_info = predicate_remap_config.get(source_predicate_curie, None)   
        else:
            # there is a original predicate CURIE in the graph that is not in the config file
            source_predicate_curies_not_in_config.add(source_predicate_curie)
            #print(f"Source predicate curie missing {source_predicate_curie}")
            pred_remap_info = {'operation': 'keep'}
        
        assert pred_remap_info is not None, f"Edge {edge_dict} missing {pred_remap_info}"
        
        invert = False
        get_new_rel_info = False

        operation = pred_remap_info.get('operation', None)
        if operation == "delete":
            continue
        get_new_rel_info = True
        if operation == "invert":
            invert = True
        elif pred_remap_info.get("core_predicate") is None:
            assert operation == "keep"
            get_new_rel_info = False

        qualified_predicate = None
        qualified_object_aspect = None
        qualified_object_direction = None

        if get_new_rel_info:
            assert pred_remap_info.get("core_predicate") is not None
            core_predicate_curie = pred_remap_info.get("core_predicate")
            qualified_predicate = pred_remap_info.get("qualified_predicate", None)
            qualifiers = pred_remap_info.get("qualifiers", None)
            if qualifiers is not None:
                qualifiers_dict = qualifiers
                qualified_object_aspect = qualifiers_dict.get("object_aspect", None)
                qualified_object_direction = qualifiers_dict.get("object_direction", None)
            if qualified_object_aspect is not None and qualified_object_direction is not None and \
                    qualifiers is None:
                assert qualified_predicate is not None, f"Qualifier but not qualified predicate {edge_dict}"
        if invert:
            edge_dict['relation_label'] = 'INVERTED:' + source_predicate_label
            new_object = edge_dict['subject']
            edge_dict['subject'] = edge_dict['object']
            edge_dict['object'] = new_object
        edge_dict["predicate_label"] = predicate_label
        if drop_self_edges_except is not None and \
                edge_dict['subject'] == edge_dict['object'] and \
                predicate_label not in drop_self_edges_except:
            continue
        edge_dict['predicate'] = predicate_curie
        edge_dict['qualified_predicate'] = qualified_predicate
        edge_dict['qualified_object_aspect'] = qualified_object_aspect
        edge_dict['qualified_object_direction'] = qualified_object_direction
        if core_predicate_curie is None and predicate_curie.startswith(kg2_util.CURIE_PREFIX_BIOLINK + ":"):
            core_predicate_curie = predicate_curie
        edge_dict['predicate'] = core_predicate_curie
        edge_id = edge_dict["id"]
        new_edge_id = update_edge_id(edge_id, qualified_predicate, qualified_object_aspect, qualified_object_direction)
        edge_dict["id"] = new_edge_id

        if predicate_curie not in nodes:
            predicate_curie_prefix = predicate_curie.split(':')[0]
            # predicate_uri_prefix = curie_to_uri_expander(predicate_curie_prefix + ':')
            # # Create list of curies to complain about if not in biolink
            # if predicate_uri_prefix == predicate_curie_prefix:
            #     source_predicate_curies_not_in_nodes.add(predicate_curie)
            source_predicate_curies_not_in_nodes.add(predicate_curie)
        if edge_dict.get("primary_knowledge_source") is None:
            #print(f"{edge_dict}")
            edge_dict["primary_knowledge_source"] = edge_dict.pop("knowledge_source")
        primary_knowledge_source = edge_dict["primary_knowledge_source"]
        infores_curie_dict = infores_remap_config.get(primary_knowledge_source, None)
        if infores_curie_dict is None:
            knowledge_source_curies_not_in_config_edges.add(primary_knowledge_source)
        else:
            infores_curie = infores_curie_dict['infores_curie']
            edge_dict['primary_knowledge_source'] = infores_curie

        # Added for #358; a bit roundabout given setup of infores_curie, which might not exist if infores_curie_dict was None
        knowledge_source_not_in_klat_map = set()
        kl_at_search_source = edge_dict.get('primary_knowledge_source', primary_knowledge_source)
        knowledge_level_agent_type_dict = knowledge_level_agent_type_map.get(kl_at_search_source, None)
        if knowledge_level_agent_type_dict is None:
            knowledge_source_not_in_klat_map.add(kl_at_search_source)
        else:
            knowledge_level = knowledge_level_agent_type_dict['knowledge_level']
            agent_type = knowledge_level_agent_type_dict['agent_type']
            edge_dict['knowledge_level'] = knowledge_level
            edge_dict['agent_type'] = agent_type

        edge_subject = edge_dict['subject'] 
        edge_object = edge_dict['object']

        edge_triple = (edge_subject, edge_dict['predicate'], edge_object)
        if edge_triple in edge_blocklist:
            print("Edge:", edge_triple, "in the edge blocklist. Not adding it to edges_output.")
            continue

        edge_key = f"{edge_subject} /// {predicate_curie} /// {qualified_predicate} /// {qualified_object_aspect} /// {qualified_object_direction} /// {edge_object} /// {primary_knowledge_source}"

        edges_output.write(edge_dict)

    kg2_util.end_read_jsonlines(edges_read_jsonlines_info)
    print(f"Finished edges {kg2_util.date()}")

    # Warnings for issues that came up
    warning_record_of_source_predicate_curie_occurrences(record_of_source_predicate_curie_occurrences)
    warning_source_predicate_curies_not_in_nodes(source_predicate_curies_not_in_nodes)
    warning_source_predicate_curies_not_in_config(source_predicate_curies_not_in_config)
    warning_knowledge_source_curies_not_in_config_edges(knowledge_source_curies_not_in_config_edges)
    warning_knowledge_level_agent_source_not_in_config_edges(knowledge_source_not_in_klat_map)


def load_edge_blocklist(edge_blocklist_dict):
    edge_blocklist = list()
    for edge in edge_blocklist_dict:
        for edge_subject in edge['subject_ids']:
            for edge_object in edge['object_ids']:
                edge_blocklist.append((edge_subject, edge['predicate'], edge_object))

    return edge_blocklist


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    predicate_remap_file_name = args.predicateRemapYaml
    infores_remap_file_name = args.inforesRemapYaml
    curies_to_uri_file_name = args.curiesToURIFile
    knowledge_level_agent_type_file_name = args.knowledgeLevelAgentTypeFile
    edge_blocklist_file_name = args.edgeBlocklistFile
    input_nodes_file_name = args.inputNodesFile
    input_edges_file_name = args.inputEdgesFile
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile
    test_mode = args.test
    drop_negated = args.drop_negated
    drop_self_edges_except = args.drop_self_edges_except

    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    infores_remap_config = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(infores_remap_file_name))
    knowledge_level_agent_type_map = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(knowledge_level_agent_type_file_name))
    edge_blocklist_map = load_edge_blocklist(kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(edge_blocklist_file_name)))

    source_predicate_curies_not_in_config = set()
    knowledge_source_curies_not_in_config_nodes = set()
    source_predicate_curies_not_in_nodes = set()
    knowledge_source_curies_not_in_config_edges = set()

    if drop_self_edges_except is not None:
        assert type(drop_self_edges_except) == str
        drop_self_edges_except = set(drop_self_edges_except.split(','))

    nodes = process_nodes(input_nodes_file_name, infores_remap_config, nodes_output)
    
    process_edges(input_edges_file_name, infores_remap_config, knowledge_level_agent_type_map, predicate_remap_file_name, curies_to_uri_file_name, edges_output, drop_self_edges_except, nodes, edge_blocklist_map)
    
    update_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    version_file = open(args.versionFile, 'r')
    build_name = str
    # Add node to describe build
    for line in version_file:
        test_flag = ""
        if test_mode:
            test_flag = "-TEST"
        build_name = "RTX-KG" + line.rstrip() + test_flag
        break
    build_node = kg2_util.make_node(kg2_util.CURIE_PREFIX_RTX + ':' + 'KG2',
                                    kg2_util.BASE_URL_RTX + 'KG2',
                                    build_name,
                                    kg2_util.SOURCE_NODE_CATEGORY,
                                    update_date,
                                    kg2_util.CURIE_PREFIX_RTX + ':')
    build_info = {'version': build_node['name'], 'timestamp_utc': build_node['update_date']}
    pprint.pprint(build_info)
    nodes_output.write(build_node)
    print(f"Closing simplified file {kg2_util.date()}")
    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)
    print(f"Completed closing file {kg2_util.date()}")
