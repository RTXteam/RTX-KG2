#!/usr/bin/env bash
# This script builds a canonicalized version of KG2. If the path to your clone of the RTX repo is not provided as a
# command line argument, it will assume that directory is located at ~/RTX.
# Usage: build-kg2c.sh [path_to_your_rtx_directory]

set -e

rtx_dir=${1:-~/RTX}

# Rebuild the NodeSynonymizer using the KG2 endpoint specified under the "KG2" slot in RTX/code/config.json
cd ${rtx_dir}/data/KGmetadata
python3 dumpdata.py
cd ${rtx_dir}/code/ARAX/NodeSynonymizer
python3 sri_node_normalizer.py --build
python3 node_synonymizer.py --build --kg_name=both

# Create the canonicalized KG from the KG2 at the endpoint specified under the "KG2" slot in RTX/code/config.json
cd ${rtx_dir}/code/kg2/canonicalized
python3 -u create_kg2c_files.py

# Upload the generated TSV files to S3
tarball_name=kg2c-tsv.tar.gz
tar -czvf ${tarball_name} nodes_c.tsv nodes_c_header.tsv edges_c.tsv edges_c_header.tsv
aws s3 cp --no-progress --region us-west-2 ${tarball_name} s3://rtx-kg2/
