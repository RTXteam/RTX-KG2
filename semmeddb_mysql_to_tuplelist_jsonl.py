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
    arg_parser.add_argument('mysqlConfigFile', type=str)
    arg_parser.add_argument('mysqlDBName', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser


if __name__ == '__main__':
    print("Starting semmeddb_mysql_to_tuple_list_json.py at", kg2_util.date())
    args = make_arg_parser().parse_args()
    mysql_config_file = args.mysqlConfigFile
    mysql_db_name = args.mysqlDBName
    output_file_name = args.outputFile
    version_number = version_number.strip('VER')
    connection = pymysql.connect(read_default_file=mysql_config_file, db=mysql_db_name)
    preds_dict = dict()

    output_info = kg2_util.create_single_jsonlines(False)
    output = output_info[0]

    # https://stackoverflow.com/questions/7208773/mysql-row-30153-was-cut-by-group-concat-error
    max_len_sql_statement = "SET group_concat_max_len=1000000"

    sql_statement = ("SELECT SUBJECT_CUI, PREDICATE, OBJECT_CUI, GROUP_CONCAT(DISTINCT SUBJECT_SEMTYPE), GROUP_CONCAT(DISTINCT OBJECT_SEMTYPE), "
                     "GROUP_CONCAT(DISTINCT DATE_FORMAT(CURR_TIMESTAMP, '%Y-%m-%d %H:%i:%S')), "
                     "GROUP_CONCAT(CONCAT(PMID, '|', SENTENCE, '|', SUBJECT_SCORE, '|', OBJECT_SCORE, '|', DP) SEPARATOR '\t') "
                     "FROM ((PREDICATION NATURAL JOIN CITATIONS) NATURAL JOIN SENTENCE) NATURAL JOIN PREDICATION_AUX "
                     "GROUP BY SUBJECT_CUI, PREDICATE, OBJECT_CUI")

    with connection.cursor() as cursor:
        cursor.execute(max_len_sql_statement)
        cursor.fetchall()

        # Execute statement we care about after clearing any "results"
        cursor.execute(sql_statement)
        for result in cursor.fetchall():
            output.write(result)
    connection.close()

    kg2_util.close_single_jsonlines(output_info, output_file_name)
    print("Finishing semmeddb_mysql_to_tuple_list_json.py at", kg2_util.date())
