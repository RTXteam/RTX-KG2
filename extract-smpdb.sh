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

OUTPUT_DIR=${1:-"${BUILD_DIR}/smpdb"}
SMPDB_OUTPUT_FILE="pathbank_pathways.csv"
PW_OUTPUT_FILE="pathbank_all_pwml.zip"

mkdir -p ${OUTPUT_DIR}
SMPDB_LINK="https://pathbank.org/downloads/pathbank_all_pathways.csv.zip"
PWML_LINK="https://pathbank.org/downloads/pathbank_all_pwml.zip"
SMPDB_PMIDS_FILE="SMPDB_pubmed_IDs.csv"

${CURL_GET} ${OUTPUT_DIR}/ ${SMPDB_LINK} > ${OUTPUT_DIR}/${SMPDB_OUTPUT_FILE}.zip
${CURL_GET} ${OUTPUT_DIR}/ ${PWML_LINK} > ${OUTPUT_DIR}/${PW_OUTPUT_FILE}

unzip -o ${OUTPUT_DIR}/${SMPDB_OUTPUT_FILE}.zip -d ${OUTPUT_DIR}/
unzip -o -q ${OUTPUT_DIR}/${PW_OUTPUT_FILE} -d ${OUTPUT_DIR}/

for FILE in $(ls ${OUTPUT_DIR}/pathbank_all_pwml)
do
	mv ${OUTPUT_DIR}/pathbank_all_pwml/$FILE ${OUTPUT_DIR}
done

${S3_CP_CMD} s3://${S3_BUCKET}/${SMPDB_PMIDS_FILE} ${OUTPUT_DIR}

date
echo "================= finishing extract-smpdb.sh =================="