#!/usr/bin/env python3
''' Prompts the user to enter a password on standard input and saves the password to a temporary file. Prints the temp file name.

    Usage: prompt_for_password_and_save_to_temp_file.py
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
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configFile", type=str, help="RTXConfiguration JSON file containing the password", required=True)
    arguments = parser.parse_args()
    config_file_name = arguments.configFile
    config_data = json.load(open(config_file_name, 'r'))
    config_data_kg2_neo4j = config_data['KG2']['neo4j']
    neo4j_password = config_data_kg2_neo4j['password']
    print(neo4j_password)
