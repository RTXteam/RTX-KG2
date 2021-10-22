#!/usr/bin/env python3
''' drugcentral_json_to_kg_json.py: Converts the DrugCentral JSON
    file into a KG JSON file

    Usage: drugcentral_json_to_kg_json.py [--test] <inputFile.txt>
    <outputFile.json>
'''


import json
import argparse
import kg2_util


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

CURIE_PREFIX_DRUGCENTRAL = kg2_util.CURIE_PREFIX_DRUGCENTRAL

BASE_URL_DRUGCENTRAL = kg2_util.BASE_URL_DRUGCENTRAL

DRUGCENTRAL_SOURCE = kg2_util.CURIE_ID_DRUGCENTRAL_SOURCE
DRUGCENTRAL_RELATION_CURIE_PREFIX = kg2_util.CURIE_PREFIX_DRUGCENTRAL

TEST_MODE_EDGE_COUNT = 10000


def get_args():
    description = "drugcentral_json_to_kg_json.py: converts the DrugCentral \
                   JSON file into a KG JSON file"
    arg_parser = argparse.ArgumentParser(description=description)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    return arg_parser.parse_args()


def format_drugcentral_id(struct_id):
    return CURIE_PREFIX_DRUGCENTRAL + ':' + struct_id


def format_edge(subject_id, object_id, predicate, update_date):
    relation_curie = kg2_util.predicate_label_to_curie(predicate,
                                                       DRUGCENTRAL_RELATION_CURIE_PREFIX)
    if predicate == kg2_util.EDGE_LABEL_BIOLINK_SAME_AS:
        return kg2_util.make_edge_biolink(subject_id,
                                          object_id,
                                          predicate,
                                          DRUGCENTRAL_SOURCE,
                                          update_date)
    else:
        return kg2_util.make_edge(subject_id,
                                  object_id,
                                  relation_curie,
                                  predicate,
                                  DRUGCENTRAL_SOURCE,
                                  update_date)


def process_external_ids(external_ids, update_date, test_mode):
    edges = []
    edge_count = 0
    prefix_map = {'MESH_DESCRIPTOR_UI': kg2_util.CURIE_PREFIX_MESH,
                  'RXNORM': None,
                  'VANDF': kg2_util.CURIE_PREFIX_VANDF,
                  'IUPHAR_LIGAND_ID': None,
                  'PDB_CHEM_ID': None,
                  'INN_ID': None,
                  'SECONDARY_CAS_RN': None,
                  'SNOMEDCT_US': kg2_util.CURIE_PREFIX_SNOMED,
                  'CHEBI': kg2_util.CURIE_PREFIX_CHEBI,
                  'NDDF': None,
                  'NUI': None,
                  'UNII': None,
                  'MESH_SUPPLEMENTAL_RECORD_UI': kg2_util.CURIE_PREFIX_MESH,
                  'PUBCHEM_CID': None,
                  'VUID': None,
                  'KEGG_DRUG': kg2_util.CURIE_PREFIX_KEGG_DRUG,
                  'DRUGBANK_ID': kg2_util.CURIE_PREFIX_DRUGBANK,
                  'MMSL': None,
                  'UMLSCUI': kg2_util.CURIE_PREFIX_UMLS,
                  'ChEMBL_ID': kg2_util.CURIE_PREFIX_CHEMBL_COMPOUND}
    for original_predicate in external_ids:
        edge_count += 1
        if test_mode and edge_count > TEST_MODE_EDGE_COUNT:
            break
        prefix = prefix_map.get(original_predicate['id_type'], None)
        if prefix is None or \
           len(original_predicate['struct_id']) < 1 or \
           len(original_predicate['identifier']) < 1:
            continue
        drug_central_id = format_drugcentral_id(original_predicate['struct_id'])
        external_id = prefix + ':' + original_predicate['identifier']
        predicate = kg2_util.EDGE_LABEL_BIOLINK_SAME_AS
        edge = format_edge(drug_central_id,
                           external_id,
                           predicate,
                           update_date)
        edges.append(edge)
    return edges


