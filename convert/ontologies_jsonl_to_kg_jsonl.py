#!/usr/bin/env python3
''' ontologies_jsonl_to_kg_jsonl.py: Converts JSON Lines representation of ontologies into KG JSON Lines format

    Usage: ontologies_jsonl_to_kg_jsonl.py [--test] <inputFile.jsonl> <curiesToCategoriesYAML.yaml> <curiesToURLsYAML.yaml>  <biolink_version_number> <outputNodesFile.jsonl> <outputEdgesFile.jsonl>
'''


import argparse
import kg2_util
import json
import datetime

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


ID_TAG = "rdf:about"
NAME_TAG = "rdfs:label"

TEXT_KEY = "ENTRY_TEXT"
RESOURCE_KEY = "rdf:resource"

OWL_SOURCE_KEY = "owl_source"
OWL_SOURCE_NAME_KEY = "owl_source_name"

KEYS_DICT = dict()

COMMENT_PREFIX = "COMMENTS: "
DESCRIPTION_DELIM = " // "

# Encoding styles for different predicates
BASE_EDGE_TYPES = {"mondo-base:exactMatch": RESOURCE_KEY,
                   "mondo-base:closeMatch": RESOURCE_KEY,
                   "mondo-base:relatedMatch": RESOURCE_KEY,
                   "mondo-base:broadMatch": RESOURCE_KEY,
                   "mondo-base:narrowMatch": RESOURCE_KEY,
                   "skos:exactMatch": RESOURCE_KEY,
                   "skos:closeMatch": RESOURCE_KEY,
                   "skos:broadMatch": RESOURCE_KEY,
                   "skos:relatedMatch": RESOURCE_KEY,
                   "skos:narrowMatch": RESOURCE_KEY,
                   "obo:IAO_0100001": RESOURCE_KEY,
                   "obo:RO_0002175": RESOURCE_KEY,
                   "obo:RO_0002161": RESOURCE_KEY,
                   "obo:RO_0002604": RESOURCE_KEY,
                   "obo:RO_0002171": RESOURCE_KEY,
                   "obo:RO_0002174": RESOURCE_KEY,
                   "obo:RO_0002475": RESOURCE_KEY,
                   "obo:RO_0001900": RESOURCE_KEY,
                   "oboInOwl:hasAlternativeId": TEXT_KEY,
                   "oboInOwl:hasDbXref": TEXT_KEY,
                   "oboInOwl:xref": TEXT_KEY}

# Mapping structure used to recursively determine node category
CLASS_TO_SUPERCLASSES = dict()

# Node information storage, for while categories are determined
SAVED_NODE_INFO = dict()

# Storage for source information
SOURCE_INFO = dict()

# Used to store the category of nodes both from curies-to-categories.yaml and as they are recursively mapped
NODE_CATEGORY_MAPPINGS = dict()

# Used to store the prefix mappings from curies-to-categories.yaml
PREFIX_MAPPINGS = dict()

# Used to store extracted information from curies-to-urls-map.yaml
URI_MAP = dict()
URI_MAP_KEYS = list()
PREFIX_TO_IRI_MAP = dict()

# Prefixes for owl:Class elements that were unable to be mapped with curies-to-urls-map.yaml
MISSING_ID_PREFIXES = set()

# Category mapping techniques
FILE_MAPPING = "file"
PREFIX_MAPPING = "prefix"
RECURSE_MAPPING = "recurse"

# Keys for saving node and edges information between its initial processing and node/edge creation
ID_KEY = "id"
DEPRECATED_KEY = "deprecated"
UPDATE_DATE_KEY = "update_date"
CREATION_DATE_KEY = "creation_date"
SYNONYM_KEY = "synonym"
DESCRIPTION_KEY = "description_list"
NAME_KEY = "name"
SOURCE_KEY = "source"
BIOLOGICAL_SEQUENCE_KEY = "has_biological_sequence"
CATEGORY_KEY = "category"
EDGES_KEY = "edges"
IRI_KEY = "iri"
VERSION_KEY = "version"


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('curiesToCategoriesYAML', type=str)
    arg_parser.add_argument('curiesToURLsYAML', type=str)
    arg_parser.add_argument('biolinkVersionNumber', type=str)
    arg_parser.add_argument('outputNodesFile', type=str)
    arg_parser.add_argument('outputEdgesFile', type=str)
    return arg_parser.parse_args()


