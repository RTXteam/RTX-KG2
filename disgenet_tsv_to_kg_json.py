#!/usr/bin/env python3
'''disgenet_tsv_to_kg_json.py: Extracts a KG2 JSON file from the DisGeNET
   gene to disease annoations in TSV format

   Usage: disgenet_tsv_to_kg_json.py [--test] <inputFile.tsv> <outputNodesFile.json> <outputEdgesFile.json>
'''

import argparse
import kg2_util
import csv
import datetime

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
    arg_parser.add_argument('outputNodesFile', type=str)
    arg_parser.add_argument('outputEdgesFile', type=str)
    return arg_parser.parse_args()


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_id(id: str, prefix: str):
    return prefix + ':' + id.strip()


def make_edges(input_file: str, edges_output, test_mode: bool):
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
                edge['publications'] = []
                if pmid is not None and pmid != '':
                    publication = kg2_util.CURIE_PREFIX_PMID + ':' + pmid
                    edge['publications'].append(publication)
                edges_output.write(edge)


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

    make_edges(input_file_name, edges_output, test_mode)

    kp_node = kg2_util.make_node(DISGENET_KB_CURIE,
                                 DISGENET_BASE_IRI,
                                 "DisGeNET",
                                 kg2_util.SOURCE_NODE_CATEGORY,
                                 None,
                                 DISGENET_KB_CURIE)
    nodes_output.write(kp_node)

    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)

    print("Finish time: ", date())
