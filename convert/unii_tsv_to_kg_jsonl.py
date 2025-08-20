#!/usr/bin/env python3
'''unii_tsv_to_kg_json.py: Extracts a KG2 JSON file from the FDA UNII identifiers data file that is in TSV format

   Usage: unii_tsv_to_kg_json.py [--test] <inputFile.tsv> <outputNodesFile.json>
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
import kg2_util
import os
import datetime

## From the file "READ ME UNII Lists.txt":
## of = name identified as having official status
## sys = Systematic Name  (chemical and taxonomic names)
## cn = Common Name
## cd = Code
## bn = Brand/Trade Name
                                                                                
UNII_BASE_IRI = kg2_util.BASE_URL_UNII
UNII_KB_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY + ':' + 'unii'
UNII_KB_URL = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + 'unii'


def get_args():
    arg_parser = argparse.ArgumentParser(description='unii_tsv_to_kg_json.py: builds a KG2 JSON representation for FDA UNII identifiers')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputNodesFile', type=str)
    return arg_parser.parse_args()


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def make_node(unii_ingredient_id: str,
              name: str,
              full_name: str,
              update_date: str,
              category_label: str,
              other_synonyms: list = None) -> dict:

    if other_synonyms is None:
        other_synonyms = []
    node_curie = kg2_util.CURIE_PREFIX_UNII + ':' + unii_ingredient_id
    iri = UNII_BASE_IRI + unii_ingredient_id
    node_dict = kg2_util.make_node(node_curie,
                                   iri,
                                   name,
                                   category_label,
                                   update_date,
                                   UNII_KB_CURIE_ID)
    node_dict['synonym'] = sorted(list(set(other_synonyms)))
    node_dict['full_name'] = full_name
    return node_dict


def make_kg2_graph(input_file_name: str, nodes_output, test_mode: bool = False):

    update_date = os.path.getmtime(input_file_name)
    ontology_curie_id = UNII_KB_CURIE_ID
    ens_kp_node = kg2_util.make_node(ontology_curie_id,
                                     UNII_KB_URL,
                                     'FDA UNII',
                                     kg2_util.SOURCE_NODE_CATEGORY,
                                     update_date,
                                     ontology_curie_id)
    nodes_output.write(ens_kp_node)

    node_info_by_id = dict()
    
    line_ctr = 0
    with open(input_file_name, 'r') as input_file:
        for line in input_file:
            if line.startswith('#'):
                continue
            if line.startswith('Name') and line_ctr==0:
                continue
            if test_mode and line_ctr > 10000:
                break
            fields = line.rstrip("\n").split("\t")
            [name, ingredient_name_type, unii_ingredient_id, display_name] = fields
            assert name is not None
            assert display_name is not None
            node_info = node_info_by_id.get(unii_ingredient_id, None)
            if node_info is None:
                node_info = {'cn': set(),
                             'sys': set(),
                             'of': set(),
                             'bn': set(),
                             'cd': set(),
                             'mn': set(),
                             'synonyms': set()}
                node_info_by_id[unii_ingredient_id] = node_info
            assert ingredient_name_type in node_info, f"unknown ingredient name type ({ingredient_name_type}): " + line
            node_info[ingredient_name_type].add((name, display_name))
            node_info['synonyms'].add(name)
            node_info['synonyms'].add(display_name)
     
    ingredient_ctr = 0
    for unii_ingredient_id, node_info in node_info_by_id.items():
        ingredient_ctr += 1
        if node_info['of']:
            [name, display_name] = next(iter(node_info['of']))
        elif node_info['cn']:
            [name, display_name] = next(iter(node_info['cn']))
        elif node_info['cd']:
            [name, display_name] = next(iter(node_info['cd']))
        elif node_info['bn']:
            [name, display_name] = next(iter(node_info['bn']))
        elif node_info['sys']:
            [name, display_name] = next(iter(node_info['sys']))
        elif node_info['mn']:
            [name, display_name] = next(iter(node_info['mn']))
        else:
            assert False
        node_synonyms = node_info['synonyms']
        node_synonyms.remove(name)
        if display_name in node_synonyms:
            node_synonyms.remove(display_name)
        node_dict = make_node(unii_ingredient_id,
                              display_name,
                              name,
                              update_date,
                              'named thing',
                              node_synonyms)
        node_curie_id = node_dict['id']
        node_description = ''
        nodes_output.write(node_dict)


if __name__ == '__main__':
    print("Start time: ", date())
    args = get_args()
    input_file_name = args.inputFile
    output_nodes_file_name = args.outputNodesFile
    test_mode = args.test

    nodes_info, _ = kg2_util.create_kg2_jsonlines(test_mode, include_edges=False)
    nodes_output = nodes_info[0]

    make_kg2_graph(input_file_name, nodes_output, test_mode)
    
    kg2_util.close_kg2_jsonlines(nodes_info, None, output_nodes_file_name, None)

    print("Finish time: ", date())
