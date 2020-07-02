#!/usr/bin/env python3
'''Checks the file `owl-load-inventory.yaml` for correctness.  This script
   should be run each time `owl-load-inventory.yaml` or
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
import os.path

BIOLINK_MODEL_OWL = kg2_util.BIOLINK_MODEL_OWL


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='validate_curies_to_categories.py: checks the file `curies-to-categories.yaml` for correctness.')
    arg_parser.add_argument('owlLoadInventoryFile', type=str)
    arg_parser.add_argument('curiesToURLsMapFile', type=str)
    return arg_parser


args = make_arg_parser().parse_args()
owl_load_inventory_file_name = args.owlLoadInventoryFile
curies_to_urls_map_file_name = args.curiesToURLsMapFile
owl_load_inventory_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(owl_load_inventory_file_name))
# curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_urls_map_file_name))
# curies_to_url_map_data_bidir = {next(iter(listitem.keys())) for listitem in curies_to_url_map_data['use_for_bidirectional_mapping']}

assert os.path.exists(BIOLINK_MODEL_OWL)
biolink_ont = kg2_util.load_ontology_from_owl_or_json_file(BIOLINK_MODEL_OWL)
biolink_categories_ontology_depths = kg2_util.get_biolink_categories_ontology_depths(biolink_ont)

iri_shortener = kg2_util.make_uri_to_curie_shortener(kg2_util.make_curies_to_uri_map(kg2_util.read_file_to_string(curies_to_urls_map_file_name),
                                                                                     kg2_util.IDMapperType.CONTRACT))

for list_item in owl_load_inventory_data:
    url = list_item['url']
    assert url is not None, url
