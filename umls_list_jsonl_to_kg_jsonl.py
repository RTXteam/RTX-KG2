#!/usr/bin/env python3
'''umls_list_jsonl_to_kg_jsonl.py: converts UMLS MySQL JSON Lines dump into KG2 JSON format

   Usage: umls_list_jsonl_to_kg_jsonl.py [--test] <inputFile.jsonl> <outputNodesFile.json> <outputEdgesFile.jsonl>
'''

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


import argparse
import kg2_util
import json


DESIRED_CODES = ['ATC', 'CHV', 'DRUGBANK', 'FMA', 'GO', 'HCPCS', 'HGNC', 'HL7V3.0',
                 'HL7', 'HPO', 'ICD10PCS', 'ICD9CM', 'MED-RT', 'MEDLINEPLUS', 'MSH',
                 'MTH', 'NCBI', 'NCBITAXON', 'NCI', 'NDDF', 'NDFRT', 'OMIM', 'PDQ',
                 'PSY', 'RXNORM', 'VANDF']
CUIS_KEY = 'cuis'
INFO_KEY = 'attributes'
NAMES_KEY = 'names'
TUIS_KEY = 'tuis'

UMLS_SOURCE_PREFIX = kg2_util.CURIE_PREFIX_UMLS_SOURCE


def get_args():
    arg_parser = argparse.ArgumentParser(description='umls_list_jsonl_to_kg_jsonl.py: converts UMLS MySQL JSON Lines dump into KG2 JSON format')
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputNodesFile', type=str)
    arg_parser.add_argument('outputEdgesFile', type=str)
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    return arg_parser.parse_args()


def extract_node_id(node_id_str):
    node_id_str = node_id_str.replace('(', '').replace(')', '').replace("'", '')
    node_id = node_id_str.split(',')
    return node_id[1].strip(), node_id[0].strip()


def make_node_id(curie_prefix, node_id):
    return curie_prefix + ':' + node_id


def process_drugbank_item(node_id, info, tui_mappings, iri_mappings, nodes_output, edges_output):
    curie_prefix = kg2_util.CURIE_PREFIX_DRUGBANK
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, curie_prefix)
    iri = iri_mappings[curie_prefix] + node_id
    node_curie = make_node_id(curie_prefix, node_id)
    cuis = info.get(CUIS_KEY, list())
    tuis = info.get(TUIS_KEY, list())
    fda_codes = info.get(INFO_KEY, dict()).get('FDA_UNII_CODE', list())
    secondary_accession_keys = info.get(INFO_KEY, dict()).get('SID', list())
    name = info.get(NAMES_KEY, dict()).get('IN', dict()).get('N', list())
    if len(name) == 0:
        name = info.get(NAMES_KEY, dict()).get('IN', dict()).get('Y', list())
    assert len(name) == 1, str(name) + " " + node_curie
    name = name[0]
    synonyms = list()
    for syn_cat in info.get(NAMES_KEY, dict()).get('SY', dict()):
        synonyms += info.get(NAMES_KEY, dict()).get('SY', dict())[syn_cat]
    for syn_cat in info.get(NAMES_KEY, dict()).get('FSY', dict()):
        synonyms += info.get(NAMES_KEY, dict()).get('FSY', dict())[syn_cat]

    # TODO: figure out update date
    node = kg2_util.make_node(node_curie, iri, name, tui_mappings[str(tuple(tuis))], "2023", provided_by)
    node['synonym'] = synonyms
    description = str()
    for tui in tuis:
        description += "; UMLS Semantic Type: STY:" + tui
    description.strip("; ")
    node['description'] = description
    
    nodes_output.write(node)


if __name__ == '__main__':
    args = get_args()
    input_file_name = args.inputFile
    test_mode = args.test
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile

    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    input_read_jsonlines_info = kg2_util.start_read_jsonlines(input_file_name)
    input_items = input_read_jsonlines_info[0]

    tui_mappings = dict()

    with open('tui_combo_mappings.json') as mappings:
        tui_mappings = json.load(mappings)

    iri_mappings = dict()
    iri_mappings_raw = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('curies-to-urls-map.yaml'))['use_for_bidirectional_mapping']
    for item in iri_mappings_raw:
        for prefix in item:
            iri_mappings[prefix] = item[prefix]
    print(json.dumps(iri_mappings, indent=4, sort_keys=True))

    for data in input_items:
        # There should only be one item in the data dictionary
        for entity in data:
            if entity == "('NOCODE', 'MTH')":
                continue
            value = data[entity]
            source, node_id = extract_node_id(entity)
            if source not in DESIRED_CODES and source != 'UMLS':
                continue

            # Process the data specifically by source
            if source == 'DRUGBANK':
                process_drugbank_item(node_id, value, tui_mappings, iri_mappings, nodes_output, edges_output)

    kg2_util.end_read_jsonlines(input_read_jsonlines_info)
    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)