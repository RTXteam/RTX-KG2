#!/usr/bin/env python3

''' Creates a set of tsv files for importing into Neo4j from KG2 JSON

    Usage: kg_json_to_tsv.py  <inputKGfile.json> <outputFileLocationDirectory>
'''

import json
import csv as tsv
import datetime
import argparse
import sys

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

NEO4J_CHAR_LIMIT = 3000000


def no_space(original_str, keyslist, replace_str):
    """
    :param original_str: A string found in the keyslist
    :param keyslist: A list of keys found in the each of the two knowledge
                    graph dictionaries (nodes and edges)
    :param replace_str: A string to replace the original_str in the keyslist
    """
    # Find the location of the original string in the list
    index_str = keyslist.index(original_str)

    # Remove the original string from the list
    keyslist.remove(original_str)

    # Insert the new string where the original string used to be
    keyslist.insert(index_str, replace_str)
    return keyslist


def output_files(output_file_location, graph_type):
    """
    :param output_file_location: A string containing the path to
                                the TSV output directory
    :param graph_type: A string (either "nodes" or "edges") used to
                        name the TSV output files
    """
    returnlist = []

    # If the output file location name ends with a "/" create
    # output file names without adding in a "/"
    # Otherwise, add a "/" to the end of the output file location
    if output_file_location[len(output_file_location) - 1] == "/":
        output_file = output_file_location + graph_type + ".tsv"
        output_file_header = output_file_location + graph_type + "_header.tsv"
    else:
        output_file = output_file_location + "/" + graph_type + ".tsv"
        output_file_header = output_file_location + "/" + \
            graph_type + "_header.tsv"

    # Add the two output file names to a list that will be returned
    returnlist.append(output_file)
    returnlist.append(output_file_header)
    return returnlist


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def check_all_edges_have_same_set(edgekeys_list):
    """
    :param edgekeys_list: A list containing keys for an edge
    """
    # Supported_ls is a list of properties that edges can have
    supported_ls = ["edge label", "negated", "object", "provided by",
                    "publications", "publications info",
                    "relation", "relation curie", "subject", "update date",
                    "simplified relation curie","simplified relation",
                    "simplified edge label"]
    for edgelabel in edgekeys_list:
        if edgelabel not in supported_ls:
            raise ValueError("edge label not in supported list: " + edgelabel)


def truncate_node_synonyms_if_too_large(node_synonym_field, node_id):
    """
    Truncates a node's list of synonyms if it's too large for Neo4j. (Neo4j apparently cannot 'read a field larger than
    buffer size 4194304' - see Github issue #460).
    """
    if len(json.dumps(node_synonym_field)) > NEO4J_CHAR_LIMIT:
        print("warning: truncating 'synonym' field on node {} because it's too big for neo4j".format(node_id), file=sys.stderr)
        return node_synonym_field[0:20]  # Only include the first 20 synonyms
    else:
        return node_synonym_field


def shorten_description_if_too_large(node_description_field, node_id):
    """
    Truncates a node's description if it's too large for Neo4j. (Neo4j apparently cannot 'read a field larger than
    buffer size 4194304' - see Github issue #460).
    """
    if len(node_description_field) > NEO4J_CHAR_LIMIT:
        print("warning: truncating 'description field on node {} because it's too big for neo4j".format(node_id), file=sys.stderr)
        return str(list(node_description_field)[0:NEO4J_CHAR_LIMIT]).replace("[", "").replace("]", "").replace("', '", "").replace("'", "")
    else:
        return node_description_field


