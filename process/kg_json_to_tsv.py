#!/usr/bin/env python3

''' Creates a set of tsv files for importing into Neo4j from KG2 JSON

    Usage: kg_json_to_tsv.py  <inputKGfile.json> <outputFileLocationDirectory>
'''

import json
import csv as tsv
import datetime
import argparse
import sys
import yaml
import kg2_util

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood', 'Liliana Acevedo']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

NEO4J_CHAR_LIMIT = 3000000


def get_args():
    arg_parser = argparse.ArgumentParser(description='kg_json_to_tsv.py: \
                                         converts KG2 JSON to TSV form for Neo4j import')
    arg_parser.add_argument("inputNodesFile", type=str, help="Path to Knowledge Graph Nodes JSON File to Import")
    arg_parser.add_argument("inputEdgesFile", type=str, help="Path to Knowledge Graph Edges JSON File to Import")
    arg_parser.add_argument("kg2ProvidedByCurieToInforesCurieFile", type=str, help="kg2-provided-by-curie-to-infores-curie.yaml")
    arg_parser.add_argument("outputFileLocation", help="Path to Directory for Output TSV Files to Go", type=str)
    return arg_parser.parse_args()


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
    supported_ls = ["relation_label",
                    "negated",
                    "object",
                    "primary_knowledge_source",
                    "publications",
                    "publications_info",
                    "source_predicate",
                    "subject",
                    "update_date",
                    "predicate",
                    "predicate_label",
                    "id",
                    "qualified_predicate",
                    "qualified_object_aspect",
                    "qualified_object_direction",
                    "domain_range_exclusion",
                    "knowledge_level",
                    "agent_type"]
    for edgelabel in edgekeys_list:
        if edgelabel not in supported_ls:
            raise ValueError("relation_label not in supported list: " + edgelabel)


def truncate_node_synonyms_if_too_large(node_synonym_field, node_id):
    """
    Truncates a node's list of synonyms if it's too large for Neo4j. (Neo4j apparently cannot 'read a field larger than
    buffer size 4194304' - see Github issue #460).
    Replaces any newlines with spaces - see Github issue #1076.
    """
    if len(json.dumps(node_synonym_field)) > NEO4J_CHAR_LIMIT:
        print("warning: truncating 'synonym' field on node {} because it's too big for neo4j".format(node_id), file=sys.stderr)
        return [synonym.replace("\n"," ") for synonym in node_synonym_field[0:20] if synonym is not None]  # Only include the first 20 synonyms
    else:
        return [synonym.replace("\n"," ") for synonym in node_synonym_field if synonym is not None]


def shorten_description_if_too_large(node_description_field, node_id):
    """
    Truncates a node's description if it's too large for Neo4j. (Neo4j apparently cannot 'read a field larger than
    buffer size 4194304' - see Github issue #460).
    Also replaces newlines with spaces - see Github issue #1076.
    """
    if len(node_description_field) > NEO4J_CHAR_LIMIT:
        print("warning: truncating 'description field on node {} because it's too big for neo4j".format(node_id), file=sys.stderr)
        return str(list(node_description_field)[0:NEO4J_CHAR_LIMIT]).replace("[", "").replace("]", "").replace("', '", "").replace("'", "").replace("\n"," ")
    else:
        return node_description_field.replace("\n"," ")


def check_all_nodes_have_same_set(nodekeys_list):
    """
    :param nodekeys_list: A list containing keys for a node
    """
    supported_node_keys = ["category",
                           "category_label",
                           "creation_date",
                           "id",
                           "iri",
                           "name",
                           "full_name",
                           "description",
                           "synonym",
                           "publications",
                           "update_date",
                           "deprecated",
                           "replaced_by",
                           "provided_by",
                           "has_biological_sequence"]
    for node_label in nodekeys_list:
        assert node_label in supported_node_keys, f"Node label not in supported list: {node_label}"

    
def nodes(input_nodes_file, provided_by_infores_map, output_file_location):
    """
    :param input_file: The input file
    :param output_file_location: A string containing the
                                path to the TSV output directory
    """
    # Generate list of output file names for the nodes TSV files
    nodes_file = output_files(output_file_location, "nodes")

    # Open output TSV files
    # To address #278, added newline='' per https://docs.python.org/3/library/csv.html#id1
    tsvfile = open(nodes_file[0], 'w+', newline='')
    tsvfile_h = open(nodes_file[1], 'w+', newline='')

    # Set up TSV files to be written to
    tsvwrite = tsv.writer(tsvfile, delimiter="\t",
                          quoting=tsv.QUOTE_MINIMAL)
    tsvwrite_h = tsv.writer(tsvfile_h, delimiter="\t",
                            quoting=tsv.QUOTE_MINIMAL)

    # Create infores map to verify knowledge_source with
    with open(provided_by_infores_map, 'r') as yaml_file:
        ir_map = yaml.safe_load(yaml_file)
        map_ks_curie_to_infores_curie = {k: d['infores_curie'] for k, d in ir_map.items()}

    input_nodes_jsonlines_info = kg2_util.start_read_jsonlines(input_nodes_file)
    input_nodes = input_nodes_jsonlines_info[0]

    node_ctr = 0
    for node in input_nodes:
        node_ctr += 1
        if node_ctr % 1000000 == 0:
            print(f"Processing node: {node_ctr}")

        # Add all node property labels to a list and check if they are supported
        knowledge_source = node.get('knowledge_source')
        if knowledge_source is not None:
            assert type(knowledge_source)==str, "expected a string type"
            knowledge_source_infores = map_ks_curie_to_infores_curie.get(knowledge_source)
            if knowledge_source_infores is not None:
                provided_by = node.get('provided_by')
                if provided_by is not None:
                    assert type(provided_by)==list, "expected a list type"
                    provided_by = list(set(provided_by + [knowledge_source_infores]))
                    node['provided_by'] = provided_by
                else:
                    node['provided_by'] = [knowledge_source_infores]
            del node['knowledge_source']

        nodekeys = list(sorted(node.keys()))
        check_all_nodes_have_same_set(nodekeys)
        nodekeys.append("category")

        vallist = []

        for key in nodekeys:
            assert key in nodekeys, key
            if key == "synonym":
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
            if type(value) == str:
                value = value.replace('\t', ' ').replace('\n', ' ').replace('\r', ' ')
            vallist.append(value)

        if node_ctr == 1:
            nodekeys = no_space('id', nodekeys, 'id:ID')
            nodekeys = no_space('publications', nodekeys, "publications:string[]")
            nodekeys = no_space('synonym', nodekeys, "synonym:string[]")
            nodekeys = no_space('category', nodekeys, ':LABEL')
            tsvwrite_h.writerow(nodekeys)

        tsvwrite.writerow(vallist)

    # Close all of the files to prevent a memory leak
    kg2_util.end_read_jsonlines(input_nodes_jsonlines_info)
    tsvfile.close()
    tsvfile_h.close()


