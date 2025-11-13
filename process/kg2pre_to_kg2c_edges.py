#!/usr/bin/env python3

import argparse
import functools
import itertools as it
import math
import multiprocessing
import operator
import sqlite3
from typing import Any, Optional

import bmt
import pandas as pd

import local_babel as lb
import kg2_util
from tqdm import tqdm

DEFAULT_CHUNK_SIZE = 10_000
DEFAULT_ESTIM_NUM_EDGES = 57_803_754

# kg2_util.py imports to parameterize the file
PROTEIN_CATEGORY = kg2_util.convert_biolink_category_to_curie(kg2_util.BIOLINK_CATEGORY_PROTEIN)
SMALL_MOLECULE_CATEGORY = kg2_util.convert_biolink_category_to_curie(kg2_util.BIOLINK_CATEGORY_SMALL_MOLECULE)
CHEMICAL_ENTITY_CATEGORY = kg2_util.convert_biolink_category_to_curie(kg2_util.BIOLINK_CATEGORY_CHEMICAL_ENTITY)

AFFECTS_PREDICATE = kg2_util.CURIE_PREFIX_BIOLINK + ':' + kg2_util.EDGE_LABEL_BIOLINK_AFFECTS
HAS_INPUT_PREDICATE = kg2_util.CURIE_PREFIX_BIOLINK + ':' + kg2_util.EDGE_LABEL_BIOLINK_HAS_INPUT
# MAY_BE_TREATED_BY_PREDICATE = kg2_util.CURIE_PREFIX_BIOLINK + ':' + kg2_util.EDGE_LABEL_BIOLINK_MAY_BE_TREATED_BY ## DOESN'T EXIST IN BIOLINK
COEXISTS_WITH_PREDICATE = kg2_util.CURIE_PREFIX_BIOLINK + ':' + kg2_util.EDGE_LABEL_BIOLINK_COEXISTS_WITH
# MAY_TREAT_PREDICATE = kg2_util.CURIE_PREFIX_BIOLINK + ':' + kg2_util.EDGE_LABEL_BIOLINK_MAY_TREAT  ## DOESN'T EXIST IN BIOLINK
CAUSES_PREDICATE = kg2_util.CURIE_PREFIX_BIOLINK + ':' + kg2_util.EDGE_LABEL_BIOLINK_CAUSES

SUBJECT_KEY = kg2_util.EDGE_SUBJECT_SLOT
OBJECT_KEY = kg2_util.EDGE_OBJECT_SLOT
ID_KEY = kg2_util.EDGE_ID_SLOT
KG2_IDS_KEY = kg2_util.EDGE_KG2_IDS_SLOT
PREDICATE_KEY = kg2_util.EDGE_PREDICATE_SLOT
AGENT_TYPE_KEY = kg2_util.EDGE_AGENT_TYPE_SLOT
KNOWLEDGE_LEVEL_KEY = kg2_util.EDGE_KNOWLEDGE_LEVEL_SLOT
PRIMARY_KNOWLEDGE_SOURCE_KEY = kg2_util.EDGE_PRIMARY_KNOWLEDGE_SOURCE_SLOT
DOMAIN_RANGE_EXCLUSION_KEY = kg2_util.EDGE_DOMAIN_RANGE_EXCLUSION_SLOT
QUALIFIED_PREDICATE_KEY = kg2_util.EDGE_QUALIFIED_PREDICATE_SLOT
OBJECT_DIRECTION_QUALIFIER_KEY = kg2_util.EDGE_OBJECT_DIRECTION_QUALIFIER_SLOT
OBJECT_ASPECT_QUALIFIER_KEY = kg2_util.EDGE_OBJECT_ASPECT_QUALIFIER_SLOT
PUBLICATIONS_KEY = kg2_util.EDGE_PUBLICATIONS_SLOT
PUBLICATIONS_INFO_KEY = kg2_util.EDGE_PUBLICATIONS_INFO_SLOT

def _get_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description='kg2pre_to_kg2c_edges.py: '
                                 'from a JSON-lines format of KG2pre edges'
                                 'as input, produce a JSON-lines KG2c edges file')
    ap.add_argument('edges_file',
                    type=str,
                    help=('the edges JSON lines file, like kg2-10-3-edges.jsonl'
                          'or kg2-10-3-edges.jsonl'))
    ap.add_argument('babel_db',
                    type=str,
                    help='the sqlite database file for the local Babel database')
    ap.add_argument('edges_output_file',
                    type=str,
                    help=('the edges JSON lines file to which the output should be '
                          'saved'))
    ap.add_argument('--chunk_size',
                    default=DEFAULT_CHUNK_SIZE,
                    type=int,
                    dest='chunk_size',
                    help=('number of jsonlines lines to be read into a single chunk'))
    ap.add_argument('--estim_num_edges',
                    default=DEFAULT_ESTIM_NUM_EDGES,
                    type=int,
                    dest='estim_num_edges',
                    help=('number of jsonlines lines in the input edges file'))
    return ap.parse_args()

