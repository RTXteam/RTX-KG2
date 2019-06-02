#!/usr/bin/env python3
'''kg2_merge.py: merge two KGs that are in the KG2 JSON format

   Usage: kg2_merge.py <kg_alpha.json> <kg_beta.json> <output.json>
   Note: any of the three file arguments can have a ".gz" extension, in which case gzip is used for reading/writing.
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
import gzip
import json
import pprint
import pymysql
import shutil
import tempfile


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='semmeddb_mysql_to_json.py: extracts all the predicate triples from SemMedDB, in the RTX KG2 JSON format')
    arg_parser.add_argument('kgAlpha', type=str, nargs=1)
    arg_parser.add_argument('kgBeta', type=str, nargs=1)
    arg_parser.add_argument('outputFile', type=str, nargs=1)
    return arg_parser

if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    kg1_file_name = args.kgAlpha[0]
    if not kg1_file_name.endswith('.gz'):
        kg1_file = open(kg1_file_name, 'r')
        kg1 = json.load(kg1_file)
    else:
        kg1_file = gzip.GzipFile(kg1_file_name, 'r')
        kg1 = json.loads(kg1_file.read().decode('utf-8'))
    kg2_file_name = args.kgBeta[0]
    if not kg2_file_name.endswith('.gz'):
        kg2_file = open(kg2_file_name, 'r')
        kg2 = json.load(kg2_file)
    else:
        kg2_file = gzip.GzipFile(kg2_file_name, 'r')
        kg2 = json.loads(kg2_file.read().decode('utf-8'))
    kg1['edges'] = kg1['edges'] + kg2['edges']
    kg1['nodes'] = kg1['nodes'] + kg2['nodes']
    temp_output_file_name = tempfile.mkstemp(prefix='kg2-')[1]
    output_file_name = args.outputFile[0]
    if not output_file_name.endswith('.gz'):
        temp_output_file = open(temp_output_file_name, 'w')
        json.dump(kg1, temp_output_file, indent=4, sort_keys=True)
    else:
        temp_output_file = gzip.GzipFile(temp_output_file_name, 'w')
        temp_output_file.write(json.dumps(kg1, indent=4, sort_keys=True).encode('utf-8'))
    shutil.move(temp_output_file_name, output_file_name)

        

    
