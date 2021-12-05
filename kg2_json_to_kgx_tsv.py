#!/usr/bin/env python3

''' Loads the KG2 simplified json file kg2-simplified.json
and writes out a nodes.tsv and edges.tsv in Translator KGX TSV format

    Usage: python3 kg2_json_to_kgx_tsv.py
'''

import json
import sys
import os

__author__ = 'Liliana Acevedo'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

max_edges = None  ## Set to 100 for a test run or None for a full build

if max_edges is None:
    node_ids_to_select = None
else:
    edge_counter = 0
    node_ids_to_select = set()

# Clear any old output files
if os.path.exists('edges.tsv'):
    os.remove('edges.tsv')
if os.path.exists('kg2_json_to_kgx_tsv.log'):
    os.remove('kg2_json_to_kgx_tsv.log')
if os.path.exists('nodes.tsv'):
    os.remove('nodes.tsv')

# Read the input file kg2-simplified.json
with open("kg2-biolink-simplified.json", "r") as input_file:
    input_data = json.load(input_file)
    input_file.close()

# Populate edges header row
edge_fields = ['subject', 'object', 'predicate', 'knowledge_source', 'publications', 'publications_info', 'id']

# Begin writing edges.tsv
print("--- Begin writing edges.tsv ---", file=open("kg2_json_to_kgx_tsv.log", "a"))
output_file = open('edges.tsv', 'a')

for item in edge_fields:
    if edge_fields.index(item) == len(edge_fields)-1:
        output_file.write(item+'\n')
    else:
        output_file.write(item+'\t')
print("--- Headers written to edges.tsv ---", file=open("kg2_json_to_kgx_tsv.log", "a"))

# Write edges.tsv
num_edges = 0
edges_data = input_data['edges']
for item in edges_data:
    if max_edges is None or num_edges < max_edges:
        output_file.write(item['subject']+'\t')
        output_file.write(item['object']+'\t')
        output_file.write(item['predicate'] + '\t')
        # knowledge source is a list
        output_file.write('|'.join(item['knowledge_source']) + '\t')
        # publications is a list
        output_file.write('|'.join(item['publications']) + '\t')
        # publications_info is a dictionary
        output_file.write('|'.join(item['publications_info']) + '\t')
        output_file.write(item['id'] + '\n')
    num_edges += 1

output_file.close()
print("--- Edges.tsv completed --- ", file=open("kg2_json_to_kgx_tsv.log", "a"))

# Populate nodes header row
node_fields = ['id', 'name', 'category', 'iri', 'description', 'publications']

# Begin writing nodes.tsv
print("--- Begin writing nodes.tsv ---", file=open("kg2_json_to_kgx_tsv.log", "a"))
output_file = open('nodes.tsv', 'a')

for item in node_fields:
    if node_fields.index(item) == len(node_fields)-1:
        output_file.write(item+'\n')
    else:
        output_file.write(item+'\t')
print("--- Headers written to nodes.tsv ---", file=open("kg2_json_to_kgx_tsv.log", "a"))
nodes_data = input_data['nodes']

# Write nodes.tsv
num_edges = 0
nodes_data = input_data['nodes']
for item in nodes_data:
    if max_edges is None or num_edges < max_edges:
        output_file.write(item['id']+'\t')
        output_file.write(str(item['name'])+'\t')
        output_file.write(item['category'] + '\t')
        output_file.write(item['iri'] + '\t')
        # publications is a list
        output_file.write('|'.join(item['publications']) + '\n')
    num_edges += 1

output_file.close()
print("--- Nodes.tsv completed --- ", file=open("kg2_json_to_kgx_tsv.log", "a"))

print("--- Finished script kg2_json_to_kgx_tsv.py --- ", file=open("kg2_json_to_kgx_tsv.log", "a"))