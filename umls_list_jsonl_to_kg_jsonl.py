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
HL7_PREFIX = kg2_util.CURIE_PREFIX_UMLS
HPO_PREFIX = kg2_util.CURIE_PREFIX_HP
ICD10PCS_PREFIX = kg2_util.CURIE_PREFIX_ICD10PCS
ICD9CM_PREFIX = kg2_util.CURIE_PREFIX_ICD9
MEDRT_PREFIX = kg2_util.CURIE_PREFIX_UMLS
MEDLINEPLUS_PREFIX = kg2_util.CURIE_PREFIX_UMLS
MSH_PREFIX = kg2_util.CURIE_PREFIX_MESH
MTH_PREFIX = kg2_util.CURIE_PREFIX_UMLS
NCBI_PREFIX = kg2_util.CURIE_PREFIX_NCBI_TAXON

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
    cuis = info.get(CUIS_KEY, list())
    tuis = info.get(TUIS_KEY, list())
    if curie_prefix == kg2_util.CURIE_PREFIX_UMLS:
        if len(cuis) != 1:
            return None, None, None, None, None, None, None, None
        node_id = cuis[0]
    node_curie = make_node_id(curie_prefix, node_id)
    iri = IRI_MAPPINGS[curie_prefix] + node_id
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
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(FMA_PREFIX, node_id, info, ['PT', 'SY', 'AB', 'OP', 'IS'])

    # Currently not used, but extracting them in case we want them in the future
    authority = info.get(INFO_KEY, dict()).get('AUTHORITY', list())
    date_last_modified = info.get(INFO_KEY, dict()).get('DATE_LAST_MODIFIED', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_go_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['PT', 'MTH_PT', 'ET', 'MTH_ET', 'SY', 'MTH_SY', 'OP', 'MTH_OP', 'OET', 'MTH_OET', 'IS', 'MTH_IS']
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
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(HCPCS_PREFIX, node_id, info, ['PT', 'MP', 'MTH_HT'])

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
    accession_heirarchy = ['PT', 'ACR', 'MTH_ACR', 'NA', 'SYN', 'NP', 'NS']
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


def process_hl7_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['CSY', 'PT', 'CDO', 'VS', 'BR', 'CPR', 'CR', 'NPT'] # https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(HL7_PREFIX, node_id, info, accession_heirarchy)
    if node_curie == None:
        return
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, 'HL7')

    # Currently not used, but extracting them in case we want them in the future - descriptions from https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/attribute_names.html
    attributes = info.get(INFO_KEY, dict())
    hl7at = attributes.get('HL7AT', list())
    hl7ii = attributes.get('HL7II', list())
    hl7im = attributes.get('HL7IM', list())
    hl7lt = attributes.get('HL7LT', list())
    hl7un = attributes.get('HL7UN', list())
    hl7oa = attributes.get('HL7OA', list())
    hl7scs = attributes.get('HL7SCS', list())
    hl7cc = attributes.get('HL7CC', list())
    hl7na = attributes.get('HL7NA', list())
    hl7in = attributes.get('HL7IN', list())
    hl7ap = attributes.get('HL7AP', list())
    hl7mi = attributes.get('HL7MI', list())
    hl7hi = attributes.get('HL7HI', list())
    hl7ir = attributes.get('HL7IR', list())
    hl7ai = attributes.get('HL7AI', list())
    hl7ha = attributes.get('HL7HA', list())
    hl7rf = attributes.get('HL7RF', list())
    hl7rd = attributes.get('HL7RD', list())
    hl7vd = attributes.get('HL7VD', list())
    hl7dc = attributes.get('HL7DC', list())
    hl7rk = attributes.get('HL7RK', list())
    hl7is = attributes.get('HL7IS', list())
    hl7sy = attributes.get('HL7SY', list())
    hl7cd = attributes.get('HL7CD', list())
    hl7sl = attributes.get('HL7SL', list())
    hl7pl = attributes.get('HL7PL', list())
    hl7vc = attributes.get('HL7VC', list())
    hl7ty = attributes.get('HL7TY', list())
    hl7rg = attributes.get('HL7RG', list())
    hl7csc = attributes.get('HL7CSC', list())
    hl7od = attributes.get('HL7OD', list())
    hl7id = attributes.get('HL7ID', list())
    hl7tr = attributes.get('HL7TR', list())
    hl7di = attributes.get('HL7DI', list())
    hl7cs = attributes.get('HL7CS', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_hpo_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['PT', 'SY', 'ET', 'OP', 'IS', 'OET'] # https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(HPO_PREFIX, node_id.replace('HP:', ''), info, accession_heirarchy)

    # Currently not used, but extracting them in case we want them in the future
    attributes = info.get(INFO_KEY, dict())
    sid = attributes.get('SID', list())
    hpo_comment = attributes.get('HPO_COMMENT', list())
    date_created = attributes.get('DATE_CREATED', list())
    syn_qualifier = attributes.get('SYN_QUALIFIER', list())
    ref = attributes.get('REF', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_icd10pcs_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['PT', 'PX', 'HX', 'MTH_HX', 'HT', 'HS', 'AB'] # https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(ICD10PCS_PREFIX, node_id, info, accession_heirarchy)

    # Currently not used, but extracting them in case we want them in the future
    attributes = info.get(INFO_KEY, dict())
    added_meaning = attributes.get('ADDED_MEANING', list())
    order_no = attributes.get('ORDER_NO', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_icd9cm_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['PT', 'HT', 'AB'] # https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(ICD9CM_PREFIX, node_id, info, accession_heirarchy)
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, 'ICD9CM')

    # Currently not used, but extracting them in case we want them in the future
    attributes = info.get(INFO_KEY, dict())
    icc = attributes.get('ICC', list())
    ice = attributes.get('ICE', list())
    icf = attributes.get('ICF', list())
    sos = attributes.get('SOS', list())
    icn = attributes.get('ICN', list())
    ica = attributes.get('ICA', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)

def process_medrt_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['PT', 'FN', 'SY'] # https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(MEDRT_PREFIX, node_id, info, accession_heirarchy)
    if node_curie == None:
        return
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, 'MED-RT')

    # Currently not used, but extracting them in case we want them in the future
    attributes = info.get(INFO_KEY, dict())
    term_status = attributes.get('TERM_STATUS', list())
    concept_type = attributes.get('CONCEPT_TYPE', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_medlineplus_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['PT', 'ET', 'SY', 'HT'] # https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(MEDLINEPLUS_PREFIX, node_id, info, accession_heirarchy)
    if node_curie == None:
        return
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, 'MEDLINEPLUS')

    # Currently not used, but extracting them in case we want them in the future
    attributes = info.get(INFO_KEY, dict())
    sos = attributes.get('SOS', list())
    date_created = attributes.get('DATE_CREATED', list())
    mp_group_url = attributes.get('MP_GROUP_URL', list())
    mp_primary_institute_url = attributes.get('MP_PRIMARY_INSTITUTE_URL', list())
    mp_other_language_url = attributes.get('MP_OTHER_LANGUAGE_URL', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_msh_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['MH', 'TQ', 'PEP', 'ET', 'XQ', 'PXQ', 'NM', 'N1', 'PCE', 'CE', 'HT', 'HS', 'DEV', 'DSV', 'QAB', 'QEV', 'QSV', 'PM'] # https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(MSH_PREFIX, node_id, info, accession_heirarchy)
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, 'MSH')

    # Currently not used, but extracting them in case we want them in the future
    attributes = info.get(INFO_KEY, dict())
    mmr = attributes.get('MMR', list())
    fx = attributes.get('FX', list())
    lt = attributes.get('LT', list())
    dc = attributes.get('DC', list())
    pa = attributes.get('PA', list())
    rr = attributes.get('RR', list())
    hm = attributes.get('HM', list())
    pi = attributes.get('PI', list())
    ec = attributes.get('EC', list())
    hn = attributes.get('HN', list())
    termui = attributes.get('TERMUI', list())
    th = attributes.get('TH', list())
    sos = attributes.get('SOS', list())
    ii = attributes.get('II', list())
    rn = attributes.get('RN', list())
    an = attributes.get('AN', list())
    cx = attributes.get('CX', list())
    dq = attributes.get('DQ', list())
    dx = attributes.get('DX', list())
    pm = attributes.get('PM', list())
    aql = attributes.get('AQL', list())
    sc = attributes.get('SC', list())
    fr = attributes.get('FR', list())
    mda = attributes.get('MDA', list())
    src = attributes.get('SRC', list())
    ol = attributes.get('OL', list())
    mn = attributes.get('MN', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_mth_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['PN', 'CV', 'XM', 'PT', 'SY', 'RT', 'DT'] # https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(MTH_PREFIX, node_id, info, accession_heirarchy)
    if node_curie == None:
        return
    provided_by = make_node_id(UMLS_SOURCE_PREFIX, 'MTH')

    # Currently not used, but extracting them in case we want them in the future
    attributes = info.get(INFO_KEY, dict())
    mth_mapsetcomplexity = attributes.get('MTH_MAPSETCOMPLEXITY', list())
    fromvsab = attributes.get('FROMVSAB', list())
    mapsetrsab = attributes.get('MAPSETRSAB', list())
    mapsetversion = attributes.get('MAPSETVERSION', list())
    mapsetvsab = attributes.get('MAPSETVSAB', list())
    tovsab = attributes.get('TOVSAB', list())
    mth_mapfromexhaustive = attributes.get('MTH_MAPFROMEXHAUSTIVE', list())
    torsab = attributes.get('TORSAB', list())
    mapsetsid = attributes.get('MAPSETSID', list())
    mapsetgrammar = attributes.get('MAPSETGRAMMAR', list())
    mapsettype = attributes.get('MAPSETTYPE', list())
    mth_maptoexhaustive = attributes.get('MTH_MAPTOEXHAUSTIVE', list())
    fromrsab = attributes.get('FROMRSAB', list())
    mth_mapfromcomplexity = attributes.get('MTH_MAPFROMCOMPLEXITY', list())
    lt = attributes.get('LT', list())
    mth_maptocomplexity = attributes.get('MTH_MAPTOCOMPLEXITY', list())
    sos = attributes.get('SOS', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_ncbi_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['SCN', 'USN', 'USY', 'SY', 'UCN', 'CMN', 'UE', 'EQ'] # https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(NCBI_PREFIX, node_id, info, accession_heirarchy)
    # Currently not used, but extracting them in case we want them in the future
    attributes = info.get(INFO_KEY, dict())
    div = attributes.get('DIV', list())
    authority_name = attributes.get('AUTHORITY_NAME', list())
    rank = attributes.get('RANK', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


def process_nci_item(node_id, info, nodes_output, edges_output):
    accession_heirarchy = ['PT', 'SY', 'CSN', 'DN', 'FBD', 'HD', 'CCN', 'AD', 'CA2', 'CA3', 'BN', 'AB', 'CCS', 'OP'] # https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/precedence_suppressibility.html
    node_curie, iri, name, provided_by, category, synonyms, cuis, tuis = get_basic_info(NCBI_PREFIX, node_id, info, accession_heirarchy)
    # Currently not used, but extracting them in case we want them in the future
    attributes = info.get(INFO_KEY, dict())
    clinvar_variation_id = attributes.get('CLINVAR_VARIATION_ID', list())
    micronutrient = attributes.get('MICRONUTRIENT', list())
    genbank_accession_number = attributes.get('GENBANK_ACCESSION_NUMBER', list())
    fda_table = attributes.get('FDA_TABLE', list())
    usda_id = attributes.get('USDA_ID', list())
    icd_o_3_code = attributes.get('ICD-O-3_CODE', list())
    tolerable_level = attributes.get('TOLERABLE_LEVEL', list())
    ncbi_taxon_id = attributes.get('NCBI_TAXON_ID', list())
    mgi_accession_id = attributes.get('MGI_ACCESSION_ID', list())
    homologous_gene = attributes.get('HOMOLOGOUS_GENE', list())
    pid_id = attributes.get('PID_ID', list())
    swiss_prot = attributes.get('SWISS_PROT', list())
    essential_amino_acid = attributes.get('ESSENTIAL_AMINO_ACID', list())
    publish_value_set = attributes.get('PUBLISH_VALUE_SET', list())
    cas_registry = attributes.get('CAS_REGISTRY', list())
    value_set_pair = attributes.get('VALUE_SET_PAIR', list())
    accepted_therapeutic_use_for = attributes.get('ACCEPTED_THERAPEUTIC_USE_FOR', list())
    hgnc_id = attributes.get('HGNC_ID', list())
    nci_drug_dictionary_id = attributes.get('NCI_DRUG_DICTIONARY_ID', list())
    chebi_id = attributes.get('CHEBI_ID', list())
    cnu = attributes.get('CNU', list())
    mirbase_id = attributes.get('MIRBASE_ID', list())
    macronutrient = attributes.get('MACRONUTRIENT', list())
    essential_fatty_acid = attributes.get('ESSENTIAL_FATTY_ACID', list())
    unit = attributes.get('UNIT', list())
    pdq_open_trial_search_id = attributes.get('PDQ_OPEN_TRIAL_SEARCH_ID', list())
    term_browser_value_set_description = attributes.get('TERM_BROWSER_VALUE_SET_DESCRIPTION', list())
    entrezgene_id = attributes.get('ENTREZGENE_ID', list())
    infoods = attributes.get('INFOODS', list())
    pubmedid_primary_reference = attributes.get('PUBMEDID_PRIMARY_REFERENCE', list())
    biocarta_id = attributes.get('BIOCARTA_ID', list())
    extensible_list = attributes.get('EXTENSIBLE_LIST', list())
    use_for = attributes.get('USE_FOR', list())
    neoplastic_status = attributes.get('NEOPLASTIC_STATUS', list())
    nsc_number = attributes.get('NSC_NUMBER', list())
    omim_number = attributes.get('OMIM_NUMBER', list())
    lt = attributes.get('LT', list())
    kegg_id = attributes.get('KEGG_ID', list())
    gene_encodes_product = attributes.get('GENE_ENCODES_PRODUCT', list())
    pdq_closed_trial_search_id = attributes.get('PDQ_CLOSED_TRIAL_SEARCH_ID', list())
    design_note = attributes.get('DESIGN_NOTE', list())
    nutrient = attributes.get('NUTRIENT', list())
    fda_unii_code = attributes.get('FDA_UNII_CODE', list())
    us_recommended_intake = attributes.get('US_RECOMMENDED_INTAKE', list())
    chemical_formula = attributes.get('CHEMICAL_FORMULA', list())

    make_umls_node(node_curie, iri, name, category, "2023", provided_by, synonyms, create_description("", tuis), nodes_output)


DESIRED_CODES = {'ATC': process_atc_item,
                 'CHV': process_chv_item,
                 'DRUGBANK': process_drugbank_item,
                 'FMA': process_fma_item,
                 'GO': process_go_item,
                 'HCPCS': process_hcpcs_item,
                 'HGNC': process_hgnc_item,
                 'HL7V3.0': process_hl7_item,
                 'HPO': process_hpo_item,
                 'ICD10PCS': process_icd10pcs_item,
                 'ICD9CM': process_icd9cm_item,
                 'MED-RT': process_medrt_item,
                 'MEDLINEPLUS': process_medlineplus_item,
                 'MSH': process_msh_item,
                 'MTH': process_mth_item,
                 'NCBI': process_ncbi_item,
                 'NCI': process_nci_item}
                 # 'NDDF': process_nddf_item,
                 # 'NDFRT': process_ndfrt_item,
                 # 'OMIM': process_omim_item,
                 # 'PDQ': process_pdq_item,
                 # 'PSY': process_psy_item,
                 # 'RXNORM': process_rxnorm_item,
                 # 'VANDF': process_vandf_item}

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

            if source == 'NDDF':
                name_keys.add(get_name_keys(value.get(NAMES_KEY, dict())))
                attribute_keys.update(get_attribute_keys(value.get(INFO_KEY, dict())))

            if source not in DESIRED_CODES:
                continue

            # Process the data specifically by source
            DESIRED_CODES[source](node_id, value, nodes_output, edges_output)


    kg2_util.end_read_jsonlines(input_read_jsonlines_info)
    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)
    print(json.dumps(name_keys, indent=4, sort_keys=True, default=list))
    print(json.dumps(attribute_keys, indent=4, sort_keys=True, default=list))
    print("Finishing umls_list_jsonl_to_kg_jsonl.py at", kg2_util.date())
