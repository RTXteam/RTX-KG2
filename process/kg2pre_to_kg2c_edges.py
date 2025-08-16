#!/usr/bin/env python3.12

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
import tqdm

import local_babel as lb
import stitchutils as su

DEFAULT_CHUNK_SIZE = 10_000
DEFAULT_ESTIM_NUM_EDGES = 57_803_754

def _predicate_curie_to_space_case(curie: str) -> str: # noqa
    return curie[len('biolink:'):].replace('_', ' ')

def _get_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description='kg2pre_to_kg2c_edges.py: '
                                 'from a JSON-lines format of KG2pre edges'
                                 'as input, produce a JSON-lines KG2c edges file')
    ap.add_argument('nodes_file',
                    type=str,
                    help=('the nodes JSON-lines file, like kg2-10-3-nodes.jsonl'
                          'or kg2-10-3-nodes.jsonl.gz (i.e., compression is OK)'))
    ap.add_argument('edges_file',
                    type=str,
                    help=('the edges JSON lines file, like kg2-10-3-edges.jsonl'
                          'or kg2-10-3-edges.jsonl.gz (i.e., compression is OK)'))
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
    ('agent_type',
     'knowledge_level',
     'predicate',
     'primary_knowledge_source',
     'domain_range_exclusion',)

EDGE_PROPERTIES_COPY_FROM_KG2PRE_IF_EXIST = \
    ('qualified_predicate',
     'qualified_object_direction',
     'qualified_object_aspect',
     'publications',
     'publications_info')

PREDICATE_CURIES_SKIP: tuple[str, ...] = \
    tuple(
#        'biolink:same_as',
#     'biolink:related_to',
#     'biolink:close_match',
#     'biolink:subclass_of',
#     'biolink:has_subclass',
#     'biolink:exact_match')
    )

def _pick_category(categories: set[str],
                       sub_obj: str,
                       predicate: str) -> set[str]:
    return set()

def _make_pick_category():
    tk = bmt.Toolkit()
    def pick_category(categories: set[str],
                      sub_obj: str,
                      predicate: str) -> set[str]:
        if sub_obj == "subject":
            pred_finder = tk.get_all_predicates_with_class_domain
        elif sub_obj == "object":
            pred_finder = tk.get_all_predicates_with_class_range
        else:
            raise ValueError(f"invalid value for sub_obj: {sub_obj}; "
                             "must be \"subject\" or \"object\"")
        for category in categories:
            allowed_preds = pred_finder(category, check_ancestors=True, formatted=True)
            if predicate in allowed_preds:
                return {category}
        if categories == {'biolink:Protein', 'biolink:SmallMolecule'}:
            return {'biolink:SmallMolecule'}
        if categories == {'biolink:Protein', 'biolink:ChemicalEntity'}:
            if predicate == 'biolink:coexists_with':
                return {'biolink:Protein'}
            if (predicate == 'biolink:may_be_treated_by' \
                and sub_obj == 'object') \
                or \
                (predicate == 'biolink:may_treat' \
                 and sub_obj == 'subject'):
                return {'biolink:ChemicalEntity'}
            if (predicate == 'biolink:affects' and sub_obj == 'object') or \
               (predicate in {'biolink:causes', 'biolink:has_input'} and \
                sub_obj == 'subject'):
                return {'biolink:Protein'}
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
        curie = 'NCIT:' + curie[len('OBO:NCIT_'):]
    return curie

# Returns a boolean based on whether or not an entity (str, list, or dict) exists
def _check_if_property_exists(prop_val: Any):
    if prop_val == {} or prop_val == []:
        return False
    return su.nan_to_none(prop_val)

