#!/usr/bin/env python3
'''kg2_merge.py: merge two KGs that are in the KG2 JSON format

   Usage: kg2_merge.py <kg_alpha.json> <kg_beta.json> <output.json>
   Note: any of the three file arguments can have a ".gz" extension, in which case gzip is used for reading/writing.
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import argparse
import gzip
import json
import shutil
import tempfile


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='add_edges_to_kg_json.py: takes a JSON file of KG edges and adds the edges to a JSON-specified KG')
    arg_parser.add_argument('kgFile', type=str, nargs=1)
    arg_parser.add_argument('kgFileNewEdges', type=str, nargs=1)
    arg_parser.add_argument('outputFile', type=str, nargs=1)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    kg_file_name = args.kgFile[0]
    kg_edges_file_name = args.kgFileNewEdges[0]
    kg = json.load(open(kg_file_name, 'r'))
    kg_edges_new = json.load(open(kg_edges_file_name, 'r'))
    nodes_dict = {node['id']: node for node in kg['nodes']}
    kg_orphan_edges = {'edges': []}
    for rel_dict in kg_edges_new['edges']:
        subject_curie = rel_dict['subject']
        object_curie = rel_dict['object']
        if subject_curie in nodes_dict and object_curie in nodes_dict:
            kg['edges'].append(rel_dict)
        else:
            kg_orphan_edges['edges'].append(rel_dict)
    temp_output_file_name = tempfile.mkstemp(prefix='kg2-')[1]
    output_file_name = args.outputFile[0]
    temp_output_file = open(temp_output_file_name, 'w')
    json.dump(kg, temp_output_file, indent=4, sort_keys=True)
    shutil.move(temp_output_file_name, output_file_name)
