#!/usr/bin/env python3
'''kg2_merge.py: merge two KGs that are in the KG2 JSON format

   Usage: kg2_merge.py --kgFile <kgFile> --kgFileNewEdges <kgFileNewEdges> 
                      [--kgFileOrphanEdges <kgFileOrphanEdges>] 
                       --outputFile <output.json>
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
import kg2_util
import json
import sys


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='add_edges_to_kg_json.py: takes a JSON file of KG edges and adds the edges to a JSON-specified KG')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('--kgFile', type=str, nargs=1)
    arg_parser.add_argument('--kgFileNewEdges', type=str, nargs='+')
    arg_parser.add_argument('--kgFileOrphanEdges', type=str, nargs='?', default=None)
    arg_parser.add_argument('--outputFile', type=str, nargs=1)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    kg_file_name = args.kgFile[0]
    kg_edges_file_names = args.kgFileNewEdges
    test_mode = args.test
    output_file_name = args.outputFile[0]
    kg = json.load(open(kg_file_name, 'r'))
    kg_orphan_edges = {'edges': []}
    for kg_edges_file_name in kg_edges_file_names:
        kg_orphan_edges_new = []
        kg_edges_new = json.load(open(kg_edges_file_name, 'r'))
        nodes_dict = {node['id']: node for node in kg['nodes']}
        for rel_dict in kg_edges_new['edges']:
            subject_curie = rel_dict['subject']
            object_curie = rel_dict['object']
            if subject_curie in nodes_dict and object_curie in nodes_dict:
                kg['edges'].append(rel_dict)
            else:
                kg_orphan_edges_new.append(rel_dict)
        kg_orphan_edges['edges'] += kg_orphan_edges_new
        kg2_util.log_message("number of orphan edges: " + str(len(kg_orphan_edges['edges'])),
                             ontology_name=kg_edges_file_name,
                             output_stream=sys.stderr)
    kg2_util.save_json(kg, output_file_name, test_mode)
    kg_file_orphan_edges = args.kgFileOrphanEdges
    if kg_file_orphan_edges is not None and len(kg_file_orphan_edges) == 1:
        kg2_util.save_json(kg_orphan_edges, kg_file_orphan_edges[0])
