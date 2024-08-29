import argparse
import kg2_util
import json

OWL_CLASS_TAG = "owl:Class"
SUBCLASS_TAG = "rdfs:subClassOf"
DESCRIPTION_TAG = "obo:IAO_0000115"
XREF_TAG = "oboInOwl:hasDbXref"
ID_TAG = "rdf:about"
NAME_TAG = "rdfs:label"
EXACT_MATCH_TAG = "skos:exactMatch"
COMMENT_TAG = "rdfs:comment"

TEXT_KEY = "ENTRY_TEXT"
RESOURCE_KEY = "rdf:resource"

OWL_SOURCE_KEY = "owl_source"

KEYS_DICT = dict()

COMMENT_PREFIX = "COMMENTS: "

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

CLASS_TO_SUPERCLASSES = dict()
SAVED_NODE_INFO = dict()
SOURCE_INFO = dict()

NODE_CATEGORY_MAPPINGS = dict()
PREFIX_MAPPINGS = dict()

CLASSES_DICT = dict()

URI_MAP = dict()
URI_MAP_KEYS = list()

MISSING_ID_PREFIXES = set()

FILE_MAPPING = "file"
PREFIX_MAPPING = "prefix"
RECURSE_MAPPING = "recurse"

def get_args():
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('--test', dest='test',
							action="store_true", default=False)
	arg_parser.add_argument('inputFile', type=str)
	arg_parser.add_argument('curiesToCategoriesYAML', type=str)
	arg_parser.add_argument('outputFile', type=str)
	return arg_parser.parse_args()

def categorize_node(node_id, recursion_depth=0):
	node_prefix = node_id.split(':')[0]

	if node_id in NODE_CATEGORY_MAPPINGS and NODE_CATEGORY_MAPPINGS[node_id][1] == FILE_MAPPING:
		return NODE_CATEGORY_MAPPINGS[node_id][0]

	if node_prefix in PREFIX_MAPPINGS:
		node_category = PREFIX_MAPPINGS[node_prefix]
		NODE_CATEGORY_MAPPINGS[node_id] = (node_category, PREFIX_MAPPING)
		return PREFIX_MAPPINGS[node_prefix]

	# Get try to get the most common superclass categorization
	superclass_categorizations = dict()
	highest_value = 0
	highest_category = kg2_util.BIOLINK_CATEGORY_NAMED_THING
	if recursion_depth == 10:
		return kg2_util.BIOLINK_CATEGORY_NAMED_THING

	for superclass in CLASS_TO_SUPERCLASSES.get(node_id, list()):
		superclass_category = categorize_node(superclass, recursion_depth + 1)
		if superclass_category not in superclass_categorizations:
			superclass_categorizations[superclass_category] = 0
		superclass_categorizations[superclass_category] += 1
		if superclass_categorizations[superclass_category] > highest_value:
			highest_value = superclass_categorizations[superclass_category]
			highest_category = superclass_category

	NODE_CATEGORY_MAPPINGS[node_id] = (highest_category, RECURSE_MAPPING)
	return highest_category



