#!/usr/bin/env python3

import inspect
import os
import pprint
import requests
import sys
import yaml

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import kg2_util

BIOLINK_CURIE_PREFIX = kg2_util.CURIE_PREFIX_BIOLINK
EDGE_NORM_BASE_URL = 'https://edgenormalization-sri.renci.org/resolve_predicate'

HTTP_STATUS_CODE_GOOD = 200

query_results = dict()
raw_curies_to_query = dict()
pred_map = yaml.safe_load(open('../predicate-remap.yaml', 'r'))
for raw_curie, map_entry in pred_map.items():
    map_inst, map_details = next(iter(map_entry.items()))
    if not raw_curie.startswith(BIOLINK_CURIE_PREFIX) and map_inst == 'keep':
        query_results[raw_curie] = None
        raw_curies_to_query[raw_curie] = raw_curie
        continue
    if map_details is not None:
        new_curie = map_details[1]
        if not new_curie.startswith(BIOLINK_CURIE_PREFIX):
            query_results[new_curie] = None
            raw_curies_to_query[raw_curie] = new_curie
req_res = requests.get(EDGE_NORM_BASE_URL,
                       params={'version': 'latest',
                               'predicate': [pred_curie for pred_curie in query_results.keys()]})
http_status_code = req_res.status_code
if http_status_code != HTTP_STATUS_CODE_GOOD:
    sys.exit("unexpected HTTP status code [" + str(http_status_code) + "] from predicate normalization service")
res_json = req_res.json()
for pred_curie, pred_map_info in res_json.items():
    assert pred_curie in query_results
    if len(pred_map_info) > 0:
        res_curie = pred_map_info['identifier']
        if ':' not in res_curie:
            print("WARNING: for query CURIE ID " + pred_curie + ", the returned identifier (" + res_curie +
                  ") does not appear to be a CURIE prefix; going to boldly prepend a biolink CURIE prefix",
                  file=sys.stderr)
            res_curie = BIOLINK_CURIE_PREFIX + ':' + res_curie
        query_results[pred_curie] = [pred_map_info['label'],
                                     res_curie]

for raw_curie, query_curie in raw_curies_to_query.items():
    query_res = query_results[query_curie]
    map_entry = pred_map[raw_curie]
    pred_map_inst, pred_map_details = next(iter(map_entry.items()))
    if query_res is not None:
        new_curie = query_res[1]
        if pred_map_details is not None:
            orig_mapped_curie = pred_map_details[1]
        else:
            orig_mapped_curie = None
        if new_curie != raw_curie or (orig_mapped_curie is not None and orig_mapped_curie != new_curie):
            if pred_map_inst == 'keep':
                pred_map_dict = {'rename': query_res}
            elif pred_map_inst == 'rename':
                if new_curie != raw_curie:
                    pred_map_dict = {'rename': query_res}
                else:
                    pred_map_dict = {'keep': None}
            elif pred_map_inst == 'invert':
                pred_map_dict = {'invert': query_res}
            else:
                assert "Unexpected instruction: " + pred_map_inst + " for raw CURIE " + raw_curie
            pred_map[raw_curie] = pred_map_dict
yaml.Dumper.ignore_aliases = lambda *args: True
with open('predicate-remap-new.yaml', 'w') as output_file:
    yaml.dump(pred_map, output_file, sort_keys=True)
