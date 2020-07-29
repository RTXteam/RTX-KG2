#!/usr/bin/env bash

rtx_dir = ~/RTX

# Rebuild NodeSynonymizer using the latest KG2
cd ${rtx-dir}/data/KGmetadata
python3 dumpdata.py
cd ${rtx-dir}/code/ARAX/NodeSynonymizer
python3 sri_node_normalizer.py --build
python3 node_synonymizer.py --build --kg_name=both

# Create the canonicalized KG from the slim KG
cd ${rtx-dir}/code/kg2
python3 -u create_canonicalized_kg_tsvs.py

# Convert that json file into TSV files and upload to S3 TODO
#tar -czvf kg2-canonicalized-tsv.tar.gz nodes_c.tsv nodes_c_header.tsv edges_c.tsv edges_c_header.tsv
#aws s3 cp --no-progress --region us-west-2 kg2-canonicalized-tsv.tar.gz s3://rtx-kg2/
