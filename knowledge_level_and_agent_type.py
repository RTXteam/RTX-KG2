#!/usr/bin/env python3

''' Processes kg2_simplified_edges,jsonl and adds knowledge_level and agent_type to the edges.
    Agent type is the service that generated a knowledge triple.
    Usage: python3 knowledge_level_and_agent_type.py <input_edges_file> <output_file_location> <output_file>
    Example: python3 knowledge_level_and_agent_type.py kg2_simplified_edges.jsonl /kg2-build/ /kg2_simplified_edges_with_knowledge_level_and_agent_type.jsonl
'''

__author__ = 'Liliana Acevedo'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.0.1'
__maintainer__ = ''
__email__ = ''
__status__ = 'prototype'

import argparse
import kg2_util


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='kg2_jsonl_to_kgx_jsonl.py: converts a JSONL file in the KG2 format to a JSONL file in the KGX format')
    arg_parser.add_argument('input_edges_file', type=str)
    arg_parser.add_argument('output_file_location', type=str)
    arg_parser.add_argument('output_file', type=str)
    return arg_parser


# Check that all sources are represented in the agent_type dictionary
def check_sources(agent_type_dict, sources):
    for source in sources:
        if source not in agent_type_dict:
            print(f"Source {source} not in agent_type_dict")


# Add knowledge_level and agent_type to edges
def process_edges(input_edges_file, output_file_location, output_file, agent_type_map):

    print(f"Adding knowledge_level and agent_type to edges from {input_edges_file} to {output_file_location}/{output_file}")
  #  print(f"Type: {type(agent_type_map)} /nAgent type map: {agent_type_map}")

    edge_ctr = 0
    edges_read_jsonlines_data = kg2_util.start_read_jsonlines(input_edges_file)
    edges = edges_read_jsonlines_data[0]
    
    edges_info = kg2_util.create_kg2_jsonlines()
    edges_output = edges_info[0]

    for edge_dict in edges:
        edge_ctr += 1
        if edge_ctr % 1000000 == 0:
            print(f"Processed {edge_ctr} edges")
        # TODO: Add agent type map
        # check_sources(agent_type_map, sources)
        edge_dict['agent_type'] = 'not_provided'
        edge_dict['knowledge_level'] = 'not_provided'
        edges_info.write(edge_dict)


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
#    agent_type_map_file = args.agent_type_map_file
    input_edges_file = args.input_edges_file
    output_file_location = args.output_file_location
    output_file = args.output_file

    # TODO: Add agent type map
    # agent_type_map = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(agent_type_map_file))

    process_edges(input_edges_file, output_file_location, output_file)
