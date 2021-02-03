#!/usr/bin/env python3

''' Parses KG2 TSV files to the mediKanren CSV format
    Usage: tsv-to-medikanren-csv.py  <inputDir> <outputDir>
'''

import csv
import sys
import argparse
import re

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


csv.field_size_limit(sys.maxsize)


def output_file_names(directory: str):
    directory = directory.strip("/") + "/"

    filebase = directory + "rtx_kg2."

    return {"nodes": [filebase + "node.tsv", filebase + "nodeprop.tsv"],
            "edges": [filebase + "edge.tsv", filebase + "edgeprop.tsv"]}


def input_file_names(directory: str):
    directory = directory.strip("/") + "/"

    return {"nodes": [directory + "nodes.tsv", directory + "nodes_header.tsv"],
            "edges": [directory + "edges.tsv", directory + "edges_header.tsv"]}


def make_tsv_list(stringifiedlist: str):
    prop_value_list = stringifiedlist.split(";")
    prop_value_string = '('
    for prop_string in prop_value_list:
        if prop_value_string[-1] != "(":
            prop_value_string += " "
        if len(prop_string) > 0:
            prop_value_string += '""' + prop_string.strip() + '""'
    if len(prop_string) > 1:
        prop_value_string += ')'
        stringifiedlist = prop_value_string

    return stringifiedlist


def nodes(nodes_input, nodes_output):
    nodes_o = open(nodes_output[0], 'w+')
    output_nodes = csv.writer(nodes_o, delimiter="\t")
    output_nodes.writerow([":ID"])

    nodes_prop_o = open(nodes_output[1], 'w+')
    nodes_prop_o.write(":ID\tpropname\tvalue\n")

    header = []
    with open(nodes_input[1]) as nodes_header:
        for line in csv.reader(nodes_header, delimiter="\t"):
            header = line

    id_index = header.index("id:ID")

    with open(nodes_input[0]) as nodes:
        for line in csv.reader(nodes, delimiter="\t"):
            id = line[id_index]
            output_nodes.writerow([id])

            if "\t" in id:
                id = '"' + id + '"'

            index = 0

            for propvalue in line:
                propfull = header[index]
                prop = propfull.split(":")[0]

                if ":string[]" in propfull:
                    propvalue = make_tsv_list(propvalue)

                if len(prop) > 0 and len(propvalue) > 0:
                    if "\t" in propvalue or '"' in propvalue or '\n' in propvalue:
                        propvalue = '"' + re.sub(r'\n+', '\n', propvalue.replace('"', "'")).strip() + '"'
                    proplist = id + "\t" + prop + "\t" + propvalue + "\n"
                    nodes_prop_o.write(proplist)
                index += 1

    nodes_o.close()
    nodes_prop_o.close()


def edges(edges_input, edges_output):
    edges_o = open(edges_output[0], 'w+')
    output_edges = csv.writer(edges_o, delimiter="\t")
    output_edges.writerow([":ID", ":START", ":END"])

    edges_prop_o = open(edges_output[1], 'w+')
    edges_prop_o.write(":ID\tpropname\tvalue\n")

    header = []
    with open(edges_input[1]) as edges_header:
        for line in csv.reader(edges_header, delimiter="\t"):
            header = line

    start_index = header.index(":START_ID")
    end_index = header.index(":END_ID")
    with open(edges_input[0]) as edges:
        line_id = 0
        for line in csv.reader(edges, delimiter="\t"):
            source_id = line[start_index]
            target_id = line[end_index]
            output_edges.writerow([line_id,
                                   source_id,
                                   target_id])

            index = 0

            for propvalue in line:
                propfull = header[index]
                prop = propfull.split(":")[0]
                if ":string[]" in propfull:
                    propvalue = make_tsv_list(propvalue)

                if len(prop) > 0 and len(propvalue) > 0:
                    if "\t" in propvalue or '"' in propvalue or '\n' in propvalue:
                        propvalue = '"' + re.sub(r'\n+', '\n', propvalue.replace('"', "'")).strip() + '"'
                    proplist = str(line_id) + "\t" + prop + "\t" + propvalue + "\n"
                    edges_prop_o.write(proplist)
                index += 1

            line_id += 1

    edges_o.close()
    edges_prop_o.close()


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputDir", type=str)
    parser.add_argument("outputDir", type=str)

    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()

    input_file_names = input_file_names(args.inputDir)
    output_file_names = output_file_names(args.outputDir)

    nodes(input_file_names["nodes"], output_file_names["nodes"])
    edges(input_file_names["edges"], output_file_names["edges"])