def nodes(graph, output_file_location):
    """
    :param graph: A dictionary containing KG2
    :param output_file_location: A string containing the
                                path to the TSV output directory
    """
    # Generate list of output file names for the nodes TSV files
    nodes_file = output_files(output_file_location, "nodes")

    # Create dictionary of nodes from KG2
    nodes = graph["nodes"]

    # Open output TSV files
    tsvfile = open(nodes_file[0], 'w+')
    tsvfile_h = open(nodes_file[1], 'w+')

    # Set loop (node counter) to zero
    loop = 0

    # Set up TSV files to be written to
    tsvwrite = tsv.writer(tsvfile, delimiter="\t",
                          quoting=tsv.QUOTE_MINIMAL)
    tsvwrite_h = tsv.writer(tsvfile_h, delimiter="\t",
                            quoting=tsv.QUOTE_MINIMAL)

    # Set single loop to zero and get list of node properties, which will go
    # in the header, to compare other nodes to
    single_loop = 0
    for node in nodes:
        single_loop += 1
        if single_loop == 1:
            nodekeys_official = list(sorted(node.keys()))
            nodekeys_official.append("category label")

    for node in nodes:
        # Inrease node counter by one each loop
        loop += 1

        # Add all node property labels to a list in the same order
        nodekeys = list(sorted(node.keys()))
        nodekeys.append("category label")

        # Create list for values of node properties to be added to
        vallist = []

        # Set index in list of node properties to zero, to be iterated through
        key_count = 0
        for key in nodekeys:
            if key != nodekeys_official[key_count]:
                # Add a property from the header list of node properties
                # if it doesn't exist and make the value for that property " "
                nodekeys.insert(key_count, nodekeys_official[key_count])
                value = " "
            elif key == "synonym":
                value = truncate_node_synonyms_if_too_large(node[key], node['id'])
                value = str(value).replace("', '", "; ").replace("'", "").replace("[", "").replace("]", "")
            elif key == "publications":
                value = str(node[key]).replace("', '", "; ").replace("'", "").replace("[", "").replace("]", "")
            elif key == "description" and node[key] is not None:
                value = shorten_description_if_too_large(node[key], node['id'])
            else:
                # If the property does exist, assign the property value
                value = node[key]
            # Add the value of the property to the property value list
            vallist.append(value)

            # Increase the index count by one
            key_count += 1

        # Add the edge property labels to the edge header TSV file
        # But only for the first edge
        if loop == 1:
            nodekeys = no_space('provided by', nodekeys, 'provided_by')
            nodekeys = no_space('replaced by', nodekeys, 'replaced_by')
            nodekeys = no_space('creation date', nodekeys, 'creation_date')
            nodekeys = no_space('full name', nodekeys, 'full_name')
            nodekeys = no_space('update date', nodekeys, 'update_date')
            nodekeys = no_space('category label', nodekeys, ':LABEL')
            nodekeys = no_space('category label', nodekeys, 'category_label')
            nodekeys = no_space('id', nodekeys, 'id:ID')
            nodekeys = no_space('publications', nodekeys, "publications:string[]")
            nodekeys = no_space('synonym', nodekeys, "synonym:string[]")
            tsvwrite_h.writerow(nodekeys)
        tsvwrite.writerow(vallist)

    # Close the TSV files to prevent a memory leak
    tsvfile.close()
    tsvfile_h.close()


def limit_publication_info_size(key, pub_inf_dict):
    """
    :param key: A list containing keys for an edge
    :param pub_inf_dict: A dictionary containing the publications info fields
    """
    new_pub_inf_dict = {}

    # Dump the publications info dictionary into a string
    value_string = json.dumps(pub_inf_dict)

    # If the publications info dictionary is longer than 300000 characters
    # Limit the dicitionary to 6 pieces of publication info
    if len(value_string) > 300000:
        loop = 0
        for pub_key in pub_inf_dict:
            loop += 1
            if loop < 7:
                new_pub_inf_dict.update({pub_key: pub_inf_dict[pub_key]})
        pub_inf_dict = new_pub_inf_dict
    return pub_inf_dict


