#!/usr/bin/env python3
'''Filters the RTX "KG2" second-generation knowledge graph, simplifying predicates and removing redundant edges.

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
import sys
from datetime import datetime

# - check for any input edge labels that occur twice in the predicate-remap.yaml file
# - rename script something like "filter_kg_and_remap_edge_labels.py"
# - need to detect the command "keep" in the YAML file
# - drop edges with 'NEGATION' ?
# - *don't* merge two edges if at least one of them has nonempty publication_info
# - change 'xref' to skos:closeMatch (skos)
# - drop any edge if it is in between two SnoMedCT nodes (optionally; use command-line option)
# - programmatically generate list of "keep" lines to add to the YAML file so all 1,100
#   distinct edge labels are represented in the file
# - note (somehow) if a relationship has been inverted, in the "orig_relation_curie" field


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='filter_kg.py: filters and simplifies the KG2 knowledge grpah for the RTX system')
    arg_parser.add_argument('predicateRemapYaml', type=str, help="The YAML file describing how predicates should be remapped to simpler predicates")
    arg_parser.add_argument('curiesToURIFile', type=str, help="The file mapping CURIE prefixes to URI fragments")
    arg_parser.add_argument('inputFileJson', type=str, help="The input KG2 grah, in JSON format")
    arg_parser.add_argument('outputFileJson', type=str, help="The output KG2 graph, in JSON format")
    arg_parser.add_argument('versionFile', type=str, help="The text file storing the KG2 version")
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('--dropSelfEdgesExcept', required=False, dest='drop_self_edges_except', default=None)
    arg_parser.add_argument('--dropNegated', dest='drop_negated', action='store_true', default=False)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    predicate_remap_file_name = args.predicateRemapYaml
    curies_to_uri_file_name = args.curiesToURIFile
    input_file_name = args.inputFileJson
    output_file_name = args.outputFileJson
    test_mode = args.test
    drop_negated = args.drop_negated
    drop_self_edges_except = args.drop_self_edges_except
    if drop_self_edges_except is not None:
        assert type(drop_self_edges_except) == str
        drop_self_edges_except = set(drop_self_edges_except.split(','))
    predicate_remap_config = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(predicate_remap_file_name))
    map_dict = kg2_util.make_uri_curie_mappers(curies_to_uri_file_name)
    [curie_to_uri_expander, uri_to_curie_shortener] = [map_dict['expand'], map_dict['contract']]
    graph = kg2_util.load_json(input_file_name)
    edge_keys = set()
    new_edges = dict()
    relation_curies_not_in_config = set()
    record_of_relation_curie_occurrences = {relation_curie: False for relation_curie in
                                            predicate_remap_config.keys()}
    command_set = {'delete', 'keep', 'invert', 'rename'}
    for relation_curie, command in predicate_remap_config.items():
        assert len(command) == 1
        assert next(iter(command.keys())) in command_set
    relation_curies_not_in_nodes = set()
    nodes_dict = {node['id']: node for node in graph['nodes']}
    edge_ctr = 0
    for edge_dict in graph['edges']:
        edge_ctr += 1
        if edge_ctr % 1000000 == 0:
            print('processing edge ' + str(edge_ctr) + ' out of ' + str(len(graph['edges'])))
        if drop_negated and edge_dict['negated']:
            continue
        edge_label = edge_dict['edge label']
        simplified_edge_label = edge_label
        relation_curie = edge_dict['relation curie']
        simplified_relation_curie = relation_curie
        relation = edge_dict['relation']
        simplified_relation = relation
        if record_of_relation_curie_occurrences.get(relation_curie, None) is not None:
            record_of_relation_curie_occurrences[relation_curie] = True
            pred_remap_info = predicate_remap_config.get(relation_curie, None)
        else:
            # there is a relation CURIE in the graph that is not in the config file
            relation_curies_not_in_config.add(relation_curie)
            pred_remap_info = {'keep': None}
        assert pred_remap_info is not None
        invert = False
        get_new_rel_info = False
        if pred_remap_info is None:
            assert relation_curie in relation_curies_not_in_config
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
            simplified_edge_label = remap_subinfo[0]
            simplified_relation_curie = remap_subinfo[1]
        if invert:
            edge_dict['edge label'] = 'INVERTED:' + edge_label
            new_object = edge_dict['subject']
            edge_dict['subject'] = edge_dict['object']
            edge_dict['object'] = new_object
        edge_dict['simplified edge label'] = simplified_edge_label
        if drop_self_edges_except is not None and \
           edge_dict['subject'] == edge_dict['object'] and \
           simplified_edge_label not in drop_self_edges_except:
            continue  # see issue 743
        edge_dict['simplified relation curie'] = simplified_relation_curie
        if simplified_relation_curie in nodes_dict:
            simplified_relation = nodes_dict[simplified_relation_curie]['iri']
        else:
            simplified_relation_curie_prefix = simplified_relation_curie.split(':')[0]
            simplified_relation_uri_prefix = curie_to_uri_expander(simplified_relation_curie_prefix + ':')
            if simplified_relation_uri_prefix != simplified_relation_curie_prefix:
                simplified_relation = kg2_util.predicate_label_to_iri_and_curie(simplified_edge_label,
                                                                                simplified_relation_curie_prefix,
                                                                                simplified_relation_uri_prefix)[0]
            else:
                simplified_relation = relation
                relation_curies_not_in_nodes.add(simplified_relation_curie)
        edge_dict['simplified relation'] = simplified_relation
        edge_dict['provided by'] = [edge_dict['provided by']]
        edge_key = edge_dict['subject'] + ' /// ' + simplified_edge_label + ' /// ' + edge_dict['object']
        existing_edge = new_edges.get(edge_key, None)
        if existing_edge is not None:
            existing_edge['provided by'] = list(set(existing_edge['provided by'] + edge_dict['provided by']))
            existing_edge['publications'] += edge_dict['publications']
            existing_edge['publications info'].update(edge_dict['publications info'])
        else:
            new_edges[edge_key] = edge_dict
    del graph['edges']
    graph['edges'] = [edge_dict for edge_dict in new_edges.values()]
    for relation_curie_not_in_config in relation_curies_not_in_config:
        if not relation_curie_not_in_config.startswith(kg2_util.CURIE_PREFIX_BIOLINK + ':'):
            print('relation curie is missing from the YAML config file: ' + relation_curie_not_in_config,
                  file=sys.stderr)
    for relation_curie in record_of_relation_curie_occurrences:
        if not record_of_relation_curie_occurrences[relation_curie]:
            print('relation curie is in the config file but was not detected in the graph: ' + relation_curie, file=sys.stderr)
    for relation_curie in relation_curies_not_in_nodes:
        print('could not get IRI for relation curie: ' + relation_curie)
    update_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    version_file = open(args.versionFile, 'r')
    build_name = str
    for line in version_file:
        build_name = "RTX KG" + line
        break
    build_info = kg2_util.make_node(kg2_util.CURIE_PREFIX_RTX + ':' + 'KG2',
                                    kg2_util.BASE_URL_RTX + 'KG2',
                                    build_name,
                                    kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                    update_date,
                                    kg2_util.CURIE_PREFIX_RTX + ':')
    graph["build"] = build_info
    graph["nodes"].append(build_info)
    kg2_util.save_json(graph, output_file_name, test_mode)
