#!/usr/bin/env bash
set -e

rtx_dir=${1:-~/RTX}

# Rebuild NodeSynonymizer using the latest KG2
cd ${rtx_dir}/data/KGmetadata
python3 dumpdata.py
cd ${rtx_dir}/code/ARAX/NodeSynonymizer
python3 sri_node_normalizer.py --build
python3 node_synonymizer.py --build --kg_name=both

# Create the canonicalized KG
cd ${rtx_dir}/code/kg2/canonicalized
python3 -u create_canonicalized_kg_tsvs.py

# Upload the TSV files to S3
tar -czvf kg2-canonicalized-tsv.tar.gz nodes_c.tsv nodes_c_header.tsv edges_c.tsv edges_c_header.tsv
aws s3 cp --no-progress --region us-west-2 kg2-canonicalized-tsv.tar.gz s3://rtx-kg2/
