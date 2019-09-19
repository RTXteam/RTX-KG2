#!/usr/bin/env bash
# download-graph.sh: Download a csv of the neo4j graph specified in the config.yml file


# Run the neo4j download
python3.7 kgx/neo4j_download.py

# copy over the resulting csvs
mkdir mediKanren/biolink/data/rtx_kg2
mv kgx/rtx_kg2.edge.csv mediKanren/biolink/data/rtx_kg2/rtx_kg2.edge.csv
mv kgx/rtx_kg2.edgeprop.csv mediKanren/biolink/data/rtx_kg2/rtx_kg2.edgeprop.csv
mv kgx/rtx_kg2.node.csv mediKanren/biolink/data/rtx_kg2/rtx_kg2.node.csv
mv kgx/rtx_kg2.nodeprop.csv mediKanren/biolink/data/rtx_kg2/rtx_kg2.nodeprop.csv

