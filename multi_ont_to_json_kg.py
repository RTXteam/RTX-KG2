#!/usr/bin/env python3
'''Builds the RTX "KG2" second-generation knowledge graph, from various OWL input files.

   Usage: multi_ont_to_json_kg.py <categoriesFile.yaml> <curiesToURILALFile>
                                  <ontLoadInventoryFile.yaml> <outputFile>
   (note: outputFile can end in .json or in .gz; if the latter, it will be written as a gzipped file;
   but using the gzip options for input or output seems to significantly increase transient memory
   usage)
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


import argparse
import kg2_util
import ontobio
import os.path
import re
import sys
import urllib.parse
import urllib.request
from typing import Dict

# -------------- define globals here ---------------

REGEX_ENSEMBL = re.compile('ENS[A-Z]{0,3}([PG])[0-9]{11}')
REGEX_YEAR = re.compile('([12][90][0-9]{2})')
REGEX_YEAR_MONTH_DAY = re.compile('([12][90][0-9]{2})_([0-9]{1,2})_([0-9]{1,2})')
REGEX_MONTH_YEAR = re.compile('([0-9]{1,2})_[12][90][0-9]{2}')
REGEX_YEAR_MONTH = re.compile('[12][90][0-9]{2}_([0-9]{1,2})')
REGEX_PUBLICATIONS = re.compile(r'((?:(?:PMID)|(?:ISBN)):\d+)')
REGEX_XREF_END_DESCRIP = re.compile(r'.*\[([^\]]+)\]$')

IRI_OBO_XREF = kg2_util.IRI_OBO_FORMAT_XREF
CURIE_OBO_XREF = kg2_util.CURIE_ID_OBO_FORMAT_XREF
OWL_BASE_CLASS = kg2_util.CURIE_ID_OWL_THING
OWL_NOTHING = kg2_util.CURIE_ID_OWL_NOTHING

NOCODE = 'NOCODE'
MYSTERIOUS_BASE_NODE_ID_TO_FILTER = '_:genid'
ENSEMBL_LETTER_TO_CATEGORY = {'P': 'protein',
                              'G': 'gene',
                              'T': 'transcript'}


# -------------- subroutines with side-effects go here ------------------


def delete_ontobio_cachier_caches():
    kg2_util.purge("~/.cachier", ".ontobio*")
    kg2_util.purge("~/.cachier", ".prefixcommons*")


def load_ont_file_return_ontology_and_metadata(file_name: str,
                                               download_url: str = None,
                                               ontology_title: str = None,
                                               save_pickle: bool = False):
    ontology = kg2_util.make_ontology_from_local_file(file_name, save_pickle=save_pickle)
    file_last_modified_timestamp = kg2_util.format_timestamp(kg2_util.get_file_last_modified_timestamp(file_name))
    print("file: " + file_name + "; last modified: " + file_last_modified_timestamp)
    ont_version = ontology.meta.get('version', None)
    bpv = ontology.meta.get('basicPropertyValues', None)
    title = ontology_title
    description = None
    umls_sver = None
    umls_release = None
    source_file_date = None
    if bpv is not None:
        for bpv_dict in bpv:
            pred = bpv_dict['pred']
            value = bpv_dict['val']
            if 'description' in pred:
                description = value
            elif 'title' in pred:
                if title is None:
                    title = value
            elif pred == kg2_util.BASE_URL_UMLS + 'sver':
                ont_version = value
                umls_sver = value
            elif pred == kg2_util.BASE_URL_OWL + 'versionInfo':
                umls_release = value
            elif pred.endswith('source_file_date'):
                source_file_date = value
    if ont_version is None:
        ont_version = 'downloaded:' + file_last_modified_timestamp
    ontology_id = None
    if download_url is not None:
        ontology_id = download_url
    else:
        ontology_id = ontology.id
        #    print(ontology_id)
        if not kg2_util.is_a_valid_http_url(ontology_id):
            ontology_id = os.path.basename(file_name)
    metadata_dict = {'id': ontology_id,
                     'handle': ontology.handle,
                     'file': file_name,
                     'file last modified timestamp': file_last_modified_timestamp,
                     'version': ont_version,
                     'title': title,
                     'description': description,
                     'umls-sver': umls_sver,
                     'umls-release': umls_release,
                     'source-file-date': source_file_date}
#    print(metadata_dict)
    return [ontology, metadata_dict]


def make_kg2(curies_to_categories: dict,
             uri_to_curie_shortener: callable,
             curie_to_uri_expander: callable,
             ont_urls_and_files: tuple,
             output_file_name: str,
             test_mode: bool = False,
             save_pickle: bool = False):

    ont_file_information_dict_list = []

    # for each OWL file (or URL for an OWL file) described in the YAML config file...
    for ont_source_info_dict in ont_urls_and_files:
        if ont_source_info_dict['download']:
            # get the OWL file onto the local file system and get a full path to it
            print(ont_source_info_dict["url"])
            local_file_name = kg2_util.download_file_if_not_exist_locally(ont_source_info_dict['url'],
                                                                          ont_source_info_dict['file'])
        else:
            local_file_name = ont_source_info_dict['file']
            assert os.path.exists(ont_source_info_dict['file']), local_file_name
        # load the OWL file data into an ontobio.ontol.Ontology data structure and information dictionary
        [ont, metadata_dict] = load_ont_file_return_ontology_and_metadata(local_file_name,
                                                                          ont_source_info_dict['url'],
                                                                          ont_source_info_dict['title'],
                                                                          save_pickle)
        metadata_dict['ontology'] = ont
        ont_file_information_dict_list.append(metadata_dict)

    kg2_util.log_message('Calling make_nodes_dict_from_ontologies_list')

    nodes_dict = make_nodes_dict_from_ontologies_list(ont_file_information_dict_list,
                                                      curies_to_categories,
                                                      uri_to_curie_shortener,
                                                      curie_to_uri_expander)

    kg2_util.log_message('Calling make_map_of_node_ontology_ids_to_curie_ids')

    map_of_node_ontology_ids_to_curie_ids = make_map_of_node_ontology_ids_to_curie_ids(nodes_dict)

    kg2_util.log_message('Calling get_rels_dict')

    # get a dictionary of all relationships including xrefs as relationships
    all_rels_dict = get_rels_dict(nodes_dict,
                                  ont_file_information_dict_list,
                                  uri_to_curie_shortener,
                                  curie_to_uri_expander,
                                  map_of_node_ontology_ids_to_curie_ids)

    kg2_dict = dict()
    kg2_dict['edges'] = [rel_dict for rel_dict in all_rels_dict.values()]
    kg2_util.log_message('Number of edges: ' + str(len(kg2_dict['edges'])))
    kg2_dict['nodes'] = list(nodes_dict.values())
    kg2_util.log_message('Number of nodes: ' + str(len(kg2_dict['nodes'])))
    del nodes_dict

    # delete xrefs from all_nodes_dict
    for node_dict in kg2_dict['nodes']:
        del node_dict['xrefs']
        del node_dict['ontology node ids']

    kg2_util.log_message('Saving JSON file')
    kg2_util.save_json(kg2_dict, output_file_name, test_mode)


def get_biolink_category_for_node(ontology_node_id: str,
                                  node_curie_id: str,
                                  ontology: ontobio.ontol.Ontology,
                                  curies_to_categories: dict,
                                  uri_to_curie_shortener: callable,
                                  ontology_node_ids_previously_seen: set,
                                  get_node_id_of_node_with_category: bool,
                                  biolink_category_depths: dict):

    if node_curie_id is None:
        kg2_util.log_message("Ontology node " + ontology_node_id + " has node_curie_id of None",
                             ontology_name=ontology.id,
                             output_stream=sys.stderr)
        return [None, None]

    # if we have already looked for a category for this node, return None
    if ontology_node_id in ontology_node_ids_previously_seen:
        return [None, None]

    ontology_node_ids_previously_seen.add(ontology_node_id)

    curie_prefix = get_prefix_from_curie_id(node_curie_id)

    if curie_prefix is None:
        kg2_util.log_message("Unable to get prefix from node CURIE id",
                             ontology_name=ontology.id,
                             node_curie_id=node_curie_id,
                             output_stream=sys.stderr)
        return [None, None]

        # Inelegant hack to ensure that TUI: nodes get mapped to "semantic type" while still enabling us
        # to use get_biolink_category_for_node to determine the specific semantic type of a CUI based on its
        # TUI record. Need to think about a more elegant way to do this. [SAR]
    if curie_prefix == kg2_util.CURIE_PREFIX_UMLS_STY and node_curie_id.split(':')[1].startswith('T') and ontology.id == kg2_util.BASE_URL_UMLS_STY:
        return [kg2_util.BIOLINK_CATEGORY_ONTOLOGY_CLASS, None]

    if get_node_id_of_node_with_category:
        ret_ontology_node_id_of_node_with_category = ontology_node_id
    else:
        ret_ontology_node_id_of_node_with_category = None

    curies_to_categories_terms = curies_to_categories['term-mappings']
    curies_to_categories_prefixes = curies_to_categories['prefix-mappings']

    # check if the term directly maps
    ret_category = curies_to_categories_terms.get(node_curie_id, None)
    if ret_category is None:
        ret_category = curies_to_categories_prefixes.get(curie_prefix, None)
    if ret_category is None:
        # need to walk the ontology hierarchy until we encounter a parent term with a defined biolink category
        parent_nodes_list = list(ontology.parents(ontology_node_id, ['subClassOf']))
        parent_nodes_same_prefix = set()
        parent_nodes_different_prefix = set()
        parent_nodes_ont_to_curie = dict()
        for parent_ontology_node_id in parent_nodes_list:
            parent_node_curie_id = get_node_curie_id_from_ontology_node_id(parent_ontology_node_id,
                                                                           ontology,
                                                                           uri_to_curie_shortener,
                                                                           curie_to_uri_expander)
            parent_node_curie_prefix = get_prefix_from_curie_id(parent_node_curie_id)
            if parent_node_curie_prefix is None:
                kg2_util.log_message("Unable to get prefix from node CURIE id",
                                     ontology_name=ontology.id,
                                     node_curie_id=parent_node_curie_id,
                                     output_stream=sys.stderr)
                continue
            if parent_node_curie_prefix == curie_prefix:
                parent_nodes_same_prefix.add(parent_ontology_node_id)
            else:
                parent_nodes_different_prefix.add(parent_ontology_node_id)
            parent_nodes_ont_to_curie[parent_ontology_node_id] = parent_node_curie_id
        candidate_categories = set()
        for parent_ontology_node_id in list(parent_nodes_same_prefix) + list(parent_nodes_different_prefix):
            parent_node_curie_id = parent_nodes_ont_to_curie[parent_ontology_node_id]
            try:
                [candidate_category,
                 ontology_node_id_of_node_with_category] = get_biolink_category_for_node(parent_ontology_node_id,
                                                                                         parent_node_curie_id,
                                                                                         ontology,
                                                                                         curies_to_categories,
                                                                                         uri_to_curie_shortener,
                                                                                         ontology_node_ids_previously_seen,
                                                                                         get_node_id_of_node_with_category,
                                                                                         biolink_category_depths)
                if get_node_id_of_node_with_category and ontology_node_id_of_node_with_category is not None:
                    ret_ontology_node_id_of_node_with_category = ontology_node_id_of_node_with_category
            except RecursionError:
                kg2_util.log_message(message="recursion error: " + ontology_node_id,
                                     ontology_name=ontology.id,
                                     node_curie_id=node_curie_id,
                                     output_stream=sys.stderr)
                assert False
            if candidate_category is not None:
                candidate_categories.add(candidate_category)
        if len(candidate_categories) == 1:
            ret_category = next(iter(candidate_categories))
        elif len(candidate_categories) > 1:
            candidate_category_depths = {category: biolink_category_depths.get(kg2_util.CURIE_PREFIX_BIOLINK + ':' +
                                                                               kg2_util.convert_snake_case_to_camel_case(category.replace(' ', '_'),
                                                                                                                         uppercase_first_letter=True), None) for
                                         category in sorted(candidate_categories)}
            keys_remove = {k for k, v in candidate_category_depths.items() if v is None}
            for k in keys_remove:
                kg2_util.log_message(message="unexpected None category depth for category " + k,
                                     ontology_name=ontology.id,
                                     node_curie_id=node_curie_id,
                                     output_stream=sys.stderr)
                del candidate_category_depths[k]
#            candidate_category_depths = {k: v for k, v in candidate_category_depths.items() if v is not None}
            if len(candidate_category_depths) > 0:
                ret_category = max(candidate_category_depths, key=candidate_category_depths.get)
            else:
                assert ret_category is None
    if ret_category is None:
        if node_curie_id.startswith(kg2_util.CURIE_PREFIX_ENSEMBL + ':'):
            curie_suffix = node_curie_id.replace(kg2_util.CURIE_PREFIX_ENSEMBL + ':', '')
            ensembl_match = REGEX_ENSEMBL.match(curie_suffix)
            if ensembl_match is not None:
                ensembl_match_letter = ensembl_match[1]
                ret_category = ENSEMBL_LETTER_TO_CATEGORY.get(ensembl_match_letter, None)
                if ret_category is None:
                    kg2_util.log_message(message="unrecognized Ensembl ID: " + curie_suffix,
                                         ontology_name=ontology.id,
                                         node_curie_id=node_curie_id,
                                         output_stream=sys.stderr)

    return [ret_category, ret_ontology_node_id_of_node_with_category]


# --------------- subroutines that have no side effects except logging printing ----------


def make_rel_key(subject_id: str,
                 predicate_name: str,
                 object_id: str,
                 ontology_id: str = None):
    key = subject_id + ';' + predicate_name + ';' + object_id
    if ontology_id is not None:
        key += ';' + ontology_id
    return key


def parse_umls_sver_date(umls_sver: str, sourcename: str):
    if umls_sver.startswith(sourcename + '_'):
        umls_sver = umls_sver.split(sourcename + '_')[1]
    umls_sver_match = REGEX_YEAR.match(umls_sver)
    updated_date = None
    if umls_sver_match is not None:
        updated_date = umls_sver_match[0]
    else:
        umls_sver_match = REGEX_YEAR_MONTH_DAY.match(umls_sver)
        if umls_sver_match is not None:
            updated_date = umls_sver_match[0] + '-' + ('%0.2d' % int(umls_sver_match[1])) + '-' + ('%0.2d' % int(umls_sver_match[2]))
        else:
            umls_sver_match = REGEX_MONTH_YEAR.match(umls_sver)
            if umls_sver_match is not None:
                updated_date = umls_sver_match[1] + '-' + ('%0.2d' % int(umls_sver_match[0]))
            else:
                umls_sver_match = REGEX_YEAR_MONTH.match(umls_sver)
                if umls_sver_match is not None:
                    updated_date = umls_sver_match[0] + ('%0.2d' % int(umls_sver_match[1]))
    return updated_date


# ===========================================
# These next functions (until make_nodes_dict_from_ontologies_list)
# are for addressing issue #762 regarding duplicate TUIs


def generate_biolink_category_tree(biolink_ontology: ontobio.ontol.Ontology,
                                   curies_to_categories: dict):
    # Adapts biolink parent-child relationships into a tree format
    # Format is {parent1: [child1, child2], parent2: [child3, child4]}
    # Such that every parent is also a child of another with the exception
    # of "named thing" and no child is a child of more than one parent

    biolink_category_tree = kg2_util.get_biolink_category_tree(biolink_ontology)

    # Takes the TUI mappings from the curies-to-categories.yaml file
    # and stores them for the later functions to use
    mappings_to_categories = dict()
    terms = curies_to_categories['term-mappings']
    for term in terms:
        if term.startswith(kg2_util.CURIE_PREFIX_UMLS_STY):
            mappings_to_categories[term.split(':')[1]] = terms[term]

    return [biolink_category_tree, mappings_to_categories]


def get_shorter_list_first(list1: list, list2: list):
    # Returns the compared lists in the form [short_list, long_list]
    # for use in comparing two lists of biolink category hierarchies

    len1 = len(list1)
    len2 = len(list2)

    if len1 > len2:
        return [list2, list1]
    return [list1, list2]


def compare_two_lists_in_reverse(list1: list, list2: list):
    # Returns most specific category that present in both lists.
    # The most specific category of each list is in [0]
    # So, by comparing them in reverse, once you get to a discrepancy,
    # you go forward back to the last one where they were the same

    [shortlist, longlist] = get_shorter_list_first(list1, list2)
    for short_item in reversed(shortlist):
        if short_item not in longlist:
            return shortlist[shortlist.index(short_item) + 1]
    return shortlist[0]


def get_path(tree_dict: dict,
             base_node: str,
             goal_node: str,
             return_list: list):
    # Iterates through the biolink category tree until it gets to
    # the goal category in one of the subclasses. Once it does that,
    # it adds the superclass to the return list (which contains the
    # category hierarchy for the goal category), and if the superclass
    # isn't "named thing" (the base category), it recursively calls it again
    # with the superclass as the goal category this time, continuing
    # to add onto the return list until it hits the base category

    for superclass, subclasses in tree_dict.items():
        if goal_node in subclasses:
            return_list.append(superclass)
            if superclass != base_node:
                get_path(tree_dict, base_node, superclass, return_list)


def split_into_chunks(fulllist: list):
    # Takes a list of TUI categories and splits it into a list
    # of pairs of TUI categories so that the multiple TUI categories can
    # can be handled in pairs
    # Ex. [molecular entity, chemical substance, chemical substance] ->
    # [[molecular entity, chemical substance], [chemical substance]]

    returnlist = []
    addtofullarray = True

    for element in fulllist:
        if addtofullarray:
            returnlist.append([element])
            addtofullarray = False
        else:
            returnlist[-1].append(element)
            addtofullarray = True

    return returnlist


def find_common_ancestor(tui_categories: list, biolink_category_tree: dict):
    # Iterates through chunked TUI category list in pairs, such that
    # the most specific common ancestor between the two categories is found
    # and stored in the category list, which then gets re-chunked.
    # This continues until there is only one category - the most specific common
    # ancestory - left in the tui_categories list.

    tui_split = split_into_chunks(tui_categories)

    while len(tui_split) > 0:
        if len(tui_split[0]) == 1:
            break
        for pair in tui_split:
            if len(pair) < 2:
                tui_split[tui_split.index(pair)] = pair[0]
            else:
                path_list1 = []
                path_list1.append(pair[0])
                get_path(biolink_category_tree, "named thing", pair[0], path_list1)
                path_list2 = []
                path_list2.append(pair[1])
                get_path(biolink_category_tree, "named thing", pair[1], path_list2)
                tui_split[tui_split.index(pair)] = compare_two_lists_in_reverse(path_list1,
                                                                                path_list2)

        tui_split = split_into_chunks(tui_split)

    return tui_split[0][0]


def get_category_for_multiple_tui(biolink_category_tree: dict,
                                  tui_group: list,
                                  mappings_to_categories: dict):
    # Takes the list of multiple TUIs and uses the mappings to categories
    # dictionary to create a list of categories that can be used to find
    # the most common ancestor between them

    tui_categories = []
    for tui in tui_group:
        tui_category_snakecase = mappings_to_categories[tui]
        tui_categories.append(tui_category_snakecase)

    return find_common_ancestor(tui_categories, biolink_category_tree)


def make_nodes_dict_from_ontologies_list(ontology_info_list: list,
                                         curies_to_categories: dict,
                                         uri_to_curie_shortener: callable,
                                         curie_to_uri_expander: callable) -> Dict[str, dict]:
    ret_dict = dict()
    ontologies_iris_to_curies = dict()

    tuis_not_in_mappings_but_in_kg2 = set()

    biolink_categories_ontology_depths = None

    first_ontology = ontology_info_list[0]['ontology']

    assert first_ontology.id == kg2_util.BASE_URL_BIOLINK_ONTOLOGY, "biolink needs to be first in ont-load-inventory.yaml"

    [biolink_category_tree, mappings_to_categories] = generate_biolink_category_tree(first_ontology, curies_to_categories)

    biolink_categories_ontology_depths = kg2_util.get_biolink_categories_ontology_depths(first_ontology)

    convert_bpv_pred_to_curie_func = make_convert_bpv_predicate_to_curie(uri_to_curie_shortener,
                                                                         curie_to_uri_expander)

    def biolink_depth_getter(category: str):
        return biolink_categories_ontology_depths.get(category, None)

    for ontology_info_dict in ontology_info_list:
        ontology = ontology_info_dict['ontology']
        iri_of_ontology = ontology_info_dict['id']
        assert iri_of_ontology is not None

        ontology_curie_id = uri_to_curie_shortener(iri_of_ontology)

        if ontology_curie_id is None or len(ontology_curie_id) == 0:
            ontology_curie_id = iri_of_ontology

        print(f"processing ontology: {ontology_curie_id}", file=sys.stderr)

        umls_sver = ontology_info_dict.get('umls-sver', None)
        updated_date = None
        if umls_sver is not None:
            # if you can, parse sver string into a date string
            updated_date = parse_umls_sver_date(umls_sver, ontology_curie_id.split(':')[1])

        if updated_date is None:
            updated_date = ontology_info_dict.get('source-file-date', None)

        if updated_date is None:
            umls_release = ontology_info_dict.get('umls-release', None)
            if umls_release is not None:
                updated_date = re.sub(r'\D', '', umls_release)

        if updated_date is None:
            updated_date = ontology_info_dict['file last modified timestamp']

        ontology_node = kg2_util.make_node(ontology_curie_id,
                                           iri_of_ontology,
                                           ontology_info_dict['title'],
                                           kg2_util.BIOLINK_CATEGORY_DATA_FILE,
                                           updated_date,
                                           ontology_curie_id)
        ontology_node['description'] = ontology_info_dict['description']
        ontology_node['ontology node ids'] = [iri_of_ontology]
        ontology_node['xrefs'] = []
        ret_dict[ontology_curie_id] = ontology_node

        ontologies_iris_to_curies[iri_of_ontology] = ontology_curie_id

        for ontology_node_id in ontology.nodes():
            onto_node_dict = ontology.node(ontology_node_id)
            assert onto_node_dict is not None

            if ontology_node_id.startswith(MYSTERIOUS_BASE_NODE_ID_TO_FILTER):
                continue

            if ontology_node_id == OWL_NOTHING:
                continue

            if ontology_node_id.endswith(NOCODE):
                continue

            node_curie_id = get_node_curie_id_from_ontology_node_id(ontology_node_id,
                                                                    ontology,
                                                                    uri_to_curie_shortener,
                                                                    curie_to_uri_expander)
            if node_curie_id is None:
                kg2_util.log_message(message="Unable to obtain a CURIE for ontology node ID: " + ontology_node_id,
                                     ontology_name=iri_of_ontology,
                                     output_stream=sys.stderr)
                continue

            iri = onto_node_dict.get('id', None)
            if iri is None:
                iri = ontology_node_id

            if not kg2_util.is_a_valid_http_url(iri):
                iri = curie_to_uri_expander(iri)

            iri = curie_to_uri_expander(node_curie_id)
            if iri is None:
                kg2_util.log_message(message="Cannot obtain IRI for CURIE",
                                     ontology_name=iri_of_ontology,
                                     node_curie_id=node_curie_id,
                                     output_stream=sys.stderr)
                continue

            assert kg2_util.is_a_valid_http_url(iri), iri

            node_name = onto_node_dict.get('label', None)
            node_full_name = None

            assert node_curie_id is not None

            if node_curie_id in ret_dict:
                prev_provided_by = ret_dict[node_curie_id].get('provided_by', None)
                if prev_provided_by is not None and node_curie_id == prev_provided_by:
                    continue  # issue 984

            curie_prefix = get_prefix_from_curie_id(node_curie_id)
            if curie_prefix == kg2_util.CURIE_PREFIX_UMLS_STY and node_curie_id.split(':')[1].startswith('T') and ontology.id != kg2_util.BASE_URL_UMLS_STY:
                # this is a UMLS semantic type TUI node from a non-STY UMLS source, ignore it
                continue

            [node_category_label, node_with_category] = get_biolink_category_for_node(ontology_node_id,
                                                                                      node_curie_id,
                                                                                      ontology,
                                                                                      curies_to_categories,
                                                                                      uri_to_curie_shortener,
                                                                                      set(),
                                                                                      True,
                                                                                      biolink_categories_ontology_depths)

            node_deprecated = False
            node_description = None
            node_creation_date = None
            node_update_date = None
            node_replaced_by_curie = None
            node_full_name = None
            node_publications = set()
            node_synonyms = set()
            node_xrefs = set()
            node_tui = None
            node_has_cui = False
            node_tui_category_label = None

            node_meta = onto_node_dict.get('meta', None)
            if node_meta is not None:
                node_deprecated = node_meta.get('deprecated', False)
                node_definition = node_meta.get('definition', None)
                if node_definition is not None:
                    node_description = node_definition['val']

                    node_definition_xrefs = node_definition.get('xrefs', None)
                    if node_definition_xrefs is not None:
                        assert type(node_definition_xrefs) == list
                        for xref in node_definition_xrefs:
                            xref_pub = xref_as_a_publication(xref)
                            if xref_pub is not None:
                                node_publications.add(xref_pub)

                node_synonyms_list = node_meta.get('synonyms', None)
                if node_synonyms_list is not None:
                    for syn_dict in node_synonyms_list:
                        syn_pred = syn_dict['pred']
                        if syn_pred == 'hasExactSynonym':
                            node_synonyms.add(syn_dict['val'])
                            syn_xrefs = syn_dict['xrefs']
                            if len(syn_xrefs) > 0:
                                for syn_xref in syn_xrefs:
                                    syn_xref_pub = xref_as_a_publication(syn_xref)
                                    if syn_xref_pub is not None:
                                        node_publications.add(syn_xref_pub)

                node_xrefs_list = node_meta.get('xrefs', None)
                if node_xrefs_list is not None:
                    for xref_dict in node_xrefs_list:
                        xref_curie = xref_dict['val']
                        if xref_curie.startswith('UMLS:C'):
                            xref_curie = kg2_util.CURIE_PREFIX_UMLS + ':' + xref_curie.split('UMLS:')[1]
                        node_xrefs.add(xref_curie)
                basic_property_values = node_meta.get('basicPropertyValues', None)
                if basic_property_values is not None:
                    node_tui_list = []
                    for basic_property_value_dict in basic_property_values:
                        bpv_pred = basic_property_value_dict['pred']
                        bpv_pred_curie = convert_bpv_pred_to_curie_func(bpv_pred)
                        if bpv_pred_curie is None:
                            bpv_pred_curie = bpv_pred
                        bpv_val = basic_property_value_dict['val']
                        if bpv_pred_curie in {kg2_util.CURIE_ID_OIO_CREATION_DATE,
                                              kg2_util.CURIE_ID_DCTERMS_ISSUED,
                                              kg2_util.CURIE_ID_HGNC_DATE_CREATED}:
                            node_creation_date = bpv_val
                        elif bpv_pred_curie == kg2_util.CURIE_ID_HGNC_DATE_LAST_MODIFIED:
                            node_update_date = bpv_val
                        elif bpv_pred_curie == kg2_util.CURIE_ID_IAO_TERM_REPLACED_BY:
                            if not node_deprecated:
                                node_deprecated = True
                                kg2_util.log_message(message="Node has IAO:0100001 attribute but not owl:deprecated; setting deprecated=True",
                                                     ontology_name=iri_of_ontology,
                                                     node_curie_id=node_curie_id,
                                                     output_stream=sys.stderr)
                            node_replaced_by_uri = bpv_val
                            node_replaced_by_curie = uri_to_curie_shortener(node_replaced_by_uri)
                        elif bpv_pred_curie == kg2_util.CURIE_ID_UMLS_HAS_TUI:  # STY_BASE_IRI:
                            node_tui_list.append(bpv_val)
                        elif bpv_pred_curie == kg2_util.CURIE_ID_SKOS_PREF_LABEL:
                            if not node_curie_id.startswith(kg2_util.CURIE_PREFIX_HGNC + ':'):
                                node_name = bpv_val
                            else:
                                node_full_name = bpv_val
                                if node_name is None:
                                    node_name = node_full_name
                        elif bpv_pred_curie == kg2_util.CURIE_ID_SKOS_ALT_LABEL:
                            node_synonyms.add(bpv_val)
                        elif bpv_pred_curie == kg2_util.CURIE_ID_SKOS_DEFINITION:
                            node_description = kg2_util.strip_html(bpv_val)
                        elif bpv_pred_curie == kg2_util.CURIE_ID_HGNC_GENE_SYMBOL:
                            node_name = bpv_val
                            node_synonyms.add(bpv_val)
                        elif bpv_pred_curie == kg2_util.CURIE_ID_UMLS_HAS_CUI:
                            node_has_cui = True
                    if len(node_tui_list) == 1:
                        node_tui = node_tui_list[0]
                        node_tui_curie = kg2_util.CURIE_PREFIX_UMLS_STY + ':' + node_tui
                        node_tui_uri = curie_to_uri_expander(node_tui_curie)
                        assert node_tui_curie is not None
                        [node_tui_category_label,
                         _] = get_biolink_category_for_node(node_tui_uri,
                                                            node_tui_curie,
                                                            ontology,
                                                            curies_to_categories,
                                                            uri_to_curie_shortener,
                                                            set(),
                                                            True,
                                                            biolink_categories_ontology_depths)

                node_comments = node_meta.get('comments', None)
                if node_comments is not None:
                    comments_str = 'COMMENTS: ' + (' // '.join(node_comments))
                    if node_description is not None:
                        node_description += ' // ' + comments_str
                    else:
                        node_description = comments_str

            if node_category_label is None:
                node_type = onto_node_dict.get('type', None)
                if node_type is not None and node_type == 'PROPERTY':
                    node_category_label = kg2_util.BIOLINK_CATEGORY_ATTRIBUTE

            if node_category_label is None:
                node_category_label = 'named thing'
                try:
                    # This is a fix for #891. It was supposed to be addressed on line 756 ("if node_category_label is None:") 
                    # and 757 ("node_category_label = node_tui_category_label"), but due to the assignment of the label
                    # 'named thing', that condition was never triggered. Instead, that is now handled here.
                    if node_tui is not None:
                        node_category_label = mappings_to_categories[node_tui]
                except KeyError:
                    if not node_deprecated:
                        kg2_util.log_message(message="Node with ontology_node_id " + ontology_node_id + " does not have a category and has tui " + node_tui,
                                             output_stream=sys.stderr)
                        tuis_not_in_mappings_but_in_kg2.add(node_tui)

            if node_has_cui:
                assert node_tui is not None or len(node_tui_list) > 0
                if node_tui_category_label is None:
                    node_tui_category_label = 'named thing'
                    if node_tui is not None:
                        kg2_util.log_message(message='Node ' + ontology_node_id + ' has CUI whose TUI cannot be mapped to category: ' + node_tui,
                                             ontology_name=iri_of_ontology,
                                             output_stream=sys.stderr)
                    else:
                        try:
                            # POSSIBLY SHOULD REMOVE "or node_category_label == 'named thing'"
                            if node_category_label is None or node_category_label == 'named thing' or node_curie_id.split(":")[0] == kg2_util.CURIE_PREFIX_UMLS:
                                node_tui_category_label = get_category_for_multiple_tui(biolink_category_tree, node_tui_list, mappings_to_categories)
                                node_category_label = node_tui_category_label
                        except KeyError:
                            kg2_util.log_message(message='Node ' + node_curie_id + ' has CUI with multiple associated TUIs: ' + ', '.join(node_tui_list) +
                                                 ' and could not be mapped',
                                                 ontology_name=iri_of_ontology,
                                                 output_stream=sys.stderr)
                else:
                    if node_category_label is None:
                        node_category_label = node_tui_category_label  # override the node category_label if we have a TUI
                node_tui_category_curie = kg2_util.convert_biolink_category_to_curie(node_tui_category_label)
            ontology_curie_id = ontologies_iris_to_curies[iri_of_ontology]
            source_ontology_information = ret_dict.get(ontology_curie_id, None)
            if source_ontology_information is None:
                kg2_util.log_message(message="ontology IRI has no information dictionary available",
                                     ontology_name=iri_of_ontology,
                                     output_stream=sys.stderr)
                assert False
            source_ontology_update_date = source_ontology_information['update_date']
            if node_update_date is None:
                node_update_date = source_ontology_update_date

            if node_description is not None:
                node_description_xrefs_match = REGEX_XREF_END_DESCRIP.match(node_description)
                if node_description_xrefs_match is not None:
                    node_description_xrefs_str = node_description_xrefs_match[1]
                    node_description_xrefs_list = node_description_xrefs_str.split(',')
                    for node_description_xref_str in node_description_xrefs_list:
                        node_description_xref_str = node_description_xref_str.strip()
                        if ':' in node_description_xref_str:
                            node_xrefs.add(node_description_xref_str)
                node_description_pubs = REGEX_PUBLICATIONS.findall(node_description)
                for pub_curie in node_description_pubs:
                    node_publications.add(pub_curie)

            # deal with node names that are ALLCAPS
            if node_name is not None and node_name.isupper():
                node_name = kg2_util.allcaps_to_only_first_letter_capitalized(node_name)

            if node_name is not None:
                if node_name.lower().startswith('obsolete:'):
                    continue

            if node_description is not None:
                if node_description.lower().startswith('obsolete:') or node_description.lower().startswith('obsolete.'):
                    continue

            provided_by = ontology_curie_id
            if node_category_label == kg2_util.BIOLINK_CATEGORY_ATTRIBUTE:
                provided_by = kg2_util.CURIE_ID_UMLS_STY

            node_dict = kg2_util.make_node(node_curie_id,
                                           iri,
                                           node_name,
                                           node_category_label,
                                           node_update_date,
                                           provided_by)

            node_dict['full_name'] = node_full_name
            node_dict['description'] = node_description
            node_dict['creation_date'] = node_creation_date      # slot name is not biolink standard
            node_dict['deprecated'] = node_deprecated            # slot name is not biolink standard
            node_dict['replaced_by'] = node_replaced_by_curie    # slot name is not biolink standard
            node_dict['ontology node ids'] = [ontology_node_id]  # slot name is not biolink standard
            node_dict['xrefs'] = sorted(list(node_xrefs))        # slot name is not biolink standard
            node_dict['synonym'] = sorted(list(node_synonyms))   # slot name is not biolink standard
            node_dict['publications'] = sorted(list(node_publications))

            # check if we need to make a CUI node
            if node_meta is not None and basic_property_values is not None:
                for basic_property_value_dict in basic_property_values:
                    bpv_pred = basic_property_value_dict['pred']
                    bpv_pred_curie = convert_bpv_pred_to_curie_func(bpv_pred)
                    bpv_val = basic_property_value_dict['val']
                    if bpv_pred_curie == kg2_util.CURIE_ID_UMLS_HAS_CUI:
                        cui_node_dict = dict(node_dict)
                        cui_uri = kg2_util.BASE_URL_UMLS + bpv_val
                        cui_curie = uri_to_curie_shortener(cui_uri)
                        assert cui_curie is not None
                        # Skip this CUI if it's identical to the ontology node itself (happens with files created
                        # using 'load_on_cuis' - part of fix for issue #565)
                        if get_local_id_from_curie_id(cui_curie) == get_local_id_from_curie_id(node_curie_id):
                            continue
                        cui_node_dict['id'] = cui_curie
                        cui_node_dict['iri'] = cui_uri
                        cui_node_dict['synonym'] = []
                        cui_node_dict['category'] = node_tui_category_curie
                        cui_node_dict['category_label'] = node_tui_category_label.replace(' ', '_')
                        cui_node_dict['ontology node ids'] = []
                        cui_node_dict['provided_by'] = kg2_util.CURIE_ID_UMLS_SOURCE_CUI
                        cui_node_dict['xrefs'] = []  # blanking the "xrefs" here is *vital* in order to avoid issue #395
                        cui_node_dict_existing = ret_dict.get(cui_curie, None)
                        if cui_node_dict_existing is not None:
                            cui_node_dict = kg2_util.merge_two_dicts(cui_node_dict,
                                                                     cui_node_dict_existing,
                                                                     biolink_depth_getter)
                        ret_dict[cui_curie] = cui_node_dict
                        node_dict_xrefs = node_dict['xrefs']
                        node_dict_xrefs.append(cui_curie)
                        node_dict['xrefs'] = sorted(list(set(node_dict_xrefs)))
                    elif bpv_pred_curie == kg2_util.CURIE_ID_HGNC_ENTREZ_GENE_ID:
                        entrez_gene_id = bpv_val
                        entrez_node_dict = dict(node_dict)
                        entrez_curie = kg2_util.CURIE_PREFIX_NCBI_GENE + ':' + entrez_gene_id
                        entrez_node_dict['id'] = entrez_curie
                        entrez_node_dict['iri'] = curie_to_uri_expander(entrez_curie)
                        ret_dict[entrez_curie] = entrez_node_dict
                        node_dict_xrefs = node_dict['xrefs']
                        node_dict_xrefs.append(entrez_curie)
                        node_dict['xrefs'] = sorted(list(set(node_dict_xrefs)))
            if node_curie_id in ret_dict:
                if node_curie_id != provided_by:
                    node_dict = kg2_util.merge_two_dicts(ret_dict[node_curie_id],
                                                         node_dict,
                                                         biolink_depth_getter)
                    ret_dict[node_curie_id] = node_dict
                else:
                    ret_dict[node_curie_id] = node_dict  # issue 984
            else:
                ret_dict[node_curie_id] = node_dict

    return ret_dict


def get_rels_dict(nodes: dict,
                  ont_file_information_dict_list: list,
                  uri_to_curie_shortener: callable,
                  curie_to_uri_expander: callable,
                  map_of_node_ontology_ids_to_curie_ids: dict):
    rels_dict = dict()

    for ont_file_information_dict in ont_file_information_dict_list:
        ontology = ont_file_information_dict['ontology']
        ontology_id = ont_file_information_dict['id']
        ont_graph = ontology.get_graph()
        ontology_curie_id = map_of_node_ontology_ids_to_curie_ids[ontology_id]
        for (object_id, subject_id, predicate_dict) in ont_graph.edges(data=True):
            assert type(predicate_dict) == dict

            ontology_node = nodes.get(ontology_curie_id, None)
            if ontology_node is not None:
                ontology_update_date = ontology_node['update_date']

            if subject_id == OWL_BASE_CLASS or object_id == OWL_BASE_CLASS:
                continue

            if subject_id == OWL_NOTHING or object_id == OWL_NOTHING:
                continue

            if subject_id.startswith(MYSTERIOUS_BASE_NODE_ID_TO_FILTER) or \
               object_id.startswith(MYSTERIOUS_BASE_NODE_ID_TO_FILTER):
                continue

            if subject_id.endswith(NOCODE) or object_id.endswith(NOCODE):
                continue

            # subject_id and object_id are IDs from the original ontology objects; these may not
            # always be the node curie IDs (e.g., for SNOMED terms). Need to map them
            subject_curie_id = map_of_node_ontology_ids_to_curie_ids.get(subject_id, None)
            if subject_curie_id is None:
                kg2_util.log_message(message="subject node ontology ID has no curie ID in the map",
                                     ontology_name=ontology.id,
                                     node_curie_id=subject_id,
                                     output_stream=sys.stderr)
                continue
            object_curie_id = map_of_node_ontology_ids_to_curie_ids.get(object_id, None)
            if object_curie_id is None:
                kg2_util.log_message(message="object node ontology ID has no curie ID in the map",
                                     ontology_name=ontology.id,
                                     node_curie_id=object_id,
                                     output_stream=sys.stderr)
                continue

            predicate_label = None
            edge_pred_string = predicate_dict['pred']

            if subject_curie_id.startswith(kg2_util.CURIE_PREFIX_UMLS_STY) and \
               object_curie_id.startswith(kg2_util.CURIE_PREFIX_UMLS_STY) and edge_pred_string == 'subClassOf':
                continue

            if edge_pred_string == "type" and ontology_curie_id.startswith(kg2_util.CURIE_PREFIX_BIOLINK_SOURCE + ':'):
                continue

            if not kg2_util.is_a_valid_http_url(edge_pred_string):
                # edge_pred_string is not a URI; this is the most common case
                if ':' not in edge_pred_string:
                    # edge_pred_string is not a CURIE; this is the most common subcase
                    if edge_pred_string in kg2_util.RDFS_EDGE_NAMES_SET:
                        predicate_curie = kg2_util.CURIE_PREFIX_RDFS + ':' + edge_pred_string
                    elif edge_pred_string in kg2_util.OWL_EDGE_NAMES_SET:
                        predicate_curie = kg2_util.CURIE_PREFIX_OWL + ':' + edge_pred_string
                    elif edge_pred_string in kg2_util.MONDO_EDGE_NAMES_SET:
                        predicate_curie = kg2_util.CURIE_PREFIX_MONDO + ':' + edge_pred_string
                    else:
                        assert "Cannot map predicate name: " + edge_pred_string + " to a predicate CURIE, in ontology: " + ontology.id
                    predicate_label = kg2_util.convert_camel_case_to_snake_case(edge_pred_string)
                else:
                    # edge_pred_string is a CURIE
                    predicate_curie = edge_pred_string
                    predicate_node = nodes.get(predicate_curie, None)
                    if predicate_node is not None:
                        predicate_label = predicate_node['name']
                    else:
                        # predicate has no node object defined; just pull the label out of the CURIE
                        if edge_pred_string.startswith(kg2_util.CURIE_PREFIX_OBO + ':'):
                            test_curie = edge_pred_string.replace(kg2_util.CURIE_PREFIX_OBO + ':', '').replace('_', ':')
                            predicate_node = nodes.get(test_curie, None)
                            if predicate_node is None:
                                predicate_label = edge_pred_string.split(':')[1].split('#')[-1]
                            else:
                                predicate_curie = test_curie
                        else:
                            predicate_label = edge_pred_string
                predicate_iri = curie_to_uri_expander(predicate_curie)
                predicate_curie_new = uri_to_curie_shortener(predicate_iri)
                if predicate_curie_new is not None:
                    predicate_curie = predicate_curie_new
            else:
                predicate_iri = edge_pred_string
                predicate_curie = uri_to_curie_shortener(predicate_iri)

            if predicate_curie is None:
                kg2_util.log_message(message="predicate IRI has no CURIE: " + predicate_iri,
                                     ontology_name=ontology.id,
                                     output_stream=sys.stderr)
                continue

            if subject_curie_id == object_curie_id and predicate_label == 'xref':
                continue

            if predicate_curie == kg2_util.CURIE_ID_UMLS_HAS_STY:
                subject_node = nodes[subject_curie_id]
                object_node = nodes[object_curie_id]
                subject_description = subject_node['description']
                if subject_description is None:
                    subject_description = ''
                subject_node['description'] = '; '.join(list(filter(None, [subject_description,
                                                                           'UMLS Semantic Type: ' + object_node['id']])))
                continue

            rel_key = make_rel_key(subject_curie_id, predicate_curie, object_curie_id, ontology_curie_id)

            if predicate_label is None and ':' in predicate_curie:
                pred_node = nodes.get(predicate_curie, None)
                if pred_node is not None:
                    predicate_label = pred_node['name']
                    assert predicate_label is not None
                    if predicate_label[0].isupper():
                        predicate_label = predicate_label[0].lower() + predicate_label[1:]

            assert predicate_label is not None
            predicate_label = predicate_label.replace(' ', '_')
            # Only tested on Food and Efo ontologies
            predicate_label = kg2_util.convert_camel_case_to_snake_case(predicate_label)
            if rels_dict.get(rel_key, None) is None:
                edge = kg2_util.make_edge(subject_curie_id,
                                          object_curie_id,
                                          predicate_curie,
                                          predicate_label,
                                          ontology_curie_id,
                                          ontology_update_date)
                rels_dict[rel_key] = edge
        for node_id, node_dict in nodes.items():
            xrefs = node_dict['xrefs']
            if xrefs is not None:
                for xref_node_id in xrefs:
                    if xref_node_id in nodes and node_id != xref_node_id:
                        provided_by = nodes[node_id]['provided_by']
                        key = make_rel_key(node_id, CURIE_OBO_XREF, xref_node_id, provided_by)
                        if rels_dict.get(key, None) is None:
                            edge = kg2_util.make_edge(node_id,
                                                      xref_node_id,
                                                      CURIE_OBO_XREF,
                                                      'xref',
                                                      provided_by,
                                                      ontology_update_date)
                            rels_dict[key] = edge

    return rels_dict


def get_node_curie_id_from_ontology_node_id(ontology_node_id: str,
                                            ontology: ontobio.ontol.Ontology,
                                            uri_to_curie_shortener: callable,
                                            curie_to_uri_expander: callable):
    node_curie_id = None
    if not kg2_util.is_a_valid_http_url(ontology_node_id):
        # this ontology_node_id is probably a CURIE ID; proceed accordingly
        iri = curie_to_uri_expander(ontology_node_id)
        if iri is not None:
            node_curie_id = uri_to_curie_shortener(iri)
        else:
            kg2_util.log_message(message="Unable to expand ontology node ID to an IRI",
                                 ontology_name=ontology.id,
                                 node_curie_id=ontology_node_id,
                                 output_stream=sys.stderr)
            return None
    else:
        iri = ontology_node_id
        node_curie_id = uri_to_curie_shortener(iri)

    if node_curie_id is None:
        kg2_util.log_message(message="could not shorten this IRI to a CURIE",
                             ontology_name=ontology.id,
                             node_curie_id=iri,
                             output_stream=sys.stderr)

    if node_curie_id is not None:
        if is_cui_id(node_curie_id):
            curie_prefix = get_prefix_from_curie_id(node_curie_id)
            if curie_prefix is not None:
                if curie_prefix != kg2_util.CURIE_PREFIX_UMLS:
                    node_curie_id = kg2_util.CURIE_PREFIX_UMLS + ':' + get_local_id_from_curie_id(node_curie_id)
            else:
                kg2_util.log_message(message="could not obtain prefix from node CURIE ID",
                                     ontology_name=ontology.id,
                                     node_curie_id=node_curie_id,
                                     output_stream=sys.stderr)

#    if node_curie_id is None:
#        print(ontology_node_id)
#    else:
#    # Ensure that all CUI CURIE IDs use the "umls:" prefix (part of fix for issue #565)
#        if is_cui_id(node_curie_id) and get_prefix_from_curie_id(node_curie_id) != CUI_PREFIX:
#            node_curie_id = CUI_PREFIX + ":" + get_local_id_from_curie_id(node_curie_id)

    return node_curie_id

# --------------- pure functions here -------------------


def is_ignorable_ontology_term(iri: str):
    parsed_iri = urllib.parse.urlparse(iri)
    iri_netloc = parsed_iri.netloc
    iri_path = parsed_iri.path
    return iri_netloc in ('example.com', 'usefulinc.com') or iri_path.startswith('/ontology/provisional')


def get_prefix_from_curie_id(curie_id: str):
    if curie_id is None or ':' not in curie_id:
        return None
    return curie_id.split(':')[0]


def get_local_id_from_curie_id(curie_id: str):
    """
    This function returns the local ID from a CURIE ID, where a CURIE ID consists of "<Prefix>:<Local ID>".
    For example, the function would return "C3540330" for CURIE ID "umls:C3540330".
    """
    assert ':' in curie_id
    return curie_id.split(':')[1]


def is_cui_id(curie_id: str):
    """
    This function determines if the local ID in a CURIE ID is a CUI, regardless of the CURIE prefix used.
    For example, the function would return True for CURIE ID "MTH:C1527116".
    """
    local_id = get_local_id_from_curie_id(curie_id)
    # CUIs consist of the letter 'C' followed by 7 numbers
    return True if local_id.startswith('C') and len(local_id) == 8 and local_id[1:].isdigit() else False


def make_map_of_node_ontology_ids_to_curie_ids(nodes: dict):
    ret_dict = dict()
    for curie_id, node_dict in nodes.items():
        ontology_node_ids = node_dict['ontology node ids']
        assert curie_id not in ret_dict
        assert ontology_node_ids is not None
        assert type(ontology_node_ids) == list
        for ontology_node_id in ontology_node_ids:
            ret_dict[ontology_node_id] = curie_id
    return ret_dict


def xref_as_a_publication(xref: str):
    ret_xref = None
    xref = xref.lower().strip("url:").strip()

    pubmed_url_prefixes = ['https://pubmed.ncbi.nlm.nih.gov/',
                           'http://www.ncbi.nlm.nih.gov/pubmed/',
                           'https://www.ncbi.nlm.nih.gov/pubmed/',
                           'http://www.ncbi.nlm.nih.gov/pubmed?term=',
                           'http://www.pubmedcentral.nih.gov/articlerender.fcgi?tool=pubmed&pubmedid=',
                           'http://www.ncbi.nlm.nih.gov/entrez/query.fcgi?cmd=retrieve&db=pubmed&list_uids=',
                           'http://www.ncbi.nlm.nih.gov:80/entrez/query.fcgi?cmd=retrieve&db=pubmed&list_uids=',
                           None]

    if xref.upper().startswith(kg2_util.CURIE_PREFIX_PMID + ':') or xref.upper().startswith(kg2_util.CURIE_PREFIX_ISBN + ':'):
        ret_xref = xref.upper()
    elif kg2_util.is_a_valid_http_url(xref):
        for pubmed_url_prefix in pubmed_url_prefixes:
            if pubmed_url_prefix is None:
                ret_xref = xref
            elif xref.startswith(pubmed_url_prefix):
                ret_xref = kg2_util.CURIE_PREFIX_PMID + ':' + xref.replace(pubmed_url_prefix, "")
                ret_xref = ret_xref.upper().replace("DOPT=ABSTRACT", "")
                ret_xref = ret_xref.replace("TERM=", "").replace("/", "")
                ret_xref = ret_xref.replace(",", "").replace("&", "").replace("?", "")
                break

    return ret_xref


def convert_bpv_predicate_to_curie(bpv_pred: str,
                                   uri_shortener: callable,
                                   curie_expander: callable) -> str:
    if kg2_util.is_a_valid_http_url(bpv_pred):
        bpv_pred_curie = uri_shortener(bpv_pred)
    else:
        assert ':' in bpv_pred, bpv_pred
        uri = curie_expander(bpv_pred)
        if uri is None:
            raise ValueError('unable to expand CURIE: ' + bpv_pred)
        bpv_pred_curie = uri_shortener(uri)
    return bpv_pred_curie


def make_convert_bpv_predicate_to_curie(uri_shortener: callable,
                                        curie_expander: callable) -> callable:
    return lambda bpv_pred: convert_bpv_predicate_to_curie(bpv_pred,
                                                           uri_shortener,
                                                           curie_expander)


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='multi_ont_to_json_kg.py: builds the KG2 knowledge graph for the RTX system')
    arg_parser.add_argument('--test', dest='test', action="store_true", default=False)
    arg_parser.add_argument('--savePickle', dest='save_pickle', action="store_true", default=False)
    arg_parser.add_argument('categoriesFile', type=str)
    arg_parser.add_argument('curiesToURIFile', type=str)
    arg_parser.add_argument('ontLoadInventoryFile', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser


# --------------- main starts here -------------------

if __name__ == '__main__':
    delete_ontobio_cachier_caches()
    args = make_arg_parser().parse_args()
    curies_to_categories_file_name = args.categoriesFile
    curies_to_uri_file_name = args.curiesToURIFile
    ont_load_inventory_file = args.ontLoadInventoryFile
    output_file = args.outputFile
    save_pickle = args.save_pickle
    test_mode = args.test
    curies_to_categories = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_categories_file_name))
    map_dict = kg2_util.make_uri_curie_mappers(curies_to_uri_file_name)
    [curie_to_uri_expander, uri_to_curie_shortener] = [map_dict['expand'], map_dict['contract']]

    ont_urls_and_files = tuple(kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(ont_load_inventory_file)))

    make_kg2(curies_to_categories,
             uri_to_curie_shortener,
             curie_to_uri_expander,
             ont_urls_and_files,
             output_file,
             test_mode,
             save_pickle)
