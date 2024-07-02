#!/usr/bin/env bash
# remove-uncompressed-output-files.sh: script to be run after a successful build to save on storage costs. The files are kept after zipping in finish-snakemake.sh to allow for partial rebuilds of rules after Merge. See #1104.
# Copyright 2020 Stephen A. Ramsey
# Author Lindsey Kvarfordt


set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

echo "================= starting remove-uncompressed-files.sh =================="
date

rm -f ${BUILD_DIR}/kg2.json

rm -f ${BUILD_DIR}/kg2-simplified.json
rm -f ${BUILD_DIR}/kg2-simplified-nodes.json
rm -f ${BUILD_DIR}/kg2-nodes.json
rm -f ${BUILD_DIR}/kg2-orphans-edges.json
rm -f ${BUILD_DIR}/kg2-slim.json


date
echo "================ script finished ============================"
