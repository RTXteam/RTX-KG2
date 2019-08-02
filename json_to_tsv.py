#!/usr/bin/env python3

''' Creates a set of tsv files for importing into Neo4j from KG2 JSON

    Usage: json_to_tsv.py --inputFile <inputKGfile.json>
                        --outputFileLocation <directory>
'''

import json
import csv as tsv
import neo4j
import collections
import datetime
import argparse
import ijson


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def no_space(original_str, keyslist, replace_str):
    """
    :param original_str: A string found in the keyslist
    :param keyslist: A list of keys found in the each of the two knowledge
                    graph dictionaries (nodes and edges)
    :param replace_str: A string to replace the original_str in the keyslist
    """
    index_str = keyslist.index(original_str)
    keyslist.remove(original_str)
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
    if output_file_location[len(output_file_location) - 1] == "/":
        output_file = output_file_location + graph_type + ".tsv"
        output_file_header = output_file_location + graph_type + "_header.tsv"
    else:
        output_file = output_file_location + "/" + graph_type + ".tsv"
        output_file_header = output_file_location + "/" + \
            graph_type + "_header.tsv"
    returnlist.append(output_file)
    returnlist.append(output_file_header)
    return returnlist


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def all_egdes_have_same_set(edgekeys_list):
    """
    :param edgekeys_list: A list containing keys for an edge
    """
    supported_ls = ["edge label", "negated", "object", "provided by",
                    "publications", "publications info",
                    "relation", "relation curie", "subject", "update date"]
    list_count = 0
    for edgelabel in edgekeys_list:
        if edgelabel not in supported_ls:
            edgekeys_list.remove(edgelabel)

    return edgekeys_list


def nodes(graph, output_file_location):
    """
    :param file: A string containing the path to the
                knowledge graph json file
    :param output_file_location: A string containing the
                                path to the TSV output directory
    """
    nodes = []
    nodes_file = output_files(output_file_location, "nodes")
    nodes = graph["nodes"]
    tsvfile = open(nodes_file[0], 'w+')
    tsvfile_h = open(nodes_file[1], 'w+')
    loop = 0
    tsvwrite = tsv.writer(tsvfile, delimiter="\t",
                          quoting=tsv.QUOTE_MINIMAL)
    tsvwrite_h = tsv.writer(tsvfile_h, delimiter="\t",
                            quoting=tsv.QUOTE_MINIMAL)
    single_loop = 0
    for node in nodes:
        single_loop += 1
        if single_loop == 1:
            nodekeys_official = list(sorted(node.keys()))
            nodekeys_official.append("category label")

    for node in nodes:
        loop += 1
        nodekeys = list(sorted(node.keys()))
        nodekeys.append("category label")
        vallist = []
        key_count = 0
        for key in nodekeys:
            if key != nodekeys_official[key_count]:
                nodekeys.insert(key_count, nodekeys_official[key_count])
                value = " "
            else:
                value = node[key]
            vallist.append(value)
            key_count += 1
        if loop == 1:
            nodekeys = no_space('provided by', nodekeys, 'provided_by')
            nodekeys = no_space('replaced by', nodekeys, 'replaced_by')
            nodekeys = no_space('creation date', nodekeys, 'creation_date')
            nodekeys = no_space('full name', nodekeys, 'full_name')
            nodekeys = no_space('update date', nodekeys, 'update_date')
            nodekeys = no_space('category label', nodekeys, ':LABEL')
            nodekeys = no_space('category label', nodekeys, 'category_label')
            nodekeys = no_space('id', nodekeys, 'id:ID')
            tsvwrite_h.writerow(nodekeys)
        tsvwrite.writerow(vallist)
    tsvfile.close()
    tsvfile_h.close()


def limit_publication_info_size(key, pub_inf_dict):
    """
    :param key: A list containing keys for an edge
    :param pub_inf_dict: A dictionary containing the publications info fields
    """
    new_pub_inf_dict = {}
    value_string = json.dumps(pub_inf_dict)
    if len(value_string) > 300000:
        loop = 0
        for pub_key in pub_inf_dict:
            loop += 1
            if loop < 7:
                new_pub_inf_dict.update({pub_key: pub_inf_dict[pub_key]})
        pub_inf_dict = new_pub_inf_dict
    return pub_inf_dict


def edges(file, output_file_location):
    """
    :param file: A string containing the path to the knowledge
                graph json file
    :param output_file_location: A string containing the path to the
                                TSV output directory
    """
    edges = []
    edges_file = output_files(output_file_location, "edges")
    edges = graph["edges"]
    new_file = output_file_location + "chembl_edges.json"
    tsvfile = open(edges_file[0], 'w+')
    tsvfile_h = open(edges_file[1], 'w+')
    loop = 0
    tsvwrite = tsv.writer(tsvfile, delimiter="\t", quoting=tsv.QUOTE_MINIMAL)
    tsvwrite_h = tsv.writer(tsvfile_h, delimiter="\t",
                            quoting=tsv.QUOTE_MINIMAL)
    predicate_label = []
    for edge in edges:
        loop += 1
        edgekeys = list(sorted(edge.keys()))
        edgekeys = all_egdes_have_same_set(edgekeys)
        edgekeys.append('edge label')
        vallist = []
        for key in edgekeys:
            value = edge[key]
            if key == "publications info":
                value = limit_publication_info_size(key, value)
            vallist.append(value)
        if loop == 1:
            edgekeys = no_space('publications info', edgekeys,
                                'publications_info')
            edgekeys = no_space('provided by', edgekeys, 'provided_by')
            edgekeys = no_space('relation curie', edgekeys, 'relation_curie')
            edgekeys = no_space('update date', edgekeys, 'update_date')
            edgekeys = no_space('edge label', edgekeys, 'edge_label:TYPE')
            edgekeys = no_space('edge label', edgekeys, 'edge_label')
            edgekeys = no_space('subject', edgekeys, ':START_ID')
            edgekeys = no_space('object', edgekeys, ':END_ID')
            tsvwrite_h.writerow(edgekeys)
        tsvwrite.writerow(vallist)
    tsvfile.close()
    tsvfile_h.close()

if __name__ == '__main__':
    print("Start time: ", date())
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputFile", type=str, help="Path to Knowledge Graph \
                        JSON File to Import",
                        nargs=1, required=True)
    parser.add_argument("--outputFileLocation", help="Path to Directory for Output\
                        TSV Files to Go", type=str, nargs=1, required=True)
    arguments = parser.parse_args()
    print("Start load: ", date())
    with open(arguments.inputFile[0]) as json_file:
        graph = json.load(json_file)
        print("End load: ", date())
        print("Start nodes: ", date())
        nodes(graph, arguments.outputFileLocation[0])
        print("Finish nodes: ", date())
        print("Start edges: ", date())
        edges(graph, arguments.outputFileLocation[0])
        print("Finish edges: ", date())
        json_file.close()
        print("Finish time: ", date())
