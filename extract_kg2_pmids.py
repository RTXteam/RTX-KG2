#!/usr/bin/env python3
''' extract_kg2_pmids.py: stores all PMIDs listed in KG2 in
    a JSON file to be used by pubmed_xml_to_kg_json.py

    Usage: extract_kg2_pmids.py <inputDirectory> <outputFile.json>
'''

import datetime
import kg2_util
import json
import argparse


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def get_args():
    arg_parser = argparse.ArgumentParser(description='extract_kg2_pmids.py: \
                                         stores all unique PMIDs listed in \
                                         KG2 in a JSON file to be used by \
                                         pubmed_xml_to_kg_json.py')
    input_description = "The Full KG2 JSON File"
    arg_parser.add_argument('inputFile', type=str, help=input_description)
    output_description = "A JSON File that Will Store a List of Unique PMIDs"
    arg_parser.add_argument('outputFile', type=str, help=output_description)
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    input_file = open(args.inputFile)
    kg2_data = json.load(input_file)
    input_file.close()

    publications = {}
    for node in kg2_data["nodes"]:
        for publication in node["publications"]:
            publications[publication] = None

    for edge in kg2_data["edges"]:
        for publication in edge["publications_info"].keys():
            publications[publication] = None
        for publication in edge["publications"]:
            publications[publication] = None

    publications_list = []
    for publication in publications.keys():
        if publication.startswith("PMID"):
            publications_list.append(publication)

    with open(args.outputFile, 'w+') as output_file:
        output_file.write(json.dumps(publications_list))