def process_omop_relations(omop_relations, update_date, test_mode):
    edges = []
    edge_count = 0
    for original_predicate in omop_relations:
        edge_count += 1
        if test_mode and edge_count > TEST_MODE_EDGE_COUNT:
            break
        umls_id = original_predicate['umls_cui']
        doid_id = original_predicate['doid']
        drug_central_id = original_predicate['struct_id']
        predicate = original_predicate['relationship_name'].replace(' ', '_')
        if (len(doid_id) < 1 and len(umls_id) < 1) or \
           len(drug_central_id) < 1 or \
           len(predicate) < 1:
            continue
        object_id = ''
        if len(doid_id) < 1:
            object_id = kg2_util.CURIE_PREFIX_UMLS + ':' + umls_id
        else:
            object_id = kg2_util.CURIE_PREFIX_DOID + ':' + doid_id.replace('DOID:', '')
        drug_central_id = format_drugcentral_id(drug_central_id)
        edge = format_edge(drug_central_id, object_id, predicate, update_date)
        edges.append(edge)
    return edges


def process_faers_data(faers_edges, update_date, test_mode):
    edges = []
    edge_count = 0
    for original_predicate in faers_edges:
        edge_count += 1
        if test_mode and edge_count > TEST_MODE_EDGE_COUNT:
            break
        meddra_id = original_predicate['meddra_code']
        drug_central_id = original_predicate['struct_id']
        predicate = 'has_faers'
        likelihood = float(original_predicate['llr'])
        likelihood_threshold = float(original_predicate['llr_threshold'])
        if likelihood < likelihood_threshold:
            continue
        if len(meddra_id) < 1 or len(drug_central_id) < 1:
            continue
        meddra_id = kg2_util.CURIE_PREFIX_MEDDRA + ':' + meddra_id
        drug_central_id = format_drugcentral_id(drug_central_id)
        edge = format_edge(drug_central_id, meddra_id, predicate, update_date)
        edges.append(edge)
    return edges


def process_atc_codes(atc_codes, update_date, test_mode):
    edges = []
    edge_count = 0
    for original_predicate in atc_codes:
        edge_count += 1
        if test_mode and edge_count > TEST_MODE_EDGE_COUNT:
            break
        atc_id = original_predicate['atc_code']
        drug_central_id = original_predicate['struct_id']
        if len(atc_id) < 1 or len(drug_central_id) < 1:
            continue
        atc_id = kg2_util.CURIE_PREFIX_ATC + ':' + atc_id
        drug_central_id = format_drugcentral_id(drug_central_id)
        predicate = 'struct2atc'
        edge = format_edge(drug_central_id, atc_id, predicate, update_date)
        edges.append(edge)
    return edges


def format_publication(url):
    pubmed_url = 'http://www.ncbi.nlm.nih.gov/pubmed/'
    return kg2_util.CURIE_PREFIX_PMID + ':' + url.replace(pubmed_url, '')


def process_bioactivities(bioactivities, update_date, test_mode):
    edges = []
    edge_count = 0
    for original_predicate in bioactivities:
        edge_count += 1
        if test_mode and edge_count > TEST_MODE_EDGE_COUNT:
            break
        publications = []
        action_type = original_predicate['action_type'].lower().replace(' ', '_')
        moa_source = original_predicate['moa_source']
        moa_source_url = original_predicate['moa_source_url']
        drug_central_id = format_drugcentral_id(original_predicate['struct_id'])
        act_source = original_predicate['act_source']
        act_source_url = original_predicate['act_source_url']
        if len(act_source_url) > 0 and act_source == "SCIENTIFIC LITERATURE":
            publications.append(format_publication(act_source_url))
        if len(moa_source_url) > 0 and moa_source == "SCIENTIFIC LITERATURE":
            publications.append(format_publication(moa_source_url))
        if len(action_type) < 1:
            continue
        for accession in original_predicate['accession'].split('|'):
            if len(accession) < 1:
                continue
            uniprot_id = kg2_util.CURIE_PREFIX_UNIPROT + ':' + accession
            edge = format_edge(drug_central_id,
                               uniprot_id,
                               action_type,
                               update_date)
            edge['publications'] = publications
            edges.append(edge)
    return edges


