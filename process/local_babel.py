#!/usr/bin/env python3.12

import functools
import itertools
import multiprocessing
import multiprocessing.pool
import random
import sqlite3
from typing import Callable, Iterable, Optional, TypeAlias, TypedDict, TypeVar

# define the type aliases that we need for brevity
MultProcPool: TypeAlias = multiprocessing.pool.Pool
CurieCurieAndType: TypeAlias = tuple[str, str, str]
CurieCurieAndInt: TypeAlias = tuple[str, str, int]

T = TypeVar("T")
R = TypeVar("R")

class IdentifierInfo(TypedDict):
    description: str  # noqa
    identifier: str  # noqa
    label: str  # noqa


class CliqueInfo(TypedDict):
    ic: float  # noqa
    id: IdentifierInfo  # noqa
    type: list[str]  # noqa



MAX_IDENTIFIERS_PER_STRING_SQLITE = 1000

# below I define the function's type hint using parametric
# polymorphism; T will have be whatever type the user passes
# to the function



def _batch_tuple(x: tuple[T, ...], batch_size: int) -> tuple[tuple[T, ...], ...]:
    it = iter(x)
    return tuple(
        tuple(itertools.islice(it, batch_size))
        for _ in range((len(x) + batch_size - 1) // batch_size)
    )

def _map_with_batching(
    items: tuple[T, ...],
    processor: Callable[[tuple[T, ...]], Iterable[R]],
    pool: Optional[MultProcPool],
    max_batch_size: int = MAX_IDENTIFIERS_PER_STRING_SQLITE
) -> tuple[R, ...]:
    num_workers = pool._processes if pool else 1  # type: ignore[attr-defined]
    batch_size = min(max(1, len(items) // num_workers), max_batch_size)
    batches = _batch_tuple(items, batch_size)
    mapper = pool.imap if pool else map
    return tuple(itertools.chain.from_iterable(mapper(processor, batches)))

def connect_to_db_read_only(db_filename: str) -> sqlite3.Connection:
    # opening with "?mode=ro" is compatible with multiple python processes
    # reading the database at the same time, which we need for multiprocessing;
    # this is why we are not opening the database file with "?immutable=1"
    conn = sqlite3.connect("file:" + db_filename + "?mode=ro",
                           uri=True)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def _map_curies_to_conflation_curies(db_filename: str,
                                     curie_batch: Iterable[str],
                                     pool: Optional[MultProcPool] = None) -> \
                                     tuple[CurieCurieAndInt, ...]:
    s = """
SELECT id2.curie, id1.curie, conflation_clusters.type
FROM identifiers AS id1
INNER JOIN conflation_members AS cm1
ON cm1.identifier_id = id1.id
INNER JOIN conflation_members AS cm2
ON cm2.cluster_id = cm1.cluster_id
INNER JOIN identifiers AS id2
ON id2.id = cm2.identifier_id
INNER JOIN conflation_clusters
ON cm2.cluster_id = conflation_clusters.id
WHERE id2.curie = ?
AND id1.curie <> id2.curie;
    """ # noqa W291
    with connect_to_db_read_only(db_filename) as db_conn:
        cursor = db_conn.cursor()
        res = tuple((row[0], row[1], row[2])
                    for curie in curie_batch
                    for row in cursor.execute(s, (curie,)).fetchall())
    return res


def map_curies_to_conflation_curies(db_filename: str,
                                    curies: tuple[str, ...],
                                    pool: Optional[MultProcPool] = None) -> \
                                    tuple[CurieCurieAndInt, ...]:
    processor = functools.partial(_map_curies_to_conflation_curies,
                                  db_filename)
    return _map_with_batching(curies, processor, pool)


def map_curie_to_conflation_curies(conn: sqlite3.Connection,
                                   curie: str,
                                   conflation_type: int) -> tuple[str]:
    s = """
SELECT id1.curie
FROM identifiers AS id1
INNER JOIN conflation_members AS cm1
ON cm1.identifier_id = id1.id
INNER JOIN conflation_members AS cm2
ON cm2.cluster_id = cm1.cluster_id
INNER JOIN identifiers AS id2
ON id2.id = cm2.identifier_id
INNER JOIN conflation_clusters
ON cm2.cluster_id = conflation_clusters.id
WHERE conflation_clusters.type = ?
AND id2.curie = ?
AND id1.curie <> id2.curie;
    """ # noqa W291
    res = conn.cursor().execute(s, (conflation_type, curie)).fetchall()
    return tuple(row[0] for row in res)

def _map_curies_to_preferred_curies(db_filename: str,
                                    curie_batch: Iterable[str]) -> \
                                    tuple[CurieCurieAndType, ...]:
    s = """
SELECT prim_identif.curie, types.curie, identifiers.curie
FROM identifiers as prim_identif 
INNER JOIN cliques ON prim_identif.id = cliques.primary_identifier_id 
INNER JOIN identifiers_cliques AS idcl ON cliques.id = idcl.clique_id 
INNER JOIN identifiers on idcl.identifier_id = identifiers.id
INNER JOIN types on types.id = cliques.type_id
WHERE identifiers.curie = ?;"""  # noqa W291   
    with connect_to_db_read_only(db_filename) as db_conn:
        cursor = db_conn.cursor()
        res = tuple((row[0], row[1], row[2])
                    for curie in curie_batch
                    for row in cursor.execute(s, (curie,)).fetchall())
    return res

def map_curie_to_preferred_curies(db_conn: sqlite3.Connection,
                                  curie: str) -> \
                                  tuple[CurieCurieAndType, ...]:
    s = """
SELECT prim_identif.curie, types.curie, identifiers.curie
FROM identifiers as prim_identif
INNER JOIN cliques ON prim_identif.id = cliques.primary_identifier_id
INNER JOIN identifiers_cliques AS idcl ON cliques.id = idcl.clique_id
INNER JOIN identifiers on idcl.identifier_id = identifiers.id
INNER JOIN types on types.id = cliques.type_id
WHERE identifiers.curie = ?;"""  # noqa W291
    cursor = db_conn.cursor()
    res = tuple((row[0], row[1], row[2])
                for row in cursor.execute(s, (curie,)).fetchall())
    return res

def map_curies_to_preferred_curies(db_filename: str,
                                   curies: tuple[str, ...],
                                   pool: Optional[MultProcPool] = None) -> \
                                   tuple[CurieCurieAndType, ...]:
    processor = functools.partial(_map_curies_to_preferred_curies,
                                  db_filename)
    return _map_with_batching(curies, processor, pool)


def map_preferred_curie_to_cliques(conn: sqlite3.Connection,
                                   curie: str) -> tuple[CliqueInfo, ...]:
    s = """
SELECT prim_identif.curie, types.curie, cliques.ic, descrip.desc,
cliques.preferred_name
FROM identifiers as prim_identif 
INNER JOIN cliques ON prim_identif.id = cliques.primary_identifier_id 
INNER JOIN types on cliques.type_id = types.id
LEFT JOIN identifiers_descriptions as idd ON idd.identifier_id = prim_identif.id
LEFT JOIN descriptions AS descrip ON descrip.id = idd.description_id
WHERE prim_identif.curie = ?;"""  # noqa W291
    rows = conn.execute(s, (curie,)).fetchall()
    return tuple({'id': {'identifier': row[0],
                         'description': row[3],
                         'label': row[4]},
                  'ic': row[2],
                  'type': [row[1]]} for row in rows)


def map_any_curie_to_cliques(conn: sqlite3.Connection,
                             curie: str) -> tuple[CliqueInfo, ...]:
    s = """
SELECT prim_identif.curie, types.curie, cliques.ic, descrip.desc, cliques.preferred_name
FROM identifiers as prim_identif 
INNER JOIN cliques ON prim_identif.id = cliques.primary_identifier_id 
INNER JOIN identifiers_cliques AS idcl ON cliques.id = idcl.clique_id 
INNER JOIN identifiers as sec_identif on idcl.identifier_id = sec_identif.id
INNER JOIN types on cliques.type_id = types.id
LEFT JOIN identifiers_descriptions as idd ON idd.identifier_id = prim_identif.id
LEFT JOIN descriptions AS descrip ON descrip.id = idd.description_id
WHERE sec_identif.curie = ?;"""  # noqa W291
    rows = conn.execute(s, (curie,)).fetchall()

    # TODO: make these keys not hard coded in so that other files don't have to worry about changes
    return tuple({'id': {'identifier': row[0],
                         'description': row[3],
                         'label': row[4]},
                  'ic': row[2],
                  'type': [row[1]]} for row in rows)


def map_pref_curie_to_synonyms(cursor: sqlite3.Cursor,
                               pref_curie: str) -> set[str]:
    s = """SELECT identifiers.curie
FROM identifiers as prim_identif 
INNER JOIN cliques ON prim_identif.id = cliques.primary_identifier_id 
INNER JOIN identifiers_cliques AS idcl ON cliques.id = idcl.clique_id 
INNER JOIN identifiers on idcl.identifier_id = identifiers.id
WHERE prim_identif.curie = ?;"""  # noqa W291
    rows = cursor.execute(s, (pref_curie,)).fetchall()
    return set(c[0] for c in rows)

def _get_identifier_curies_by_int_id(db_filename: str,
                                     id_batch: Iterable[int]) -> tuple[str, ...]:
    with connect_to_db_read_only(db_filename) as conn:
        id_batch_t = tuple(id_batch)
        cursor = conn.cursor()
        placeholders = ",".join("?" for _ in id_batch_t)
        query = f"SELECT curie FROM identifiers WHERE id IN ({placeholders})"
        cursor.execute(query, id_batch_t)
        result: tuple[str] = tuple(row[0] for row in cursor.fetchall())
        return result

# This function is intended to be used for testing; it will grab CURIEs from `n`
# rows of the `identifiers` table selected at random.
def get_n_random_curies(db_filename: str,
                        n: int,
                        pool: Optional[MultProcPool]) -> tuple[str, ...]:
    with connect_to_db_read_only(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM identifiers")
        row = cursor.fetchone()
        max_id = row[0] if row else None

    if max_id is None:
        raise ValueError("no rows returned")

    random_ids = random.sample(range(1, max_id + 1), n)
    batch_size = MAX_IDENTIFIERS_PER_STRING_SQLITE
    batches = tuple(
        random_ids[i:i+batch_size]
        for i in range(0, len(random_ids), batch_size)
    )

    mapper = pool.imap if pool else map
    chainer = itertools.chain.from_iterable
    processor = functools.partial(_get_identifier_curies_by_int_id, db_filename)
    return tuple(chainer(mapper(processor, batches)))


def get_table_row_counts(conn: sqlite3.Connection) -> dict[str, int]:
    """Returns a dictionary mapping each table name to its row count."""
    cursor = conn.cursor()

    # Get the list of user-defined tables (excluding internal SQLite tables)
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type = 'table' AND name NOT LIKE 'sqlite_%';
    """)
    tables = [row[0] for row in cursor.fetchall()]

    row_counts: dict[str, int] = {}
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        row_counts[table] = count

    return row_counts

def get_taxon_for_gene_or_protein(conn: sqlite3.Connection,
                                  curie: str) -> Optional[str]:
    row = conn.cursor().execute("""
    SELECT id2.curie FROM identifiers AS id1
    INNER JOIN identifiers_taxa ON identifiers_taxa.identifier_id = id1.id
    INNER JOIN identifiers AS id2 ON identifiers_taxa.taxa_identifier_id = id2.id
    WHERE id1.curie = ?;
    """, (curie, )).fetchone()
    return row[0] if row else None