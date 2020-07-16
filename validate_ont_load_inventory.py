#!/usr/bin/env python3
'''Checks the file `ont-load-inventory.yaml` for correctness.  This script
   should be run each time `ont-load-inventory.yaml` or
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
    arg_parser.add_argument('umls2rdfConfFile', type=str)
    return arg_parser


args = make_arg_parser().parse_args()
owl_load_inventory_file_name = args.owlLoadInventoryFile
curies_to_urls_map_file_name = args.curiesToURLsMapFile
umls2rdf_conf_file_name = args.umls2rdfConfFile
owl_load_inventory_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(owl_load_inventory_file_name))

umls_ttl_files = None
with open(umls2rdf_conf_file_name, 'r') as umls2rdf_conf_file:
    umls_ttl_files = {line.split(",")[1] for line in umls2rdf_conf_file.read().splitlines() if len(line) > 0 and not line.startswith('#')}
    umls2rdf_conf_file.close()
umls_ttl_files.add('umls-semantictypes.ttl')

assert os.path.exists(BIOLINK_MODEL_OWL)
biolink_ont = kg2_util.load_ontology_from_owl_or_json_file(BIOLINK_MODEL_OWL)
biolink_categories_ontology_depths = kg2_util.get_biolink_categories_ontology_depths(biolink_ont)

iri_shortener = kg2_util.make_uri_to_curie_shortener(kg2_util.make_curies_to_uri_map(kg2_util.read_file_to_string(curies_to_urls_map_file_name),
                                                                                     kg2_util.IDMapperType.CONTRACT))

source_files_in_inventory = {list_item['file'] for list_item in owl_load_inventory_data if list_item['file'].startswith('umls-')}

assert source_files_in_inventory == umls_ttl_files, str(source_files_in_inventory.symmetric_difference(umls_ttl_files))

for list_item in owl_load_inventory_data:
    url = list_item['url']
    assert url is not None, url
    assert iri_shortener(url) is not None, "unable to shorten: " + url
