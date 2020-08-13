#!/usr/bin/env python3
'''semmeddb_mysql_to_tuple_list_json.py: extracts all the predicate triples from SemMedDB, in a JSON tuple list

   Usage: semmeddb_mysql_to_tuple_list_json.py [--test] <mysqlConfigFile> <mysqlDBName> <outputFile.json>
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
import kg2_util
import pymysql
import re


NEG_REGEX = re.compile('^NEG_', re.M)


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='semmeddb_mysql_to_tuple_list_json.py: extracts all the predicate triples from SemMedDB, ' +
                                         'as a list of tuples')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('mysqlConfigFile', type=str)
    arg_parser.add_argument('mysqlDBName', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser


if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    mysql_config_file = args.mysqlConfigFile
    mysql_db_name = args.mysqlDBName
    test_mode = args.test
    connection = pymysql.connect(read_default_file=mysql_config_file, db=mysql_db_name)
    preds_dict = dict()
    sql_statement = ("SELECT PMID, SUBJECT_CUI, PREDICATE, OBJECT_CUI, DP, SENTENCE, SUBJECT_SCORE, "
                     "OBJECT_SCORE, DATE_FORMAT(CURR_TIMESTAMP, '%Y-%m-%d %H:%i:%S') FROM ((PREDICATION NATURAL JOIN CITATIONS) "
                     "NATURAL JOIN SENTENCE) NATURAL JOIN PREDICATION_AUX")
    if test_mode:
        sql_statement += " LIMIT 10000"
    results = {'data_dictionary': ['pmid',
                                   'subject_cui_str',
                                   'predicate',
                                   'object_cui_str',
                                   'pub_date',
                                   'sentence',
                                   'subject_score',
                                   'object_score',
                                   'curr_timestamp']}

    with connection.cursor() as cursor:
        cursor.execute(sql_statement)
        results['rows'] = cursor.fetchall()
    connection.close()
    output_file_name = args.outputFile
    kg2_util.save_json(results, output_file_name, test_mode)
