#!/usr/bin/env python3
'''umls_mysql_to_list_jsonl.py: extracts all of the information from UMLS and stores it in a JSON Lines output

   Usage: umls_mysql_to_list_jsonl.py [--test] <mysqlConfigFile> <mysqlDBName> <outputFile.json>
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
import pymysql


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='umls_mysql_to_list_jsonl.py: extracts all of the information from UMLS and stores it in a JSON Lines output')
    arg_parser.add_argument('mysqlConfigFile', type=str)
    arg_parser.add_argument('mysqlDBName', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser


def get_english_sources(cursor):
    sources_sql_statement = "SELECT RSAB, LAT FROM MRSAB"
    sources = []

    cursor.execute(sources_sql_statement)
    for result in cursor.fetchall():
        (source, language) = result
        if language == 'ENG':
            sources.append(source)

    print("Finished sources_sql_statement at", kg2_util.date())

    return sources


def code_sources(cursor, output):
    code_source_info = dict()
    cui_key = 'cuis'
    name_key = 'names'
    info_key = 'info'

    names_sql_statement = "SELECT con.CODE, con.SAB, GROUP_CONCAT(DISTINCT con.CUI), GROUP_CONCAT(DISTINCT CONCAT(con.ISPREF, '|', con.STR) SEPARATOR '\t') FROM MRCONSO con GROUP BY con.CODE, con.SAB"
    extra_info_sql_statement = "SELECT sat.CODE, sat.SAB, GROUP_CONCAT(DISTINCT CONCAT(sat.ATN, '|', sat.ATV) SEPARATOR '\t') FROM MRSAT sat GROUP BY sat.CODE, sat.SAB"

    cursor.execute(names_sql_statement)
    for result in cursor.fetchall():
        (node_id, node_source, cui, name) = result
        key = (node_id, node_source)
        code_source_info[key] = dict()
        code_source_info[key][cui_key] = cui.split(',')
        code_source_info[key][name_key] = name.split('\t')

    print("Finished names_sql_statement at", kg2_util.date())

    cursor.execute(extra_info_sql_statement)
    for result in cursor.fetchall():
        (node_id, node_source, info) = result
        key = (node_id, node_source)
        if key not in code_source_info:
            code_source_info[key] = dict()
            print(key, "not in original code_source_info dict")
        code_source_info[key][info_key] = info.split('\t')

    print("Finished extra_info_sql_statement at", kg2_util.date())

    for key, val in code_source_info.items():
        # It needs to print it all out for some reason to actually do the output write
        print(str({str(key): val}))
        output.write({str(key): val})


def cui_sources(cursor, output, sources):
    cui_source_info = dict()
    tui_key = 'tuis'
    name_key = 'names'
    relation_key = 'relations'
    definitions_key = 'definitions'

    sources_where = str(sources).replace('[', '(').replace(']', ')')

    names_sql_statement = "SELECT CUI, GROUP_CONCAT(DISTINCT CONCAT(SAB, '|', ISPREF, '|', STR) SEPARATOR '\t') FROM MRCONSO WHERE SAB IN " + sources_where + " GROUP BY CUI"
    tuis_sql_statement = "SELECT CUI, GROUP_CONCAT(TUI) FROM MRSTY GROUP BY CUI"
    relations_sql_statement = "SELECT CUI1, REL, RELA, DIR, CUI2, SAB FROM MRREL WHERE SAB IN " + sources_where
    definitions_sql_statement = "SELECT CUI, DEF FROM MRDEF WHERE SAB IN " + sources_where

    cursor.execute(names_sql_statement)
    for result in cursor.fetchall():
        (node_id, names) = result
        key = node_id
        cui_source_info[key] = dict()
        cui_source_info[key][name_key] = dict()
        for name in names.split('\t'):
            split_name = name.split('|')
            assert len(split_name) == 3, split_name
            if split_name[0] not in cui_source_info[key][name_key]:
                cui_source_info[key][name_key][split_name[0]] = dict()
            if split_name[1] not in cui_source_info[key][name_key][split_name[0]]:
                cui_source_info[key][name_key][split_name[0]][split_name[1]] = list()
            existing_val = cui_source_info[key][name_key][split_name[0]][split_name[1]].append(split_name[2])

    print("Finished names_sql_statement at", kg2_util.date())

    cursor.execute(tuis_sql_statement)
    for result in cursor.fetchall():
        (node_id, tuis) = result
        key = node_id
        if key not in cui_source_info:
            # This happens if a node doesn't have an English name. See https://github.com/RTXteam/RTX-KG2/issues/316#issuecomment-1672074392
            continue
        cui_source_info[key][tui_key] = tuis.split('\t')

    print("Finished tuis_sql_statement at", kg2_util.date())

    cursor.execute(relations_sql_statement)
    for result in cursor.fetchall():
        (cui1, rel, rela, direction, cui2, source) = result
        key = cui1
        if key not in cui_source_info:
            # See above for explanation
            continue
        if relation_key not in cui_source_info[key]:
            cui_source_info[key][relation_key] = list()
        cui_source_info[key][relation_key].append((rel, rela, direction, cui2, source))

    print("Finished relations_sql_statement at", kg2_util.date())

    cursor.execute(definitions_sql_statement)
    for result in cursor.fetchall():
        (node_id, definition) = result
        key = node_id
        if key not in cui_source_info:
            # See above for explanation
            continue
        cui_source_info[key][definitions_key] = definition

    print("Finished definitions_sql_statement at", kg2_util.date())

    for key, val in cui_source_info.items():
        # It needs to print it all out for some reason to actually do the output write
        print(str({str(key): val}))
        output.write({str(key): val})



if __name__ == '__main__':
    print("Starting umls_mysql_to_list_jsonl.py at", kg2_util.date())
    args = make_arg_parser().parse_args()
    mysql_config_file = args.mysqlConfigFile
    mysql_db_name = args.mysqlDBName
    output_file_name = args.outputFile
    connection = pymysql.connect(read_default_file=mysql_config_file, db=mysql_db_name)
    preds_dict = dict()

    output_info = kg2_util.create_single_jsonlines(False)
    output = output_info[0]

    # https://stackoverflow.com/questions/7208773/mysql-row-30153-was-cut-by-group-concat-error
    max_len_sql_statement = "SET group_concat_max_len=1000000000"

    with connection.cursor() as cursor:
        cursor.execute(max_len_sql_statement)
        cursor.fetchall()

        # Execute statement we care about after clearing any "results"
        sources = get_english_sources(cursor)

        cui_sources(cursor, output, sources)

        # code_sources(cursor, output)
    connection.close()

    kg2_util.close_single_jsonlines(output_info, output_file_name)
    print("Finishing umls_mysql_to_list_jsonl.py at", kg2_util.date())