def categorize_node(node_id, recursion_depth=0):
    """
        Recursively navigate the hierarchy of node superclasses to identify the optimal categorization for a node.
        If a particular category for a node is desired, classify it as such within curies-to-categories.yaml.
    """
    # First, retrieve the node prefix
    node_prefix = node_id.split(':')[0]

    # If the node is directly mapped in curies-to-categories.yaml, utilize that mapping
    # The [1] field of NODE_CATEGORY_MAPPINGS[node_id] refers to the way that node was mapped
    if node_id in NODE_CATEGORY_MAPPINGS and NODE_CATEGORY_MAPPINGS[node_id][1] == FILE_MAPPING:
        return NODE_CATEGORY_MAPPINGS[node_id][0]

    # If the node isn't in curies-to-categories.yaml, but its prefix is, use that mapping
    if node_prefix in PREFIX_MAPPINGS:
        node_category = PREFIX_MAPPINGS[node_prefix]
        NODE_CATEGORY_MAPPINGS[node_id] = (node_category, PREFIX_MAPPING)
        return PREFIX_MAPPINGS[node_prefix]

    # Try to get the most common superclass categorization (naive method for picking category of nodes with multiple superclasses)
    # Initialize the category as named thing as a default
    superclass_categorizations = dict()
    highest_value = 0
    highest_category = kg2_util.BIOLINK_CATEGORY_NAMED_THING

    # To avoid unnecessary recursion, stop at 10 layers (prevents errors in subclass cycles)
    if recursion_depth == 10:
        return kg2_util.BIOLINK_CATEGORY_NAMED_THING

    # Perform the recursive mapping search for all of the node's superclasses
    for superclass in CLASS_TO_SUPERCLASSES.get(node_id, list()):
        # First, recurse
        superclass_category = categorize_node(superclass, recursion_depth + 1)

        # Then, determine the optimal categorization for the node based on naive category determination method
        if superclass_category not in superclass_categorizations:
            superclass_categorizations[superclass_category] = 0
        superclass_categorizations[superclass_category] += 1
        if superclass_categorizations[superclass_category] > highest_value:
            highest_value = superclass_categorizations[superclass_category]
            highest_category = superclass_category

    # Save the categorization
    NODE_CATEGORY_MAPPINGS[node_id] = (highest_category, RECURSE_MAPPING)
    return highest_category


def reformat_obo_date(date_str):
    """
        Reformat a date from an OWL field and save it as a datetime object for comparison purposes, handling a variety of input date styles
    """
    if date_str is None:
        return None

    if '-' in date_str:
        delim = 'T'
        if ' ' in date_str:
            delim = ' '
        date_spl = date_str.strip('Z').split(delim)
        date_fh = date_spl[0].split('-')
        year = int(date_fh[0])
        month = int(date_fh[1])
        day = int(date_fh[2])

        if month < 1 or month > 12 or day < 1 or day > 31:
            return None

        if len(date_spl) > 1:
            date_sh = date_spl[1].split(':')
            hour = int(date_sh[0])
            minute = int(date_sh[1])
            second = int(date_sh[2][0:1])

            return datetime.datetime(year, month, day, hour, minute, second)
        else:
            return datetime.datetime(year, month, day)
    else:
        date_spl = date_str.split(' ')
        date_fh = date_spl[0].split(':')
        year = int(date_fh[2])
        month = int(date_fh[1])
        day = int(date_fh[0])

        if month < 1 or month > 12 or day < 1 or day > 31:
            return None

        return datetime.datetime(year, month, day)


def pick_most_recent_date(dates, alternate_date=None):
    """
        Given a list of datetime objects, determine the most recent one
    """
    latest_date = None
    for date in dates:
        if date == None:
            continue
        if latest_date == None or date > latest_date:
            latest_date = date
    
    if latest_date == None:
        if alternate_date is not None:
            latest_date = alternate_date
        else:
            return None

    return latest_date.isoformat(sep=' ')


