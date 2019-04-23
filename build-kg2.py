#!/usr/bin/python3
'''Builds the RTX "KG2" second-generation knowledge graph, from various OWL input files.

   Usage: build-kg2.py <categoriesFile.yaml> <curiesToURILALFile> <owlLoadInventoryFile.yaml> <outputFile>
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import argparse
import collections
import copy
import errno
import functools
import hashlib
import io
import json
import ontobio
import os.path
import pathlib
import pickle
import posixpath
import pprint
import prefixcommons
import re
import shutil
import ssl
import subprocess
import sys
import tempfile
import time
import timeit
import urllib.parse
import urllib.request
import yaml
# import ipdb # need this for interactive debugging


# -------------- define globals here ---------------

USE_ONTOBIO_JSON_CACHE = True
BIOLINK_CATEGORY_BASE_IRI = 'http://w3id.org/biolink'
FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')
ENSEMBL_RE = re.compile('ENS[A-Z]{0,3}([PG])[0-9]{11}')
TEMP_FILE_PREFIX = 'kg2'

# -------------- subroutines with side-effects go here ------------------


def purge(dir, pattern):
    exp_dir = os.path.expanduser(dir)
    for f in os.listdir(exp_dir):
        if re.search(pattern, f):
            os.remove(os.path.join(exp_dir, f))


def delete_ontobio_cachier_caches():
    purge("~/.cachier", ".ontobio*")
    purge("~/.cachier", ".prefixcommons*")


# this function is needed due to an issue with caching in Ontobio; see this GitHub issue:
#     https://github.com/biolink/ontobio/issues/301
def delete_ontobio_cache_json(file_name):
    file_name_hash = hashlib.sha256(file_name.encode()).hexdigest()
    temp_file_path = os.path.join("/tmp", file_name_hash)
    if os.path.exists(temp_file_path):
        try:
            log_message(message="Deleting ontobio JSON cache file: " + temp_file_path)
            os.remove(temp_file_path)
        except OSError as e:
            if e.errno == errno.ENOENT:
                log_message(message="Error deleting ontobio JSON cache file: " + temp_file_path)
            else:
                raise e


def head_list(x: list, n: int = 3):
    pprint.pprint(x[0:n])


def head_dict(x: dict, n: int = 3):
    pprint.pprint(dict(list(x.items())[0:(n-1)]))


def log_message(message: str,
                ontology_name: str = None,
                node_curie_id: str = None,
                output_stream=sys.stdout):
    if node_curie_id is not None:
        node_str = ": " + node_curie_id
    else:
        node_str = ""
    if ontology_name is not None:
        ont_str = '[' + ontology_name + '] '
    else:
        ont_str = ''
    print(ont_str + message + node_str, file=output_stream)


# this function will load the ontology object from a pickle file (if it exists) or
# it will create the ontology object by parsing the OWL-XML ontology file
def make_ontology_from_local_file(file_name: str):
    file_name_without_ext = os.path.splitext(file_name)[0]
    file_name_with_pickle_ext = file_name_without_ext + ".pickle"
    if not os.path.isfile(file_name_with_pickle_ext):
        temp_file_name = tempfile.mkstemp(prefix=TEMP_FILE_PREFIX + '-')[1] + '.json'
        size = os.path.getsize(file_name)
        log_message(message="Reading ontology file: " + file_name + "; size: " + "{0:.2f}".format(size/1024) + " KiB",
                    ontology_name=None)
        cp = subprocess.run(['owltools', file_name, '-o', '-f', 'json', temp_file_name])
        # robot commented out because it is giving a NullPointerException on umls_semantictypes.owl
#        cp = subprocess.run(['robot', 'convert', '--input', file_name, '--output', temp_file_name])
        if cp.stdout is not None:
            log_message(message="OWL convert result: " + cp.stdout, ontology_name=None, output_stream=sys.stdout)
        if cp.stderr is not None:
            log_message(message="OWL convert result: " + cp.stderr, ontology_name=None, output_stream=sys.stderr)
        assert cp.returncode == 0
        json_file = file_name_without_ext + ".json"
        shutil.move(temp_file_name, json_file)
        size = os.path.getsize(json_file)
        log_message(message="Reading ontology JSON file: " + json_file + "; size: " + "{0:.2f}".format(size/1024) + " KiB",
                    ontology_name=None)
#        if not USE_ONTOBIO_JSON_CACHE:
#            delete_ontobio_cache_json(file_name)
        ont_return = ontobio.ontol_factory.OntologyFactory().create(json_file, ignore_cache=True)
    else:
        size = os.path.getsize(file_name_with_pickle_ext)
        log_message("Reading ontology file: " + file_name_with_pickle_ext + "; size: " + "{0:.2f}".format(size/1024) + " KiB", ontology_name=None)
        ont_return = pickle.load(open(file_name_with_pickle_ext, "rb"))
    return ont_return


def get_file_last_modified_timestamp(file_name: str):
    return time.gmtime(os.path.getmtime(file_name))


def make_ontology_dict_from_local_file(file_name: str,
                                       download_url: str = None,
                                       ontology_title: str = None):
    ontology = make_ontology_from_local_file(file_name)
    file_last_modified_timestamp = time.strftime('%Y-%m-%d %H:%M:%S %Z',
                                                 get_file_last_modified_timestamp(file_name))
    ont_version = ontology.meta.get('version', None)
    bpv = ontology.meta.get('basicPropertyValues', None)
    title = ontology_title
    description = None
    if bpv is not None:
        for bpv_dict in bpv:
            pred = bpv_dict['pred']
            value = bpv_dict['val']
            if 'description' in pred:
                description = value
            elif 'title' in pred and title is None:
                title = value
    if ont_version is None:
        ont_version = 'downloaded:' + file_last_modified_timestamp
    ontology_id = ontology.id
    if not ontology_id.startswith('http:'):
        if download_url is not None:
            ontology_id = download_url
        else:
            ontology_id = os.path.basename(file_name)
    ont_dict = {'ontology': ontology,
                'id': ontology_id,
                'handle': ontology.handle,
                'file': file_name,
                'file last modified timestamp': file_last_modified_timestamp,
                'version': ont_version,
                'title': title,
                'description': description}
    return ont_dict


def download_file_if_not_exist_locally(url: str, local_file_name: str):
    if url is not None:
        local_file_path = pathlib.Path(local_file_name)
        if not local_file_path.is_file():
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            # the following code is ugly but necessary because sometimes the TLS
            # certificates of remote sites are broken and some of the PURL'd
            # URLs resolve to HTTPS URLs (would prefer to just use
            # urllib.request.urlretrieve, but it doesn't seem to support
            # specifying an SSL "context" which we need in order to ignore the cert):
            temp_file_name = tempfile.mkstemp(prefix=TEMP_FILE_PREFIX + '-')[1]
            with urllib.request.urlopen(url, context=ctx) as u, open(temp_file_name, 'wb') as f:
                f.write(u.read())
            shutil.move(temp_file_name, local_file_name)
    return local_file_name


def read_file_to_string(local_file_name: str):
    with open(local_file_name, 'r') as myfile:
        file_contents_string = myfile.read()
    myfile.close()
    return file_contents_string


def make_kg2(curies_to_categories: dict,
             uri_to_curie_shortener: callable,
             map_category_label_to_iri: callable,
             ontology_urls_and_files: tuple,
             output_file: str):

    ontology_data = []
    for ont_source_info_dict in ontology_urls_and_files:
        local_file_name = download_file_if_not_exist_locally(ont_source_info_dict['url'],
                                                             ont_source_info_dict['file'])
        ont = make_ontology_dict_from_local_file(local_file_name,
                                                 ont_source_info_dict['url'],
                                                 ont_source_info_dict['title'])
        ontology_data.append(ont)

    master_ontology = copy.deepcopy(ontology_data[0]['ontology'])
    master_ontology.merge([ont_dict['ontology'] for ont_dict in ontology_data[1:len(ontology_data)]])

    nodes_dict = make_nodes_dict_from_ontology(master_ontology,
                                               curies_to_categories,
                                               uri_to_curie_shortener,
                                               map_category_label_to_iri)

    nodes_dict.update(make_node_dicts_for_ontologies(ontology_data,
                                                     uri_to_curie_shortener,
                                                     map_category_label_to_iri))

    map_of_node_ontology_ids_to_curie_ids = make_map_of_node_ontology_ids_to_curie_ids(nodes_dict)
    kg2_dict = dict()

    # get a dictionary of all relationships including xrefs as relationships
    all_rels_dict = dict()
    for ontology in ontology_data:
        rels_dict = get_rels_dict(nodes_dict,
                                  ontology['ontology'],
                                  uri_to_curie_shortener,
                                  map_of_node_ontology_ids_to_curie_ids)
        all_rels_dict = merge_two_dicts(all_rels_dict, rels_dict)
    kg2_dict['edges'] = [rel_dict for rel_dict in all_rels_dict.values()]
#    kg2_dict['edges'] = list(get_rels_dict(nodes_dict,
#                                           master_ontology,
#                                           uri_to_curie_shortener,
#                                           map_of_node_ontology_ids_to_curie_ids).values())
    log_message('Number of edges: ' + str(len(kg2_dict['edges'])))
    kg2_dict['nodes'] = list(nodes_dict.values())
    for node in kg2_dict['nodes']:
        if node['category'] is None:
            log_message('Node does not have a category defined', node['source ontology iri'], node['id'], output_stream=sys.stderr)
    log_message('Number of nodes: ' + str(len(kg2_dict['nodes'])))
    del nodes_dict

    # delete xrefs from all_nodes_dict
    for node_dict in kg2_dict['nodes']:
        del node_dict['xrefs']

#    timestamp_str = datetime.datetime.utcnow().replace(microsecond=0).isoformat()
    temp_output_file = tempfile.mkstemp(prefix='kg2')[1]
    with open(temp_output_file, 'w') as outfile:
        json.dump(kg2_dict, outfile)
    shutil.move(temp_output_file, output_file)

#    pickle.dump(kg2_dict, open(os.path.join(output_dir, 'kg2-' + timestamp_str + '.pickle'), 'wb'))


# --------------- subroutines that could be made into pure functions ----------


def shorten_iri_to_curie(iri: str, curie_to_iri_lookaside_list: list = []):
    if iri.startswith('owl:'):
        return iri
    curie_list = prefixcommons.contract_uri(iri,
                                            prefixcommons.curie_util.default_curie_maps +
                                            curie_to_iri_lookaside_list)
    assert len(curie_list) in [0, 1]
    if len(curie_list) == 1:
        curie_id = curie_list[0]
    else:
        curie_id = None
    return curie_id


def get_biolink_category_for_node(ontology_node_id: str,
                                  node_curie_id: str,
                                  ontology: ontobio.ontol.Ontology,
                                  curies_to_categories: dict,
                                  uri_to_curie_shortener: callable):

    ret_category = None
    if ontology_node_id == 'owl:Nothing' or node_curie_id is None:
        return None

#    print("looking for category for node: " + node_curie_id)
    curie_prefix = get_prefix_from_curie_id(node_curie_id)
    curies_to_categories_prefixes = curies_to_categories['prefix-mappings']
    ret_category = curies_to_categories_prefixes.get(curie_prefix, None)
    if ret_category is None:
        # need to walk the ontology hierarchy until we encounter a parent term with a defined biolink category
        curies_to_categories_terms = curies_to_categories['term-mappings']
        ret_category = curies_to_categories_terms.get(node_curie_id, None)
        if ret_category is None:
            for parent_ontology_node_id in ontology.parents(ontology_node_id, ['subClassOf']):
                parent_node_curie_id = get_node_curie_id_from_ontology_node_id(parent_ontology_node_id,
                                                                               ontology,
                                                                               uri_to_curie_shortener)
                try:
                    ret_category = get_biolink_category_for_node(parent_ontology_node_id,
                                                                 parent_node_curie_id,
                                                                 ontology,
                                                                 curies_to_categories,
                                                                 uri_to_curie_shortener)
                except RecursionError:
                    log_message(message="recursion error: " + ontology_node_id,
                                ontology_name=ontology.id,
                                node_curie_id=node_curie_id,
                                output_stream=sys.stderr)
                    assert False
                if ret_category is not None:
                    break
    if ret_category is None:
        # this is to handle SNOMED CT attributes:
        if node_curie_id.startswith('SNOMEDCT_US'):
            ontology_node_lbl = ontology.node(ontology_node_id).get('lbl', None)
            if ontology_node_lbl is not None:
                if '(attribute)' in ontology_node_lbl:
                    ret_category = 'attribute'
                else:
                    log_message('Node does not have a label or any parents',
                                'http://snomed.info/sct/900000000000207008',
                                node_curie_id, output_stream=sys.stderr)
        elif node_curie_id.startswith('ENSEMBL:'):
            curie_suffix = node_curie_id.replace('ENSEMBL:', '')
            ensembl_match = re.match(ENSEMBL_RE, curie_suffix)
            if ensembl_match is not None:
                ensembl_match_letter = ensembl_match[1]
                if ensembl_match_letter == 'G':
                    ret_category = 'gene'
                elif ensembl_match_letter == 'P':
                    ret_category = 'protein'
                elif ensembl_match_letter == 'T':
                    ret_category = 'transcript'
                else:
                    log_message(message="unrecognized Ensembl ID: " + curie_suffix,
                                ontology_name=ontology.id,
                                node_curie_id=node_curie_id,
                                output_stream=sys.stderr)
    return ret_category


def get_node_curie_id_from_ontology_node_id(ontology_node_id: str,
                                            ontology: ontobio.ontol.Ontology,
                                            uri_to_curie_shortener: callable):
    node_curie_id = None
    if not ontology_node_id.startswith('http:') and not ontology_node_id.startswith('https:'):
        node_curie_id = ontology_node_id
    else:
        node_curie_id = uri_to_curie_shortener(ontology_node_id)
        if node_curie_id is None:
            log_message(message="could not shorten this IRI to a CURIE",
                        ontology_name=ontology.id,
                        node_curie_id=ontology_node_id,
                        output_stream=sys.stderr)
            node_curie_id = ontology_node_id
    return node_curie_id


def make_nodes_dict_from_ontology(ontology: ontobio.ontol.Ontology,
                                  curies_to_categories: dict,
                                  uri_to_curie_shortener: callable,
                                  category_label_to_iri_mapper: callable):
    ret_dict = dict()

    for ontology_node_id in ontology.nodes():
        onto_node_dict = ontology.node(ontology_node_id)
        assert onto_node_dict is not None

        if ontology_node_id.startswith('_:genid'):
            continue

        node_curie_id = get_node_curie_id_from_ontology_node_id(ontology_node_id,
                                                                ontology,
                                                                uri_to_curie_shortener)
#        if len(onto_node_dict) == 0:
#            log_message('Node has empty dictionary of data', ontology.id, node_curie_id,
#                        output_stream=sys.stderr)
#            continue
        iri = onto_node_dict.get('id', None)
        if iri is None:
            iri = ontology_node_id

        node_dict = dict()
        node_dict['id'] = node_curie_id
        node_dict['iri'] = iri
        node_label = onto_node_dict.get('label', None)
        node_name = onto_node_dict.get('lbl', None)
        node_meta = onto_node_dict.get('meta', None)
        if node_meta is not None:
            node_deprecated = node_meta.get('deprecated', False)
        node_category_label = get_biolink_category_for_node(ontology_node_id,
                                                            node_curie_id,
                                                            ontology,
                                                            curies_to_categories,
                                                            uri_to_curie_shortener)
        node_deprecated = False
        node_description = None
        node_synonyms = None
        node_xrefs = None
        node_creation_date = None
        node_replaced_by_curie = None
        if node_meta is not None:
            node_definition = node_meta.get('definition', None)
            if node_definition is not None:
                node_description = node_definition['val']
                if node_description.startswith('OBSOLETE:') or node_description.startswith('Obsolete.'):
                    continue
            node_synonyms = node_meta.get('synonyms', None)
            if node_synonyms is not None:
                node_synonyms = [syn_dict['val'] for syn_dict in node_synonyms if syn_dict['pred'] == 'hasExactSynonym']
            node_xrefs = node_meta.get('xrefs', None)
            if node_xrefs is not None:
                node_xrefs = [xref['val'] for xref in node_xrefs]
            basic_property_values = node_meta.get('basicPropertyValues', None)
            if basic_property_values is not None:
                for basic_property_value_dict in basic_property_values:
                    bpv_pred = basic_property_value_dict['pred']
                    bpv_val = basic_property_value_dict['val']
                    if bpv_pred == 'OIO:creation_date' or bpv_pred == 'dcterms:issued':
                        node_creation_date = bpv_val
                    elif bpv_pred == 'IAL:0100001':
                        assert node_deprecated
                        node_replaced_by_uri = bpv_val
                        node_replaced_by_curie = uri_to_curie_shortener(node_replaced_by_uri)
                    elif bpv_pred == 'http://purl.bioontology.org/ontology/STY':
                        node_tui = bpv_val
                        # fix some impedance mismatch between URIs used in umls2rdf and in umls_semantictypes.owl:
                        node_tui_uri = posixpath.join(bpv_pred, node_tui)
                        node_tui_curie = uri_to_curie_shortener(node_tui_uri)
                        assert node_tui_curie is not None
#                        print('getting category for URI: ' + node_tui_uri + ' and CURIE: ' + node_tui_curie)
                        node_tui_category_label = get_biolink_category_for_node(node_tui_uri,
                                                                                node_tui_curie,
                                                                                ontology,
                                                                                curies_to_categories,
                                                                                uri_to_curie_shortener)
#                        print(node_tui_category_label)
                        if node_tui_category_label is None:
                            node_tui_category_label = 'unknown category'
                            log_message(message='unknown category: ' + node_tui_uri)
                        node_tui_category_iri = category_label_to_iri_mapper(node_tui_category_label)
                        node_category_label = node_tui_category_label  # override the node category label if we have a TUI
                    elif bpv_pred == 'http://www.w3.org/2004/02/skos/core#prefLabel':
                        node_name = bpv_val
                    elif bpv_pred == 'http://www.w3.org/2004/02/skos/core#definition':
                        node_description = bpv_val
        if node_category_label is None:
            if not node_deprecated:
                log_message("Node does not have a category", ontology.id, node_curie_id, output_stream=sys.stderr)
                node_category_label = 'unknown category'
            else:
                node_category_label = 'deprecated node'
        node_category_iri = category_label_to_iri_mapper(node_category_label)

        # if we have a label but no name, use the label as the name
        if node_name is None and node_label is not None:
            node_name = node_label

        # if we have a name but no label, use the name as the label
        if node_label is None and node_name is not None:
            node_label = node_name

        node_dict['name'] = node_name
        node_dict['full name'] = node_label
        node_dict['category'] = node_category_iri
        node_dict['category label'] = node_category_label
        node_dict['description'] = node_description
        node_dict['synonyms'] = node_synonyms             # slot name is not biolink standard
        node_dict['xrefs'] = node_xrefs                   # slot name is not biolink standard
        node_dict['creation date'] = node_creation_date   # slot name is not biolink standard
        node_dict['deprecated'] = node_deprecated         # slot name is not biolink standard
        node_dict['update date'] = node_creation_date
        node_dict['replaced by'] = node_replaced_by_curie  # slot name is not biolink standard
        node_dict['source ontology iri'] = ontology.id    # slot name is not biolink standard
        node_type = onto_node_dict.get('type', None)
        node_dict['ontology node type'] = node_type       # slot name is not biolink standard
        node_dict['ontology node id'] = ontology_node_id  # slot name is not biolink standard
        if node_curie_id in ret_dict:
            node_dict = merge_two_dicts(ret_dict[node_curie_id], node_dict)
        ret_dict[node_curie_id] = node_dict

        # check if we need to make a CUI node
        if basic_property_values is not None:
            for basic_property_value_dict in basic_property_values:
                bpv_pred = basic_property_value_dict['pred']
                bpv_val = basic_property_value_dict['val']
                if bpv_pred == 'http://purl.bioontology.org/ontologies/umls/cui':
                    assert node_tui is not None
                    cui_node_dict = dict(node_dict)
                    cui_uri = bpv_pred + '/' + bpv_val
                    cui_curie = uri_to_curie_shortener(cui_uri)
                    assert cui_curie is not None
                    cui_node_dict['id'] = cui_curie
                    cui_node_dict['iri'] = cui_uri
                    cui_node_dict['category'] = node_tui_category_iri
                    cui_node_dict['category label'] = node_tui_category_label
                    cui_node_dict['ontology node id'] = None
                    cui_node_dict_existing = ret_dict.get(cui_curie, None)
                    if cui_node_dict_existing is not None:
                        cui_node_dict = merge_two_dicts(cui_node_dict,
                                                        cui_node_dict_existing)
                    ret_dict[cui_curie] = cui_node_dict
    return ret_dict


def get_rels_dict(nodes: dict,
                  ontology: ontobio.ontol.Ontology,
                  uri_to_curie_shortener: callable,
                  map_of_node_ontology_ids_to_curie_ids: dict):
    rels_dict = dict()
    ont_graph = ontology.get_graph()

    for (object_id, subject_id, predicate_dict) in ont_graph.edges(data=True):
        if subject_id == 'owl:Thing' or object_id == 'owl:Thing':
            continue

        if subject_id.startswith('_:genid') or object_id.startswith('_:genid'):
            continue

        # subject_id and object_id are IDs from the original ontology objects; these may not
        # always be the node curie IDs (e.g., for SNOMED terms). Need to map them
        subject_curie_id = map_of_node_ontology_ids_to_curie_ids.get(subject_id, None)
        if subject_curie_id is None:
            log_message(message="ontology node ID has no curie ID in the map",
                        ontology_name=ontology.id,
                        node_curie_id=subject_id,
                        output_stream=sys.stderr)
            continue
        object_curie_id = map_of_node_ontology_ids_to_curie_ids.get(object_id, None)
        if object_curie_id is None:
            log_message(message="ontology node ID has no curie ID in the map",
                        ontology_name=ontology.id,
                        node_curie_id=object_id,
                        output_stream=sys.stderr)
            continue
        predicate_label = predicate_dict['pred']
        if not predicate_label.startswith('http:'):
            if ':' not in predicate_label:
                if predicate_label != 'subClassOf':
                    predicate_curie = 'owl:' + predicate_label
                else:
                    predicate_curie = 'rdfs:subClassOf'
                predicate_label = convert_owl_camel_case_to_biolink_spaces(predicate_label)
            else:
                predicate_curie = predicate_label
                predicate_node = nodes.get(predicate_curie, None)
                if predicate_node is not None:
                    predicate_label = predicate_node['name']
            predicate_iri = prefixcommons.expand_uri(predicate_curie)
        else:
            predicate_iri = predicate_label
            predicate_curie = uri_to_curie_shortener(predicate_iri)
        if predicate_curie is None:
            log_message(message="predicate IRI has no CURIE: " + predicate_iri,
                        ontology_name=ontology.id,
                        output_stream=sys.stderr)
            continue

        key = subject_curie_id + ';' + predicate_curie + ';' + object_curie_id + ';' + ontology.id

        if rels_dict.get(key, None) is None:
            rels_dict[key] = {'subject': subject_curie_id,
                              'object': object_curie_id,
                              'type': predicate_label,
                              'relation': predicate_iri,
                              'relation curie': predicate_curie,  # slot is not biolink standard
                              'negated': False,
                              'provided by': ontology.id}
    for node_id, node_dict in nodes.items():
        xrefs = node_dict['xrefs']
        if xrefs is not None:
            for xref_node_id in xrefs:
                if xref_node_id in nodes:
                    key = node_id + ';' + predicate_curie + ';' + xref_node_id
                    if rels_dict.get(key, None) is None:
                        rels_dict[key] = {'subject': node_id,
                                          'object': xref_node_id,
                                          'type': 'xref',
                                          'relation': 'http://purl.org/obo/owl/oboFormat#oboFormat_xref',
                                          'relation curie': 'oboFormat:xref',
                                          'negated': False,
                                          'provided by': nodes[xref_node_id]['source ontology iri'],
                                          'id': None}
    return rels_dict

# --------------- pure functions here -------------------
# (Note: a "pure" function here can still have logging print statements)


def is_ignorable_ontology_term(iri: str):
    parsed_iri = urllib.parse.urlparse(iri)
    iri_netloc = parsed_iri.netloc
    iri_path = parsed_iri.path
    return iri_netloc in ('example.com', 'usefulinc.com') or iri_path.startswith('/ontology/provisional')


def make_node_dicts_for_ontologies(ont_dict_list: list,
                                   uri_to_curie_shortener: callable,
                                   category_label_to_iri_mapper: callable):
    ret_dict = dict()
    for ont_dict in ont_dict_list:
        ontology = ont_dict['ontology']
        assert type(ontology) == ontobio.ontol.Ontology
        ontology_iri = ont_dict['id']
        ontology_curie_id = uri_to_curie_shortener(ontology_iri)
        if ontology_curie_id is None or len(ontology_curie_id) == 0:
            ontology_curie_id = ontology_iri
        ret_dict.update({ontology_curie_id: {
            'id':  ontology_curie_id,
            'iri': ontology_iri,
            'full name': ont_dict['title'],
            'name': ont_dict['title'],
            'category': category_label_to_iri_mapper('data source'),
            'category label': 'data source',
            'description': ont_dict['description'],
            'synonyms': None,
            'xrefs': None,
            'creation date': None,
            'update date': ont_dict['file last modified timestamp'],
            'deprecated': False,
            'replaced by': None,
            'source ontology iri': None,
            'ontology node type': 'INDIVIDUAL',
            'ontology node id': None}})
    return ret_dict


def make_uri_to_curie_shortener(curie_to_iri_lookaside_list: list = []):
    return lambda iri: shorten_iri_to_curie(iri, curie_to_iri_lookaside_list)


def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='build-kg2: builds the KG2 knowledge graph for the RTX system')
    arg_parser.add_argument('categoriesFile', type=str, nargs=1)
    arg_parser.add_argument('curiesToURILALFile', type=str, nargs=1)
    arg_parser.add_argument('owlLoadInventoryFile', type=str, nargs=1)
    arg_parser.add_argument('outputFile', type=str, nargs=1)
    return arg_parser


def convert_owl_camel_case_to_biolink_spaces(name: str):
    s1 = FIRST_CAP_RE.sub(r'\1 \2', name)
    converted = ALL_CAP_RE.sub(r'\1 \2', s1).lower()
    return converted.replace('sub class', 'subclass')


def convert_biolink_category_to_iri(biolink_category_base_iri, biolink_category_label: str):
    return urllib.parse.urljoin(biolink_category_base_iri, biolink_category_label.title().replace(' ', ''))


def safe_load_yaml_from_string(yaml_string: str):
    return yaml.safe_load(io.StringIO(yaml_string))


def get_prefix_from_curie_id(curie_id: str):
    assert ':' in curie_id
    return curie_id.split(':')[0]


def count_node_types_with_none_category(nodes: dict):
    return collections.Counter([curie_id.split(':')[0] for curie_id in nodes.keys() if nodes[curie_id]['category'] is None])


def get_nodes_with_none_category(nodes: dict):
    return {mykey: myvalue for mykey, myvalue in nodes.items() if myvalue['category'] is None}


def count_node_curie_prefix_types(nodes: dict):
    return collections.Counter([node['id'].split(':')[0] for node in nodes.values()])


def count_node_category_types(nodes: dict):
    return collections.Counter([node['category'] for node in nodes.values()])


def merge_two_dicts(x: dict, y: dict):
    ret_dict = copy.deepcopy(x)
    for key, value in y.items():
        stored_value = ret_dict.get(key, None)
        if stored_value is None:
            if value is not None:
                ret_dict[key] = value
        else:
            if value is not None and value != stored_value:
                if type(value) == str and type(stored_value) == str:
                    if value != stored_value:
                        if key == 'description':
                            ret_dict[key] = stored_value + '; ' + value
                        elif key == 'ontology node id' or key == 'ontology node type':
                            ret_dict[key] = [stored_value, value]
                        else:
                            log_message("warning:  for key: " + key + ", dropping second value: " + value + '; keeping first value: ' + stored_value,
                                        output_stream=sys.stderr)
                elif type(value) == list and type(stored_value) == list:
                    ret_dict[key] = list(set(value + stored_value))
                elif type(value) == dict and type(stored_value) == dict:
                    ret_dict[key] = merge_two_dicts(value, stored_value)
                elif key == 'deprecated' and type(value) == bool:
                    ret_dict[key] = True  # special case for deprecation; True always trumps False for this property
                else:
                    ret_dict[key] = [value, stored_value]
    return ret_dict


def compose_two_multinode_dicts(node1: dict, node2: dict):
    ret_dict = copy.deepcopy(node1)
    for key, value in node2.items():
        stored_value = ret_dict.get(key, None)
        if stored_value is None:
            ret_dict[key] = value
        else:
            if value is not None:
                ret_dict[key] = merge_two_dicts(node1[key], value)
    return ret_dict


def make_map_of_node_ontology_ids_to_curie_ids(nodes: dict):
    ret_dict = dict()
    for curie_id, node_dict in nodes.items():
        ontology_node_id = node_dict['ontology node id']
        assert curie_id not in ret_dict
        if ontology_node_id is not None:
            if type(ontology_node_id) == str:
                ret_dict[ontology_node_id] = curie_id
            elif type(ontology_node_id) == list:
                for id in ontology_node_id:
                    ret_dict[id] = curie_id
            else:
                assert False
    return ret_dict


# --------------- main starts here -------------------

if not USE_ONTOBIO_JSON_CACHE:
    delete_ontobio_cachier_caches()

args = make_arg_parser().parse_args()
curies_to_categories_file_name = args.categoriesFile[0]
curies_to_uri_lal_file_name = args.curiesToURILALFile[0]
owl_load_inventory_file = args.owlLoadInventoryFile[0]
output_file = args.outputFile[0]

curies_to_categories = safe_load_yaml_from_string(read_file_to_string(curies_to_categories_file_name))
curies_to_uri_lal = safe_load_yaml_from_string(read_file_to_string(curies_to_uri_lal_file_name))
map_category_label_to_iri = functools.partial(convert_biolink_category_to_iri, BIOLINK_CATEGORY_BASE_IRI)
uri_to_curie_shortener = make_uri_to_curie_shortener(curies_to_uri_lal)

ontology_urls_and_files = tuple(safe_load_yaml_from_string(read_file_to_string(owl_load_inventory_file)))

running_time = timeit.timeit(lambda: make_kg2(curies_to_categories,
                                              uri_to_curie_shortener,
                                              map_category_label_to_iri,
                                              ontology_urls_and_files,
                                              output_file), number=1)
print('running time for KG2 construction: ' + str(running_time))


# # ---------------- Notes -----------------
# # - use NCBI Entrez Gene IDs for gene identifiers
# # - use UniProt IDs for protein identifiers
