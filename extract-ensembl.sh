#!/usr/bin/env bash
# extract-ensembl.sh: download Ensembl datafile of annotated human genes 
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [all|test]"
    exit 2
fi

echo "================= starting extract-ensembl.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

ENSEMBL_RELEASE=97

ENSEMBL_JSON_FILE=${1:-"${BUILD_DIR}/ensembl/ensembl_genes_homo_sapiens.json"}
OUTPUT_DIR=`dirname ${ENSEMBL_JSON_FILE}`

mkdir -p ${OUTPUT_DIR}

${CURL_GET} ftp://ftp.ensembl.org/pub/release-${ENSEMBL_RELEASE}/json/homo_sapiens/homo_sapiens.json > ${ENSEMBL_JSON_FILE}

date
echo  "================= finished extract-ensembl.sh ================="
