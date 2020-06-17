#!/usr/bin/env python3
''' drugbank_xml_to_kg_json.py: Extracts a KG2 JSON file from the
    DrugBank database in XML format

    Usage: drugbank_xml_to_kg_json.py [--test] <inputFile.json>
    <outputFile.json>
'''

import json
import kg2_util as kg2_util
import argparse
import xmltodict
import datetime

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

DRUGBANK_BASE_IRI = 'https://identifiers.org/drugbank:'
DRUGBANK_KB_CURIE_ID = kg2_util.IDENTIFIERS_ORG_REGISTRY_CURIE_PREFIX \
                                + ":drugbank"
DRUGBANK_RELATION_CURIE_PREFIX = 'DRUGBANK'
DRUGBANK_KB_IRI = 'https://registry.identifiers.org/registry/drugbank'


def get_args():
    arg_parser = argparse.ArgumentParser(description='drugbank_xml_to_kg_json.py: \
                                         builds a KG2 JSON representation of \
                                         DrugBank drugs')
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_node(drugbank_id: str,
                description: str,
                name: str,
                update_date: str,
                synonyms: list,
                publications: list,
                category_label: str,
                creation_date: str):
    iri = DRUGBANK_BASE_IRI + drugbank_id
    node_curie = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + drugbank_id
    node_dict = kg2_util.make_node(node_curie,
                                   iri,
                                   name,
                                   category_label,
                                   update_date,
                                   DRUGBANK_KB_CURIE_ID)
    node_dict["synonym"] = synonyms
    node_dict["creation date"] = creation_date
    node_dict["description"] = description
    node_dict["publications"] = publications
    return node_dict


def format_edge(subject_id: str,
                object_id: str,
                predicate_label: str,
                description: str,
                publications: list=None):
    [relation, relation_curie] = kg2_util.predicate_label_to_iri_and_curie(predicate_label,
                                                                           DRUGBANK_RELATION_CURIE_PREFIX,
                                                                           DRUGBANK_KB_IRI)

    edge = kg2_util.make_edge(subject_id,
                              object_id,
                              relation,
                              relation_curie,
                              predicate_label,
                              DRUGBANK_KB_CURIE_ID,
                              None)

    if description is not None:
        edge["publications info"] = {"sentence": description}

    if publications is not None:
        edge["publications"] = publications

    return edge


def get_publications(references: list):
    publications = []
    if references is not None:
        if references["articles"] is not None:
            if references["articles"]["article"] is not None:
                for publication in references["articles"]["article"]:
                    if isinstance(publication, dict) and \
                       publication["pubmed-id"] is not None:
                        publications.append("PMID" + publication["pubmed-id"])

    return publications


def make_node(drug: dict):
    drugbank_id = get_drugbank_id(drug)
    synonyms = []
    if drug["synonyms"] is not None:
        if drug["synonyms"]["synonym"] is not None:
            for synonym in drug["synonyms"]["synonym"]:
                if isinstance(synonym, dict):
                    synonyms.append(synonym["#text"])
    publications = get_publications(drug["general-references"])
    node = None
    if len(drugbank_id) > 0:
        node = format_node(drugbank_id=drugbank_id,
                           description=drug["description"],
                           name=drug["name"],
                           update_date=drug["@updated"],
                           synonyms=synonyms,
                           publications=publications,
                           category_label="drug",
                           creation_date=drug["@created"])
        ''' For description, also consider "drug["description"]" --
            might be a good question for Steve
        '''
    return node


def get_drugbank_id(drug: dict):
    drugbank_id = ""
    if isinstance(drug["drugbank-id"], list):
        for id in drug["drugbank-id"]:
            if isinstance(id, dict):
                if id["@primary"] == "true":
                    drugbank_id = id["#text"]
    elif isinstance(drug["drugbank-id"], dict):
        id = drug["drugbank-id"]
        if id["@primary"] == "true":
            drugbank_id = id["#text"]
    return drugbank_id


