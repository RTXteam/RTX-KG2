#!/usr/bin/env python3

'''Counts edges that reference a retired CUI node in a JSON knowledge graph in Biolink format; prints report to STDOUT.

   Usage: report_retired_cuis_in_json_kg_edges.py --inputFile <inputKGFile.json> --outputFile <outputFile.json>
   The input file can be optionally gzipped (specify with the .gz extension).
'''

__author__ = 'Amy Glen'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Amy Glen']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


import argparse
import datetime
import gzip
import json
import shutil
import sys
import tempfile


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='build-kg2: builds the KG2 knowledge graph for the RTX system')
    arg_parser.add_argument('--inputFile', type=str, nargs=1)
    arg_parser.add_argument('--outputFile', type=str, nargs=1)
    return arg_parser


def get_retired_cuis():
    retired_cuis = set()
    with open('/home/ubuntu/kg2-build/umls/META/MRCUI.RRF', 'r') as retired_cui_file:
        for line in retired_cui_file:
            cui = line.split('|')[0].strip()  # First column contains the retired CUI
            retired_cuis.add(cui)
    return retired_cuis


def is_cui_node(curie_id: str):
    assert ':' in curie_id
    return curie_id.split(':')[0] == 'CUI'


def get_cui(curie_id: str):
    assert 'CUI:' in curie_id
    cui = curie_id.split(':')[1]
    return cui


def count_edges_referencing_retired_cui_node(edges: list, retired_cuis: list):
    return len([edge for edge in edges if (is_cui_node(edge['subject']) and get_cui(edge['subject']) in retired_cuis)
                                        or (is_cui_node(edge['object']) and get_cui(edge['object']) in retired_cuis)])


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    input_file_name = args.inputFile[0]
    if not input_file_name.endswith('.gz'):
        input_file = open(input_file_name, 'r')
        graph = json.load(input_file)
    else:
        input_file = gzip.GzipFile(input_file_name, 'r')
        graph = json.loads(input_file.read().decode('utf-8'))

    if 'edges' not in graph:
        print("ERROR: Input JSON file doesn't have an 'edges' property!", file=sys.stderr)
    else:
        edges = graph['edges']
        retired_cuis = get_retired_cuis()
        stats = {'_report_datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 '_total_number_of_edges': len(edges),  # underscore is to make sure it sorts to the top of the report
                 'number_of_edges_referencing_retired_cui_node': count_edges_referencing_retired_cui_node(edges, retired_cuis)}

        temp_output_file = tempfile.mkstemp(prefix='kg2-')[1]
        with open(temp_output_file, 'w') as outfile:
            json.dump(stats, outfile, indent=4, sort_keys=True)
        shutil.move(temp_output_file, args.outputFile[0])
