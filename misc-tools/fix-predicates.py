#!/usr/bin/env python3

import pprint
import urllib.request
import yaml

biolink_model = yaml.safe_load(urllib.request.urlopen('https://raw.githubusercontent.com/biolink/biolink-model/master/biolink-model.yaml'))

biolink_to_external_mappings = {'biolink:' + relation.replace(' ', '_'):
                                list(map(lambda x: x.lower(), relation_info.get('mappings', []))) for
                                relation, relation_info in biolink_model['slots'].items()}
for relation, relation_info in biolink_model['slots'].items():
    inverted_relation = relation_info.get('inverse', None)
    mappings = relation_info.get('mappings', None)
    if inverted_relation is not None and mappings is not None:
        biolink_curie = 'biolink:' + inverted_relation.replace(' ', '_')
        existing_list = biolink_to_external_mappings.get(biolink_curie, None)
        if existing_list is None:
            existing_list = []
        existing_list += list(map(lambda x: x.lower(), mappings))
        biolink_to_external_mappings[biolink_curie] = existing_list

biolink_to_external_mappings['skos:closeMatch'] = []

external_to_biolink_mappings = dict()
for biolink_curie, external_curies in biolink_to_external_mappings.items():
    for external_curie in external_curies:
        if external_to_biolink_mappings.get(external_curie, None) is None:
            external_to_biolink_mappings[external_curie] = set()
        external_to_biolink_mappings[external_curie].add(biolink_curie)


pred_info = yaml.safe_load(open('../predicate-remap.yaml', 'r'))
for relation, instruction_dict in pred_info.items():
    command, subinfo = next(iter(instruction_dict.items()))
    if command == 'keep' and not relation.startswith('biolink:'):
        if not relation.startswith('BSPO:') and \
           not relation.startswith('FMA:') and \
           not relation.startswith('UBERON:'):
            assert False, relation
        else:
            command = 'rename'
            subinfo = ['coexists_with', 'biolink:coexists_with']
    if subinfo is not None:
        simplified_relation = subinfo[1]
        if not simplified_relation.startswith('biolink:') and not simplified_relation.startswith('skos:closeMatch'):
            if simplified_relation.startswith('FMA:') or \
               simplified_relation.startswith('BSPO:') or \
               simplified_relation.startswith('UBERON:'):
                command = 'rename'
                subinfo = ['coexists_with', 'biolink:coexists_with']
            else:
                assert False
    if subinfo is not None:
        assert subinfo[1] in biolink_to_external_mappings, relation
        allowed_biolink_curies_set = external_to_biolink_mappings.get(relation.lower(), None)
        if allowed_biolink_curies_set is not None:
            assert subinfo[1] in allowed_biolink_curies_set, relation
    else:
        assert command == 'keep' or command == 'delete'
        if command == 'keep':
            assert relation in biolink_to_external_mappings, relation
            assert relation.startswith('biolink:') or relation.startswith('skos:')
    instruction_dict[command] = subinfo
with open('predicate-remap-new.yaml', 'w') as outfile:
    yaml.dump(pred_info, outfile)
