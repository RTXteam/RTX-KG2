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
    arg_parser.add_argument('biolinkModelURL', type=str)
    arg_parser.add_argument('biolinkModelLocalFile', type=str)
    return arg_parser


CURIE_PREFIXES_FOR_NUMBERED_RELATION_TYPES = {kg2_util.CURIE_PREFIX_RO,
                                              kg2_util.CURIE_PREFIX_NCIT}
CURIE_PREFIXES_FOR_CAMELCASE_RELATION_TYPES = {kg2_util.CURIE_PREFIX_SKOS}

args = make_arg_parser().parse_args()
curies_to_urls_map_file_name = args.curiesToURLsMapFile
predicate_remap_file_name = args.predicateRemapFile
biolink_model_url = args.biolinkModelURL
biolink_model_file_name = args.biolinkModelLocalFile

curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_urls_map_file_name))
curies_to_url_map_data_bidir = {next(iter(listitem.keys())) for listitem in curies_to_url_map_data['use_for_bidirectional_mapping']}

kg2_util.download_file_if_not_exist_locally(biolink_model_url, biolink_model_file_name)
biolink_ont = kg2_util.make_ontology_from_local_file(biolink_model_file_name)
biolink_categories_ontology_depths = kg2_util.get_biolink_categories_ontology_depths(biolink_ont)

biolink_edge_labels = {url.replace(kg2_util.BASE_URL_BIOLINK_META, '') for url in
                       biolink_ont.children(kg2_util.BASE_URL_BIOLINK_META + 'SlotDefinition')}

map_data = yaml.safe_load(open(predicate_remap_file_name, 'r'))
for relation_curie, instructions_dict in map_data.items():
    for instruction, instructions_list in instructions_dict.items():
        new_edge_label = None
        if instruction == 'keep':
            relation_curie_to_check = relation_curie
            assert instructions_list is None, relation_curie
        elif instruction == 'delete':
            continue
        else:
            new_edge_label, relation_curie_to_check = instructions_list
            assert relation_curie_to_check != relation_curie, relation_curie
        curie_prefix, curie_suffix = relation_curie_to_check.split(':')
        assert curie_prefix in curies_to_url_map_data_bidir, relation_curie_to_check
        if new_edge_label is not None and new_edge_label != curie_suffix and \
           (curie_prefix not in CURIE_PREFIXES_FOR_NUMBERED_RELATION_TYPES and
            (curie_prefix not in CURIE_PREFIXES_FOR_CAMELCASE_RELATION_TYPES or
             kg2_util.convert_snake_case_to_camel_case(new_edge_label) != curie_suffix)):
            print("CURIE suffix mismatch with edge label: " + str(instructions_dict))
        if relation_curie_to_check.startswith(kg2_util.CURIE_PREFIX_BIOLINK + ':'):
            edge_label = relation_curie_to_check.replace(kg2_util.CURIE_PREFIX_BIOLINK + ':', '')
            assert edge_label in biolink_edge_labels, relation_curie
            if instructions_list is not None:
                assert edge_label == instructions_list[0], relation_curie
            else:
                assert instruction == 'keep', relation_curie

