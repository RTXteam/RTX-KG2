#!/usr/bin/env python3
'''Checks the file `curies-to-categories.yaml` for correctness.  This script
   should be run each time `curies-to-categories.yaml` or
   `curies-to-urls-map.yaml` is changed.

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


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='validate_curies_to_categories.py: checks the file `curies-to-categories.yaml` for correctness.')
    arg_parser.add_argument('curiesToCategoriesFile', type=str)
    arg_parser.add_argument('curiesToURLsMapFile', type=str)
    arg_parser.add_argument('biolinkModelURL', type=str)
    arg_parser.add_argument('biolinkModelLocalFile', type=str)
    return arg_parser


args = make_arg_parser().parse_args()
curies_to_categories_file_name = args.curiesToCategoriesFile
curies_to_urls_map_file_name = args.curiesToURLsMapFile
biolink_model_url = args.biolinkModelURL
biolink_model_file_name = args.biolinkModelLocalFile
curies_to_categories_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_categories_file_name))
curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_urls_map_file_name))
curies_to_url_map_data_bidir = {next(iter(listitem.keys())) for listitem in curies_to_url_map_data['use_for_bidirectional_mapping']}

kg2_util.download_file_if_not_exist_locally(biolink_model_url, biolink_model_file_name)
biolink_ont = kg2_util.make_ontology_from_local_file(biolink_model_file_name)
biolink_categories_ontology_depths = kg2_util.get_biolink_categories_ontology_depths(biolink_ont)

for prefix in curies_to_categories_data['prefix-mappings'].keys():
    assert prefix in curies_to_url_map_data_bidir, prefix

for curie_id in curies_to_categories_data['term-mappings'].keys():
    prefix = curie_id.split(':')[0]
    assert prefix in curies_to_url_map_data_bidir, prefix

categories_to_check = list(curies_to_categories_data['prefix-mappings'].values()) +\
    list(curies_to_categories_data['term-mappings'].values())

for category in categories_to_check:
    category_camelcase = kg2_util.convert_space_case_to_camel_case(category)
    category_iri = kg2_util.BASE_URL_BIOLINK_META + category_camelcase
    assert category_camelcase in biolink_categories_ontology_depths or category_iri in biolink_ont.nodes(), category
