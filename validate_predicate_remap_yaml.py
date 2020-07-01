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
    return arg_parser


args = make_arg_parser().parse_args()
curies_to_urls_map_file_name = args.curiesToURLsMapFile
predicate_remap_file_name = args.predicateRemapFile

curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_urls_map_file_name))
curies_to_url_map_data_bidir = {next(iter(listitem.keys())) for listitem in curies_to_url_map_data['use_for_bidirectional_mapping']}

map_data = yaml.safe_load(open(predicate_remap_file_name, 'r'))
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