# the "Any" type hint is because Pandas doesn't play
# well with mypy, specifically when using ".itertuples".
def _process_edges_row(conn: sqlite3.Connection,
                       edge_pandas: Any) -> \
        tuple[tuple[Optional[dict[str, Any]], str, str], ...]:
    edge = edge_pandas._asdict()
    kg2pre_edge_id = edge['id']
    res_edge = {k: edge[k] for k in EDGE_PROPERTIES_COPY_FROM_KG2PRE}
    res_edge['id'] = None  # this will eventually be a global integer index
                           # of the edge in a list of all edges (can't compute
                           # that information here since we are processing one
                           # edge only, within this function
    res_edge['kg2_ids'] = [kg2pre_edge_id]
    predicate = res_edge['predicate']
    if predicate in PREDICATE_CURIES_SKIP:
        return ((None,
                 kg2pre_edge_id,
                 f"predicate is on the skip list: {predicate}"),)
    res_edge.update({k: edge[k] for k in \
                     EDGE_PROPERTIES_COPY_FROM_KG2PRE_IF_EXIST
                     if _check_if_property_exists(edge[k])})
    kg2pre_subject_curie = _fix_curie_if_broken(edge['subject'])
    pref_curie_tuple = lb.map_curie_to_preferred_curies(conn,
                                                        kg2pre_subject_curie)
    picked_pref_curies_subject = _filter_pref_curies(pref_curie_tuple,
                                                     "subject",
                                                     predicate)
    if len(picked_pref_curies_subject)==0:
        return ((None, kg2pre_edge_id,
                 "unable to find preferred CURIE for subject: "
                 f"{kg2pre_subject_curie}"),)
    kg2pre_object_curie = _fix_curie_if_broken(edge['object'])
    pref_curie_tuple = lb.map_curie_to_preferred_curies(conn,
                                                        kg2pre_object_curie)
    picked_pref_curies_object = _filter_pref_curies(pref_curie_tuple,
                                                    "object",
                                                    predicate)
    if len(picked_pref_curies_object)==0:
        return ((None, kg2pre_edge_id,
                 "unable to find preferred CURIE for object: "
                 f"{kg2pre_object_curie}"),)
    if len(picked_pref_curies_subject) > 2 or \
       len(picked_pref_curies_object) > 2:
        print(edge_pandas)
        assert False
    res: list[tuple[Optional[dict[str, Any]], str, str]] = []
    for subject_curie, object_curie in it.product(picked_pref_curies_subject,
                                                  picked_pref_curies_object):
        new_res_edge = res_edge
        new_res_edge['subject'] = subject_curie
        new_res_edge['object'] = object_curie
        res.append((new_res_edge, kg2pre_edge_id, 'OK'))
    if len(res) == 0:
        res.append((None,
                    kg2pre_edge_id,
                    "no preferred curies available"))
    return tuple(res)

def _non_null_first_tuple_entry(t: tuple) -> bool:
    return t[0] is not None

def _process_chunk_of_edges(db_filename: str,
                            edge_chunk: pd.DataFrame) -> \
        list[tuple[Optional[dict[str, Any]], str, str]]:
    with lb.connect_to_db_read_only(db_filename) as conn:
        result = []
        for row in edge_chunk.itertuples(index=False):
            for entry in _process_edges_row(conn, row):
                if _non_null_first_tuple_entry(entry):
                    result.append(entry)
        return result

def main(nodes_file: str,
         edges_file: str,
         babel_db: str,
         edges_output_file: str,
         chunk_size: int,
         estim_num_edges: int):
    print(f"nodes file is: {nodes_file}")
    print(f"edges file is: {edges_file}")
    print(f"babel-db file is: {babel_db}")
    estim_num_chunks = math.ceil(estim_num_edges / chunk_size)
    print(f"number of chunks: {estim_num_chunks}")
    global _pick_category
    _pick_category = _make_pick_category()
    chunks_iter = su.read_jsonl_file_chunks(edges_file, chunk_size)
    global _process_chunk_of_edges
    process_chunk_of_edges = functools.partial(_process_chunk_of_edges,
                                               babel_db)
    with multiprocessing.pool.Pool() as p:
        mapped_iter = p.imap_unordered(process_chunk_of_edges,
                                       chunks_iter)
        tqdm_iter = tqdm.tqdm(mapped_iter, total=estim_num_chunks, desc="Processing")
        chained_iter = it.chain.from_iterable(tqdm_iter)
        filtered_iter = filter(lambda t: t[0] is not None, chained_iter)
        edges_iter = map(operator.itemgetter(0), filtered_iter)
        su.write_jsonl_file(edges_iter, edges_output_file)

if __name__ == "__main__":
    main(**su.namespace_to_dict(_get_args()))

