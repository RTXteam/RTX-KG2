#!/usr/bin/env python3
''' count_orphan_curie_prefix_pairs.py: Creates a sorted dictionary of
		the curie prefix pairs (subject and object) from a KG2
		orphan edges file (sorted by value from highest to lowest)

    Usage: count_orphan_curie_prefix_pairs.py <inputFile.json> 
	    <outputFile.json>
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
	description = 'count_orphan_curie_prefix_pairs.py: \
					Creates a sorted dictionary of the curie prefix \
					(subject and object) from a KG2 orphan edges file \
					(sorted by value from highest to lowest)'
	arg_parser = argparse.ArgumentParser(description=description)
	arg_parser.add_argument('--test',
							dest='test',
							action="store_true",
							default=False)
	input_help = "A KG2 Orphan Edges JSON File"
	arg_parser.add_argument('inputFile', type=str, help=input_help)

	output_help = "The JSON destination for the output dictionary"
	arg_parser.add_argument('outputFile', type=str, help=output_help)
	return arg_parser.parse_args()


if __name__ == '__main__':
	args = get_args()

	# Load in the orphan edges file
	with open(args.inputFile) as input_file:
		data = json.load(input_file)

		# subject_object_pairs is for the initial collection of the prefixes
		subject_object_pairs = {}

		# subject_object_pairs_sorted is for the sorted collection of them
		subject_object_pairs_sorted = {}
		
		# iterate through all the edges and store the curie prefix pairs
		for edge in data["edges"]:
			subject_object_pair = edge["subject"].split(":")[0] + "-" + \
								  edge["object"].split(":")[0]
			
			# add up how many times they show up
			if subject_object_pair in subject_object_pairs:
				subject_object_pairs[subject_object_pair] += 1
			else:
				subject_object_pairs[subject_object_pair] = 1

		# iterate through a list of the values from high to low
		for sorted_count in sorted(list(subject_object_pairs.values()),
								   reverse=True):
			# iterate through the items in the dictionary
			for prefix_pair, count in subject_object_pairs.items():
				if count == sorted_count:
					# store the prefix pairs from high to low by adding them
					# to the new dictionary in the high to low order
					subject_object_pairs_sorted[prefix_pair] = sorted_count

	# pretty print the output, but don't use sort_keys=True!
	data = json.dumps(subject_object_pairs_sorted, indent=4)

	# write the sorted data to the output file
	with open(args.outputFile, 'w') as output_file:
		output_file.write(data)