EDGE_PROPERTIES_COPY_FROM_KG2PRE = \
    (AGENT_TYPE_KEY,
     KNOWLEDGE_LEVEL_KEY,
     PREDICATE_KEY,
     PRIMARY_KNOWLEDGE_SOURCE_KEY,
     DOMAIN_RANGE_EXCLUSION_KEY,)

EDGE_PROPERTIES_COPY_FROM_KG2PRE_IF_EXIST = \
    (QUALIFIED_PREDICATE_KEY,
     OBJECT_DIRECTION_QUALIFIER_KEY,
     OBJECT_ASPECT_QUALIFIER_KEY,
     PUBLICATIONS_KEY,
     PUBLICATIONS_INFO_KEY)


def _is_str_none_or_empty(in_str: str):
    return in_str is None or in_str == ""

def _is_list_none_or_empty(in_list: list):
    return in_list is None or in_list == []

def _pick_category(categories: set[str],
                       sub_obj: str,
                       predicate: str) -> set[str]:
    return set()

def _make_pick_category():
    tk = bmt.Toolkit()
    def pick_category(categories: set[str],
                      sub_obj: str,
                      predicate: str) -> set[str]:
        if sub_obj == SUBJECT_KEY:
            pred_finder = tk.get_all_predicates_with_class_domain
        elif sub_obj == OBJECT_KEY:
            pred_finder = tk.get_all_predicates_with_class_range
        else:
            raise ValueError(f"invalid value for sub_obj: {sub_obj}; "
                             "must be \"subject\" or \"object\"")
        for category in categories:
            allowed_preds = pred_finder(category, check_ancestors=True, formatted=True)
            if predicate in allowed_preds:
                return {category}
        if categories == {PROTEIN_CATEGORY, SMALL_MOLECULE_CATEGORY}:
            return {SMALL_MOLECULE_CATEGORY}
        if categories == {PROTEIN_CATEGORY, CHEMICAL_ENTITY_CATEGORY}:
            if predicate == COEXISTS_WITH_PREDICATE:
                return {PROTEIN_CATEGORY}
            if (predicate == AFFECTS_PREDICATE and sub_obj == OBJECT_KEY) or \
               (predicate in {CAUSES_PREDICATE, HAS_INPUT_PREDICATE} and \
                sub_obj == SUBJECT_KEY):
                return {PROTEIN_CATEGORY}
        return categories
    return pick_category

def _filter_pref_curies(pref_curie_tuple: tuple[tuple[str, str, str], ...],
                        sub_obj: str,
                        predicate: str) -> set[str]:
    if len(pref_curie_tuple) == 0:
        return set()
    if len(pref_curie_tuple) == 1:
        return {pref_curie_tuple[0][0]}
    categories_to_pref_curies = {st[1]: st[0] for st in pref_curie_tuple}
    categories = set(categories_to_pref_curies.keys())
    picked_categories = _pick_category(categories, sub_obj, predicate)
    return {categories_to_pref_curies[c] for c in picked_categories}

def _fix_curie_if_broken(curie: str) -> str:
    if curie.startswith('OBO:NCIT_'):
        curie = kg2_util.CURIE_PREFIX_NCIT + ':' + curie[len('OBO:NCIT_'):]
    return curie

# Returns a boolean based on whether or not an entity (str, list, or dict) exists
def _check_if_property_exists(prop_val: Any):
    if prop_val == {} or prop_val == []:
        return False
    return kg2_util.nan_to_none(prop_val)

