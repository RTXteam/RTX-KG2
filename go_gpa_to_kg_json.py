#!/usr/bin/env python3

''' Converts a Gene Ontology GPA file for humans to the KG2 JSON edges

    Usage: go_gpa_to_kg_json.py  <inputFile.json> <outputFile.json>
'''

import csv
import datetime
import kg2_util
import argparse

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


GO_BASE_IRI = kg2_util.BASE_URL_GO
GO_PROVIDED_BY_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY \
                                + ":go"
CURIE_PREFIX_GO = kg2_util.CURIE_PREFIX_GO


def get_args():
    arg_parser = argparse.ArgumentParser(description='go_gpa_to_kg_json.py: \
                                         converts a Gene Ontology GPA file \
                                         for humans into KG2 JSON edges')
    arg_parser.add_argument('--test',
                            dest='test',
                            action="store_true",
                            default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    print("Starting at", date())
    args = get_args()
    gaf_file = open(args.inputFile)
    file_arr = csv.reader(gaf_file, delimiter="\t")
    edges = []
    databases = {}

    for line in file_arr:
        if line[0].startswith("!") is False:
            predicate_label = line[2]
            subject_curie = kg2_util.CURIE_PREFIX_UNIPROT + ":" + line[1]
            object_curie = line[3]
            publications = [line[4]]
            eco_code = line[5]
            source = line[6].split("|")
            update_date = line[8]
            evidence = line[10]
            negated = False
            if "NOT|" in predicate_label:
                negated = True
                predicate_label = predicate_label.replace("NOT|", "")

            relation = GO_BASE_IRI + predicate_label
            relation_curie = CURIE_PREFIX_GO + ":" + predicate_label

            edge = kg2_util.make_edge(subject_curie,
                                      object_curie,
                                      relation,
                                      relation_curie,
                                      predicate_label,
                                      GO_PROVIDED_BY_CURIE_ID,
                                      update_date)
            edge["negated"] = negated
            edge["publications"] = publications
            edges.append(edge)

    kg2_util.save_json({"nodes": [], "edges": edges},
                       args.outputFile,
                       args.test)

    print("Ending at", date())
