#!/usr/bin/env python3

'''Prints a JSON overview report of a knowledge graph in Neo4j, to STDOUT.

   Usage: report_stats_on_neo4j_kg.py
   changing the bolt, user, and password accordingly
'''

__author__ = 'Veronica Flores'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Veronica Flores']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


import datetime
import json
import kg2_util
import neo4j
import pprint

output_file_name = 'kg2-test-report-from-neo4j.json'


def count_nodes(session):
    res = session.run('MATCH (n) RETURN count(*)')
    return res.value()[0]


def count_edges(session):
    res = session.run('MATCH (n)-[r]->() RETURN count(r)')
    return res.value()[0]


def count_nodes_with_no_category(session):
    res = session.run('MATCH (n) WHERE n.category is null RETURN count(n) AS\
    NoCategoryNodes')
    return res.value()[0]


def count_nodes_by_curie_prefix(session):
    res = session.run('MATCH (n) WITH split(n.id, ":")[0] AS CuriePrefix,\
    count(n) AS NumberofNodes RETURN DISTINCT CuriePrefix, NumberofNodes ORDER\
    BY CuriePrefix')
    return {record[0]: record[1] for record in res.records()}


def count_nodes_by_curie_prefix_given_no_category(session):
    res = session.run('MATCH (n) WHERE n.category_label is null RETURN DISTINCT\
    split(n.id, ":")[0] AS CuriePrefix, count(*) AS Count')
    return {record[0]: record[1] for record in res.records()}


def count_nodes_by_category(session):
    res = session.run('MATCH (n) RETURN n.category_label AS Category, count(n)\
    AS NumberOfNodes ORDER BY n.category_label')
    return {record[0]: record[1] for record in res.records()}


def count_nodes_by_source(session):
    res = session.run('MATCH (n) RETURN n.provided_by AS Source, count(n) AS\
    Number ORDER BY n.provided_by')
    return {record[0]: record[1] for record in res.records()}


def count_nodes_by_source_and_category(session):
    res = session.run('MATCH (n) RETURN DISTINCT n.provided_by AS Source \
    ORDER BY n.provided_by')

    restwo = session.run('MATCH (n) WHERE NOT n.provided_by is null \
    RETURN DISTINCT n.provided_by AS Source, n.category_label AS Category, \
    count(n) AS Count ORDER BY n.provided_by')

    categorycountlist = []
    fulldict = {}
    restwolist = []
    sourcelist = []
    # scc = source, category, count
    sccdict = restwo.data()
    for dicts in sccdict:
        dictionary = dicts
        # flatten using list comprehension
        scclist = [item for tup in dictionary.items() for item in tup]
        restwolist.append(scclist)
    sourcedict = res.data()
    for dictionary in sourcedict:
        items = dictionary.items()
        for item in items:
            sourcelist.append(item[1])
    for source in sourcelist:
        categorycountlist = []
        for scclist in restwolist:
            if scclist[1] == source:
                categorycounttuple = (scclist[3], scclist[5])
                # Create a dictionary from a tuple
                categorycountlist.append(categorycounttuple)
        categorycountdict = dict(categorycountlist)
        fulldict.update({source: categorycountdict})
    return fulldict


def count_edges_by_source(session):
    res = session.run('MATCH ()-[r]->() RETURN r.provided_by AS Source,\
    count(r) AS NumberofRelationships ORDER BY r.provided_by')
    return {record[0]: record[1] for record in res.records()}


def count_edges_by_predicate_curie(session):
    res = session.run('MATCH ()-[r]->()RETURN r.relation AS Curie,\
    count(r) AS NumberofRelationships ORDER BY r.relation')
    return {record[0]: record[1] for record in res.records()}


def count_edges_by_predicate_type(session):
    res = session.run('MATCH (n)-[r]->() RETURN r.predicate AS PredicateType,\
    count(r) AS NumberofRelationships ORDER BY r.predicate')
    return {record[0]: record[1] for record in res.records()}


def count_edges_by_predicate_curie_prefix(session):
    res = session.run('MATCH ()-[r]->() RETURN DISTINCT split(r.relation,\
    ":")[0] AS CuriePrefix, count(r) AS NumberofRelationships ORDER BY\
    CuriePrefix')
    return {record[0]: record[1] for record in res.records()}


def count_predicates_by_predicate_curie_prefix(session):
    res = session.run('MATCH (n)-[r]->() WITH split(r.relation, ":")[0]\
    AS CuriePrefix, count(DISTINCT r.predicate) AS Count RETURN DISTINCT\
    CuriePrefix, Count')
    return {record[0]: record[1] for record in res.records()}


