#!/usr/bin/env python3
'''ensembl_json_to_kg_json.py: Extracts a KG2 JSON file from the Ensembl human gene distribution in JSON format

   Usage: ensembl_json_to_kg_json.py [--test] --inputFile <inputFile.json> --outputFile <outputFile.json>
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


ENSEMBL_BASE_IRI = 'http://ensembl.org/Homo_sapiens/Gene/Summary?db=core;g='
ENSEMBL_KB_IRI = 'http://ensembl.org/Homo_sapiens/Gene'


def get_args():
    arg_parser = argparse.ArgumentParser(description='ensembl_json_to_kg2_json.py: builds a KG2 JSON representation for Ensembl genes')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('--inputFile', type=str, nargs=1)
    arg_parser.add_argument('--outputFile', type=str, nargs=1)
    return arg_parser.parse_args()


def make_node(ensembl_gene_id: str,
              description: str,
              gene_symbol: str,
              update_date: str,
              other_synonyms: list = None):
    category_label = 'gene'
    if other_synonyms is None:
        other_synonyms = []
    node_curie = kg2_util.CURIE_PREFIX_ENSEMBL + ensembl_gene_id
    node_dict = {
        'id': node_curie,
        'iri': ENSEMBL_BASE_IRI + '/' + ensembl_gene_id,
        'full name': description,
        'name': description,
        'category': kg2_util.convert_biolink_category_to_iri(category_label),
        'category label': category_label,
        'description': None,
        'synonym': [gene_symbol] + other_synonyms,
        'publications': [],
        'creation date': None,
        'update date': update_date,
        'deprecated': False,
        'replaced by': None,
        'provided by': ENSEMBL_KB_IRI
    }
#        'ontology node type': 'INDIVIDUAL'
    return node_dict


def make_kg2_graph(input_file_name: str, test_mode: bool = False):
    ensembl_data = kg2_util.load_json(input_file_name)
    nodes = []
    edges = []
    genebuild_str = ensembl_data['genebuild']
    update_date = genebuild_str.split('/')[1]
    gene_ctr = 0
    for gene_dict in ensembl_data['genes']:
        gene_ctr += 1
        if test_mode and gene_ctr > 10000:
            break
        ensembl_gene_id = gene_dict['id']
        description = gene_dict.get('description', None)
        gene_symbol = gene_dict.get('name', None)
        other_synonyms = []
        xrefs = gene_dict.get('xrefs', None)
        if xrefs is not None:
            other_synonyms = list(set([xref['primary_id'] for xref in xrefs if xref['primary_id'] != ensembl_gene_id]))
        node_dict = make_node(ensembl_gene_id,
                              description,
                              gene_symbol,
                              update_date,
                              other_synonyms)
        nodes.append(node_dict)
        ensembl_gene_curie_id = node_dict['id']
        taxon_id_int = gene_dict.get('taxon_id', None)
        assert taxon_id_int == 9606, "unexpected taxon ID"
        edges.append(kg2_util.make_edge(ensembl_gene_curie_id,
                                        'NCBITaxon:' + str(taxon_id_int),
                                        'gene_found_in_organism',
                                        ENSEMBL_KB_IRI,
                                        update_date))
        hgnc_list = gene_dict.get('HGNC', None)
        if hgnc_list is not None:
            for hgnc_curie in hgnc_list:
                edges.append({
                    'subject': ensembl_gene_curie_id,
                    'object': hgnc_curie,
                    'edge label': 'is_equivalent_to',
                    'relation': kg2_util.IRI_OWL_SAME_AS,
                    'relation curie': kg2_util.CURIE_OWL_SAME_AS,
                    'negated': False,
                    'publications': [],
                    'publications info': {},
                    'update date': update_date,
                    'provided by': ENSEMBL_KB_IRI
                })
    return {'nodes': nodes,
            'edges': edges}


if __name__ == '__main__':
    args = get_args()
    input_file_name = args.inputFile[0]
    output_file_name = args.outputFile[0]
    test_mode = args.test
    graph = make_kg2_graph(input_file_name, test_mode)
    kg2_util.save_json(graph, output_file_name, test_mode)
