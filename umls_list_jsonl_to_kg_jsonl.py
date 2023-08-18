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

TUI_MAPPINGS = dict()
IRI_MAPPINGS = dict()

ATC_PREFIX = kg2_util.CURIE_PREFIX_ATC
CHV_PREFIX = kg2_util.CURIE_PREFIX_CHV
DRUGBANK_PREFIX = kg2_util.CURIE_PREFIX_DRUGBANK
FMA_PREFIX = kg2_util.CURIE_PREFIX_FMA
GO_PREFIX = kg2_util.CURIE_PREFIX_GO
HCPCS_PREFIX = kg2_util.CURIE_PREFIX_HCPCS
HGNC_PREFIX = kg2_util.CURIE_PREFIX_HGNC

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


def get_attribute_keys(attributes_dict):
    keys_list = []
    for key in attributes_dict:
        keys_list.append(key)
    return set(keys_list)


def make_umls_node(node_curie, iri, name, category, update_date, provided_by, synonyms, description, nodes_output):
    node = kg2_util.make_node(node_curie, iri, name, category, "2023", provided_by)
    node['synonym'] = synonyms
    node['description'] = description

    nodes_output.write(node)


def get_basic_info(curie_prefix, node_id, info, accession_heirarchy):
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, curie_prefix)
    iri = IRI_MAPPINGS[curie_prefix] + node_id
    node_curie = make_node_id(curie_prefix, node_id)
    cuis = info.get(CUIS_KEY, list())
    tuis = info.get(TUIS_KEY, list())
    category = TUI_MAPPINGS[str(tuple(tuis))]

    names = info.get(NAMES_KEY, dict())
    name, synonyms = get_name_synonyms(names, accession_heirarchy)

    return node_curie, iri, name, provided_by, category, synonyms, cuis, tuis


