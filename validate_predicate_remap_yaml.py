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

import yaml

curies_to_url_map_data = yaml.safe_load(open('curies-to-urls-map.yaml', 'r'))
curies_to_url_map_data_bidir = {next(iter(listitem.keys())) for listitem in curies_to_url_map_data['use_for_bidirectional_mapping']}

map_data = yaml.safe_load(open('predicate-remap.yaml', 'r'))
for relation_curie, instructions_dict in map_data.items():
    for instruction, instructions_list in instructions_dict.items():
        if instruction == 'keep':
            relation_curie_to_check = relation_curie
        elif instruction == 'delete':
            continue
        else:
            relation_curie_to_check = instructions_list[1]
        curie_prefix = relation_curie_to_check.split(':')[0]
        assert curie_prefix in curies_to_url_map_data_bidir, relation_curie_to_check