# the "Any" type hint is because Pandas doesn't play
# well with mypy, specifically when using ".itertuples".
def _process_edges_row(conn: sqlite3.Connection,
                       edge_pandas: Any) -> \
        tuple[tuple[Optional[dict[str, Any]], str, str], ...]:
    edge = edge_pandas._asdict()
    kg2pre_edge_id = edge[ID_KEY]
    res_edge = {k: edge[k] for k in EDGE_PROPERTIES_COPY_FROM_KG2PRE}
    res_edge[ID_KEY] = None
    res_edge[KG2_IDS_KEY] = [kg2pre_edge_id]
    predicate = res_edge[PREDICATE_KEY]
    res_edge.update({k: edge[k] for k in EDGE_PROPERTIES_COPY_FROM_KG2PRE_IF_EXIST
                     if _check_if_property_exists(edge[k])})

    # -------------------
    # SUBJECT VALIDATION
    # -------------------
    kg2pre_subject_curie = _fix_curie_if_broken(edge[SUBJECT_KEY])
    subject_cliques = lb.map_curie_to_preferred_curies(conn, kg2pre_subject_curie)

    if not subject_cliques:
        return ((None, kg2pre_edge_id,
                f"subject missing required fields: {kg2pre_subject_curie}"),)
    preferred_subject_curie = subject_cliques[0][0]

    # -------------------
    # OBJECT VALIDATION
    # -------------------
    kg2pre_object_curie = _fix_curie_if_broken(edge[OBJECT_KEY])
    object_cliques = lb.map_curie_to_preferred_curies(conn, kg2pre_object_curie)

    preferred_object_curie = preferred_object_name = preferred_object_category = None
    if not object_cliques:
        return ((None, kg2pre_edge_id,
                f"object missing required fields: {kg2pre_object_curie}"),)
    preferred_object_curie = object_cliques[0][0]
    # -------------------
    # BUILD EDGE
    # -------------------
    if preferred_subject_curie == preferred_object_curie and \
        predicate not in ["interacts_with", "physically_interacts_with"]:
        return ((None, kg2pre_edge_id, "skipped invalid self-edge"),)

    res: list[tuple[Optional[dict[str, Any]], str, str]] = []
    new_res_edge = res_edge.copy()
    new_res_edge[SUBJECT_KEY] = preferred_subject_curie
    new_res_edge[OBJECT_KEY] = preferred_object_curie
    res.append((new_res_edge, kg2pre_edge_id, 'OK'))

    return tuple(res)


def _non_null_first_tuple_entry(t: tuple) -> bool:
    return t[0] is not None

def _process_chunk_of_edges(db_filename: str,
                            edge_chunk: pd.DataFrame) -> \
        tuple[list[tuple[Optional[dict[str, Any]], str, str]], dict[str, str]]:
    with lb.connect_to_db_read_only(db_filename) as conn:
        result = []
        invalid = {}
        for row in edge_chunk.itertuples(index=False):
            for entry in _process_edges_row(conn, row):
                if _non_null_first_tuple_entry(entry):
                    result.append(entry)
                else:
                    edge_id = entry[1]
                    reason = entry[2]
                    invalid[edge_id] = reason
        return result, invalid



def main(edges_file: str,
         babel_db: str,
         edges_output_file: str,
         chunk_size: int,
         estim_num_edges: int):
    print("Starting at:", kg2_util.date())
    print(f"edges file is: {edges_file}")
    print(f"babel-db file is: {babel_db}")

    estim_num_chunks = math.ceil(estim_num_edges / chunk_size)
    print(f"number of chunks: {estim_num_chunks}")

    global _pick_category
    _pick_category = _make_pick_category()

    chunks_iter = kg2_util.read_jsonl_file_chunks(edges_file, chunk_size)
    process_chunk_of_edges = functools.partial(_process_chunk_of_edges, babel_db)

    all_valid_edges = []
    all_invalid_edges = {}

    with multiprocessing.pool.Pool() as p:
        # Wrap mapped_iter with tqdm to visualize progress
        mapped_iter = p.imap_unordered(process_chunk_of_edges, chunks_iter)

        for valid_chunk, invalid_chunk in tqdm(mapped_iter,
                                               total=estim_num_chunks,
                                               desc="Processing edges",
                                               unit="chunk"):
            all_valid_edges.extend(valid_chunk)
            all_invalid_edges.update(invalid_chunk)

    # Write valid edges
    edge_tuples = tuple(t[0] for t in all_valid_edges if t[0] is not None)
    kg2_util.write_jsonl_file(edge_tuples, edges_output_file)

    # Write skipped edges summary
    missing_edges_file = edges_output_file.replace(".jsonl", "_missing_edges.jsonl")
    kg2_util.write_jsonl_file(
        [{"edge_id": eid, "reason": reason} for eid, reason in all_invalid_edges.items()],
        missing_edges_file
    )

    print(f"Skipped {len(all_invalid_edges)} edges due to missing required fields. "
          f"Logged to {missing_edges_file}")
    print("Ending at:", kg2_util.date())

if __name__ == "__main__":
    main(**kg2_util.namespace_to_dict(_get_args()))