def make_category_edges(drug: dict):
    category_edges = []

    subject_id = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + get_drugbank_id(drug)

    predicate_label = "category"

    if drug["categories"] is not None:
        if drug["categories"]["category"] is not None:
            for category in drug["categories"]["category"]:
                if isinstance(category, dict):
                    if category["mesh-id"] is not None and \
                       subject_id is not None and \
                       category["category"] is not None:
                        edge = format_edge(subject_id,
                                           "MESH:" + category["mesh-id"],
                                           predicate_label,
                                           category["category"])
                        category_edges.append(edge)
    return category_edges


def make_interaction_edges(drug: dict):
    interaction_edges = []

    subject_id = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + get_drugbank_id(drug)

    predicate_label = "drug-interaction"

    if drug["drug-interactions"] is not None:
        if drug["drug-interactions"]["drug-interaction"] is not None:
            for interaction in drug["drug-interactions"]["drug-interaction"]:
                if isinstance(interaction, dict) and \
                   interaction["drugbank-id"] is not None and \
                   interaction["description"] is not None:
                    object_id = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + \
                                interaction["drugbank-id"]
                    edge = format_edge(subject_id,
                                       object_id,
                                       predicate_label,
                                       interaction["description"])
                    interaction_edges.append(edge)
    return interaction_edges


def make_equivalent_edges(drug: dict):
    equivalent_edges = []

    subject_id = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + get_drugbank_id(drug)

    predicate_label = "external-identifier"

    external_identifier_conversion = {"KEGG Drug": kg2_util.CURIE_PREFIX_KEGG,
                                      "UniProtKB": kg2_util.CURIE_PREFIX_UNIPROT,
                                      "Therapeutic Targets Database": kg2_util.CURIE_PREFIX_TTD,
                                      "ChEMBL": kg2_util.CURIE_PREFIX_CHEMBL,
                                      "KEGG Compound": kg2_util.CURIE_PREFIX_KEGG,
                                      "ChEBI": kg2_util.CURIE_PREFIX_CHEBI}
    if drug["external-identifiers"] is not None:
        if drug["external-identifiers"]["external-identifier"] is not None:
            for ex_id in drug["external-identifiers"]["external-identifier"]:
                if isinstance(ex_id, dict):
                    if ex_id["identifier"] is not None and \
                       ex_id["resource"] in external_identifier_conversion:
                        resource = ex_id["resource"]
                        conversion = external_identifier_conversion[resource]
                        object_id = conversion + ":" + ex_id["identifier"]
                        edge = format_edge(subject_id,
                                           object_id,
                                           predicate_label,
                                           None)
                        equivalent_edges.append(edge)
    return equivalent_edges


def extract_pathway_edge(pathway: dict, subject_id: str, predicate_label: str):
    edge = None
    if pathway["smpdb-id"] is not None and pathway["name"] is not None:
        object_id = kg2_util.CURIE_PREFIX_SMPDB + ":" + pathway["smpdb-id"]
        edge = format_edge(subject_id,
                           object_id,
                           predicate_label,
                           pathway["name"])
    return edge


def make_pathway_edges(drug: dict):
    pathway_edges = []

    subject_id = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + get_drugbank_id(drug)

    predicate_label = "pathway"

    if drug["pathways"] is not None:
        if drug["pathways"]["pathway"] is not None:
                if isinstance(drug["pathways"]["pathway"], list):
                    for pathway in drug["pathways"]["pathway"]:
                        pathway_edges.append(extract_pathway_edge(pathway,
                                                                  subject_id,
                                                                  predicate_label))
                if isinstance(drug["pathways"]["pathway"], dict):
                    pathway = drug["pathways"]["pathway"]
                    pathway_edges.append(extract_pathway_edge(pathway,
                                                              subject_id,
                                                              predicate_label))
    return pathway_edges


def extract_polypeptide(target: dict,
                        polypeptide: dict,
                        subject_id: str,
                        predicate_label: str):
    edge = None
    if polypeptide["@id"] is not None:
                object_id = kg2_util.CURIE_PREFIX_UNIPROT + \
                            ":" + polypeptide["@id"]
                edge = format_edge(subject_id,
                                   object_id,
                                   predicate_label,
                                   polypeptide["general-function"],
                                   get_publications(target["references"]))
    return edge


