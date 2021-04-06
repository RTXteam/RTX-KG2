#!/usr/bin/env python3
''' intact_tsv_to_kg_json.py: Converts the IntAct TSV
    file into a KG JSON file

    Usage: intact_tsv_to_kg_json.py [--test] <inputFile.txt>
    <outputFile.json>
'''


import json
import argparse
import kg2_util
import datetime


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


HUMAN_TAXON = "taxid:9606(human)|taxid:9606(Homo sapiens)"

BASE_URL_INTACT = kg2_util.BASE_BASE_URL_IDENTIFIERS_ORG + 'intact:'
INTACT_KB_URI = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + 'intact'
INTACT_KB_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY + \
                        ':' + 'intact'

EDGE_LIMIT_TEST_MODE = 10000


def get_args():
    description = "intact_tsv_to_kg_json.py: converts the IntAct \
                   TSV dump into a KG JSON file"
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    return arg_parser.parse_args()


def format_date(date: str):
    date = date.split('/')
    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    return str(datetime.date(year, month, day))


def format_pmid(publication: str):
    return publication.replace('pubmed', kg2_util.CURIE_PREFIX_PMID)


def format_rel_label(label: str):
    return label.split('"')[2].strip('(').strip(')').replace(' ', '_')


def make_edge(intact_row):
    if row.startswith('#'):
        return None
    data = row.split('\t')
    # last data element is 'Identification method participant B'
    [subject_id,  # ID(s) interactor A
     object_id,  # ID(s) interactor B,
     _,  # Alt. ID(s) interactor A,
     _,  # Alt. ID(s) interactor B,
     subject_name,  # Alias(es) interactor A,
     object_name,  # Alias(es) interactor B,
     _,  # Interaction detection method(s),
     _,  # Publication 1st author(s),
     publications,  # Publication Identifier(s),
     subject_taxon,  # Taxid interactor A,
     object_taxon,  # Taxid interactor B,
     predicate,  # Interaction type(s),
     _,  # Source database(s),
     _,  # Interaction identifier(s),
     confidence,  # Confidence value(s),
     _,  # Expansion method(s),
     _,  # Biological role(s) interactor A,
     _,  # Biological role(s) interactor B,
     _,  # Experimental role(s) interactor A,
     _,  # Experimental role(s) interactor B,
     _,  # Type(s) interactor A,
     _,  # Type(s) interactor B,
     _,  # Xref(s) interactor A,
     _,  # Xref(s) interactor B,
     _,  # Interaction Xref(s),
     _,  # Annotation(s) interactor A,
     _,  # Annotation(s) interactor B,
     _,  # Interaction annotation(s),
     taxon,  # Host organism(s),
     _,  # Interaction parameter(s),
     created_date,  # Creation date,
     update_date,  # Update date,
     _,  # Checksum(s) interactor A,
     _,  # Checksum(s) interactor B,
     _,  # Interaction Checksum(s),
     _,  # Negative,
     _,  # Feature(s) interactor A,
     _,  # Feature(s) interactor B,
     _,  # Stoichiometry(s) interactor A,
     _,  # Stoichiometry(s) interactor B,
     _,  # Identification method participant A
     _] = data
    if subject_taxon == HUMAN_TAXON and object_taxon == HUMAN_TAXON:
        publications = [format_pmid(publication)
                        for publication in publications.split('|')
                        if publication.startswith('pubmed')]
        confidence = [score.replace('intact-miscore:', '')
                      for score in confidence.split('|')
                      if confidence.startswith('intact-miscore:')]
        if len(confidence) < 1:
            confidence = None
        else:
            confidence = confidence[0]
        relation_label = format_rel_label(predicate)
        relation = predicate.split('"')[1]
        subject_id = subject_id.replace('uniprotkb',
                                        kg2_util.CURIE_PREFIX_UNIPROT)
        object_id = object_id.replace('uniprotkb',
                                      kg2_util.CURIE_PREFIX_UNIPROT)
        created_date = format_date(created_date)
        update_date = format_date(update_date)
        edge = kg2_util.make_edge(subject_id,
                                  object_id,
                                  relation,
                                  relation_label,
                                  INTACT_KB_CURIE_ID,
                                  update_date)
        edge['publications'] = publications
        return edge
    return None


if __name__ == '__main__':
    args = get_args()
    with open(args.inputFile, 'r') as intact:
        edges = []
        nodes = []
        edge_count = 0
        for row in intact:
            edge = make_edge(row)
            if edge is not None and (args.test is False or
                                     edge_count < EDGE_LIMIT_TEST_MODE):
                edges.append(edge)
                edge_count += 1
        kp_node = kg2_util.make_node(INTACT_KB_CURIE_ID,
                                     INTACT_KB_URI,
                                     "IntAct",
                                     kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                     None,
                                     INTACT_KB_CURIE_ID)
        nodes.append(kp_node)
        graph = {'edges': edges, 'nodes': nodes}
        kg2_util.save_json(graph, args.outputFile, args.test)
