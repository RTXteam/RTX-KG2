#!/usr/bin/env python3

'''Script for investigating usage of invalid and retired CUIs in knowledge graph edges.

   Usage: report_problem_cuis_in_kg_edges.py --inputFile <inputKGFile.json> --outputFile <outputFile.json>
   The input file can be optionally gzipped (specify with the .gz extension).
'''

__author__ = 'Amy Glen'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Amy Glen']


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


def get_retired_cuis_by_type():
    retired_cuis_by_type = dict()
    retired_cuis_by_type['ALL'] = set()
    with open('/home/ubuntu/kg2-build/umls/META/MRCUI.RRF', 'r') as retired_cui_file:
        # Line format in MRCUI file: retired_cui|release|map_type|||remapped_cui|is_current|
        for line in retired_cui_file:
            row = line.split('|')
            old_cui = row[0]
            map_type = row[2]
            retired_cuis_by_type['ALL'].add(old_cui)
            if map_type not in retired_cuis_by_type:
                retired_cuis_by_type[map_type] = set()
            retired_cuis_by_type[map_type].add(old_cui)
    return retired_cuis_by_type


def is_cui_node(curie_id: str):
    assert ':' in curie_id
    return curie_id.split(':')[0] == 'CUI'


def get_cui(curie_id: str):
    assert 'CUI:' in curie_id
    cui = curie_id.split(':')[1]
    return cui


def count_edges_with_cui_in_set(edges: list, cuis: set):
    return sum(1 for edge in edges if (is_cui_node(edge['subject']) and get_cui(edge['subject']) in cuis)
                                        or (is_cui_node(edge['object']) and get_cui(edge['object']) in cuis))


def is_invalid_cui(curie_id: str):
    if is_cui_node(curie_id):
        cui = get_cui(curie_id)
        # CUIs are supposed to contain the letter 'C' followed by 7 numbers
        return len(cui) != 8 or not cui.startswith('C') or not cui[1:].isdigit()
    else:
        return False


def count_edges_with_invalid_cui(edges: list):
    return sum(1 for edge in edges if is_invalid_cui(edge['subject']) or is_invalid_cui(edge['object']))


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
        retired_cuis_by_type = get_retired_cuis_by_type()

        stats = {'_report_datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 '_total_number_of_edges': len(edges),  # underscore is to make sure it sorts to the top of the report
                 'number_of_edges_with_retired_cui': count_edges_with_cui_in_set(edges, retired_cuis_by_type.get('ALL')),
                 'number_of_edges_with_retired_cui_with_synonym': count_edges_with_cui_in_set(edges, retired_cuis_by_type.get('SY')),
                 'number_of_edges_with_invalid_cui': count_edges_with_invalid_cui(edges)}

        temp_output_file = tempfile.mkstemp(prefix='kg2-')[1]
        with open(temp_output_file, 'w') as outfile:
            json.dump(stats, outfile, indent=4, sort_keys=True)
        shutil.move(temp_output_file, args.outputFile[0])
