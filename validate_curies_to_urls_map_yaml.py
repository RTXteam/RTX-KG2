#!/usr/bin/env python3
'''Checks the file `curies-to-urls-map.yaml` for correctness.
   This script should be run each time `curies-to-urls-map.yaml` is changed.'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import argparse
import json
import sys
import yaml

BIDIR = 'use_for_bidirectional_mapping'
CONT = 'use_for_contraction_only'
EXPA = 'use_for_expansion_only'

TOP_KEYS = {BIDIR, CONT, EXPA}


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='validate_curies_to_urls_map.py: checks the file `curies-to-urls-map.yaml` for correctness.')
    arg_parser.add_argument('curiesToURLsMapFile', type=str)
    arg_parser.add_argument('biolinkContextJsonLDFile', type=str)
    return arg_parser


def make_map_from_list(thelist: list, reverse: bool) -> dict:
    ret_map = dict()
    for submap in thelist:
        assert len(submap) == 1
        subkey = next(iter(submap.keys()))
        subvalue = next(iter(submap.values()))
        if reverse:
            temp = subkey
            subkey = subvalue
            subvalue = temp
        assert subkey not in ret_map, subkey
        ret_map[subkey] = subvalue
    return ret_map


args = make_arg_parser().parse_args()
curies_to_urls_map_file_name = args.curiesToURLsMapFile
biolink_context_json_ld_file_name = args.biolinkContextJsonLDFile

map_data = yaml.safe_load(open(curies_to_urls_map_file_name, 'r'))
assert set(map_data.keys()) == TOP_KEYS

biolink_context_curie_prefixes = set(json.load(open(biolink_context_json_ld_file_name, 'r'))['@context'].keys())

map_data_bidir_list = map_data[BIDIR]
map_data_expa_list = map_data[EXPA]
map_data_cont_list = map_data[CONT]

# construct maps
map_data_bidir = make_map_from_list(map_data_bidir_list, reverse=False)
map_data_expa = make_map_from_list(map_data_expa_list, reverse=False)
map_data_cont = make_map_from_list(map_data_cont_list, reverse=True)

# none of the CURIE prefixes in expa should appear in bidir:
overlap_set = set(iter(map_data_bidir.keys())) & set(iter(map_data_expa.keys()))
assert len(overlap_set) == 0, str(overlap_set)

for curie_prefix in map_data_bidir.keys():
    if curie_prefix not in biolink_context_curie_prefixes:
        print("WARNING: KG2 CURIE prefix " + curie_prefix + " is not in the Biolink context.jsonld file", file=sys.stderr)
# every URL in the expa map should be a value in the bidir map_data (or at least a partial match)
bidir_map_urls = set(iter(map_data_bidir.values()))
for expa_url in map_data_expa.values():
    if expa_url not in bidir_map_urls:
        found_url_partial_match = False
        for url in bidir_map_urls:
            if url.startswith(expa_url) or expa_url.startswith(url):
                found_url_partial_match = True
                break
        assert found_url_partial_match, expa_url

# every value in the cont map should be a prefix in bidir:
for prefix in set(iter(map_data_cont.values())):
    assert prefix in map_data_bidir, prefix

# none of the URLs in the contraction map should be in the bidirectional map_data
overlap = set(iter(map_data_cont.keys())) & set(iter(map_data_bidir.values()))
assert len(overlap) == 0, str(overlap)
