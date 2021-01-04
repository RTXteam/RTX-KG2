#!/usr/bin/env python3

import getpass
import json
import requests

NEO4J_URL = 'http://kg2endpoint2.rtx.ai:7474'
TIMEOUT_SEC = 3600

first_line = True


def query_neo4j(neo4j_auth: dict, http_uri: str, cypher_query: str, test_mode=False):
    if not http_uri.startswith('http://') and not http_uri.startswith('https://'):
        http_uri = 'http://' + http_uri
    if not http_uri.endswith('/db/data'):
        http_uri = http_uri + '/db/data'
    http_uri = http_uri + "/cypher"
    if test_mode:
        print("Querying Neo4j at URI: " + http_uri + "; cypher query: " + cypher_query)
    query_response = requests.post(http_uri,
                                   headers={'Content-type': 'application/json; charset=UTF-8; stream=true',
                                            'Accept': 'application/json',
                                            'X-Stream': 'true'},  # X-Stream is *VITAL* in order to avoid HTTP 400 error code (SAR)
                                   data=json.dumps({'query': cypher_query, 'params': {}}),
                                   auth=requests.auth.HTTPBasicAuth(neo4j_auth['user'],
                                                                    neo4j_auth['password']),
                                   timeout=TIMEOUT_SEC)
    status_code = query_response.status_code
    if status_code != 200:
        raise Exception('HTTP response status code: ' + str(status_code) + ' for URL: ' + http_uri)
    return query_response.json()['data']


neo4j_password = getpass.getpass('Enter password for Neo4j database server ' + NEO4J_URL + " ")

neo4j_auth = {'user': 'neo4j',
              'password': neo4j_password}

json_res = query_neo4j(neo4j_auth,
                       NEO4J_URL,
                       "MATCH (n)-[r]->(m) return r.relation_curie, r.provided_by",
                       True)
curie_info = dict()
for row in json_res:
    relation_curie = row[0]
    provided_by = json.loads(row[1].replace('\'', '\"'))
    existing_provided_by = curie_info.get(relation_curie, None)
    if existing_provided_by is None:
        existing_provided_by = set()
        assert type(provided_by) == list
        for provided_by_iri in provided_by:
            existing_provided_by.add(provided_by_iri)
            curie_info[relation_curie] = existing_provided_by
with open('curies-to-provided-by.tsv', 'w') as output_file:
    for [relation_curie, provided_by_set] in curie_info.items():
        print(relation_curie + '\t' + str(list(provided_by_set)).replace('[', '').replace(']', '').replace('\'', ''),
              file=output_file)


# with neo4j.GraphDatabase.driver(NEO4J_URL,
#                                 auth=neo4j.basic_auth
#                                 ('neo4j', mypassword)) as driver:
#     with driver.session() as session:
#         with open('predicate-curation-for-translator - Sheet1.tsv', 'r') as input_file:
#             for line in input_file:
#                 if first_line:
#                     first_line = False
#                     continue
#                 fields = line.rstrip().split('\t')
#                 relation_curie = fields[0]
#                 cypher_str = 'MATCH (n)-[r {relation_curie: \'' + relation_curie + '\'}]->(m) return r.provided_by'
#                 print(cypher_str)
#                 res = session.run(cypher_str).records()
#                 print(res)
