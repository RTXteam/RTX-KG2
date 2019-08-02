import neo4j
import argparse


def run_query(query):
    """
    :param query: a cypher statement as a string to run
    """
    session = driver.session()
    query = session.run(query)
    session.close()
    return query


def labels():
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


def index_name(label_list):
    """
    :param label_list: a list of the node labels in Neo4j
    """
    for label in label_list:
        index_query = "CREATE INDEX ON :" + label + " (name)"
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
    label_list = labels()
    index_name(label_list)
    constraint(label_list)
    driver.close()
