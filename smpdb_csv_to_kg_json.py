#!/usr/bin/env python3
''' smpdb_csv_to_kg_json.py: Extracts a KG2 JSON file from the
    SMPDB dataset

    Usage: drugbank_xml_to_kg_json.py [--test] <inputFile.csv>
    <outputFile.json>
'''

import csv
import kg2_util
import json
import os
import xmltodict
import datetime
import argparse

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

SMPDB_BASE_IRI = 'https://identifiers.org/smpdb:'
SMPDB_RELATION_CURIE_PREFIX = 'SMPDB'
SMPDB_KB_IRI = 'https://registry.identifiers.org/registry/smpdb'
SMPDB_PROVIDED_BY_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY \
                                + ":smpdb"

def get_args():
    arg_parser = argparse.ArgumentParser(description='smpdb_csv_to_kg_json: \
                                         builds a KG2 JSON representation of \
                                         the Small Molecule Pathway Database')
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def make_smpdb_node(smpdb_id: str,
                description: str,
                name: str,
                category_label: str):
    iri = SMPDB_BASE_IRI + smpdb_id
    node_curie = kg2_util.CURIE_PREFIX_SMPDB + ":" + smpdb_id
    node_dict = kg2_util.make_node(node_curie,
                                    iri,
                                    name,
                                    category_label,
                                    None,
                                    SMPDB_PROVIDED_BY_CURIE_ID)
    node_dict["description"] = description
    return node_dict

def make_smpdb_nodes(smpdb):
    row = 1
    nodes = []
    for line in smpdb:
        if row > 1:
            node_smpdb = make_smpdb_node(line[0], line[4], line[2], "pathway")
            nodes.append(node_smpdb)
        row += 1
    return nodes

if __name__ == '__main__':
    args = get_args()
    test_mode = args.test
    input_file_name = args.inputFile
    output_file_name = args.outputFile
    smpdb = csv.reader(open(input_file_name), delimiter=",", quotechar='"')
    smpdb_kp_node = kg2_util.make_node(SMPDB_PROVIDED_BY_CURIE_ID,
                                       SMPDB_KB_IRI,
                                       "Small Molecule Pathway Database",
                                       kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                       None,
                                       SMPDB_PROVIDED_BY_CURIE_ID)
    nodes = []
    edges = []

    smpdb_data = make_smpdb_nodes(smpdb)
    for node in smpdb_data:
        nodes.append(node)

    nodes.append(smpdb_kp_node)
    kg2_util.save_json({"nodes" : nodes, "edges": edges}, output_file_name, test_mode)