#!/usr/bin/env python3
''' hmdb_xml_to_kg_json.py: Extracts a KG2 JSON file from the
    HMDB metabolite download in XML format

    Usage: hmdb_xml_to_kg_json.py [--test] <inputFile.xml>
    <outputFile.json>
'''

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
    arg_parser = argparse.ArgumentParser(description='update_version.py: \
                                         increments the version of KG2')
    arg_parser.add_argument('--increment',
                            dest='increment',
                            action="store_true",
                            default=False)
    arg_parser.add_argument('versionFile', type=str)
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    input_file_name = args.versionFile
    increment = args.increment

    input_file = open(input_file_name, "r")
    for line in input_file:
    	input_file.close()
    	output_file = open(input_file_name, "w")
    	old_version = line.split(".")
    	graph_ver = old_version[0]
    	major_ver = old_version[1]
    	minor_ver = int(old_version[2])
    	if increment:
    		minor_ver += 1
    	new_version = graph_ver + "." + major_ver + "." + str(minor_ver)
    	output_file.write(new_version)
    	output_file.close()
    	break