def save_biolink_information(biolink_version_number):
    """
        Save the Biolink version with the ontologies versions so we can construct a Biolink version node (hacky workaround)
    """
    source = kg2_util.CURIE_PREFIX_BIOLINK_SOURCE
    source_id = source + ":"
    iri = PREFIX_TO_IRI_MAP[source]
    name = "Biolink"
    SOURCE_INFO[source] = {SOURCE_KEY: source_id, IRI_KEY: iri, NAME_KEY: name, UPDATE_DATE_KEY: None, VERSION_KEY: biolink_version_number}


def process_ontology_term(ontology_node, source, ontology_name, owl_source=True):
    """
        Given an owl:Ontology (or analogous) element, determine all of the relevant attributes to construct a source node
    """
    # Only use the owl prefix on terms if it is an owl_source (i.e., not ORDO)
    owl_prefix = ""
    if owl_source:
        owl_prefix = "owl:"

    # Determine the version of the ontology through one of the three encoding methods (version number, version IRI, or date)
    ontology_version = None
    ontology_versions = [version.get(TEXT_KEY, str()) for version in ontology_node.get(owl_prefix + "versionInfo", list()) if TEXT_KEY in version]
    ontology_version_iri = [version.get(RESOURCE_KEY, str()) for version in ontology_node.get(owl_prefix + "versionIRI", list()) if RESOURCE_KEY in version]
    ontology_dates = [reformat_obo_date(version.get(TEXT_KEY, str())) for date_type in ["oboInOwl:date", "dcterms:date", "dc:date"] for version in ontology_node.get(date_type, list()) if TEXT_KEY in version]
    ontology_iri = ontology_node.get("rdf:about", str())
    if len(ontology_versions) == 1:
        ontology_version = ontology_versions[0]
    elif len(ontology_version_iri) == 1:
        # Strip the version number out of the IRI
        ontology_version = ontology_version_iri[0]
        version_replacements = [ontology_iri.replace('.owl', '') + '/', '/' + source, 'releases/']
        for replacement in version_replacements:
            ontology_version = ontology_version.replace(replacement, "")
        ontology_version = ontology_version.split('/')[0]
    elif len(ontology_dates) >= 1:
        ontology_version = pick_most_recent_date(ontology_dates)

    # Issue a warning if there is no versioning information
    if ontology_version is None:
        print("Warning: source", source, "lacks any versioning information.")

    ontology_date = reformat_obo_date(pick_most_recent_date(ontology_dates))

    # Convert the source file name to a CURIE ID
    source_id = kg2_util.CURIE_PREFIX_OBO + ':' + source

    # Add the source information to the SOURCE_INFO dictionary to later be made into a source node
    if source not in SOURCE_INFO:
        SOURCE_INFO[source] = {SOURCE_KEY: source_id, IRI_KEY: ontology_iri, NAME_KEY: ontology_name, UPDATE_DATE_KEY: ontology_date, VERSION_KEY: ontology_version}


