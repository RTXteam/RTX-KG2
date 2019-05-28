#!/usr/bin/env python3

import MySQLdb
import getpass
# Generate configuration for the "umls2rdf" software, by querying which data sources are
# available in an installed UMLS mysql database; this script prints the configuration
# information as CSV to stdout.

password = getpass.getpass("Please enter the password for accessing a UMLS mysql database: ")

conn = MySQLdb.connect(host='kg2dev.saramsey.org',
                       user='ubuntu',
                       passwd=password,
                       db='umls',
                       use_unicode=True)

cursor = conn.cursor()
cursor.execute("select distinct RSAB from MRSAB")  # SAR: add where clause to specify language = ENG?
for record in cursor.fetchall():
    sab = record[0]
    print(sab + ',' + 'umls-' + sab.lower() + '.ttl' + ',' + 'load_on_codes')
