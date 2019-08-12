#!/usr/bin/env python3

''' Creates Neo4j index and constraints for KG2

    Usage: create_indexes_constraints.py --user <Neo4j Username>
                        --password <Neo4j Password>
'''
import neo4j
import argparse


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def run_query(query):
    """
    :param query: a cypher statement as a string to run
    """
    session = driver.session()
    query = session.run(query)
    session.close()
    return query


def node_labels():
    labels = "MATCH (n) RETURN distinct labels(n)"
    query = run_query(labels)
    data = query.data()
    label_list = []
    for dictionary in data:
        for key in dictionary:
            value = dictionary[key]
            value_string = value[0]
            label_list.append(value_string)
    return label_list


def edge_labels():
    labels = "MATCH (n)-[e]-(m) RETURN distinct type(e)"
    query = run_query(labels)
    data = query.data()
    print(data)
    label_list = []
    for dictionary in data:
        for key in dictionary:
            value = dictionary[key]
            label_list.append(value)
    print(label_list)
    return label_list


def create_index(label_list, property_name):
    """
    :param label_list: a list of the node labels in Neo4j
    """
    for label in label_list:
        if label.find(":") < 0: ##CREATE INDEX ON :BFO:0000050 (edge_label) gives error
            index_query = "CREATE INDEX ON :" + label + " (" + property_name + ")"
        run_query(index_query)


def constraint(label_list):
    """
    :param label_list: a list of the node labels in Neo4j
    """
    for label in label_list:
        constraint_query = "CREATE CONSTRAINT ON (n:" + label + ") \
                            ASSERT n.id IS UNIQUE"
        run_query(constraint_query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", type=str, help="Neo4j Username",
                        nargs=1, required=True)
    parser.add_argument("--password", help="Neo4j Password",
                        type=str, nargs=1, required=True)
    arguments = parser.parse_args()
    username = arguments.user[0]
    password = arguments.password[0]
    bolt = 'bolt://127.0.0.1:7687'
    driver = neo4j.GraphDatabase.driver(bolt, auth=(username, password))
    node_label_list = node_labels()
    edge_label_list = edge_labels()
    create_index(node_label_list, "category")
    create_index(node_label_list, "category_label")
    create_index(node_label_list, "deprecated")
    create_index(node_label_list, "description")
    create_index(node_label_list, "full_name")
    create_index(node_label_list, "iri")
    create_index(node_label_list, "name")
    create_index(node_label_list, "provided_by")
    create_index(node_label_list, "publications")
    create_index(node_label_list, "replaced_by")
    create_index(node_label_list, "synonym")
    create_index(node_label_list, "update_date")

    create_index(edge_label_list, "edge_label")
    create_index(edge_label_list, "negated")
    create_index(edge_label_list, "object")
    create_index(edge_label_list, "provided_by")
    create_index(edge_label_list, "publications")
    create_index(edge_label_list, "publications_info")
    create_index(edge_label_list, "relation")
    create_index(edge_label_list, "relation_curie")
    create_index(edge_label_list, "subject")
    create_index(edge_label_list, "update_date")
    constraint(node_label_list)
    driver.close()