def edges(graph, output_file_location):
    """
    :param graph: A dictionary containing KG2
    :param output_file_location: A string containing the path to the
                                TSV output directory
    """
    # Generate list of output file names for the edges TSV files
    edges_file = output_files(output_file_location, "edges")

    # Create dictionary of edges from KG2
    edges = graph["edges"]

    # Open output TSV files
    tsvfile = open(edges_file[0], 'w+')
    tsvfile_h = open(edges_file[1], 'w+')

    # Set loop (edge counter) to zero
    loop = 0

    # Set up TSV files to be written to
    tsvwrite = tsv.writer(tsvfile, delimiter="\t", quoting=tsv.QUOTE_MINIMAL)
    tsvwrite_h = tsv.writer(tsvfile_h, delimiter="\t",
                            quoting=tsv.QUOTE_MINIMAL)
    for edge in edges:
        # Inrease edge counter by one each loop
        loop += 1

        # Add all edge property label to a list in the same order and test
        # to make sure they are the same
        edgekeys = list(sorted(edge.keys()))
        check_all_edges_have_same_set(edgekeys)

        # Add an extra property of "edge label" to the list so that edge_labels
        # can be a property and a label
        edgekeys.append('simplified edge label')
        edgekeys.append('subject')
        edgekeys.append('object')

        # Create list for values of edge properties to be added to
        vallist = []
        for key in edgekeys:
            # Add the value for each edge property to the value list
            # and limit the size of the publications info dictionary
            # to avoid Neo4j buffer size error
            value = edge[key]
            if key == "publications info":
                value = limit_publication_info_size(key, value)
            elif key == 'provided by':
                value = str(value).replace("', '", "; ").replace("['", "").replace("']", "")
            elif key == 'edge label':  # fix for issue number 473 (hyphens in edge labels)
                value = value.replace('-', '_').replace('(', '').replace(')', '')
            elif key == 'publications':
                value = str(value).replace("', '", "; ").replace("'", "").replace("[", "").replace("]", "")
            vallist.append(value)

        # Add the edge property labels to the edge header TSV file
        # But only for the first edge
        if loop == 1:
            edgekeys = no_space('publications info', edgekeys,
                                'publications_info')
            edgekeys = no_space('provided by', edgekeys, 'provided_by:string[]')
            edgekeys = no_space('relation curie', edgekeys, 'relation_curie')
            edgekeys = no_space('update date', edgekeys, 'update_date')
            edgekeys = no_space('simplified relation curie', edgekeys, 'simplified_relation_curie')
            edgekeys = no_space('simplified relation', edgekeys, 'simplified_relation')
            edgekeys = no_space('simplified edge label', edgekeys, 'simplified_edge_label')
            edgekeys = no_space('simplified edge label', edgekeys, 'edge_label:TYPE')
            edgekeys = no_space('edge label', edgekeys, 'edge_label')
            edgekeys = no_space('subject', edgekeys, ':START_ID')
            edgekeys = no_space('object', edgekeys, ':END_ID')
            edgekeys = no_space('publications', edgekeys, "publications:string[]")
            tsvwrite_h.writerow(edgekeys)
        tsvwrite.writerow(vallist)

    # Close the TSV files to prevent a memory leak
    tsvfile.close()
    tsvfile_h.close()


if __name__ == '__main__':
    print("Start time: ", date())
    parser = argparse.ArgumentParser()
    parser.add_argument("inputFile", type=str, help="Path to Knowledge Graph \
                        JSON File to Import")
    parser.add_argument("outputFileLocation", help="Path to Directory for Output\
                        TSV Files to Go", type=str)
    arguments = parser.parse_args()
    print("Start load: ", date())
    with open(arguments.inputFile) as json_file:
        graph = json.load(json_file)
        print("End load: ", date())
        print("Start nodes: ", date())
        output_file_location = arguments.outputFileLocation
        nodes(graph, output_file_location)
        print("Finish nodes: ", date())
        print("Start edges: ", date())
        edges(graph, output_file_location)
        print("Finish edges: ", date())
        json_file.close()
        print("Finish time: ", date())
