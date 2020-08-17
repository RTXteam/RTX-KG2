#!/usr/bin/env python3
'''unichem_tsv_to_edges_json.py: loads TSV ChEMBL-CHEBI mappings and converts into RTX KG2 JSON format

   Usage: unichem_tsv_to_edges_json.py <inputFile.tsv> <outputFile.json>
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


UNICHEM_KB_CURIE = kg2_util.CURIE_ID_UNICHEM


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
    arg_parser = argparse.ArgumentParser(description='unichem_tsv_to_edges_json.py: loads TSV ChEMBL-CURIE mappings and converts into RTX KG2 JSON format')
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_file_name = args.inputFile
    output_file_name = args.outputFile
    test_mode = args.test
    edges = []
    nodes = []
    update_date = None
    line_ctr = 0
    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            if line.startswith('#'):
                update_date = line.split('# ')[1].rstrip()
                continue
            line_ctr += 1
            if test_mode and line_ctr > 10000:
                break
            (chembl_curie_id, equiv_curie_id) = line.rstrip().split('\t')
            edges.append(make_xref(chembl_curie_id, equiv_curie_id, update_date))

    out_graph = {'edges': edges, 'nodes': nodes}
    kg2_util.save_json(out_graph, output_file_name, test_mode)
