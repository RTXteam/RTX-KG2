#!/usr/bin/env python3
''' validate_provided_by_to_infores_map.py: checks the file 
    `kg2-provided-by-curie-to-infores-curie.yaml` for correctness

    Usage: validate_provided_by_to_infores_map.py <kg2ProvidedByCurieToInforesCurieFile.yaml>
    <inforesCatalogFile.yaml>
'''

import kg2_util
import argparse
import json

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

def get_args():
    description = 'validate_provided_by_to_infores_map_yaml.py: checks the file `kg2-provided-by-curie-to-infores-curie.yaml` for correctness.'
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('kg2ProvidedByCurieToInforesCurieFile', type=str)
    arg_parser.add_argument('inforesCatalogFile', type=str)
    return arg_parser.parse_args()


def make_infores_look_up(infores_catalog):
    infores_dict = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(infores_catalog))
    infores_look_up = dict()
    for infores_entry in infores_dict['information_resources']:
        infores_name = infores_entry['name']
        infores_curie = infores_entry['id']
        if infores_name not in infores_look_up:
            infores_look_up[infores_name] = list()
        infores_look_up[infores_name].append(infores_curie)
    return infores_look_up


def make_kg2_infores_look_up(infores_map):
    kg2_infores_look_up = dict()
    infores_map_dict = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(infores_map))
    for infores_map_entry in infores_map_dict:
        infores_map_name = infores_map_dict[infores_map_entry]['source_name']
        infores_map_curie = infores_map_dict[infores_map_entry]['infores_curie']
        if infores_map_name not in kg2_infores_look_up:
            kg2_infores_look_up[infores_map_name] = list()
        kg2_infores_look_up[infores_map_name].append(infores_map_curie)
    return kg2_infores_look_up


def validate_infores_curies(infores_look_up, kg2_infores_look_up):
    name_exceptions = []
    for kg2_infores_name in kg2_infores_look_up:
        kg2_infores_curies = kg2_infores_look_up[kg2_infores_name]
        exceptions = False
        for name in name_exceptions:
            exceptions = name == kg2_infores_name or exceptions
        if kg2_infores_name not in infores_look_up:
            print(kg2_infores_name)
        # assert kg2_infores_name in infores_look_up or exceptions, kg2_infores_name
        for kg2_infores_curie in kg2_infores_curies:
            assert exceptions or kg2_infores_curie in infores_look_up[kg2_infores_name], kg2_infores_curie + ' ' + str(infores_look_up[kg2_infores_name])
    return name_exceptions


if __name__ == '__main__':
    args = get_args()
    infores_catalog = args.inforesCatalogFile
    infores_map = args.kg2ProvidedByCurieToInforesCurieFile
    infores_look_up = make_infores_look_up(infores_catalog)
    kg2_infores_look_up = make_kg2_infores_look_up(infores_map)
    name_exceptions = validate_infores_curies(infores_look_up, kg2_infores_look_up)
    if len(name_exceptions) > 0:
        print('Warning, exceptions present for infores CURIEs with the following names in the mapping file:', name_exceptions)