def process_ontology_item(ontology_item):
	source = ontology_item.get(OWL_SOURCE_KEY, str())
	for owl_class in ontology_item.get(OWL_CLASS_TAG, list()):
		# Typically genid classes which don't neatly map onto the KG2 schema
		if ID_TAG not in owl_class:
			continue
		node_id = match_prefix(owl_class.get(ID_TAG, str()))
		if node_id is None:
			continue

		# Configure the name
		name_list = [name.get(TEXT_KEY, None) for name in owl_class.get("rdfs:label", dict()) if TEXT_KEY in name]
		if len(name_list) == 0:
			continue

		# Configure the description
		description_list = list()
		description_list += [description.get(TEXT_KEY, None) for description in owl_class.get("obo:IAO_0000115", list()) if (TEXT_KEY in description)]
		description_list += [COMMENT_PREFIX + description.get(TEXT_KEY, str()) for description in owl_class.get("rdfs:comment", list()) if (TEXT_KEY in description)]
		description_list += [description.get(TEXT_KEY, None) for description in owl_class.get("obo:UBPROP_0000001", list()) if (TEXT_KEY in description)]
		description_list += [description.get(TEXT_KEY, None) for description in owl_class.get("obo:UBPROP_0000005", list()) if (TEXT_KEY in description)]
		description_list += [description.get(TEXT_KEY, None) for description in owl_class.get("efo1:source_description", list()) if (TEXT_KEY in description)]

		# Configure the biological sequence
		has_biological_sequence = dict()
		has_biological_sequence['formula'] = [biological_sequence.get(TEXT_KEY, None) for biological_sequence in owl_class.get("chebi:formula", list()) if TEXT_KEY in biological_sequence]
		has_biological_sequence['smiles'] = [biological_sequence.get(TEXT_KEY, None) for biological_sequence in owl_class.get("chebi:smiles", list()) if TEXT_KEY in biological_sequence]
		has_biological_sequence['inchi'] = [biological_sequence.get(TEXT_KEY, None) for biological_sequence in owl_class.get("chebi:inchi", list()) if TEXT_KEY in biological_sequence]
		has_biological_sequence['inchikey'] = [biological_sequence.get(TEXT_KEY, None) for biological_sequence in owl_class.get("chebi:inchikey", list()) if TEXT_KEY in biological_sequence]

		# Extract edge triples
		edges_list = list()

		for edge_type in BASE_EDGE_TYPES:
			for edge in owl_class.get(edge_type, list()):
				if BASE_EDGE_TYPES[edge_type] in edge:
					edges_list.append((edge_type, edge.get(BASE_EDGE_TYPES[edge_type], None)))


		restriction_edges = list()
		restriction_edges += [(edge, "rdfs:subClassOf") for edge in owl_class.get("rdfs:subClassOf", list())]
		for equiv in owl_class.get("owl:equivalentClass", list()):
			for mini_class in equiv.get("owl:Class", list()):
				for edge in mini_class.get("owl:intersectionOf", list()):
					restriction_edges.append((edge, "owl:equivalentClass"))

		for (edge, general_edge_type) in restriction_edges:
			for restriction in edge.get("owl:Restriction", list()):
				edge_type = restriction.get("owl:onProperty", list())
				edge_object = restriction.get("owl:someValuesFrom", list())
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

			if RESOURCE_KEY in edge:
				edges_list.append((general_edge_type, edge.get(RESOURCE_KEY, None)))

		superclasses = set()
		final_edges_list = list()
		for (edge_relation, edge_object) in edges_list:
			edge_object = match_prefix(edge_object)
			if edge_object is None:
				continue
			edge_relation = match_prefix(edge_relation)
			if edge_relation is None:
				continue
			if edge_relation in ["rdfs:subClassOf"]:
				superclasses.add(edge_object)
			final_edges_list.append((edge_relation, edge_object))

		# Imperfect way to make it deterministic
		superclasses = sorted(list(superclasses))
		if node_id not in CLASS_TO_SUPERCLASSES:
			CLASS_TO_SUPERCLASSES[node_id] = list()
		CLASS_TO_SUPERCLASSES[node_id] += superclasses
		CLASS_TO_SUPERCLASSES[node_id] = sorted(list(set(CLASS_TO_SUPERCLASSES[node_id])))

		if node_id not in SAVED_NODE_INFO:
			SAVED_NODE_INFO[node_id] = list()
		SAVED_NODE_INFO[node_id].append({"id": node_id, "description_list": description_list, "name": name_list, "source": source, "has_biological_sequence": has_biological_sequence, "edges": final_edges_list})

	for ontology_node in ontology_item.get("owl:Ontology", list()):
		ontology_version = None
		ontology_versions = [version.get(TEXT_KEY, str()) for version in ontology_node.get("owl:versionInfo", list()) if TEXT_KEY in version]
		ontology_version_iri = [version.get(RESOURCE_KEY, str()) for version in ontology_node.get("owl:versionIRI", list()) if RESOURCE_KEY in version]
		ontology_date = [version.get(TEXT_KEY, str()) for date_type in ["oboInOwl:date", "dcterms:date", "dc:date"] for version in ontology_node.get(date_type, list()) if TEXT_KEY in version]
		if len(ontology_versions) == 1:
			ontology_version = ontology_versions[0]
		elif len(ontology_version_iri) == 1:
			ontology_version = ontology_version_iri[0]
		elif len(ontology_date) == 1:
			ontology_version = ontology_date[0]

		if ontology_version is None:
			print("Warning: source", source, "lacks any versioning information.")
		if source not in SOURCE_INFO:
			SOURCE_INFO[source] = {"source": source, "ontology_date": ontology_date, "ontology_version": ontology_version}


