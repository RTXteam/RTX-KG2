#!/usr/bin/env python3
'''semmeddb_tuple_list_json_to_kg_json.py: extracts all the predicate triples from SemMedDB, in the RTX KG2 JSON format

   Usage: semmeddb_tuple_list_json_to_kg_json.py [--mrcuiFile <MRCUI.RRF_file>] <inputFile.json> <outputFile.json>
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


def make_rel(preds_dict: dict,
             subject_curie: str,
             object_curie: str,
             predicate: str,
             pmid: str,
             pub_date: str,
             sentence: str,
             subject_score: str,
             object_score: str,
             negated: bool):
    key = subject_curie + '-' + predicate + '-' + object_curie
    key_val = preds_dict.get(key, None)
    publication_curie = kg2_util.CURIE_PREFIX_PMID + ':' + pmid
    publication_info_dict = {
        'publication date': pub_date,
        'sentence': sentence,
        'subject score': subject_score,
        'object score': object_score}
    if key_val is None:
        relation_type = predicate.lower()
        if relation_type != 'xref':
            relation_curie = SEMMEDDB_CURIE_PREFIX + ':' + relation_type
        else:
            relation_curie = 'OBO:xref'
        edge_dict = kg2_util.make_edge(subject_curie,
                                       object_curie,
                                       relation_curie,
                                       relation_type,
                                       SEMMEDDB_CURIE_PREFIX + ':',
                                       curr_timestamp)
        edge_dict['publications'] = [publication_curie]
        edge_dict['publications_info'] = {publication_curie: publication_info_dict}
        edge_dict['negated'] = negated
        preds_dict[key] = edge_dict
    else:
        key_val['publications_info'][publication_curie] = publication_info_dict
        key_val['publications'] = key_val['publications'] + [publication_curie]


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='semmeddb_mysql_to_json.py: extracts all the predicate triples from SemMedDB, in the RTX KG2 JSON format')
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('--mrcuiFile', dest='mrcui_file_name', type=str, default=None)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
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


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    mrcui_file_name = args.mrcui_file_name  # '/home/ubuntu/kg2-build/umls/META/MRCUI.RRF'
    input_file_name = args.inputFile
    output_file_name = args.outputFile
    test_mode = args.test
    input_data = json.load(open(input_file_name, 'r'))
    edges_dict = dict()
    nodes_dict = dict()

    if mrcui_file_name is not None:
        remapped_cuis = get_remapped_cuis(mrcui_file_name)
    else:
        remapped_cuis = dict()

    row_ctr = 0

    update_date_dt = datetime.datetime.fromisoformat('2018-01-01 00:00:00')  # picking an arbitrary time in the past

    for (pmid, subject_cui_str, predicate, object_cui_str, pub_date, sentence,
         subject_score, object_score, curr_timestamp) in input_data['rows']:
        row_ctr += 1
        curr_timestamp_dt = datetime.datetime.fromisoformat(curr_timestamp)
        if curr_timestamp_dt > update_date_dt:
            update_date_dt = curr_timestamp_dt
        if row_ctr % 100000 == 0:
            print("Have processed " + str(row_ctr) + " rows out of " + str(len(input_data['rows'])) + " rows")
        if test_mode and row_ctr > 10000:
            break
        if NEG_REGEX.match(predicate):
            negated = True
            predicate = NEG_REGEX.sub('', predicate, 1)
        else:
            negated = False

        # Create the new edge(s) based on this SemMedDB row
        for rel_to_make in get_rels_to_make_for_row(subject_cui_str, object_cui_str, predicate, remapped_cuis):
            subject_curie = rel_to_make[0]
            object_curie = rel_to_make[1]
            edge_label = rel_to_make[2]
            # Exclude self-edges for certain types of predicates
            if subject_curie != object_curie or edge_label.lower() not in EDGE_LABELS_EXCLUDE_FOR_LOOPS:
                make_rel(edges_dict, subject_curie, object_curie, edge_label, pmid, pub_date, sentence,
                         subject_score, object_score, negated)

        if predicate not in nodes_dict:
            relation_iri = kg2_util.convert_snake_case_to_camel_case(predicate.lower().replace(' ', '_'))
            relation_iri = SEMMEDDB_IRI + '#' + relation_iri
            nodes_dict[predicate] = kg2_util.make_node(id=SEMMEDDB_CURIE_PREFIX + ':' + predicate.lower(),
                                                       iri=relation_iri,
                                                       name=predicate.lower(),
                                                       category_label=kg2_util.BIOLINK_CATEGORY_RELATIONSHIP_TYPE,
                                                       update_date=curr_timestamp,
                                                       provided_by=SEMMEDDB_CURIE_PREFIX + ':')
    semmeddb_kb_curie_id = SEMMEDDB_CURIE_PREFIX + ':'
    nodes_dict[semmeddb_kb_curie_id] = kg2_util.make_node(
        id=semmeddb_kb_curie_id,
        iri=SEMMEDDB_IRI,
        name='Semantic Medline Database (SemMedDB)',
        category_label=kg2_util.BIOLINK_CATEGORY_DATA_FILE,
        update_date=update_date_dt.strftime('%Y-%m-%d %H:%M:%S'),
        provided_by=semmeddb_kb_curie_id)

    out_graph = {'edges': [rel_dict for rel_dict in edges_dict.values()],
                 'nodes': [node_dict for node_dict in nodes_dict.values()]}

    for rel_dict in out_graph['edges']:
        if len(rel_dict['publications']) > 1:
            rel_dict['publications'] = list(set(rel_dict['publications']))

    kg2_util.save_json(out_graph, output_file_name, test_mode)
