#!/usr/bin/env python3
'''dgidb_tsv_to_kg_json.py: Extracts a KG2 JSON file from the DGIdb interactions file in TSV format

   Usage: dgidb_tsv_to_kg_json.py [--test] --inputFile <inputFile.tsv> --outputFile <outputFile.json>
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


DGIDB_BASE_IRI = 'http://www.dgidb.org'
DGIDB_CURIE_PREFIX = 'DGIDB'

def get_args():
    arg_parser = argparse.ArgumentParser(description='dgidb_tsv_to_kg_json.py: builds a KG2 JSON file from the DGIdb interactions.tsv file')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('--inputFile', type=str, nargs=1)
    arg_parser.add_argument('--outputFile', type=str, nargs=1)
    return arg_parser.parse_args()


def make_kg2_graph(input_file_name: str, test_mode: bool = False):
    nodes = []
    edges = []
    gene_ctr = 0
    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            line = line.rstrip()
            if line.startswith('#'):
                update_date = line.replace('#', '')
                continue
            gene_ctr += 1
            if test_mode and gene_ctr > 10000:
                break
            fields = line.split("\t")
            [gene_name,
             gene_claim_name,
             entrez_id,
             interaction_claim_source,
             interaction_types,
             drug_claim_name,
             drug_claim_primary_name,
             drug_name,
             drug_chembl_id,
             PMIDs] = fields
            if drug_chembl_id != "" and entrez_id != "" and interaction_types != "":
                interaction_list = interaction_types.split(',')
                for interaction in interaction_list:
                    interaction = interaction.replace(' ', '_')
                    edge_dict = kg2_util.make_edge('CHEMBL.COMPOUND:' + drug_chembl_id,
                                                   'NCBIGene:' + entrez_id,
                                                   DGIDB_BASE_IRI + '/' +
                                                   kg2_util.convert_snake_case_to_camel_case(interaction),
                                                   DGIDB_CURIE_PREFIX + ':' + interaction,
                                                   interaction,
                                                   DGIDB_BASE_IRI,
                                                   update_date)
                    edges.append(edge_dict)
    return {'nodes': nodes,
            'edges': edges}


if __name__ == '__main__':
    args = get_args()
    input_file_name = args.inputFile[0]
    output_file_name = args.outputFile[0]
    test_mode = args.test
    graph = make_kg2_graph(input_file_name, test_mode)
    kg2_util.save_json(graph, output_file_name, test_mode)
