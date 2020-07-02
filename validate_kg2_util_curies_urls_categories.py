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

import argparse
import kg2_util


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='validate_kg2_util_curies_urls_categories.py: ' +
                                         'checks the file `kg2_util.py` for correctness for its CURIE IDs, Base URLs, and biolink categories.')
    arg_parser.add_argument('curiesToCategoriesFile', type=str)
    arg_parser.add_argument('curiesToURLsMapFile', type=str)
    return arg_parser


args = make_arg_parser().parse_args()
curies_to_categories_file_name = args.curiesToCategoriesFile
curies_to_urls_map_file_name = args.curiesToURLsMapFile

iri_shortener = kg2_util.make_uri_to_curie_shortener(kg2_util.make_curies_to_uri_map(kg2_util.read_file_to_string(curies_to_urls_map_file_name),
                                                                                     kg2_util.IDMapperType.CONTRACT))

curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_urls_map_file_name))
curies_to_url_map_data_bidir = {key: listitem[key] for listitem in curies_to_url_map_data['use_for_bidirectional_mapping'] for key in listitem.keys()}

curies_to_url_map_data_cont = {key: listitem[key] for listitem in curies_to_url_map_data['use_for_contraction_only'] for key in listitem.keys()}

curies_to_categories_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_categories_file_name))

categories_to_check = set(list(curies_to_categories_data['prefix-mappings'].values()) +
                          list(curies_to_categories_data['term-mappings'].values()))

for variable_name in dir(kg2_util):
    if variable_name.startswith('CURIE_PREFIX_'):
        assert getattr(kg2_util, variable_name) in curies_to_url_map_data_bidir, variable_name
    elif variable_name.startswith('BASE_URL_'):
        url_str = getattr(kg2_util, variable_name)
        curie = iri_shortener(url_str)
        assert curie is not None, url_str
    elif variable_name.startswith('BIOLINK_CATEGORY_'):
        category_label = getattr(kg2_util, variable_name)
        assert category_label in categories_to_check, category_label
    elif variable_name.startswith('CURIE_ID_'):
        curie_id = getattr(kg2_util, variable_name)
        assert ':' in curie_id, variable_name
        assert curie_id.split(':')[0] in curies_to_url_map_data_bidir, variable_name
    elif variable_name.startswith('IRI_'):
        url = getattr(kg2_util, variable_name)
        assert iri_shortener(url) is not None, url
