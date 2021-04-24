#!/usr/bin/env python3
''' smpdb_csv_to_kg_json.py: Extracts a KG2 JSON file from the
    SMPDB pathways in PWML and CSV format

    Usage: smpdb_csv_to_kg_json.py [--test] <inputDirectory>
    <outputFile.json>
'''

import csv
import kg2_util
import os
import xmltodict
import argparse


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

SMPDB_BASE_IRI = kg2_util.BASE_URL_SMPDB
SMPDB_KB_IRI = kg2_util.BASE_URL_IDENTIFIERS_ORG_REGISTRY + "smpdb"
SMPDB_PROVIDED_BY_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY \
                                + ":smpdb"


PW_BASE_IRI = kg2_util.BASE_URL_PATHWHIZ
PW_BASE_PROTEIN_COMPLEX_IRI = kg2_util.BASE_URL_PATHWHIZ_PROTEIN_COMPLEX
PW_BASE_ELEMENT_COLLECTION_IRI = kg2_util.BASE_URL_PATHWHIZ_ELEMENT_COLLECTION
PW_BASE_NUCLEIC_ACIDS_IRI = kg2_util.BASE_URL_PATHWHIZ_NUCLEIC_ACID
PW_BASE_COMPOUNDS_IRI = kg2_util.BASE_URL_PATHWHIZ_COMPOUND
PW_BASE_REACTIONS_IRI = kg2_util.BASE_URL_PATHWHIZ_REACTION
PW_BASE_BOUNDS_IRI = kg2_util.BASE_URL_PATHWHIZ_BOUND
PW_RELATION_CURIE_PREFIX = kg2_util.CURIE_PREFIX_PATHWHIZ
PW_PROVIDED_BY_CURIE_ID = kg2_util.CURIE_ID_PATHWHIZ_SOURCE


