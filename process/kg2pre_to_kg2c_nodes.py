#!/usr/bin/env python3

import argparse
import sqlite3
from typing import Any, Optional
import local_babel as lb
import stitchutils as su
import datetime
import json

# Fill in with kg2_util.py when merged
CURIE_ID_KEY = 'id'
IRI_KEY = 'iri'
PUBLICATIONS_KEY = 'publications'
DESCRIPTION_KEY = 'description'
NAME_KEY = 'name'
CATEGORY_KEY = 'category'
SYNONYM_KEY = 'synonym'
TAXON_KEY = 'in_taxon' # Not in KGX yet
CHEMBL_COMPOUND_PREFIX = 'CHEMBL.COMPOUND'

def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _get_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description='kg2pre_to_kg2c_nodes.py: '
                                 'from a JSON-lines format of KG2pre nodes '
                                 'as input, produce a JSON-lines KG2c nodes file')
    ap.add_argument('nodes_file',
                    type=str,
                    help=('the nodes JSON-lines file, like kg2-10-3-nodes.jsonl'))
    ap.add_argument('babel_db',
                    type=str,
                    help='the sqlite database file for the local Babel database')
    ap.add_argument('nodes_output_file',
                    type=str,
                    help=('the nodes JSON lines file to which the output should be '
                          'saved'))
    return ap.parse_args()

def _is_str_none_or_empty(in_str: str):
    return in_str is None or in_str == ""

def _is_list_none_or_empty(in_list: list):
    return in_list is None or in_list == []

def _is_chembl_compound(node_curie: str):
    return node_curie.split(':')[0] == CHEMBL_COMPOUND_PREFIX


def process_nodes(conn, nodes_input_file, nodes_output_file):
    cursor = conn.cursor()

    nodes_read_jsonlines_info = su.start_read_jsonlines(nodes_input_file)
    nodes = nodes_read_jsonlines_info[0]

    kg2c_nodes = dict()

    curie_skipped = set()
    name_skipped = set()
    category_skipped = set()

    node_count = 0
    for node in nodes:
        node_count += 1
        node_curie = node[CURIE_ID_KEY]
        node_publications = node[PUBLICATIONS_KEY]
        node_description = node[DESCRIPTION_KEY]

        node_cliques = lb.map_any_curie_to_cliques(conn, node_curie)
        
        if _is_list_none_or_empty(node_cliques):
            curie_skipped.add(node_curie)

        for node_clique in node_cliques:
            # Required properties
            preferred_node_curie = node_clique['id']['identifier']
            preferred_node_name = node_clique['id']['label']
            preferred_node_category = node_clique['type']

            # Special case for CHEMBL.COMPOUND nodes without names (per discussion with SAR on Slack)
            if _is_str_none_or_empty(preferred_node_name) and _is_chembl_compound(node_curie):
                preferred_node_name = node_curie.split(':')[1]
            elif _is_str_none_or_empty(preferred_node_curie) or _is_str_none_or_empty(preferred_node_name) or _is_list_none_or_empty(preferred_node_category):
                if _is_str_none_or_empty(preferred_node_curie):
                    curie_skipped.add(node_curie)
                if _is_str_none_or_empty(preferred_node_name):
                    name_skipped.add(node_curie)
                if _is_list_none_or_empty(preferred_node_category):
                    category_skipped.add(node_curie)

                continue # Can't export if not all required properties are present

            preferred_node_description = node_clique['id']['description']

            # Start building the output
            preferred_node_dict = dict()
            if preferred_node_curie in kg2c_nodes:
                # If it's already in the output dictionary, we only have to add the information relevant to this KG2pre synonymous node
                if PUBLICATIONS_KEY in kg2c_nodes[preferred_node_curie]:
                    kg2c_nodes[preferred_node_curie][PUBLICATIONS_KEY] = sorted(list(set(kg2c_nodes[preferred_node_curie][PUBLICATIONS_KEY]) | set(node_publications)))
                elif not _is_list_none_or_empty(node_publications):
                    kg2c_nodes[preferred_node_curie][PUBLICATIONS_KEY] = sorted(node_publications)

                # If this node curie matches the preferred curie and the node didn't already have a description, save the KG2pre description
                if DESCRIPTION_KEY not in kg2c_nodes[preferred_node_curie] and _is_str_none_or_empty(preferred_node_description):
                    if preferred_node_curie == node_curie and not _is_str_none_or_empty(preferred_node_description):
                        preferred_node_dict[DESCRIPTION_KEY] = node_description

                continue # Then move to next loop, since we already have the rest of the data
            
            preferred_node_dict[CURIE_ID_KEY] = preferred_node_curie
            preferred_node_dict[NAME_KEY] = preferred_node_name
            preferred_node_dict[CATEGORY_KEY] = preferred_node_category

            if _is_str_none_or_empty(preferred_node_description):
                if preferred_node_curie == node_curie: # Description choosing system discussed with SAR on slack
                    preferred_node_description = node_description

            if not _is_str_none_or_empty(preferred_node_description):
                preferred_node_dict[DESCRIPTION_KEY] = preferred_node_description

            if len(preferred_node_category) > 0:
                for one_preferred_node_category in preferred_node_category:
                    if one_preferred_node_category in {"biolink:Protein", "biolink:Gene"}:
                        preferred_node_organism_taxon = lb.get_taxon_for_gene_or_protein(conn, preferred_node_curie)

                        if not _is_str_none_or_empty(preferred_node_organism_taxon):
                            preferred_node_dict[TAXON_KEY] = preferred_node_organism_taxon
                            break # only need to get this once

            preferred_node_synonyms = lb.map_pref_curie_to_synonyms(cursor, preferred_node_curie) # Note, these are curies, not synonym names
            if not _is_list_none_or_empty(preferred_node_synonyms):
                preferred_node_dict[SYNONYM_KEY] = sorted(list(preferred_node_synonyms))

            if not _is_list_none_or_empty(node_publications):
                preferred_node_dict[PUBLICATIONS_KEY] = node_publications

            kg2c_nodes[preferred_node_curie] = preferred_node_dict

        if node_count % 100000 == 0:
            print(node_count, "nodes processed.")

    su.end_read_jsonlines(nodes_read_jsonlines_info)

    print("Finished processing nodes.")
    print(curie_skipped, "skipped due to missing preferred curie. This is a total of", len(curie_skipped), "nodes excluded.")
    print(name_skipped, "skipped due to missing preferred name. This is a total of", len(name_skipped), "nodes excluded.")
    print(category_skipped, "skipped due to missing preferred category. This is a total of", len(category_skipped), "nodes excluded.")

    nodes_output_info = su.create_single_jsonlines()
    nodes_output = nodes_output_info[0]

    for node_curie in kg2c_nodes:
        nodes_output.write(kg2c_nodes[node_curie])

    su.close_single_jsonlines(nodes_output_info, nodes_output_file)


def main(nodes_file: str,
         babel_db: str,
         nodes_output_file: str):
    print("Starting time:", date())
    print(f"nodes file is: {nodes_file}")
    print(f"babel-db file is: {babel_db}")

    with lb.connect_to_db_read_only(babel_db) as conn:
        process_nodes(conn, nodes_file, nodes_output_file)

    print("Ending time:", date())

if __name__ == "__main__":
    main(**su.namespace_to_dict(_get_args()))