def process_ontology_class(owl_class, source, ontology_name, owl_source=True):
    """
        Given an owl:Class (or analogous) element, strip out all of the relevant date to construct the node and edges 
    """
    # Only use the owl prefix on terms if it is an owl_source (i.e., not ORDO)
    owl_prefix = ""
    if owl_source:
        owl_prefix = "owl:"

    # Configure the node_id and node_iri
    # We only want to construct nodes for standard nodes that fit into KG2 mappings
    if ID_TAG not in owl_class:
        # These are typically genid classes which don't neatly map onto the KG2 schema
        return
    node_id = match_prefix(owl_class.get(ID_TAG, str()))
    if node_id is None:
        return
    node_prefix = node_id.split(':')[0]
    node_iri = PREFIX_TO_IRI_MAP[node_prefix] + node_id.replace(node_prefix + ':', '')

    # Configure the name
    name_list = [name.get(TEXT_KEY, None) for name in owl_class.get("rdfs:label", dict()) if TEXT_KEY in name]
    # Return if the node has no names
    if len(name_list) == 0:
        return

    # Configure the description
    description_list = list()
    description_list += [description.get(TEXT_KEY, None) for description in owl_class.get("obo:IAO_0000115", list()) if (TEXT_KEY in description)]
    description_list += [COMMENT_PREFIX + description.get(TEXT_KEY, str()) for description in owl_class.get("rdfs:comment", list()) if (TEXT_KEY in description)]
    description_list += [description.get(TEXT_KEY, None) for description in owl_class.get("obo:UBPROP_0000001", list()) if (TEXT_KEY in description)]
    description_list += [description.get(TEXT_KEY, None) for description in owl_class.get("obo:UBPROP_0000005", list()) if (TEXT_KEY in description)]
    description_list += [description.get(TEXT_KEY, None) for description in owl_class.get("efo1:source_description", list()) if (TEXT_KEY in description)]

    # Determine whether the node is deprecated
    deprecated = "true" in owl_class.get(owl_prefix + "deprecated", list())
    for name in name_list:
        search_name = name.lower()
        if search_name.startswith("obsolete") or search_name.startswith("(obsolete") or search_name.endswith("obsolete"):
            deprecated = True

    # Configure the synonyms
    synonym_list = list()
    synonym_keys = ["oboInOwl:hasExactSynonym", "oboInOwl:hasRelatedSynonym", "oboInOwl:hasNarrowSynonym", "oboInOwl:hasBroadSynonym", "go:hasExactSynonym",
                    "go:hasSynonym", "go:hasNarrowSynonym", "go:hasBroadSynonym", "obo:IAO_0000118", "obo:IAO_0000589", "go:hasRelatedSynonym", "obo:IAO_0000111",
                    "obo:IAO_0000028", "skos:prefLabel"]
    synonym_list += [synonym.get(TEXT_KEY, None) for synonym_key in synonym_keys for synonym in owl_class.get(synonym_key, list()) if (TEXT_KEY in synonym)]

    # Configure the update date
    update_date_list = list()
    update_date_keys = ["dc:date", "dcterms:date", "terms:date"]
    update_date_list += [reformat_obo_date(update_date.get(TEXT_KEY, None)) for update_date_key in update_date_keys for update_date in owl_class.get(update_date_key, list()) if (TEXT_KEY in update_date)]

    # Configure the creation date
    creation_date_list = list()
    creation_date_keys = ["oboInOwl:creation_date", "go:creation_date"]
    creation_date_list += [reformat_obo_date(creation_date.get(TEXT_KEY, None)) for creation_date_key in creation_date_keys for creation_date in owl_class.get(creation_date_key, list()) if (TEXT_KEY in creation_date)]

    # Configure the biological sequence
    # We are only currently using inchi, but we might as well extract all of them in case this changes in the future
    has_biological_sequence = dict()
    has_biological_sequence['formula'] = [biological_sequence.get(TEXT_KEY, None) for biological_sequence in owl_class.get("chebi:formula", list()) if TEXT_KEY in biological_sequence]
    has_biological_sequence['smiles'] = [biological_sequence.get(TEXT_KEY, None) for biological_sequence in owl_class.get("chebi:smiles", list()) if TEXT_KEY in biological_sequence]
    has_biological_sequence['inchi'] = [biological_sequence.get(TEXT_KEY, None) for biological_sequence in owl_class.get("chebi:inchi", list()) if TEXT_KEY in biological_sequence]
    has_biological_sequence['inchikey'] = [biological_sequence.get(TEXT_KEY, None) for biological_sequence in owl_class.get("chebi:inchikey", list()) if TEXT_KEY in biological_sequence]

    # Extract edge triples
    edges_list = list()

    # First, extract the edges with predicates that easily map to extraction patters
    for edge_type in BASE_EDGE_TYPES:
        for edge in owl_class.get(edge_type, list()):
            if BASE_EDGE_TYPES[edge_type] in edge:
                edges_list.append((edge_type, edge.get(BASE_EDGE_TYPES[edge_type], None)))

    # Next, identify the edges which are tightly nested under a layer of other information
    restriction_edges = list()
    restriction_edges += [(edge, "rdfs:subClassOf") for edge in owl_class.get("rdfs:subClassOf", list())]
    for equiv in owl_class.get(owl_prefix + "equivalentClass", list()):
        for mini_class in equiv.get(owl_prefix + "Class", list()):
            for edge in mini_class.get(owl_prefix + "intersectionOf", list()):
                restriction_edges.append((edge, owl_prefix + "equivalentClass"))

    # Then, extract the actual information from those edges
    for (edge, general_edge_type) in restriction_edges:
        # First, handle those with the restriction elements (the owl:EquivalentClass and rdfs:subClassOf sub-predicate cases)
        for restriction in edge.get(owl_prefix + "Restriction", list()):
            edge_type = restriction.get(owl_prefix + "onProperty", list())
            edge_object = restriction.get(owl_prefix + "someValuesFrom", list())

            # Ensure each of those lists only have one item, so that we can pull item [0] in the next step to correctly identify the respective information
            if len(edge_type) != 1:
                assert len(edge_type) <= 1, edge 
                continue
            if len(edge_object) != 1:
                assert len(edge_object) <= 1, edge
                continue
            edge_type = edge_type[0].get(RESOURCE_KEY, None)
            edge_object = edge_object[0].get(RESOURCE_KEY, None)

            if edge_type != None and edge_object != None:
                edges_list.append((edge_type, edge_object))

        # Then handle the generic rdfs:subClassOf case
        if RESOURCE_KEY in edge:
            edges_list.append((general_edge_type, edge.get(RESOURCE_KEY, None)))

    # Convert the edges into CURIEs so they can later be converted into edges
    superclasses = set()
    final_edges_list = list()
    for (edge_relation, edge_object) in edges_list:
        # Ensure the edge corresponds to a KG2 mapping
        edge_object = match_prefix(edge_object)
        if edge_object is None:
            continue
        edge_relation = match_prefix(edge_relation)
        if edge_relation is None:
            continue

        # Identify superclass relationships
        if edge_relation in ["rdfs:subClassOf"]:
            superclasses.add(edge_object)

        # Add the processed edge to the list of this node's edges
        final_edges_list.append((edge_relation, edge_object))

    # Formally save the superclass relations to the superclass hierarchy
    # This is an imperfect way to make it deterministic; We don't want duplicate superclasses, but we also want the order to remain the same across runs
    superclasses = sorted(list(superclasses))
    if node_id not in CLASS_TO_SUPERCLASSES:
        CLASS_TO_SUPERCLASSES[node_id] = list()
    CLASS_TO_SUPERCLASSES[node_id] += superclasses
    CLASS_TO_SUPERCLASSES[node_id] = sorted(list(set(CLASS_TO_SUPERCLASSES[node_id])))

    # Make sure that we have an entry for the node (since multiple sources can have information on a particular node)
    if node_id not in SAVED_NODE_INFO:
        SAVED_NODE_INFO[node_id] = list()
    # Save this source's version of the node information
    SAVED_NODE_INFO[node_id].append({ID_KEY: node_id,
                                     DEPRECATED_KEY: deprecated,
                                     UPDATE_DATE_KEY: update_date_list,
                                     CREATION_DATE_KEY: creation_date_list,
                                     SYNONYM_KEY: synonym_list,
                                     DESCRIPTION_KEY: description_list,
                                     NAME_KEY: name_list,
                                     SOURCE_KEY: source,
                                     BIOLOGICAL_SEQUENCE_KEY: has_biological_sequence,
                                     IRI_KEY: node_iri,
                                     EDGES_KEY: final_edges_list})