def count_types_of_pairs_of_curies_for_xrefs(session):
    res = session.run('MATCH (n)-[r:xref]->(m) WITH split(n.id, ":")[0] AS\
    Pair1, split(m.id, ":")[0] AS Pair2, count(n) AS NumberofNodes RETURN\
    DISTINCT Pair1, Pair2, NumberofNodes ORDER BY Pair1')
    return {(record[0] + "---" + record[1]): record[2] for record in
            res.records()}


def count_types_of_pairs_of_curies_for_equivs(session):
    res = session.run('MATCH (n)-[r:' + kg2_util.EDGE_LABEL_OWL_SAME_AS + ']->(m) WITH\
    split(n.id, ":")[0] AS Pair1, split(m.id, ":")[0] AS Pair2, count(n) AS \
    NumberofNodes RETURN DISTINCT Pair1, Pair2, NumberofNodes ORDER BY Pair1')
    return {(record[0] + "---" + record[1]): record[2] for record in
            res.records()}


def count_types_of_pairs_of_curies(session):
    res = session.run('MATCH (n)-[r]->(m) WITH split(n.id, ":")[0] AS Pair1,\
    split(m.id, ":")[0] AS Pair2, count(n) AS NumberofNodes RETURN DISTINCT\
    Pair1, Pair2, NumberofNodes ORDER BY Pair1')
    return {(record[0] + "---" + record[1]): record[2] for record in
            res.records()}


with neo4j.GraphDatabase.driver('bolt://localhost:7687',
                                auth=neo4j.basic_auth
                                ('user', 'password')) as driver:
    number_of_nodes = count_nodes(driver.session())
    number_of_edges = count_edges(driver.session())
    number_of_nodes_with_no_category = \
        count_nodes_with_no_category(driver.session())
    number_of_nodes_by_curie_prefix = \
        count_nodes_by_curie_prefix(driver.session())
    number_of_nodes_by_curie_prefix_given_no_category = \
        count_nodes_by_curie_prefix_given_no_category(driver.session())
    number_of_nodes_by_category = count_nodes_by_category(driver.session())
    number_of_nodes_by_source = count_nodes_by_source(driver.session())
    number_of_nodes_by_source_and_category = \
        count_nodes_by_source_and_category(driver.session())
    number_of_edges_by_source = count_edges_by_source(driver.session())
    number_of_edges_by_predicate_curie = \
        count_edges_by_predicate_curie(driver.session())
    number_of_edges_by_predicate_type = \
        count_edges_by_predicate_type(driver.session())
    number_of_edges_by_predicate_curie_prefix = \
        count_edges_by_predicate_curie_prefix(driver.session())
    number_of_predicates_by_predicate_curie_prefix = \
        count_predicates_by_predicate_curie_prefix(driver.session())
    number_of_types_of_pairs_of_curies_for_xrefs = \
        count_types_of_pairs_of_curies_for_xrefs(driver.session())
    number_of_types_of_pairs_of_curies_for_equivs = \
        count_types_of_pairs_of_curies_for_equivs(driver.session())
    number_of_types_of_pairs_of_curies = \
        count_types_of_pairs_of_curies(driver.session())

overall_results = {'_number_of_nodes': number_of_nodes,
                   '_number_of_edges': number_of_edges,
                   '_report_datetime': datetime.datetime.now().
                   strftime("%Y-%m-%d %H:%M:%S"),
                   'number_of_nodes_without_category':
                   number_of_nodes_with_no_category,
                   'number_of_nodes_by_curie_prefix':
                   number_of_nodes_by_curie_prefix,
                   'number_of_nodes_without_category_by_curie_prefix':
                   number_of_nodes_by_curie_prefix_given_no_category,
                   'number_of_nodes_by_category_label':
                   number_of_nodes_by_category,
                   'number_of_nodes_by_source': number_of_nodes_by_source,
                   'number_of_nodes_by_source_and_category':
                   number_of_nodes_by_source_and_category,
                   'number_of_edges_by_source': number_of_edges_by_source,
                   'number_of_edges_by_predicate_curie':
                   number_of_edges_by_predicate_curie,
                   'number_of_edges_by_predicate_type':
                   number_of_edges_by_predicate_type,
                   'number_of_edges_by_predicate_curie_prefixes':
                   number_of_edges_by_predicate_curie_prefix,
                   'number_of_predicates_by_predicate_curie_prefixes':
                   number_of_predicates_by_predicate_curie_prefix,
                   'types_of_pairs_of_curies_for_xrefs':
                   number_of_types_of_pairs_of_curies_for_xrefs,
                   'types_of_pairs_of_curies_for_equivs':
                   number_of_types_of_pairs_of_curies_for_equivs,
                   'types_of_pairs_of_curies':
                   number_of_types_of_pairs_of_curies}

pprint.pprint(overall_results)

with open(output_file_name, 'w') as output_file:
    json.dump(overall_results, output_file, indent=4, sort_keys=True)
