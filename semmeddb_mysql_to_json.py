#!/usr/bin/env python3
'''semmeddb_mysql_to_json.py: extracts all the predicate triples from SemMedDB, in the RTX KG2 JSON format

   Usage: semmeddb_mysql_to_json.py <mysqlConfigFile> <mysqlDBName> <outputFile.json>
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
import gzip
import kg2_util
import json
import pymysql
import shutil
import tempfile

SEMMEDDB_IRI = 'https://skr3.nlm.nih.gov/SemMedDB'


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='semmeddb_mysql_to_json.py: extracts all the predicate triples from SemMedDB, in the RTX KG2 JSON format')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('mysqlConfigFile', type=str, nargs=1)
    arg_parser.add_argument('mysqlDBName', type=str, nargs=1)
    arg_parser.add_argument('outputFile', type=str, nargs=1)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    mysql_config_file = args.mysqlConfigFile[0]
    mysql_db_name = args.mysqlDBName[0]
    test_mode = args.test
    connection = pymysql.connect(read_default_file=mysql_config_file, db='semmeddb')
    preds_dict = dict()
    sql_statement = ("SELECT PMID, SUBJECT_CUI, PREDICATE, OBJECT_CUI, DP, SENTENCE, SUBJECT_SCORE, "
                     "OBJECT_SCORE, CURR_TIMESTAMP FROM ((PREDICATION NATURAL JOIN CITATIONS) "
                     "NATURAL JOIN SENTENCE) NATURAL JOIN PREDICATION_AUX")
    if test_mode:
        sql_statement += " LIMIT 10000"
    with connection.cursor() as cursor:
        cursor.execute(sql_statement)
        results = cursor.fetchall()
        for (pmid, subject_cui, predicate, object_cui, pub_date, sentence,
             subject_score, object_score, curr_timestamp) in results:
            key = subject_cui + '-' + predicate + '-' + object_cui
            key_val = preds_dict.get(key, None)
            publication_curie = 'PMID:' + pmid
            publication_info_dict = {
                'publication date': pub_date,
                'sentence': sentence,
                'subject score': subject_score,
                'object score': object_score}
            if key_val is None:
                relation_type = predicate.replace('_', ' ').lower()
                relation_iri = relation_type.title().replace(' ', '')
                relation_iri = relation_iri[0].lower() + relation_iri[1:]
                relation_iri = SEMMEDDB_IRI + '#' + relation_iri
                key_val = {'subject': 'CUI:' + subject_cui,
                           'object': 'CUI:' + object_cui,
                           'type': relation_type,
                           'relation': relation_iri,
                           'relation curie': 'SEMMEDDB:' + relation_type,
                           'negated': False,
                           'publications': [publication_curie],
                           'publications info': {publication_curie: publication_info_dict},
                           'update date': kg2_util.format_timestamp(curr_timestamp),
                           'provided by': SEMMEDDB_IRI}
                preds_dict[key] = key_val
            else:
                key_val['publications info'][publication_curie] = publication_info_dict
                key_val['publications'] = key_val['publications'] + [publication_curie]
    connection.close()
    out_graph = {'edges': [rel_dict for rel_dict in preds_dict.values()],
                 'nodes': []}
    for rel_dict in out_graph['edges']:
        if len(rel_dict['publications']) > 1:
            rel_dict['publications'] = list(set(rel_dict['publications']))

    output_file_name = args.outputFile[0]
    temp_output_file_name = tempfile.mkstemp(prefix='kg2-')[1]
    if not output_file_name.endswith('.gz'):
        temp_output_file = open(temp_output_file_name, 'w')
        json.dump(out_graph, temp_output_file, indent=4, sort_keys=True)
    else:
        temp_output_file = gzip.GzipFile(temp_output_file_name, 'w')
        temp_output_file.write(json.dumps(out_graph, indent=4, sort_keys=True).encode('utf-8'))
    shutil.move(temp_output_file_name, output_file_name)

