#!/usr/bin/env python3
'''umls_mysql_to_list_jsonl.py: extracts all of the information from UMLS and stores it in a JSON Lines output

   Usage: umls_mysql_to_list_jsonl.py [--test] <mysqlConfigFile> <mysqlDBName> <outputFile.jsonl>
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


def get_args():
    arg_parser = argparse.ArgumentParser(description='umls_mysql_to_list_jsonl.py: extracts all of the information from UMLS and stores it in a JSON Lines output')
    arg_parser.add_argument('mysqlConfigFile', type=str)
    arg_parser.add_argument('mysqlDBName', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


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
    tui_key = 'tuis'
    cui_key = 'cuis'
    name_key = 'names'
    definitions_key = 'definitions'

    # See info about these here: https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/attribute_names.html
    info_key = 'attributes'

    # See TTY meanings here: https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/abbreviations.html
    names_sql_statement = "SELECT con.CODE, con.SAB, GROUP_CONCAT(DISTINCT con.CUI), GROUP_CONCAT(DISTINCT CONCAT(con.TTY, '|', con.ISPREF, '|', con.STR) SEPARATOR '\t') FROM MRCONSO con GROUP BY con.SAB, con.CODE"
    extra_info_sql_statement = "SELECT sat.CODE, sat.SAB, GROUP_CONCAT(DISTINCT CONCAT(sat.ATN, '|', REPLACE(sat.ATV, '\t', ' ')) SEPARATOR '\t') FROM MRSAT sat GROUP BY sat.SAB, sat.CODE"
    tuis_sql_statement = "SELECT con.CODE, con.SAB, GROUP_CONCAT(DISTINCT sty.TUI) FROM MRCONSO con LEFT JOIN MRSTY sty ON con.CUI = sty.CUI GROUP BY con.SAB, con.CODE"
    definitions_sql_statement = "SELECT con.CODE, con.SAB, GROUP_CONCAT(DISTINCT def.DEF SEPARATOR ';') FROM MRCONSO con INNER JOIN MRDEF def on con.CUI=def.CUI WHERE con.SAB=def.SAB GROUP BY con.SAB, con.CODE"

    cursor.execute(names_sql_statement)
    for result in cursor.fetchall():
        (node_id, node_source, cui, names) = result
        key = (node_source, node_id)
        code_source_info[key] = dict()
        code_source_info[key][cui_key] = cui.split(',')
        if name_key not in code_source_info[key]:
            code_source_info[key][name_key] = dict()
        for name in names.split('\t'):
            split_name = name.split('|')
            assert len(split_name) == 3, split_name
            if split_name[0] not in code_source_info[key][name_key]:
                code_source_info[key][name_key][split_name[0]] = dict()
            if split_name[1] not in code_source_info[key][name_key][split_name[0]]:
                code_source_info[key][name_key][split_name[0]][split_name[1]] = list()
            code_source_info[key][name_key][split_name[0]][split_name[1]].append(split_name[2])

    print("Finished names_sql_statement at", kg2_util.date())

    cursor.execute(extra_info_sql_statement)
    for result in cursor.fetchall():
        (node_id, node_source, info) = result
        key = (node_source, node_id)
        if key not in code_source_info:
            # This occurs if a node doesn't have a name.
            continue
        if info_key not in code_source_info[key]:
            code_source_info[key][info_key] = dict()
        for info_piece in info.split('\t'):
            split_info_piece = info_piece.split('|')
            assert len(split_info_piece) == 2, split_info_piece
            if split_info_piece[0] not in code_source_info[key][info_key]:
                code_source_info[key][info_key][split_info_piece[0]] = set()
            code_source_info[key][info_key][split_info_piece[0]].add(split_info_piece[1])
        for info_type in code_source_info[key][info_key]:
            code_source_info[key][info_key][info_type] = list(code_source_info[key][info_key][info_type])

    print("Finished extra_info_sql_statement at", kg2_util.date())

    cursor.execute(tuis_sql_statement)
    for result in cursor.fetchall():
        (node_id, node_source, tuis) = result
        key = (node_source, node_id)
        if key not in code_source_info:
            # This occurs if a node doesn't have a name.
            continue
        code_source_info[key][tui_key] = tuis.split(',')

    print("Finished tuis_sql_statement at", kg2_util.date())

    cursor.execute(definitions_sql_statement)
    for result in cursor.fetchall():
        (node_id, node_source, definition) = result
        key = (node_source, node_id)
        if key not in code_source_info:
            # This occurs if a node doesn't have a name.
            continue
        code_source_info[key][definitions_key] = definition

    print("Finished definitions_sql_statement at", kg2_util.date())

    record_num = 0
    for key, val in code_source_info.items():
        record_num += 1
        output.write({str(key): val})

    print("Finished adding", record_num, "records in code_sources() at", kg2_util.date())


def cui_sources(cursor, output, sources):
    cui_source_info = dict()
    tui_key = 'tuis'
    name_key = 'names'
    relation_key = 'relations'
    definitions_key = 'definitions'
    umls_source_name = 'UMLS'

    # Make the sources list a MySQL list
    sources_where = str(sources).replace('[', '(').replace(']', ')')

    # See TTY meanings here: https://www.nlm.nih.gov/research/umls/knowledge_sources/metathesaurus/release/abbreviations.html
    names_sql_statement = "SELECT CUI, GROUP_CONCAT(DISTINCT CONCAT(TTY, '|', SAB, '|', ISPREF, '|', STR) SEPARATOR '\t') FROM MRCONSO WHERE SAB IN " + sources_where + " GROUP BY CUI"
    tuis_sql_statement = "SELECT CUI, GROUP_CONCAT(TUI) FROM MRSTY GROUP BY CUI"
    relations_sql_statement = "SELECT DISTINCT CUI1, REL, RELA, DIR, CUI2, SAB FROM MRREL WHERE SAB IN " + sources_where
    definitions_sql_statement = "SELECT CUI, GROUP_CONCAT(DISTINCT CONCAT(SAB, '|', DEF) SEPARATOR '\t') FROM MRDEF WHERE SAB IN " + sources_where + " GROUP BY CUI"

    cursor.execute(names_sql_statement)
    for result in cursor.fetchall():
        (node_id, names) = result
        key = (umls_source_name, node_id)
        cui_source_info[key] = dict()
        cui_source_info[key][name_key] = dict()
        for name in names.split('\t'):
            split_name = name.split('|')
            assert len(split_name) == 4, split_name
            name_tty = split_name[0]
            name_source = split_name[1]
            name_ispref = split_name[2]
            name_str = split_name[3]
            if name_source not in cui_source_info[key][name_key]:
                cui_source_info[key][name_key][name_source] = dict()
            if name_tty not in cui_source_info[key][name_key][name_source]:
                cui_source_info[key][name_key][name_source][name_tty] = dict()
            if name_ispref not in cui_source_info[key][name_key][name_source][name_tty]:
                cui_source_info[key][name_key][name_source][name_tty][name_ispref] = list()
            cui_source_info[key][name_key][name_source][name_tty][name_ispref].append(name_str)

    print("Finished names_sql_statement at", kg2_util.date())

    cursor.execute(tuis_sql_statement)
    for result in cursor.fetchall():
        (node_id, tuis) = result
        key = (umls_source_name, node_id)
        if key not in cui_source_info:
            # This happens if a node doesn't have an English name. See https://github.com/RTXteam/RTX-KG2/issues/316#issuecomment-1672074392
            continue
        cui_source_info[key][tui_key] = tuis.split(',')

    print("Finished tuis_sql_statement at", kg2_util.date())

    cursor.execute(relations_sql_statement)
    for result in cursor.fetchall():
        (cui1, rel, rela, direction, cui2, source) = result
        key = (umls_source_name, cui1)
        if key not in cui_source_info:
            # See above for explanation
            continue
        if relation_key not in cui_source_info[key]:
            cui_source_info[key][relation_key] = dict()

        relation_type_key = ','.join([str(rel), str(rela), str(direction)])
        if source not in cui_source_info[key][relation_key]:
            cui_source_info[key][relation_key][source] = dict()
        if relation_type_key not in cui_source_info[key][relation_key][source]:
            cui_source_info[key][relation_key][source][relation_type_key] = list()
        cui_source_info[key][relation_key][source][relation_type_key].append(cui2)

    print("Finished relations_sql_statement at", kg2_util.date())

    cursor.execute(definitions_sql_statement)
    for result in cursor.fetchall():
        (node_id, definition) = result
        key = (umls_source_name, node_id)
        if key not in cui_source_info:
            # See above for explanation
            continue
        for def_piece in definition.split('\t'):
            split_def_piece = def_piece.split('|')
            assert len(split_def_piece) == 2, split_def_piece
            cui_source_info[key][definitions_key][split_def_piece[0]] = split_def_piece[1]

    print("Finished definitions_sql_statement at", kg2_util.date())

    record_num = 0
    for key, val in cui_source_info.items():
        record_num += 1
        output.write({str(key): val})

    print("Finished adding", record_num, "records in cui_sources() at", kg2_util.date())


if __name__ == '__main__':
    print("Starting umls_mysql_to_list_jsonl.py at", kg2_util.date())
    args = get_args()
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

        # This ensure we don't have UMLS sources that overwrite each other's names
        sources = get_english_sources(cursor)

        code_sources(cursor, output)
        cui_sources(cursor, output, sources)

    connection.close()

    kg2_util.close_single_jsonlines(output_info, output_file_name)
    print("Finishing umls_mysql_to_list_jsonl.py at", kg2_util.date())