def process_pharmacologic_actions(pharm_acts, update_date, test_mode):
    edges = []
    prefix_map = {'CHEBI': kg2_util.CURIE_PREFIX_CHEBI,
                  'FDA': None,
                  'MeSH': kg2_util.CURIE_PREFIX_MESH}
    edge_count = 0
    for action in pharm_acts:
        edge_count += 1
        if test_mode and edge_count > TEST_MODE_EDGE_COUNT:
            break
        prefix = prefix_map.get(action['source'], None)
        if prefix is None:
            continue
        predicate = action['type'].replace(' ', '_')
        chebi_pr = kg2_util.CURIE_PREFIX_CHEBI + ':'
        object_id = prefix + ':' + action['class_code'].replace(chebi_pr, '')
        drug_central_id = format_drugcentral_id(action['struct_id'])
        edge = format_edge(drug_central_id, object_id, predicate, update_date)
        edges.append(edge)
    return edges


def make_nodes(drugcentral_ids, update_date):
    nodes = []
    reformatted_json = dict()
    category_label = kg2_util.BIOLINK_CATEGORY_DRUG
    for name_row in drugcentral_ids:
        drug_central_id = name_row['id']
        name = name_row['name']
        if len(drug_central_id) < 1:
            continue
        drug_central_id = format_drugcentral_id(drug_central_id)
        if drug_central_id not in reformatted_json:
            reformatted_json[drug_central_id] = dict()
            reformatted_json[drug_central_id]['synonyms'] = []
        if name_row['preferred_name'] == "1":
            reformatted_json[drug_central_id]['name'] = name
        else:
            reformatted_json[drug_central_id]['synonyms'].append(name)
    for node_id in reformatted_json:
        synonyms = reformatted_json[node_id]['synonyms']
        name = reformatted_json[node_id]['name']
        iri = BASE_URL_DRUGCENTRAL + node_id.split(':')[1]
        provided_by = DRUGCENTRAL_SOURCE
        node = kg2_util.make_node(node_id,
                                  iri,
                                  name,
                                  category_label,
                                  update_date,
                                  provided_by)
        node['synonym'] = synonyms
        nodes.append(node)
    return nodes


if __name__ == '__main__':
    args = get_args()
    edges = []
    nodes = []
    test_mode = args.test
    with open(args.inputFile, 'r') as input_file:
        json_data = json.load(input_file)
        update_date = json_data['version'][0]['dtime']
        version_number = json_data['version'][0]['version as version_number']
        edges = process_external_ids(json_data['external_ids'],
                                     update_date,
                                     test_mode)
        edges += process_omop_relations(json_data['omop_relations'],
                                        update_date,
                                        test_mode)
        edges += process_faers_data(json_data['faers_data'],
                                    update_date,
                                    test_mode)
        edges += process_atc_codes(json_data['atc_ids'],
                                   update_date,
                                   test_mode)
        edges += process_bioactivities(json_data['bioactivities'],
                                       update_date,
                                       test_mode)
        edges += process_pharmacologic_actions(json_data['pharmacologic_action'],
                                               update_date,
                                               test_mode)
        nodes = make_nodes(json_data['drugcentral_ids'], update_date)
        kp_node = kg2_util.make_node(DRUGCENTRAL_SOURCE,
                                     BASE_URL_DRUGCENTRAL,
                                     'DrugCentral v' + version_number,
                                     kg2_util.BIOLINK_CATEGORY_INFORMATION_RESOURCE,
                                     update_date,
                                     DRUGCENTRAL_SOURCE)
        nodes.append(kp_node)
    graph = {'edges': edges, 'nodes': nodes}
    kg2_util.save_json(graph, args.outputFile, test_mode)
