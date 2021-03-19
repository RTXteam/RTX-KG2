# What is KG2canonicalized?

KG2canonicalized (KG2c) is a lightweight version of KG2 in which synonymous nodes have been merged. It is built from the regular KG2's Neo4j endpoint and uses the [ARAX NodeSynonymizer](https://github.com/RTXteam/RTX/tree/master/code/ARAX/NodeSynonymizer) to determine which nodes are equivalent. 

The Neo4j endpoint for KG2c is accessible at http://kg2canonicalized2.rtx.ai:7474/browser/ (contact the maintainer for username and password).

### Schema
Example KG2c node:
```
{
  "id": "MONDO:0000710",
  "name": "gastroduodenal Crohn disease",
  "category": "biolink:Disease",
  "iri": "http://purl.obolibrary.org/obo/MONDO_0000710",
  "description": "An inflammatory bowel disease characterized by inflammation located_in stomach and located_in duodenum, has_symptom nausea, has_symptom vomiting, has_symptom weight loss and has_symptom loss of appetite.",
    "all_categories": [
    "biolink:Disease"
  ],
  "expanded_categories": [
    "biolink:BiologicalEntity",
    "biolink:Disease",
    "biolink:DiseaseOrPhenotypicFeature",
    "biolink:NamedThing",
    "biolink:PhenotypicFeature"
  ],
  "equivalent_curies": [
    "DOID:0060191",
    "MONDO:0000710"
  ],
  "all_names": [
    "gastroduodenal Crohn disease",
    "gastroduodenal Crohn's disease"
  ],
  "publications": [
    "PMID:12769447",
    "http://en.wikipedia.org/wiki/crohn%27s_disease",
    "http://www.bidmc.org/centers-and-departments/departments/digestive-disease-center/inflammatory-bowel-disease-program/crohns-disease/what-are-the-types-of-crohns-disease.aspx",
    "http://www.ccfa.org/what-are-crohns-and-colitis/what-is-crohns-disease/types-of-crohns-disease.htm"
  ]
}
```
The node `id` is the 'preferred' curie for the group of synonymous nodes this KG2c node represents (according to the ARAX `NodeSynonymizer`). Similarly, the node `category` and `name` are the 'preferred' category/name, according to the `NodeSynonymizer`.

Example KG2c edge:
```
{
  "subject": "UMLS:C0180600",
  "object": "MONDO:0000001",
  "predicate": "treats",
  "provided_by": [
    "SEMMEDDB:"
  ],
  "publications": [
    "PMID:14477543",
    "PMID:4266234"
  ]
}
```
In creating KG2c, edges from the regular KG2 are remapped to use only 'preferred' curies for their `subject` and `object`; edges with the same `subject`, `object`, and `predicate` are then merged.

# How to create it

### Build KG2canonicalized

(1) Clone the GitHub repository into your home directory:
```
cd ~
git clone https://github.com/RTXteam/RTX.git
```

(2) Follow step 1 in the [ARAX wiki](https://github.com/RTXteam/RTX/wiki/Dev-info) so that you will be able to build the `NodeSynonymizer`

(3) Install AWS CLI and configure it:
```
sudo apt-get install -y awscli
aws configure
```

(4) Build KG2c (should take around 4 hours):
```
cd ~/RTX/code/kg2/canonicalized/
bash -x build-kg2c.sh
```
This produces TSV files containing the KG (formatted for Neo4j import) and uploads them to the KG2 S3 bucket. It requires around 80GB of RAM.

### Host KG2canonicalized in Neo4j

These instructions assume Neo4j is not already installed and that you are hosting Neo4j on an AWS instance.

(1) Clone the GitHub repository into your home directory
```
cd ~
git clone https://github.com/RTXteam/RTX.git
```

(2) Setup the instance for Neo4j
```
bash -x RTX/code/kg2/setup-kg2-neo4j.sh
```

(3) Load the latest KG2c into Neo4j
```
bash -x RTX/code/kg2/canonicalized/tsv-to-neo4j-canonicalized.sh
```

# Contact
## Maintainer
- Amy Glen, Oregon State University (glena@oregonstate.edu)