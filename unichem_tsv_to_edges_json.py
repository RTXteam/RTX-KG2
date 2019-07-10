#!/usr/bin/env python3
'''unichem_tsv_to_edges_json.py: loads TSV ChEMBL-CHEBI mappings and converts into RTX KG2 JSON format

   Usage: unichem_tsv_to_edges_json.py --inputFile <inputFile.tsv> --outputFile <outputFile.json>
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


UNICHEM_KB_IRI = 'https://www.ebi.ac.uk/unichem/'

def make_xref(subject: str,
              object: str,
              update_date: str):
    return {
        'subject': subject,
        'object': object,
        'edge label': 'xref',
        'relation': kg2_util.IRI_OBO_XREF,
        'relation curie': kg2_util.CURIE_OBO_XREF,
        'negated': False,
        'publications': [],
        'publications info': {},
        'update date': update_date,
        'provided by': UNICHEM_KB_IRI}


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='unichem_tsv_to_edges_json.py: loads TSV ChEMBL-CHEBI mappings and converts into RTX KG2 JSON format')
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('--inputFile', type=str, nargs=1)
    arg_parser.add_argument('--outputFile', type=str, nargs=1)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_file_name = args.inputFile[0]
    output_file_name = args.outputFile[0]
    test_mode = args.test
    edges = []
    nodes = []
    update_date = None
    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            if line.startswith('#'):
                update_date = line.split('# ')[1]
                continue
            (chembl_curie_id, chebi_curie_id) = line.rstrip().split('\t')
            edges.append(make_xref(chembl_curie_id, chebi_curie_id, update_date))
            edges.append(make_xref(chebi_curie_id, chembl_curie_id, update_date))

    output_file_name = args.outputFile[0]
    out_graph = {'edges': edges, 'nodes': nodes}
    kg2_util.save_json(out_graph, output_file_name, test_mode)
