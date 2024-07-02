# Adding Node and Edge Properties in KG2

## Criteria for Adding Properties
Properties should not be added into KG2 on a whim. Every KG2 node and every KG2 edge has the same properties. We use TSV files as the basis for our Neo4j import. One of the requirements for TSV files is that every column be in line with the header. Thus, it is important that every KG2 node and every KG2 edge must contain all of the same properties in its respective TSV file. Due to the scope of KG2, storage costs are a real concern. Consequently, it is important that we don't add properties that won't be filled. Rows and rows of null values do not bring additional value to KG2 but increase our computational costs. Before adding properties, consider the following rules of thumb:
 - A new property should be able to be filled by multiple sources.
 - A new property should serve a defined role to the downstream system.

## How to Pick Where to Add a Property
There are two general sections of the build code where properties can be added:
 - [Within the ETL scripts](#etl-based-property-add)
    - This is the standard place to add properties. If the value of a property comes from the source file/database, it should be assigned within the ETL scripts.
 - [When the graph is being filtered (`filter_kg_and_remap_predicates.py`)](#post-etl-generalized-property-add)
    - This is a good place to add properties if they are based on a property assigned in an ETL script, but need to be assigned across ETL scripts. Currently, we assign predicates this way. There is a one-to-one mapping guide for source relations (ex. `HMDB:in_pathway`) to Biolink predicates (ex. `biolink:participates_in`). This is useful because if a relation-predicate pair changes, it is fast and easy to rebuild. There is no need to rebuild a source file (a `kg2-{source}.json` file) if a mapping changes. Also, it prevents a relation (such as `owl:sameAs`, which is assigned as a source relation in multiple scripts) from being mapped two different ways to a biolink predicate. This generally involves creating a YAML file that supplies mappings from the property assigned in the ETL script to the new property.

## ETL-Based Property Add

1. Update the `make_node` and `make_edge` functions in `kg2_util.py`.
    - This ensures that nodes and edges are uniform throughout KG2.
    - Currently, all nodes and edges must have the same properties (even if some of their values are null) because of the TSV import method we use for Neo4j.
    - There are ways that we could restructure the build process and our Neo4j import method so that this is not necessary, but our current perspective is that the work required does not return a big enough reward. However, I will link instructions about how that could be done down the road here, in case that is desired in the future: https://neo4j.com/docs/operations-manual/current/tools/neo4j-admin-import/#import-tool-syntax (see "Example 1").

**Editing `make_node`**:
```diff
def make_node(id: str,
              iri: str,
              name: str,
              category_label: str,
              update_date: str,
              provided_by: str):
    if '-' in category_label:
        raise ValueError('underscore character detected in category_label argument to function kg2_util.make_node: ' + category_label)
    return {'id': id,
            'iri': iri,
            'name': name,
            'full_name': name,
            'category': convert_biolink_category_to_curie(category_label),
            'category_label': category_label.replace(' ', '_'),
            'description': None,
            'synonym': [],
            'publications': [],
            'creation_date': None,
            'update_date': update_date,
            'deprecated': False,
            'replaced_by': None,
            'provided_by': provided_by,
-           'has_biological_sequence': None}
+           'has_biological_sequence': None,
+           'molecular_weight': None}
```
<figcaption>

 - A `molecular_weight` property with a default value of `None` is added when nodes are created by `make_node`.

</figcaption>
<br \>

**Editing `make_edge`**:

```diff
def make_edge(subject_id: str,
              object_id: str,
              relation_curie: str,
              relation_label: str,
              provided_by: str,
              update_date: str = None):

    edge = {'subject': subject_id,
            'object': object_id,
            'relation_label': relation_label,
            'relation': relation_curie,
            'negated': False,
            'publications': [],
            'publications_info': {},
            'update_date': update_date,
-           'provided_by': provided_by}
+           'provided_by': provided_by,
+           'score': None}
    edge_id = make_edge_key(edge)
    edge["id"] = edge_id
    return edge
```
<figcaption>

 - A `score` property with a default value of `None` is added when edges are created by `make_edge`.

</figcaption>
<br \>

2. Update ETL scripts based on new added properties.
    - For an additional property to be worth the added costs associated with adding it, it is important that multiple sources contribute values to that new node/edge property
    - In some cases, it is relatively easy to update the ETL scripts so that they can contribute values to the new property. This is usually the case in scripts that anticipated the addition of a property later on. For example, `intact_tsv_to_kg_json.py` and `disgenet_tsv_to_kg_json.py` already have score information extracted, because the person who did the ETL anticipated that a score property would be added into KG2 later.
    - In other cases, you may not have any idea if a source has information to contribute to a specific property. In these cases, you will have to go look in the source data file/database. This will both show you if a source has/doesn't have a property and, if so, how to extract it.
        - For XML sources (ex. HMDB, DrugBank, PathWhiz files), I would recommend converting the file (or a subset of the file) to pretty-printed JSON to inspect it. This is often much easier than trying to sort through the raw XML.
        - For TSV/CSV sources (ex. IntAct, DisGeNET, GO Annotations, NCBIGene, DGIdb, JensenLab), I would recommend converting the file into pretty-printed JSON by attaching header terms to their values in each line (creating a list of dictionaries, one for each row)
        - For DAT sources (ex. UniProt, miRBase), I would recommend converting the file into a pretty-printed JSON file as well, using the functions built into those scripts
        - For UMLS and the Ontologies, I wouldn't spend too much time trying to find new properties in that data. Due to the way we import the data (using ontobio), the data structure is pretty rigid and it would be difficult to extract anymore out of it.
        - For SQL-based sources (ex. SemMedDB, Reactome, ChemBL, DrugCentral), I would recommend starting by inspecting their schema's on their respective websites. It takes quite a bit of time to learn a database, so it is important to weigh the costs vs benefits before diving into extracting more information out of these.

**Example 1, `disgenet_tsv_to_kg_json.py` -- adding `score` edge property**:
```diff
def make_edges(input_file: str, test_mode: bool):
    edges = []
    count = 0
    non_befree_count = 0
    with open(input_file, 'r') as input_tsv:
        tsvreader = csv.reader(input_tsv, delimiter='\t')
        for line in tsvreader:
            count += 1
            if count == 1:
                continue
            if test_mode and non_befree_count >= TEST_MODE_LIMIT:
                break
            [subject_id,
             _,
             _,
             _,
             object_id,
             _,
             _,
             _,
             _,
             score,
             evidence_score,
             created_date,
             update_date,
             pmid,
             source] = line
            if source != 'BEFREE':
                non_befree_count += 1
                subject_id = format_id(subject_id,
                                       kg2_util.CURIE_PREFIX_NCBI_GENE)
                object_id = format_id(object_id,
                                      kg2_util.CURIE_PREFIX_UMLS)
                predicate = kg2_util.EDGE_LABEL_BIOLINK_GENE_ASSOCIATED_WITH_CONDITION
                edge = kg2_util.make_edge_biolink(subject_id,
                                                  object_id,
                                                  predicate,
                                                  DISGENET_KB_CURIE,
                                                  update_date)
                publication = kg2_util.CURIE_PREFIX_PMID + ':' + pmid
                edge['publications'] = [publication]
+               edge['score'] = score
                edges.append(edge)
    return edges
```

**Example 2, `drugbank_xml_to_kg_json.py` -- adding `molecular_weight` node property**:
```diff
def format_node(drugbank_id: str,
                description: str,
                name: str,
                update_date: str,
                synonyms: list,
                publications: list,
                category_label: str,
                creation_date: str,
-               sequence: str):
+               sequence: str,
+               molecular_weight: str):
    iri = DRUGBANK_BASE_IRI + drugbank_id
    node_curie = kg2_util.CURIE_PREFIX_DRUGBANK + ":" + drugbank_id
    node_dict = kg2_util.make_node(node_curie,
                                   iri,
                                   name,
                                   category_label,
                                   update_date,
                                   DRUGBANK_KB_CURIE_ID)
    node_dict["synonym"] = synonyms
    node_dict["creation_date"] = creation_date
    node_dict["description"] = description
    node_dict["publications"] = publications
    node_dict["has_biological_sequence"] = sequence
+   node_dict['molecular_weight'] = float(molecular_weight)
    return node_dict


def format_edge(subject_id: str,
                object_id: str,
                predicate_label: str,
                description: str,
                publications: list = None):
    relation_curie = kg2_util.predicate_label_to_curie(predicate_label,
                                                       DRUGBANK_RELATION_CURIE_PREFIX)

    edge = kg2_util.make_edge(subject_id,
                              object_id,
                              relation_curie,
                              predicate_label,
                              DRUGBANK_KB_CURIE_ID,
                              None)

    if description is not None:
        edge["publications_info"] = {"sentence": description}

    if publications is not None:
        edge["publications"] = publications

    return edge


def get_publications(references: list):
    publications = []
    if references is not None:
        if references["articles"] is not None:
            if references["articles"]["article"] is not None:
                for publication in references["articles"]["article"]:
                    if isinstance(publication, dict) and \
                       publication["pubmed-id"] is not None:
                        publications.append(kg2_util.CURIE_PREFIX_PMID +
                                            ':' + publication["pubmed-id"])

    return publications


def get_SMILES(calculated_properties: dict):
    if calculated_properties is not None and isinstance(calculated_properties, dict):
        properties = calculated_properties['property']
        if properties is not None:
            if isinstance(properties, list):
                for property in properties:
                    if property['kind'] == "SMILES":
                        return property['value']
            if isinstance(properties, dict):
                if properties['kind'] == "SMILES":
                    return properties['value']
+
+
+def get_molecular_weight(experimental_properties: dict):
+   if experimental_properties is not None and isinstance(experimental_properties, dict):
+       properties = experimental_properties['property']
+       if properties is not None:
+           if isinstance(properties, list):
+               for property in properties:
+                   if property['kind'] == 'Molecular Weight':
+                       return property['value'], property['source']
+           if isinstance(properties, dict):
+               if properties['kind'] == 'Molecular Weight':
+                   return properties['value'], properties['source']
+   return None, None
+

def make_node(drug: dict):
    drugbank_id = get_drugbank_id(drug)
    synonyms = []
    drug_type = drug["@type"]
    if drug_type == TYPE_SMALL_MOLECULE:
        category = kg2_util.BIOLINK_CATEGORY_SMALL_MOLECULE
    elif drug_type == TYPE_BIOTECH:
        category = kg2_util.BIOLINK_CATEGORY_MOLECULAR_ENTITY
    else:
        print(f"Unknown type: {drug_type} for drug ID: {drugbank_id}; treating as chemical entity",
              file=sys.stderr)
        category = kg2_util.BIOLINK_CATEGORY_CHEMICAL_ENTITY
    if drug["synonyms"] is not None:
        if drug["synonyms"]["synonym"] is not None:
            for synonym in drug["synonyms"]["synonym"]:
                if isinstance(synonym, dict):
                    synonyms.append(synonym["#text"])
    publications = get_publications(drug["general-references"])
    smiles = get_SMILES(drug.get('calculated-properties', None)) # Per Issue #1273, if desired down the road
+   molecular_weight, molecular_weight_source = get_molecular_weight(drug.get('experimental-properties', None))
    node = None
    description = drug["description"]
    if description is not None:
        description = description.replace('\n', ' ').replace('\r', ' ')
    if len(drugbank_id) > 0:
        node = format_node(drugbank_id=drugbank_id,
                           description=description,
                           name=drug["name"],
                           update_date=drug["@updated"],
                           synonyms=synonyms,
                           publications=publications,
                           category_label=category,
                           creation_date=drug["@created"],
-                          sequence=smiles)
+                          sequence=smiles,
+                          molecular_weight=molecular_weight)
    return node
```

3. Update `kg2_util.py` merge dictionary code (if adding a node property) or `filter_kg_and_remap_predicates.py` merge code (if adding an edge property).

**Example 1, node merging**:
```diff
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
                        if key == 'update_date':
                            # Use the longer of the two update-date fields
                            #   NOTE: this is not ideal; better to have actual
                            #         dates (and not strings) so we can use the
                            #         most recent date (see issue #980)
                            if len(value) > len(stored_value):
                                ret_dict[key] = value
                        elif key == 'description':
                            ret_dict[key] = stored_value + '; ' + value
                        elif key == 'ontology node type':
                            log_message("warning:  for key: " + key + ", dropping second value: " + value + '; keeping first value: ' + stored_value,
                                        output_stream=sys.stderr)
                            ret_dict[key] = stored_value
                        elif key == 'provided_by':
                            if value.endswith('/STY'):
                                ret_dict[key] = value
                        elif key == 'category_label':
                            if biolink_depth_getter is not None:
                                depth_x = biolink_depth_getter(CURIE_PREFIX_BIOLINK + ':' + convert_snake_case_to_camel_case(stored_value, uppercase_first_letter=True))
                                depth_y = biolink_depth_getter(CURIE_PREFIX_BIOLINK + ':' + convert_snake_case_to_camel_case(value, uppercase_first_letter=True))
                                if depth_y is not None:
                                    if depth_x is not None:
                                        if depth_y > depth_x:
                                            ret_dict[key] = value
                                    else:
                                        ret_dict[key] = value
                            else:
                                if 'named_thing' != value:
                                    if stored_value == 'named_thing':
                                        ret_dict[key] = value
                                    else:
                                        log_message(message="inconsistent category_label information; keeping original category_label " + stored_value +
                                                    " and discarding new category_label " + value,
                                                    ontology_name=str(x.get('provided_by', 'provided_by=UNKNOWN')),
                                                    node_curie_id=x.get('id', 'id=UNKNOWN'),
                                                    output_stream=sys.stderr)
                                continue
                        elif key == 'category':
                            if biolink_depth_getter is not None:
                                depth_x = biolink_depth_getter(stored_value)
                                depth_y = biolink_depth_getter(value)
                                if depth_y is not None:
                                    if depth_x is not None:
                                        if depth_y > depth_x:
                                            ret_dict[key] = value
                                    else:
                                        ret_dict[key] = value
                            else:
                                if not value.endswith('NamedThing'):
                                    if stored_value.endswith('NamedThing'):
                                        ret_dict[key] = value
                                    else:
                                        log_message(message="inconsistent category information; keeping original category " + stored_value +
                                                    " and discarding new category " + value,
                                                    ontology_name=str(x.get('provided_by', 'provided_by=UNKNOWN')),
                                                    node_curie_id=x.get('id', 'id=UNKNOWN'),
                                                    output_stream=sys.stderr)
                                continue
                        elif key == 'name' or key == 'full_name':
                            if value.replace(' ', '_') != stored_value.replace(' ', '_'):
                                stored_desc = ret_dict.get('description', None)
                                new_desc = y.get('description', None)
                                if stored_desc is not None and new_desc is not None:
                                    if len(new_desc) > len(stored_desc):
                                        ret_dict[key] = value
                                elif new_desc is not None:
                                    ret_dict[key] = value
                                    log_message(message='Warning: for ' + x.get('id', 'id=UNKNOWN') + ' original name of ' + stored_value +
                                                ' is being overwritten to ' + value,
                                                output_stream=sys.stderr)
                        elif key == 'has_biological_sequence':
                            if stored_value is None and value is not None:
                                ret_dict[key] = value
+                       elif key == 'molecular_weight':
+                           # I'm not sure if this is exactly what we'd want to happen in a merge for this. This is strictly an example of the type of edits that need to be made.
+                           if stored_value is None and value is not None:
+                               ret_dict[key] = value
+                           elif stored_value is not None and value is not None and stored_value != value:
+                               if int(stored_value) == int(value):
+                                   ret_dict[key] = int(stored_value)
+                               else:
+                                   ret_dict[key] = None
                        else:
                            log_message("warning:  for key: " + key + ", dropping second value: " + value + '; keeping first value: ' + stored_value,
                                        output_stream=sys.stderr)
                elif type(value) == list and type(stored_value) == list:
                    if key != 'synonym':
                        ret_dict[key] = sorted(list(set(value + stored_value)))
                    else:
                        if len(stored_value) > 0:
                            first_element = {stored_value[0]}
                        elif len(value) > 0 and len(stored_value) == 0:
                            first_element = {value[0]}
                        else:
                            first_element = set()
                        ret_dict[key] = list(first_element) + sorted(filter(None, list(set(value + stored_value) - first_element)))
                elif type(value) == list and type(stored_value) == str:
                    ret_dict[key] = sorted(list(set(value + [stored_value])))
                elif type(value) == str and type(stored_value) == list:
                    ret_dict[key] = sorted(list(set([value] + stored_value)))
                elif type(value) == dict and type(stored_value) == dict:
                    ret_dict[key] = merge_two_dicts(value, stored_value, biolink_depth_getter)
                elif key == 'deprecated' and type(value) == bool:
                    ret_dict[key] = True  # special case for deprecation; True always trumps False for this property
                else:
                    log_message(message="invalid type for key: " + key,
                                ontology_name=str(x.get('provided_by', 'provided_by=UNKNOWN')),
                                node_curie_id=x.get('id', 'id=UNKNOWN'),
                                output_stream=sys.stderr)
                    assert False
    return ret_dict
```

**Example 2, edge merging**:
```diff
        existing_edge = new_edges.get(edge_key, None)
        if existing_edge is not None:
            existing_edge['provided_by'] = sorted(list(set(existing_edge['provided_by'] + edge_dict['provided_by'])))
            existing_edge['publications'] += edge_dict['publications']
            existing_edge['publications_info'].update(edge_dict['publications_info'])
+           existing_edge['score'] = (existing_edge['score'] + edge_dict['score']) / 2 # This is an example, not necessarily how score merging should be handled
        else:
            new_edges[edge_key] = edge_dict
```

4. Update `kg_json_to_tsv.py`.

 - If the new property is of a list type, make sure to accomodate accordingly in `kg_json_to_tsv.py`
    - The header should contain the `[]` symbol after the type (ex. `synonym:string[]`) to indicate that it is an array.
    - The Python list should be turned into a semi-colon delimited list (see the `--array-delimiter` command line option for `neo4j-admin import`) using code like this: `str(value).replace("', '", "; ").replace("'", "").replace("[", "").replace("]", "")`. See below for it in use:
     ```Python
            elif key == "synonym":
                value = truncate_node_synonyms_if_too_large(node[key], node['id'])
                value = str(value).replace("', '", "; ").replace("'", "").replace("[", "").replace("]", "")
            elif key == "publications":
                value = str(node[key]).replace("', '", "; ").replace("'", "").replace("[", "").replace("]", "")
    ```

**Example 1, updating edge properties**:
```diff
def check_all_edges_have_same_set(edgekeys_list):
    """
    :param edgekeys_list: A list containing keys for an edge
    """
    # Supported_ls is a list of properties that edges can have
    supported_ls = ["relation_label",
                    "negated",
                    "object",
                    "provided_by",
                    "publications",
                    "publications_info",
                    "relation",
                    "subject",
                    "update_date",
                    "predicate",
                    "predicate_label",
-                   "id"]
+                   "id",
+                   "score"]
    for edgelabel in edgekeys_list:
        if edgelabel not in supported_ls:
            raise ValueError("relation_label not in supported list: " + edgelabel)

...

def edges(graph, output_file_location):
    """
    :param graph: A dictionary containing KG2
    :param output_file_location: A string containing the path to the
                                TSV output directory
    """
    # Generate list of output file names for the edges TSV files
    edges_file = output_files(output_file_location, "edges")

    # Create dictionary of edges from KG2
    edges = graph["edges"]

    # Open output TSV files
    tsvfile = open(edges_file[0], 'w+')
    tsvfile_h = open(edges_file[1], 'w+')

    # Set loop (edge counter) to zero
    loop = 0

    # Set up TSV files to be written to
    tsvwrite = tsv.writer(tsvfile, delimiter="\t", quoting=tsv.QUOTE_MINIMAL)
    tsvwrite_h = tsv.writer(tsvfile_h, delimiter="\t",
                            quoting=tsv.QUOTE_MINIMAL)
    for edge in edges:
        # Inrease edge counter by one each loop
        loop += 1

        # Add all edge property label to a list in the same order and test
        # to make sure they are the same
        edgekeys = list(sorted(edge.keys()))
        check_all_edges_have_same_set(edgekeys)

        # Add an extra property of "predicate" to the list so that predicates
        # can be a property and a label
        edgekeys.append('predicate')
        edgekeys.append('subject')
        edgekeys.append('object')

        # Create list for values of edge properties to be added to
        vallist = []
        for key in edgekeys:
            # Add the value for each edge property to the value list
            # and limit the size of the publications_info dictionary
            # to avoid Neo4j buffer size error
            value = edge[key]
            if key == "publications_info":
                value = limit_publication_info_size(key, value)
            elif key == 'provided_by':
                value = str(value).replace("', '", "; ").replace("['", "").replace("']", "")
            elif key == 'relation_label':  # fix for issue number 473 (hyphens in relation_labels)
                value = value.replace('-', '_').replace('(', '').replace(')', '')
            elif key == 'publications':
                value = str(value).replace("', '", "; ").replace("'", "").replace("[", "").replace("]", "")
            vallist.append(value)

        # Add the edge property labels to the edge header TSV file
        # But only for the first edge
        if loop == 1:
            edgekeys = no_space('provided_by', edgekeys, 'provided_by:string[]')
            edgekeys = no_space('predicate', edgekeys, 'predicate:TYPE')
            edgekeys = no_space('subject', edgekeys, ':START_ID')
            edgekeys = no_space('object', edgekeys, ':END_ID')
            edgekeys = no_space('publications', edgekeys, "publications:string[]")
+           edgekeys = no_space('score', edgekeys, 'score:float')
            tsvwrite_h.writerow(edgekeys)
        tsvwrite.writerow(vallist)

    # Close the TSV files to prevent a memory leak
    tsvfile.close()
    tsvfile_h.close()
```
**Example 2, updating node properties**
```diff
def nodes(graph, output_file_location):
    """
    :param graph: A dictionary containing KG2
    :param output_file_location: A string containing the
                                path to the TSV output directory
    """
    # Generate list of output file names for the nodes TSV files
    nodes_file = output_files(output_file_location, "nodes")

    # Create dictionary of nodes from KG2
    nodes = graph["nodes"]

    # Open output TSV files
    tsvfile = open(nodes_file[0], 'w+')
    tsvfile_h = open(nodes_file[1], 'w+')

    # Set loop (node counter) to zero
    loop = 0

    # Set up TSV files to be written to
    tsvwrite = tsv.writer(tsvfile, delimiter="\t",
                          quoting=tsv.QUOTE_MINIMAL)
    tsvwrite_h = tsv.writer(tsvfile_h, delimiter="\t",
                            quoting=tsv.QUOTE_MINIMAL)

    # Set single loop to zero and get list of node properties, which will go
    # in the header, to compare other nodes to
    single_loop = 0
    for node in nodes:
        single_loop += 1
        if single_loop == 1:
            nodekeys_official = list(sorted(node.keys()))
            nodekeys_official.append("category")

    for node in nodes:
        # Inrease node counter by one each loop
        loop += 1

        # Add all node property labels to a list in the same order
        nodekeys = list(sorted(node.keys()))
        nodekeys.append("category")

        # Create list for values of node properties to be added to
        vallist = []

        # Set index in list of node properties to zero, to be iterated through
        key_count = 0
        for key in nodekeys:
            if key != nodekeys_official[key_count]:
                # Add a property from the header list of node properties
                # if it doesn't exist and make the value for that property " "
                nodekeys.insert(key_count, nodekeys_official[key_count])
                value = " "
            elif key == "synonym":
                value = truncate_node_synonyms_if_too_large(node[key], node['id'])
                value = str(value).replace("', '", "; ").replace("'", "").replace("[", "").replace("]", "")
            elif key == "publications":
                value = str(node[key]).replace("', '", "; ").replace("'", "").replace("[", "").replace("]", "")
            elif key == "description" and node[key] is not None:
                value = shorten_description_if_too_large(node[key], node['id'])
            else:
                # If the property does exist, assign the property value
                value = node[key]
            # Add the value of the property to the property value list
            vallist.append(value)

            # Increase the index count by one
            key_count += 1

        # Add the edge property labels to the edge header TSV file
        # But only for the first edge
        if loop == 1:
            nodekeys = no_space('id', nodekeys, 'id:ID')
            nodekeys = no_space('publications', nodekeys, "publications:string[]")
            nodekeys = no_space('synonym', nodekeys, "synonym:string[]")
            nodekeys = no_space('category', nodekeys, ':LABEL')
+           nodekeys = no_space('molecular_weight', nodekeys, 'molecular_weight:float')
            tsvwrite_h.writerow(nodekeys)
        tsvwrite.writerow(vallist)

    # Close the TSV files to prevent a memory leak
    tsvfile.close()
    tsvfile_h.close()
```

## Post-ETL (Generalized) Property Add

For these steps, I am going to go through what the process would be to add a property after the ETL steps. As an example, I am going to use adding a `knowledge_source` node and edge property. While this may seem specific, the general process should be similar for other properties added post-ETL.

1. Make a mapping file between an existing property or existing properties to the new property/properties.
This will likely be a YAML file. Below is an example snippet for adding the `knowledge_source` property:
```YAML
DGIdb:
    infores_curie: infores:dgidb
    knowledge_type: aggregator_knowledge_source
DisGeNET:
    infores_curie: infores:disgenet
    knowledge_type: aggregator_knowledge_source
DOID:doid.owl:
    infores_curie: infores:disease-ontology
    knowledge_type: knowledge_source
```

2. Edit `filter_kg_and_remap_predicates.py` to assign the new property/properties.
```diff
def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='filter_kg.py: filters and simplifies the KG2 knowledge grpah for the RTX system')
    arg_parser.add_argument('predicateRemapYaml', type=str, help="The YAML file describing how predicates should be remapped to simpler predicates")
+   arg_parser.add_argument('inforesRemapYaml', type=str, help="The YAML file describing how provided_by fields should be remapped to Translator infores curies")
    arg_parser.add_argument('curiesToURIFile', type=str, help="The file mapping CURIE prefixes to URI fragments")
    arg_parser.add_argument('inputFileJson', type=str, help="The input KG2 grah, in JSON format")
    arg_parser.add_argument('outputFileJson', type=str, help="The output KG2 graph, in JSON format")
    arg_parser.add_argument('versionFile', type=str, help="The text file storing the KG2 version")
    arg_parser.add_argument('--test', dest='test', action='store_true', default=False)
    arg_parser.add_argument('--dropSelfEdgesExcept', required=False, dest='drop_self_edges_except', default=None)
    arg_parser.add_argument('--dropNegated', dest='drop_negated', action='store_true', default=False)
    return arg_parser




if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    predicate_remap_file_name = args.predicateRemapYaml
+   infores_remap_file_name = args.inforesRemapYaml
    curies_to_uri_file_name = args.curiesToURIFile
    input_file_name = args.inputFileJson
    output_file_name = args.outputFileJson
    test_mode = args.test
    drop_negated = args.drop_negated
    drop_self_edges_except = args.drop_self_edges_except
    if drop_self_edges_except is not None:
        assert type(drop_self_edges_except) == str
        drop_self_edges_except = set(drop_self_edges_except.split(','))
    predicate_remap_config = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(predicate_remap_file_name))
+   infores_remap_config = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(infores_remap_file_name))
    map_dict = kg2_util.make_uri_curie_mappers(curies_to_uri_file_name)
    [curie_to_uri_expander, uri_to_curie_shortener] = [map_dict['expand'], map_dict['contract']]
    graph = kg2_util.load_json(input_file_name)
    new_edges = dict()
    relation_curies_not_in_config = set()
+   provided_by_curies_not_in_config_nodes = set()
+   provided_by_curies_not_in_config_edges = set()
    record_of_relation_curie_occurrences = {relation_curie: False for relation_curie in
                                            predicate_remap_config.keys()}
    command_set = {'delete', 'keep', 'invert', 'rename'}
    for relation_curie, command in predicate_remap_config.items():
        assert len(command) == 1
        assert next(iter(command.keys())) in command_set
    relation_curies_not_in_nodes = set()
-   nodes_dict = {node['id']: node for node in graph['nodes']}
+   nodes_dict = dict()
+   for node_dict in graph['nodes']:
+       node_id = node_dict['id']
+       provided_by = node_dict['provided_by']
+       infores_curie_dict = infores_remap_config.get(provided_by, None)
+       if infores_curie_dict is None:
+           provided_by_curies_not_in_config_nodes.add(provided_by)
+       else:
+           infores_curie = infores_curie_dict['infores_curie']
+       node_dict['knowledge_source'] = infores_curie
+       nodes_dict[id] = node_dict
    edge_ctr = 0
    for edge_dict in graph['edges']:
        edge_ctr += 1
        if edge_ctr % 1000000 == 0:
            print('processing edge ' + str(edge_ctr) + ' out of ' + str(len(graph['edges'])))
        if drop_negated and edge_dict['negated']:
            continue
        relation_label = edge_dict['relation_label']
        predicate_label = relation_label
        relation_curie = edge_dict['relation']
        predicate_curie = relation_curie
        if record_of_relation_curie_occurrences.get(relation_curie, None) is not None:
            record_of_relation_curie_occurrences[relation_curie] = True
            pred_remap_info = predicate_remap_config.get(relation_curie, None)
        else:
            # there is a relation CURIE in the graph that is not in the config file
            relation_curies_not_in_config.add(relation_curie)
            pred_remap_info = {'keep': None}
        assert pred_remap_info is not None
        invert = False
        get_new_rel_info = False
        if pred_remap_info is None:
            assert relation_curie in relation_curies_not_in_config
        else:
            if 'delete' in pred_remap_info:
                continue
            remap_subinfo = pred_remap_info.get('invert', None)
            if remap_subinfo is not None:
                invert = True
                get_new_rel_info = True
            else:
                remap_subinfo = pred_remap_info.get('rename', None)
                if remap_subinfo is None:
                    assert 'keep' in pred_remap_info
                else:
                    get_new_rel_info = True
        if get_new_rel_info:
            predicate_label = remap_subinfo[0]
            predicate_curie = remap_subinfo[1]
        if invert:
            edge_dict['relation_label'] = 'INVERTED:' + relation_label
            new_object = edge_dict['subject']
            edge_dict['subject'] = edge_dict['object']
            edge_dict['object'] = new_object
        edge_dict['predicate_label'] = predicate_label
        if drop_self_edges_except is not None and \
           edge_dict['subject'] == edge_dict['object'] and \
           predicate_label not in drop_self_edges_except:
            continue  # see issue 743
        edge_dict['predicate'] = predicate_curie
        if predicate_curie not in nodes_dict:
            predicate_curie_prefix = predicate_curie.split(':')[0]
            predicate_uri_prefix = curie_to_uri_expander(predicate_curie_prefix + ':')
            if predicate_uri_prefix == predicate_curie_prefix:
                relation_curies_not_in_nodes.add(predicate_curie)
+       provided_by = edge_dict['provided_by']
+       infores_curie_dict = infores_remap_config.get(provided_by, None)
+       if infores_curie_dict is None:
+           provided_by_curies_not_in_config_edges.add(provided_by)
+       else:
+           infores_curie = infores_curie_dict['infores_curie']
-       edge_dict['provided_by'] = [edge_dict['provided_by']]
+       edge_dict['provided_by'] = [provided_by]
+       edge_dict['knowledge_source'] = [infores_curie]
        edge_key = edge_dict['subject'] + ' /// ' + predicate_label + ' /// ' + edge_dict['object']
        existing_edge = new_edges.get(edge_key, None)
        if existing_edge is not None:
            existing_edge['provided_by'] = sorted(list(set(existing_edge['provided_by'] + edge_dict['provided_by'])))
+           existing_edge['knowledge_source'] = sorted(list(set(existing_edge['knowledge_source'] + edge_dict['knowledge_source'])))
            existing_edge['publications'] += edge_dict['publications']
            existing_edge['publications_info'].update(edge_dict['publications_info'])
        else:
            new_edges[edge_key] = edge_dict
    del graph['edges']
+   del graph['nodes']
+   graph['nodes'] = list(nodes_dict.values())
    del nodes_dict
    graph['edges'] = list(new_edges.values())
    del new_edges
    for relation_curie in record_of_relation_curie_occurrences:
        if not record_of_relation_curie_occurrences[relation_curie]:
            print('relation curie is in the config file but was not used in any edge in the graph: ' + relation_curie, file=sys.stderr)
    for relation_curie in relation_curies_not_in_nodes:
        print('could not find a node for relation curie: ' + relation_curie)
    relation_curies_not_in_config_for_iteration = list(relation_curies_not_in_config)
    for relation_curie_not_in_config in relation_curies_not_in_config_for_iteration:
        if not relation_curie_not_in_config.startswith(kg2_util.CURIE_PREFIX_BIOLINK + ':'):
            print('relation curie is missing from the YAML config file: ' + relation_curie_not_in_config,
                  file=sys.stderr)
        else:
            relation_curies_not_in_config.remove(relation_curie_not_in_config)
+   for provided_by_curies_not_in_config_node in provided_by_curies_not_in_config_nodes:
+       print('provided_by node curie is missing from the YAML config file: ' + provided_by_curies_not_in_config_node,
+              file=sys.stderr)
+   for provided_by_curies_not_in_config_edge in provided_by_curies_not_in_config_edges:
+       print('provided_by node curie is missing from the YAML config file: ' + provided_by_curies_not_in_config_edge,
+              file=sys.stderr)
    if len(relation_curies_not_in_config) > 0:
        print("There are relation curies missing from the yaml config file. Please add them and try again. Exiting.", file=sys.stderr)
        exit(1)
+   if len(provided_by_curies_not_in_config_nodes) > 0:
+       print("There are nodes provided_by curies missing from the yaml config file. Please add them and try again. Exiting.", file=sys.stderr)
+       exit(1)
+   if len(provided_by_curies_not_in_config_edges) > 0:
+       print("There are edges provided_by curies missing from the yaml config file. Please add them and try again. Exiting.", file=sys.stderr)
+       exit(1)
    update_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    version_file = open(args.versionFile, 'r')
    build_name = str
    for line in version_file:
        test_flag = ""
        if test_mode:
            test_flag = "-TEST"
        build_name = "RTX KG" + line.rstrip() + test_flag
        break
    build_node = kg2_util.make_node(kg2_util.CURIE_PREFIX_RTX + ':' + 'KG2',
                                    kg2_util.BASE_URL_RTX + 'KG2',
                                    build_name,
                                    kg2_util.SOURCE_NODE_CATEGORY,
                                    update_date,
                                    kg2_util.CURIE_PREFIX_RTX + ':')
    build_info = {'version': build_node['name'], 'timestamp_utc': build_node['update_date']}
    pprint.pprint(build_info)
    graph["build"] = build_info
    graph["nodes"].append(build_node)
    kg2_util.save_json(graph, output_file_name, test_mode)
    del graph
```

3. Update `kg_json_to_tsv.py`.

Instructions the same as above (see [ETL-Based Property Add Section 4](#etl-based-property-add))

4. Update `run-simplify.sh` and `master-config.shinc`.

If you've updated the parameters of `filter_kg_and_remap_predicates.py`, you will need to update `run-simplify.sh` (which runs that script) to adjust to the new parameters. In addition, you will want to update `master-config.shinc` to include that new parameter.

```diff
if [ -z ${test_suffix+x} ]; then test_suffix=""; fi
BUILD_DIR=~/kg2-build
VENV_DIR=~/kg2-venv
CODE_DIR=~/kg2-code
umls_dir=${BUILD_DIR}/umls
umls_dest_dir=${umls_dir}/META
s3_region=us-west-2
s3_bucket=rtx-kg2
s3_bucket_public=rtx-kg2-public
s3_bucket_versioned=rtx-kg2-versioned
s3_cp_cmd="aws s3 cp --no-progress --region ${s3_region}"
mysql_conf=${BUILD_DIR}/mysql-config.conf
curl_get="curl -s -L -f"
curies_to_categories_file=${CODE_DIR}/curies-to-categories.yaml
curies_to_urls_file=${CODE_DIR}/curies-to-urls-map.yaml
predicate_mapping_file=${CODE_DIR}/predicate-remap.yaml
+infores_mapping_file=${CODE_DIR}/kg2-provided-by-curie-to-infores-curie.yaml
ont_load_inventory_file=${CODE_DIR}/ont-load-inventory${test_suffix}.yaml
umls2rdf_config_master=${CODE_DIR}/umls2rdf-umls.conf
rtx_config_file=RTXConfiguration-config.json
biolink_model_version=2.1.0

```

```diff
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/filter_kg_and_remap_predicates.py ${test_flag} --dropNegated \\
                           --dropSelfEdgesExcept interacts_with,positively_regulates,inhibits,increase \\
-                          ${predicate_mapping_file} ${curies_to_urls_file} ${input_json} ${output_json} \\
+                          ${predicate_mapping_file} ${infores_mapping_file} ${curies_to_urls_file} ${input_json} ${output_json} \\
                           ${local_version_filename}
```

5. (Optional) Add validation script for mapping file.

The purpose of this is to verify our own, local mapping file against Biolink mappings. However, since Biolink doesn't yet contain infores mappings, this will be developed later for this specific example.