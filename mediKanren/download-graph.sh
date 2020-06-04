#!/usr/bin/env bash
# download-graph.sh: Download a csv of the neo4j graph specified in the config.yml file

set -o nounset -o pipefail -o errexit

# Run the neo4j download
python3.7 kgx/neo4j_download.py

# copy over the resulting csvs
mkdir -p mediKanren/biolink/data/rtx_kg2
mv rtx_kg2.edge.csv mediKanren/biolink/data/rtx_kg2/rtx_kg2.edge.csv
mv rtx_kg2.edgeprop.csv mediKanren/biolink/data/rtx_kg2/rtx_kg2.edgeprop.csv
mv rtx_kg2.node.csv mediKanren/biolink/data/rtx_kg2/rtx_kg2.node.csv
mv rtx_kg2.nodeprop.csv mediKanren/biolink/data/rtx_kg2/rtx_kg2.nodeprop.csv

