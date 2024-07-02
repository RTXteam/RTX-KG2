#!/usr/bin/env python3
''' query_kegg.py: Creates a JSON dump of the KEGG API

    Usage: query_kegg.py [--test] <outputFile.json>
'''

import sys
import json
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


def get_args():
    arg_parser = argparse.ArgumentParser(description='query_kegg.py: \
                                         creates a JSON dump of the KEGG API')
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def send_query(query):
    """
    :param query: This parameter provides the query we need to perform
    """
    site_request = requests.get(query)

    # We don't want the first two characters of the response
    site_response = str(site_request.content)[2:]

    # We want to split the response into lines
    results = site_response.strip().split("\\n")
    return results


def preliminary_queries():
    """
    This function runs a set of queries that are not specific to particular KEGG ids to prime the results dictionary
    """
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

    # These queries save the name of each KEGG id
    for query in list_queries:
        results = send_query(query)
        for result in results:
            result = result.split("\\t")
            if len(result) < 2:
                continue
            results_dict[result[0]] = {'name': result[1]}

    # These queries save the equivalent identifiers for each KEGG id
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

    # This query gets the metadata for KEGG
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

    # Return both the primed results dictionary and the metadata info dictionary
    return results_dict, info_dict


def create_query_lists(kegg_id_dict, num_threads):
    """
    :param kegg_id_dict: This parameter corresponds to the full KEGG id dictionary, as given by preliminary_queries()
    :param num_threads: This parameter corresponds to the number of threads we want to use to query kegg
    """
    # We need to keep track of each of our threads
    query_lists = list()

    # For each thread, we want to keep track of the KEGG_Querier we use and its own KEGG id dictionary. To do this,
    # we use a list that is length 2
    for n in range(0, num_threads):
        query_lists.append([KEGG_Querier("Thread-" + str(n)), dict()])

    # We make sure each thread is responsible for roughly the same number of queries by assigning each KEGG_Querier
    # one KEGG id at a time and cycling through all of the threads before assigning another to each thread 
    kegg_id_count = 0
    for kegg_id, val in kegg_id_dict.items():
        # We determine which thread's turn it is to get a thread by looking at the modulus of the index
        index = kegg_id_count % num_threads

        # We are adding to the dictionary corresponding to each thread, which is stored in the index 1 (second)
        # piece of data in each query_lists item. We then assign the kegg_id and its base dictionary to that place
        query_lists[index][1][kegg_id] = val

        # Then, we increase our count so we can move to the next index
        kegg_id_count += 1

    # We return the list of KEGG_Querier's and each instance's query dictionary
    return query_lists


def create_threads(num_threads, output_writer):
    """
    :param num_threads: This parameter is the number of threads that will be employed to query KEGG
    :param output_writer: This parameter is the output JSON Lines that we can write to
    """
    # First, we need to create the preliminary queries to prime the results dictionary with all of the KEGG ids
    kegg_id_dict, info_dict = preliminary_queries()

    # Then, we need to write the info dictionary to the output first, so that the first line accessed will have KEGG's
    # metadata to create the source node
    output_writer.write({"info": info_dict})

    # We need to divide up the nodes in the kegg_id_dict based on the number of threads
    query_lists = create_query_lists(kegg_id_dict, num_threads)

    # We need to keep track of all of the different threads we create, so we use a list to do so
    threads = list()

    # Log the number of queriers we are using
    print("Number of queriers: ", len(query_lists))
    print("Starting at", kg2_util.date())

    # Go through each KEGG_Querier instance and the set of KEGG ids associated with it
    for kegg_querier, query_dict in query_lists:
        # Note the number of KEGG ids this thread is responsible for
        print(kegg_querier.name + ": " + str(len(query_dict)))

        # Create a thread on this KEGG_Querier instance's run_set_of_queries function using the corresponding
        # KEGG ids dictionary
        thread = threading.Thread(target=kegg_querier.run_set_of_queries, args=(query_dict,))

        # Start the thread and add it to our list of threads for tracking purposes
        thread.start()
        threads.append(thread)

    # Indicate that we are waiting for each thread to complete before moving on
    for thread in threads:
        thread.join()

    # Add every KEGG id results dictionary from each KEGG_Querier to the output file
    for kegg_querier, query_dict in query_lists:
        for item in kegg_querier.output_list:
            output_writer.write(item)


