#!/usr/bin/env python3
''' hmdb_xml_to_kg_json.py: Extracts a KG2 JSON file from the
    HMDB metabolite download in XML format

    Usage: hmdb_xml_to_kg_json.py [--test] <inputFile.xml>
    <outputFile.json>
'''

import xmltodict
import kg2_util
import argparse
import datetime
import os


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


HMDB_BASE_IRI = kg2_util.BASE_BASE_URL_IDENTIFIERS_ORG + "hmdb:"
HMDB_KB_IRI = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + "hmdb"
HMDB_PROVIDED_BY_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY \
                                + ":hmdb"

CURIE_PREFIX_HMDB = kg2_util.CURIE_PREFIX_HMDB


def get_args():
    arg_parser = argparse.ArgumentParser(description='hmdb_xml_to_kg_json.py: \
                                         builds a KG2 JSON representation of \
                                         HMDB Metabolites using the XML dump')
    arg_parser.add_argument('--test',
                            dest='test',
                            action="store_true",
                            default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def convert_date(time):
    return datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')


def make_hmdb_edge(subject_id: str,
                   object_id: str,
                   subject_prefix: str,
                   object_prefix: str,
                   predicate_label: str,
                   update_date: str,
                   publications_info: dict):
    relation_curie = kg2_util.predicate_label_to_curie(predicate_label,
                                                       CURIE_PREFIX_HMDB)
    subject = subject_prefix + ":" + subject_id
    object = object_id
    if object_prefix is not None:
        object = object_prefix + ":" + object_id
    if predicate_label == kg2_util.EDGE_LABEL_BIOLINK_SAME_AS:
        edge = kg2_util.make_edge_biolink(subject,
                                          object,
                                          predicate_label,
                                          HMDB_PROVIDED_BY_CURIE_ID,
                                          update_date)

    else:
        edge = kg2_util.make_edge(subject,
                                  object,
                                  relation_curie,
                                  predicate_label,
                                  HMDB_PROVIDED_BY_CURIE_ID,
                                  update_date)
    edge["publications info"] = publications_info

    return edge


def make_node(metabolite: dict, hmdb_id: str):
    iri = HMDB_BASE_IRI + hmdb_id
    name = metabolite["name"]
    category_label = kg2_util.BIOLINK_CATEGORY_METABOLITE
    update_date = metabolite["update_date"]
    creation_date = metabolite["creation_date"]
    provided_by = HMDB_PROVIDED_BY_CURIE_ID
    description = metabolite["description"]
    synonyms = []
    if (isinstance(metabolite["synonyms"], dict) and
            "synonym" in metabolite["synonyms"]):
        synonym_store = metabolite["synonyms"]["synonym"]
        if isinstance(synonym_store, list):
            for synonym in synonym_store:
                synonyms.append(synonym)
        else:
            synonyms.append(synonym_store)
    general_references = pull_out_references(metabolite["general_references"])
    publications = [reference for reference in general_references.keys()]

    node = kg2_util.make_node(CURIE_PREFIX_HMDB + ":" + hmdb_id,
                              iri,
                              name,
                              category_label,
                              update_date,
                              provided_by)
    node["description"] = description
    node["synonym"] = synonyms
    node["creation date"] = creation_date
    node["publications"] = publications

    return node


def pull_out_references(full_references: dict):
    publications_info = {}
    if isinstance(full_references, dict) and "reference" in full_references:
        references = full_references["reference"]
        if isinstance(references, list):
            for reference in references:
                if ("pubmed_id" in reference and
                        reference["pubmed_id"] is not None):
                    sentence = reference["reference_text"]
                    pubmed_id = kg2_util.CURIE_PREFIX_PMID + ":" + \
                        reference["pubmed_id"]
                    publications_info[pubmed_id] = {"sentence": sentence}
        else:
            if ("pubmed_id" in references and
                    references["pubmed_id"] is not None):
                sentence = references["reference_text"]
                pubmed_id = kg2_util.CURIE_PREFIX_PMID + ":" + \
                    references["pubmed_id"]
                publications_info[pubmed_id] = {"sentence": sentence}
    return publications_info


def make_disease_edges(metabolite: dict, hmdb_id: str):
    edges = []
    predicate_label = "disease"
    update_date = metabolite["update_date"]
    if (isinstance(metabolite["diseases"], dict) and
            "disease" in metabolite["diseases"]):
        diseases = metabolite["diseases"]["disease"]
        if isinstance(diseases, list):
            for disease in diseases:
                publications_info = pull_out_references(disease["references"])
                object_id = disease['omim_id']
                if object_id is not None:
                    edge = make_hmdb_edge(hmdb_id,
                                          object_id,
                                          CURIE_PREFIX_HMDB,
                                          kg2_util.CURIE_PREFIX_OMIM,
                                          predicate_label,
                                          update_date,
                                          publications_info)
                    edges.append(edge)
        else:
            publications_info = pull_out_references(diseases["references"])
            object_id = diseases['omim_id']
            if object_id is not None:
                edge = make_hmdb_edge(hmdb_id,
                                      object_id,
                                      CURIE_PREFIX_HMDB,
                                      kg2_util.CURIE_PREFIX_OMIM,
                                      predicate_label,
                                      update_date,
                                      publications_info)
                edges.append(edge)

    return edges


def make_protein_edges(metabolite: dict, hmdb_id: str):
    edges = []
    predicate_label = "has_protein_association"
    update_date = metabolite["update_date"]
    if (isinstance(metabolite["protein_associations"], dict) and
            "protein" in metabolite["protein_associations"]):
        proteins = metabolite["protein_associations"]["protein"]
        if isinstance(proteins, list):
            for protein in proteins:
                object_id = protein['uniprot_id']
                if object_id is not None:
                    edge = make_hmdb_edge(hmdb_id,
                                          object_id,
                                          CURIE_PREFIX_HMDB,
                                          kg2_util.CURIE_PREFIX_UNIPROT,
                                          predicate_label,
                                          update_date,
                                          {})
                    edges.append(edge)
        else:
            object_id = proteins['uniprot_id']
            if object_id is not None:
                edge = make_hmdb_edge(hmdb_id,
                                      object_id,
                                      CURIE_PREFIX_HMDB,
                                      kg2_util.CURIE_PREFIX_UNIPROT,
                                      predicate_label,
                                      update_date,
                                      {})
                edges.append(edge)
    return edges


def get_id(metabolite: dict, key: str):
    return metabolite.get(key, None)


def add_if_string(id_dict: dict, id_list: list, id, prefix):
    if isinstance(id, str):
        id_list.append(id)
        id_dict[id] = prefix


def equivocate(id_prefixes: dict,
               ids: list,
               eq_label: str,
               update_date: str):
    edges = []
    index = 0
    while index < len(ids):
        subject_id = ids[index]
        subject_prefix = id_prefixes[subject_id]
        for obj in ids[(index + 1):]:
            object_prefix = id_prefixes[obj]
            edges.append(make_hmdb_edge(subject_id,
                                        obj,
                                        subject_prefix,
                                        object_prefix,
                                        eq_label,
                                        update_date,
                                        {}))
        index += 1

    return edges


def make_equivalencies(metabolite: dict, hmdb_id: str):
    predicate_label = kg2_util.EDGE_LABEL_BIOLINK_SAME_AS
    edges = []

    kegg_id = get_id(metabolite, "kegg_id")
    drugbank_id = get_id(metabolite, "drugbank_id")
    chebi_id = get_id(metabolite, "chebi_id")
    id_list = []
    id_prefixes = {}

    add_if_string(id_prefixes,
                  id_list,
                  kegg_id,
                  kg2_util.CURIE_PREFIX_KEGG)
    add_if_string(id_prefixes,
                  id_list,
                  drugbank_id,
                  kg2_util.CURIE_PREFIX_DRUGBANK)
    add_if_string(id_prefixes,
                  id_list,
                  hmdb_id,
                  CURIE_PREFIX_HMDB)
    add_if_string(id_prefixes,
                  id_list,
                  chebi_id,
                  kg2_util.CURIE_PREFIX_CHEBI)

    for edge in equivocate(id_prefixes,
                           id_list,
                           predicate_label,
                           metabolite["update_date"]):
        edges.append(edge)
    return edges


def biospecimen_converter(biospecimen: str):
    urine = kg2_util.CURIE_PREFIX_UMLS + ":C0042036"
    pericardian_effusion = kg2_util.CURIE_PREFIX_UMLS + ":C1253937"
    blood = kg2_util.CURIE_PREFIX_UMLS + ":C0005767"
    aminotic_fluid = kg2_util.CURIE_PREFIX_UMLS + ":C0552315"
    sweat = kg2_util.CURIE_PREFIX_UMLS + ":C0038984"
    csf = kg2_util.CURIE_PREFIX_UMLS + ":C0007806"
    breast_milk = kg2_util.CURIE_PREFIX_UMLS + ":C0026140"
    cytoplasm = "FMA:66835"
    saliva = kg2_util.CURIE_PREFIX_UMLS + ":C0036087"
    semen = kg2_util.CURIE_PREFIX_UMLS + ":C2756969"
    bile = kg2_util.CURIE_PREFIX_MESH + ":D001646"
    feces = kg2_util.CURIE_PREFIX_UMLS + ":C0015733"
    biospecimen_dict = {"Urine": urine,
                        "Pericardial Effusion": pericardian_effusion,
                        "Blood": blood,
                        "Amniotic Fluid": aminotic_fluid,
                        "Sweat": sweat,
                        "Cerebrospinal Fluid (CSF)": csf,
                        "Breast Milk": breast_milk,
                        "Cellular Cytoplasm": cytoplasm,
                        "Saliva": saliva,
                        "Semen": semen,
                        "Bile": bile,
                        "Feces": feces,
                        "Prostate Tissue": None,
                        "Aqueous Humour": "EHDAA2:0000139",
                        "Ascites Fluid": None,
                        "Lymph": kg2_util.CURIE_PREFIX_MESH + ":D008196",
                        "Tears": kg2_util.CURIE_PREFIX_UMLS + ":C0039409"}
    return biospecimen_dict[biospecimen]


def cellular_locations_converter(cellular_location: str):
    umls = kg2_util.CURIE_PREFIX_UMLS
    locations_dict = {"Membrane": "GO:0016020",
                      "Golgi apparatus": "GO:0005794",
                      "Endoplasmic reticulum": "GO:0005783",
                      "Mitochondria": "GO:0005739",
                      "Nucleus": "GO:0005634",
                      "Peroxisome": "GO:0005777",
                      "Cytoplasm": "GO:0005737",
                      "Microsomes": "FMA:67438",
                      "Lysosome": "GO:0005764",
                      "Extracellular": "GO:0005576",
                      "Inner mitochondrial membrane": umls + ":C0230840"}
    return locations_dict[cellular_location]


def tissues_converter(tissue: str):
    mesh = kg2_util.CURIE_PREFIX_MESH
    chembl = kg2_util.CURIE_PREFIX_CHEMBL_TARGET
    cui = kg2_util.CURIE_PREFIX_UMLS
    tissues_dict = {"Ovary": "FMA:7209",
                    "Skin": "FMA:7163",
                    "Muscle": "FMA:30316",
                    "Lymphocyte": "FMA:62863",
                    "Pineal Gland": mesh + ":D010870",
                    "Teeth": "OMIM:MTHU000055",
                    "Brain": mesh + ":D001921",
                    "Cervical": cui + ":C0205064",
                    "Myocardium": "FMA:9462",
                    "Lymph Node": "FMA:5034",
                    "Cardiovascular System": "FMA:7161",
                    "Fetus": "FMA:63919",
                    "Bladder": "NCIT:C12414",
                    "Red Blood Cell": None,
                    "Beta Cell": "FMA:85704",
                    "Hepatocyte": "FMA:14515",
                    "Umbilical cord": "FMA:85541",
                    "Mast Cell": "FMA:66784",
                    "Embryo": "FMA:296970",
                    "Striatum": "FMA:77618",
                    "colon": "FMA:14543",
                    "Keratinocyte": "NCIT:C12589",
                    "Bone": "FMA:30317",
                    "Plasma": cui + ":C1609077",
                    "Adipose Tissue": "FMA:20110",
                    "Thyroid Gland": "FMA:9603",
                    "Hair": "FMA:53667",
                    "Heart": "FMA:7088",
                    "Parathyroid": cui + ":C3714631",
                    "Mouth": "FMA:49184",
                    "Thalamus": "FMA:62007",
                    "IMR-90 Cells (Fetal Lung Diploid Fibroblasts)": None,
                    "All Tissues": None,
                    "Central Nervous System": mesh + ":D002490",
                    "Leukocyte": "FMA:62852",
                    "Hippocampus": "FMA:275020",
                    "Adrenal Medulla": "FMA:15633",
                    "Cartilage": mesh + ":D002356",
                    "Stratum Corneum": "NCIT:C33625",
                    "Hypothalamus": "FMA:62008",
                    "Neutrophil": "FMA:62860",
                    "Artery": "FMA:50720",
                    "Testes": chembl + ":CHEMBL613664",
                    "Primarily Liver": None,
                    "Intestine": "FMA:7199",
                    "Spleen": "FMA:7196",
                    "Lymphoblast": "FMA:83030",
                    "Gut": None,
                    "Temporal Lobe": "FMA:61825",
                    "Large Intestine": "FMA:7201",
                    "Small Intestine": "FMA:7200",
                    "Epidermis": "FMA:70596",
                    "Basal Ganglia": mesh + ":D001479",
                    "Sperm": "CL:0000019",
                    "Uterus": "FMA:17558",
                    "Prostate": "FMA:9600",
                    "Smooth Muscle": "EFO:0000889",
                    "Spinal Cord": "FMA:7647",
                    "Vitreous humor": "NCIT:C13323",
                    "Reticulocyte": "FMA:66785",
                    "Kidney": "FMA:7203",
                    "Nervous Tissues": None,
                    "Gastrointestinal Tract": "FMA:71132",
                    "Lens": "FMA:58241",
                    "Adrenal Cortex": "FMA:15632",
                    "Blood Platelet": None,
                    "Caudate Nucleus": "FMA:61833",
                    "Neuron": "FMA:54527",
                    "Liver": "FMA:7197",
                    "Gingiva": "FMA:59762",
                    "Most Tissues": None,
                    "Fibroblasts": mesh + ":D005347",
                    "Bone Marrow": "FMA:9608",
                    "Activated T-Lymphocytes": None,
                    "Skin (Cultured Fibroblasts)": None,
                    "Platelet": "FMA:62851",
                    "Eye Lens": None,
                    "Bile": mesh + ":D001646",
                    "Pancreas": "FMA:7198",
                    "Lung": "FMA:7195",
                    "Nerve Cells": None,
                    "WI-38 Cells (Fetal Lung Diploid Fibroblasts)": None,
                    "Bile Duct": "FMA:9706",
                    "T-Lymphocyte": "NCIT:C12476",
                    "Retina": "FMA:58301",
                    "Skeletal Muscle": cui + ":C1550659",
                    "Urine": cui + ":C0042036",
                    "Myelin": "FMA:62977",
                    "Skeletal": cui + ":C0521324",
                    "Blood": cui + ":C0005767",
                    "Spermatozoa": cui + ":C0043291",
                    "Sciatic Nerve": "FMA:19034",
                    "Connective Tissue": mesh + ":D003238",
                    "Gonads": mesh + ":D006066",
                    "Adrenal Gland": "FMA:9604",
                    "Oesophagus": "EHDAA2:0001285",
                    "Erythrocyte": "FMA:62845",
                    "Tissues Containing Microbial Flora": None,
                    "Placenta": "FMA:63934",
                    "Brain Plaques": None,
                    "Gall Bladder": "UBERON:0002110",
                    "Urinary Bladder": mesh + ":D001743",
                    "Chylomicrons": cui + ":C0008731",
                    "Tongue": "FMA:54640",
                    "Caecum": cui + ":C3463927",
                    "Liver Parathyroid Gland": None,
                    "Erythroleukemia": "MEDDRA:10015282",
                    "White Blood Cells": "MEDDRA:10047955",
                    "Cerebral Cortex": "FMA:61830",
                    "Endothelium: Skin": None,
                    "Aorta": "FMA:3734",
                    "Blood Vessels": mesh + ":D001808",
                    "Erythroid Cells": mesh + ":D041905",
                    "Granulocytes": None,
                    "Gum": None,
                    "Dermis": mesh + ":D020405",
                    "Melanocyte": "FMA:70545",
                    "Endothelium (Fibroblasts)": None,
                    "Epithelium": mesh + ":D004848"}
    return tissues_dict[tissue]


def make_property_edges(metabolite: dict, hmdb_id: str):
    tissue_label = "at_tissue"
    locations_label = "at_cellular_location"
    biospecimen_label = "in_biospecimen"
    pathway_label = "in_pathway"
    update_date = metabolite["update_date"]

    edges = []
    try:
        biological_properties = metabolite["biological_properties"]
        try:
            biospecimens = (biological_properties["biospecimen_locations"]
                                                 ["biospecimen"])
        except (KeyError, TypeError):
            biospecimens = None
        try:
            locations = biological_properties["cellular_locations"]["cellular"]
        except (KeyError, TypeError):
            locations = None
        try:
            tissues = biological_properties["tissue_locations"]["tissue"]
        except (KeyError, TypeError):
            tissues = None
        try:
            pathways = biological_properties["pathways"]["pathway"]
        except (KeyError, TypeError):
            pathways = None
    except (KeyError, TypeError):
        try:
            biospecimens = metabolite["biospecimen_locations"]["biospecimen"]
        except (KeyError, TypeError):
            biospecimens = None
        try:
            locations = metabolite["cellular_locations"]["cellular"]
        except (KeyError, TypeError):
            locations = None
        try:
            tissues = metabolite["tissue_locations"]["tissue"]
        except (KeyError, TypeError):
            tissues = None
        try:
            pathways = metabolite["pathways"]["pathway"]
        except (KeyError, TypeError):
            pathways = None

    if isinstance(biospecimens, list):
        for biospecimen in biospecimens:
            try:
                object_id = biospecimen_converter(biospecimen)
            except (KeyError, TypeError):
                print("Biospecimen not found:", biospecimen)
                object_id = None
            if object_id is not None:
                edge = make_hmdb_edge(hmdb_id,
                                      object_id,
                                      CURIE_PREFIX_HMDB,
                                      None,
                                      biospecimen_label,
                                      update_date,
                                      {})
                edges.append(edge)
    elif biospecimens is not None:
        try:
            object_id = biospecimen_converter(biospecimens)
        except (KeyError, TypeError):
            print("Biospecimen not found:", biospecimens)
            object_id = None
        if object_id is not None:
            edge = make_hmdb_edge(hmdb_id,
                                  object_id,
                                  CURIE_PREFIX_HMDB,
                                  None,
                                  biospecimen_label,
                                  update_date,
                                  {})
            edges.append(edge)

    if isinstance(locations, list):
        for location in locations:
            try:
                object_id = cellular_locations_converter(location)
            except (KeyError, TypeError):
                print("Location not found:", location)
                object_id = None
            if object_id is not None:
                edge = make_hmdb_edge(hmdb_id,
                                      object_id,
                                      CURIE_PREFIX_HMDB,
                                      None,
                                      locations_label,
                                      update_date,
                                      {})
                edges.append(edge)
    elif locations is not None:
        try:
            object_id = cellular_locations_converter(locations)
        except (KeyError, TypeError):
            print("Location not found:", locations)
            object_id = None
        if object_id is not None:
            edge = make_hmdb_edge(hmdb_id,
                                  object_id,
                                  CURIE_PREFIX_HMDB,
                                  None,
                                  locations_label,
                                  update_date,
                                  {})
            edges.append(edge)

    if isinstance(tissues, list):
        for tissue in tissues:
            try:
                object_id = tissues_converter(tissue)
            except (KeyError, TypeError):
                print("Tissue not found:", tissue)
                object_id = None
            if object_id is not None:
                edge = make_hmdb_edge(hmdb_id,
                                      object_id,
                                      CURIE_PREFIX_HMDB,
                                      None,
                                      tissue_label,
                                      update_date,
                                      {})
                edges.append(edge)
    elif tissues is not None:
        try:
            object_id = tissues_converter(tissues)
        except (KeyError, TypeError):
            print("Tissue not found:", tissues)
            object_id = None
        if object_id is not None:
            edge = make_hmdb_edge(hmdb_id,
                                  object_id,
                                  CURIE_PREFIX_HMDB,
                                  None,
                                  tissue_label,
                                  update_date,
                                  {})
            edges.append(edge)

    if isinstance(pathways, list):
        for pathway in pathways:
            object_id = pathway["smpdb_id"]
            if object_id is not None:
                object_id = "SMP00" + object_id.split("SMP")[1]  # Temporary, see #976
                edge = make_hmdb_edge(hmdb_id,
                                      object_id,
                                      CURIE_PREFIX_HMDB,
                                      kg2_util.CURIE_PREFIX_SMPDB,
                                      pathway_label,
                                      update_date,
                                      {})
                edges.append(edge)
    elif pathways is not None:
        object_id = pathways["smpdb_id"]
        if object_id is not None:
            object_id = "SMP00" + object_id.split("SMP")[1]  # Temporary, see #976
            edge = make_hmdb_edge(hmdb_id,
                                  object_id,
                                  CURIE_PREFIX_HMDB,
                                  kg2_util.CURIE_PREFIX_SMPDB,
                                  pathway_label,
                                  update_date,
                                  {})
            edges.append(edge)

    return edges


if __name__ == '__main__':
    args = get_args()
    print("Script starting at", date())
    print("Starting load at", date())
    xml_file = open(args.inputFile)
    metabolite_data = xmltodict.parse(xml_file.read())
    xml_file.close()
    print("Finishing load at", date())
    locations = {}
    nodes = []
    edges = []
    tissue_dict = {}

    metabolite_count = 0

    for metabolite in metabolite_data["hmdb"]["metabolite"]:
        metabolite_count += 1

        if metabolite_count <= 10000:
            hmdb_id = metabolite["accession"]
            nodes.append(make_node(metabolite, hmdb_id))
            for edge in make_disease_edges(metabolite, hmdb_id):
                edges.append(edge)
            for edge in make_protein_edges(metabolite, hmdb_id):
                edges.append(edge)
            for edge in make_equivalencies(metabolite, hmdb_id):
                edges.append(edge)
            for edge in make_property_edges(metabolite, hmdb_id):
                edges.append(edge)
        else:
            break

    file_update_date = convert_date(os.path.getmtime(args.inputFile))
    hmdb_kp_node = kg2_util.make_node(HMDB_PROVIDED_BY_CURIE_ID,
                                      HMDB_KB_IRI,
                                      "Human Metabolome Database",
                                      kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                      file_update_date,
                                      HMDB_PROVIDED_BY_CURIE_ID)
    nodes.append(hmdb_kp_node)
    print("Saving JSON at", date())
    kg2_util.save_json({"nodes": nodes,
                        "edges": edges},
                       args.outputFile,
                       args.test)
    print("Finished saving JSON at", date())
    print("Script finished at", date())
