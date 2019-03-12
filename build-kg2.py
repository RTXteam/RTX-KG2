import collections
import copy
import errno
import functools
import hashlib
import io
import json
import networkx
import ontobio
import os.path
import pathlib
import pickle
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
#import ipdb # need this for interactive debugging


# -------------- define globals here ---------------

IRI_NETLOCS_IGNORE = ('example.com', 'usefulinc.com')
USE_ONTOBIO_JSON_CACHE = False
ONTOLOGY_LOAD_CONFIG_FILE = 'ontology-load-config.yaml'
BIOLINK_CATEGORY_BASE_IRI = 'http://w3id.org/biolink'
FIRST_CAP_RE = re.compile('(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile('([a-z0-9])([A-Z])')
CURIES_TO_CATEGORIES_FILE_NAME = "curies-to-categories.yaml"

# -------------- subroutines with side-effects go here ------------------

def purge(dir, pattern):
    exp_dir = os.path.expanduser(dir)
    for f in os.listdir(exp_dir):
        if re.search(pattern, f):
            os.remove(os.path.join(exp_dir, f))
            
def delete_ontobio_cachier_caches():
    purge("~/.cachier", ".ontobio*")
    purge("~/.cachier", ".prefixcommons*")


## this function is needed due to an issue with caching in Ontobio; see this GitHub issue:
##     https://github.com/biolink/ontobio/issues/301
def delete_ontobio_cache_json(file_name):
    file_name_hash = hashlib.sha256(file_name.encode()).hexdigest()
    temp_file_path = os.path.join("/tmp", file_name_hash)
    print("testing if file exists: " + temp_file_path)
    if os.path.exists(temp_file_path):
        try:
            log_message(message="Deleting ontobio JSON cache file: " + temp_file_path)
            os.remove(temp_file_path)
        except OSError as e:
            if e.errno == errno.ENOENT:
                log_message(message="Error deleting ontobio JSON cache file: " + temp_file_path)
            else:
                raise e


def head_list(x: list, n=3):
    pprint.pprint(x[0:n])


def head_dict(x: dict, n: int=3):
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
        if not USE_ONTOBIO_JSON_CACHE:
            delete_ontobio_cache_json(file_name)        
        size = os.path.getsize(file_name)
        log_message(message="Reading ontology file: " + file_name + "; size: " + "{0:.2f}".format(size/1024) + " KiB",
                    ontology_name=None)        
        ont_return = ontobio.ontol_factory.OntologyFactory().create(file_name, ignore_cache=True)
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
        assert download_url is not None
        ontology_id = download_url
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
            temp_file_name = tempfile.mkstemp(prefix='kg2')[1]
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
             map_category_label_to_iri: callable,
             ontology_urls_and_files: tuple):
    
    ontology_data = []
    for ont_source_info_dict in ontology_urls_and_files:
        local_file_name = download_file_if_not_exist_locally(ont_source_info_dict['url'],
                                                             ont_source_info_dict['file'])
        ont = make_ontology_dict_from_local_file(local_file_name,
                                                 ont_source_info_dict['url'],
                                                 ont_source_info_dict['title'])
        ontology_data.append(ont)

    master_ontology = copy.deepcopy(ontology_data[0]['ontology'])
    master_ontology.merge([ont_dict['ontology'] for ont_dict in ontology_data])
        
    nodes_dict = make_nodes_dict_from_ontology_dict(master_ontology,
                                                   curies_to_categories,
                                                   map_category_label_to_iri)

    nodes_dict.update(make_node_dicts_for_ontologies(ontology_data,
                                                     map_category_label_to_iri))
    
#    nodes_dict = functools.reduce(lambda x, y: compose_two_multinode_dicts(x, y),
#                                  ontology_node_dicts)

    map_of_node_ontology_ids_to_curie_ids = make_map_of_node_ontology_ids_to_curie_ids(nodes_dict)
    kg2_dict = dict()
    
# get a dictionary of all relationships including xrefs as relationships
    kg2_dict['edges'] = list(get_rels_dict(nodes_dict, master_ontology,
                                           map_of_node_ontology_ids_to_curie_ids).values())
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

    with open('kg2.json', 'w') as outfile:
        json.dump(kg2_dict, outfile)

    pickle.dump(kg2_dict, open('kg2.pickle', 'wb'))


# --------------- subroutines that could be made into pure functions ----------

def is_ignorable_ontology_term(iri: str):
    parsed_iri = urllib.parse.urlparse(iri)
    iri_netloc = parsed_iri.netloc
    iri_path = parsed_iri.path
    return iri_netloc in IRI_NETLOCS_IGNORE or iri_path.startswith('/ontology/provisional')


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
        elif iri.startswith('http://www.ebi.ac.uk/efo/EFO_'):
            curie_id = iri.replace('http://www.ebi.ac.uk/efo/EFO_', 'EFO:')
        elif iri.startswith('http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl'):
            curie_id = iri.replace('http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#',
                                   'NCIT:')
        else:
            curie_id = None
    return curie_id


def get_biolink_category_for_node(ontology_node_id: str,
                                  ontology: ontobio.ontol.Ontology,
                                  curies_to_categories: dict):

