#!/usr/bin/env bash
# extract-smpdb.sh: Download the Small Molecule Pathway Database
# Copyright 2019 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output-dir>"
    exit 2
fi

# Usage: extract-smpdb.sh <output-dir>

echo "================= starting extract-smpdb.sh =================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

OUTPUT_DIR=${1:-"${BUILD_DIR}/smpdb/"}
OUTPUT_FILE=smpdb_pathways.csv

mkdir -p ${OUTPUT_DIR}
SMPDB_LINK="https://smpdb.ca/downloads/smpdb_pathways.csv.zip"

${CURL_GET} ${SMPDB_LINK} > ${OUTPUT_DIR}${OUTPUT_FILE}.zip

unzip ${OUTPUT_DIR}${OUTPUT_FILE}.zip
mv ${OUTPUT_FILE} ${OUTPUT_DIR}

date
echo "================= finishing extract-smpdb.sh =================="