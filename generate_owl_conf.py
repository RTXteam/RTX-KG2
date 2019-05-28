#!/usr/bin/env python3

# generates a YAML configuration file listing all of the UMLS-derived OWL files
# for use with build-kg2.py
import pandas
import os
import yaml

# retrieve MRSAB.RRF from the kg2dev instance
os.system('scp ubuntu@kg2dev.saramsey.org:kg2-build/umls/META/MRSAB.RRF .')
df_umls_sources = pandas.read_csv("MRSAB.RRF", sep="|", index_col=3,
                                  header=None).iloc[:, [22]]
df_umls_sources.columns = ['Vocabulary']

conf_data = list()

df_umls2rdf = pandas.read_csv("umls2rdf-umls.conf", comment="#",
                              names=['RSAB', 'filename', 'load'])

for row in df_umls2rdf.iterrows():
    filename = row[1]['filename']
    curie = row[1]['RSAB']
    rsab = curie
    if ';' in curie:
        split_data = curie.split(';')
        curie = split_data[1]
        rsab = split_data[0]

    source_title = df_umls_sources.loc[rsab, "Vocabulary"]
    if type(source_title) == pandas.DataFrame:
        source_title = source_title.tolist()[0]
    conf_data.append({'url': 'https://identifiers.org/umls/' + curie,
                      'file': filename,
                      'download': False,
                      'title': source_title})

yaml.dump(conf_data, open('owl-load-inventory-umls.yaml','w'),
          default_flow_style=False)
