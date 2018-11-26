import collections
import copy
import functools
import json
import ontobio
import os.path
import pathlib
import pprint
import prefixcommons
import re
import shutil
import ssl
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import yaml

# -------------- impure functions here ------------------


def head_list(x: list, n=3):
    pprint.pprint(x[0:n])


def head_dict(x: dict, n: int=3):
    pprint.pprint(dict(list(x.items())[0:(n-1)]))


def make_ontology_from_local_file(file_name: str):
    print("Creating ontology from file: " + file_name)
    return ontobio.ontol_factory.OntologyFactory().create(file_name)


def make_ontology_dict_from_local_file(file_name: str, ontology_title: str = None):
    ontology = make_ontology_from_local_file(file_name)
    file_last_modified_timestamp = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.gmtime(os.path.getmtime(file_name)))
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
    ont_dict = {'ontology': ontology,
                'id': ontology.id,
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
            temp_file_name = tempfile.mkdtemp(prefix='kg2')
            with urllib.request.urlopen(url, context=ctx) as u, open(temp_file_name, 'wb') as f:
                f.write(u.read())
            shutil.move(temp_file_name, local_file_name)
    return local_file_name


def read_file_to_string(local_file_name: str):
    with open(local_file_name, 'r') as myfile:
        file_contents_string = myfile.read()
    myfile.close()
    return file_contents_string


# --------------- pure functions here -------------------
# (Note: a "pure" function here can still have debugging print statements)

def get_biolink_map_of_curies_to_categories(biolink_yaml_data: dict):
    map_curie_to_biolink_category = dict()
    for category_name, reldata in biolink_yaml_data['classes'].items():
        mappings = reldata.get('mappings', None)
        if mappings is not None:
            assert type(mappings) == list
            for curie_id in mappings:
                map_curie_to_biolink_category[curie_id] = category_name
    return map_curie_to_biolink_category


def shorten_iri_to_curie(iri: str):
    curie_list = prefixcommons.contract_uri(iri)
    assert len(curie_list) in [0, 1]
    if len(curie_list) == 1:
        curie_id = curie_list[0]
    else:
        if iri.startswith('http://snomed.info/id'):
            curie_id = iri.replace('http://snomed.info/id/', 'SNOMEDCT_US:')
        elif iri.startswith('http://snomed.info/sct'):
            curie_id = iri.replace('http://snomed.info/sct/', 'SNOMEDCT_US:')
        elif iri.startswith('http://identifiers.org/hgnc/'):
            curie_id = iri.replace('http://identifiers.org/hgnc/', 'HGNC:')
        else:
            print("warning: iri does not map to a curie ID via prefixcommons: " + iri, file=sys.stderr)
            curie_id = None
    return curie_id


def get_biolink_category_for_node(ontology_node_id: str, ontology, map_curie_to_biolink_category: dict):
    if not ontology_node_id.startswith('http:'):
        node_curie_id = ontology_node_id
    else:
        node_curie_id = shorten_iri_to_curie(ontology_node_id)
    ret_category = None
    if node_curie_id is None:
        node_curie_id = ontology_node_id
    if node_curie_id.startswith('HGNC:'):
        ret_category = 'gene'
    elif node_curie_id.startswith('UniProtKB:'):
        ret_category = 'protein'
    else:
        map_category = map_curie_to_biolink_category.get(node_curie_id, None)
        if map_category is not None:
            ret_category = map_category
        else:
            for parent_ontology_node_id in ontology.parents(ontology_node_id, ['subClassOf']):
                parent_category = get_biolink_category_for_node(parent_ontology_node_id, ontology, map_curie_to_biolink_category)
                if parent_category is not None:
                    ret_category = parent_category
                    break
    return ret_category


def get_nodes_dict_from_ontology_dict(ont_dict: dict,
                                      map_curie_to_biolink_category: dict,
                                      category_label_to_iri_mapper: callable):
    ontology = ont_dict['ontology']
    assert type(ontology) == ontobio.ontol.Ontology
    ontology_iri = ont_dict['id']
    assert ontology_iri.startswith('http:')
    ontology_curie_id = shorten_iri_to_curie(ontology_iri)

    ret_dict = {ontology_curie_id: {
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
        'ontology node id': None}}

    for ontology_node_id in ontology.nodes():
        onto_node_dict = ontology.node(ontology_node_id)
        if not onto_node_dict:
            continue
        if not ontology_node_id.startswith('http://snomed.info'):
            node_curie_id = ontology_node_id
            iri = onto_node_dict.get('id', None)
            assert iri is not None
            parsed_iri = urllib.parse.urlparse(iri)
            iri_netloc = parsed_iri.netloc
            iri_path = parsed_iri.path
            if iri_netloc in ('example.com', 'usefulinc.com') or iri_path.startswith('/ontology/provisional'):
                continue
            if iri is None:
                iri = prefixcommons.expand_uri(node_curie_id)
        else:
            # have to handle snomed ontology specially since the node IDs are not CURIE IDs.
            # When we import the SNOMED CT ontology from OWL format into ontobio, the node IDs
            # are of the form: http://snomed.info/id/12237791000119102.
            node_curie_id = ontology_node_id.replace('http://snomed.info/id/', 'SNOMED:')
            iri = prefixcommons.expand_uri(node_curie_id)
            node_curie_id = node_curie_id.replace('SNOMED:', 'SNOMEDCT_US:')
        node_dict = dict()
        node_dict['id'] = node_curie_id
        node_dict['iri'] = iri
        node_label = onto_node_dict.get('label', None)
        node_dict['full name'] = node_label
        node_name = onto_node_dict.get('lbl', None)
        if node_name is None:
            node_name = node_dict['full name']
        node_dict['name'] = node_name
        node_meta = onto_node_dict.get('meta', None)
        node_category_label = get_biolink_category_for_node(ontology_node_id, ontology, map_curie_to_biolink_category)
        if node_category_label is not None:
            node_category_iri = category_label_to_iri_mapper(node_category_label)
        else:
            node_category_iri = None
        node_dict['category'] = node_category_iri
        node_dict['category label'] = node_category_label
        node_deprecated = False
        node_description = None
        node_synonyms = None
        node_xrefs = None
        node_creation_date = None
        node_replaced_by = None
        if node_meta is not None:
            node_deprecated = node_meta.get('deprecated', False)
            node_definition = node_meta.get('definition', None)
            if node_definition is not None:
                node_description = node_definition['val']
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
                    if bpv_pred == 'OIO:creation_date':
                        node_creation_date = bpv_val
                    elif bpv_pred == 'IAL:0100001':
                        assert node_deprecated
                        node_replaced_by = bpv_val
        node_dict['description'] = node_description
        node_dict['synonyms'] = node_synonyms             # slot name is not biolink standard
        node_dict['xrefs'] = node_xrefs                   # slot name is not biolink standard
        node_dict['creation date'] = node_creation_date   # slot name is not biolink standard
        node_dict['deprecated'] = node_deprecated         # slot name is not biolink standard
        node_dict['update date'] = node_creation_date
        node_dict['replaced by'] = node_replaced_by       # slot name is not biolink standard
        node_dict['source ontology iri'] = ontology.id    # slot name is not biolink standard
        node_type = onto_node_dict.get('type', None)
        node_dict['ontology node type'] = node_type       # slot name is not biolink standard
        node_dict['ontology node id'] = ontology_node_id  # slot name is not biolink standard
        ret_dict[node_curie_id] = node_dict
    return ret_dict


def get_map_of_node_ontology_ids_to_curie_ids(nodes: dict):
    ret_dict = dict()
    for curie_id, node_dict in nodes.items():
        ontology_node_id = node_dict['ontology node id']
        assert curie_id not in ret_dict
        if ontology_node_id is not None:
            ret_dict[ontology_node_id] = curie_id
    return ret_dict


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
                    svr = stored_value.replace('_', ' ')
                    vr = value.replace('_', ' ')
                    if vr == svr:
                        ret_dict[key] = svr
                elif type(value) == list and type(stored_value) == list:
                    ret_dict[key] = list(set(value + stored_value))
                elif key == 'deprecated' and type(value) == bool:
                    ret_dict[key] = True  # special case for deprecation; True always trumps False for this property
                else:
                    ret_dict[key] = [value, stored_value]
                    if key not in ('source ontology iri', 'category label', 'category'):
                        print("warning: incompatible data in two dictionaries: " + str(value) + "; " + str(stored_value) + "; key is: " + key, file=sys.stderr)
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


def convert_biolink_category_to_iri(biolink_category_base_iri, biolink_category_label: str):
    return urllib.parse.urljoin(biolink_category_base_iri, biolink_category_label.title().replace(' ', ''))


def make_map_category_label_to_iri(biolink_category_base_iri: str):
    return functools.partial(convert_biolink_category_to_iri, biolink_category_base_iri)
#     return lambda category_label: convert_biolink_category_to_iri(biolink_category_base_iri, category_label)


def convert_owl_camel_case_to_biolink_spaces(name: str):
    s1 = FIRST_CAP_RE.sub(r'\1 \2', name)
    converted = ALL_CAP_RE.sub(r'\1 \2', s1).lower()
    return converted.replace('sub class', 'subclass')


def get_rels_dict(nodes: dict, ontology: ontobio.ontol.Ontology,
                  map_of_node_ontology_ids_to_curie_ids: dict):
    rels_dict = dict()
    for (subject_id, object_id, predicate_dict) in ontology.get_graph().edges_iter(data=True):
        # subject_id and object_id are IDs from the original ontology objects; these may not
        # always be the node curie IDs (e.g., for SNOMED terms). Need to map them
        subject_curie_id = map_of_node_ontology_ids_to_curie_ids.get(subject_id, None)
        if subject_curie_id is None:
            print("ontology ID has no curie ID in the map: " + subject_id, file=sys.stderr)
            continue
        object_curie_id = map_of_node_ontology_ids_to_curie_ids.get(object_id, None)
        if object_curie_id is None:
            print("ontology ID has no curie ID in the map: " + object_id, file=sys.stderr)
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
            predicate_curie = shorten_iri_to_curie(predicate_iri)
        key = subject_curie_id + ';' + predicate_curie + ';' + object_curie_id
        if rels_dict.get(key, None) is None:
            rels_dict[key] = {'subject': subject_curie_id,
                              'object': object_curie_id,
                              'type': predicate_label,
                              'relation': predicate_iri,
                              'relation curie': predicate_curie,  # slot is not biolink standard
                              'negated': False,
                              'provided by': ontology.id,
                              'id': None}
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


# --------------- define constants -------------------

# note: this could be loaded from a config file
ONTOLOGY_URLS_AND_FILES = ({'url':  'http://purl.obolibrary.org/obo/bfo.owl',
                            'file': 'bfo.owl',
                            'title': 'Basic Formal Ontology'},
                           {'url':  'http://purl.obolibrary.org/obo/ro.owl',
                            'file': 'ro.owl',
                            'title': 'Relation Ontology'},
                           {'url':  'http://purl.obolibrary.org/obo/hp.owl',
                            'file': 'hp.owl',
                            'title': 'Human Phenotype Ontology'},
                           {'url':  'http://purl.obolibrary.org/obo/go/extensions/go-plus.owl',
                            'file': 'go-plus.owl',
                            'title': 'Gene Ontology'},
                           {'url':  'http://purl.obolibrary.org/obo/chebi.owl',
                            'file': 'chebi.owl',
                            'title': 'Chemical Entities of Biological Interest'},
                           {'url':  'http://purl.obolibrary.org/obo/ncbitaxon/subsets/taxslim.owl',
                            'file': 'taxslim.owl',
                            'title': 'NCBITaxon'},
                           {'url':  'http://purl.obolibrary.org/obo/fma.owl',
                            'file': 'fma.owl',
                            'title': 'Foundational Model of Anatomy'},
                           {'url':  'http://purl.obolibrary.org/obo/pato.owl',
                            'file': 'pato.owl',
                            'title': 'Phenotypic Quality Ontology'},
                           {'url':  'http://purl.obolibrary.org/obo/mondo.owl',
                            'file': 'mondo.owl',
                            'title': 'MONDO Disease Ontology'},
                           {'url':  'http://purl.obolibrary.org/obo/cl.owl',
                            'file': 'cl.owl',
                            'title': 'Cell Ontology'},
                           {'url':  'http://purl.obolibrary.org/obo/doid.owl',
                            'file': 'doid.owl',
                            'title': 'Disease Ontology'},
                           {'url':  'http://purl.obolibrary.org/obo/pr.owl',
                            'file': 'pr.owl',
                            'title': 'Protein Ontology'},
                           {'url':  'http://purl.obolibrary.org/obo/uberon/ext.owl',
                            'file': 'uberon-ext.owl',
                            'title': 'Uber-anatomy Ontology'},
                           {'url':  'http://purl.obolibrary.org/obo/ncit.owl',
                            'file': 'ncit.owl',
                            'title': 'NCI Thesaurus'},
                           {'url':  None,
                            'file': 'snomed.owl',
                            'title': 'SNOMED CT Ontology'}, )

BIOLINK_MODEL_YAML_URL = 'file:biolink-model--updated-for-kg2.yaml'

# ------------- save --------------
# BIOLINK_MODEL_YAML_URL = 'https://raw.githubusercontent.com/biolink/biolink-model/master/biolink-model.yaml'
# ------------- save --------------

BIOLINK_CATEGORY_BASE_IRI = 'http://w3id.org/biolink'

FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')

ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')


# --------------- main starts here -------------------

# download all the ontology OWL files and load them; fold in the original data from ONTOLOGY_URLS_AND_FILES
ontology_data = tuple(make_ontology_dict_from_local_file(download_file_if_not_exist_locally(ont_dict['url'],
                                                                                            ont_dict['file']),
                                                         ont_dict['title'])
                      for ont_dict in ONTOLOGY_URLS_AND_FILES)


biolink_data = yaml.safe_load(urllib.request.urlopen(BIOLINK_MODEL_YAML_URL))
biolink_map_of_curies_to_categories = get_biolink_map_of_curies_to_categories(biolink_data)

map_category_label_to_iri = make_map_category_label_to_iri(BIOLINK_CATEGORY_BASE_IRI)

ontology_node_dicts = [get_nodes_dict_from_ontology_dict(ont_dict,
                                                         biolink_map_of_curies_to_categories,
                                                         map_category_label_to_iri)
                       for ont_dict in ontology_data]


kg2_dict = dict()

kg2_dict['nodes'] = functools.reduce(lambda x, y: compose_two_multinode_dicts(x, y),
                                     ontology_node_dicts)

map_of_node_ontology_ids_to_curie_ids = get_map_of_node_ontology_ids_to_curie_ids(kg2_dict['nodes'])

master_ontology = copy.deepcopy(ontology_data[0]['ontology'])
master_ontology.merge([ont_dict['ontology'] for ont_dict in ontology_data])

# get a dictionary of all relationships including xrefs as relationships
kg2_dict['rels'] = get_rels_dict(kg2_dict['nodes'], master_ontology,
                                 map_of_node_ontology_ids_to_curie_ids)

# delete xrefs from all_nodes_dict
for node_dict in kg2_dict['nodes'].values():
    del node_dict['xrefs']

with open('kg2.json', 'w') as outfile:
    json.dump(kg2_dict, outfile)


# # ----------- CODE GRAVEYARD ----------
# # command to convert an OWL file to an OBO file:
# #   owltools nbo.owl -o -f obo nbo.obo

# # don't use the SPARQL query method (i.e., like OntologyFactory.create("hp")) because you don't get all
# # the fields that you want for each ontology term

# # ontology_codes = ["obo:bfo", "obo:ro", "obo:hp", "obo:go", "obo:chebi", "obo:go",
# #                   "http://purl.obolibrary.org/obo/ncbitaxon/subsets/taxslim.owl",
# #                   "obo:fma", "obo:pato", "obo:mondo", "obo:cl", "obo:doid", "obo:pr",
# #                   "http://purl.obolibrary.org/obo/uberon/ext.owl",
# #                   "obo:dron"]

# def make_ontology_from_ontcode_remote_query_with_caching(ontcode: str):
#     print("Creating ontology object: " + ontcode)
#     return ontobio.ontol_factory.OntologyFactory().create(ontcode)



# # ---------------- Notes -----------------
# # - use NCBI Entrez Gene IDs for gene identifiers
# # - use UniProt IDs for protein identifiers
