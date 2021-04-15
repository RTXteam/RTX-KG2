#!/usr/bin/env python3
''' jensenlab_tsv_to_kg_json.py: Extracts a KG2 JSON file from the
    Jensen Lab filtered text mining channel tsv file.
    
    Usage: jensenlab_tsv_to_kg_json.py [--test] <inputDirectory>
    <outputFile.json>
'''
import csv
import sys
import re
import kg2_util
import argparse
import datetime
from collections import defaultdict
from typing import *

__author__ = 'Lindsey Kvarfordt'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Lindsey Kvarfordt']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

csv.field_size_limit(sys.maxsize)

# for now, just using HGNC gene ids to keep the size of this etl managable.
# regex from https://www.uniprot.org/help/accession_numbers
# REGEX_UNIPROT_ID = re.compile(r'^[P,Q,O][0-9][A-Z0-9][A-Z0-9][A-Z0-9][0-9]$')
# regex from multi_ont_to_kg_json.py
# REGEX_ENSEMBL_ID = re.compile('ENS[A-Z]{0,3}([PG])[0-9]{11}')

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

def make_gene_id_dictionary(human_names_file:str, human_entities_file:str) -> Dict[str, list]:
    _human_entities_dict = dict(); # string_id: dictionary_serial_no
    _human_names_dict = defaultdict(lambda: list()) # dictionary_serial_no: [external_idsinkg2]
    with open(human_entities_file, 'r') as tsvin:
        tsvin = csv.reader(tsvin, delimiter="\t")
        for row  in tsvin:
            _human_entities_dict[row[2]]=row[0]
    with open(human_names_file, "r") as tsvin:
        tsvin = csv.reader(tsvin, delimiter="\t")
        for row in tsvin:
            identifier = _reformat_id(row[1])
            if identifier is not None:
                _human_names_dict[row[0]].append(identifier)
    gene_id_dict = dict() # string id: [external_ids in kg2]
    for k, v in _human_entities_dict.items():
        if len(_human_names_dict[v]) != 0:
            gene_id_dict[k] = _human_names_dict[v]
    return gene_id_dict

def make_gene_pmids_dict(gene_ids:set, filename:str) -> Dict[str, set]:
    gene_pmids_dict = dict()
    with open(filename, 'r') as inp:
        tsvin = csv.reader(inp, delimiter="\t")
        for row in tsvin:
            gene_id, pmidlist = row
            if gene_id not in gene_ids:
                continue
            pmidlist = ["PMID:"+idnum for idnum in pmidlist.split(' ')]
            gene_pmids_dict[gene_id] = set(pmidlist)
    return gene_pmids_dict

def make_disease_pmids_dict(filename:str) -> Dict[str,set]:
    disease_pmids_dict = dict()
    with open(filename, 'r') as inp:
        tsvin = csv.reader(inp, delimiter="\t")
        for row in tsvin:
            disease_id, pmidlist = row
            if "DOID" not in disease_id:
                continue
            pmidlist = ["PMID:"+idnum for idnum in pmidlist.split(' ')]
            disease_pmids_dict[disease_id] = set(pmidlist)
    return disease_pmids_dict


def _reformat_id(id:str):
    if "HGNC" in id:
        return id; # HGNC ids are already formatted the same as KG2 nodes
    # for now, just using HGNC gene ids to keep the size of this etl managable.
    #uniprot_match = REGEX_UNIPROT_ID.match(id)
    #if uniprot_match is not None:
    #    return "UniProtKB:"+id
    #ensembl_match = REGEX_ENSEMBL_ID.match(id)
    #if ensembl_match is not None:
    #    return "ENSEMBL:"+id
    return None 
    
def make_edges(input_tsv:str, gene_id_dict:Dict[str,list], pmids_dict:Dict[str,Dict[str,set]], test_mode: bool) -> list:
    gene_ids_actually_used = set()
    update_date = datetime.datetime.now().replace(microsecond=0).isoformat()
    with open(input_tsv) as inp:
        tsvin = csv.reader(inp, delimiter="\t")
        edges = list()
        for row in tsvin:
            [gene_id,
            gene_name,
            disease_id,
            disease_name,
            z_score,
            _,
            source_url] = row
            gene_ids_actually_used.add(gene_id)
            kg2_gene_id_list = gene_id_dict.get(gene_id, None)
            if kg2_gene_id_list is None:
                # print(f"Missing kg2 equivalent gene ids for {gene_id}. Skipping")
                continue
            if float(z_score) < 2.0:
                continue
            for kg2_gene_id in kg2_gene_id_list:
                if pmids_dict['disease'].get(disease_id, None) is None:
                    # print(f"Disease id {disease_id} is not DOID. Skipping.")
                    continue
                publications_list = list(pmids_dict['gene'][gene_id].intersection(pmids_dict['disease'][disease_id]))
                edge = kg2_util.make_edge(kg2_gene_id,
                                          disease_id,
                                          "JensenLab:associated_with",
                                          "associated_with",
                                          kg2_util.CURIE_ID_JENSENLAB,
                                          update_date)
                # seems hacky, but following example in rtx_kg1_neo4j_to_kg_json.py
                publication_info_dict = {'publication date': None,
                                         'sentence': None,
                                         'subject score': None,
                                         'object score': str(z_score)}
                publications_info = {edge['object']: publication_info_dict}
                edge["publications"] = publications_list
                edge["publications_info"] = publications_info
                edges.append(edge)
            if test_mode and len(gene_ids_actually_used) > 1000:
                break
        
    used_genes_missing_ids = gene_ids_actually_used - set(gene_id_dict.keys())
    print(f"Skipped {len(used_genes_missing_ids)} rows for lack of kg2 gene ids.")
    print(f"Found {len(gene_ids_actually_used - used_genes_missing_ids)} used kg2 gene ids.")
    return edges

if __name__ == '__main__':
    args = get_args()
    human_names_file = f"{args.inputDirectory}/human_dictionary/human_names.tsv" 
    human_entities_file = f"{args.inputDirectory}/human_dictionary/human_entities.tsv" 
    edges_tsv_file = f"{args.inputDirectory}/human_disease_textmining_full.tsv"
    gene_publications_file = f"{args.inputDirectory}/gene_pmids.tsv"
    disease_publications_file = f"{args.inputDirectory}/disease_pmids.tsv"
    gene_id_dict = make_gene_id_dictionary(human_names_file, human_entities_file)
    gene_pmids_dict = make_gene_pmids_dict(set(gene_id_dict.keys()), gene_publications_file)
    disease_pmids_dict = make_disease_pmids_dict(disease_publications_file)
    pmids_dict = { "gene": gene_pmids_dict,
                   "disease" : disease_pmids_dict }    

    edge_list = make_edges(edges_tsv_file, gene_id_dict, pmids_dict, args.test)
    print(f"Added {len(edge_list)} edges.")
    nodes = []
    update_date = datetime.datetime.now().replace(microsecond=0).isoformat()
    jensen_lab_source_node = kg2_util.make_node(kg2_util.CURIE_ID_JENSENLAB,
                                                kg2_util.BASE_URL_JENSENLAB,
                                                "Jensen Lab Disease Gene Associations",
                                                kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                                update_date,
                                                kg2_util.CURIE_ID_JENSENLAB)
                                        
    nodes.append(jensen_lab_source_node)
    graph = {'nodes': nodes,
             'edges': edge_list}
    kg2_util.save_json(graph, args.outputFile, args.test)
