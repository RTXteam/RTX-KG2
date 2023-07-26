#!/usr/bin/env python3
'''ncbigene_tsv_to_kg_json.py: Extracts a KG2 JSON file from the NCBI human gene distribution in TSV format

   Usage: ncbigene_tsv_to_kg_json.py [--test] <inputFile.tsv> <outputNodesFile.json> <outputEdgesFile.json>
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
import datetime


NCBI_BASE_IRI = kg2_util.BASE_URL_NCBIGENE
NCBI_KB_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY + ':' + 'ncbigene'
NCBI_KB_URL = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + 'ncbigene'


def get_args():
    arg_parser = argparse.ArgumentParser(description='ncbigene_tsv_to_kg_json.py: builds a KG2 JSON representation for NCBI human genes')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputNodesFile', type=str)
    arg_parser.add_argument('outputEdgesFile', type=str)
    return arg_parser.parse_args()


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def make_node(ncbi_gene_id: str,
              name: str,
              full_name: str,
              gene_symbol: str,
              update_date: str,
              category_label: str,
              other_synonyms: list = None) -> dict:

    if other_synonyms is None:
        other_synonyms = []
    node_curie = kg2_util.CURIE_PREFIX_NCBI_GENE + ':' + ncbi_gene_id
    iri = NCBI_BASE_IRI + ncbi_gene_id
    node_dict = kg2_util.make_node(node_curie,
                                   iri,
                                   name,
                                   category_label,
                                   update_date,
                                   NCBI_KB_CURIE_ID)
    node_dict['synonym'] = [gene_symbol] + sorted(list(set(other_synonyms)))
    node_dict['full_name'] = full_name
    return node_dict


def make_kg2_graph(input_file_name: str, nodes_output, edges_output, test_mode: bool = False):
    gene_ctr = 0

    update_date = os.path.getmtime(input_file_name)
    ontology_curie_id = NCBI_KB_CURIE_ID
    ens_kp_node = kg2_util.make_node(ontology_curie_id,
                                     NCBI_KB_URL,
                                     'NCBI Genes',
                                     kg2_util.SOURCE_NODE_CATEGORY,
                                     update_date,
                                     ontology_curie_id)
    nodes_output.write(ens_kp_node)

    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            if line.startswith('#'):
                continue
            gene_ctr += 1
            if test_mode and gene_ctr > 10000:
                break
            fields = line.rstrip("\n").split("\t")
            fields = [(field if field.strip() != '-' else None) for field in fields]
            [taxon_id_str,
             ncbi_gene_id,
             gene_symbol,
             locus_tag,
             synonyms_str,
             db_xrefs,
             chromosome,
             map_location,
             description,
             type_of_gene,
             symbol_auth,
             full_name_auth,
             nomenc_status,
             other_desig,
             modify_date,
             feature_type] = fields
            taxon_id_int = int(taxon_id_str)
            if taxon_id_int != kg2_util.NCBI_TAXON_ID_HUMAN:
                # skip neanderthal- and denisovan-specific genes
                continue
            node_synonyms = list()
            if synonyms_str is not None:
                node_synonyms += synonyms_str.split('|')
            if other_desig is not None:
                node_synonyms += other_desig.split('|')
            if symbol_auth is not None and symbol_auth != gene_symbol:
                node_synonyms = [symbol_auth] + node_synonyms
            node_synonyms = list(set(node_synonyms))
            full_name = full_name_auth
            if full_name is None:
                full_name = description
            if type_of_gene != "unknown" or (db_xrefs is None) or (not db_xrefs.startswith("MIM:")) or \
               nomenc_status is not None:
                category_label = kg2_util.BIOLINK_CATEGORY_GENE
                name = gene_symbol
            else:
                full_name = 'Genetic locus associated with ' + full_name
                name = 'Genetic locus associated with ' + gene_symbol
                category_label = kg2_util.BIOLINK_CATEGORY_NUCLEIC_ACID_ENTITY
            node_dict = make_node(ncbi_gene_id,
                                  name,
                                  full_name,
                                  gene_symbol,
                                  modify_date,
                                  category_label,
                                  node_synonyms)
            node_curie_id = node_dict['id']
            type_str = 'Type:' + type_of_gene
            node_description = ''
            if description is not None and description != full_name_auth:
                node_description = description + '; '
            node_description += type_str
            if nomenc_status is not None:
                nomenc_tag = 'official'
            else:
                nomenc_tag = 'unofficial'
            if map_location is not None:
                node_description += '; Locus:' + map_location
            node_description += '; NameStatus:' + nomenc_tag
            node_dict['description'] = node_description
            nodes_output.write(node_dict)
            org_curie = kg2_util.CURIE_PREFIX_NCBI_TAXON + ':' + taxon_id_str
            predicate_label = 'in_taxon'

            edge_dict = kg2_util.make_edge_biolink(node_curie_id,
                                                   org_curie,
                                                   predicate_label,
                                                   NCBI_KB_CURIE_ID,
                                                   modify_date)
            edges_output.write(edge_dict)
            if db_xrefs is not None:
                xrefs_list = db_xrefs.split('|')
                for xref_curie in xrefs_list:
                    if xref_curie.startswith('HGNC:HGNC:'):
                        xref_curie = kg2_util.CURIE_PREFIX_HGNC + ':' + xref_curie.replace('HGNC:', '')
                    elif xref_curie.startswith('Ensembl:'):
                        xref_curie = xref_curie.upper()
                    elif xref_curie.startswith('MIM:'):
                        xref_curie = kg2_util.CURIE_PREFIX_OMIM + ':' + xref_curie.replace('MIM:', '')
                        edges_output.write(kg2_util.make_edge_biolink(node_curie_id,
                                                                      xref_curie,
                                                                      kg2_util.EDGE_LABEL_BIOLINK_RELATED_TO,
                                                                      NCBI_KB_CURIE_ID,
                                                                      modify_date))
                        continue
                    elif xref_curie.startswith('miRBase:'):
                        xref_curie = kg2_util.CURIE_PREFIX_MIRBASE + ':' + xref_curie.replace('miRBase:', '')
                    edges_output.write(kg2_util.make_edge(node_curie_id,
                                                          xref_curie,
                                                          kg2_util.CURIE_ID_OWL_SAME_AS,
                                                          kg2_util.EDGE_LABEL_OWL_SAME_AS,
                                                          NCBI_KB_CURIE_ID,
                                                          modify_date))


if __name__ == '__main__':
    print("Start time: ", date())
    args = get_args()
    input_file_name = args.inputFile
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile
    test_mode = args.test

    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    make_kg2_graph(input_file_name, nodes_output, edges_output, test_mode)
    
    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)

    print("Finish time: ", date())
