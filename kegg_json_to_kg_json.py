#!/usr/bin/env python3
''' kegg_json_to_kg_json.py: Extracts a KG2 JSON file from a
    KEGG API JSON dump

    Usage: kegg_json_to_kg_json.py [--test] <inputFile.json>
    <outputFile.json>
'''

import json
import kg2_util
import argparse
import os

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

KEGG_COMPOUND_PREFIX = 'cpd:'
KEGG_PATHWAY_PREFIX = 'path:hsa'
KEGG_ENZYME_PREFIX = 'ec:'
KEGG_GLYCAN_PREFIX = 'gl:'
KEGG_DRUG_PREFIX = 'dr:'
KEGG_REACTION_PREFIX = 'rn:'

KEGG_CURIE_PREFIX = kg2_util.CURIE_PREFIX_KEGG
CHEMBL_COMPOUND_CURIE_PREFIX = kg2_util.CURIE_PREFIX_CHEMBL_COMPOUND
CHEBI_CURIE_PREFIX = kg2_util.CURIE_PREFIX_CHEBI
RHEA_CURIE_PREFIX = kg2_util.CURIE_PREFIX_RHEA

KEGG_BASE_IRI = "https://www.genome.jp/dbget-bin/www_bget?"
KEGG_PROVIDED_BY = kg2_util.CURIE_ID_KEGG
KEGG_SOURCE_IRI = "https://www.genome.jp"


def get_args():
    arg_parser = argparse.ArgumentParser(description='kegg_json_to_kg_json.py: \
                                         builds a KG2 JSON representation of \
                                         KEGG')
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def format_node(node_id,
                name,
                category_label,
                update_date,
                description=None,
                sequence=None,
                synonym=[]):
    iri = KEGG_BASE_IRI + node_id
    curie_id = format_id(node_id)
    node = kg2_util.make_node(curie_id,
                              iri,
                              name,
                              category_label,
                              update_date,
                              KEGG_PROVIDED_BY)
    node['description'] = description
    if sequence is not None and len(sequence) > 0:
        node['has_biological_sequence'] = sequence
    node['synonym'] = synonym

    return node


def format_same_as_edge(kegg_id, external_id, update_date):
    edge = kg2_util.make_edge_biolink(format_id(kegg_id),
                                      external_id,
                                      kg2_util.EDGE_LABEL_BIOLINK_SAME_AS,
                                      KEGG_PROVIDED_BY,
                                      update_date)
    return edge


def process_xref(xref):
    xref = xref.replace(': ', ':')
    prefix = xref.split(':')[0] + ':'
    xrefs = [prefix + xref_id.replace(prefix, '') for xref_id in xref.split(' ')]
    allowed_xrefs = {'ChEBI': CHEBI_CURIE_PREFIX,
                     'ChEMBL': CHEMBL_COMPOUND_CURIE_PREFIX,
                     'RHEA': RHEA_CURIE_PREFIX}
    return_xrefs = []
    for xref in xrefs:
        if xref.split(':')[0] in allowed_xrefs:
            for allowed_xref in allowed_xrefs:
                xref = xref.replace(allowed_xref, allowed_xrefs[allowed_xref])
            return_xrefs.append(xref)
    return return_xrefs


def format_id(id):
    return KEGG_CURIE_PREFIX + ':' + id


def process_reaction(reaction_dict, kegg_id):
    node_name = reaction_dict.get('NAME', '')
    if isinstance(node_name, list):
        node_name = node_name[0]
    node_name = node_name.strip()
    xrefs = process_xref(reaction_dict.get('DBLINKS', ''))
    node_id = format_id(kegg_id.replace(KEGG_REACTION_PREFIX, ''))
    description = reaction_dict['DEFINITION'].strip()
    if len(node_name) < 1:
        node_name = description
    synonym = [syn.strip() for syn in reaction_dict['name'].split(';')[1:]]
    enzymes = pull_out_enzymes(reaction_dict)
    pathways = pull_out_pathways(reaction_dict)
    return None


