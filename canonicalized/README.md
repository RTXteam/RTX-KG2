# What is KG2canonicalized?

KG2canonicalized (KG2c) is a lightweight version of KG2 in which synonymous nodes have been collapsed into one. It is built from the 'production' KG2 Neo4j endpoint and uses the [ARAX NodeSynonymizer](https://github.com/RTXteam/RTX/tree/master/code/ARAX/NodeSynonymizer) to determine which nodes are equivalent. 

The Neo4j endpoint for KG2c is accessible at http://kg2canonicalized2.rtx.ai:7474/browser/ (contact the maintainer for username and password).

### Schema
Example KG2c node:
```
{
  "id": "MONDO:0009433",
  "name": "hypoplastic left heart syndrome 1",
  "category": "biolink:Disease",
  "iri": "http://purl.obolibrary.org/obo/MONDO_0009433",
  "description": "Hypoplastic left heart syndrome results from defective development of the aorta proximal to the entrance of the ductus arteriosus...",
  "all_categories": [
    "biolink:Disease",
    "biolink:PhenotypicFeature"
  ],
  "all_names": [
    "hypoplastic left heart syndrome 1",
    "HYPOPLASTIC LEFT HEART SYNDROME 1; HLHS1",
    "Hypoplastic left heart syndrome 1"
  ],
  "equivalent_curies": [
    "UMLS:C4551854",
    "OMIM:241550",
    "MONDO:0009433"
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

(4) Build KG2c (should take less than 2 hours):
```
cd ~/RTX/code/kg2/canonicalized/
bash -x build-kg2-canonicalized.sh
```
This produces TSV files containing the KG (formatted for Neo4j import) and uploads them to the KG2 S3 bucket. It requires a bit more than 64GB of RAM.

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