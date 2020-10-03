#!/usr/bin/env python3
'''Checks the file `predicate-remap.yaml` for correctness.  This script should
   be run each time `predicate-remap.yaml` or `curies-to-urls-map.yaml` is
   changed.

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
import yaml


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='validate_predicate_remap_yaml.py: checks the file `predicate-remap.yaml` for correctness.')
    arg_parser.add_argument('curiesToURLsMapFile', type=str)
    arg_parser.add_argument('predicateRemapFile', type=str)
    arg_parser.add_argument('biolinkModelYamlURL', type=str)
    arg_parser.add_argument('biolinkModelYamlLocalFile', type=str)
    return arg_parser


args = make_arg_parser().parse_args()
curies_to_urls_map_file_name = args.curiesToURLsMapFile
predicate_remap_file_name = args.predicateRemapFile
biolink_model_url = args.biolinkModelYamlURL
biolink_model_file_name = args.biolinkModelYamlLocalFile

curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_urls_map_file_name))
curies_to_url_map_data_bidir = {next(iter(listitem.keys())) for listitem in curies_to_url_map_data['use_for_bidirectional_mapping']}

kg2_util.download_file_if_not_exist_locally(biolink_model_url, biolink_model_file_name)

biolink_model = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(biolink_model_file_name))

biolink_to_external_mappings = {'biolink:' + relation.replace(' ', '_'):
                                list(map(lambda x: x.lower(), relation_info.get('mappings', []))) for
                                relation, relation_info in biolink_model['slots'].items()}
for relation, relation_info in biolink_model['slots'].items():
    inverted_relation = relation_info.get('inverse', None)
    mappings = relation_info.get('mappings', None)
    if inverted_relation is not None and mappings is not None:
        biolink_curie = 'biolink:' + inverted_relation.replace(' ', '_')
        existing_list = biolink_to_external_mappings.get(biolink_curie, None)
        if existing_list is None:
            existing_list = []
        existing_list += list(map(lambda x: x.lower(), mappings))
        biolink_to_external_mappings[biolink_curie] = existing_list

biolink_to_external_mappings['skos:closeMatch'] = []

external_to_biolink_mappings = dict()
for biolink_curie, external_curies in biolink_to_external_mappings.items():
    for external_curie in external_curies:
        if external_to_biolink_mappings.get(external_curie, None) is None:
            external_to_biolink_mappings[external_curie] = set()
        external_to_biolink_mappings[external_curie].add(biolink_curie)

pred_info = yaml.safe_load(open(predicate_remap_file_name, 'r'))

for relation, instruction_dict in pred_info.items():
    command, subinfo = next(iter(instruction_dict.items()))
    assert len(instruction_dict) == 1, relation
    if command == 'keep' and not relation.startswith('biolink:'):
        if not relation.startswith('BSPO:') and \
           not relation.startswith('FMA:') and \
           not relation.startswith('UBERON:'):
            assert False, relation
        else:
            command = 'rename'
            subinfo = ['coexists_with', 'biolink:coexists_with']
    if subinfo is not None:
        simplified_relation = subinfo[1]
        if not simplified_relation.startswith('biolink:') and not simplified_relation.startswith('skos:closeMatch'):
            if simplified_relation.startswith('FMA:') or \
               simplified_relation.startswith('BSPO:') or \
               simplified_relation.startswith('UBERON:'):
                command = 'rename'
                subinfo = ['coexists_with', 'biolink:coexists_with']
            else:
                assert False
    if subinfo is not None:
        assert subinfo[1] in biolink_to_external_mappings, relation
        allowed_biolink_curies_set = external_to_biolink_mappings.get(relation.lower(), None)
        if allowed_biolink_curies_set is not None:
            assert subinfo[1] in allowed_biolink_curies_set, relation
    else:
        assert command == 'keep' or command == 'delete'
        if command == 'keep':
            assert relation in biolink_to_external_mappings, relation
            assert relation.startswith('biolink:') or relation.startswith('skos:')