def process_ontology_item(ontology_item):
    """
        Handler for processing ontology subsets
    """
    # Extract these custom input attributes (parts of ont-load-inventory.yaml put into owlparser.py output)
    source = ontology_item.get(OWL_SOURCE_KEY, str())
    ontology_name = ontology_item.get(OWL_SOURCE_NAME_KEY, str())

    for owl_class in ontology_item.get("owl:Class", list()):
        process_ontology_class(owl_class, source, ontology_name)

    # Special case for non-owl prefix sources (e.g. ORDO)
    for owl_class in ontology_item.get("Class", list()):
        process_ontology_class(owl_class, source, ontology_name, False)

    for ontology_node in ontology_item.get("owl:Ontology", list()):
        process_ontology_term(ontology_node, source, ontology_name)

    # Special case for non-owl prefix sources (e.g. ORDO)
    for ontology_node in ontology_item.get("Ontology", list()):
        process_ontology_term(ontology_node, source, ontology_name, False)


def generate_uri_map(curies_to_urls_file_name):
    """
        Import the curies-to-urls-map.yaml for use in CURIE ID and IRI resolution
    """
    uri_input_map = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_urls_file_name))
    bidirectional_map = uri_input_map['use_for_bidirectional_mapping']
    contraction_map = uri_input_map['use_for_contraction_only']

    # Import the bidirectional map for both ID mapping (URI_MAP) and IRI expansion, given the standard prefix (PREFIX_TO_IRI_MAP)
    for curie_prefix_dict in bidirectional_map:
        for curie_prefix in curie_prefix_dict:
            curie_url = curie_prefix_dict[curie_prefix]
            URI_MAP[curie_url] = curie_prefix
            PREFIX_TO_IRI_MAP[curie_prefix] = curie_url

    # Import the contraction map for ID mapping (URI_MAP)
    for curie_prefix_dict in contraction_map:
        for curie_prefix in curie_prefix_dict:
            curie_url = curie_prefix_dict[curie_prefix]
            URI_MAP[curie_url] = curie_prefix

    # So that you get the most accurate match, you want to match to the longest url (in case one is a substring of another)
    # Apparently have to use global key word to write to a module wide list (https://stackoverflow.com/questions/4630543/defining-lists-as-global-variables-in-python)
    global URI_MAP_KEYS
    URI_MAP_KEYS = sorted(URI_MAP.keys(), key=len, reverse=True)


