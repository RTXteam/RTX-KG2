#!/usr/bin/env python3

''' Loads the KG2 simplified json file kg2-simplified.json
and writes out a nodes.tsv and edges.tsv in Translator KGX TSV format

    Usage: python3 kg2_json_to_kgx_tsv.py
'''

import json
import sys
import os
import argparse
import jsonlines

__author__ = 'Liliana Acevedo'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def check_tab(the_string: str):
    if '\t' in the_string:
        the_string = the_string.replace('\t', '    ')
    if '\n' in the_string:
        the_string = the_string.replace('\n', ' ')
    return the_string


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='kg2_json_to_kgx_tsv.py: load a RTX-KG2pre graph in JSON format and export it to KGX TSV format')
    arg_parser.add_argument('--logFile', type=str, default='kg2_json_to_kgx_tsv.log')
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
output_dir_name = args.outputDir
input_edges_file = '~/kg2-build/kg2_simplified_edges.jsonl'
input_nodes_file = '~/kg2-build/kg2_simplified_nodes.jsonl'

output_edges_file = '~/kg2-build/kg2_edges_kgx.jsonl'
output_nodes_file = '~/kg2-build/kg2_nodes_kgx.jsonl'

# Clear any old output files
if os.path.exists(output_edges_file):
    os.remove(output_edges_file)
if os.path.exists(log_file_name):
    os.remove(log_file_name)
if os.path.exists(output_nodes_file):
    os.remove(output_nodes_file)

edge_fields = ['subject',
               'object',
               'predicate',
               'primary_knowledge_source',
               'publications',
               'publications_info',
               'id']
node_fields = ['id', 'name', 'category', 'iri', 'description', 'publications', 'provided_by']

# Read the input files
with jsonlines.open(input_edges_file) as reader, jsonlines.open(output_edges_file, mode='w') as writer:
    for item in edges_fields: 
        edges_header += item + '\t'
    writer.write(edge_header)
    print("--- Edge headers written ---", file=log_file)
    for item in reader:
        pubs_list = [check_tab(publication) for publication in item['publications']]
        edge = check_tab(item['subject'] + '\t'
              + check_tab(item['object']) + '\t'
              + check_tab(item['source_predicate']) + '\t'
              + check_tab(item['primary_knowledge_source']) + '\t' + '|'.join(pubs_list) + '\t'
              + json.dumps(item['publications_info']) + '\t' + check_tab(item['id'])
        writer.write(edge)
        num_edges += 1
        if num_edges % 1000000 == 0:
            print(f"Processed edge {num_edges}", file=log_file)
    print("--- Edges completed --- ", file=log_file)

with jsonlines.open(input_nodes_file) as reader, jsonlines.open(output_nodes_file, mode='w') as writer:
    for item in nodes_fields: 
             nodes_header += item + '\t'
         writer.write(nodes_header)    
    print("--- Node headers written ---", file=log_file)
    print("--- Begin writing nodes ---", file=log_file)
    for item in reader: 
        desc = item['description']
        if desc is not None:
            desc = check_tab(desc)
        else:
            desc = ''
        pub_list = [check_tab(publication) for publication in item['publications']]
        provided_by_list = [check_tab(provided_by) for provided_by in item['provided_by']]
        node = check_tab(item['id']) + '\t' + check_tab(str(item['name'])) + '\t' + 
                check_tab(item['category']) + '\t' + check_tab(item['iri']) + '\t' + desc + '\t' + 
                '|'.join(pub_list) + '\t' + '|'.join(provided_by_list)
        writer.write(node)
        num_nodes += 1
        if num_nodes % 1000000 == 0:
            print(f"Processed node {num_edges}", file=log_file)
    print("--- Nodes completed --- ", file=log_file)

    print("--- Finished script kg2_json_to_kgx_tsv.py --- ", file=log_file)