#    print("searching for category for node: " + ontology_node_id)
    ret_category = None

    if ontology_node_id == 'owl:Nothing':
        return None
    
    if not ontology_node_id.startswith('http:'):
        # most node objects have an ID that is a CURIE ID
        node_curie_id = ontology_node_id
    else:
        # but some nodes objects have an IRI as their ID; need to shorten to a CURIE
        node_curie_id = shorten_iri_to_curie(ontology_node_id)
        if node_curie_id is None:
            log_message(message="could not shorten this IRI to a CURIE",
                        ontology_name=ontology.id,
                        node_curie_id=ontology_node_id,
                        output_stream=sys.stderr)
            
    if node_curie_id is not None:
        curie_prefix = get_prefix_from_curie_id(node_curie_id)
        curies_to_categories_prefixes = curies_to_categories['prefix-mappings']
        ret_category = curies_to_categories_prefixes.get(curie_prefix, None)
        if ret_category is None:
            ## need to walk the ontology hierarchy until we encounter a parent term with a defined biolink category
            curies_to_categories_terms = curies_to_categories['term-mappings']
            ret_category = curies_to_categories_terms.get(node_curie_id, None)
            if ret_category is None:
                for parent_ontology_node_id in ontology.parents(ontology_node_id, ['subClassOf']):
                    try:
                        ret_category = get_biolink_category_for_node(parent_ontology_node_id, ontology, curies_to_categories)
                    except RecursionError as re:
                        log_message(message="recursion error: " + ontology_node_id,
                                    ontology_name=ontology.id,
                                    node_curie_id=node_curie_id,
                                    output_stream=sys.stderr)
                        raise RecursionError()
                    if ret_category is not None:
                        break
        if ret_category is None:  # this is to handle SNOMED CT attributes
            if node_curie_id.startswith('SNOMEDCT_US'):
                ontology_node_lbl = ontology.node(ontology_node_id).get('lbl', None)
                if ontology_node_lbl is not None:
                    if '(attribute)' in ontology_node_lbl:
                        ret_category = 'attribute'
                    else:
                        log_message('Node does not have a label or any parents', 'http://snomed.info/sct/900000000000207008', node_curie_id, output_stream=sys.stderr)
                        
    return ret_category


def make_node_dicts_for_ontologies(ont_dict_list: list,
                                   category_label_to_iri_mapper: callable):
    ret_dict = dict()
    for ont_dict in ont_dict_list:
        ontology = ont_dict['ontology']
        assert type(ontology) == ontobio.ontol.Ontology
        ontology_iri = ont_dict['id']
        if not ontology_iri.startswith('http:'):
            log_message(message="unexpected IRI format: " + ontology_iri,
                        ontology_name=ontology_iri,
                        output_stream=sys.stderr)
            assert ontology_iri.startswith('http:')
        ontology_curie_id = shorten_iri_to_curie(ontology_iri)    
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


def make_nodes_dict_from_ontology_dict(ontology: ontobio.ontol.Ontology,
                                      curies_to_categories: dict,
                                      category_label_to_iri_mapper: callable):
    ret_dict = dict()

    for ontology_node_id in ontology.nodes():
        onto_node_dict = ontology.node(ontology_node_id)
        assert onto_node_dict is not None
        if not ontology_node_id.startswith('http://snomed.info'):
            node_curie_id = ontology_node_id
            iri = onto_node_dict.get('id', None)
            if iri is None:
                iri = prefixcommons.expand_uri(node_curie_id)
                if iri == node_curie_id or iri == '':
                    continue
            assert iri is not None
            if is_ignorable_ontology_term(iri):
                continue
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
        node_category_label = get_biolink_category_for_node(ontology_node_id, ontology, curies_to_categories)
        if node_category_label is not None:
            node_category_iri = category_label_to_iri_mapper(node_category_label)
        else:
            log_message("Node does not have a category", ontology.id, node_curie_id, output_stream=sys.stderr)
            continue
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


def get_rels_dict(nodes: dict,
                  ontology: ontobio.ontol.Ontology,
                  map_of_node_ontology_ids_to_curie_ids: dict):
    rels_dict = dict()
    ont_graph = ontology.get_graph()
    for (subject_id, object_id, predicate_dict) in ont_graph.edges(data=True):
        # subject_id and object_id are IDs from the original ontology objects; these may not
        # always be the node curie IDs (e.g., for SNOMED terms). Need to map them
        subject_curie_id = map_of_node_ontology_ids_to_curie_ids.get(subject_id, None)
        if subject_curie_id is None:
            log_message(message="ontology node ID has no curie ID in the map: " + subject_id,
                        ontology_name=ontology.id,
                        node_curie_id=subject_id,
                        output_stream=sys.stderr)
            continue
        object_curie_id = map_of_node_ontology_ids_to_curie_ids.get(object_id, None)
        if object_curie_id is None:
            log_message(message="ontology node ID has no curie ID in the map: " + object_id,
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
            predicate_curie = shorten_iri_to_curie(predicate_iri)
        if predicate_curie is None:
            log_message(message="predicate IRI has no CURIE: " + predicate_iri,
                        ontology_name=ontology.id,
                        output_stream=sys.stderr)
            continue
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

# --------------- pure functions here -------------------
# (Note: a "pure" function here can still have logging print statements)

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
                        log_message("warning: incompatible data in two dictionaries: " + str(value) + "; " + str(stored_value) + "; key is: " + key, file=sys.stderr)
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
            ret_dict[ontology_node_id] = curie_id
    return ret_dict

# --------------- main starts here -------------------

if not USE_ONTOBIO_JSON_CACHE:
    delete_ontobio_cachier_caches()

curies_to_categories = safe_load_yaml_from_string(read_file_to_string(CURIES_TO_CATEGORIES_FILE_NAME))

map_category_label_to_iri = functools.partial(convert_biolink_category_to_iri, BIOLINK_CATEGORY_BASE_IRI)

ontology_urls_and_files = tuple(safe_load_yaml_from_string(read_file_to_string(ONTOLOGY_LOAD_CONFIG_FILE)))

make_kg2(curies_to_categories,
         map_category_label_to_iri,
         ontology_urls_and_files) 


# # ---------------- Notes -----------------
# # - use NCBI Entrez Gene IDs for gene identifiers
# # - use UniProt IDs for protein identifiers