def extract_target_edge(target: dict, subject_id: str, predicate_label: str):
    target_edges = []
    if "polypeptide" in target and target["polypeptide"] is not None:
        if isinstance(target["polypeptide"], dict):
            target_edges.append(extract_polypeptide(target,
                                                    target["polypeptide"],
                                                    subject_id,
                                                    predicate_label))
        if isinstance(target["polypeptide"], list):
            for polypeptide in target["polypeptide"]:
                target_edges.append(extract_polypeptide(target,
                                                        polypeptide,
                                                        subject_id,
                                                        predicate_label))

    return target_edges


def make_target_edge(drug: dict):
    target_edges = []

    subject_id = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + get_drugbank_id(drug)

    predicate_label = "target"

    if drug["targets"] is not None:
        if drug["targets"]["target"] is not None:
            if isinstance(drug["targets"]["target"], dict):
                for edge in extract_target_edge(drug["targets"]["target"],
                                                subject_id,
                                                predicate_label):
                    target_edges.append(edge)
            if isinstance(drug["targets"]["target"], list):
                for target in drug["targets"]["target"]:
                    for edge in extract_target_edge(target,
                                                    subject_id,
                                                    predicate_label):
                        target_edges.append(edge)

    return target_edges


def make_edges(drug: dict):
    edges = []
    category_edges = make_category_edges(drug)
    if category_edges is not None:
        for category_edge in make_category_edges(drug):
            edges.append(category_edge)

    interaction_edges = make_interaction_edges(drug)
    if interaction_edges is not None:
        for interaction_edge in interaction_edges:
            edges.append(interaction_edge)

    equivalent_edges = make_equivalent_edges(drug)
    if equivalent_edges is not None:
        for equivalent_edge in equivalent_edges:
            edges.append(equivalent_edge)

    pathway_edges = make_pathway_edges(drug)
    if pathway_edges is not None:
        for pathway_edge in pathway_edges:
            edges.append(pathway_edge)

    target_edges = make_target_edge(drug)
    if target_edges is not None:
        for target_edge in target_edges:
            edges.append(target_edge)

    return edges


def make_kg2_graph(drugbank_dict: dict, test_mode: bool):
    drugs = drugbank_dict["drugbank"]["drug"]

    nodes = []
    edges = []

    update_date = drugbank_dict["drugbank"]["@exported-on"]
    drugbank_kp_node = kg2_util.make_node(DRUGBANK_KB_CURIE_ID,
                                          DRUGBANK_KB_IRI,
                                          "DrugBank",
                                          kg2_util.TYPE_DATA_SOURCE,
                                          update_date,
                                          DRUGBANK_KB_CURIE_ID)

    nodes.append(drugbank_kp_node)

    drug_ctr = 0

    for drug in drugs:
        drug_ctr += 1
        if test_mode and drug_ctr > 10000:
            break
        node = make_node(drug)
        if node is not None:
            nodes.append(node)
        for edge in make_edges(drug):
            if edge is not None:
                edges.append(edge)

    return {"nodes": nodes,
            "edges": edges}


def xml_to_drugbank_dict(input_file_name: str):
    drugbank = open(input_file_name)
    drugbank_dict = xmltodict.parse(drugbank.read())
    drugbank.close()
    return drugbank_dict


if __name__ == '__main__':
    print("Start time: ", date())
    args = get_args()
    input_file_name = args.inputFile
    output_file_name = args.outputFile
    test_mode = args.test
    print("Start load: ", date())
    drugbank_dict = xml_to_drugbank_dict(input_file_name)
    print("Finish load: ", date())
    print("Start nodes and edges: ", date())
    graph = make_kg2_graph(drugbank_dict, test_mode)
    print("Finish nodes and edges: ", date())
    print("Start saving JSON: ", date())
    kg2_util.save_json(graph, output_file_name, test_mode)
    print("Finish saving JSON: ", date())
    print("Finish time: ", date())
