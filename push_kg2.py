import os
import sys
from collections import namedtuple, Counter
from neo4j.v1 import GraphDatabase, basic_auth
import argparse
import time

try:
    from RTXConfiguration import RTXConfiguration
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from RTXConfiguration import RTXConfiguration



class push_kg2:
    
    def __init__(self, bolt, user = None, password = None):
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

        # Connection information for the neo4j server, populated with orangeboard
        self.driver = GraphDatabase.driver(bolt, auth=basic_auth(user, password))

    def close(self):
        """
        Closes the driver connection
        """
        self.driver.close()

    def push_nodes(self, json_file, batch = 10000):
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
                                "CALL apoc.create.node([n.`category label`, 'Base'], {}) YIELD node " +\
                                'SET node.category = n.category, node.id = n.id, node.name = n.name, ' +\
                                'node.`creation date` = n.`creation date`, node.deprecated = n.deprecated, ' +\
                                'node.description = n.description, node.`full name` = n.`full name`, ' +\
                                'node.iri = n.iri, node.`ontology node type` = n.`ontology node type`, ' +\
                                'node.`provided by` = n.`provided by`, node.publications = n.publications, ' +\
                                'node.`replaced by` = n.`replaced by`, node.synonym = n.synonym, ' +\
                                'node.`update date` = n.`update date` ' +\
                                'RETURN count(*)' +\
                                '", {batchSize: ' + batch + ', iterateList: true})'
        with self.driver.session() as session:
            res = session.run(cypher_upload_nodes)
            session.run("CREATE INDEX ON :Base(id)")
        return res.value()[0]

    def push_edges(self, json_file, batch = 10000):
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
                                'CALL apoc.create.relationship(a,e.`edge label`,{}, b) YIELD rel ' +\
                                'SET rel.`provided by` = e.`provided by`, rel.publications = e.publications, ' +\
                                'rel.negated = e.negated, rel.relation = e.relation, rel.`relation curie` = e.`relation curie`, ' +\
                                'rel.`update date` = e.`update date` ' +\
                                'RETURN count(*) ' +\
                                '", {batchSize: ' + batch + ', iterateList: true})'
        with self.driver.session() as session:
            res = session.run(cypher_upload_edges)
        return res.value()[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--user", type=str, help="The neo4j username", default = None)
    parser.add_argument("-p", "--password", type=str, help="The neo4j passworl", default = None)
    parser.add_argument("-b", "--bolt", type=str, help="The neo4j bolt address", default = "kg2ase2.rtx.ai:7687")
    parser.add_argument("-f", "--file", type=str, help="The path of the json file for upload prefixed with 'file:///' (can also be a url)", default = "file:///var/lib/neo4j/import/kg2-test2.json")
    parser.add_argument("-n","--nodes", action="store_true", help="include if you just want to upload nodes (if used in conjunction with edges option will upload both)")
    parser.add_argument("-e","--edges", action="store_true", help="include if you just want to upload edges (if used in conjunction with nodes option will upload both)")
    parser.add_argument("--batch", type=int, help="The batch size used for uploading the edges (must be a positive integer)", default=10000)
    parser.add_argument("--debug", action="store_true")
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

    kg2_pusher = push_kg2(args.bolt, args.user, args.password)
    if node_flag:
        t0 = time.time()
        count = kg2_pusher.push_nodes(args.file)
        if args.debug:
            print(str(count), " batches of ", args.batch," nodes uploaded in ", str(time.time() - t0), " seconds.")
    if edge_flag:
        t0 = time.time()
        count = kg2_pusher.push_edges(args.file, str(args.batch))
        if args.debug:
            print(str(count), " batches of ", args.batch," edges uploaded in ", str(time.time() - t0), " seconds.")

    kg2_pusher.close()


