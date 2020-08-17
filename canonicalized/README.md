# What is Canonicalized KG2?

Canonicalized KG2 is a lightweight version of KG2 in which synonymous nodes have been collapsed into one. It is built from the 'production' KG2 neo4j endpoint and uses the ARAX `NodeSynonymizer` to determine which nodes are equivalent. 

In Canonicalized KG2, nodes contain the following fields: `id`, `name`, `types`, `preferred_type`, and `equivalent_curies`. Edges contain the following fields: `subject`, `object`, `simplified_edge_label`, and `provided_by`.

The Neo4j endpoint for KG2 Canonicalized is accessible at http://kg2canonicalized.rtx.ai:7474/browser/ (contact the maintainer for username and password).

# Contact
## Maintainer
- Amy Glen, Oregon State University (glena@oregonstate.edu)

# Build Canonicalized KG2

(1) Change directories into your home directory:

`cd ~`

(2) Clone the GitHub repository:

`git clone https://github.com/RTXteam/RTX.git`

(3) Follow step 1 in the [ARAX wiki](https://github.com/RTXteam/RTX/wiki/Dev-info) so that you will be able to build the `NodeSynonymizer`.

(4) Install AWS CLI and configure it:

`sudo apt-get install -y awscli`

`aws configure`

(5) Change directories into the `canonicalized` directory:

`cd ~/RTX/code/kg2/canonicalized/`

(6) Build Canonicalized KG2 (should take less than 3 hours):

`bash -x build-kg2-canonicalized.sh`

# Host Canonicalized KG2 in Neo4j

These instructions assume Neo4j is not already installed and that you are hosting Neo4j on an AWS instance.

(1) Change directories into your home directory.

`cd ~`

(2) Clone the GitHub repository.

`git clone https://github.com/RTXteam/RTX.git`

(3) Setup the instance for Neo4j.

`bash -x RTX/code/kg2/setup-kg2-neo4j.sh`

(4) Load the latest Canonicalized KG2 into Neo4j

`bash -x RTX/code/kg2/canonicalized/tsv-to-neo4j-canonicalized.sh`