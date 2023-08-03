#!/usr/bin/env python3
''' query_kegg.py: Creates a JSON dump of the KEGG API

    Usage: query_kegg.py [--test] <outputFile.json>
'''

import sys
import json
import datetime
import argparse
import kg2_util
import requests
import threading
import time
import random


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood', 'Deqing Qu', 'Liliana Acevedo']
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
    site_request = requests.get(query)
    site_response = str(site_request.content)[2:]
    results = site_response.strip().split("\\n")
    return results


def preliminary_queries():
    results_dict = dict()
    info_queries = ["http://rest.kegg.jp/info/kegg/"]
    list_queries = ["http://rest.kegg.jp/list/pathway/hsa",
                    "http://rest.kegg.jp/list/compound",
                    "http://rest.kegg.jp/list/glycan",
                    "http://rest.kegg.jp/list/reaction",
                    "http://rest.kegg.jp/list/enzyme",
                    "http://rest.kegg.jp/list/drug"]
    conv_queries = ["http://rest.kegg.jp/conv/compound/chebi",
                    "http://rest.kegg.jp/conv/glycan/chebi",
                    "http://rest.kegg.jp/conv/drug/chebi"]

    for query in list_queries:
        results = send_query(query)
        for result in results:
            result = result.split("\\t")
            if len(result) < 2:
                continue
            results_dict[result[0]] = {'name': result[1]}

    for query in conv_queries:
        results = send_query(query)
        for result in results:
            if len(result) < 1:
                continue
            result = result.split('\\t')
            if len(result) > 1:
                if result[1] not in results_dict:
                    results_dict[result[1]] = {}
                results_dict[result[1]]['eq_id'] = result[0]

    info_dict = {}
    for query in info_queries:
        results = send_query(query)
        for result in results:
            result = result.strip("kegg").strip().split()
            if len(results) < 1:
                continue
            if result[0] == "Release":
                info_dict['version'] = result[1].split('/')[0].strip('+')
                info_dict['update_date'] = result[2] + '-' + result[3]

    return results_dict, info_dict


def create_query_lists(kegg_id_dict, num_threads):
    query_lists = list()
    for n in range(0, num_threads):
        query_lists.append([KEGG_Querier("Thread-" + str(n)), dict()])

    kegg_id_count = 0
    for kegg_id, val in kegg_id_dict.items():
        index = kegg_id_count % num_threads
        query_lists[index][1][kegg_id] = val
        kegg_id_count += 1

    return query_lists


def create_threads(num_threads, output_writer):
    kegg_id_dict, info_dict = preliminary_queries()
    output_writer.write({"info": info_dict})
    query_lists = create_query_lists(kegg_id_dict, num_threads)

    threads = list()
    print("Number of queriers: ", len(query_lists))
    print("Starting at", kg2_util.date())
    for kegg_querier, query_dict in query_lists:
        print(kegg_querier.name + ": " + str(len(query_dict)))
        thread = threading.Thread(target=kegg_querier.run_set_of_queries, args=(query_dict,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    for kegg_querier, query_dict in query_lists:
        for item in kegg_querier.output_list:
            output_writer.write(item)


class KEGG_Querier:
    def __init__(self, name):
        self.output_list = list()
        self.name = name


    def process_get_query(self, results, results_dict, kegg_id):
        previous_line_starter = ''
        for line in results:
            if len(line) < 1 or line == '///':
                continue
            if line.startswith(' '):
                if isinstance(results_dict[previous_line_starter], list):
                    results_dict[previous_line_starter].append(line.strip())
                else:
                    previous_result = results_dict[previous_line_starter]
                    results_dict[previous_line_starter] = list()
                    results_dict[previous_line_starter].append(previous_result.strip())
                    results_dict[previous_line_starter].append(line.strip())
            else:
                line = line.split(' ', 1)
                line_starter = line[0]
                if line_starter in results_dict:
                    if isinstance(results_dict[line_starter], list):
                        results_dict[line_starter].append(line[1].strip())
                    else:
                        previous_result = results_dict[line_starter]
                        results_dict[line_starter] = list()
                        results_dict[line_starter].append(previous_result.strip())
                        results_dict[line_starter].append(line[1].strip())
                else:
                    try:
                        results_dict[line_starter] = line[1].strip()
                    except IndexError:
                        results_dict[line_starter] = ''
                previous_line_starter = line_starter
        self.output_list.append({kegg_id: results_dict})


    def run_set_of_queries(self, kegg_id_dict):
        get_base_query = "http://rest.kegg.jp/get/"
        kegg_ids = len(kegg_id_dict.keys())
        get_count = 0

        for kegg_id in kegg_id_dict:
            previous_line_starter = ''

            # If we have a connection issue (which will cause a parsing error), spin until it works, but put a note in the log
            while True:
                try:
                    results = send_query(get_base_query + kegg_id)
                    self.process_get_query(results, kegg_id_dict[kegg_id], kegg_id)
                except IndexError:
                    print("Trying again with", kegg_id, "at count", get_count, "on thread", self.name)
                    # We want to sleep for a random time to try and counteract when the other threads may or may not be sleeping
                    # or going in general
                    time.sleep(random.randint(1, 5))
                    continue
                else:
                    break
            get_count += 1
            if get_count % 100 == 0:
                print("Processed", get_count, "out of", kegg_ids, "at", date(), "on thread", self.name)


if __name__ == '__main__':
    args = get_args()
    output_file_name = args.outputFile

    output_info = kg2_util.create_single_jsonlines(True)
    output_writer = output_info[0]

    # Six threads seems to be the maximum we can achieve without having to spin to work
    create_threads(6, output_writer)

    kg2_util.close_single_jsonlines(output_info, output_file_name)