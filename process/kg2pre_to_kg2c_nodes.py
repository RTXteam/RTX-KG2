import argparse
import stitch_proj.local_babel as lb
import kg2_util
import datetime
import sqlite3
from tqdm import tqdm
from typing import Optional

CURIE_ID_KEY = kg2_util.NODE_ID_SLOT
PUBLICATIONS_KEY = kg2_util.NODE_PUBLICATIONS_SLOT
DESCRIPTION_KEY = kg2_util.NODE_DESCRIPTION_SLOT
NAME_KEY = kg2_util.NODE_NAME_SLOT
CATEGORY_KEY = kg2_util.NODE_CATEGORY_SLOT
SYNONYM_KEY = kg2_util.NODE_SYNONYM_SLOT
TAXON_KEY = kg2_util.NODE_TAXON_SLOT
ALL_CATEGORIES_KEY = kg2_util.NODE_ALL_CATEGORIES_SLOT
NODE_IRI_KEY = kg2_util.NODE_IRI_SLOT
CHEMBL_COMPOUND_PREFIX = kg2_util.CURIE_PREFIX_CHEMBL_COMPOUND
SAME_AS_KEY = kg2_util.NODE_SAME_AS_SLOT # NOTE: to align with current KGX compliace, see issue #494 

PROTEIN_CATEGORY = kg2_util.convert_biolink_category_to_curie(kg2_util.BIOLINK_CATEGORY_PROTEIN)
GENE_CATEGORY = kg2_util.convert_biolink_category_to_curie(kg2_util.BIOLINK_CATEGORY_GENE)

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

def _is_str_none_or_empty(in_str: Optional[str]):
    return in_str is None or in_str == ""

def _is_list_none_or_empty(in_list: list):
    return in_list is None or in_list == []

def _is_chembl_compound(node_curie: str):
    return node_curie.split(':')[0] == CHEMBL_COMPOUND_PREFIX


