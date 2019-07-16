#!/usr/bin/env python3
'''push_kg2.py: push a JSON KG to an (empty) Neo4j database (NOTE: if local, the JSON file needs to be in 
                /var/lib/neo4j/import and readable by user neo4j

   Usage: push_kg2.py
'''

import argparse
import os
import sys
from neo4j.v1 import GraphDatabase, basic_auth
import time

try:
    from RTXConfiguration import RTXConfiguration
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from RTXConfiguration import RTXConfiguration


class push_kg2:

    def __init__(self, bolt, user=None, password=None, debug=False):
        """
        :param bolt: A string containing the bolt address of the neo4j instance you wish to upload to
        :param user: A string containing the username for neo4j
        :param password: A string containing the password for neo4j
        """
        if user is None or password is None:
            rtxConfig = RTXConfiguration()
            if user is None:
                user = rtxConfig.neo4j_username
            if password is None:
                password = rtxConfig.neo4j_password

        self.debug = debug
        # Connection information for the neo4j server, populated with orangeboard
        self.driver = GraphDatabase.driver(bolt, auth=basic_auth(user, password))

    def get_number_of_nodes_in_db(self):
        num_nodes = None
        with self.driver.session() as session:
            result = session.run("MATCH (n) return count(*)")
            num_nodes = result.value()[0]
        return num_nodes

    def close(self):
        """
        Closes the driver connection
        """
        self.driver.close()

    def run_cypher(self, cypher: str):
        if self.debug:
            print(cypher)
        with self.driver.session() as session:
            res = session.run(cypher)
            if self.debug:
                notifs_list = res.summary().notifications
                if len(notifs_list) > 0:
                    print(notifs_list)
            return res

    def neo4j_clear(self):
        """deletes all nodes and relationships in the orangeboard

        :returns: nothing
        """
        self.run_cypher('MATCH (n) DETACH DELETE n')
        self.run_cypher('CALL apoc.schema.assert({},{},true) YIELD label, key')

    def push_nodes(self, json_file, batch=10000):
        """
        :param json_file: A string containing the path (or URL) to the json file
        :param batch: A string or integer containing a positive integer number of nodes to include in each batch upload
        """
        if isinstance(batch, int):
            batch = str(batch)
        # This need to be updated with publications info when the json is updated to be a string
        cypher_upload_nodes = 'CALL apoc.periodic.iterate("' +\
            "WITH '" + json_file + "' AS file " +\
            'CALL apoc.load.json(file) YIELD value ' +\
            'UNWIND value.nodes AS n RETURN n ' +\
            '"," ' +\
            "CALL apoc.create.node([n.category_label, 'Base'], {}) YIELD node " +\
            'SET node.category = n.category, ' +\
            'node.id = n.id, node.name = n.name, ' +\
            'node.creation_date = n.`creation date`, ' +\
            'node.deprecated = n.deprecated, ' +\
            'node.description = n.description, ' +\
            'node.full_name = n.`full name`, ' +\
            'node.iri = n.iri, ' +\
            'node.provided_by = n.`provided by`, ' +\
            'node.publications = n.publications, ' +\
            'node.replaced_by = n.`replaced by`, ' +\
            'node.synonym = n.synonym, ' +\
            'node.update_date = n.`update date`, ' +\
            'node.category_label = n.`category label` ' +\
            'RETURN count(*)' +\
            '", {batchSize: ' + batch + ', iterateList: true})'
        res = self.run_cypher(cypher_upload_nodes)
        res_ctr = res.value()[0]
        # Redundancy to make querying by property rather than label possible
        self.run_cypher('CREATE CONSTRAINT ON (n:Base) ASSERT n.id IS UNIQUE')

        return res_ctr

    def push_edges(self, json_file, batch=10000):
        """
        :param json_file: A string containing the path (or URL) to the json file
        :param batch: A string or integer containing a positive integer number of edges to include in each batch upload
        """
        if isinstance(batch, int):
            batch = str(batch)
        cypher_upload_edges = 'CALL apoc.periodic.iterate("' +\
            "WITH '" + json_file + "' AS file " +\
            'CALL apoc.load.json(file) YIELD value ' +\
            'UNWIND value.edges AS e RETURN e ' +\
            '"," ' +\
            'MATCH (a:Base {id:e.subject}) , (b:Base {id:e.object}) ' +\
            'CALL apoc.create.relationship(a, e.`edge label`, {}, b) YIELD rel ' +\
            'SET rel.provided_by = e.`provided by`, ' +\
            'rel.publications = e.publications, ' +\
            'rel.publications_info = e.`publications info`, ' +\
            'rel.negated = e.negated, ' +\
            'rel.relation = e.relation, ' +\
            'rel.relation_curie = e.`relation curie`, ' +\
            'rel.update_date = e.`update date`, ' +\
            'rel.edge_label = e.`edge label` ' +\
            'RETURN count(*) ' +\
            '", {batchSize: ' + batch + ', iterateList: true})'
        res = self.run_cypher(cypher_upload_edges)
        res_ctr = res.value()[0]
        return res_ctr


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", type=str, help="The neo4j username", default=None)
    parser.add_argument("-p", "--password", type=str, help="The neo4j passworl", default=None)
    parser.add_argument("-b", "--bolt", type=str, help="The neo4j bolt URI (including port)", default="bolt://localhost:7687")
    parser.add_argument("-f", "--file", type=str, help="The name <rel_file> of the JSON file to import (<rel_file> should be a relative path to the file within /var/lib/neo4j/import; <rel_file> should *not* contain /var/lib/neo4j/import; file should be readable by user neo4j)",
                        default="file:///kg2-test.json")
    parser.add_argument("-n", "--nodes", action="store_true",
                        help="include if you just want to upload nodes (if used in conjunction with edges option will upload both)")
    parser.add_argument("-e", "--edges", action="store_true",
                        help="include if you just want to upload edges (if used in conjunction with nodes option will upload both)")
    parser.add_argument("--batch", type=int, help="The batch size used for uploading the edges (must be a positive integer)", default=10000)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--clear", action="store_true", help="Clear the neo4j database before uploading data")
    args = parser.parse_args()

    if args.user is None or args.password is None:
        rtxConfig = RTXConfiguration()
        if args.user is None:
            args.user = rtxConfig.neo4j_username
        if args.password is None:
            args.password = rtxConfig.neo4j_password

    if args.bolt is None:
        raise Exception("Must specify a bolt address for the neo4j instance.")

    node_flag = True
    edge_flag = True
    if args.nodes and not args.edges:
        edge_flag = False
    elif args.edges and not args.nodes:
        node_flag = False

    kg2_pusher = push_kg2(args.bolt, args.user, args.password, args.debug)
    if args.debug:
        num_nodes = kg2_pusher.get_number_of_nodes_in_db()
        if num_nodes > 0 and not args.clear:
            print("WARNING: pushing nodes to a non-empty database", file=sys.stderr)
    if args.clear:
        kg2_pusher.neo4j_clear()
    if node_flag:
        t0 = time.time()
        count = kg2_pusher.push_nodes(args.file)
        if args.debug:
            print(str(count), " batches of ", args.batch, " nodes uploaded in ", str(time.time() - t0), " seconds.")
    if edge_flag:
        t0 = time.time()
        count = kg2_pusher.push_edges(args.file, str(args.batch))
        if args.debug:
            print(str(count), " batches of ", args.batch, " edges uploaded in ", str(time.time() - t0), " seconds.")

    kg2_pusher.close()