def match_prefix(node_id):
    """
        Given a node_id from an ontology (possibly actually an IRI), return the KG2-standard CURIE ID for the node
    """
    # Iterate through the map keys, comparing with the longest urls first (for the most accurate match)
    for curie_url in URI_MAP_KEYS:
        if node_id.startswith(curie_url):
            return node_id.replace(curie_url, URI_MAP[curie_url] + ":")
    
    # If there is no match, attempt to distill down the ID into just the prefix (not always possible) and add it to the list of prefixes not in KG2
    if "http" in node_id:
        MISSING_ID_PREFIXES.add('/'.join(node_id.split('/')[0:-1]) + "/")
    elif ':' in node_id:
        MISSING_ID_PREFIXES.add(node_id.split(':')[0] + ":")
    elif '_' in node_id:
        MISSING_ID_PREFIXES.add(node_id.split('_')[0] + "_")
    else:
        MISSING_ID_PREFIXES.add(node_id)


def construct_nodes_and_edges(nodes_output, edges_output):
    """
        Output the nodes and edges from the ontologies once the node information has been extracted and categories have been assigned
    """
    # Construct all of the source nodes
    for source in SOURCE_INFO:
        source_date = pick_most_recent_date([SOURCE_INFO[source][UPDATE_DATE_KEY]])
        source_name = SOURCE_INFO[source][NAME_KEY] + " v" + SOURCE_INFO[source][VERSION_KEY]
        source_id = SOURCE_INFO[source][SOURCE_KEY]
        source_iri = SOURCE_INFO[source][IRI_KEY]
        node = kg2_util.make_node(source_id, source_iri, source_name, kg2_util.SOURCE_NODE_CATEGORY, source_date, source_id)

        nodes_output.write(node)

    # Constrct the regular nodes and edges
    for node_id in SAVED_NODE_INFO:
        # Iterate across all of the sources which have defined this node
        for source_node_index in range(len(SAVED_NODE_INFO[node_id])):
            # Ignore deprecated nodes
            if SAVED_NODE_INFO[node_id][source_node_index][DEPRECATED_KEY]:
                continue
            # Extract all of the information from the SAVED_NODE_INFO dictionary
            name = SAVED_NODE_INFO[node_id][source_node_index][NAME_KEY][0] # Imperfect way of choosing the name
            node_iri = SAVED_NODE_INFO[node_id][source_node_index][IRI_KEY]
            description = DESCRIPTION_DELIM.join(SAVED_NODE_INFO[node_id][source_node_index][DESCRIPTION_KEY])
            has_biological_sequence = SAVED_NODE_INFO[node_id][source_node_index][BIOLOGICAL_SEQUENCE_KEY].get("smiles", None)
            synonyms = SAVED_NODE_INFO[node_id][source_node_index][SYNONYM_KEY]
            category = SAVED_NODE_INFO[node_id][source_node_index][CATEGORY_KEY]

            # Obtain source information
            source = SAVED_NODE_INFO[node_id][source_node_index][SOURCE_KEY]
            provided_by = kg2_util.CURIE_PREFIX_OBO + ':' + source
            source_date = SOURCE_INFO[source][UPDATE_DATE_KEY]

            # Determine the node's dates
            update_date = pick_most_recent_date(SAVED_NODE_INFO[node_id][source_node_index][UPDATE_DATE_KEY], source_date)
            creation_date = pick_most_recent_date(SAVED_NODE_INFO[node_id][source_node_index][CREATION_DATE_KEY], source_date)

            # Construct the node and add in the other attributes
            node = kg2_util.make_node(node_id, node_iri, name, category, update_date, provided_by)
            node["description"] = description
            node["has_biological_sequence"] = has_biological_sequence
            node["creation_date"] = creation_date
            node["synonym"] = synonyms

            # Output the node
            nodes_output.write(node)

            # Construct the edges from the triples saved
            for (edge_relation, edge_object) in SAVED_NODE_INFO[node_id][source_node_index][EDGES_KEY]:
                relation_label = edge_relation.split(':')[1]
                edge = kg2_util.make_edge(node_id, edge_object, edge_relation, relation_label, provided_by, update_date)

                edges_output.write(edge)


