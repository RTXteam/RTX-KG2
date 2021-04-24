#!/usr/bin/env python3
''' Creates Neo4j index and constraints for Canonicalized KG2

    Usage: create_indexes_constraints_canonicalized.py [--passwordFile=<password-file-name>] <Neo4j Username> [<Neo4j Password>]
'''
import argparse
import neo4j
import getpass
import sys
import json

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
    # Start a neo4j session, run a query, then close the session
    session = driver.session()
    query = session.run(query)
    session.close()
    return query


def node_labels():
    # Create a list of dictionaries where each key is "labels(n)"
    # and each value is a list containing a node label
    labels = "MATCH (n) RETURN distinct labels(n)"
    query = run_query(labels)
    data = query.data()
    label_list = []
    # Iterate through the list and dicitionaries to create a list
    # of node labels
    for dictionary in data:
        for key in dictionary:
            value = dictionary[key]
            value_string = value[0]
            label_list.append(value_string)
    return label_list


def create_index(label_list, property_name):
    """
    :param label_list: a list of the node labels in Neo4j
    """
    # For every label in the label list, create an index
    # on the given property name
    for label in label_list:
        run_query(f"CREATE INDEX ON :`{label}` ({property_name})")


def constraint(label_list):
    """
    :param label_list: a list of the node labels in Neo4j
    """
    # For every label in the label list, create a unique constraint
    # on the node id property
    constraint_query = "CREATE CONSTRAINT ON (n:Base) ASSERT n.id IS UNIQUE"
    run_query(constraint_query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configFile", type=str, help="RTXConfiguration JSON file containing the password", required=False, default=None)
    parser.add_argument("-u", "--user", type=str, help="Neo4j Username", default=None, required=False)
    parser.add_argument("-p", "--password", help="Neo4j Password", type=str, default=None, required=False)
    arguments = parser.parse_args()
    config_file_name = arguments.configFile
    if arguments.password is not None and arguments.configFile is not None:
        print("Not allowed to specify both password_file and password command-line options", file=sys.stderr)
        sys.exit()
    if arguments.user is None and arguments.configFile is None:
        print("Must specify a username on the command-line or via the RTXConfiguration config file", file=sys.stderr)
        sys.exit()
    if arguments.user is not None and arguments.configFile is not None:
        print("Cannot specify the username on both the command-line and the RTXConfiguration config file", file=sys.stderr)
        sys.exit()
    password = None
    neo4j_password = None
    neo4j_user = None
    if config_file_name is not None:
        print(config_file_name)
        config_data = json.load(open(config_file_name, 'r'))
        config_data_kg2_neo4j = config_data['KG2']['neo4j']
        neo4j_user = config_data_kg2_neo4j['username']
        neo4j_password = config_data_kg2_neo4j['password']
    if neo4j_password is None:
        neo4j_password = arguments.password
    if neo4j_password is None:
        neo4j_password = getpass.getpass("Please enter the Neo4j database password: ")
    if arguments.user is not None:
        neo4j_user = arguments.user
    bolt = 'bolt://127.0.0.1:7687'
    driver = neo4j.GraphDatabase.driver(bolt, auth=(neo4j_user, neo4j_password))
    node_label_list = node_labels() + ['Base']

    print("NOTE: If you are running create_indexes_constraints.py standalone and not via tsv-to-neo4j-canonicalized.sh, please make sure to re-set the read-only status of" +
          " the Neo4j database to TRUE", file=sys.stderr)

    # Create Indexes on Node Properties
    create_index(node_label_list, "name")
    create_index(node_label_list, "category")

    constraint(node_label_list)
    driver.close()
