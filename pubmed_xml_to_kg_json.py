#!/usr/bin/env python3
''' pubmed_xml_to_kg_json.py: Extracts a KG2 JSON file from the
    PubMed XML files

    Usage: pubmed_xml_to_kg_json.py [--test] <inputDirectory>
    <kg2PMIDs.json> <outputFile.json>
'''

import xmltodict
import datetime
import kg2_util
import json
import gzip
import os
import argparse


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


PMID_BASE_IRI = kg2_util.BASE_URL_PMID
PMID_KB_IRI = kg2_util.BASE_URL_PMID
BIOLINK_CATEGORY_PUBLICATION = "publication"
PMID_PROVIDED_BY_CURIE_ID = kg2_util.CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY \
                                + ":pubmed"


def get_args():
    arg_parser = argparse.ArgumentParser(description='pubmed_xml_to_kg_json.py: \
                                         Extracts a KG2 JSON file from the \
                                         PubMed XML files')
    arg_parser.add_argument('--test',
                            dest='test',
                            action="store_true",
                            default=False)
    arg_parser.add_argument('inputDirectory', type=str)
    arg_parser.add_argument('kg2PMIDs', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()


def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def extract_date(date: dict):
    return datetime.date(int(date["Year"]), int(date["Month"]), int(date["Day"])).isoformat()


def date_to_num(date: str):
    date = str(date.split("-"))
    date = date.replace("[", "").replace("]", "").replace(" ", "")
    return int(date.replace(",", "").replace("'", ""))


def exist_or_empty_string(dictionary: dict, key: str):
    data_string = ""
    try:
        data_string = dictionary[key]
    except:
        data_string = ""
    return data_string


def get_authors(article_citation: dict):
    authors = []

    article = article_citation["Article"]
    try:
        author_list = article["AuthorList"]["Author"]
    except:
        return []

    if isinstance(author_list, list):
        for author in article["AuthorList"]["Author"]:
            first_name = exist_or_empty_string(author, "ForeName")
            last_name = exist_or_empty_string(author, "LastName")
            authors.append(first_name + " " + last_name)
    else:
        first_name = exist_or_empty_string(author_list, "ForeName")
        last_name = exist_or_empty_string(author_list, "LastName")
        authors.append(first_name + " " + last_name)
    return authors


def get_journal(article_citation: dict):
    article = article_citation["Article"]

    journal = article["Journal"]["Title"]

    return journal


def make_node_and_edges(article: dict,
                        mesh_predicate_label: str,
                        mesh_relation_curie: str):
    nodes = []
    edges = []

    article_citation = article["MedlineCitation"]

    pmid = kg2_util.CURIE_PREFIX_PMID + ":" + article_citation["PMID"]["#text"]

    update_date = extract_date(article_citation["DateRevised"])

    if pmid in pmids:
        # These aren't necessary yet, but it might be someday, so I wrote
        # and tested a couple of functions to extract them

        #authors = get_authors(article_citation)

        #journal = get_journal(article_citation)

        name = article_citation["Article"]["ArticleTitle"]
        if isinstance(name, dict):
            try:
                name = name["#text"]
            except:
                temp_name = name
                for key in temp_name:
                    name = temp_name[key]["#text"]

        try:
            created_date = extract_date(article_citation["Article"]
                                                        ["ArticleDate"])
        except:
            created_date = None

        iri = PMID_BASE_IRI + article_citation["PMID"]["#text"]

        node = kg2_util.make_node(pmid,
                                  iri,
                                  name,
                                  BIOLINK_CATEGORY_PUBLICATION,
                                  update_date,
                                  PMID_PROVIDED_BY_CURIE_ID)
        node["creation date"] = created_date
        nodes.append(node)
        try:
            for mesh_topic in (article_citation["MeshHeadingList"]
                                               ["MeshHeading"]):
                mesh_id = kg2_util.CURIE_PREFIX_MESH + ":" + \
                          mesh_topic["DescriptorName"]["@UI"]
                edge = kg2_util.make_edge(pmid,
                                          mesh_id,
                                          mesh_relation_curie,
                                          mesh_predicate_label,
                                          PMID_PROVIDED_BY_CURIE_ID,
                                          update_date)
                edges.append(edge)
        except:
            mesh_id = None

    return [{"nodes": nodes, "edges": edges}, update_date]


if __name__ == '__main__':
    print("Starting Script:", date())
    args = get_args()
    print("Starting PubMed ID Load:", date())
    pmids = set(json.load(open(args.kg2PMIDs)))
    print("Finishing PubMedID Load:", date(), ",", len(pmids), "PMIDs in KG2")
    pubmed_dir = args.inputDirectory
    nodes = []
    edges = []
    latest_date = 0
    mesh_predicate_label = "references"
    mesh_relation_curie = kg2_util.predicate_label_to_curie(mesh_predicate_label,
                                                            kg2_util.CURIE_PREFIX_PMID)
    for filename in os.listdir(pubmed_dir):
        if ".gz" in filename:
            print("Starting Load of", filename, ":", date())
            xml_file = gzip.open(pubmed_dir + filename)
            data = xmltodict.parse(xml_file.read())
            print("Finished Load of", filename, ":", date())
            articles = data["PubmedArticleSet"]["PubmedArticle"]

            for article in articles:
                [data, update_date] = make_node_and_edges(article,
                                                          mesh_predicate_label,
                                                          mesh_relation_curie)
                for node in data["nodes"]:
                    nodes.append(node)
                for edge in data["edges"]:
                    edges.append(edge)
                if date_to_num(update_date) > latest_date:
                    latest_date = date_to_num(update_date)

    latest_date = {"Year": str(latest_date)[0:4],
                   "Month": str(latest_date)[4:6],
                   "Day": str(latest_date)[6:]}
    pmid_kp_node = kg2_util.make_node(PMID_PROVIDED_BY_CURIE_ID,
                                      PMID_KB_IRI,
                                      "PubMed",
                                      kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                      extract_date(latest_date),
                                      PMID_PROVIDED_BY_CURIE_ID)
    nodes.append(pmid_kp_node)
    print("Saving JSON:", date())
    kg2_util.save_json({"nodes": nodes,
                        "edges": edges},
                       args.outputFile,
                       args.test)
    print("Finished saving JSON:", date())
    print("Script Finished:", date())
