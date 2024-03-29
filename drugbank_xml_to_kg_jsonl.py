#!/usr/bin/env python3
''' drugbank_xml_to_kg_json.py: Extracts a KG2 JSON file from the
    DrugBank database in XML format

    Usage: drugbank_xml_to_kg_json.py [--test] <inputFile.json>
    <outputNodesFile.json> <outputEdgesFile.json>
'''

import kg2_util as kg2_util
import argparse
import xmltodict
import datetime
import sys
import pickle
import json

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood', 'Lindsey Kvarfordt']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

DRUGBANK_BASE_IRI = kg2_util.BASE_URL_DRUGBANK
DRUGBANK_KB_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY \
                                + ":drugbank"
DRUGBANK_RELATION_CURIE_PREFIX = kg2_util.CURIE_PREFIX_DRUGBANK
DRUGBANK_KB_IRI = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + 'drugbank'

APPROVED_DRUG_NODE_ID = "MI:2099"
NUTRACEUTICAL_DRUG_NODE_ID = "MI:2102"
ILLICIT_DRUG_NODE_ID = "MI:2150"
INVESTIGATIONAL_DRUG_NODE_ID = "MI:2148"
WITHDRAWN_DRUG_NODE_ID = "MI:2149"
EXPERIMENTAL_DRUG_NODE_ID = "MI:2100"
TYPE_SMALL_MOLECULE = "small molecule"
TYPE_BIOTECH = "biotech"


def get_args():
    arg_parser = argparse.ArgumentParser(description='drugbank_xml_to_kg_json.py: \
                                         builds a KG2 JSON representation of \
                                         DrugBank drugs')
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputNodesFile', type=str)
    arg_parser.add_argument('outputEdgesFile', type=str)
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
                creation_date: str,
                sequence: str):
    iri = DRUGBANK_BASE_IRI + drugbank_id
    node_curie = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + drugbank_id
    node_dict = kg2_util.make_node(node_curie,
                                   iri,
                                   name,
                                   category_label,
                                   update_date,
                                   DRUGBANK_KB_CURIE_ID)
    node_dict["synonym"] = synonyms
    node_dict["creation_date"] = creation_date
    node_dict["description"] = description
    node_dict["publications"] = publications
    node_dict["has_biological_sequence"] = sequence
    return node_dict


def format_edge(subject_id: str,
                object_id: str,
                predicate_label: str,
                description: str,
                publications: list = None):
    relation_curie = kg2_util.predicate_label_to_curie(predicate_label,
                                                       DRUGBANK_RELATION_CURIE_PREFIX)

    edge = kg2_util.make_edge(subject_id,
                              object_id,
                              relation_curie,
                              predicate_label,
                              DRUGBANK_KB_CURIE_ID,
                              None)

    if description is not None:
        edge["publications_info"] = {"sentence": description}

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
                        publications.append(kg2_util.CURIE_PREFIX_PMID +
                                            ':' + publication["pubmed-id"])

    return publications


def get_SMILES(calculated_properties: dict):
    if calculated_properties is not None and isinstance(calculated_properties, dict):
        properties = calculated_properties['property']
        if properties is not None:
            if isinstance(properties, list):
                for property in properties:
                    if property['kind'] == "SMILES":
                        return property['value']
            if isinstance(properties, dict):
                if properties['kind'] == "SMILES":
                    return properties['value']


