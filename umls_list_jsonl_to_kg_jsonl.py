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
    return node_id[0].strip(), node_id[1].strip()


def make_node_id(curie_prefix, node_id):
    return curie_prefix + ':' + node_id


def create_description(comment, tuis):
    description = comment
    for tui in tuis:
        description += "; UMLS Semantic Type: STY:" + tui
    description = description.strip("; ")
    return description    


def get_name_synonyms(names_dict, accession_heirarchy):
    names = list()
    for key in accession_heirarchy:
        names += [name for name in names_dict.get(key, dict()).get('Y', list())]
        names += [name for name in names_dict.get(key, dict()).get('N', list())]
    assert len(names) > 0
    if len(names) == 1:
        return names[0], list()
    return names[0], names[1:]


def get_name_keys(names_dict):
    keys_list = []
    for key in names_dict:
        keys_list.append(key)
    return str(sorted(keys_list))


def process_atc_item(node_id, info, tui_mappings, iri_mappings, nodes_output, edges_output):
    curie_prefix = kg2_util.CURIE_PREFIX_ATC
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, curie_prefix)
    iri = iri_mappings[curie_prefix] + node_id
    node_curie = make_node_id(curie_prefix, node_id)
    cuis = info.get(CUIS_KEY, list())
    tuis = info.get(TUIS_KEY, list())

    # Currently not used, but extracting them in case we want them in the future
    atc_level = info.get(INFO_KEY, dict()).get('ATC_LEVEL', list())[0]
    is_drug_class = info.get(INFO_KEY, dict()).get('IS_DRUG_CLASS', list()) == ["Y"]

    name = str()
    synonyms = list()
    names = info.get(NAMES_KEY, dict())
    name, synonyms = get_name_synonyms(names, ['RXN_PT', 'PT', 'RXN_IN', 'IN'])

    node = kg2_util.make_node(node_curie, iri, name, tui_mappings[str(tuple(tuis))], "2023", provided_by)
    node['synonym'] = synonyms
    node['description'] = create_description("", tuis)

    nodes_output.write(node)


def process_chv_item(node_id, info, tui_mappings, iri_mappings, nodes_output, edges_output):
    curie_prefix = "CHV" # This should be replaced with a kg2_util prefix at some point
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, curie_prefix)
    iri = iri_mappings[curie_prefix] + node_id
    node_curie = make_node_id(curie_prefix, node_id)
    cuis = info.get(CUIS_KEY, list())
    tuis = info.get(TUIS_KEY, list())

    # Currently not used, but extracting them in case we want them in the future
    combo_score = info.get(INFO_KEY, dict()).get('COMBO_SCORE', list())
    combo_score_no_top_words = info.get(INFO_KEY, dict()).get('COMBO_SCORE_NO_TOP_WORDS', list())
    context_score = info.get(INFO_KEY, dict()).get('CONTEXT_SCORE', list())
    cui_score = info.get(INFO_KEY, dict()).get('CUI_SCORE', list())
    disparaged = info.get(INFO_KEY, dict()).get('DISPARAGED', list())
    frequency = info.get(INFO_KEY, dict()).get('FREQUENCY', list())

    name = str()
    synonyms = list()
    names = info.get(NAMES_KEY, dict())
    name, synonyms = get_name_synonyms(names, ['PT', 'SY'])

    node = kg2_util.make_node(node_curie, iri, name, tui_mappings[str(tuple(tuis))], "2023", provided_by)
    node['synonym'] = synonyms
    node['description'] = create_description("", tuis)

    nodes_output.write(node)


def process_drugbank_item(node_id, info, tui_mappings, iri_mappings, nodes_output, edges_output):
    curie_prefix = kg2_util.CURIE_PREFIX_DRUGBANK
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, curie_prefix)
    iri = iri_mappings[curie_prefix] + node_id
    node_curie = make_node_id(curie_prefix, node_id)
    cuis = info.get(CUIS_KEY, list())
    tuis = info.get(TUIS_KEY, list())

    # Currently not used, but extracting them in case we want them in the future
    fda_codes = info.get(INFO_KEY, dict()).get('FDA_UNII_CODE', list())
    secondary_accession_keys = info.get(INFO_KEY, dict()).get('SID', list())

    names = info.get(NAMES_KEY, dict())
    name, synonyms = get_name_synonyms(names, ['IN', 'SY', 'FSY'])

    # TODO: figure out update date
    node = kg2_util.make_node(node_curie, iri, name, tui_mappings[str(tuple(tuis))], "2023", provided_by)
    node['synonym'] = synonyms
    node['description'] = create_description("", tuis)
    
    nodes_output.write(node)


