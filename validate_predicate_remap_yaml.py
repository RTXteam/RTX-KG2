#!/usr/bin/env python3
'''Checks the file `predicate-remap.yaml` for correctness.  This script should
   be run each time `predicate-remap.yaml` or `curies-to-urls-map.yaml` is
   changed.

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
import kg2_util
import yaml
from collections import defaultdict
import json

BIOLINK_SLOT_TYPES_SKIP = {"biolink:has_attribute",
                           "biolink:synonym",
                           "biolink:has_attribute_type"}

relation_mapping_exceptions = {"SEMMEDDB:diagnoses"}

def make_arg_parser():
    arg_parser = argparse.ArgumentParser(
        description='validate_predicate_remap_yaml.py: checks the file `predicate-remap.yaml` for correctness.')
    arg_parser.add_argument('curiesToURLsMapFile', type=str)
    arg_parser.add_argument('predicateRemapFile', type=str)
    arg_parser.add_argument('biolinkModelYamlURL', type=str)
    arg_parser.add_argument('biolinkModelYamlLocalFile', type=str)
    return arg_parser


def convert_biolink_yaml_association_to_predicate(association: str) -> str:
    return 'biolink:' + association.replace(',', '').replace(' ', '_')


def create_biolink_to_external_mappings(biolink_model: dict, mapping_heirarchy: list) -> dict:
    # biolink_to_external[biolink relation][mapterm]= list([externals])
    biolink_mixins = list()
    biolink_to_external_mappings = dict()
    inverted_relations = []
    for relation, relation_info in biolink_model['slots'].items():
        predicate_str = convert_biolink_yaml_association_to_predicate(relation)
        mixin = relation_info.get('mixin', False)
        if mixin == True:
            biolink_mixins.append(predicate_str)
            continue
        is_a_type = relation_info.get('is_a', '')
        if is_a_type in ['node property', 'association slot', 'aggregate statistic']:
            continue
        domain_type = relation_info.get('domain', '')
        if domain_type in ['quantity value', 'attribute']:
            continue
        if biolink_to_external_mappings.get(predicate_str, None) is None:
            biolink_to_external_mappings[predicate_str] = defaultdict(lambda: [])
        inverted_relation = relation_info.get('inverse', None)
        annotations = relation_info.get('annotations', dict())
        # Adjustment due to biolink issue #808
        tag = str
        if isinstance(annotations, list):
            tags = list()
            for annotation in annotations:
                tag = annotation.get('tag', None)
                tags.append(tag)
            if len(tags) > 1:
                print('Error:', predicate_str, 'has multiple tags:', tags + '. Exiting')
                exit(1)
            tag = tags[0]
        else:
            tag = annotations.get('tag', None)
        for mapping_term in mapping_hierarchy:
            mapping_value = relation_info.get(mapping_term, [])
            if mapping_value is None:
                mapping_value = []
            mappings = list(map(lambda x: x.lower(), mapping_value))
            biolink_to_external_mappings[predicate_str][mapping_term] += mappings
            if inverted_relation is not None and len(mappings) != 0:
                biolink_curie = convert_biolink_yaml_association_to_predicate(inverted_relation)
                if biolink_to_external_mappings.get(biolink_curie, None) is None:
                    biolink_to_external_mappings[biolink_curie] = defaultdict(lambda: [])
                existing_list = biolink_to_external_mappings[biolink_curie][mapping_term]
                existing_list += list(map(lambda x: x.lower(), mappings))
                biolink_to_external_mappings[biolink_curie][mapping_term] = existing_list
                if tag != "biolink:canonical_predicate":
                    inverted_relations.append(predicate_str)
    for inverted_relation in inverted_relations:
        biolink_to_external_mappings.pop(inverted_relation, None)
    biolink_to_external_mappings['skos:closeMatch'] = defaultdict(lambda: [])

    # See Issue #63 for why we are doing this
    try:
       biolink_to_external_mappings['biolink:subclass_of']['narrow_mappings'].remove("umls:rb")
    except ValueError:
       print('UMLS:RB work around no longer necessary')
    return biolink_to_external_mappings, biolink_mixins, inverted_relations


args = make_arg_parser().parse_args()
curies_to_urls_map_file_name = args.curiesToURLsMapFile
predicate_remap_file_name = args.predicateRemapFile
biolink_model_url = args.biolinkModelYamlURL
biolink_model_file_name = args.biolinkModelYamlLocalFile

curies_to_url_map_data = kg2_util.safe_load_yaml_from_string(
    kg2_util.read_file_to_string(curies_to_urls_map_file_name))
curies_to_url_map_data_bidir = {next(iter(listitem.keys(
))) for listitem in curies_to_url_map_data['use_for_bidirectional_mapping']}

kg2_util.download_file_if_not_exist_locally(
    biolink_model_url, biolink_model_file_name)

biolink_model = kg2_util.safe_load_yaml_from_string(
    kg2_util.read_file_to_string(biolink_model_file_name))

mapping_hierarchy = ["exact_mappings", "close_mappings", "narrow_mappings", "broad_mappings", "related_mappings"]  # TODO: determine correct order of mappings

biolink_to_external_mappings, biolink_mixins, inverted_relations = create_biolink_to_external_mappings(
    biolink_model, mapping_hierarchy)

external_to_biolink_mappings = dict()
for biolink_curie, mappings in biolink_to_external_mappings.items():
    for mapping_term, external_curies in mappings.items():
        for external_curie in external_curies:
            if external_to_biolink_mappings.get(external_curie, None) is None:
                external_to_biolink_mappings[external_curie] = defaultdict(lambda: set())
            if biolink_curie not in BIOLINK_SLOT_TYPES_SKIP:
                external_to_biolink_mappings[external_curie][mapping_term].add(biolink_curie)

pred_info = yaml.safe_load(open(predicate_remap_file_name, 'r'))

for relation, instruction_dict in pred_info.items():
    command, subinfo = next(iter(instruction_dict.items()))
    assert len(instruction_dict) == 1, relation
    if command == 'keep' and not relation.startswith('biolink:'):
        if not relation.startswith('BSPO:') and \
           not relation.startswith('FMA:') and \
           not relation.startswith('UBERON:'):
            assert False, relation
        else:
            command = 'rename'
            subinfo = ['coexists_with', 'biolink:coexists_with']
    if subinfo is not None:
        predicate = subinfo[1]
        if not predicate.startswith('biolink:') and not predicate.startswith('skos:closeMatch'):
            if predicate.startswith('FMA:') or \
               predicate.startswith('BSPO:') or \
               predicate.startswith('UBERON:'):
                command = 'rename'
                subinfo = ['coexists_with', 'biolink:coexists_with']
            else:
                assert False
    if subinfo is not None:
        assert subinfo[1] not in biolink_mixins, (relation, subinfo[1], {'Mixins': biolink_mixins})
        assert subinfo[1] not in inverted_relations, (relation, subinfo[1], {'Inverted Relations': inverted_relations})
        assert subinfo[1] in biolink_to_external_mappings, (relation, subinfo[1])

        allowed_biolink_curies_set = set()
        biolink_term_externals = external_to_biolink_mappings.get(
            relation.lower(), None)
        if biolink_term_externals is not None:
            mapping_term_used = "none"
            for mapping_term in mapping_hierarchy:
                allowed_biolink_curies_set = biolink_term_externals[mapping_term]
                if len(allowed_biolink_curies_set) != 0:
                    mapping_term_used = mapping_term
                    break
            if len(allowed_biolink_curies_set) != 0 and relation not in relation_mapping_exceptions:
                err_str = "%s should map to %s (%s)" % (relation, allowed_biolink_curies_set, mapping_term_used.split("_")[0])
                assert subinfo[1] in allowed_biolink_curies_set, err_str

    else:
        assert command == 'keep' or command == 'delete'
        if command == 'keep':
            assert relation in biolink_to_external_mappings, relation
            assert relation.startswith(
                'biolink:') or relation.startswith('skos:')