class KEGG_Querier:
    def __init__(self, name):
        """
        :param name: This parameter is the given name for this thread
        """
        # This is the output list for this querier. We can't write directly to the JSON Lines format because there would be clashing
        # between the different threads, leading to garbage results
        self.output_list = list()

        # Naming each querier makes it much easier to keep track of what is happening on each querier (when there are resends/
        # or processing count achievements)
        self.name = name


    def process_get_query(self, results, results_dict, kegg_id):
        """
        :param results: This parameter is a list of results from the KEGG query
        :param results_dict: This parameter has the starting results dictionary, with name and eq_id information, that we will add to
        :param kegg_id: This parameter is the kegg_id that we are working with, so we can save it with the returned information
        """

        # We start by seeding the previous_line_starter as empty
        previous_line_starter = ''
        for line in results:
            # Skip empty lines
            if len(line) < 1 or line == '///':
                continue

            # If a line starts with a space, it is a subset of the previous line(s), so we have to add the current line to the
            # list of data given by the original key for this set of lines. The lines are stripped on addition because the
            # spacing contains information
            if line.startswith(' '):
                # If there have already been two lines in this set, it will already exist as a list in the results set and
                # we only need to add the current line
                if isinstance(results_dict[previous_line_starter], list):
                    results_dict[previous_line_starter].append(line.strip())

                # If there's only been one line so far in this set, we need to reset it as a list, adding both lines into the
                # line's new list form
                else:
                    previous_result = results_dict[previous_line_starter]
                    results_dict[previous_line_starter] = list()
                    results_dict[previous_line_starter].append(previous_result.strip())
                    results_dict[previous_line_starter].append(line.strip())
            else:
                # There are two pieces of information in the data: the line starter and the line data
                line = line.split(' ', 1)
                line_starter = line[0]

                # If we have already encountered the line starter, we need to treat it the same way
                # we treated the lines that started with a space (see above)
                if line_starter in results_dict:
                    if isinstance(results_dict[line_starter], list):
                        results_dict[line_starter].append(line[1].strip())
                    else:
                        previous_result = results_dict[line_starter]
                        results_dict[line_starter] = list()
                        results_dict[line_starter].append(previous_result.strip())
                        results_dict[line_starter].append(line[1].strip())

                # If we haven't seen it before, we need to add the key to the results dictionary
                else:
                    try:
                        results_dict[line_starter] = line[1].strip()
                    except IndexError:
                        results_dict[line_starter] = ''
                previous_line_starter = line_starter

        # Once we have processed every line, we need to add the output list
        self.output_list.append({kegg_id: results_dict})


    def run_set_of_queries(self, kegg_id_dict):
        """
        :param kegg_id_dict: This parameter provides the list of KEGG ids this thread is responsible for
        """
        # Defining the base URL for every KEGG id query
        get_base_query = "http://rest.kegg.jp/get/"

        # Keep track of our progress compared to the number of queries we have left
        kegg_ids_total = len(kegg_id_dict.keys())
        get_count = 0

        for kegg_id in kegg_id_dict:
            previous_line_starter = ''

            # If we have a connection issue (which will cause a parsing error), spin until it works, but put a note in the log
            while True:
                try:
                    # We retreive the data for each KEGG id from the API, then process it
                    results = send_query(get_base_query + kegg_id)
                    self.process_get_query(results, kegg_id_dict[kegg_id], kegg_id)

                # The index error occurs because the processing step cannot parse an error page
                except IndexError:
                    # Place a note in the log file
                    print("Trying again with", kegg_id, "at count", get_count, "on thread", self.name)

                    # We want to sleep for a random time to try and counteract when the other threads may or may not be sleeping
                    # or going in general. We DO NOT want to hit this, because it substantially slows down the code. The optimal
                    # number of threads will have this except statement never hit.
                    time.sleep(random.randint(1, 5))

                    # Continue to the next loop so the query will run again
                    continue

                # Once we have finished processing the query successfully, we want to break this loop
                else:
                    break

            # Increase the count only once we have a successful query completion
            get_count += 1

            # Since we use threads, we want to record in our progress in small incremements and document the thread
            if get_count % 100 == 0:
                print("Processed", get_count, "out of", kegg_ids_total, "at", kg2_util.date(), "on thread", self.name)


if __name__ == '__main__':
    args = get_args()
    output_file_name = args.outputFile

    # We need to create the output JSON Lines file
    output_info = kg2_util.create_single_jsonlines(True)
    output_writer = output_info[0]

    # We need to get all of the KEGG data. It is slow to serially query the API, so we want to use threads.
    # Six threads seems to be the maximum we can achieve without having to spin to work.
    create_threads(6, output_writer)

    # We need to close the JSON Lines output, so it saves to the output file
    kg2_util.close_single_jsonlines(output_info, output_file_name)