def limit_publication_info_size(key, pub_inf_dict):
    """
    :param key: A list containing keys for an edge
    :param pub_inf_dict: A dictionary containing the publications_info fields
    """
    new_pub_inf_dict = {}

    # Dump the publications_info dictionary into a string
    value_string = json.dumps(pub_inf_dict)

    # If the publications_info dictionary is longer than 300000 characters
    # Limit the dicitionary to 6 pieces of publication info
    if len(value_string) > 300000:
        loop = 0
        for pub_key in pub_inf_dict:
            loop += 1
            if loop < 7:
                new_pub_inf_dict.update({pub_key: pub_inf_dict[pub_key]})
        pub_inf_dict = new_pub_inf_dict
    return pub_inf_dict


def edges(input_edges_file, output_file_location):
    """
    :param input_file: The input file
    :param output_file_location: A string containing the path to the
                                TSV output directory
    """
    # Generate list of output file names for the edges TSV files
    edges_file = output_files(output_file_location, "edges")

    # Open output TSV files
    # To address #278, added newline='' per https://docs.python.org/3/library/csv.html#id1
    tsvfile = open(edges_file[0], 'w+', newline='')
    tsvfile_h = open(edges_file[1], 'w+', newline='')

    # Set up TSV files to be written to
    tsvwrite = tsv.writer(tsvfile, delimiter="\t", quoting=tsv.QUOTE_MINIMAL)
    tsvwrite_h = tsv.writer(tsvfile_h, delimiter="\t",
                            quoting=tsv.QUOTE_MINIMAL)

    input_edges_jsonlines_info = kg2_util.start_read_jsonlines(input_edges_file)
    input_edges = input_edges_jsonlines_info[0]

    edge_ctr = 0
    for edge in input_edges:
        edge_ctr += 1
        if edge_ctr % 1000000 == 0:
            print(f"Processing edge: {edge_ctr}")

        # Add all edge property label to a list in the same order and test
        # to make sure they are the same
        edgekeys = list(sorted(edge.keys()))
        check_all_edges_have_same_set(edgekeys)

        # Add an extra property of "predicate" to the list so that predicates
        # can be a property and a label
        edgekeys.append('predicate')
        edgekeys.append('subject')
        edgekeys.append('object')

        # Create list for values of edge properties to be added to
        vallist = []
        for key in edgekeys:
            # Add the value for each edge property to the value list
            # and limit the size of the publications_info dictionary
            # to avoid Neo4j buffer size error
            value = edge.get(key)
            if key == "publications_info":
                value = limit_publication_info_size(key, value)
            elif key == 'relation_label':  # fix for issue number 473 (hyphens in relation_labels)
                value = value.replace('-', '_').replace('(', '').replace(')', '')
            elif key == 'publications':
                value = str(value).replace("', '", "; ").replace("'", "").replace("[", "").replace("]", "")
            vallist.append(value)

        # Add the edge property labels to the edge header TSV file
        # But only for the first edge
        if edge_ctr == 1:
            edgekeys = no_space('predicate', edgekeys, 'predicate:TYPE')
            edgekeys = no_space('subject', edgekeys, ':START_ID')
            edgekeys = no_space('object', edgekeys, ':END_ID')
            edgekeys = no_space('publications', edgekeys, "publications:string[]")
            tsvwrite_h.writerow(edgekeys)
        tsvwrite.writerow(vallist)

    # Close all of the files to prevent a memory leak
    kg2_util.end_read_jsonlines(input_edges_jsonlines_info)
    tsvfile.close()
    tsvfile_h.close()


if __name__ == '__main__':
    print(f"Start time: {date()}")
    args = get_args()
    input_nodes_file = args.inputNodesFile
    input_edges_file = args.inputEdgesFile
    provided_by_infores_map = args.kg2ProvidedByCurieToInforesCurieFile
    output_file_location = args.outputFileLocation
    
    print("Start nodes: ", date())
    nodes(input_nodes_file, provided_by_infores_map, output_file_location)
    print("Finish nodes: ", date())
    print("Start edges: ", date())
    edges(input_edges_file, output_file_location)
    print("Finish edges: ", date())
    print("Finish time: ", date())
