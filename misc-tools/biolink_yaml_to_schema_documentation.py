#!/usr/bin/env python3
'''Generates markdown documentation of the Translator Knowledge Graph from the Biolink model

   Usage:  ./biolink_yaml_to_schema_documentation.py biolink-model.yaml output.md
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


import argparse
import io
import jsonschema2md
import yaml


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(
        description='biolink_yaml_to_schema_documentation.py: analyzes the biolink-model.yaml file to generate a JSON representation of the Biolink KG schema.')
    arg_parser.add_argument('biolinkModelYamlLocalFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser


def read_file_to_string(local_file_name: str):
    with open(local_file_name, 'r') as myfile:
        file_contents_string = myfile.read()
    myfile.close()
    return file_contents_string


def safe_load_yaml_from_string(yaml_string: str):
    return yaml.safe_load(io.StringIO(yaml_string))


args = make_arg_parser().parse_args()
biolink_model_file_name = args.biolinkModelYamlLocalFile
output_file_name = args.outputFile

biolink_model = safe_load_yaml_from_string(read_file_to_string(biolink_model_file_name))
classes_info = biolink_model['classes']
entity_class_info = classes_info['entity']
entity_slot_names = entity_class_info['slots']
association_class_info = classes_info['association']
association_slot_names = association_class_info['slots']
named_thing_class_info = classes_info['named thing']
named_thing_slot_names = list(named_thing_class_info['slot_usage'].keys())
top_types = biolink_model['types']

master_schema = "http://json-schema.org/draft-07/schema#"

node_required = []

node_properties = dict()
schema_nodes = {'$schema': master_schema,
                'title': 'Node',
                'description': 'Biolink knowledge graph node',
                'properties': node_properties,
                'required': node_required}

edge_properties = dict()
schema_edges = {'$schema': master_schema,
                'title': 'Edge',
                'description': 'Biolink knowledge graph edge',
                'properties': edge_properties}

js2md_parser = jsonschema2md.Parser()


def get_properties(slot_names: str, class_info: dict) -> dict:
    properties = dict()
    slot_info_all = biolink_model['slots']
    for slot_name in slot_names:
        slot_info = slot_info_all[slot_name]
        description = slot_info.get('description', '').replace('\n', '').replace(' * ', '')
        slot_uri = slot_info.get('slot_uri', None)
        multivalued = slot_info.get('multivalued', False)
        required = slot_info.get('required', False)
        slot_usage_info = class_info.get('slot_usage', {})
        if slot_name in slot_usage_info:
            slot_usage_info_individual = slot_usage_info[slot_name]
            if 'required' in slot_usage_info_individual:
                required = slot_usage_info_individual['required']
        if slot_info.get('identifier', False):
            slot_type = "uriorcurie"
        elif slot_info.get('range', None) is not None:
            slot_range_type = slot_info['range']
            if top_types.get(slot_range_type, None) is not None:
                slot_type = top_types[slot_range_type]['typeof']
            elif classes_info.get(slot_range_type, None) is not None:
                if classes_info[slot_range_type].get('values_from', None) is not None:
                    slot_type = classes_info[slot_range_type]['values_from']
                else:
                    slot_type = slot_range_type
            else:
                slot_type = slot_range_type
        elif slot_uri is not None:
            slot_type = "string"
        else:
            slot_type = 'unknown'
        if slot_type == 'named thing':
            slot_type = 'node-id'
        if multivalued:
            slot_type = [slot_type]
        name = slot_name.replace(' ', '_')
        if slot_uri is not None:
            description += '; semantic URI: ' + slot_uri
        description += '; '
        if required:
            description += '**'
        description += 'required: ' + str(required)
        if required:
            description += '**'
        properties[name] = {'type': slot_type,
                            'description': description,
                            'required': required}
    return properties


entity_properties = get_properties(entity_slot_names, entity_class_info)
named_thing_properties = get_properties(named_thing_slot_names, named_thing_class_info)
node_properties = entity_properties.copy()
node_properties.update(named_thing_properties)
association_properties = get_properties(association_slot_names, association_class_info)
edge_properties = entity_properties.copy()
edge_properties.update(association_properties)

schema_nodes['properties'] = node_properties
schema_nodes['required'] = list(set([property_name for property_name, property_dict in node_properties.items() if property_dict['required']]))

nodes_md = js2md_parser.parse_schema(schema_nodes)

schema_edges['properties'] = edge_properties
schema_nodes['required'] = list(set([property_name for property_name, property_dict in edge_properties.items() if property_dict['required']]))

edges_md = js2md_parser.parse_schema(schema_edges)

with open(output_file_name, 'w') as output_file:
    print(('# Translator Project knowledge graph schema\n'
           '## Generated from the Biolink model version ' + biolink_model['version'] + '\n'
           '## by the script [`biolink_yaml_to_schema_documentation.py`](biolink_yaml_to_schema_documentation.py)' + '\n'),
          file=output_file)
    for line in nodes_md + edges_md:
        print(line, file=output_file)
    print(('# Postscript\n'
           'To see an example JSON serialization of a simple KG, refer to the document '
           '[KGX Format](https://github.com/biolink/kgx/blob/master/specification/kgx-format.md).'),
          file=output_file)