def process_fma_item(node_id, info, tui_mappings, iri_mappings, nodes_output, edges_output):
    curie_prefix = "FMA" # This should be replaced with a kg2_util prefix at some point
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, curie_prefix)
    iri = iri_mappings[curie_prefix] + node_id
    node_curie = make_node_id(curie_prefix, node_id)
    cuis = info.get(CUIS_KEY, list())
    tuis = info.get(TUIS_KEY, list())

    # Currently not used, but extracting them in case we want them in the future
    authority = info.get(INFO_KEY, dict()).get('AUTHORITY', list())
    date_last_modified = info.get(INFO_KEY, dict()).get('DATE_LAST_MODIFIED', list())

    name = str()
    synonyms = list()
    names = info.get(NAMES_KEY, dict())
    name, synonyms = get_name_synonyms(names, ['PT', 'SY'])

    node = kg2_util.make_node(node_curie, iri, name, tui_mappings[str(tuple(tuis))], "2023", provided_by)
    node['synonym'] = synonyms
    node['description'] = create_description("", tuis)

    nodes_output.write(node)


def process_go_item(node_id, info, tui_mappings, iri_mappings, nodes_output, edges_output):
    curie_prefix = kg2_util.CURIE_PREFIX_GO
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, curie_prefix)
    node_id = node_id.replace('GO:', '')
    iri = iri_mappings[curie_prefix] + node_id
    node_curie = make_node_id(curie_prefix, node_id)
    cuis = info.get(CUIS_KEY, list())
    tuis = info.get(TUIS_KEY, list())
    go_namespace = info.get(INFO_KEY, dict()).get('GO_NAMESPACE', list())
    assert len(go_namespace) == 1
    go_namespace = go_namespace[0]
    namespace_category_map = {'molecular_function': kg2_util.BIOLINK_CATEGORY_MOLECULAR_ACTIVITY,
                              'cellular_component': kg2_util.BIOLINK_CATEGORY_CELLULAR_COMPONENT,
                              'biological_process': kg2_util.BIOLINK_CATEGORY_BIOLOGICAL_PROCESS}
    category = namespace_category_map.get(go_namespace, tui_mappings[str(tuple(tuis))])
    go_comment = info.get(INFO_KEY, dict()).get('GO_COMMENT', str())

    # Currently not used, but extracting them in case we want them in the future
    date_created = info.get(INFO_KEY, dict()).get('DATE_CREATED', list())
    go_subset = info.get(INFO_KEY, dict()).get('GO_SUBSET', list())
    gxr = info.get(INFO_KEY, dict()).get('GXR', list())
    ref = info.get(INFO_KEY, dict()).get('REF', list())
    sid = info.get(INFO_KEY, dict()).get('SID', list())

    name = str()
    synonyms = list()
    names = info.get(NAMES_KEY, dict())
    name, synonyms = get_name_synonyms(names, ['PT', 'MTH_PT', 'SY', 'MTH_SY', 'ET', 'MTH_ET'])

    node = kg2_util.make_node(node_curie, iri, name, category, "2023", provided_by)
    node['synonym'] = synonyms
    if len(go_comment) > 0:
        go_comment = go_comment[0]
        go_comment = "// COMMENTS: " + go_comment
    node['description'] = create_description(go_comment, tuis)

    nodes_output.write(node)

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

    tui_mappings = dict()
    name_keys = set()

    with open('tui_combo_mappings.json') as mappings:
        tui_mappings = json.load(mappings)

    iri_mappings = dict()
    iri_mappings_raw = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string('curies-to-urls-map.yaml'))['use_for_bidirectional_mapping']
    for item in iri_mappings_raw:
        for prefix in item:
            iri_mappings[prefix] = item[prefix]

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
            if source == 'ATC':
                process_atc_item(node_id, value, tui_mappings, iri_mappings, nodes_output, edges_output)

            if source == 'CHV':
                process_chv_item(node_id, value, tui_mappings, iri_mappings, nodes_output, edges_output)

            if source == 'DRUGBANK':
                process_drugbank_item(node_id, value, tui_mappings, iri_mappings, nodes_output, edges_output)

            if source == 'FMA':
                process_fma_item(node_id, value, tui_mappings, iri_mappings, nodes_output, edges_output)

            if source == 'GO':
                process_go_item(node_id, value, tui_mappings, iri_mappings, nodes_output, edges_output)

    kg2_util.end_read_jsonlines(input_read_jsonlines_info)
    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)
    # print(json.dumps(name_keys, indent=4, sort_keys=True, default=list))
    print("Finishing umls_list_jsonl_to_kg_jsonl.py at", kg2_util.date())
