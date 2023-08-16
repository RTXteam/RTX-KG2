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
INFO_KEY = 'info'
NAMES_KEY = 'names'
TUIS_KEY = 'tuis'

TUI_MAPPINGS = {"T001": "individual organism",
                "T002": "organism taxon",
                "T004": "organism taxon",
                "T005": "organism taxon",
                "T007": "organism taxon",
                "T008": "organism taxon",
                "T010": "organism taxon",
                "T011": "organism taxon",
                "T012": "organism taxon",
                "T013": "organism taxon",
                "T014": "organism taxon",
                "T015": "organism taxon",
                "T016": "organism taxon",
                "T017": "anatomical entity",
                "T018": "gross anatomical structure",
                "T019": "disease",
                "T020": "disease",
                "T021": "gross anatomical structure",
                "T022": "anatomical entity",
                "T023": "gross anatomical structure",
                "T024": "gross anatomical structure",
                "T025": "cell",
                "T026": "cellular component",
                "T028": "biological entity",
                "T029": "anatomical entity",
                "T030": "anatomical entity",
                "T031": "anatomical entity",
                "T032": "named thing",
                "T033": "disease or phenotypic feature",
                "T034": "phenomenon",
                "T037": "pathological process",
                "T038": "phenomenon",
                "T039": "physiological process",
                "T040": "physiological process",
                "T041": "behavior",
                "T042": "physiological process",
                "T043": "physiological process",
                "T044": "molecular activity",
                "T045": "physiological process",
                "T046": "pathological process",
                "T047": "disease",
                "T048": "disease",
                "T049": "disease",
                "T050": "biological entity",
                "T051": "event",
                "T052": "activity",
                "T053": "behavior",
                "T054": "behavior",
                "T055": "behavior",
                "T056": "activity",
                "T057": "activity",
                "T058": "activity",
                "T059": "procedure",
                "T060": "procedure",
                "T061": "procedure",
                "T062": "activity",
                "T063": "procedure",
                "T064": "activity",
                "T065": "activity",
                "T066": "activity",
                "T067": "phenomenon",
                "T068": "phenomenon",
                "T069": "phenomenon",
                "T070": "phenomenon",
                "T071": "named thing",
                "T072": "physical entity",
                "T073": "physical entity",
                "T074": "device",
                "T075": "device",
                "T077": "information content entity",
                "T078": "information content entity",
                "T079": "information content entity",
                "T080": "information content entity",
                "T081": "information content entity",
                "T082": "information content entity",
                "T083": "geographic location",
                "T085": "biological entity",
                "T086": "nucleic acid entity",
                "T087": "polypeptide",
                "T088": "biological entity",
                "T089": "information content entity",
                "T090": "individual organism",
                "T091": "named thing",
                "T092": "agent",
                "T093": "agent",
                "T094": "agent",
                "T095": "agent",
                "T096": "agent",
                "T097": "cohort",
                "T098": "population of individual organisms",
                "T099": "cohort",
                "T100": "cohort",
                "T101": "cohort",
                "T102": "information content entity",
                "T103": "chemical entity",
                "T104": "chemical entity",
                "T109": "chemical entity",
                "T114": "nucleic acid entity",
                "T116": "polypeptide",
                "T120": "chemical entity",
                "T121": "drug",
                "T122": "device",
                "T123": "chemical entity",
                "T125": "chemical entity",
                "T126": "protein",
                "T127": "small molecule",
                "T129": "biological entity",
                "T130": "chemical entity",
                "T131": "chemical entity",
                "T167": "chemical entity",
                "T168": "food",
                "T169": "information content entity",
                "T170": "publication",
                "T171": "information content entity",
                "T184": "phenotypic feature",
                "T185": "information content entity",
                "T190": "disease",
                "T191": "disease",
                "T192": "protein",
                "T194": "organism taxon",
                "T195": "drug",
                "T196": "small molecule",
                "T197": "chemical entity",
                "T200": "drug",
                "T201": "named thing",
                "T203": "device",
                "T204": "organism taxon"}

def get_args():
    arg_parser = argparse.ArgumentParser(description='umls_list_jsonl_to_kg_jsonl.py: converts UMLS MySQL JSON Lines dump into KG2 JSON format')
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputNodesFile', type=str)
    arg_parser.add_argument('outputEdgesFile', type=str)
    return arg_parser.parse_args()


def extract_node_id(node_id_str):
    node_id_str = node_id_str.replace('(', '').replace(')', '').replace("'", '')
    node_id = node_id_str.split(',')
    return node_id[1].strip(), node_id[0].strip()


def make_node_id(curie_prefix, node_id_val):
    return curie_prefix + ':' + node_id_val


def process_drugbank_item(node_id_val, info):
    node_curie = make_node_id(kg2_util.CURIE_PREFIX_DRUGBANK, node_id_val)
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
    for syn_cat in info.get('SY', dict()):
        synonyms += info['SY'][syn_cat]
    
    print(json.dumps({'node_curie': node_curie, 'cuis': cuis, 'tuis': tuis, 'fda_codes': fda_codes, 'secondary_accession_keys': secondary_accession_keys, 'name': name, 'synonyms': synonyms}))
    return str(tuis)


if __name__ == '__main__':
    args = get_args()
    input_file_name = args.inputFile

    input_read_jsonlines_info = kg2_util.start_read_jsonlines(input_file_name)
    input_items = input_read_jsonlines_info[0]

    tui_combos = dict()

    for data in input_items:
        # There should only be one item in the data dictionary
        for entity in data:
            if entity == "('NOCODE', 'MTH')":
                continue
            value = data[entity]
            source, node_id_val = extract_node_id(entity)
            if source not in DESIRED_CODES and source != 'UMLS':
                continue

            # Process the data specifically by source
            tui_combo = tuple(sorted(value.get(TUIS_KEY, list())))
            if tui_combo not in tui_combos:
                tui_combos[tui_combo] = dict()
                tui_combos[tui_combo]['tuis'] = list()
                tui_combos[tui_combo]['tui_count'] = 0
            tui_combos[tui_combo]['tuis'].append(entity)
            tui_combos[tui_combo]['tui_count'] += 1
            if source == 'DRUGBANK':
                process_drugbank_item(node_id_val, value)

    lines = str()
    for tui_combo in tui_combos:
        line = str(tui_combos[tui_combo]['tui_count']) + '\t'
        for tui in tui_combo:
            line += tui + "\t" + TUI_MAPPINGS[tui] + "\t"
        line = line.strip()
        line += '\n'
        lines += line

    print(lines)

    kg2_util.end_read_jsonlines(input_read_jsonlines_info)