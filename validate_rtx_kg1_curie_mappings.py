#! /usr/bin/env python3
'''Checks the KG1_PROVIDED_BY_TO_KG2_IRIS in "rtx_kg1_neo4j_to_kg_json.py"
   script for correctness.  This script should be run each time
   `rtx_kg1_neo4j_to_kg_json.py` or `curies-to-urls-map.yaml` or
   `biolink-model.owl` is changed.

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
import rtx_kg1_neo4j_to_kg_json


curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('curies-to-urls-map.yaml'))
curies_to_url_map_data_bidir = {next(iter(listitem.keys())) for listitem in curies_to_url_map_data['use_for_bidirectional_mapping']}

curie_prefixes = set(curie_id.split(':')[0] for curie_id in rtx_kg1_neo4j_to_kg_json.KG1_PROVIDED_BY_TO_KG2_IRIS.values())
for curie_prefix in curie_prefixes:
    assert curie_prefix in curies_to_url_map_data_bidir, curie_prefix

