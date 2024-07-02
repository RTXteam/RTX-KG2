#!/usr/bin/env python3
'''semmeddb_tuple_list_json_to_kg_json.py: extracts all the predicate triples from SemMedDB, in the RTX KG2 JSON format

   Usage: semmeddb_tuple_list_json_to_kg_json.py [--mrcuiFile <MRCUI.RRF_file>] <inputFile.json> <outputNodesFile.json> <outputEdgesFile.json>
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
import datetime
import json
import kg2_util
import re
import sys

SEMMEDDB_CURIE_PREFIX = kg2_util.CURIE_PREFIX_SEMMEDDB
SEMMEDDB_IRI = kg2_util.BASE_URL_SEMMEDDB

NEG_REGEX = re.compile('^NEG_', re.M)
EDGE_LABELS_EXCLUDE_FOR_LOOPS = {'same_as', 'higher_than', 'lower_than', 'different_from', 'compared_with'}
CUI_PREFIX = kg2_util.CURIE_PREFIX_UMLS
NCBIGENE_PREFIX = kg2_util.CURIE_PREFIX_NCBI_GENE
XREF_EDGE_LABEL = 'xref'

EXCLUDE_EMPTY_STR = "n/a"
SEMANTIC_TYPE_EXCLUSION = "semantic type exclusion"
DOMAIN_EXCLUSION = "Domain exclusion"
RANGE_EXCLUSION = "Range exclusion"

def get_remapped_cuis(retired_cui_file_name: str) -> dict:
    """
    Creates a dictionary of retired CUIs and the current CUIs they map to in UMLS; currently only includes remappings
    labeled as a 'synonym' (vs. 'broader', 'narrower', or 'other related').
    """
    remapped_cuis = dict()
    with open(retired_cui_file_name, 'r') as retired_cui_file:
        # Line format in MRCUI file: retired_cui|release|map_type|||remapped_cui|is_current|
        for line in retired_cui_file:
            row = line.split('|')
            map_type = row[2]
            is_current = row[6]
            old_cui = row[0]
            new_cui = row[5]
            # Only include the remapping if it's a 'synonym' (and is current)
            if map_type == 'SY' and is_current == 'Y' and new_cui != '':
                remapped_cuis[old_cui] = new_cui
    return remapped_cuis


def date(print_str: str):
    return print(print_str, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def make_rel(edges_output,
             subject_curie: str,
             object_curie: str,
             predicate: str,
             publications_info: str,
             negated: bool,
             domain_range_exclusion: bool):
    key = subject_curie + '-' + predicate + '-' + object_curie
    publications_info_list = publications_info.split('\t')
    edge_publications_info = dict()
    edges_publications = list()
    for publication in publications_info_list:
        publication_traits = publication.split('|')
        # Make this an assertion later, but this isn't helpful for testing
        if len(publication_traits) != 5:
            print("Issue with ", key, "; Need to Lengthen Max Group Concat")
            continue
        (pmid, sentence, subject_score, object_score, pub_date) = publication_traits
        publication_curie = kg2_util.CURIE_PREFIX_PMID + ':' + pmid
        publication_info_dict = {
            'publication date': pub_date,
            'sentence': sentence,
            'subject score': subject_score,
            'object score': object_score}
        edge_publications_info[publication_curie] = publication_info_dict
        edges_publications.append(publication_curie)

    relation_type = predicate.lower()
    relation_curie = SEMMEDDB_CURIE_PREFIX + ':' + relation_type
    edge_dict = kg2_util.make_edge(subject_curie,
                                   object_curie,
                                   relation_curie,
                                   relation_type,
                                   SEMMEDDB_CURIE_PREFIX + ':',
                                   curr_timestamp)
    edge_dict['publications'] = sorted(list(set(edges_publications)))
    edge_dict['publications_info'] = edge_publications_info
    edge_dict['negated'] = negated
    edge_dict['domain_range_exclusion'] = domain_range_exclusion
    
    edges_output.write(edge_dict)


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='semmeddb_mysql_to_json.py: extracts all the predicate triples from SemMedDB, in the RTX KG2 JSON format')
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('--mrcuiFile', dest='mrcui_file_name', type=str, default='/home/ubuntu/kg2-build/umls/META/MRCUI.RRF')
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('semmedExcludeList', type=str)
    arg_parser.add_argument('versionFile', type=str)
    arg_parser.add_argument('outputNodesFile', type=str)
    arg_parser.add_argument('outputEdgesFile', type=str)
    return arg_parser


def get_cui_if_exists(field_ids: list, remapped_cuis: dict):
    """
    Given a list of IDs present in a SemMedDB SUBJECT_CUI or OBJECT_CUI field, this function returns the CUI, if one
    exists (sometimes only NCBIGene IDs are present).
    """
    first_id = field_ids[0]
    if first_id.upper().startswith('C'):
        cui = remapped_cuis.get(first_id, first_id)  # Use remapped CUI if one exists
        return cui
    else:
        return None


def get_xref_rels(cui: str, ncbigene_ids: list):
    """
    This function creates 'xref' relationships between the input CUI and each input NCBIGene ID; it outputs a list of
    subject-object-predicate tuples representing each such 'xref' edge.
    """
    xref_rels = []
    for gene_id in ncbigene_ids:
        xref_rels.append([CUI_PREFIX + ':' + cui, NCBIGENE_PREFIX + ':' + gene_id, XREF_EDGE_LABEL])
    return xref_rels


def get_rels_to_make_for_row(subject_str: str, object_str: str, predicate: str, remapped_cuis: dict):
    """
    Because SemMedDB subject and object strings can contain multiple IDs (namely, an optional CUI followed by 0 or
    more NCBIGene IDs), this function determines what edges will need to be created from a given SemMedDB row and
    outputs a list of tuples containing the subject, object, and predicate for each such edge.
    (Examples of subject/object CUI strings from SemMedDB: 'C0796614', 'C0796614|931', '6520', '3429|5715|10534'.)
    """
    subject_split = subject_str.split("|")
    object_split = object_str.split("|")
    subject_cui = get_cui_if_exists(subject_split, remapped_cuis)
    object_cui = get_cui_if_exists(object_split, remapped_cuis)
    num_subject_ids = len(subject_split)
    num_object_ids = len(object_split)

    rels_to_make = []
    if subject_cui and object_cui:
        # Connect the two CUIs
        rels_to_make.append((CUI_PREFIX + ':' + subject_cui, CUI_PREFIX + ':' + object_cui, predicate))
        # Create xrefs within each side as needed (from the CUI to any NCBIGenes on the same side)
        if num_subject_ids > 1:
            rels_to_make += get_xref_rels(subject_cui, subject_split[1:])
        if num_object_ids > 1:
            rels_to_make += get_xref_rels(object_cui, object_split[1:])
    elif subject_cui:
        # Connect the subject CUI to each NCBIGene on the object side
        for gene_id in object_split:
            rels_to_make.append((CUI_PREFIX + ':' + subject_cui, NCBIGENE_PREFIX + ':' + gene_id, predicate))
        # Create xrefs within subject side as needed (from CUI to NCBIGenes)
        if num_subject_ids > 1:
            rels_to_make += get_xref_rels(subject_cui, subject_split[1:])
    elif object_cui:
        # Connect each NCBIGene in the subject to the object CUI
        for gene_id in subject_split:
            rels_to_make.append((NCBIGENE_PREFIX + ':' + gene_id, CUI_PREFIX + ':' + object_cui, predicate))
        # Create xrefs within object side as needed (from CUI to NCBIGenes)
        if num_object_ids > 1:
            rels_to_make += get_xref_rels(object_cui, object_split[1:])
    elif num_subject_ids == 1:
        # Connect the subject NCBIGene to each NCBIGene on the object side
        for object_gene_id in object_split:
            rels_to_make.append((NCBIGENE_PREFIX + ':' + subject_split[0], NCBIGENE_PREFIX + ':' + object_gene_id, predicate))
    elif num_object_ids == 1:
        # Connect each NCBIGene on the subject side to the object NCBIGene
        for subject_gene_id in subject_split:
            rels_to_make.append((NCBIGENE_PREFIX + ':' + subject_gene_id, NCBIGENE_PREFIX + ':' + object_split[0], predicate))
    else:
        print('WARNING: Skipping SemMedDB row because BOTH subject and object have multiple NCBIGene IDs and no CUI.',
              file=sys.stderr)

    return rels_to_make


def create_semmed_exclude_list(semmed_exclude_list_name):
    semmed_list = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(semmed_exclude_list_name))
    exclusions = dict()

    # Exclusion types
    exclusions[SEMANTIC_TYPE_EXCLUSION] = set()
    exclusions[DOMAIN_EXCLUSION] = dict()
    exclusions[RANGE_EXCLUSION] = dict()

    for exclude_item in semmed_list['excluded_semmedb_records']:
        exclusion_type = exclude_item['exclusion_type']
        assert exclusion_type in exclusions, exclusion_type

        sub_code = exclude_item['semmed_subject_code']
        obj_code = exclude_item['semmed_object_code']
        pred = exclude_item['semmed_predicate']

        if exclusion_type == SEMANTIC_TYPE_EXCLUSION:
            if sub_code != EXCLUDE_EMPTY_STR:
                exclusions[SEMANTIC_TYPE_EXCLUSION].add(sub_code)
            if obj_code != EXCLUDE_EMPTY_STR:
                exclusions[SEMANTIC_TYPE_EXCLUSION].add(obj_code)

        if exclusion_type == DOMAIN_EXCLUSION:
            if pred not in exclusions[DOMAIN_EXCLUSION]:
                exclusions[DOMAIN_EXCLUSION][pred] = set()
            exclusions[DOMAIN_EXCLUSION][pred].add(sub_code)

        if exclusion_type == RANGE_EXCLUSION:
            if pred not in exclusions[RANGE_EXCLUSION]:
                exclusions[RANGE_EXCLUSION][pred] = set()
            exclusions[RANGE_EXCLUSION][pred].add(obj_code)

    return exclusions


if __name__ == '__main__':
    date("Starting semmeddb_tuple_list_json_to_kg_json.py")
    args = make_arg_parser().parse_args()
    mrcui_file_name = args.mrcui_file_name  # '/home/ubuntu/kg2-build/umls/META/MRCUI.RRF'
    semmed_exclude_list_name = args.semmedExcludeList
    exclusions = create_semmed_exclude_list(semmed_exclude_list_name)
    input_file_name = args.inputFile
    version_file = args.versionFile
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile
    test_mode = args.test

    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    nodes_set = set()

    if mrcui_file_name is not None:
        remapped_cuis = get_remapped_cuis(mrcui_file_name)
    else:
        remapped_cuis = dict()

    row_ctr = 0

    with open(version_file, 'r') as versioning:
        line_count = 0
        for line in versioning:
            line_count += 1
            if line_count == 1:
                version_number = line.replace('Version: VER', '')
            if line_count == 2:
                version_date = line.replace('Year: ', '')

    update_date_dt = datetime.datetime.fromisoformat('2018-01-01 00:00:00')  # picking an arbitrary time in the past

    input_read_jsonlines_info = kg2_util.start_read_jsonlines(input_file_name, list)
    input_data = input_read_jsonlines_info[0]

    for (subject_cui_str, predicate, object_cui_str, subject_semtype, object_semtype,
         curr_timestamp, publications_info) in input_data:
        row_ctr += 1
        try:
            curr_timestamp_dt = datetime.datetime.fromisoformat(curr_timestamp.split(',')[-1])
            if curr_timestamp_dt > update_date_dt:
                update_date_dt = curr_timestamp_dt
        except ValueError:
            pass
        if row_ctr % 100000 == 0:
            print("Have processed " + str(row_ctr) + " rows")
        if test_mode and row_ctr > 10000:
            break
        if NEG_REGEX.match(predicate):
            negated = True
            predicate = NEG_REGEX.sub('', predicate, 1)
        else:
            negated = False

        # Handle domain_range_exclusion (#281)
        domain_range_exclusion = False
        if subject_semtype in exclusions[SEMANTIC_TYPE_EXCLUSION] \
           or object_semtype in exclusions[SEMANTIC_TYPE_EXCLUSION] \
           or subject_semtype in exclusions[DOMAIN_EXCLUSION].get(predicate, set()) \
           or object_semtype in exclusions[RANGE_EXCLUSION].get(predicate, set()):
            domain_range_exclusion = True

        # Create the new edge(s) based on this SemMedDB row
        for rel_to_make in get_rels_to_make_for_row(subject_cui_str, object_cui_str, predicate, remapped_cuis):
            subject_curie = rel_to_make[0]
            object_curie = rel_to_make[1]
            relation_label = rel_to_make[2]
            # Exclude self-edges for certain types of predicates
            if subject_curie != object_curie or relation_label.lower() not in EDGE_LABELS_EXCLUDE_FOR_LOOPS:
                make_rel(edges_output, subject_curie, object_curie, relation_label, publications_info, negated, domain_range_exclusion)

        if predicate not in nodes_set:
            relation_iri = kg2_util.convert_snake_case_to_camel_case(predicate.lower().replace(' ', '_'))
            relation_iri = SEMMEDDB_IRI + '#' + relation_iri
            nodes_set.add(predicate)
            nodes_output.write(kg2_util.make_node(id=SEMMEDDB_CURIE_PREFIX + ':' + predicate.lower(),
                                                  iri=relation_iri,
                                                  name=predicate.lower(),
                                                  category_label=kg2_util.BIOLINK_CATEGORY_NAMED_THING,
                                                  update_date=curr_timestamp,
                                                  provided_by=SEMMEDDB_CURIE_PREFIX + ':'))

    kg2_util.end_read_jsonlines(input_read_jsonlines_info)

    semmeddb_kb_curie_id = SEMMEDDB_CURIE_PREFIX + ':'
    nodes_output.write(kg2_util.make_node(id=semmeddb_kb_curie_id,
                                          iri=SEMMEDDB_IRI,
                                          name='Semantic Medline Database (SemMedDB) v' + version_number,
                                          category_label=kg2_util.SOURCE_NODE_CATEGORY,
                                          update_date=update_date_dt.strftime('%Y-%m-%d %H:%M:%S'),
                                          provided_by=semmeddb_kb_curie_id))

    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)

    date("Finishing semmeddb_tuple_list_json_to_kg_json.py")
