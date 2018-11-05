import ontobio
import copy
import yaml
import urllib.request
import prefixcommons

#biolink_url = "https://raw.githubusercontent.com/biolink/biolink-model/master/biolink-model.yaml"
biolink_url = "file:biolink-model.yaml"
biolink_data = yaml.safe_load(urllib.request.urlopen(biolink_url))

# command to convert an OWL file to an OBO file:
#   owltools nbo.owl -o -f obo nbo.obo

# need to pull in these OWL ontologies:
# "http://purl.obolibrary.org/obo/fma.owl",

# don't use the SPARQL query method (i.e., like OntologyFactory.create("hp")) because you don't get all
# the fields that you want for each ontology term

# ontology_codes = ["obo:bfo", "obo:ro", "obo:hp", "obo:go", "obo:chebi", "obo:go",
#                   "http://purl.obolibrary.org/obo/ncbitaxon/subsets/taxslim.owl",
#                   "obo:fma", "obo:pato", "obo:mondo", "obo:cl", "obo:doid", "obo:pr",
#                   "http://purl.obolibrary.org/obo/uberon/ext.owl",
#                   "obo:dron"]

ontology_codes = ['obo:hp', 'obo:go']


def get_biolink_map_of_curies_to_categories(biolink_yaml_data):
    map_curie_to_biolink_category = dict()
    for category_name, reldata in biolink_yaml_data['classes'].items():
        mappings = reldata.get('mappings', None)
        if mappings is not None:
            assert type(mappings) == list
            for curie_id in mappings:
                map_curie_to_biolink_category[curie_id] = category_name
    return map_curie_to_biolink_category


biolink_map_of_curies_to_categories = get_biolink_map_of_curies_to_categories(biolink_data)


def head_list(mylist, n=3):
    return mylist[0:n]


def head_dict(mydict, n=3):
    return dict(list(mydict.items())[0:(n-1)])


def make_ontology_from_ontcode(ontcode):
    print("Creating ontology object: " + ontcode)
    return ontobio.ontol_factory.OntologyFactory().create(ontcode)


def get_biolink_category_for_node(curie_id, ontology, map_curie_to_biolink_category):
    ret_category = None
    map_category = map_curie_to_biolink_category.get(curie_id, None)
    if map_category is not None:
        ret_category = map_category
    else:
        for parent_curie_id in ontology.parents(curie_id, ['subClassOf']):
            parent_category = get_biolink_category_for_node(parent_curie_id, ontology, map_curie_to_biolink_category)
            if parent_category is not None:
                ret_category = parent_category
                break
    return ret_category


def get_nodes_dict(ontology, map_curie_to_biolink_category):
    ret_dict = dict()
    for node_curie_id in ontology.nodes():
        onto_node_dict = ontology.node(node_curie_id)
        node_dict = dict()
        iri = onto_node_dict['id']
        node_dict['id'] = node_curie_id
        node_dict['iri'] = iri
        node_label = onto_node_dict.get('label', None)
        node_dict['full name'] = node_label
        node_name = onto_node_dict.get('lbl', None)
        if node_name is None:
            node_name = node_dict['full name']
        node_dict['name'] = node_name
        node_meta = onto_node_dict.get('meta', None)
        node_category = get_biolink_category_for_node(node_curie_id, ontology, map_curie_to_biolink_category)
        node_dict['category'] = node_category
        node_description = None
        if node_meta is not None:
            node_definition = node_meta.get('definition', None)
            if node_definition is not None:
                node_description = node_definition['val']
        node_dict['description'] = node_description
        node_type = onto_node_dict.get('type', None)
        node_dict['ontology_node_type'] = node_type
        ret_dict[node_curie_id] = node_dict
    return ret_dict


ontology_objects = [make_ontology_from_ontcode(ontcode) for ontcode in ontology_codes]

master_ontology = copy.deepcopy(ontology_objects[0])
master_ontology.merge(ontology_objects)

predicate_strs_list = master_ontology.relations_used()
nodes_dict = get_nodes_dict(master_ontology, biolink_map_of_curies_to_categories)

