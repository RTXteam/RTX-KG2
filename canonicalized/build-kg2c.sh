#!/usr/bin/env bash
# This script builds a canonicalized version of KG2; it requires an ARAX NodeSynonymizer built from the KG2 you intend
# to make this KG2c from. This synonymizer (e.g., node_synonymizer.sqlite) should be in your code/ARAX/NodeSynonymizer
# directory. Your configv2.json must point to the Neo4j endpoint for whatever KG2 version you want to build this
# KG2c from. You must specify which Biolink model version to use (should match that of the KG2 this KG2c is being built
# from).
# Usage: build-kg2c.sh <Biolink model version>

set -e

if [ $# -eq 0 ]  # No arguments were supplied
  then
    echo "You must specify the Biolink Model version to use (e.g., 1.8.1)"
    exit 1
fi
biolink_version=$1

kg2c_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"  # Thanks https://stackoverflow.com/a/246128

# Create a KG2c from the KG2 at the endpoint specified under the "KG2" slot in RTX/code/configv2.json
cd ${kg2c_dir}
python3 -u create_kg2c_files.py

# Compute and save some additional meta info (meta knowledge graph and neighbor counts)
python3 -u record_kg2c_meta_info.py ${biolink_version}

# Upload generated files to S3
tarball_name=kg2c-tsv.tar.gz
json_file_name=kg2c.json
json_lite_file_name=kg2c_lite.json
tar -czvf ${tarball_name} nodes_c.tsv nodes_c_header.tsv edges_c.tsv edges_c_header.tsv
aws s3 cp --no-progress --region us-west-2 ${tarball_name} s3://rtx-kg2/
gzip -f ${json_file_name}
gzip -f ${json_lite_file_name}
aws s3 cp --no-progress --region us-west-2 ${json_file_name}.gz s3://rtx-kg2/
aws s3 cp --no-progress --region us-west-2 ${json_lite_file_name}.gz s3://rtx-kg2/
