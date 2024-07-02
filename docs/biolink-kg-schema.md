# Translator Project knowledge graph schema
## Generated from the Biolink model version 4.2.1
## by the script [`biolink_yaml_to_schema_documentation.py`](biolink_yaml_to_schema_documentation.py)

# Node


*Biolink knowledge graph node*


## Properties


- **`id`** *(uriorcurie)*: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI; **required: True**.

- **`iri`** *(uriorcurie)*: An IRI for an entity. This is determined by the id using expansion rules.; required: False.

- **`category`** *(['uriorcurie'])*: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In a neo4j database this MAY correspond to the neo4j label tag. In an RDF database it should be a biolink model class URI. This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`. In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}; **required: True**.

- **`type`** *(['string'])*: ; semantic URI: rdf:type; required: False.

- **`name`** *(string)*: A human-readable name for an attribute or entity.; semantic URI: rdfs:label; required: False.

- **`description`** *(string)*: a human-readable description of an entity; semantic URI: dct:description; required: False.

- **`has_attribute`** *(['attribute'])*: connects any entity to an attribute; required: False.

- **`deprecated`** *(boolean)*: A boolean flag indicating that an entity is no longer considered current or valid.; required: False.

# Edge


*Biolink knowledge graph edge*


## Properties


- **`id`** *(uriorcurie)*: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI; **required: True**.

- **`iri`** *(uriorcurie)*: An IRI for an entity. This is determined by the id using expansion rules.; required: False.

- **`category`** *(['uriorcurie'])*: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class. In a neo4j database this MAY correspond to the neo4j label tag. In an RDF database it should be a biolink model class URI. This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`. In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}; required: False.

- **`type`** *(['string'])*: ; semantic URI: rdf:type; required: False.

- **`name`** *(string)*: A human-readable name for an attribute or entity.; semantic URI: rdfs:label; required: False.

- **`description`** *(string)*: a human-readable description of an entity; semantic URI: dct:description; required: False.

- **`has_attribute`** *(['attribute'])*: connects any entity to an attribute; required: False.

- **`deprecated`** *(boolean)*: A boolean flag indicating that an entity is no longer considered current or valid.; required: False.

- **`subject`** *(node-id)*: connects an association to the subject of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.; semantic URI: rdf:subject; **required: True**.

- **`predicate`** *(uriorcurie)*: A high-level grouping for the relationship type. AKA minimal predicate. This is analogous to category for nodes.; semantic URI: rdf:predicate; **required: True**.

- **`object`** *(node-id)*: connects an association to the object of the association. For example, in a gene-to-phenotype association, the gene is subject and phenotype is object.; semantic URI: rdf:object; **required: True**.

- **`negated`** *(boolean)*: if set to true, then the association is negated i.e. is not true; required: False.

- **`qualifier`** *(unknown)*: grouping slot for all qualifiers on an edge.  useful for testing compliance with association classes; required: False.

- **`qualifiers`** *(['ontology class'])*: connects an association to qualifiers that modify or qualify the meaning of that association; required: False.

- **`publications`** *(['publication'])*: One or more publications that report the statement expressed in an Association, or provide information used as evidence supporting this statement.; required: False.

- **`has_evidence`** *([['eco']])*: connects an association to an instance of supporting evidence; required: False.

- **`knowledge_source`** *(unknown)*: An Information Resource from which the knowledge expressed in an Association was retrieved, directly or indirectly. This can be any resource through which the knowledge passed on its way to its currently serialized form. In practice, implementers should use one of the more specific subtypes of this generic property.; required: False.

- **`primary_knowledge_source`** *(unknown)*: The most upstream source of the knowledge expressed in an Association that an implementer can identify.  Performing a rigorous analysis of upstream data providers is expected; every effort is made to catalog the most upstream source of data in this property.  Only one data source should be declared primary in any association.  "aggregator knowledge source" can be used to capture non-primary sources.; required: False.

- **`aggregator_knowledge_source`** *(['unknown'])*: An intermediate aggregator resource from which knowledge expressed in an Association was retrieved downstream of the original source, on its path to its current serialized form.; required: False.

- **`knowledge_level`** *(KnowledgeLevelEnum)*: Describes the level of knowledge expressed in a statement, based on the reasoning or analysis methods used to generate the statement, or the scope or specificity of what the statement expresses to be true.; **required: True**.

- **`agent_type`** *(AgentTypeEnum)*: Describes the high-level category of agent who originally generated a  statement of knowledge or other type of information.; **required: True**.

- **`timepoint`** *(time)*: a point in time; required: False.

- **`original_subject`** *(unknown)*: used to hold the original subject of a relation (or predicate) that an external knowledge source uses before transformation to match the biolink-model specification.; required: False.

- **`original_predicate`** *(uriorcurie)*: used to hold the original relation/predicate that an external knowledge source uses before transformation to match the biolink-model specification.; required: False.

- **`original_object`** *(unknown)*: used to hold the original object of a relation (or predicate) that an external knowledge source uses before transformation to match the biolink-model specification.; required: False.

- **`subject_category`** *(ontology class)*: Used to hold the biolink class/category of an association. This is a denormalized field used primarily in the SQL serialization of a knowledge graph via KGX.; required: False.

- **`object_category`** *(ontology class)*: Used to hold the biolink class/category of an association. This is a denormalized field used primarily in the SQL serialization of a knowledge graph via KGX.; required: False.

- **`subject_closure`** *(['unknown'])*: Used to hold the subject closure of an association. This is a denormalized field used primarily in the SQL serialization of a knowledge graph via KGX.; required: False.

- **`object_closure`** *(['unknown'])*: Used to hold the object closure of an association. This is a denormalized field used primarily in the SQL serialization of a knowledge graph via KGX.; required: False.

- **`subject_category_closure`** *(['ontology class'])*: Used to hold the subject category closure of an association. This is a denormalized field used primarily in the SQL serialization of a knowledge graph via KGX.; required: False.

- **`object_category_closure`** *(['ontology class'])*: Used to hold the object category closure of an association. This is a denormalized field used primarily in the SQL serialization of a knowledge graph via KGX.; required: False.

- **`subject_namespace`** *(string)*: Used to hold the subject namespace of an association. This is a denormalized field used primarily in the SQL serialization of a knowledge graph via KGX.; required: False.

- **`object_namespace`** *(string)*: Used to hold the object namespace of an association. This is a denormalized field used primarily in the SQL serialization of a knowledge graph via KGX.; required: False.

- **`subject_label_closure`** *(['string'])*: Used to hold the subject label closure of an association. This is a denormalized field used primarily in the SQL serialization of a knowledge graph via KGX.; required: False.

- **`object_label_closure`** *(['string'])*: Used to hold the object label closure of an association. This is a denormalized field used primarily in the SQL serialization of a knowledge graph via KGX.; required: False.

- **`retrieval_source_ids`** *(['retrieval source'])*: A list of retrieval sources that served as a source of knowledge expressed in an Edge, or a source of data used to generate this knowledge.; required: False.

# JSON Example
To see an example JSON serialization of a simple KG, refer to the document [KGX Format](https://github.com/biolink/kgx/blob/master/specification/kgx-format.md).
