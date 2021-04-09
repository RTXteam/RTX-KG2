#!/usr/bin/env python3
'''disgenet_tsv_to_kg_json.py: Extracts a KG2 JSON file from the DisGeNET
   gene to disease annoations in TSV format

   Usage: disgenet_tsv_to_kg_json.py [--test] <inputFile.tsv> <outputFile.json>
'''

import argparse
import kg2_util
import csv

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


DISGENET_BASE_IRI = kg2_util.BASE_URL_DISGENET
DISGENET_KB_CURIE = kg2_util.CURIE_ID_DISGENET

TEST_MODE_LIMIT = 10000


def get_args():
    description = 'disgenet_tsv_to_kg_json.py: builds a KG2 JSON file from the \
                   DisGeNET gene to disease annoations TSV file'
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('--test',
                            dest='test',
                            action="store_true",
                            default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def format_id(id: str, prefix: str):
    return prefix + ':' + id.strip()


def make_edges(input_file: str, test_mode: bool):
    edges = []
    count = 0
    non_befree_count = 0
    with open(input_file, 'r') as input_tsv:
        tsvreader = csv.reader(input_tsv, delimiter='\t')
        for line in tsvreader:
            count += 1
            if count == 1:
                continue
            if test_mode and non_befree_count >= TEST_MODE_LIMIT:
                break
            [subject_id,
             _,
             _,
             _,
             object_id,
             _,
             _,
             _,
             _,
             score,
             evidence_score,
             created_date,
             update_date,
             pmid,
             source] = line
            if source != 'BEFREE':
                non_befree_count += 1
                subject_id = format_id(subject_id,
                                       kg2_util.CURIE_PREFIX_NCBI_GENE)
                object_id = format_id(object_id,
                                      kg2_util.CURIE_PREFIX_UMLS)
                predicate = kg2_util.EDGE_LABEL_BIOLINK_GENE_ASSOCIATED_WITH_CONDITION
                edge = kg2_util.make_edge_biolink(subject_id,
                                                  object_id,
                                                  predicate,
                                                  DISGENET_KB_CURIE,
                                                  update_date)
                edge['publications'] = [pmid]
                edges.append(edge)
    return edges


if __name__ == '__main__':
    args = get_args()
    input_file = args.inputFile
    output_file = args.outputFile
    edges = make_edges(input_file, args.test)
    nodes = []
    kp_node = kg2_util.make_node(DISGENET_KB_CURIE,
                                 DISGENET_BASE_IRI,
                                 "DisGeNET",
                                 kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                 None,
                                 DISGENET_KB_CURIE)
    nodes.append(kp_node)
    graph = {"edges": edges,
             "nodes": nodes}
    kg2_util.save_json(graph, output_file, args.test)
