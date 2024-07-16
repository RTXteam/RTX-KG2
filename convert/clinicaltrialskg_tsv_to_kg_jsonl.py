#!/usr/bin/env python3
'''clinicaltrialskg_tsv_to_kg_jsonl.py: Extracts a KG2 JSON file from the ClinicalTrials Knowledge Graphy in TSV format

   Usage: clinicaltrialskg_tsv_to_kg_jsonl.py [--test] <inputFile.tsv> <outputNodesFile.json> <outputEdgesFile.json>
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


CLINICALTRIALSKG_BASE_IRI = kg2_util.BASE_URL_CLINICALTRIALSKG
CLINICALTRIALSKG_CURIE = kg2_util.CURIE_ID_CLINICALTRIALSKG

TEST_MODE_LIMIT = 10000


def get_args():
    description = 'clinicaltrialskg_tsv_to_kg_jsonl.py: builds a KG2 JSON file from the \
                   ClinicalTrials Knowledge Graph TSV file'
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
    with open(input_file, 'r') as input_tsv:
        tsvreader = csv.reader(input_tsv, delimiter='\t')
        for line in tsvreader:
            count += 1
            if count == 1:
                continue
            if test_mode and count >= TEST_MODE_LIMIT:
                break
            [clinicaltrialskg_edge_id,
             subject_id,
             predicate,
             object_id,
             subject_name,
             object_name,
             category,
             knowledge_level,
             agent_type,
             nctid,
             phase,
             primary_purpose,
             intervention_model,
             time_perspective,
             overall_status,
             start_date,
             enrollment,
             enrollment_type,
             age_range,
             child,
             adult,
             older_adult
             unii] = line

            edge = kg2_util.make_edge_biolink(subject_id,
                                              object_id,
                                              predicate,
                                              CLINICALTRIALSKG_CURIE,
                                              start_date)
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

    kp_node = kg2_util.make_node(CLINICALTRIALSKG_CURIE,
                                 CLINICALTRIALSKG_BASE_IRI,
                                 "Clinical Trials Knowledge Graph",
                                 kg2_util.SOURCE_NODE_CATEGORY,
                                 None,
                                 CLINICALTRIALSKG_CURIE)
    nodes_output.write(kp_node)

    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)

    print("Finish time: ", date())
