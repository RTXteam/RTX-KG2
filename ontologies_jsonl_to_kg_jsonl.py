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

CLASSES_DICT = dict()

def get_args():
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('--test', dest='test',
							action="store_true", default=False)
	arg_parser.add_argument('inputFile', type=str)
	arg_parser.add_argument('outputFile', type=str)
	return arg_parser.parse_args()

def process_ontology_item(ontology_item):
	source = ontology_item.get(OWL_SOURCE_KEY, str())
	for owl_class in ontology_item.get(OWL_CLASS_TAG, list()):
		# Typically genid classes which don't neatly map onto the KG2 schema
		if ID_TAG not in owl_class:
			continue
		# TODO: MAP THIS HERE, since not all sources use same IRIs for the same nodes
		node_id = owl_class.get(ID_TAG, str())

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

		for edge_type in ["obo:RO_0002175", "obo:RO_0002161", "obo:RO_0002604", "obo:RO_0002171", "obo:RO_0002174", "obo:RO_0002475", "obo:RO_0001900", "obo:RO_0004050"]:
			for edge in owl_class.get(edge_type, list()):
				if RESOURCE_KEY in edge:
					edges_list.append((edge_type, edge.get(RESOURCE_KEY, None)))

		for edge_type in ["oboInOwl:hasDbXref"]:
			for edge in owl_class.get(edge_type, list()):
				if TEXT_KEY in edge:
					edges_list.append((edge_type, edge.get(TEXT_KEY, None)))

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


		# node_id = owl_class.get(ID_TAG, list())

		# superclasses = [superclass.get(RESOURCE_KEY, str()) for superclass in owl_class.get(SUBCLASS_TAG, list())]

		# # Also query for comments?
		# # Descriptions appear to be additive in current KG2
		# descriptions = owl_class.get(DESCRIPTION_TAG, list())
		# assert len(descriptions) <= 1
		# description = str()
		# for element in descriptions:
		# 	description += element[TEXT_KEY]

		# xrefs = [xref[TEXT_KEY] for xref in owl_class.get(XREF_TAG, list())]
		# for element in owl_class.get(XREF_TAG, list()):
		# 	xrefs.append(element[TEXT_KEY])

		# exact_matches = [exact_match[RESOURCE_KEY] for exact_match in owl_class.get(EXACT_MATCH_TAG, list())]

		# names = owl_class.get(NAME_TAG, list())
		# assert len(names) <= 1, ontology_item
		# name = str()
		# for element in names:
		# 	name += element[TEXT_KEY]

		# node = {"id": node_id, "superclasses": superclasses, "description": description, "xrefs": xrefs, "name": name, "exact_matches": exact_matches}

		node = {"id": node_id, "description_list": description_list, "name": name_list, "source": source, "has_biological_sequence": has_biological_sequence, "edges": edges_list}
		print(json.dumps(node, indent=4))


if __name__ == '__main__':
	args = get_args()
	input_file_name = args.inputFile
	output_file_name = args.outputFile

	input_read_jsonlines_info = kg2_util.start_read_jsonlines(input_file_name)
	input_data = input_read_jsonlines_info[0]

	owl_class_count = 0
	for ontology_item in input_data:
		process_ontology_item(ontology_item)

	# print("OWL Classes:", owl_class_count)
	# for key in KEYS_DICT:
	# 	KEYS_DICT[key] = KEYS_DICT[key] / owl_class_count
	# print(json.dumps(KEYS_DICT, indent=4, sort_keys=True))