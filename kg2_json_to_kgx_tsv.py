#!/usr/bin/env python3

''' Loads the KG2 simplified json file kg2-simplified.json
and writes out a nodes.tsv and edges.tsv in Translator KGX TSV format

    Usage: python3 kg2_json_to_kgx_tsv.py
'''

import json
import sys
import os
import argparse

__author__ = 'Liliana Acevedo'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def check_tab(the_string: str,
              line_ctr: int):
    assert '\t' not in the_string, "tab found on line " + str(line_ctr + 1) + \
        "; string: " + the_string
    return the_string


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='kg2_json_to_kgx_tsv.py: load a RTX-KG2pre graph in JSON format and export it to KGX TSV format')
    arg_parser.add_argument('--logFile', type=str, default='kg2_json_to_kgx_tsv.log')
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputDir', type=str, nargs='?', default='.')
    return arg_parser

    
max_rows = None  ## Set to 100 for a test run or None for a full build

if max_rows is None:
    node_ids_to_select = None
else:
    edge_counter = 0
    node_ids_to_select = set()

args = make_arg_parser().parse_args()
log_file_name = args.logFile
input_file_name = args.inputFile
output_dir_name = args.outputDir
input_file_name_full = os.path.join(output_dir_name, input_file_name)

# Clear any old output files
if os.path.exists('edges.tsv'):
    os.remove('edges.tsv')
if os.path.exists('kg2_json_to_kgx_tsv.log'):
    os.remove('kg2_json_to_kgx_tsv.log')
if os.path.exists('nodes.tsv'):
    os.remove('nodes.tsv')

# Read the input file kg2-simplified.json
with open(input_file_name_full, "r") as input_file:
    input_data = json.load(input_file)
    input_file.close()

# Populate edges header row
edge_fields = ['subject',
               'object',
               'predicate',
               'knowledge_source',
               'publications',
               'publications_info',
               'id']

with open(log_file_name, 'a') as log_file:
    # Begin writing edges.tsv
    print("--- Begin writing edges.tsv ---", file=log_file)
    output_file = open('edges.tsv', 'a')

    for item in edge_fields:
        if edge_fields.index(item) == len(edge_fields)-1:
            output_file.write(item + '\n')
        else:
            output_file.write(item + '\t')
    print("--- Headers written to edges.tsv ---", file=log_file)

    # Write edges.tsv
    num_edges = 0
    edges_data = input_data['edges']
    for item in edges_data:
        if max_rows is None or num_edges < max_rows:
            output_file.write(check_tab(item['subject'], num_edges) + '\t')
            output_file.write(check_tab(item['object'], num_edges) + '\t')
            output_file.write(check_tab(item['predicate'], num_edges) + '\t')
            # knowledge source is a list
            ks_list = [check_tab(ks, num_edges) for ks in item['knowledge_source']]
            output_file.write('|'.join(ks_list) + '\t')
            # publications is a list
            pubs_list = [check_tab(pub, num_edges) for pub in item['publications']]
            output_file.write('|'.join(pubs_list) + '\t')
            # publications_info is a dictionary
            output_file.write(json.dumps(item['publications_info']) + '\t')
            output_file.write(check_tab(item['id'], num_edges) + '\n')
        num_edges += 1

    output_file.close()
    print("--- Edges.tsv completed --- ", file=log_file)

    # Populate nodes header row
    node_fields = ['id', 'name', 'category', 'iri', 'description', 'publications']

    # Begin writing nodes.tsv
    print("--- Begin writing nodes.tsv ---", file=log_file)
    output_file = open('nodes.tsv', 'a')

    for item in node_fields:
        if node_fields.index(item) == len(node_fields)-1:
            output_file.write(item+'\n')
        else:
            output_file.write(item+'\t')
    print("--- Headers written to nodes.tsv ---", file=log_file)
    nodes_data = input_data['nodes']

    # Write nodes.tsv
    num_nodes = 0
    nodes_data = input_data['nodes']
    for item in nodes_data:
        if max_rows is None or num_nodes < max_rows:
            output_file.write(check_tab(item['id'], num_nodes) + '\t')
            output_file.write(check_tab(str(item['name']), num_nodes) + '\t')
            output_file.write(check_tab(item['category'], num_nodes) + '\t')
            output_file.write(check_tab(item['iri'], num_nodes) + '\t')
            desc = item['description']
            if desc is not None:
                check_tab(desc, num_nodes)
            else:
                desc = ''
            output_file.write(desc + '\t')
            # publications is a list
            pub_list = [check_tab(publication, num_nodes) for publication in item['publications']]
            output_file.write('|'.join(pub_list) + '\n')
        num_nodes += 1

    output_file.close()
    print("--- Nodes.tsv completed --- ", file=log_file)

    print("--- Finished script kg2_json_to_kgx_tsv.py --- ", file=log_file)
