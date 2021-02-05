# Node

*Biolink knowledge graph node*

## Properties

- **`id`** *(uriorcurie)*: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI; **required: True**.
- **`iri`** *(uriorcurie)*: An IRI for an entity. This is determined by the id using expansion rules.; **required: False**.
- **`category`** *(['uriorcurie'])*: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.In a neo4j database this MAY correspond to the neo4j label tag.In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `bl:Protein`, `bl:GeneProduct`, `bl:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {bl:GenomicEntity, bl:MolecularEntity, bl:NamedThing}; **required: False**.
- **`type`** *(string)*: ; **required: False**.
- **`name`** *(string)*: A human-readable name for an attribute or entity.; **required: False**.
- **`description`** *(string)*: a human-readable description of an entity; **required: False**.
- **`source`** *(string)*: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.; **required: False**.
- **`provided_by`** *(['agent'])*: connects an association to the agent (person, organization or group) that provided it; **required: False**.
- **`has_attribute`** *(['attribute'])*: connects any entity to an attribute; **required: False**.