def process_atc_item(node_id, info, nodes_output, edges_output):
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(ATC_PREFIX, node_id, info, ['RXN_PT', 'PT', 'RXN_IN', 'IN'])

    # Currently not used, but extracting them in case we want them in the future
    atc_level = info.get(INFO_KEY, dict()).get('ATC_LEVEL', list())[0]
    is_drug_class = info.get(INFO_KEY, dict()).get('IS_DRUG_CLASS', list()) == ["Y"]

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_chv_item(node_id, info, nodes_output, edges_output):
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(CHV_PREFIX, node_id, info, ['PT', 'SY'])

    # Currently not used, but extracting them in case we want them in the future
    combo_score = info.get(INFO_KEY, dict()).get('COMBO_SCORE', list())
    combo_score_no_top_words = info.get(INFO_KEY, dict()).get('COMBO_SCORE_NO_TOP_WORDS', list())
    context_score = info.get(INFO_KEY, dict()).get('CONTEXT_SCORE', list())
    cui_score = info.get(INFO_KEY, dict()).get('CUI_SCORE', list())
    disparaged = info.get(INFO_KEY, dict()).get('DISPARAGED', list())
    frequency = info.get(INFO_KEY, dict()).get('FREQUENCY', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_drugbank_item(node_id, info, nodes_output, edges_output):
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(DRUGBANK_PREFIX, node_id, info, ['IN', 'SY', 'FSY'])

    # Currently not used, but extracting them in case we want them in the future
    fda_codes = info.get(INFO_KEY, dict()).get('FDA_UNII_CODE', list())
    secondary_accession_keys = info.get(INFO_KEY, dict()).get('SID', list())

    # TODO: figure out update date
    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_fma_item(node_id, info, nodes_output, edges_output):
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(FMA_PREFIX, node_id, info, ['PT', 'SY'])

    # Currently not used, but extracting them in case we want them in the future
    authority = info.get(INFO_KEY, dict()).get('AUTHORITY', list())
    date_last_modified = info.get(INFO_KEY, dict()).get('DATE_LAST_MODIFIED', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_go_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['PT', 'MTH_PT', 'SY', 'MTH_SY', 'ET', 'MTH_ET']
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(GO_PREFIX, node_id.replace('GO:', ''), info, accession_heirarchy)

    # GO-specific information
    attributes = info.get(INFO_KEY, dict())
    go_namespace = attributes.get('GO_NAMESPACE', list())
    assert len(go_namespace) == 1
    go_namespace = go_namespace[0]
    namespace_category_map = {'molecular_function': kg2_util.BIOLINK_CATEGORY_MOLECULAR_ACTIVITY,
                              'cellular_component': kg2_util.BIOLINK_CATEGORY_CELLULAR_COMPONENT,
                              'biological_process': kg2_util.BIOLINK_CATEGORY_BIOLOGICAL_PROCESS}
    category = namespace_category_map.get(go_namespace, category)
    go_comment = attributes.get('GO_COMMENT', str())
    if len(go_comment) > 0:
        go_comment = go_comment[0]
        go_comment = "// COMMENTS: " + go_comment

    # Currently not used, but extracting them in case we want them in the future
    date_created = attributes.get('DATE_CREATED', list())
    go_subset = attributes.get('GO_SUBSET', list())
    gxr = attributes.get('GXR', list())
    ref = attributes.get('REF', list())
    sid = attributes.get('SID', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description(go_comment, tuis), nodes_output)


def process_hcpcs_item(node_id, info, nodes_output, edges_output):
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(HCPCS_PREFIX, node_id, info, ['PT', 'MTH_HT', 'MP'])

    # Currently not used, but extracting them in case we want them in the future - descriptions from https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/attribute_names.html
    attributes = info.get(INFO_KEY, dict())
    had = attributes.get('HAD', list()) # HCPCS Action Effective Date - effective date of action to a procedure or modifier code.
    hcc = attributes.get('HCC', list()) # HCPCS Coverage Code - code denoting Medicare coverage status. There are two subelements separated by "=".
    hts = attributes.get('HTS', list()) # HCPCS Type of Service Code - carrier assigned HCFA Type of Service which describes the particular kind(s) of service represented by the procedure code.
    hcd = attributes.get('HCD', list()) # HCPCS Code Added Date - year the HCPCS code was added to the HCFA Common Procedure Coding System.
    hpn = attributes.get('HPN', list()) # HCPCS processing note number identifying the processing note contained in Appendix A of the HCPCS Manual.
    haq = attributes.get('HAQ', list()) # HCPCS Anesthesia Base Unit Quantity - base unit represents the level of intensity for anesthesia procedure services that reflects all activities except time.
    hlc = attributes.get('HLC', list()) # HCPCS Lab Certification Code - code used to classify laboratory procedures according to the specialty certification categories listed by CMS(formerly HCFA).
    hsn = attributes.get('HSN', list()) # HCPCS Statute Number identifying statute reference for coverage or noncoverage of procedure or service.
    hpd = attributes.get('HPD', list()) # HCPCS ASC payment group effective date - date the procedure is assigned to the ASC payment group.
    hpg = attributes.get('HPG', list()) # HCPCS ASC payment group code which represents the dollar amount of the facility charge payable by Medicare for the procedure.
    hmg = attributes.get('HMR', list()) # HCPCS Medicare Carriers Manual reference section number - number identifying a section of the Medicare Carriers Manual.
    hir = attributes.get('HIR', list()) # HCPCS Coverage Issues Manual Reference Section Number - number identifying the Reference Section of the Coverage Issues Manual.
    hxr = attributes.get('HXR', list()) # HCPCS Cross reference code - an explicit reference crosswalking a deleted code or a code that is not valid for Medicare to a valid current code (or range of codes).
    hmp = attributes.get('HMP', list()) # HCPCS Multiple Pricing Indicator Code - code used to identify instances where a procedure could be priced.
    hpi = attributes.get('HPI', list()) # HCPCS Pricing Indicator Code - used to identify the appropriate methodology for developing unique pricing amounts under Part B.
    hac = attributes.get('HAC', list()) # HCPCS action code - code denoting the change made to a procedure or modifier code within the HCPCS system.
    hbt = attributes.get('HBT', list()) # HCPCS Berenson-Eggers Type of Service Code - BETOS for the procedure code based on generally agreed upon clinically meaningful groupings of procedures and services.

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_hgnc_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['ACR', 'PT', 'MTH_ACR', 'NA', 'NP', 'NS', 'SYN']
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(HGNC_PREFIX, node_id.replace('HGNC:', ''), info, accession_heirarchy)

    # Currently not used, but extracting them in case we want them in the future - descriptions from https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/attribute_names.html
    attributes = info.get(INFO_KEY, dict())
    mgd_id = attributes.get('MGD_ID', list())
    vega_id = attributes.get('VEGA_ID', list())
    genecc = attributes.get('GENCC', list())
    swp = attributes.get('SWP', list())
    mane_select = attributes.get('MANE_SELECT', list())
    local_specific_db_xr = attributes.get('LOCUS_SPECIFIC_DB_XR', list())
    locus_type = attributes.get('LOCUS_TYPE', list())
    agr = attributes.get('AGR', list())
    cytogenetic_location = attributes.get('CYTOGENETIC_LOCATION', list())
    date_created = attributes.get('DATE_CREATED', list())
    ensemblgene_id = attributes.get('ENSEMBLGENE_ID', list())
    db_xr_id = attributes.get('DB_XR_ID', list())
    locus_group = attributes.get('LOCUS_GROUP', list())
    entrezgene_id = attributes.get('ENTREZGENE_ID', list())
    date_name_changed = attributes.get('DATE_NAME_CHANGED', list())
    pmid = attributes.get('PMID', list())
    date_last_modified = attributes.get('DATE_LAST_MODIFIED', list())
    mapped_ucsc_id = attributes.get('MAPPED_UCSC_ID', list())
    refseq_id = attributes.get('REFSEQ_ID', list())
    ena = attributes.get('ENA', list())
    rgd_id = attributes.get('RGD_ID', list())
    date_symbol_changed = attributes.get('DATE_SYMBOL_CHANGED', list())
    omim_id = attributes.get('OMIM_ID', list())
    gene_fam_id = attributes.get('GENE_FAM_ID', list())
    gene_symbol = attributes.get('GENESYMBOL', list())
    ez = attributes.get('EZ', list())
    ccds_id = attributes.get('CCDS_ID', list())
    lncipedia = attributes.get('LNCIPEDIA', list())
    gene_fam_desc = attributes.get('GENE_FAM_DESC', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


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
    for item in iri_mappings_raw:
        for prefix in item:
            IRI_MAPPINGS[prefix] = item[prefix]

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
                process_atc_item(node_id, value, nodes_output, edges_output)

            if source == 'CHV':
                process_chv_item(node_id, value, nodes_output, edges_output)

            if source == 'DRUGBANK':
                process_drugbank_item(node_id, value, nodes_output, edges_output)

            if source == 'FMA':
                process_fma_item(node_id, value, nodes_output, edges_output)

            if source == 'GO':
                process_go_item(node_id, value, nodes_output, edges_output)

            if source == 'HCPCS':
                process_hcpcs_item(node_id, value, nodes_output, edges_output)

            if source == 'HGNC':
                process_hgnc_item(node_id, value, nodes_output, edges_output)

    kg2_util.end_read_jsonlines(input_read_jsonlines_info)
    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)
    # print(json.dumps(attribute_keys, indent=4, sort_keys=True, default=list))
    print("Finishing umls_list_jsonl_to_kg_jsonl.py at", kg2_util.date())
