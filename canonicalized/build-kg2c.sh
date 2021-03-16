#!/usr/bin/env bash
# This script builds a canonicalized version of KG2. If the path to your clone of the RTX repo is not provided as a
# command line argument, it will assume that directory is located at ~/RTX.
# Usage: build-kg2c.sh [path_to_your_rtx_directory]

set -e

rtx_dir=${1:-~/RTX}

# Rebuild the NodeSynonymizer using the KG2 endpoint specified under the "KG2" slot in RTX/code/configv2.json
cd ${rtx_dir}/code/ARAX/NodeSynonymizer
python3 -u dump_kg2_node_data.py
python3 -u sri_node_normalizer.py --build
python3 -u node_synonymizer.py --build --kg_name=both

# Create the canonicalized KG from the KG2 at the endpoint specified under the "KG2" slot in RTX/code/configv2.json
cd ${rtx_dir}/code/kg2/canonicalized
python3 -u create_kg2c_files.py

# Upload the generated files to S3
tarball_name=kg2c-tsv.tar.gz
json_file_name=kg2c.json
json_lite_file_name=kg2c_lite.json
sqlite_file_name=kg2c.sqlite
tar -czvf ${tarball_name} nodes_c.tsv nodes_c_header.tsv edges_c.tsv edges_c_header.tsv
aws s3 cp --no-progress --region us-west-2 ${tarball_name} s3://rtx-kg2/
gzip -f ${json_file_name}
gzip -f ${json_lite_file_name}
gzip -f ${sqlite_file_name}
aws s3 cp --no-progress --region us-west-2 ${json_file_name}.gz s3://rtx-kg2/
aws s3 cp --no-progress --region us-west-2 ${json_lite_file_name}.gz s3://rtx-kg2/
aws s3 cp --no-progress --region us-west-2 ${sqlite_file_name}.gz s3://rtx-kg2/
