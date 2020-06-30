#!/usr/bin/env python3
'''Utility functions used by various python scripts KG2 build system

   Usage:  import kg2_util
   (then call a function like kg2_util.log_message(), etc.)
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import collections
import copy
import enum
import gzip
import html.parser
import io
import json
import math
import ontobio
import os
import pathlib
import pprint
import prefixcommons
import re
import shutil
import ssl
import sys
import tempfile
import time
import typing
import urllib.parse
import urllib.request
import validators
import yaml
from typing import Dict, Optional

TEMP_FILE_PREFIX = 'kg2'
FIRST_CAP_RE = re.compile(r'(.)([A-Z][a-z]+)')
ALL_CAP_RE = re.compile(r'([a-z0-9])([A-Z])')
NCBI_TAXON_ID_HUMAN = 9606

CURIE_PREFIX_BIOLINK = 'biolink'
CURIE_PREFIX_CHEBI = 'CHEBI'
CURIE_PREFIX_CHEMBL_COMPOUND = 'CHEMBL.COMPOUND'
CURIE_PREFIX_CHEMBL_MECHANISM = 'CHEMBL.MECHANISM'
CURIE_PREFIX_CHEMBL_TARGET = 'CHEMBL.TARGET'
CURIE_PREFIX_CLINICALTRIALS = 'clinicaltrials'
CURIE_PREFIX_CUI = 'umls'
CURIE_PREFIX_DGIDB = 'DGIdb'
CURIE_PREFIX_DRUGBANK = 'DRUGBANK'
CURIE_PREFIX_ENSEMBL = 'ENSEMBL'
CURIE_PREFIX_GTPI = 'GTPI'
CURIE_PREFIX_GTPI_SOURCE = 'GTPI_source'
CURIE_PREFIX_HGNC = 'HGNC'
CURIE_PREFIX_IDENTIFIERS_ORG_REGISTRY = 'identifiers_org_registry'
CURIE_PREFIX_ISBN = 'ISBN'
CURIE_PREFIX_KEGG = 'KEGG'
CURIE_PREFIX_KEGG_SOURCE = 'KEGG_source'
CURIE_PREFIX_MESH = 'MESH'
CURIE_PREFIX_NCBI_GENE = 'NCBIGene'
CURIE_PREFIX_NCBI_TAXON = 'NCBITaxon'
CURIE_PREFIX_OBO_FORMAT = 'oboFormat'
CURIE_PREFIX_OWL = 'owl'
CURIE_PREFIX_PMID = 'PMID'
CURIE_PREFIX_REPODB = 'REPODB'
CURIE_PREFIX_RTX_KG1 = 'RTXKG1'
CURIE_PREFIX_SEMMEDDB = 'SEMMEDDB'
CURIE_PREFIX_SMPDB = 'smpdb'
CURIE_PREFIX_TTD_DRUG = 'ttd.drug'
CURIE_PREFIX_TTD_TARGET = 'ttd.target'
CURIE_PREFIX_UMLS_TUI = 'UMLSSC'
CURIE_PREFIX_UNICHEM_SOURCE = 'UNICHEM_source'
CURIE_PREFIX_UNIPROT = 'UniProtKB'

BASE_URL_BIOLINK_CONCEPTS = 'https://w3id.org/biolink/vocab/'
BASE_URL_BIOLINK_ONTOLOGY = 'https://w3id.org/biolink/'
BASE_URL_BIOLINK_META = 'https://w3id.org/biolink/biolinkml/meta/'
BASE_URL_CHEMBL_MECHANISM = 'https://www.ebi.ac.uk/chembl#'
BASE_URL_DGIDB = 'http://www.dgidb.org/'
BASE_URL_GTPI = 'https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId='
BASE_URL_GTPI_SOURCE = 'https://www.guidetopharmacology.org/'
BASE_URL_IDENTIFIERS_ORG = 'https://identifiers.org/'
BASE_URL_IDENTIFIERS_ORG_REGISTRY = 'https://registry.identifiers.org/registry/'
BASE_URL_KEGG = '"https://www.genome.jp/dbget-bin/www_bget?'
BASE_URL_OBO_FORMAT = 'http://purl.org/obo/owl/oboFormat#oboFormat_'
BASE_URL_OWL = 'http://www.w3.org/2002/07/owl#'
BASE_URL_REPODB = 'http://apps.chiragjpgroup.org/repoDB'
BASE_URL_RTX_KG1 = 'http://arax.rtx.ai'
BASE_URL_SEMMEDDB = 'https://skr3.nlm.nih.gov/SemMedDB'

BIOLINK_CATEGORY_CHEMICAL_SUBSTANCE = 'chemical substance'
BIOLINK_CATEGORY_DATA_FILE = 'data file'
BIOLINK_CATEGORY_DRUG = 'drug'
BIOLINK_CATEGORY_GENE = 'gene'
BIOLINK_CATEGORY_PROTEIN = 'protein'

CURIE_ID_OWL_SAME_AS = CURIE_PREFIX_OWL + ':' + 'sameAs'
CURIE_ID_OWL_NOTHING = CURIE_PREFIX_OWL + ':' + 'Nothing'
CURIE_ID_OWL_THING = CURIE_PREFIX_OWL + ':' + 'Thing'
CURIE_ID_OBO_FORMAT_XREF = CURIE_PREFIX_OBO_FORMAT + ':' + 'xref'

IRI_OBO_FORMAT_XREF = BASE_URL_OBO_FORMAT + 'xref'
IRI_OWL_SAME_AS = BASE_URL_OWL + 'sameAs'

OBO_REL_CURIE_RE = re.compile(r'OBO:([^#]+)#([^#]+)')
OBO_ONT_CURIE_RE = re.compile(r'OBO:([^\.]+)\.owl')

BIOLINK_MODEL_OWL = 'biolink-model.owl'


class MLStripper(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_html(input_string: str) -> str:
    html_stripper = MLStripper()
    html_stripper.feed(input_string.replace('</p><p>', '</p><p> '))
    return html_stripper.get_data()


def load_json(input_file_name: str):
    return json.load(open(input_file_name, 'r'))


def save_json(data, output_file_name: str, test_mode: bool = False):
    if not test_mode:
        indent_num = None
        sort_keys = False
    else:
        indent_num = 4
        sort_keys = True
    temp_output_file_name = tempfile.mkstemp(prefix='kg2-')[1]
    if not output_file_name.endswith('.gz'):
        temp_output_file = open(temp_output_file_name, 'w')
        json.dump(data, temp_output_file, indent=indent_num, sort_keys=sort_keys)
    else:
        temp_output_file = gzip.GzipFile(temp_output_file_name, 'w')
        temp_output_file.write(json.dumps(data, indent=indent_num, sort_keys=sort_keys).encode('utf-8'))
    shutil.move(temp_output_file_name, output_file_name)


def get_file_last_modified_timestamp(file_name: str):
    return time.gmtime(os.path.getmtime(file_name))


def read_file_to_string(local_file_name: str):
    with open(local_file_name, 'r') as myfile:
        file_contents_string = myfile.read()
    myfile.close()
    return file_contents_string


def head_list(x: list, n: int = 3):
    pprint.pprint(x[0:n])


def head_dict(x: dict, n: int = 3):
    pprint.pprint(dict(list(x.items())[0:(n-1)]))


def purge(dir, pattern):
    exp_dir = os.path.expanduser(dir)
    for f in os.listdir(exp_dir):
        if re.search(pattern, f):
            os.remove(os.path.join(exp_dir, f))


def allcaps_to_only_first_letter_capitalized(allcaps: str):
    return allcaps[0] + allcaps[1:].lower()


def safe_load_yaml_from_string(yaml_string: str):
    return yaml.safe_load(io.StringIO(yaml_string))


def shorten_iri_to_curie(iri: str, curie_to_iri_map: list) -> str:
    curie_list = prefixcommons.contract_uri(iri,
                                            curie_to_iri_map)
    if len(curie_list) == 0:
        return None

    if len(curie_list) == 1:
        curie_id = curie_list[0]
    else:
        assert False, "somehow got a list after calling prefixcommons.contract on URI: " + iri + "; list is: " + str(curie_list)
        curie_id = None

    # if curie_id is not None:
    #     # deal with IRIs like 'https://identifiers.org/umls/ATC/L01AX02' which get converted to CURIE 'UMLS:ATC/L01AX02'
    #     umls_match = REGEX_UMLS_CURIE.match(curie_id)
    #     if umls_match is not None:
    #         curie_id = umls_match[1] + ':' + umls_match[2]

    return curie_id


def make_uri_to_curie_shortener(curie_to_iri_map=None) -> callable:
    if curie_to_iri_map is None:
        curie_to_iri_map = []
    return lambda iri: shorten_iri_to_curie(iri, curie_to_iri_map)


def expand_curie_to_iri(curie_id: str, curie_to_iri_map: list) -> Optional[str]:
    if curie_id.startswith('UMLS:CN'):
        curie_id = curie_id.replace('UMLS:CN', 'medgen:CN')  # see GitHub issue 810
    iri = prefixcommons.expand_uri(curie_id, curie_to_iri_map)
    if iri == curie_id:
        iri = None
    return iri


def make_curie_to_uri_expander(curie_to_iri_map: list = None) -> callable:
    if curie_to_iri_map is None:
        curie_to_iri_map = []
    return lambda curie_id: expand_curie_to_iri(curie_id, curie_to_iri_map)


class IDMapperType(enum.Enum):
    EXPAND = 1
    CONTRACT = 2


def make_curies_to_uri_map(curies_to_uri_map_yaml_string: str, mapper_type: IDMapperType) -> dict:
    yaml_data_structure_dict = safe_load_yaml_from_string(curies_to_uri_map_yaml_string)
    if mapper_type == IDMapperType.CONTRACT:
        return typing.cast(list, typing.cast(list, typing.cast(list, yaml_data_structure_dict['use_for_bidirectional_mapping']) +
                                             yaml_data_structure_dict['use_for_contraction_only']))
    elif mapper_type == IDMapperType.EXPAND:
        return typing.cast(list, typing.cast(list, yaml_data_structure_dict['use_for_bidirectional_mapping']) +
                           typing.cast(list, yaml_data_structure_dict['use_for_expansion_only']))
    else:
        raise ValueError("Invalid mapper type: " + str(mapper_type))


def get_depths_of_ontology_terms(ontology: ontobio.ontol.Ontology,
                                 top_node_id: str):
    queue = collections.deque([top_node_id])
    distances = dict()
    distances[top_node_id] = 0
    while len(queue) > 0:
        node_id = queue.popleft()
        node_dist = distances.get(node_id, math.inf)
        assert not math.isinf(node_dist)
        for child_node_id in ontology.children(node_id, ['subClassOf']):
            if math.isinf(distances.get(child_node_id, math.inf)):
                distances[child_node_id] = node_dist + 1
                queue.append(child_node_id)
    return distances


def get_biolink_categories_ontology_depths(biolink_ontology: ontobio.ontol.Ontology):
    url_depths = get_depths_of_ontology_terms(biolink_ontology,
                                              BASE_URL_BIOLINK_META + 'NamedThing')
    ret_depths = {key.replace(BASE_URL_BIOLINK_META, ''): value for key, value in url_depths.items()}
    ret_depths['UnknownCategory'] = -1
    return ret_depths


def make_uri_curie_mappers(curies_to_uri_file_name: str) -> Dict[str, callable]:
    yaml_string = read_file_to_string(curies_to_uri_file_name)
    expand_map = make_curies_to_uri_map(yaml_string, IDMapperType.EXPAND)
    contract_map = make_curies_to_uri_map(yaml_string, IDMapperType.CONTRACT)
    expander = make_curie_to_uri_expander(expand_map)
    contracter = make_uri_to_curie_shortener(contract_map)
    return {'expand': expander, 'contract': contracter}


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


def merge_two_dicts(x: dict, y: dict, biolink_depth_getter: callable = None):
    ret_dict = copy.deepcopy(x)
    for key, value in y.items():
        stored_value = ret_dict.get(key, None)
        if stored_value is None:
            if value is not None:
                ret_dict[key] = value
        else:
            if value is not None and value != stored_value:
                if type(value) == str and type(stored_value) == str:
                    if value.lower() != stored_value.lower():
                        if key == 'description' or key == 'update date':
                            if len(value) > len(stored_value):  # use the longer of the two descriptions or update date fields
                                ret_dict[key] = value
                        elif key == 'ontology node type':
                            log_message("warning:  for key: " + key + ", dropping second value: " + value + '; keeping first value: ' + stored_value,
                                        output_stream=sys.stderr)
                            ret_dict[key] = stored_value
                        elif key == 'provided by':
                            if value.endswith('/STY'):
                                ret_dict[key] = value
                        elif key == 'category label':
                            depth_x = biolink_depth_getter(convert_snake_case_to_camel_case(stored_value, uppercase_first_letter=True))
                            depth_y = biolink_depth_getter(convert_snake_case_to_camel_case(value, uppercase_first_letter=True))
                            if depth_y is not None:
                                if depth_x is not None:
                                    if depth_y > depth_x:
                                        ret_dict[key] = value
                                else:
                                    ret_dict[key] = value
                        elif key == 'category':
                            value_category = urllib.parse.urlparse(value).path.rsplit('/', 1)[-1]
                            stored_value_category = urllib.parse.urlparse(stored_value).path.rsplit('/', 1)[-1]
                            depth_x = biolink_depth_getter(stored_value_category)
                            depth_y = biolink_depth_getter(value_category)
                            if depth_y is not None:
                                if depth_x is not None:
                                    if depth_y > depth_x:
                                        ret_dict[key] = value
                                else:
                                    ret_dict[key] = value
                        elif key == 'name' or key == 'full name':
                            if value.replace(' ', '_') != stored_value.replace(' ', '_'):
                                stored_desc = ret_dict.get('description', None)
                                new_desc = y.get('description', None)
                                if stored_desc is not None and new_desc is not None:
                                    if len(new_desc) > len(stored_desc):
                                        ret_dict[key] = value
                        else:
                            log_message("warning:  for key: " + key + ", dropping second value: " + value + '; keeping first value: ' + stored_value,
                                        output_stream=sys.stderr)
                elif type(value) == list and type(stored_value) == list:
                    ret_dict[key] = list(set(value + stored_value))
                elif type(value) == list and type(stored_value) == str:
                    ret_dict[key] = list(set(value + [stored_value]))
                elif type(value) == str and type(stored_value) == list:
                    ret_dict[key] = list(set([value] + stored_value))
                elif type(value) == dict and type(stored_value) == dict:
                    ret_dict[key] = merge_two_dicts(value, stored_value, biolink_depth_getter)
                elif key == 'deprecated' and type(value) == bool:
                    ret_dict[key] = True  # special case for deprecation; True always trumps False for this property
                else:
                    assert False
    return ret_dict


def format_timestamp(timestamp: time.struct_time):
    return time.strftime('%Y-%m-%d %H:%M:%S %Z', timestamp)


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


def convert_snake_case_to_camel_case(name: str,
                                     uppercase_first_letter: bool = False):
    name = name.title().replace('_', '')
    if not uppercase_first_letter:
        if len(name) > 0:
            name = name[0].lower() + name[1:]
    return name


def convert_space_case_to_camel_case(name: str):
    return name.title().replace(' ', '')


def convert_camel_case_to_snake_case(name: str):
    s1 = FIRST_CAP_RE.sub(r'\1_\2', name)
    converted = ALL_CAP_RE.sub(r'\1_\2', s1).lower()
    converted = converted.replace('sub_class', 'subclass')
    if converted[0].istitle():
        converted[0] = converted[0].lower()
    return converted.replace(' ', '_')


def convert_biolink_category_to_iri(biolink_category_label: str,
                                    biolink_category_base_iri: str = BASE_URL_BIOLINK_CONCEPTS):
    return urllib.parse.urljoin(biolink_category_base_iri,
                                convert_space_case_to_camel_case(biolink_category_label))


def make_node(id: str,
              iri: str,
              name: str,
              category_label: str,
              update_date: str,
              provided_by: str):
    return {'id': id,
            'iri': iri,
            'name': name,
            'full name': name,
            'category': convert_biolink_category_to_iri(category_label),
            'category label': category_label.replace(' ', '_'),
            'description': None,
            'synonym': [],
            'publications': [],
            'creation date': None,
            'update date': update_date,
            'deprecated': False,
            'replaced by': None,
            'provided by': provided_by}


def make_edge_key(edge_dict: dict):
    return edge_dict['subject'] + '---' + \
           edge_dict['object'] + '---' + \
           edge_dict['relation curie'] + '---' + \
           edge_dict['provided by']


def make_edge(subject_id: str,
              object_id: str,
              relation: str,
              relation_curie: str,
              predicate_label: str,
              provided_by: str,
              update_date: str = None):

    return {'subject': subject_id,
            'object': object_id,
            'edge label': predicate_label,
            'relation': relation,
            'relation curie': relation_curie,
            'negated': False,
            'publications': [],
            'publications info': {},
            'update date': update_date,
            'provided by': provided_by}


def predicate_label_to_iri_and_curie(predicate_label: str,
                                     relation_curie_prefix: str,
                                     relation_iri_prefix: str):
    predicate_label = predicate_label.replace(' ', '_')
    if ':' not in predicate_label:
        if relation_curie_prefix.lower() != 'biolink':
            predicate_label_to_use = convert_snake_case_to_camel_case(predicate_label)
        else:
            predicate_label_to_use = predicate_label
    else:
        predicate_label_to_use = predicate_label.replace(':', '_')
    return [urllib.parse.urljoin(relation_iri_prefix, predicate_label_to_use),
            relation_curie_prefix + ':' + predicate_label]


def make_edge_biolink(subject_curie_id: str,
                      object_curie_id: str,
                      predicate_label: str,
                      provided_by_curie: str,
                      update_date: str):
    [relation, relation_curie] = predicate_label_to_iri_and_curie(predicate_label,
                                                                  CURIE_PREFIX_BIOLINK,
                                                                  BASE_URL_BIOLINK_CONCEPTS)
    rel = make_edge(subject_curie_id,
                    object_curie_id,
                    relation,
                    relation_curie,
                    predicate_label,
                    provided_by_curie,
                    update_date)
    return rel


def is_a_valid_http_url(id: str) -> bool:
    valid = True
    try:
        validators.url(id)
        valid = id.startswith('http://') or id.startswith('https://')
    except validators.ValidationFailure:
        valid = False
    return valid


def load_ontology_from_owl_or_json_file(ontology_file_name: str):
    ont_factory = ontobio.ontol_factory.OntologyFactory()
    return ont_factory.create(ontology_file_name, ignore_cache=True)
