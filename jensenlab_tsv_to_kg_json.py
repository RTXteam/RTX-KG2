#!/usr/bin/env python3
''' jensenlab_tsv_to_kg_json.py: Extracts a KG2 JSON file from the
    Jensen Lab filtered text mining channel tsv file.
    
    Usage: jensenlab_tsv_to_kg_json.py [--test] <inputDirectory>
    <outputFile.json>
'''
import csv
import re
#import kg2_util
# import os
# import xmltodict
import argparse
from collections import defaultdict


__author__ = 'Lindsey Kvarfordt'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Lindsey Kvarfordt']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

#SMPDB_BASE_IRI = kg2_util.BASE_URL_SMPDB
#SMPDB_KB_IRI = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + "smpdb"
#SMPDB_PROVIDED_BY_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY \
#                                + ":smpdb"

#regex from https://www.uniprot.org/help/accession_numbers
REGEX_UNIPROT_ID = re.compile(r'^[P,Q,O][0-9][A-Z0-9][A-Z0-9][A-Z0-9][0-9]$')

def get_args():
    arg_parser = argparse.ArgumentParser(description='jensenlab_tsv_to_kg_json.py: \
                                         Extracts a KG2 JSON file from the \
                                        Jensen Lab filtered text mining channel tsv file.')
    arg_parser.add_argument('--test',
                            dest='test',
                            action="store_true",
                            default=False)
    arg_parser.add_argument('inputDirectory', type=str) #note to self: kg2-build/jensenlab
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()

def make_gene_id_dictionary(human_names_file:str, human_entities_file:str):
    _human_entities_dict = dict(); # string_id: dictionary_serial_no
    _human_names_dict = defaultdict(lambda: list()) # dictionary_serial_no: [external_idsinkg2]
    with open(human_entities_file, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter="\t")
        for row  in tsvin:
            _human_entities_dict[row[2]]=row[0]
    with open(human_names_file, "r") as tsvin:
        tsvin = csv.reader(tsvin, delimiter="\t")
        for row in tsvin:
            # probably filter and edit to be HGNC or UniProt or Ensembl id here
            identifier = _reformat_id(row[1])
            if identifier is not None:
                _human_names_dict[row[0]].append(identifier)
    gene_id_dict = dict() # string id: [external_ids in kg2]
    for k, v in _human_entities_dict.items():
        if len(_human_names_dict[v]) != 0:
            gene_id_dict[k] = _human_names_dict[v]
    return gene_id_dict

def _reformat_id(id:str):
    if "HGNC" in id:
        return id; # HGNC ids are already formatted the same as KG2 nodes
    uniprot_match = REGEX_UNIPROT_ID.match(id)
    if uniprot_match is not None:
        return "UniProtKB:"+id
    # need to add matching for ENSEMBL ids
    return None 
    
def make_edges(input_tsv:str, gene_id_dict:dict):
    gene_ids_actually_used = set()
    with open(input_tsv) as inp:
        tsvin = csv.reader(inp, delimiter="\t")
        for row in tsvin:
            [gene_id,
            gene_name,
            disease_id,
            disease_name,
            z_score,
            _,
            source_url] = row
            gene_ids_actually_used.add(gene_id)
            edges = list()
            kg2_gene_id_list = gene_id_dict.get(gene_id, None)
            if kg2_gene_id_list is None:
                print(f"Missing kg2 equivalent gene ids for {gene_id}. Skipping")
                continue
            for kg2_gene_id in kg2_gene_id_list:
                placeholder = "need to decide where everything goes"
                #edge = kg2_util.make_edge(kg2_gene_id,
                #                          disease_id,
                #                          "JensenLab:associated_with",
                #                          "associated_with",
                                          
        
    used_genes_missing_ids = gene_ids_actually_used - set(gene_id_dict.keys())
    print(f"Skipped {len(used_genes_missing_ids)} rows for lack of kg2 gene ids.")
    print(f"Found {len(gene_ids_actually_used - used_genes_missing_ids)} used kg2 gene ids.")

if __name__ == '__main__':
    args = get_args()
    human_names_file = f"{args.inputDirectory}/human_dictionary/human_names.tsv" 
    human_entities_file = f"{args.inputDirectory}/human_dictionary/human_entities.tsv" 
    edges_tsv_file = f"{args.inputDirectory}human_disease_text_mining_filtered.tsv"
    gene_id_dict = make_gene_id_dictionary(human_names_file, human_entities_file)
    
    make_edges(edges_tsv_file, gene_id_dict)
    