def process_nodes(conn: sqlite3.Connection, nodes_input_file, nodes_output_file):
    cursor = conn.cursor()

    nodes_read_jsonlines_info = kg2_util.start_read_jsonlines(nodes_input_file)
    nodes = nodes_read_jsonlines_info[0]

    # We will build up all the nodes to write out in the file, as dictionary `kg2c_nodes` 
    kg2c_nodes = dict()

    curie_skipped = set()
    name_skipped = set()

    node_count = 0
    for node in tqdm(nodes, desc="Processing nodes", unit="node"):
        node_count += 1
        node_curie = node[CURIE_ID_KEY]
        node_publications = node[PUBLICATIONS_KEY]
        node_description = node[DESCRIPTION_KEY]
        node_iri = node[NODE_IRI_KEY]
        node_cliques = lb.map_any_curie_to_cliques(conn, node_curie)
        
        if _is_list_none_or_empty(node_cliques):
            curie_skipped.add(node_curie)

        # In Babel, an identifier may normalize to more than one clique, in general.
        # Each clique will have a "preferred identifier" that represents it, and
        # a category (semantic type)
        for node_clique in node_cliques:
            # Required properties
            preferred_node_curie = node_clique['id']['identifier']
            preferred_node_name = node_clique['id']['label']

            if _is_str_none_or_empty(preferred_node_name):
                # Try to use the KG2pre node name
                preferred_node_name = node.get(NAME_KEY)
                # If still empty, fallback to CURIE string
                if _is_str_none_or_empty(preferred_node_name):
                    preferred_node_name = preferred_node_curie
                if _is_str_none_or_empty(preferred_node_name):
                    name_skipped.add(node_curie)
                    continue  # skip to next clique (only skips code in inner loop)

            preferred_node_category = node_clique['type']
            preferred_node_description = node_clique['id']['description']

            # Start building the output node
            preferred_node_dict = dict()

            if preferred_node_curie in kg2c_nodes:
                # If it's already in the output dictionary, we only have to add the information
                # relevant to this KG2pre synonymous node
                if PUBLICATIONS_KEY in kg2c_nodes[preferred_node_curie]:
                    kg2c_nodes[preferred_node_curie][PUBLICATIONS_KEY] = \
                        sorted(list(set(kg2c_nodes[preferred_node_curie][PUBLICATIONS_KEY]) | \
                                    set(node_publications)))
                elif not _is_list_none_or_empty(node_publications):
                    kg2c_nodes[preferred_node_curie][PUBLICATIONS_KEY] = sorted(node_publications)

                # If this node curie matches the preferred curie and the node didn't already have a
                # description, save the KG2pre description
                if _is_str_none_or_empty(kg2c_nodes[preferred_node_curie].get(DESCRIPTION_KEY, None)):
                    if not _is_str_none_or_empty(preferred_node_description):
                        kg2c_nodes[preferred_node_curie][DESCRIPTION_KEY] = preferred_node_description
                    elif (not _is_str_none_or_empty(node_description)) and \
                         node_curie == preferred_node_curie:
                        kg2c_nodes[preferred_node_curie][DESCRIPTION_KEY] = node_description

                continue # Then move to next clique, since we already have the rest of the data
            
            preferred_node_dict[CURIE_ID_KEY] = preferred_node_curie
            preferred_node_dict[NAME_KEY] = preferred_node_name
            preferred_node_dict[CATEGORY_KEY] = preferred_node_category

            # change this so that synonyms contains the string literals as required by KGX. 
            # Previously, all_names = lb.get_all_names_for_curie(conn, preferred_node_curie)
            # But synonyms should contain the string literals now 
            synonyms = lb.get_all_names_for_curie(conn, preferred_node_curie)
            if synonyms:
                preferred_node_dict[SYNONYM_KEY] = sorted(list(synonyms))
            all_categories = lb.get_categories_for_curie(conn, preferred_node_curie)
            if all_categories:
                preferred_node_dict[ALL_CATEGORIES_KEY] = list(all_categories)
            if not _is_str_none_or_empty(node_iri):
                preferred_node_dict[NODE_IRI_KEY] = node_iri

            if _is_str_none_or_empty(preferred_node_description) and \
               not _is_str_none_or_empty(node_description):
                if preferred_node_curie == node_curie: # Description choosing system discussed with SAR on slack
                    preferred_node_description = node_description

            if not _is_str_none_or_empty(preferred_node_description):
                preferred_node_dict[DESCRIPTION_KEY] = preferred_node_description

            if len(preferred_node_category) > 0:
                for one_preferred_node_category in preferred_node_category:
                    if one_preferred_node_category in {PROTEIN_CATEGORY, GENE_CATEGORY}:
                        preferred_node_organism_taxon = lb.get_taxon_for_gene_or_protein(conn, preferred_node_curie)

                        if not _is_str_none_or_empty(preferred_node_organism_taxon):
                            preferred_node_dict[TAXON_KEY] = preferred_node_organism_taxon
                            break # only need to get this once

            preferred_node_synonyms_as_curie = lb.map_pref_curie_to_synonyms(cursor, preferred_node_curie) # Note, these are curies, not synonym names
            if not _is_list_none_or_empty(preferred_node_synonyms_as_curie):
                preferred_node_dict[SAME_AS_KEY] = sorted(list(preferred_node_synonyms_as_curie))

            if not _is_list_none_or_empty(node_publications):
                preferred_node_dict[PUBLICATIONS_KEY] = node_publications

            kg2c_nodes[preferred_node_curie] = preferred_node_dict

        if node_count % 100000 == 0:
            print(node_count, "nodes processed.")

    kg2_util.end_read_jsonlines(nodes_read_jsonlines_info)

    print("Finished processing nodes.")
    
    missing_nodes_info = kg2_util.create_single_jsonlines()
    missing_nodes = missing_nodes_info[0]
    for nodes_name in name_skipped: 
        missing_nodes.write(nodes_name)

    missing_nodes_file = "missing_name_nodes.jsonl"

    print(f"Skipped {len(name_skipped)} nodes because they were missing a preferred name. Nodes were logged to {missing_nodes_file}")
    kg2_util.close_single_jsonlines(missing_nodes_info, missing_nodes_file)

    
    # create an output file, so we can write to it
    nodes_output_info = kg2_util.create_single_jsonlines()
    # create_single_jsonlines returns a tuple of a jsonlines
    # file-like object (to a temp file location), the temp output file,
    # and the filename. We don't do anything with the temp output file,
    # just the jsonlines file-like object:
    nodes_output = nodes_output_info[0]

    for node_curie in kg2c_nodes:
        nodes_output.write(kg2c_nodes[node_curie])

    kg2_util.close_single_jsonlines(nodes_output_info, nodes_output_file)


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
    main(**kg2_util.namespace_to_dict(_get_args()))
