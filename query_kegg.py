#!/usr/bin/env python3
''' query_kegg.py: Creates a JSON dump of the KEGG API

    Usage: query_kegg.py [--test] <outputFile.json>
'''

import sys
import json
from cache_control_helper import CacheControlHelper
import datetime
import argparse
import kg2_util


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood', 'Deqing Qu']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_args():
    arg_parser = argparse.ArgumentParser(description='query_kegg.py: \
                                         creates a JSON dump of the KEGG API')
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def send_query(query):
    requests = CacheControlHelper()
    res = requests.get(query, timeout=120)
    return res.text


def process_get_query(get_results, results_dict, kegg_id):
    previous_line_starter = ''
    for line in get_results.split('\n'):
        if len(line) < 1 or line == '///':
            continue
        if line.startswith(' '):
            if isinstance(results_dict[kegg_id][previous_line_starter], list):
                results_dict[kegg_id][previous_line_starter].append(line.strip())
            else:
                previous_result = results_dict[kegg_id][previous_line_starter]
                results_dict[kegg_id][previous_line_starter] = list()
                results_dict[kegg_id][previous_line_starter].append(previous_result.strip())
                results_dict[kegg_id][previous_line_starter].append(line.strip())
        else:
            line = line.split(' ', 1)
            line_starter = line[0]
            if line_starter in results_dict[kegg_id]:
                if isinstance(results_dict[kegg_id][line_starter], list):
                    results_dict[kegg_id][line_starter].append(line[1].strip())
                else:
                    previous_result = results_dict[kegg_id][line_starter]
                    results_dict[kegg_id][line_starter] = list()
                    results_dict[kegg_id][line_starter].append(previous_result.strip())
                    results_dict[kegg_id][line_starter].append(line[1].strip())
            else:
                try:
                    results_dict[kegg_id][line_starter] = line[1].strip()
                except IndexError:
                    results_dict[kegg_id][line_starter] = ''
            previous_line_starter = line_starter
    return results_dict


def run_queries():
    results_dict = {}
    list_queries = ["http://rest.kegg.jp/list/pathway/hsa",
                    "http://rest.kegg.jp/list/compound",
                    "http://rest.kegg.jp/list/glycan",
                    "http://rest.kegg.jp/list/reaction",
                    "http://rest.kegg.jp/list/enzyme",
                    "http://rest.kegg.jp/list/drug"]
    conv_queries = ["http://rest.kegg.jp/conv/compound/chebi",
                    "http://rest.kegg.jp/conv/glycan/chebi",
                    "http://rest.kegg.jp/conv/drug/chebi"]
    get_base_query = "http://rest.kegg.jp/get/"
    for query in list_queries:
        for results in send_query(query).split('\n'):
            if len(results) < 1:
                continue
            results = results.split('\t')
            results_dict[results[0]] = {'name': results[1]}
    for query in conv_queries:
        for results in send_query(query).split('\n'):
            if len(results) < 1:
                continue
            results = results.split('\t')
            results_dict[results[1]]['eq_id'] = results[0]
    kegg_ids = len(results_dict.keys())
    get_count = 0
    for kegg_id in results_dict:
        previous_line_starter = ''
        results = send_query(get_base_query + kegg_id)
        results_dict = process_get_query(results, results_dict, kegg_id)
        get_count += 1
        if get_count % 1000 == 0:
            print("Processed", get_count, "out of", kegg_ids, "at", date())
    return results_dict


if __name__ == '__main__':
    args = get_args()
    kg2_util.save_json(run_queries(), args.outputFile, True)
