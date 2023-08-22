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
import umls_util

TUI_MAPPINGS = dict()
IRI_MAPPINGS = dict()

# ATC_PREFIX = kg2_util.CURIE_PREFIX_ATC
# CHV_PREFIX = kg2_util.CURIE_PREFIX_CHV
# DRUGBANK_PREFIX = kg2_util.CURIE_PREFIX_DRUGBANK
# FMA_PREFIX = kg2_util.CURIE_PREFIX_FMA
# GO_PREFIX = kg2_util.CURIE_PREFIX_GO
# HCPCS_PREFIX = kg2_util.CURIE_PREFIX_HCPCS
# HGNC_PREFIX = kg2_util.CURIE_PREFIX_HGNC
# HL7_PREFIX = kg2_util.CURIE_PREFIX_UMLS
# HPO_PREFIX = kg2_util.CURIE_PREFIX_HP
# ICD10PCS_PREFIX = kg2_util.CURIE_PREFIX_ICD10PCS
# ICD9CM_PREFIX = kg2_util.CURIE_PREFIX_ICD9
# MEDRT_PREFIX = kg2_util.CURIE_PREFIX_UMLS
# MEDLINEPLUS_PREFIX = kg2_util.CURIE_PREFIX_UMLS
# MSH_PREFIX = kg2_util.CURIE_PREFIX_MESH
# MTH_PREFIX = kg2_util.CURIE_PREFIX_UMLS
# NCBI_PREFIX = kg2_util.CURIE_PREFIX_NCBI_TAXON
# NCI_PREFIX = kg2_util.CURIE_PREFIX_NCIT
# NDDF_PREFIX = kg2_util.CURIE_PREFIX_NDDF
# OMIM_PREFIX = kg2_util.CURIE_PREFIX_OMIM
# PDQ_PREFIX = kg2_util.CURIE_PREFIX_PDQ
# PSY_PREFIX = kg2_util.CURIE_PREFIX_PSY
# RXNORM_PREFIX = kg2_util.CURIE_PREFIX_RXNORM
# VANDF_PREFIX = kg2_util.CURIE_PREFIX_VANDF

# UMLS_SOURCE_PREFIX = kg2_util.CURIE_PREFIX_UMLS_SOURCE

# DESIRED_CODES = {'ATC': [umls_util.process_atc_item, kg2_util.CURIE_PREFIX_ATC, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'ATC')],
#                  'CHV': [umls_util.process_chv_item, kg2_util.CURIE_PREFIX_CHV, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'CHV')],
#                  'DRUGBANK': [umls_util.process_drugbank_item, kg2_util.CURIE_PREFIX_DRUGBANK, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'DRUGBANK')],
#                  'FMA': [umls_util.process_fma_item, kg2_util.CURIE_PREFIX_FMA, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'FMA')],
#                  'GO': [umls_util.process_go_item, kg2_util.CURIE_PREFIX_GO, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'GO')],
#                  'HCPCS': [umls_util.process_hcpcs_item, kg2_util.CURIE_PREFIX_HCPCS, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'HCPCS')],
#                  'HGNC': [umls_util.process_hgnc_item, kg2_util.CURIE_PREFIX_HGNC, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'HGNC')],
#                  'HL7V3.0': [umls_util.process_hl7_item, kg2_util.CURIE_PREFIX_UMLS, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'HL7')],
#                  'HPO': [umls_util.process_hpo_item, kg2_util.CURIE_PREFIX_HP, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'HPO')],
#                  'ICD10PCS': [umls_util.process_icd10pcs_item, kg2_util.CURIE_PREFIX_ICD10PCS, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'ICD10PCS')],
#                  'ICD9CM': [umls_util.process_icd9cm_item, kg2_util.CURIE_PREFIX_ICD9, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'ICD9CM')],
#                  'MED-RT': [umls_util.process_medrt_item, kg2_util.CURIE_PREFIX_UMLS, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'MED-RT')],
#                  'MEDLINEPLUS': [umls_util.process_medlineplus_item, kg2_util.CURIE_PREFIX_UMLS, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'MEDLINEPLUS')],
#                  'MSH': [umls_util.process_msh_item, kg2_util.CURIE_PREFIX_MESH, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'MSH')],
#                  'MTH': [umls_util.process_mth_item, kg2_util.CURIE_PREFIX_UMLS, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'MTH')],
#                  'NCBI': [umls_util.process_ncbi_item, kg2_util.CURIE_PREFIX_NCBI_TAXON, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'NCBITAXON')],
#                  'NCI': [umls_util.process_nci_item, kg2_util.CURIE_PREFIX_NCIT, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'NCI')],
#                  'NDDF': [umls_util.process_nddf_item, kg2_util.CURIE_PREFIX_NDDF, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'NCI')],
#                  'OMIM': [umls_util.process_omim_item, kg2_util.CURIE_PREFIX_OMIM, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'OMIM')],
#                  'PDQ': [umls_util.process_pdq_item, kg2_util.CURIE_PREFIX_PDQ, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'PDQ')],
#                  'PSY': [umls_util.process_psy_item, kg2_util.CURIE_PREFIX_PSY, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'PSY')],
#                  'RXNORM': [umls_util.process_rxnorm_item, kg2_util.CURIE_PREFIX_RXNORM, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'RXNORM')],
#                  'VANDF': [umls_util.process_vandf_item, kg2_util.CURIE_PREFIX_VANDF, umls_util.make_node_id(UMLS_SOURCE_PREFIX, 'VANDF')]}

# # Mined from HTML Page Source of https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
# ACCESSION_HEIRARCHY = list()
# ACCESSION_SOURCES_HEIRARCHY = dict()

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
    return node_id[0].strip(), node_id[1].strip()


def create_accession_heirarchy(full_heirarchy):
    for [source, key] in full_heirarchy:
        if source in DESIRED_CODES:
            ACCESSION_HEIRARCHY.append((source, key))

def create_accession_sources_heirarchy():
    for (source, key) in ACCESSION_HEIRARCHY:
        if source not in ACCESSION_SOURCES_HEIRARCHY:
            ACCESSION_SOURCES_HEIRARCHY[source] = list()
        ACCESSION_SOURCES_HEIRARCHY[source].append(key)

if __name__ == '__main__':
    print("Starting umls_list_jsonl_to_kg_jsonl.py at", kg2_util.date())
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

    name_keys = set()
    attribute_keys = set()

    with open('tui_combo_mappings.json') as mappings:
        TUI_MAPPINGS = json.load(mappings)

    iri_mappings_raw = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('curies-to-urls-map.yaml'))['use_for_bidirectional_mapping']
    full_heirarchy = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('umls-name-heirarchy.yaml'))
    for item in iri_mappings_raw:
        for prefix in item:
            IRI_MAPPINGS[prefix] = item[prefix]

    umls_processor = umls_util.UMLS_Processor(nodes_output, edges_output, TUI_MAPPINGS, IRI_MAPPINGS, full_heirarchy)

    for data in input_items:
        # There should only be one item in the data dictionary
        for entity in data:
            if entity == "('NOCODE', 'MTH')":
                continue
            value = data[entity]
            source, node_id = extract_node_id(entity)

            # Process the data specifically by source
            umls_processor.process_node(source, node_id, value)

    kg2_util.end_read_jsonlines(input_read_jsonlines_info)
    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)
    print("Finishing umls_list_jsonl_to_kg_jsonl.py at", kg2_util.date())
