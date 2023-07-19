#!/usr/bin/env python3
'''unichem_tsv_to_edges_json.py: loads TSV ChEMBL-CHEBI mappings and converts into RTX KG2 JSON format

   Usage: unichem_tsv_to_edges_json.py <inputFile.tsv> <outputNodesFile.json> <outputEdgesFile.json>
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
import os


UNICHEM_KB_CURIE = kg2_util.CURIE_ID_UNICHEM
UNICHEM_KB_IRI = kg2_util.BASE_URL_UNICHEM


def make_xref(subject: str,
              object: str,
              update_date: str):
    edge_dict = kg2_util.make_edge(subject,
                                   object,
                                   kg2_util.CURIE_ID_OWL_SAME_AS,
                                   kg2_util.EDGE_LABEL_OWL_SAME_AS,
                                   UNICHEM_KB_CURIE,
                                   update_date)
    return edge_dict


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='unichem_tsv_to_edges_json.py: loads TSV CURIE mappings and converts into RTX KG2 JSON format')
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputNodesFile', type=str)
    arg_parser.add_argument('outputEdgesFile', type=str)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_file_name = args.inputFile
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile
    test_mode = args.test

    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    update_date = None
    line_ctr = 0
    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            line_ctr += 1
            if line.startswith('#'):
                if line_ctr == 1:
                    update_date = line.split('# ')[1].rstrip()
                if line_ctr == 2:
                    version = line.split('# ')[1].rstrip()
                continue
            if test_mode and line_ctr > 10000:
                break
            (subject_curie_id, object_curie_id) = line.rstrip().split('\t')
            edges_output.write(make_xref(subject_curie_id, object_curie_id, update_date))

    unichem_kp_node = kg2_util.make_node(UNICHEM_KB_CURIE,
                                         UNICHEM_KB_IRI,
                                         "UniChem database",
                                         kg2_util.SOURCE_NODE_CATEGORY,
                                         update_date,
                                         UNICHEM_KB_CURIE)
    nodes_output.write(unichem_kp_node)

    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)
