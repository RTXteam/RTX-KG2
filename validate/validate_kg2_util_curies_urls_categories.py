#!/usr/bin/env python3
'''Checks the CURIE_PREFIX_... constants in "kg2_util.py"
   script for correctness.  This script should be run each time
   `kg2_utiul.py` or `curies-to-urls-map.yaml` is changed.
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
import json

def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='validate_kg2_util_curies_urls_categories.py: ' +
                                         'checks the file `kg2_util.py` for correctness for its CURIE IDs, Base URLs, and biolink categories.')
    arg_parser.add_argument('curiesToURLsMapFile', type=str)
    arg_parser.add_argument('biolinkModelURL', type=str)
    arg_parser.add_argument('biolinkModelLocalFile', type=str)
    return arg_parser

args = make_arg_parser().parse_args()
biolink_model_url = args.biolinkModelURL
biolink_model_file_name = args.biolinkModelLocalFile
curies_to_urls_map_file_name = args.curiesToURLsMapFile

curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_urls_map_file_name))
curies_to_url_map_data_bidir = {key: listitem[key] for listitem in curies_to_url_map_data['use_for_bidirectional_mapping'] for key in listitem.keys()}

curies_to_url_map_data_cont = {key: listitem[key] for listitem in curies_to_url_map_data['use_for_contraction_only'] for key in listitem.keys()}

valid_base_urls = list()
valid_base_urls += [value for value in curies_to_url_map_data_bidir.values()]
valid_base_urls += [value for value in curies_to_url_map_data_cont.values()]

kg2_util.download_file_if_not_exist_locally(biolink_model_url, biolink_model_file_name)
biolink_model = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(biolink_model_file_name))
biolink_edge_labels, biolink_categories = kg2_util.identify_biolink_terms(biolink_model)

for variable_name in dir(kg2_util):
    variable_value = getattr(kg2_util, variable_name)
    if variable_name.startswith('CURIE_PREFIX_'):
        assert variable_value in curies_to_url_map_data_bidir, variable_name
    elif variable_name.startswith('BASE_URL_'):
        url_str = variable_value
        assert url_str in valid_base_urls, url_str
    elif variable_name.startswith('BIOLINK_CATEGORY_'):
        category_label = variable_value
        assert category_label in biolink_categories, category_curie
        #  assert category_label in categories_to_check, category_label
    elif variable_name.startswith('CURIE_ID_'):
        curie_id = variable_value
        assert ':' in curie_id, variable_name
        assert curie_id.split(':')[0] in curies_to_url_map_data_bidir, variable_name
    elif variable_name.startswith('EDGE_LABEL_BIOLINK_'):
        relation_label = variable_value.replace('_', ' ')
        assert relation_label in biolink_edge_labels, relation_label
