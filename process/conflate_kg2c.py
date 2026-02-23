"""
conflate_kg2c.py — Conflate equivalent nodes in a knowledge graph using Babel clusters.

This script post-processes a knowledge graph represented as JSON Lines
nodes and edges files. It identifies and merges ("conflates") nodes that
correspond to the same underlying biological or chemical entity, using
conflation clusters stored in a Babel SQLite database.

NOTE: this script requires the _latest_ version of the
Translator-CATRAX/stitch-proj code.

Specifically, the script performs the following conflations:

- Gene ↔ Protein nodes that belong to the same Babel conflation cluster
- Drug ↔ Chemical and related molecular entity nodes that belong to the
  same Babel conflation cluster

For each eligible node, the canonical CURIE from the corresponding Babel
cluster is selected. Non-canonical CURIEs are merged into the canonical
node, and their metadata (synonyms, categories, and equivalences) are
combined. New canonical nodes are created when necessary.

During processing:

- Input nodes are loaded into memory and indexed by CURIE.
- Nodes eligible for conflation are matched to Babel clusters.
- Redundant nodes are removed and replaced with canonical nodes.
- Edges are rewritten to reference canonical CURIEs.
- Self-edges introduced by conflation are discarded.

Inputs:
    - A Babel SQLite database file
    - A JSON Lines file containing graph edges
    - A JSON Lines file containing graph nodes

Outputs:
    - A rewritten JSON Lines edges file with conflated identifiers
    - A rewritten JSON Lines nodes file with merged node records

This script is intended for use in the KG2c/Stitch/Babel ingestion and
normalization pipeline, where entity conflation is required to ensure
consistent identifier usage and reduce graph redundancy.

Typical usage:
    python conflate_kg2c.py <babel_db> <input_edges> <output_edges> \
                           <input_nodes> <output_nodes>
"""
import gzip
import json
import pprint
import sys
import time
from pathlib import Path
from typing import Optional

import stitch_proj.local_babel as lb

DEFAULT_ENCODING = "utf-8"


def _add_to_list_no_dups(lst: list[str], i: str) -> list[str]:
    """
    Return a new list containing the elements of `lst` in their original order,
    with duplicates removed, and with `i` appended if it is not already present.
    """
    seen: set[str] = set()
    out: list[str] = []

    # First, deduplicate lst while preserving order
    for x in lst:
        if x not in seen:
            seen.add(x)
            out.append(x)

    # Then add i if needed
    if i != '' and i not in seen:
        out.append(i)

    return out

def _open_maybe_gzip(path: Path,
                     mode: str,
                     encoding: Optional[str]):
    # Returns a text-mode file handle
    if path.suffixes[-1:] == [".gz"]:
        return gzip.open(path, mode, encoding=encoding)
    return open(path, mode, encoding=encoding)

