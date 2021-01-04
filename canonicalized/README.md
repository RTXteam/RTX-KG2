# What is KG2canonicalized?

KG2canonicalized (KG2c) is a lightweight version of KG2 in which synonymous nodes have been collapsed into one. It is built from the 'production' KG2 Neo4j endpoint and uses the [ARAX NodeSynonymizer](https://github.com/RTXteam/RTX/tree/master/code/ARAX/NodeSynonymizer) to determine which nodes are equivalent. 

The Neo4j endpoint for KG2c is accessible at http://kg2canonicalized.rtx.ai:7474/browser/ (contact the maintainer for username and password).

### Schema
Example KG2c node (all nodes have these same properties):
```
{
  "id": "CHEBI:134827",
  "name": "apronal",
  "preferred_type": "chemical_substance",
  "types": [
    "unknown_category",
    "named_thing",
    "chemical_substance"
  ],
  "equivalent_curies": [
    "CUI:C3652934",
    "ATC:N05CM12",
    "CHEBI:134827",
    "CHEMBL.COMPOUND:CHEMBL509282"
  ],
  "publications": [
    "PMID:18834112",
    "PMID:15646539"
  ]
}
```
The node `id` is the 'preferred' curie for the group of synonymous nodes this KG2c node represents (according to the ARAX `NodeSynonymizer`).

Example KG2c edge (all edges have these same properties):
```
{
  "subject": "CHEBI:24433",
  "object": "CUI:C0599078",
  "simplified_edge_label": "has_input",
  "provided_by": [
    "https://skr3.nlm.nih.gov/SemMedDB"
  ],
  "publications": [
    "PMID:3798018"
  ]
}
```
In creating KG2c, edges from the regular KG2 are remapped to use only 'preferred' curies for their `subject` and `object`; edges with the same `subject`, `object`, and `simplified_edge_label` are then merged.

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

(4) Build KG2canonicalized (should take less than 2 hours):
```
cd ~/RTX/code/kg2/canonicalized/
bash -x build-kg2-canonicalized.sh
```
This produces TSV files containing the data (formatted for Neo4j import) and uploads them to the KG2 S3 bucket.

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

(3) Load the latest KG2canonicalized into Neo4j
```
bash -x RTX/code/kg2/canonicalized/tsv-to-neo4j-canonicalized.sh
```

# Contact
## Maintainer
- Amy Glen, Oregon State University (glena@oregonstate.edu)