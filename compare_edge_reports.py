#!/usr/bin/env python3
'''compare_edge_reports.py: Checks for drastic differences between
    two KG2 JSON report JSON files.

   Usage: compare_edge_reports.py [--test] <previousFile.json>
            <currentFile.json>
'''

import json
import argparse
import kg2_util
import sys

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

def get_args():
    description = 'Checks for drastic differences between \
                   two KG2 JSON report JSON files.'
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('previousFile', type=str)
    argparser.add_argument('currentFile', type=str)
    return argparser.parse_args()

def get_percent_decrease(num1, num2):
    return (num1 - num2) / num1


if __name__ == '__main__':
    args = get_args()
    previous_json = dict()
    current_json = dict()
    with open(args.previousFile, 'r') as previous_file:
        previous_json = json.load(previous_file)
    with open(args.currentFile, 'r') as current_file:
        current_json = json.load(current_file)
    previous_edge_sources = previous_json['number_of_edges_by_source']
    current_edge_sources = current_json['number_of_edges_by_source']

    for source in previous_edge_sources:
        edge_count = previous_edge_sources[source]
        current_edge_count = current_edge_sources.get(source, None)
        if current_edge_count == None or current_edge_count == 0:
            message = f"There are no edges from {source} in this build. \
                        There were {edge_count} in the previous build."
            kg2_util.log_message(message.replace('  ', ''),
                                 output_stream=sys.stderr)
            continue
        if get_percent_decrease(edge_count, current_edge_count) > 0.2:
            message = f"There was a significant drop in edges from {source} \
                        in this build. The count dropped from {edge_count} \
                        to {current_edge_count}"
            kg2_util.log_message(message.replace('  ', ''),
                                 output_stream=sys.stderr)
