#!/usr/bin/env python3
'''merge_graphs.py: merge two KGs that are in the KG2 JSON format

   Usage: merge_graphs.py --kgFiles <kgFile1> ... <kgFile>
                         [--kgFileOrphanEdges <kgFileOrphanEdges>]
                         <output.json>
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
    arg_parser = argparse.ArgumentParser(description='merge_graphs.py: merge two or more JSON KG files')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('--kgFileOrphanEdges', type=str, nargs='?', default=None)
    arg_parser.add_argument('--outputFile', type=str, nargs='?', default=None)
    arg_parser.add_argument('kgFiles', type=str, nargs='+')
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    kg_file_names = args.kgFiles
    test_mode = args.test
    output_file_name = args.outputFile
    kg_orphan_edges = {'nodes': [], 'edges': []}
    nodes = dict()
    rels = dict()
    for kg_file_name in kg_file_names:
        kg2_util.log_message("reading nodes from file",
                             ontology_name=kg_file_name,
                             output_stream=sys.stderr)
        kg_to_add = json.load(open(kg_file_name, 'r'))
        kg_to_add_nodes = kg_to_add['nodes']
        for node in kg_to_add_nodes:
            node_id = node['id']
            if node_id not in nodes:
                nodes[node_id] = node
            else:
                nodes[node_id] = kg2_util.merge_two_dicts(nodes[node_id], node)
        kg2_util.log_message("number of nodes added: " + str(len(kg_to_add_nodes)),
                             ontology_name=kg_file_name,
                             output_stream=sys.stderr)
    ctr_edges_added = 0
    edges = []
    last_edges_added = 0
    last_orphan_edges = 0
    edge_keys = set()
    for kg_file_name in kg_file_names:
        kg_orphan_edges_new = []
        kg2_util.log_message("reading edges from file",
                             ontology_name=kg_file_name,
                             output_stream=sys.stderr)
        kg_to_add = json.load(open(kg_file_name, 'r'))
        kg_to_add_edges = kg_to_add['edges']
        for rel_dict in kg_to_add_edges:
            subject_curie = rel_dict['subject']
            object_curie = rel_dict['object']
            if subject_curie in nodes and object_curie in nodes:
                ctr_edges_added += 1
                edge_key = kg2_util.make_edge_key(rel_dict)
                if edge_key not in edge_keys:
                    edge_keys.add(edge_key)
                    rel_dict["id"] = edge_key 
                    edges.append(rel_dict)
            else:
                kg_orphan_edges_new.append(rel_dict)
        kg_orphan_edges['edges'] += kg_orphan_edges_new
        kg2_util.log_message("number of edges added: " + str(ctr_edges_added - last_edges_added),
                             ontology_name=kg_file_name,
                             output_stream=sys.stderr)
        last_edges_added = ctr_edges_added
        kg2_util.log_message("number of orphan edges: " + str(len(kg_orphan_edges['edges']) -
                                                              last_orphan_edges),
                             ontology_name=kg_file_name,
                             output_stream=sys.stderr)
        last_orphan_edges = len(kg_orphan_edges['edges'])
    kg = {'nodes': [node for node in nodes.values()],
          'edges': edges}
    del nodes
    kg2_util.save_json(kg, output_file_name, test_mode)
    kg_file_orphan_edges = args.kgFileOrphanEdges
    if kg_file_orphan_edges is not None:
        kg2_util.save_json(kg_orphan_edges, kg_file_orphan_edges, test_mode)
