#!/usr/bin/env python3
'''ensembl_json_to_kg_json.py: Extracts a KG2 JSON file from the Ensembl human gene distribution in JSON format

   Usage: ensembl_json_to_kg_json.py [--test] <inputFile.json> <outputFile.json>
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
import json
import kg2_util


ENSEMBL_BASE_IRI = kg2_util.BASE_URL_ENSEMBL
ENSEMBL_RELATION_CURIE_PREFIX = kg2_util.CURIE_PREFIX_ENSEMBL
ENSEMBL_KB_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY + ':' + 'ensembl'
ENSEMBL_KB_URI = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + "ensembl"


def get_args():
    arg_parser = argparse.ArgumentParser(description='ensembl_json_to_kg_json.py: builds a KG2 JSON representation for Ensembl genes')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def make_node(ensembl_gene_id: str,
              description: str,
              gene_symbol: str,
              update_date: str,
              category_label: str,
              other_synonyms: list = None):
    if other_synonyms is None:
        other_synonyms = []
    node_curie = kg2_util.CURIE_PREFIX_ENSEMBL + ':' + ensembl_gene_id
    iri = ENSEMBL_BASE_IRI + ensembl_gene_id
    node_dict = kg2_util.make_node(node_curie,
                                   iri,
                                   description,
                                   category_label,
                                   update_date,
                                   ENSEMBL_KB_CURIE_ID)
    node_dict['name'] = gene_symbol
    node_dict['synonym'] = [gene_symbol] + sorted(list(set(other_synonyms)))
    return node_dict


def add_prefixes_to_curie_list(curie_list, curie_prefix):
    new_curie_list = []
    for curie in curie_list:
        if curie_prefix == kg2_util.CURIE_PREFIX_GO:
            curie = curie['term'] + ' ' + curie['evidence'][0]
        if ':' in curie:
            curie = curie.split(':')[1]
        new_curie_list.append(curie_prefix + ':' + curie)
    return sorted(list(set(new_curie_list)))


def make_kg2_graph(input_file_name: str, test_mode: bool = False):
    ensembl_data = kg2_util.load_json(input_file_name)
    nodes = []
    edges = []
    genebuild_str = ensembl_data['genebuild']
    db_version = ensembl_data["dbname"].replace('homo_sapiens_core_', '').split('_')[0]
    update_date = genebuild_str.split('/')[1]
    gene_ctr = 0

    ontology_curie_id = ENSEMBL_KB_CURIE_ID
    ens_kp_node = kg2_util.make_node(ontology_curie_id,
                                     ENSEMBL_KB_URI,
                                     'Ensembl Genes v' + db_version,
                                     kg2_util.BIOLINK_CATEGORY_INFORMATION_RESOURCE,
                                     update_date,
                                     ontology_curie_id)
    nodes.append(ens_kp_node)

    for gene_dict in ensembl_data['genes']:
        gene_ctr += 1
        if test_mode and gene_ctr > 10000:
            break
        ensembl_gene_id = gene_dict['id']
        description = gene_dict.get('description', None)
        gene_symbol = gene_dict.get('name', None)
        other_synonyms = []
        pathway_xrefs =  add_prefixes_to_curie_list(gene_dict.get('Reactome', []), kg2_util.CURIE_PREFIX_REACTOME)
        gene_xrefs = add_prefixes_to_curie_list(gene_dict.get('MIM_GENE', []), kg2_util.CURIE_PREFIX_OMIM)
        gene_xrefs += add_prefixes_to_curie_list(gene_dict.get('HGNC', ''), kg2_util.CURIE_PREFIX_HGNC)
        gene_xrefs += add_prefixes_to_curie_list(gene_dict.get('EntrezGene', ''), kg2_util.CURIE_PREFIX_NCBI_GENE)
        microrna_xrefs = add_prefixes_to_curie_list(gene_dict.get('miRBase', ''), kg2_util.CURIE_PREFIX_MIRBASE)
        go_xrefs = add_prefixes_to_curie_list(gene_dict.get('GO', ''), kg2_util.CURIE_PREFIX_GO)
        node_dict = make_node(ensembl_gene_id,
                              description,
                              gene_symbol,
                              update_date,
                              kg2_util.BIOLINK_CATEGORY_GENE,
                              other_synonyms)
        nodes.append(node_dict)
        ensembl_gene_curie_id = node_dict['id']
        taxon_id_int = gene_dict.get('taxon_id', None)
        assert taxon_id_int == 9606, "unexpected taxon ID"
        edges.append(kg2_util.make_edge_biolink(ensembl_gene_curie_id,
                                                kg2_util.CURIE_PREFIX_NCBI_TAXON + ':' + str(taxon_id_int),
                                                kg2_util.EDGE_LABEL_BIOLINK_IN_TAXON,
                                                ENSEMBL_KB_CURIE_ID,
                                                update_date))
        for gene_xref in gene_xrefs:
            edges.append(kg2_util.make_edge(ensembl_gene_curie_id,
                                            gene_xref,
                                            kg2_util.CURIE_ID_OWL_SAME_AS,
                                            kg2_util.EDGE_LABEL_OWL_SAME_AS,
                                            ENSEMBL_KB_CURIE_ID,
                                            update_date))
        for transcript in gene_dict['transcripts']:
            protein_xrefs = add_prefixes_to_curie_list(transcript.get('Uniprot/SWISSPROT', []), kg2_util.CURIE_PREFIX_UNIPROT)
            ensembl_transcript_id = transcript['id']
            name = transcript['name']
            transcript_category_label = kg2_util.BIOLINK_CATEGORY_TRANSCRIPT
            description = None
            other_synonyms = []
            node_dict = make_node(ensembl_transcript_id,
                                  description,
                                  name,
                                  update_date,
                                  transcript_category_label,
                                  other_synonyms)
            nodes.append(node_dict)
            ensembl_transcript_curie_id = node_dict['id']
            edges.append(kg2_util.make_edge_biolink(ensembl_transcript_curie_id,
                                                    kg2_util.CURIE_PREFIX_NCBI_TAXON + ':' + str(taxon_id_int),
                                                    kg2_util.EDGE_LABEL_BIOLINK_IN_TAXON,
                                                    ENSEMBL_KB_CURIE_ID,
                                                    update_date))
            edges.append(kg2_util.make_edge_biolink(ensembl_transcript_curie_id,
                                                    ensembl_gene_curie_id,
                                                    kg2_util.EDGE_LABEL_BIOLINK_TRANSCRIBED_FROM,
                                                    ENSEMBL_KB_CURIE_ID,
                                                    update_date))
            for protein_xref in protein_xrefs:
                edges.append(kg2_util.make_edge_biolink(ensembl_transcript_curie_id,
                                                        protein_xref,
                                                        kg2_util.EDGE_LABEL_BIOLINK_TRANSLATES_TO,
                                                        ENSEMBL_KB_CURIE_ID,
                                                        update_date))
    return {'nodes': nodes,
            'edges': edges}


if __name__ == '__main__':
    args = get_args()
    input_file_name = args.inputFile
    output_file_name = args.outputFile
    test_mode = args.test
    graph = make_kg2_graph(input_file_name, test_mode)
    kg2_util.save_json(graph, output_file_name, test_mode)