def make_node(drug: dict):
    drugbank_id = get_drugbank_id(drug)
    synonyms = []
    drug_type = drug["@type"]
    if drug_type == TYPE_SMALL_MOLECULE:
        category = kg2_util.BIOLINK_CATEGORY_SMALL_MOLECULE
    elif drug_type == TYPE_BIOTECH:
        category = kg2_util.BIOLINK_CATEGORY_CHEMICAL_ENTITY
    else:
        print(f"Unknown type: {drug_type} for drug ID: {drugbank_id}; treating as chemical entity",
              file=sys.stderr)
        category = kg2_util.BIOLINK_CATEGORY_CHEMICAL_ENTITY
    if drug["synonyms"] is not None:
        if drug["synonyms"]["synonym"] is not None:
            for synonym in drug["synonyms"]["synonym"]:
                if isinstance(synonym, dict):
                    synonyms.append(synonym["#text"])
    publications = get_publications(drug["general-references"])
    smiles = get_SMILES(drug.get('calculated-properties', None)) # Per Issue #1273, if desired down the road
    node = None
    description = drug["description"]
    if description is not None:
        description = description.replace('\n', ' ').replace('\r', ' ')
    if len(drugbank_id) > 0:
        node = format_node(drugbank_id=drugbank_id,
                           description=description,
                           name=drug["name"],
                           update_date=drug["@updated"],
                           synonyms=synonyms,
                           publications=publications,
                           category_label=category,
                           creation_date=drug["@created"],
                           sequence=smiles)
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
                        object_id = kg2_util.CURIE_PREFIX_MESH + ":" + \
                                    category["mesh-id"]
                        edge = format_edge(subject_id,
                                           object_id,
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


    external_identifier_conversion = {"KEGG Drug": kg2_util.CURIE_PREFIX_KEGG_DRUG,
                                      "UniProtKB": kg2_util.CURIE_PREFIX_UNIPROT,
                                      "Therapeutic Targets Database": kg2_util.CURIE_PREFIX_TTD_DRUG,
                                      "ChEMBL": kg2_util.CURIE_PREFIX_CHEMBL_COMPOUND,
                                      "KEGG Compound": kg2_util.CURIE_PREFIX_KEGG_COMPOUND,
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
                        if not object_id.startswith(kg2_util.CURIE_PREFIX_UNIPROT + ':'):
                            predicate_label = "external-identifier"
                        else:
                            predicate_label = "external-identifier-protein"
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


def get_target_predicate(actions, predicate_label_default):
    predicate_label = predicate_label_default
    if actions is not None:
        predicate_label = actions['action']
        if isinstance(predicate_label, list):
            predicate_label = predicate_label[0]
    if predicate_label in ['other', 'unknown', 'other/unknown']:
        predicate_label = predicate_label_default
    return predicate_label


def make_target_edge(drug: dict):
    target_edges = []

    subject_id = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + get_drugbank_id(drug)

    predicate_label_default = "target"

    if drug["targets"] is not None:
        targets = drug["targets"]["target"]
        if targets is not None:
            if isinstance(targets, dict):
                actions = targets['actions']
                predicate_label = get_target_predicate(actions, predicate_label_default)
                for edge in extract_target_edge(targets,
                                                subject_id,
                                                predicate_label):
                    target_edges.append(edge)
            if isinstance(targets, list):
                for target in targets:
                    actions = target['actions']
                    predicate_label = get_target_predicate(actions, predicate_label_default)
                    for edge in extract_target_edge(target,
                                                    subject_id,
                                                    predicate_label):
                        target_edges.append(edge)

    return target_edges


def get_status_groups(drug: dict):
    groups = ""
    if isinstance(drug["groups"]["group"], list):
        groups = drug["groups"]["group"]
    elif isinstance(drug["groups"]["group"], str):
        groups = [drug["groups"]["group"]]
    return groups


# addresses issue 1050, and adds edges connecting drugs to their approval status
def make_group_edges(drug: dict):
    group_edges = []
    subject_id = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + get_drugbank_id(drug)
    predicate_label = "group"
    groups = get_status_groups(drug)
    for group in groups:
        object_id = ""
        if group.lower() == "approved":
            object_id = APPROVED_DRUG_NODE_ID
        elif group.lower() == "withdrawn":
            object_id = WITHDRAWN_DRUG_NODE_ID
        elif group.lower() == "nutraceutical":
            object_id = NUTRACEUTICAL_DRUG_NODE_ID
        elif group.lower() == "illicit":
            object_id = ILLICIT_DRUG_NODE_ID
        elif group.lower() == "investigational":
            object_id = INVESTIGATIONAL_DRUG_NODE_ID
        elif group.lower() == "experimental":
            object_id = EXPERIMENTAL_DRUG_NODE_ID
        elif group.lower() == "vet_approved":
            object_id = APPROVED_DRUG_NODE_ID
        if object_id == "":
            print(f"Unknown group: {group} for {subject_id}. Skipping.", file=sys.stderr)
            continue
        edge = format_edge(subject_id,
                           object_id,
                           predicate_label,
                           None)
        group_edges.append(edge)
    return group_edges


def get_atc_codes(drug: dict):
    sub_codes_return = set()
    atc_codes_dict = drug['atc-codes']
    if atc_codes_dict is None:
        return [], []
    atc_codes = atc_codes_dict['atc-code']
    main_codes = set()
    if isinstance(atc_codes, list):
        for atc_code in atc_codes:
            main_code = atc_code['@code']
            main_codes.add(main_code)
            sub_codes = atc_code['level']
            for code in sub_codes:
                sub_codes_return.add(code['@code'])
    else:
        try:
            main_code = atc_codes['@code']
        except:
            print(json.dumps(drug, indent=4, sort_keys=True))
            return [], []
        main_codes.add(main_code)
        sub_codes = atc_codes['level']
        for code in sub_codes:
            sub_codes_return.add(code['@code'])
    return sorted(list(main_codes)), sorted(list(sub_codes_return))


def make_atc_edges(drug: dict):
    atc_edges = []
    subject_id = kg2_util.CURIE_PREFIX_DRUGBANK + ':' + get_drugbank_id(drug)
    predicate_label_main = 'atc-code'
    predicate_label_sub = predicate_label_main + '-level'
    main_atc_codes, sub_atc_codes = get_atc_codes(drug)
    for main_code in main_atc_codes:
        edge = format_edge(subject_id,
                           kg2_util.CURIE_PREFIX_ATC + ':' + main_code,
                           predicate_label_main,
                           None,
                           None)
        atc_edges.append(edge)
    for sub_code in sub_atc_codes:
        edge = format_edge(subject_id,
                           kg2_util.CURIE_PREFIX_ATC + ':' + sub_code,
                           predicate_label_sub,
                           None,
                           None)
        atc_edges.append(edge)
    return atc_edges


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

    group_edges = make_group_edges(drug)
    if group_edges is not None:
        for group_edge in group_edges:
            edges.append(group_edge)

    atc_edges = make_atc_edges(drug)
    if atc_edges is not None:
        for atc_edge in atc_edges:
            edges.append(atc_edge)

    return edges


def make_kg2_graph(drugbank_dict: dict, nodes_output, edges_output, test_mode: bool):
    drugs = drugbank_dict["drugbank"]["drug"]

    update_date = drugbank_dict["drugbank"]["@exported-on"]
    version = drugbank_dict["drugbank"]["@version"]
    drugbank_kp_node = kg2_util.make_node(DRUGBANK_KB_CURIE_ID,
                                          DRUGBANK_KB_IRI,
                                          "DrugBank v" + version,
                                          kg2_util.SOURCE_NODE_CATEGORY,
                                          update_date,
                                          DRUGBANK_KB_CURIE_ID)

    nodes_output.write(drugbank_kp_node)

    drug_ctr = 0

    for drug in drugs:
        drug_ctr += 1
        if test_mode and drug_ctr > 10000:
            break
        node = make_node(drug)
        if node is not None:
            nodes_output.write(node)
        for edge in make_edges(drug):
            if edge is not None:
                edges_output.write(edge)


def xml_to_drugbank_dict(input_file_name: str):
    drugbank = open(input_file_name)
    drugbank_dict = xmltodict.parse(drugbank.read())
    drugbank.close()
    return drugbank_dict


if __name__ == '__main__':
    print("Start time: ", date())
    args = get_args()
    input_file_name = args.inputFile
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile
    test_mode = args.test

    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    print("Start load: ", date())
    drugbank_dict = xml_to_drugbank_dict(input_file_name)
    # For debugging only
    #drugbank_dict = pickle.load(open(input_file_name, 'rb'))
    print("Finish load: ", date())

    print("Start nodes and edges: ", date())
    make_kg2_graph(drugbank_dict, nodes_output, edges_output, test_mode)
    print("Finish nodes and edges: ", date())

    print("Start closing JSON: ", date())
    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)
    print("Finish closing JSON: ", date())

    print("Finish time: ", date())