if __name__ == '__main__':
    print("Start time: ", kg2_util.date())

    # Obtain all of the input arguments
    args = get_args()
    input_file_name = args.inputFile
    curies_to_categories_file_name = args.curiesToCategoriesYAML
    curies_to_urls_file_name = args.curiesToURLsYAML
    biolink_version_number = args.biolinkVersionNumber
    output_nodes_file_name = args.outputNodesFile
    output_edges_file_name = args.outputEdgesFile
    test_mode = args.test

    # Create the output files
    nodes_info, edges_info = kg2_util.create_kg2_jsonlines(test_mode)
    nodes_output = nodes_info[0]
    edges_output = edges_info[0]

    # Prepare the node category dictionaries with the information from curies-to-categories.yaml 
    curies_to_categories_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_categories_file_name))
    for mapping_node in curies_to_categories_data["term-mappings"]:
        NODE_CATEGORY_MAPPINGS[mapping_node] = (curies_to_categories_data["term-mappings"][mapping_node], FILE_MAPPING)
    for prefix in curies_to_categories_data["prefix-mappings"]:
        PREFIX_MAPPINGS[prefix] = curies_to_categories_data["prefix-mappings"][prefix]

    # Begin reading the JSON Lines input file containing all of the ontologies
    input_read_jsonlines_info = kg2_util.start_read_jsonlines(input_file_name)
    input_data = input_read_jsonlines_info[0]

    # Prepare the URI maps for mapping ontology information to KG2 CURIE IDs and IRIs
    generate_uri_map(curies_to_urls_file_name)

    # Save the Biolink node information before processing
    save_biolink_information(biolink_version_number)

    # Extract all of the necessary information from the ontologies
    for ontology_item in input_data:
        process_ontology_item(ontology_item)

    # Categorize every node and save the information in the information dictionary for the node
    for node_id in SAVED_NODE_INFO:
        categorize_node(node_id)
        node_category = NODE_CATEGORY_MAPPINGS[node_id][0]
        for index in range(len(SAVED_NODE_INFO[node_id])):
            SAVED_NODE_INFO[node_id][index][CATEGORY_KEY] = node_category

    # Save all of the node and edge information in KG2 format
    construct_nodes_and_edges(nodes_output, edges_output)

    kg2_util.close_kg2_jsonlines(nodes_info, edges_info, output_nodes_file_name, output_edges_file_name)

    print("Finish time: ", kg2_util.date())
