#!/usr/bin/env python3
'''Checks the file "curies-to-categories.yaml" for correctness.  This script
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

import kg2_util
import ontobio

curies_to_categories_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('curies-to-categories.yaml'))
curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('curies-to-urls-map.yaml'))
curies_to_url_map_data_bidir = {next(iter(listitem.keys())) for listitem in curies_to_url_map_data['use_for_bidirectional_mapping']}

biolink_ont = ontobio.ontol_factory.OntologyFactory().create("biolink-model.owl")
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
