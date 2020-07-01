#!/usr/bin/env python3
'''Checks the CURIE_PREFIX_... constants in "kg2_util.py"
   script for correctness.  This script should be run each time
   `kg2_utiul.py` or `curies-to-urls-map.yaml` is changed.
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

curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('curies-to-urls-map.yaml'))
curies_to_url_map_data_bidir = {key: listitem[key] for listitem in curies_to_url_map_data['use_for_bidirectional_mapping'] for key in listitem.keys()}

curies_to_url_map_data_cont = {key: listitem[key] for listitem in curies_to_url_map_data['use_for_contraction_only'] for key in listitem.keys()}

curies_to_categories_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('curies-to-categories.yaml'))

categories_to_check = set(list(curies_to_categories_data['prefix-mappings'].values()) +
                          list(curies_to_categories_data['term-mappings'].values()))

for variable_name in dir(kg2_util):
    if variable_name.startswith('CURIE_PREFIX_'):
        assert getattr(kg2_util, variable_name) in curies_to_url_map_data_bidir, variable_name
    elif variable_name.startswith('BASE_URL_'):
        url_str = getattr(kg2_util, variable_name)
        found_match = False
        for map_url in curies_to_url_map_data_bidir.values():
            if map_url.startswith(map_url):
                found_match = True
                break
        if not found_match:
            for map_url in curies_to_url_map_data_cont.values():
                if map_url.startswith(map_url):
                    found_match = True
                    break
        assert found_match, "URL mismatch: " + variable_name
    elif variable_name.startswith('BIOLINK_CATEGORY_'):
        category_label = getattr(kg2_util, variable_name)
        assert category_label in categories_to_check, category_label
    elif variable_name.startswith('CURIE_ID_'):
        curie_id = getattr(kg2_util, variable_name)
        assert ':' in curie_id, variable_name
        assert curie_id.split(':')[0] in curies_to_url_map_data_bidir, variable_name
    elif variable_name.startswith('IRI_'):
        url = getattr(kg2_util, variable_name)
        found_match = False
        for map_url in curies_to_url_map_data_bidir.values():
            if url.startswith(map_url):
                found_match = True
                break
        assert found_match, 'URL mismatch: ' + variable_name
