#!/usr/bin/env bash
# extract-hmdb.sh: Download the Human Metabolome Database
# Copyright 2020 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

# Usage: extract-hmdb.sh

echo "================= starting extract-hmdb.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

output_file=hmdb_metabolites

hmdb_link="https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip"

${curl_get} ${hmdb_link} > ${BUILD_DIR}/${output_file}.zip

unzip -o ${BUILD_DIR}/${output_file}.zip -d ${BUILD_DIR}

date
echo "================= finishing extract-hmdb.sh =================="
