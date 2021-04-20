#!/usr/bin/env bash
# This script builds a canonicalized version of KG2; it requires an ARAX NodeSynonymizer built from the KG2 you intend
# to make this KG2c from. This synonymizer (e.g., node_synonymizer.sqlite) should be in your code/ARAX/NodeSynonymizer
# directory. The KG2c will be built from whatever KG2 version your configv2.json file points to.
# Usage: build-kg2c.sh

set -e

kg2c_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"  # Thanks https://stackoverflow.com/a/246128

# Create a KG2c from the KG2 at the endpoint specified under the "KG2" slot in RTX/code/configv2.json
cd ${kg2c_dir}
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