def main() -> None:
    """
    The main function for this python module; invoked
    without arguments and has no return value.
    """
    args = sys.argv
    if len(sys.argv) != 6:
        raise ValueError("usage: python conflate_kg2c.py "
                         "db_filename "
                         "input_edges_filename output_edges_filename "
                         "input_nodes_filename output_nodes_filename")
    db_filename = args[1]
    input_edges_filename = args[2]
    output_edges_filename = args[3]
    input_nodes_filename = args[4]
    output_nodes_filename = args[5]

    input_edges_path = Path(input_edges_filename)
    output_edges_path = Path(output_edges_filename)

    input_nodes_path = Path(input_nodes_filename)
    output_nodes_path = Path(output_nodes_filename)

    assert input_edges_path != output_edges_path, \
        "input and output file cannot be the same"
    assert output_edges_path.suffixes[-1:] != [".gz"], \
        "output filename cannot end in .gz; not supported"

    assert input_nodes_path != output_nodes_path, \
        "input and output file cannot be the same"
    assert output_nodes_path.suffixes[-1:] != [".gz"], \
        "output filename cannot end in .gz; not supported"

    with lb.connect_to_db_read_only(db_filename) as conn, \
         _open_maybe_gzip(input_edges_path,
                          mode="rt",
                          encoding=DEFAULT_ENCODING) as edges_input, \
         _open_maybe_gzip(output_edges_path,
                          mode="wt",
                          encoding=DEFAULT_ENCODING) as edges_output, \
         _open_maybe_gzip(input_nodes_path,
                          mode="rt",
                          encoding=DEFAULT_ENCODING) as nodes_input, \
         _open_maybe_gzip(output_nodes_path,
                          mode="wt",
                          encoding=DEFAULT_ENCODING) as nodes_output:
        start = time.time()
        nodes_dict = {}

        node_ctr = 0
        print("loading nodes from the json-lines file")
        ## read in the nodes into a dictionary keyed by node CURIE ID
        for line in nodes_input:
            node_ctr += 1
            node = json.loads(line.strip())
            if not isinstance(node, dict):
                raise ValueError(f"unexpected node type at line {node_ctr}")
            assert 'id' in node
            node_curie = node['id']
            if node_curie in nodes_dict:
                raise ValueError(f"node CURIE {node_curie} is duplicated "
                                 "as an ID in the nodes file")
            nodes_dict[node_curie] = node
            if node_ctr % 1_000_000 == 0:
                print(f"  Have loaded {node_ctr:,} nodes in "
                      f"{(time.time() - start):0.2f} sec")

        print(f"Total number of nodes loaded {node_ctr:,}")

        node_ctr = 0
        start = time.time()
        conflation_check_categories = {
            'biolink:Protein',
            'biolink:ChemicalEntity',
            'biolink:SmallMolecule',
            'biolink:MolecularMixture',
            'biolink:Drug',
            'biolink:Agent',
            'biolink:PhysicalEntity',
            'biolink:ChemicalMixture',
            'biolink:MolecularEntity',
            'biolink:ComplexMolecularMixture',
            'biolink:Polypeptide',
            'biolink:NucleicAcidEntity'
        }
        conflation_dict = {}
        new_nodes = {}
        print("checking nodes for whether they need to be conflated")
        ## perform node conflation
        nodes_to_delete: set[str] = set()
        for node_curie, node in nodes_dict.items():
            node_ctr += 1
            assert 'category' in node
            node_category = node['category']
            assert isinstance(node_category, list), \
                f"for node {node_curie}, category property is not a list"
            assert len(node_category) == 1, \
                f"for node {node_curie}, there should only be one category" \
                "in the category property list"
            node_category_curie = node_category[0]
            assert isinstance(node_category_curie, str)
            for p in ('same_as',
                      'synonym',
                      'all_categories',
                      'publications'):
                v = node.get(p, [])
                assert isinstance(v, list), (node_curie, p, type(v))
                assert all(isinstance(x, str) for x in v), (node_curie, p)
            if node_category_curie in conflation_check_categories:
                conflation_rows = lb.map_curie_to_conflation_curies(conn, node_curie)
                if conflation_rows:
                    conflation_curie: Optional[str] = None
                    canonical_curie: Optional[str] = None
                    for conflation_curie, is_canonical in conflation_rows:
                        if is_canonical:
                            canonical_curie = conflation_curie
                            break
                    if canonical_curie is None:
                        raise ValueError(f"no canonical CURIE for {node_curie}")
                    if canonical_curie != node_curie:
                        conflation_dict[node_curie] = canonical_curie
                        nodes_to_delete.add(node_curie)
                        if canonical_curie not in nodes_dict:
                            if canonical_curie not in new_nodes:
                                # new node doesn't exist
                                cliques_info = \
                                    lb.map_preferred_curie_to_cliques(conn,
                                                                      canonical_curie)
                                if not cliques_info:
                                    raise ValueError("failed to get clique info "
                                                     f"for {canonical_curie}")
                                if len(cliques_info) > 1:
                                    pprint.pprint(cliques_info)
                                    raise ValueError("got more than one clique for "
                                                     f"{canonical_curie}")
                                clique_info = cliques_info[0]
                                # this should be guaranteed by DB schema:
                                assert isinstance(clique_info['type'], list)
                                assert len(clique_info['type'])==1
                                assert isinstance(clique_info['type'][0], str)
                                new_synonyms: list[str] = \
                                    node.get('synonym', []).copy()
                                new_pubs: list[str] = \
                                    node.get('publications', []).copy()
                                new_same_as: list[str] = \
                                    node.get('same_as', []).copy() + [node_curie]
                                node_all_categs = \
                                    node.get('all_categories', []).copy()
                                new_all_categs: list[str] = \
                                    node_all_categs + \
                                    [node_category_curie] + \
                                    clique_info['type']
                                new_node = {
                                    'all_categories': new_all_categs,
                                    'category': clique_info['type'],  # list[str] len 1
                                    'description': clique_info['id']['description'],
                                    'id': canonical_curie,
                                    'name': clique_info['id']['label'],
                                    'same_as': new_same_as,
                                    'synonym': new_synonyms,
                                    'publications': new_pubs
                                }
                                node_name = node.get('name', None)
                                if node_name is not None and node_name != '':
                                    assert isinstance(node_name, str)
                                    new_synonyms.append(node_name)
                                new_nodes[canonical_curie] = new_node
                            else:  # new node exists
                                new_node = new_nodes[canonical_curie]
                                new_node['same_as'] = \
                                    _add_to_list_no_dups(
                                        new_node['same_as'] +
                                        node.get('same_as', []),
                                        node_curie)
                                new_node['synonym'] = \
                                    _add_to_list_no_dups(
                                        new_node['synonym'] +
                                        node.get('synonym', []),
                                        node.get('name', ''))
                                new_node['all_categories'] = \
                                    _add_to_list_no_dups(
                                        new_node['all_categories'] +
                                        node.get('all_categories', []),
                                        node_category_curie)
                                new_node['publications'] = \
                                    _add_to_list_no_dups(
                                        new_node['publications'] +
                                        node.get('publications', []),
                                        '')
                        else:
                            conflat_node = nodes_dict[canonical_curie]
                            conflat_node['same_as'] = \
                                _add_to_list_no_dups(conflat_node.get(
                                    'same_as', []) +
                                                     node.get('same_as', []),
                                                     node_curie)
                            conflat_node['synonym'] = \
                                _add_to_list_no_dups(conflat_node.get(
                                    'synonym', []) +
                                                     node.get('synonym', []),
                                                     node.get('name', ''))
                            conflat_node['all_categories'] = \
                                _add_to_list_no_dups(conflat_node.get(
                                    'all_categories', []) +
                                                     node.get('all_categories', []),
                                                     node_category_curie)
                            if 'publications' not in conflat_node:
                                conflat_node['publications'] = []
                            conflat_pubs = conflat_node['publications']
                            conflat_pubs = list(set(conflat_pubs +
                                                    node.get('publications', [])))
                            conflat_node['publications'] = conflat_pubs
                    else:
                        # nothing to do for this CURIE; it is canonical
                        # and already exists
                        pass
                else:
                    # nothing to do for this CURIE; it is not conflatable
                    pass
            if node_ctr % 1_000_000 == 0:
                print(f"  Have checked {node_ctr:,} nodes in "
                      f"{(time.time() - start):0.2f} sec")
        print(f"Total number of nodes checked for conflation: {node_ctr:,}")
        print(f"Number of nodes that need to be conflated: {len(conflation_dict)}")
        print(f"Number of nodes that need to be deleted: {len(nodes_to_delete)}")
        print(f"Number of nodes that need to be added: {len(new_nodes)}")

        node_ctr = 0

        for node_id_to_del in nodes_to_delete:
            nodes_dict.pop(node_id_to_del)

        nodes_dict.update(new_nodes)

        # node cleanup
        for node_curie in nodes_dict:
            node = nodes_dict[node_curie]
            node_pubs = node.get('publications', [])
            if not node_pubs:
                node.pop('publications', None)
            node_name = node.get('name', None)
            node_synonym = node.get('synonym', [])
            if node_name is not None and \
               node_name != '' and node_synonym:
                node_synonym = list(set(node_synonym) -
                                    {node_name})
            if not node_synonym:
                node.pop('synonym', None)
            else:
                node['synonym'] = node_synonym
            node_same_as = node.get('same_as', [])
            node_same_as = list(set(node_same_as) -
                                {node['id']})
            node['same_as'] = node_same_as
            if not node['same_as']:
                node.pop('same_as', None)
            node_all_categories = node.get('all_categories', [])
            node_all_categories = list(set(node_all_categories))
            node['all_categories'] = node_all_categories
            if not node_all_categories:
                node.pop('all_categories', None)

        # write out nodes
        for node_curie in sorted(nodes_dict):
            json.dump(nodes_dict[node_curie], nodes_output)
            print("", file=nodes_output)
        start = time.time()
        edge_line_ctr = 1
        self_edge_ctr = 0
        for line in edges_input:
            edge = json.loads(line.strip())
            if not isinstance(edge, dict):
                raise ValueError(f"unexpected edge type at line {edge_line_ctr}")
            subject_curie = edge['subject']
            object_curie = edge['object']
            if subject_curie in conflation_dict:
                subject_curie = conflation_dict[subject_curie]
                edge['subject'] = subject_curie
            if object_curie in conflation_dict:
                object_curie = conflation_dict[object_curie]
                edge['object'] = object_curie
            if subject_curie != object_curie:
                json.dump(edge, edges_output)
                print("", file=edges_output)
            else:
                self_edge_ctr += 1

            if edge_line_ctr % 1_000_000 == 0:
                print(f"  Have processed {edge_line_ctr:,} edges in "
                      f"{(time.time() - start):0.2f} sec")
            edge_line_ctr += 1
        print(f"Total elapsed time: {(time.time() - start):0.2f} sec")

        print(f"Number of edges processed: {edge_line_ctr:,}")
        print(f"Number of self-edges dropped: {self_edge_ctr:,}")

if __name__ == "__main__":
    main()
