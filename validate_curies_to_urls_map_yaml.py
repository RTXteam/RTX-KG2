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

import yaml

BIDIR = 'use_for_bidirectional_mapping'
CONT = 'use_for_contraction_only'
EXPA = 'use_for_expansion_only'

TOP_KEYS = {BIDIR, CONT, EXPA}

map_data = yaml.safe_load(open('curies-to-urls-map.yaml', 'r'))
assert set(map_data.keys()) == TOP_KEYS

map_data_bidir_list = map_data[BIDIR]
map_data_expa_list = map_data[EXPA]
map_data_cont_list = map_data[CONT]


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


# construct maps

map_data_bidir = make_map_from_list(map_data_bidir_list, reverse=False)
map_data_expa = make_map_from_list(map_data_expa_list, reverse=False)
map_data_cont = make_map_from_list(map_data_cont_list, reverse=True)

# none of the CURIE prefixes in expa should appear in bidir:
overlap_set = set(iter(map_data_bidir.keys())) & set(iter(map_data_expa.keys()))
assert len(overlap_set) == 0, str(overlap_set)

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