def pull_out_pathways(data_dict):
    pathways_return = data_dict.get('PATHWAY', [])
    pathways = []
    if isinstance(pathways_return, list):
        for pathway in pathways_return:
            pathways.append(format_id(pathway.split(' ')[0].strip()))
    else:
        pathways.append(format_id(pathways_return.split(' ')[0].strip()))
    return pathways


def pull_out_reactions(data_dict):
    reactions_return = data_dict.get('REACTION', [])
    reactions = []
    if isinstance(reactions_return, list):
        for reaction_list in reactions_return:
            reactions += [format_id(reaction.strip()) for reaction in reaction_list.split(' ')]
    else:
        reactions += [format_id(reaction.strip()) for reaction in reactions_return.split(' ')]
    return reactions


def pull_out_enzymes(data_dict):
    enzymes_return = data_dict.get('ENZYME', [])
    enzymes = []
    if isinstance(enzymes_return, list):
        for enzyme_list in enzymes_return:
            enzymes += [format_id(enzyme.strip()) for enzyme in enzyme_list.split('     ')]
    else:
        enzymes += [format_id(enzyme.strip()) for enzyme in enzymes_return.split('     ')]
    return enzymes


def process_sequence(data_dict):
    sequence_return = data_dict.get('SEQUENCE', None)
    sequence = ''
    if sequence_return is None:
        return None
    if isinstance(sequence_return, list):
        for sequence_string in sequence_return:
            if sequence_string.startswith('GENE') or sequence_string.startswith('ORGANISM') or sequence_string.startswith('TYPE'):
                break
            sequence += sequence_string + ' '
        return sequence.strip()
    else:
        return sequence_return


def process_compound(compound_dict, kegg_id, update_date):
    node_name =  compound_dict.get('NAME', '')
    synonym = []
    if isinstance(node_name, list):
        synonym = [syn.replace(';', '') for syn in node_name[1:]]
        node_name = node_name[0]
    node_name = node_name.strip().strip(';')
    xrefs = compound_dict.get('DBLINKS', '')
    if isinstance(xrefs, str):
        xrefs = [xrefs]
    processed_xrefs = []
    for xref in xrefs:
        processed_xrefs += process_xref(xref)
    node_id = kegg_id.replace(KEGG_COMPOUND_PREFIX, '')
    
    enzymes = pull_out_enzymes(compound_dict)
    reactions = pull_out_reactions(compound_dict)
    pathways = pull_out_pathways(compound_dict)
    sequence = process_sequence(compound_dict)

    node = format_node(node_id,
                       node_name,
                       kg2_util.BIOLINK_CATEGORY_CHEMICAL_SUBSTANCE,
                       update_date,
                       sequence=sequence,
                       synonym=synonym)
    edges = []
    for xref in processed_xrefs:
        edges.append(format_same_as_edge(node_id,
                                         xref,
                                         update_date))

    return node, edges

def make_kg2_graph(kegg, update_date):
    nodes = []
    edges = []
    for kegg_id in kegg:
        kegg_dict = kegg[kegg_id]
        if kegg_id.startswith(KEGG_COMPOUND_PREFIX):
            node, compound_edges = process_compound(kegg_dict, kegg_id, update_date)
            nodes.append(node)
            edges += compound_edges

    kegg_kp_node = kg2_util.make_node(KEGG_PROVIDED_BY,
                                      KEGG_SOURCE_IRI,
                                      'Kyoto Encyclopedia of Genes and Genomes',
                                      kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                      update_date,
                                      KEGG_PROVIDED_BY)
    nodes.append(kegg_kp_node)
    return {'nodes': nodes,
            'edges': edges}


if __name__ == '__main__':
    args = get_args()
    kegg = dict()
    with open(args.inputFile, 'r') as kegg_file:
        update_date = kg2_util.convert_date(os.path.getmtime(args.inputFile))
        kegg = json.load(kegg_file)
    graph = make_kg2_graph(kegg, update_date)
    kg2_util.save_json(graph, args.outputFile, args.test)
