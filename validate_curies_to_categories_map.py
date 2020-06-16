#!/usr/bin/env python3
'''Checks the file "curies-to-categories.yaml" for correctness.
   This script should be run each time `curies-to-categories.yaml` is changed.'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import kg2_util


curies_to_categories_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('curies-to-categories.yaml'))
curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('curies-to-urls-map.yaml'))
curies_to_url_map_data_bidir = {next(iter(listitem.keys())) for listitem in curies_to_url_map_data['use_for_bidirectional_mapping']}

for prefix in curies_to_categories_data['prefix-mappings'].keys():
    assert prefix in curies_to_url_map_data_bidir, prefix

for curie_id in curies_to_categories_data['term-mappings'].keys():
    prefix = curie_id.split(':')[0]
    assert prefix in curies_to_url_map_data_bidir, prefix
