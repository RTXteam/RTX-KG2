#!/usr/bin/env python3
'''save_owl_datatype_properties.py: Saves a JSON file with the information from
   the owl:DatatypeProperty field in select TTL/OWL files.

   Usage: save_owl_datatype_properties.py [--test] [owlFiles]
           --outputFile <outputFile.json>
'''

import xmltodict
import json
import argparse

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def get_args():
    description = 'save_owl_datatype_properties.py: saves a JSON file with \
                   the information from the owl:DatatypeProperty field in \
                   select TTL/OWL files'
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('--outputFile',
                            type=str,
                            nargs='?')
    arg_parser.add_argument('owlFiles', type=str, nargs='+')
    return arg_parser.parse_args()


def extract_datatype_property(node, datatype):
    value = node.get(datatype, {})
    if isinstance(value, dict):
        return value.get('#text', None)
    else:
        values = []
        for element in value:
            values.append(element.get('#text', None))
        return values


def get_ontology_prefix(iri: str):
    base_ontology_iri = 'http://purl.bioontology.org/ontology/'
    return iri.replace(base_ontology_iri, '').replace('/', '')


def process_rdf_file(file: dict):
    datatype_properties = file['owl:DatatypeProperty']
    nodes = file['owl:NamedIndividual']
    ontology_iri = file['@xml:base']
    ontology_prefix = get_ontology_prefix(ontology_iri)
    sty_ontology_iri = 'http://purl.bioontology.org/ontology/STY/'
    node_descriptions = file['rdf:Description']
    about = '@rdf:about'

    datatypes = []
    nodes_attributes = dict()

    iri_to_id = {}

    for node_description in node_descriptions:
        node_id = node_description['skos:notation']['#text']
        iri_to_id[node_description[about]] = node_id

    for datatype_property in datatype_properties:
        datatypes.append(datatype_property[about].replace(ontology_iri, ''))
    for node in nodes:
        prefix_colon = ontology_prefix + ':'
        raw_id = iri_to_id[node[about]].replace(prefix_colon, '')
        node_id = prefix_colon + raw_id
        if sty_ontology_iri in node_id:
            continue
        node_attributes = dict()
        for datatype in datatypes:
            node_attributes[datatype] = extract_datatype_property(node,
                                                                  datatype)
        nodes_attributes[node_id] = node_attributes

    return nodes_attributes


if __name__ == '__main__':
    args = get_args()
    owl_files = args.owlFiles
    file_properties = dict()
    for owl_file in owl_files:
        with open(owl_file, 'r') as owl_file_open:
            owl_dict = xmltodict.parse(owl_file_open.read())
            file = owl_dict['rdf:RDF']
            file_name_as_ttl = owl_file.replace('.owl', '.ttl').split('/')[-1]
            file_properties[file_name_as_ttl] = process_rdf_file(file)
    with open(args.outputFile, 'w') as output_file:
        output_file.write(json.dumps(file_properties,
                                     indent=4,
                                     sort_keys=True))