def generate_uri_map():
	uri_input_map = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string("maps/curies-to-urls-map.yaml"))
	bidirectional_map = uri_input_map['use_for_bidirectional_mapping']
	contraction_map = uri_input_map['use_for_contraction_only']

	for curie_prefix_dict in bidirectional_map:
		for curie_prefix in curie_prefix_dict:
			curie_url = curie_prefix_dict[curie_prefix]
			URI_MAP[curie_url] = curie_prefix

	for curie_prefix_dict in contraction_map:
		for curie_prefix in curie_prefix_dict:
			curie_url = curie_prefix_dict[curie_prefix]
			URI_MAP[curie_url] = curie_prefix

	# So that you get the most accurate match, you want to match to the longest url (in case one is a substring of another)
	# Apparently have to use global key word to write to a module wide list (https://stackoverflow.com/questions/4630543/defining-lists-as-global-variables-in-python)
	global URI_MAP_KEYS
	URI_MAP_KEYS = sorted(URI_MAP.keys(), key=len, reverse=True)

def match_prefix(node_id):
	for curie_url in URI_MAP_KEYS:
		if node_id.startswith(curie_url):
			return node_id.replace(curie_url, URI_MAP[curie_url] + ":")
	
	if "http" in node_id:
		MISSING_ID_PREFIXES.add('/'.join(node_id.split('/')[0:-1]) + "/")
	elif ':' in node_id:
		MISSING_ID_PREFIXES.add(node_id.split(':')[0] + ":")
	elif '_' in node_id:
		MISSING_ID_PREFIXES.add(node_id.split('_')[0] + "_")
	else:
		MISSING_ID_PREFIXES.add(node_id)


if __name__ == '__main__':
	args = get_args()
	input_file_name = args.inputFile
	curies_to_categories_file_name = args.curiesToCategoriesYAML
	output_file_name = args.outputFile

	curies_to_categories_data = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(curies_to_categories_file_name))
	for mapping_node in curies_to_categories_data["term-mappings"]:
		NODE_CATEGORY_MAPPINGS[mapping_node] = (curies_to_categories_data["term-mappings"][mapping_node], FILE_MAPPING)
	for prefix in curies_to_categories_data["prefix-mappings"]:
		PREFIX_MAPPINGS[prefix] = curies_to_categories_data["prefix-mappings"][prefix]

	input_read_jsonlines_info = kg2_util.start_read_jsonlines(input_file_name)
	input_data = input_read_jsonlines_info[0]

	owl_class_count = 0
	ontology_prefixes = set()
	generate_uri_map()
	for ontology_item in input_data:
		process_ontology_item(ontology_item)

	for node_id in SAVED_NODE_INFO:
		categorize_node(node_id)

	print(json.dumps(NODE_CATEGORY_MAPPINGS, indent=4))

	# Can add this back in later
	# print(json.dumps(sorted(list(MISSING_ID_PREFIXES)), indent=4))
