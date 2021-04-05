#!/usr/bin/env python3
''' drugcentral_psql_to_drugcentral_json.py: Converts a PostgreSQL output
    file and the query that produced it and stores it under a key in
    a JSON file.

    Usage: drugcentral_psql_to_drugcentral_json.py <inputFile.txt>
    <outputFile.json> <outputKey> --query <query>
'''


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
    description = "drugcentral_psql_to_drugcentral_json.py: takes a \
                   PostgreSQL output file and query and converts \
                   it into JSON."
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    arg_parser.add_argument('outputKey', type=str)
    arg_parser.add_argument('--query', type=str, nargs='+')
    return arg_parser.parse_args()


def format_header(query: str):
    select_statement = query.split('from')[0]
    columns = query.replace('select', '').replace('distinct', '').strip()
    return [column.strip() for column in columns.split(',')]


if __name__ == '__main__':
    args = get_args()
    output_file = args.outputFile

    # Convert the query into a header for the returned data by
    # stripping off everything except the selected columns
    query = ' '.join(args.query).lower()
    header = format_header(query)

    # Iterate through each line the psql's dump file, split the
    # tab separated lines, and add a dictionary (with each item
    # in the header being attached to its item in the line) to
    # the processed_data list
    processed_data = list()
    with open(args.inputFile, 'r') as tempfile:
        for line in tempfile:
            line = [value.strip() for value in line.split('\t')]
            if len(line) < len(header):
                continue
            value_count = 0
            processed_line = dict()
            for value in line:
                processed_line[header[value_count]] = value
                value_count += 1
            processed_data.append(processed_line)

    # Open the output file and load the existing data in it into a dictionary.
    # Then, make a new key using the key passed into the script in that
    # dictionary. Finally, delete all of the data from the file and put the
    # whole dictionary in.
    with open(output_file, 'r+') as output:
        try:
            json_output = json.load(output)
        except json.decoder.JSONDecodeError:
            json_output = dict()
        json_output[args.outputKey] = processed_data
        output.seek(0)
        output.truncate()
        output.write(json.dumps(json_output))
