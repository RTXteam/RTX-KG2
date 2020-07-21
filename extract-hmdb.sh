#!/usr/bin/env bash
# extract-hmdb.sh: Download the Small Molecule Pathway Database
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

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

OUTPUT_FILE=hmdb_metabolites

HMDB_LINK="https://hmdb.ca/system/downloads/current/hmdb_metabolites.zip"

${CURL_GET} ${HMDB_LINK} > ${BUILD_DIR}/${OUTPUT_FILE}.zip

unzip -o ${BUILD_DIR}/${OUTPUT_FILE}.zip -d ${BUILD_DIR}

date
echo "================= finishing extract-hmdb.sh =================="