def get_args():
    arg_parser = argparse.ArgumentParser(description='smpdb_csv_to_kg_json.py: \
                                         builds a KG2 JSON representation of \
                                         SMPDB pathways using the PWML \
                                         dump and CSV files')
    arg_parser.add_argument('--test',
                            dest='test',
                            action="store_true",
                            default=False)
    arg_parser.add_argument('inputDirectory', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def make_smpdb_node(smpdb_id: str,
                    description: str,
                    name: str,
                    category_label: str,
                    publications: list,
                    csv_update_date):
    iri = SMPDB_BASE_IRI + smpdb_id
    node_curie = kg2_util.CURIE_PREFIX_SMPDB + ":" + smpdb_id
    node_dict = kg2_util.make_node(node_curie,
                                   iri,
                                   name,
                                   category_label,
                                   csv_update_date,
                                   SMPDB_PROVIDED_BY_CURIE_ID)
    node_dict["description"] = description
    if publications is not None:
        node_dict["publications"] = publications
    return node_dict


def make_pw_node(pw_id: str,
                 description: str,
                 name: str,
                 category_label: str,
                 publications: list,
                 csv_update_date):
    iri = PW_BASE_IRI + pw_id
    node_curie = kg2_util.CURIE_PREFIX_PATHWHIZ + ":" + pw_id
    node_dict = kg2_util.make_node(node_curie,
                                   iri,
                                   name,
                                   category_label,
                                   csv_update_date,
                                   PW_PROVIDED_BY_CURIE_ID)
    node_dict["description"] = description
    if publications is not None:
        node_dict["publications"] = publications
    return node_dict


def make_smpdb_nodes(smpdb, smpdb_dir: str, date):
    row = 1

    nodes_and_edges = {}

    category_label = kg2_util.BIOLINK_CATEGORY_PATHWAY

    pubfile = csv.reader(open(smpdb_dir + "SMPDB_pubmed_IDs.csv"),
                         delimiter=",",
                         quotechar='"')
    pubdic = {}
    for line in pubfile:
        if row > 1:
            publications = line[2].split(";")
            for pub in publications:
                index = publications.index(pub)
                strip = pub.strip()
                publications[index] = kg2_util.CURIE_PREFIX_PMID + ":" + strip
            pubdic[line[0]] = publications
        row += 1
    row = 1
    for line in smpdb:
        if row > 1:
            publications = []
            if line[0] in pubdic:
                publications = pubdic[line[0]]
            nodes = []
            node_smpdb = make_smpdb_node(line[0],
                                         line[4],
                                         line[2],
                                         category_label,
                                         publications,
                                         date)

            node_pw = make_pw_node(line[1],
                                   line[4],
                                   line[2],
                                   category_label,
                                   publications,
                                   date)
            nodes.append(node_smpdb)
            nodes.append(node_pw)
            predicate_label = kg2_util.EDGE_LABEL_BIOLINK_SAME_AS
            edge = make_pw_edge(line[0],
                                line[1],
                                predicate_label,
                                kg2_util.CURIE_PREFIX_SMPDB,
                                kg2_util.CURIE_PREFIX_PATHWHIZ,
                                date=date)
            nodes_and_edges[line[1]] = {"nodes": nodes, "edges": edge}
        row += 1

    return nodes_and_edges


def make_pw_edge(subject_id: str,
                 object_id: str,
                 predicate_label: str,
                 subject_prefix: str,
                 object_prefix: str,
                 description=None,
                 publications_info=None,
                 date=None):
    relation_curie = kg2_util.predicate_label_to_curie(predicate_label,
                                                       PW_RELATION_CURIE_PREFIX)

    if subject_prefix is not None:
        subject_id = subject_prefix + ":" + subject_id
    if object_prefix is not None:
        object_id = object_prefix + ":" + object_id

    if predicate_label == kg2_util.EDGE_LABEL_BIOLINK_SAME_AS:
        edge = kg2_util.make_edge_biolink(subject_id,
                                          object_id,
                                          predicate_label,
                                          PW_PROVIDED_BY_CURIE_ID,
                                          date)
    else:
        edge = kg2_util.make_edge(subject_id,
                                  object_id,
                                  relation_curie,
                                  predicate_label,
                                  PW_PROVIDED_BY_CURIE_ID,
                                  date)
    if description is not None:
        edge["publications_info"]["sentences"] = description
    if publications_info is not None:
        edge["publications_info"] = publications_info
    return edge


def equivocate(id_prefixes: dict,
               ids: list,
               eq_label: str,
               date=None):
    edges = []
    index = 0
    while index < len(ids):
        subject_id = ids[index]
        subject_prefix = id_prefixes[subject_id]
        for obj in ids[(index + 1):]:
            object_prefix = id_prefixes[obj]
            edges.append(make_pw_edge(subject_id,
                                      obj,
                                      eq_label,
                                      subject_prefix,
                                      object_prefix,
                                      date=date))
        index += 1

    return edges


def part_of_edges(main_id: str,
                  ids: list,
                  part_of_label: str,
                  id_prefixes: str,
                  main_id_prefix: str,
                  description=None,
                  publications_info=None,
                  date=None):
    edges = []

    for object_id in ids:
        edge = make_pw_edge(main_id,
                            object_id,
                            part_of_label,
                            main_id_prefix,
                            id_prefixes[object_id],
                            description=description,
                            publications_info=publications_info,
                            date=date)
        edges.append(edge)

    return edges


def add_if_string(id_dict: dict, id_list: list, id, prefix):
    if isinstance(id, str):
        id_list.append(id)
        id_dict[id] = prefix


def per_compound_nodes_and_edges(compound: dict, pw_id: str, date):
    equivalent_label = kg2_util.EDGE_LABEL_BIOLINK_SAME_AS
    in_pathway_label = "has_compound"

    nodes = []
    edges = []

    pwc_id = compound["id"]["#text"]
    name = compound["name"]
    category_label = kg2_util.BIOLINK_CATEGORY_CHEMICAL_SUBSTANCE
    description = compound["description"]
    iri = PW_BASE_COMPOUNDS_IRI + pwc_id
    node_curie = kg2_util.CURIE_PREFIX_PATHWHIZ_COMPOUND + ":" + pwc_id
    publications = []
    if isinstance(description, str) and \
       len(description.split("PMID")) > 1:
        splits = description.split("PMID")
        for item in splits:
            if item.startswith(":") or item.startswith(" "):
                ids = item.split(")")
                ids = ids[0].split(",")
                for id in ids:
                    if id.startswith(": "):
                        id = id[2:]
                    publications.append(kg2_util.CURIE_PREFIX_PMID + ":" +
                                        id.strip())
    node = kg2_util.make_node(node_curie,
                              iri,
                              name,
                              category_label,
                              date,
                              PW_PROVIDED_BY_CURIE_ID)
    if isinstance(description, str):
        node["description"] = description
    node["publications"] = publications
    if isinstance(compound["synonyms"], str):
        node["synonym"] = compound["synonyms"].split(";")
    nodes.append(node)

    chebi_id = compound["chebi-id"]
    drugbank_id = compound["drugbank-id"]
    kegg_id = compound["kegg-id"]

    id_list = []
    id_prefixes = {}

    add_if_string(id_prefixes,
                  id_list,
                  pwc_id,
                  kg2_util.CURIE_PREFIX_PATHWHIZ_COMPOUND)

    add_if_string(id_prefixes,
                  id_list,
                  chebi_id,
                  kg2_util.CURIE_PREFIX_CHEBI)

    add_if_string(id_prefixes,
                  id_list,
                  drugbank_id,
                  kg2_util.CURIE_PREFIX_DRUGBANK)

    add_if_string(id_prefixes,
                  id_list,
                  kegg_id,
                  kg2_util.CURIE_PREFIX_KEGG)

    for edge in equivocate(id_prefixes,
                           id_list,
                           equivalent_label,
                           date=date):
        edges.append(edge)

    for edge in part_of_edges(pw_id,
                              id_list,
                              in_pathway_label,
                              id_prefixes,
                              kg2_util.CURIE_PREFIX_PATHWHIZ,
                              date=date):
        edges.append(edge)

    compound_translator = {}

    for id in id_list:
        compound_translator[id] = id_prefixes[id]

    return [{"nodes": nodes,
             "edges": edges},
            {pwc_id: compound_translator}]


def make_compound_nodes_and_edges(pw_context: dict, pw_id: str, date):
    compounds = None
    if pw_context["compounds"] is not None:
        compounds = pw_context["compounds"]["compound"]
    else:
        return [None, None]

    nodes = []
    edges = []
    compound_translator = {}
    if isinstance(compounds, list):
        for compound in compounds:
            [compound_data,
             translator_instance] = per_compound_nodes_and_edges(compound,
                                                                 pw_id,
                                                                 date)
            if compound_data is not None:
                for node in compound_data["nodes"]:
                    nodes.append(node)
                for edge in compound_data["edges"]:
                    edges.append(edge)
            for key in translator_instance:
                compound_translator[key] = translator_instance[key]
    else:
        [compound_data,
         translator_instance] = per_compound_nodes_and_edges(compounds,
                                                             pw_id,
                                                             date)
        if compound_data is not None:
            for node in compound_data["nodes"]:
                nodes.append(node)
            for edge in compound_data["edges"]:
                edges.append(edge)
        for key in translator_instance:
            compound_translator[key] = translator_instance[key]

    return [{"nodes": nodes,
            "edges": edges},
            compound_translator]


def per_nucleic_acid_nodes_and_edges(nucl_acid: dict, pw_id: str, date):
    equivalent_label = kg2_util.EDGE_LABEL_BIOLINK_SAME_AS
    in_pathway_label = "has_nucleic_acid"

    chebi_id = nucl_acid["chebi-id"]
    pwna_id = nucl_acid["id"]["#text"]

    id_list = []
    id_prefixes = {}

    nodes = []
    edges = []

    name = nucl_acid["name"]
    category_label = kg2_util.BIOLINK_CATEGORY_GENOMIC_ENTITY
    iri = PW_BASE_NUCLEIC_ACIDS_IRI + pwna_id
    node_curie = kg2_util.CURIE_PREFIX_PATHWHIZ_NUCLEIC_ACID + ":" + pwna_id
    node = kg2_util.make_node(node_curie,
                              iri,
                              name,
                              category_label,
                              date,
                              PW_PROVIDED_BY_CURIE_ID)
    nodes.append(node)

    add_if_string(id_prefixes,
                  id_list,
                  pwna_id,
                  kg2_util.CURIE_PREFIX_PATHWHIZ_NUCLEIC_ACID)
    add_if_string(id_prefixes,
                  id_list,
                  chebi_id,
                  kg2_util.CURIE_PREFIX_CHEBI)

    for edge in equivocate(id_prefixes,
                           id_list,
                           equivalent_label,
                           date=date):
        edges.append(edge)

    for edge in part_of_edges(pw_id,
                              id_list,
                              in_pathway_label,
                              id_prefixes,
                              kg2_util.CURIE_PREFIX_PATHWHIZ,
                              date=date):
        edges.append(edge)

    nucl_acid_translator = {}

    for id in id_list:
        nucl_acid_translator[id] = id_prefixes[id]

    return [{"nodes": nodes,
            "edges": edges},
            {pwna_id: nucl_acid_translator}]


def make_nucleic_acid_nodes_and_edges(pw_context: dict, pw_id: str, date):
    nucl_acids = None
    if pw_context["nucleic-acids"] is not None:
        nucl_acids = pw_context["nucleic-acids"]["nucleic-acid"]
    else:
        return [None, None]
    nodes = []
    edges = []
    nucl_acid_translator = {}
    if isinstance(nucl_acids, list):
        for nucl_acid in nucl_acids:
            [nucl_acid_data,
             translator_instance] = per_nucleic_acid_nodes_and_edges(nucl_acid,
                                                                     pw_id,
                                                                     date)
            if nucl_acid_data is not None:
                for node in nucl_acid_data["nodes"]:
                    nodes.append(node)
                for edge in nucl_acid_data["edges"]:
                    edges.append(edge)
            for key in translator_instance:
                nucl_acid_translator[key] = translator_instance[key]
    else:
        [nucl_acid_data,
         translator_instance] = per_nucleic_acid_nodes_and_edges(nucl_acids,
                                                                 pw_id,
                                                                 date)
        if nucl_acid_data is not None:
            for node in nucl_acid_data["nodes"]:
                nodes.append(node)
            for edge in nucl_acid_data["edges"]:
                edges.append(edge)
        for key in translator_instance:
            nucl_acid_translator[key] = translator_instance[key]

    return [{"nodes": nodes,
            "edges": edges},
            nucl_acid_translator]


def per_protein_nodes_and_edges(protein: dict, pw_id: str, date):
    nodes = []
    edges = []
    equivalent_label = kg2_util.EDGE_LABEL_BIOLINK_SAME_AS
    in_pathway_label = "has_protein"

    protein_translator = {}

    protein_pw_id = protein["id"]["#text"]
    uniprot_id = protein["uniprot-id"]
    drugbank_id = protein["drugbank-id"]
#    description = protein["description"]

    publications_info = {}
    '''
    if isinstance(description, dict):
        description = None
    elif description is not None:
        pmids = description.split("PubMed")
        if len(pmids) > 1:
            for item in pmids:
                if item.startswith(":") or item.startswith(" "):
                    split = item.split(")")
                    publication = "PMID:" + split[0][1:]
                    publications.append(publication)
                    sentence_index = pmids.index(item) - 1
                    if sentence_index == 0:
                        publications_info[publication] = {}
                        sentence = pmids[sentence_index].rstrip(" (")
                        (publications_info[publication]
                                          ["sentence"]) = sentence
                    else:
                        sentence = pmids[sentence_index].split(" ", 1)
                        sentence = sentence[1]
                        sentence = sentence.rstrip(" (")
                        publications_info[publication] = {}
                        (publications_info[publication]
                                          ["sentence"]) = sentence
    if len(publications_info) > 0:
        description = None
    '''
    id_list = []
    id_prefixes = {}

    add_if_string(id_prefixes,
                  id_list,
                  uniprot_id,
                  kg2_util.CURIE_PREFIX_UNIPROT)
    add_if_string(id_prefixes,
                  id_list,
                  drugbank_id,
                  kg2_util.CURIE_PREFIX_DRUGBANK)

    for id in id_list:
        protein_translator[protein_pw_id] = {id: id_prefixes[id]}

    for edge in equivocate(id_prefixes,
                           id_list,
                           equivalent_label,
                           date=date):
        edges.append(edge)

    for edge in part_of_edges(pw_id,
                              id_list,
                              in_pathway_label,
                              id_prefixes,
                              kg2_util.CURIE_PREFIX_PATHWHIZ,
                              description=None,
                              publications_info=publications_info,
                              date=date):
        edges.append(edge)

    return [{"nodes": nodes,
             "edges": edges},
            protein_translator]


def per_protein_complex_nodes_and_edges(protein_complex: dict,
                                        pw_id: str,
                                        protein_translator: dict,
                                        date):
    has_protein_in_complex_label = "has_protein_in_complex"

    nodes = []
    edges = []

    pwp_id = protein_complex["id"]["#text"]
    name = protein_complex["name"]
    iri = PW_BASE_PROTEIN_COMPLEX_IRI + pwp_id
    category_label = kg2_util.BIOLINK_CATEGORY_MOLECULAR_ENTITY
    node_curie = kg2_util.CURIE_PREFIX_PATHWHIZ_PROTEIN_COMPLEX + ":" + pwp_id
    node = kg2_util.make_node(node_curie,
                              iri,
                              name,
                              category_label,
                              date,
                              PW_PROVIDED_BY_CURIE_ID)
    nodes.append(node)
    prefixes_in_complex = {}
    if "protein_complex-proteins" in protein_complex:
        complex_proteins = protein_complex["protein_complex-proteins"]
        complexes = complex_proteins["protein-complex-protein"]
    else:
        return [None, None]
    proteins_in_complex = []
    if isinstance(complexes, list):
        for protein in complexes:
            protein_id = protein["protein-id"]["#text"]
            for key in protein_translator[protein_id]:
                prefixes_in_complex[key] = protein_translator[protein_id][key]
                proteins_in_complex.append(key)
    else:
        protein_id = complexes["protein-id"]["#text"]
        for key in protein_translator[protein_id]:
            prefixes_in_complex[key] = protein_translator[protein_id][key]
            proteins_in_complex.append(key)

    for edge in part_of_edges(pwp_id,
                              proteins_in_complex,
                              has_protein_in_complex_label,
                              prefixes_in_complex,
                              kg2_util.CURIE_PREFIX_PATHWHIZ_PROTEIN_COMPLEX,
                              date=date):
        edges.append(edge)

    return [{"nodes": nodes,
             "edges": edges},
            {pwp_id: {pwp_id:
                      kg2_util.CURIE_PREFIX_PATHWHIZ_PROTEIN_COMPLEX}}]


def make_protein_nodes_and_edges(pw_context: dict, pw_id: str, date):
    proteins = None
    if pw_context["proteins"] is not None:
        proteins = pw_context["proteins"]["protein"]
    else:
        return [None, None, None]
    nodes = []
    edges = []

    protein_translator = {}
    if isinstance(proteins, list):
        for protein in proteins:
            [protein_data,
             translator_instance] = per_protein_nodes_and_edges(protein,
                                                                pw_id,
                                                                date)
            if protein_data is not None:
                for node in protein_data["nodes"]:
                    nodes.append(node)
                for edge in protein_data["edges"]:
                    edges.append(edge)
            for key in translator_instance:
                protein_translator[key] = translator_instance[key]
    else:
        [protein_data,
         translator_instance] = per_protein_nodes_and_edges(proteins,
                                                            pw_id,
                                                            date)
        if protein_data is not None:
            for node in protein_data["nodes"]:
                nodes.append(node)
            for edge in protein_data["edges"]:
                edges.append(edge)
        for key in translator_instance:
            protein_translator[key] = translator_instance[key]

    protein_complexes = None
    if pw_context["protein-complexes"] is not None:
        protein_complexes = pw_context["protein-complexes"]["protein-complex"]
    else:
        return [{"nodes": nodes,
                "edges": edges}, protein_translator, None]
    protein_complex_translator = {}
    if isinstance(protein_complexes, list):
        for protein_complex in protein_complexes:
            [protein_complex_data,
             translator_instance] = per_protein_complex_nodes_and_edges(protein_complex,
                                                                        pw_id,
                                                                        protein_translator,
                                                                        date)
            if protein_complex_data is not None:
                for node in protein_complex_data["nodes"]:
                    nodes.append(node)
                for edge in protein_complex_data["edges"]:
                    edges.append(edge)
            if translator_instance is not None:
                for key in translator_instance:
                    protein_complex_translator[key] = translator_instance[key]

    else:
        [protein_complex_data,
         translator_instance] = per_protein_complex_nodes_and_edges(protein_complexes,
                                                                    pw_id,
                                                                    protein_translator,
                                                                    date)
        if protein_complex_data is not None:
            for node in protein_complex_data["nodes"]:
                nodes.append(node)
            for edge in protein_complex_data["edges"]:
                edges.append(edge)
        if translator_instance is not None:
            for key in translator_instance:
                protein_complex_translator[key] = translator_instance[key]

    return [{"nodes": nodes,
            "edges": edges},
            protein_translator,
            protein_complex_translator]


def make_location_nodes_and_edges(pw_context: dict, pw_id: str, date):
    at_label = "has_location"
    query = "ontology-id"

    locations = None
    if pw_context["subcellular-locations"] is not None:
        locations = pw_context["subcellular-locations"]["subcellular-location"]
    else:
        return None
    nodes = []
    edges = []

    if isinstance(locations, list):
        for location in locations:
            location_data = per_place_nodes_and_edges(location,
                                                      pw_id,
                                                      at_label,
                                                      query,
                                                      date=date)
            for node in location_data["nodes"]:
                nodes.append(node)
            for edge in location_data["edges"]:
                edges.append(edge)
    else:
        location_data = per_place_nodes_and_edges(locations,
                                                  pw_id,
                                                  at_label,
                                                  query,
                                                  date=date)
        for node in location_data["nodes"]:
            nodes.append(node)
        for edge in location_data["edges"]:
            edges.append(edge)

    return {"nodes": nodes,
            "edges": edges}


def per_place_nodes_and_edges(tissue: dict,
                              pw_id: str,
                              at_label: str,
                              query: str,
                              prefix=None,
                              date=None):
    nodes = []
    edges = []

    if isinstance(tissue, dict):
        ontology_id = tissue[query]

        id_list = []
        id_prefixes = {}

        add_if_string(id_prefixes, id_list, ontology_id, prefix)

        for edge in part_of_edges(pw_id,
                                  id_list,
                                  at_label,
                                  id_prefixes,
                                  kg2_util.CURIE_PREFIX_PATHWHIZ,
                                  date=date):
            edges.append(edge)

    return {"nodes": nodes,
            "edges": edges}


def make_tissue_nodes_and_edges(pw_context: dict, pw_id: str, date):
    at_label = "uses_tissue"
    query = "ontology-id"

    tissues = None
    if pw_context["tissues"] is not None:
        tissues = pw_context["tissues"]["tissue"]
    else:
        return None
    nodes = []
    edges = []

    if isinstance(tissues, list):
        for tissue in tissues:
            tissue_data = per_place_nodes_and_edges(tissue,
                                                    pw_id,
                                                    at_label,
                                                    query,
                                                    date=date)
            for node in tissue_data["nodes"]:
                nodes.append(node)
            for edge in tissue_data["edges"]:
                edges.append(edge)
    else:
        tissue_data = per_place_nodes_and_edges(tissues,
                                                pw_id,
                                                at_label,
                                                query,
                                                date=date)
        for node in tissue_data["nodes"]:
            nodes.append(node)
        for edge in tissue_data["edges"]:
            edges.append(edge)

    return {"nodes": nodes,
            "edges": edges}


def make_species_nodes_and_edges(pw_context: dict, pw_id: str, date):
    at_label = "in_species"
    query = "taxonomy-id"

    species = None
    if pw_context["species"] is not None:
        species = pw_context["species"]["species"]
    else:
        return None
    nodes = []
    edges = []

    if isinstance(species, list):
        for specie in species:
            species_data = per_place_nodes_and_edges(specie,
                                                     pw_id,
                                                     at_label,
                                                     query,
                                                     kg2_util.CURIE_PREFIX_NCBI_TAXON,
                                                     date=date)
            for node in species_data["nodes"]:
                nodes.append(node)
            for edge in species_data["edges"]:
                edges.append(edge)
    else:
        species_data = per_place_nodes_and_edges(species,
                                                 pw_id,
                                                 at_label,
                                                 query,
                                                 kg2_util.CURIE_PREFIX_NCBI_TAXON,
                                                 date=date)
        for node in species_data["nodes"]:
            nodes.append(node)
        for edge in species_data["edges"]:
            edges.append(edge)

    return {"nodes": nodes,
            "edges": edges}


def create_edges_from_element(element: dict,
                              predicate_label: str,
                              main_id: str,
                              data_translator: dict,
                              pw_id,
                              date):
    edges = []
    element_id = element["element-id"]["#text"]
    element_type = element["element-type"]
    try:
        id_prefixes = data_translator[element_type][element_id]
    except:
        return edges
    id_list = id_prefixes.keys()
    for edge in part_of_edges(main_id,
                              id_list,
                              predicate_label,
                              id_prefixes,
                              kg2_util.CURIE_PREFIX_PATHWHIZ_REACTION,
                              date=date):
        edges.append(edge)
    return edges


def per_reaction_nodes_and_edges(reaction: dict,
                                 pw_id: str,
                                 data_translator: dict,
                                 date):
    left_label = "has_left_element"
    right_label = "has_right_element"
    enzyme_label = "has_enzyme"
    in_pathway_label = "has_reaction"

    nodes = []
    edges = []

    pwr_id = reaction["id"]["#text"]
    name = None
    category_label = kg2_util.BIOLINK_CATEGORY_MOLECULAR_ACTIVITY
    iri = PW_BASE_REACTIONS_IRI + pwr_id
    node_curie = kg2_util.CURIE_PREFIX_PATHWHIZ_REACTION + ":" + pwr_id
    node = kg2_util.make_node(node_curie,
                              iri,
                              name,
                              category_label,
                              date,
                              PW_PROVIDED_BY_CURIE_ID)

    nodes.append(node)

    left_elements = (reaction["reaction-left-elements"]
                             ["reaction-left-element"])
    right_elements = (reaction["reaction-right-elements"]
                              ["reaction-right-element"])
    if "reaction-enzymes" in reaction:
        enzymes = reaction["reaction-enzymes"]["reaction-enzyme"]
    else:
        enzymes = None

    if isinstance(left_elements, list):
        for left_element in left_elements:
            for edge in create_edges_from_element(left_element,
                                                  left_label,
                                                  pwr_id,
                                                  data_translator,
                                                  pw_id,
                                                  date):
                edges.append(edge)
    else:
        for edge in create_edges_from_element(left_elements,
                                              left_label,
                                              pwr_id,
                                              data_translator,
                                              pw_id,
                                              date):
            edges.append(edge)

    if isinstance(right_elements, list):
        for right_element in right_elements:
            for edge in create_edges_from_element(right_element,
                                                  right_label,
                                                  pwr_id,
                                                  data_translator,
                                                  pw_id,
                                                  date):
                edges.append(edge)
    else:
        for edge in create_edges_from_element(right_elements,
                                              right_label,
                                              pwr_id,
                                              data_translator,
                                              pw_id,
                                              date):
            edges.append(edge)

    if isinstance(enzymes, list):
        for enzyme in enzymes:
            element_id = enzyme["protein-complex-id"]["#text"]
            element_type = "ProteinComplex"
            try:
                id_prefixes = data_translator[element_type][element_id]
            except:
                continue
            id_list = id_prefixes.keys()
            for edge in part_of_edges(pwr_id,
                                      id_list,
                                      enzyme_label,
                                      id_prefixes,
                                      kg2_util.CURIE_PREFIX_PATHWHIZ_REACTION,
                                      date=date):
                edges.append(edge)

    elif enzymes is not None:
        element_id = enzymes["protein-complex-id"]["#text"]
        element_type = "ProteinComplex"
        try:
            id_prefixes = data_translator[element_type][element_id]
        except:
            id_prefixes = {}
        id_list = id_prefixes.keys()
        for edge in part_of_edges(pwr_id,
                                  id_list,
                                  enzyme_label,
                                  id_prefixes,
                                  kg2_util.CURIE_PREFIX_PATHWHIZ_REACTION,
                                  date=date):
            edges.append(edge)

    for edge in part_of_edges(pw_id,
                              [pwr_id],
                              in_pathway_label,
                              {pwr_id:
                               kg2_util.CURIE_PREFIX_PATHWHIZ_REACTION},
                              kg2_util.CURIE_PREFIX_PATHWHIZ,
                              date=date):
        edges.append(edge)

    return {"nodes": nodes,
            "edges": edges}


def make_reaction_nodes_and_edges(pw_context: dict,
                                  pw_id: str,
                                  data_translator: dict,
                                  date):
    reactions = None
    if pw_context["reactions"] is not None:
        reactions = pw_context["reactions"]["reaction"]
    else:
        return None
    nodes = []
    edges = []

    if isinstance(reactions, list):
        for reaction in reactions:
            reaction_data = per_reaction_nodes_and_edges(reaction,
                                                         pw_id,
                                                         data_translator,
                                                         date)
            if reaction_data is not None:
                for node in reaction_data["nodes"]:
                    nodes.append(node)
                for edge in reaction_data["edges"]:
                    edges.append(edge)
    else:
        reaction_data = per_reaction_nodes_and_edges(reactions,
                                                     pw_id,
                                                     data_translator,
                                                     date)
        if reaction_data is not None:
            for node in reaction_data["nodes"]:
                nodes.append(node)
            for edge in reaction_data["edges"]:
                edges.append(edge)
    return {"nodes": nodes,
            "edges": edges}


def per_bound_nodes_and_edges(bound: dict,
                              pw_id: str,
                              data_translator: dict,
                              date):
    in_pathway_label = "has_bound"
    in_bound_label = "has_element_in_bound"

    nodes = []
    edges = []

    pwb_id = bound["id"]["#text"]
    name = None
    iri = PW_BASE_BOUNDS_IRI + pwb_id
    category_label = kg2_util.BIOLINK_CATEGORY_MOLECULAR_ENTITY
    node_curie = kg2_util.CURIE_PREFIX_PATHWHIZ_BOUND + ":" + pwb_id
    node = kg2_util.make_node(node_curie,
                              iri,
                              name,
                              category_label,
                              date,
                              PW_PROVIDED_BY_CURIE_ID)
    nodes.append(node)

    elements = bound["bound-elements"]["bound-element"]
    if isinstance(elements, list):
        for element in elements:
            element_id = element["element-id"]["#text"]
            element_type = element["element-type"]
            id_prefixes = data_translator[element_type][element_id]
            id_list = id_prefixes.keys()
            for edge in part_of_edges(pwb_id,
                                      id_list,
                                      in_bound_label,
                                      id_prefixes,
                                      kg2_util.CURIE_PREFIX_PATHWHIZ_BOUND,
                                      date=date):
                edges.append(edge)
    else:
        element_id = element["element-id"]["#text"]
        element_type = element["element-type"]
        id_prefixes = data_translator[element_type][element_id]
        id_list = id_prefixes.keys()
        for edge in part_of_edges(pwb_id,
                                  id_list,
                                  in_bound_label,
                                  id_prefixes,
                                  kg2_util.CURIE_PREFIX_PATHWHIZ_BOUND,
                                  date=date):
            edges.append(edge)

    for edge in part_of_edges(pw_id,
                              [pwb_id],
                              in_pathway_label,
                              {pwb_id: kg2_util.CURIE_PREFIX_PATHWHIZ_BOUND},
                              kg2_util.CURIE_PREFIX_PATHWHIZ,
                              date=date):
        edges.append(edge)

    return [{"nodes": nodes,
             "edges": edges},
            {pwb_id: {pwb_id: kg2_util.CURIE_PREFIX_PATHWHIZ_BOUND}}]


def make_bound_nodes_and_edges(pw_context: dict,
                               pw_id: str,
                               data_translator: dict,
                               date):
    bounds = None
    if pw_context["bounds"] is not None:
        bounds = pw_context["bounds"]["bound"]
    else:
        return [None, None]
    nodes = []
    edges = []

    bound_translator = {}

    if isinstance(bounds, list):
        for bound in bounds:
            [bounds_data,
             translator_instance] = per_bound_nodes_and_edges(bound,
                                                              pw_id,
                                                              data_translator,
                                                              date)
            if bounds_data is not None:
                for node in bounds_data["nodes"]:
                    nodes.append(node)
                for edge in bounds_data["edges"]:
                    edges.append(edge)
            for key in translator_instance:
                bound_translator[key] = translator_instance[key]
    else:
        [bounds_data,
         translator_instance] = per_bound_nodes_and_edges(bounds,
                                                          pw_id,
                                                          data_translator,
                                                          date)
        if bounds_data is not None:
            for node in bounds_data["nodes"]:
                nodes.append(node)
            for edge in bounds_data["edges"]:
                edges.append(edge)
        for key in translator_instance:
            bound_translator[key] = translator_instance[key]

    return [{"nodes": nodes,
             "edges": edges},
            bound_translator]


def per_element_collection_nodes_and_edges(ec: dict, pw_id: str, date):
    equivalent_label = kg2_util.EDGE_LABEL_BIOLINK_SAME_AS
    in_pathway_label = "has_element_collection"
    nodes = []
    edges = []

    name = ec["name"]
    pwec_id = ec["id"]["#text"]
    iri = PW_BASE_ELEMENT_COLLECTION_IRI + pwec_id
    node_curie = kg2_util.CURIE_PREFIX_PATHWHIZ_ELEMENT_COLLECTION + \
        ":" + pwec_id
    category_label = kg2_util.BIOLINK_CATEGORY_MOLECULAR_ENTITY
    node = kg2_util.make_node(node_curie,
                              iri,
                              name,
                              category_label,
                              date,
                              PW_PROVIDED_BY_CURIE_ID)
    nodes.append(node)

    id_list = []
    id_prefixes = {}

    external_id_translator = {"KEGG Compound": kg2_util.CURIE_PREFIX_KEGG,
                              "ChEBI": kg2_util.CURIE_PREFIX_CHEBI,
                              "UniProt": kg2_util.CURIE_PREFIX_UNIPROT,
                              "Nothing": None,
                              "PubChem-compound": None}

    if isinstance(ec["external-id-type"], dict):
        ec["external-id-type"] = "Nothing"
    add_if_string(id_prefixes,
                  id_list,
                  pwec_id,
                  kg2_util.CURIE_PREFIX_PATHWHIZ_ELEMENT_COLLECTION)
    if external_id_translator[ec["external-id-type"]] is not None:
        add_if_string(id_prefixes,
                      id_list,
                      ec["external-id"],
                      external_id_translator[ec["external-id-type"]])

    for edge in equivocate(id_prefixes, id_list, equivalent_label, date=date):
        edges.append(edge)
    for edge in part_of_edges(pw_id,
                              id_list,
                              in_pathway_label,
                              id_prefixes,
                              kg2_util.CURIE_PREFIX_PATHWHIZ,
                              date=date):
        edges.append(edge)

    ec_translator = {}
    for id in id_list:
        ec_translator[id] = id_prefixes[id]

    return [{"nodes": nodes,
             "edges": edges},
            {pwec_id: ec_translator}]


def make_element_collection_nodes_and_edges(pw_context: dict,
                                            pw_id: str,
                                            date):
    ecs = None
    if pw_context["element-collections"] is not None:
        ecs = pw_context["element-collections"]["element-collection"]
    else:
        return [None, None]
    nodes = []
    edges = []

    ec_translator = {}

    if isinstance(ecs, list):
        for ec in ecs:
            [ec_data,
             translator_instance] = per_element_collection_nodes_and_edges(ec,
                                                                           pw_id,
                                                                           date)
            if ec_data is not None:
                for node in ec_data["nodes"]:
                    nodes.append(node)
                for edge in ec_data["edges"]:
                    edges.append(edge)
            for key in translator_instance:
                ec_translator[key] = translator_instance[key]
    else:
        [ec_data,
         translator_instance] = per_element_collection_nodes_and_edges(ecs,
                                                                       pw_id,
                                                                       date)
        if ec_data is not None:
            for node in ec_data["nodes"]:
                nodes.append(node)
            for edge in ec_data["edges"]:
                edges.append(edge)
        for key in translator_instance:
            ec_translator[key] = translator_instance[key]

    return [{"nodes": nodes,
             "edges": edges},
            ec_translator]


def add_publications_to_nodes(pw_context: dict, smpdb_nodes: list):
    publications = []

    try:
        references = pw_context["pathway"]["references"]
    except:
        return smpdb_nodes

    if isinstance(references, list):
        for reference in references:
            pubmed_id = reference["reference"]["pubmed-id"]
            if isinstance(pubmed_id, str):
                publications.append(kg2_util.CURIE_PREFIX_PMID +
                                    ":" + pubmed_id)
    else:
        pubmed_id = references["reference"]["pubmed-id"]
        if isinstance(pubmed_id, str):
            publications.append(kg2_util.CURIE_PREFIX_PMID + ":" + pubmed_id)
    for node in smpdb_nodes:
        for publication in publications:
            if (publication in node["publications"]) is False:
                node["publications"].append(publication)

    return smpdb_nodes


def make_nodes_and_edges(context,
                         pathway_id,
                         smpdb_data_pathway,
                         date):
    nodes = []
    edges = []

    data_translator = {}

    [compounds,
     compound_translator] = make_compound_nodes_and_edges(context,
                                                          pathway_id,
                                                          date)
    if compounds is not None:
        for node in compounds["nodes"]:
            nodes.append(node)
        for edge in compounds["edges"]:
            edges.append(edge)

    data_translator["Compound"] = compound_translator

    [nucl_acids,
     nucl_acid_translator] = make_nucleic_acid_nodes_and_edges(context,
                                                               pathway_id,
                                                               date)
    if nucl_acids is not None:
        for node in nucl_acids["nodes"]:
            nodes.append(node)
        for edge in nucl_acids["edges"]:
            edges.append(edge)

    data_translator["NucleicAcid"] = nucl_acid_translator

    [proteins,
     protein_translator,
     protein_complex_translator] = make_protein_nodes_and_edges(context,
                                                                pathway_id,
                                                                date)
    if proteins is not None:
        for node in proteins["nodes"]:
            nodes.append(node)
        for edge in proteins["edges"]:
            edges.append(edge)

    data_translator["Protein"] = protein_translator
    data_translator["ProteinComplex"] = protein_complex_translator

    locations = make_location_nodes_and_edges(context, pathway_id, date)
    if locations is not None:
        for node in locations["nodes"]:
            nodes.append(node)
        for edge in locations["edges"]:
            edges.append(edge)

    tissues = make_tissue_nodes_and_edges(context, pathway_id, date)
    if tissues is not None:
        for node in tissues["nodes"]:
            nodes.append(node)
        for edge in tissues["edges"]:
            edges.append(edge)

    species = make_species_nodes_and_edges(context, pathway_id, date)
    if species is not None:
        for node in species["nodes"]:
            nodes.append(node)
        for edge in species["edges"]:
            edges.append(edge)

    [ecs,
     ec_translator] = make_element_collection_nodes_and_edges(context,
                                                              pathway_id,
                                                              date)
    if ecs is not None:
        for node in ecs["nodes"]:
            nodes.append(node)
        for edge in ecs["edges"]:
            edges.append(edge)
    data_translator["ElementCollection"] = ec_translator

    [bounds,
     bounds_translator] = make_bound_nodes_and_edges(context,
                                                     pathway_id,
                                                     data_translator,
                                                     date)
    if bounds is not None:
        for node in bounds["nodes"]:
            nodes.append(node)
        for edge in bounds["edges"]:
            edges.append(edge)
    data_translator["Bound"] = bounds_translator

    reactions = make_reaction_nodes_and_edges(context,
                                              pathway_id,
                                              data_translator,
                                              date)
    if reactions is not None:
        for node in reactions["nodes"]:
            nodes.append(node)
        for edge in reactions["edges"]:
            edges.append(edge)

    smpdb_nodes = add_publications_to_nodes(context,
                                            smpdb_data_pathway["nodes"])
    for node in smpdb_nodes:
        nodes.append(node)

    return {"nodes": nodes,
            "edges": edges}


def make_kg2_graph(smpdb_dir: str, test_mode: bool):
    csv_update_date = kg2_util.convert_date(os.path.getmtime(smpdb_dir +
                                                             "pathbank_pathways.csv"))
    smpdb = csv.reader(open(smpdb_dir + "pathbank_pathways.csv"),
                       delimiter=",",
                       quotechar='"')
    smpdb_kp_node = kg2_util.make_node(SMPDB_PROVIDED_BY_CURIE_ID,
                                       SMPDB_KB_IRI,
                                       "Small Molecule Pathway Database",
                                       kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                       csv_update_date,
                                       SMPDB_PROVIDED_BY_CURIE_ID)
    pw_kp_node = kg2_util.make_node(PW_PROVIDED_BY_CURIE_ID,
                                    PW_BASE_IRI,
                                    "PathWhiz",
                                    kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                    csv_update_date,
                                    PW_PROVIDED_BY_CURIE_ID)
    nodes = []
    edges = []

    smpdb_data = make_smpdb_nodes(smpdb, smpdb_dir, csv_update_date)
    for file in smpdb_data:
        edges.append(smpdb_data[file]["edges"])

    count = 0
    for filename in os.listdir(smpdb_dir):
        count += 1
        if count % 1000 == 0:
            print(count, " files have been read by ", kg2_util.date())
        if count == 2000 and test_mode:
            break
        if ".pwml" in filename:
            file = open(smpdb_dir + filename)
            try:
                pw = xmltodict.parse(file.read())
            except:
                print(filename)
                continue
            file.close()
            if ("super-pathway-visualization" in pw and
                isinstance(pw["super-pathway-visualization"], dict) and
                isinstance((pw["super-pathway-visualization"]
                              ["pathway-visualization-contexts"]), dict) and
                isinstance((pw["super-pathway-visualization"]
                              ["pathway-visualization-contexts"]
                              ["pathway-visualization-context"]), dict)):
                context = (pw["super-pathway-visualization"]
                             ["pathway-visualization-contexts"]
                             ["pathway-visualization-context"]
                             ["pathway-visualization"])
                pathway_id = pw["super-pathway-visualization"]["pw-id"]
                pwml_update_date = kg2_util.convert_date(os.path.getmtime(smpdb_dir +
                                                                          filename))
                data = make_nodes_and_edges(context,
                                            pathway_id,
                                            smpdb_data[pathway_id],
                                            pwml_update_date)
                if data is not None:
                    for node in data["nodes"]:
                        nodes.append(node)
                    for edge in data["edges"]:
                        edges.append(edge)
            elif ("super-pathway-visualization" in pw and
                  isinstance(pw["super-pathway-visualization"], dict) and
                  isinstance((pw["super-pathway-visualization"]
                              ["pathway-visualization-contexts"]), dict) and
                  isinstance((pw["super-pathway-visualization"]
                              ["pathway-visualization-contexts"]
                              ["pathway-visualization-context"]), list)):
                pathway_id = pw["super-pathway-visualization"]["pw-id"]
                contexts = (pw["super-pathway-visualization"]
                              ["pathway-visualization-contexts"]
                              ["pathway-visualization-context"])
                pwml_update_date = kg2_util.convert_date(os.path.getmtime(smpdb_dir +
                                                                          filename))
                for context in contexts:
                    context = context["pathway-visualization"]
                    data = make_nodes_and_edges(context,
                                                pathway_id,
                                                smpdb_data[pathway_id],
                                                pwml_update_date)
                    if data is not None:
                        for node in data["nodes"]:
                            nodes.append(node)
                        for edge in data["edges"]:
                            edges.append(edge)
            else:
                print("Issue in file: ", filename)
                continue

    nodes.append(smpdb_kp_node)
    nodes.append(pw_kp_node)
    return {"nodes": nodes,
            "edges": edges}


def check_dirname(dirname: str):
    if dirname.endswith("/"):
        return dirname
    return dirname + "/"


if __name__ == '__main__':
    print("Start time: ", kg2_util.date())
    args = get_args()
    smpdb_dir = check_dirname(args.inputDirectory)
    test_mode = args.test
    output_file_name = args.outputFile
    print("Starting build: ", kg2_util.date())
    graph = make_kg2_graph(smpdb_dir,  test_mode)
    print("Finishing build: ", kg2_util.date())
    print("Start saving JSON: ", kg2_util.date())
    kg2_util.save_json(graph, output_file_name, test_mode)
    print("Finish saving JSON: ", kg2_util.date())
    print("Finish time: ", kg2_util.date())
