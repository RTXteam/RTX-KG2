#!/usr/bin/env python3
'''repodb_csv_to_kg_json.py: Extracts a KG2 JSON file from the repoDB file in CSV format
   Usage: repodb_csv_to_kg_json.py [--test] <inputFile.tsv> <outputFile.json>
'''

__author__ = ''
__copyright__ = 'Oregon State University'
__credits__ = []
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import argparse
import kg2_util
import pandas as pd

DRUGBANK_CURIE = kg2_util.CURIE_PREFIX_DRUGBANK
UMLS_CURIE = kg2_util.CURIE_PREFIX_CUI
CLINICALTRIALS_IRI = "https://clinicaltrials.gov/ct2/show/"
REPODB_IRI = kg2_util.BASE_URL_REPODB
REPODB_CURIE = kg2_util.CURIE_PREFIX_REPODB
NCT_CUTRIE = kg2_util.CURIE_PREFIX_CLINICALTRIALS


def get_args():
    arg_parser = argparse.ArgumentParser(description='repodb_csv_to_kg_json.py: builds a KG2 JSON file from the repodb csv file')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def make_kg2_graph(input_file_name: str, test_mode: bool = False):
    nodes = []
    edges = []
    df = pd.read_csv(input_file_name)
    for idx in range(len(df)):
        if not df['status'].isna()[idx]:
            status = df['status'][idx].lower()
        else:
            status = "unknown_status"
        if not df['phase'].isna()[idx]:
            phase = df['phase'][idx].lower().replace(" ", "_").replace("/", "_or_")
        else:
            phase = "unknown_phase"
        relation = "clinically_tested_" + status + "_" + phase
        edge_dict = kg2_util.make_edge(subject_id=DRUGBANK_CURIE + df['drug_id'][idx],
                                       object_id=UMLS_CURIE + df['ind_id'][idx],
                                       relation=REPODB_IRI + '#' + kg2_util.convert_snake_case_to_camel_case(relation),
                                       relation_curie=REPODB_CURIE + relation,
                                       predicate_label=relation,
                                       provided_by=REPODB_CURIE + ':',
                                       update_date=None)
        if not df['NCT'].isna()[idx]:
            edge_dict['publications'].append(NCT_CUTRIE + df['NCT'][idx])
            edge_dict['publications info'][NCT_CUTRIE + df['NCT'][idx]] = CLINICALTRIALS_IRI + df['NCT'][idx]
        edges.append(edge_dict)
    return {'nodes': nodes,
            'edges': edges}


if __name__ == '__main__':
    args = get_args()
    input_file_name = args.inputFile
    output_file_name = args.outputFile
    test_mode = args.test
    graph = make_kg2_graph(input_file_name, test_mode)
    kg2_util.save_json(graph, output_file_name, test_mode)
