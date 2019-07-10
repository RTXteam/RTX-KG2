#!/usr/bin/env bash
# extract-unichem.sh: download UniChem and extract TSV of (chembl,chebi) pairs
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_tsv_file>"
    exit 2
fi

OUTPUT_TSV_FILE=${1:-"${BUILD_DIR}/unichem/chembl-to-chebi.tsv"}

echo "================= starting build-chembl.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc
UNICHEM_DIR=`dirname ${OUTPUT_TSV_FILE}`
UNICHEM_VER=232
UNICHEM_FTP_SITE=ftp://ftp.ebi.ac.uk/pub/databases/chembl/UniChem/data

mkdir -p ${UNICHEM_DIR}

${CURL_GET} ${UNICHEM_FTP_SITE}/oracleDumps/UDRI${UNICHEM_VER}/UC_XREF.txt.gz > ${UNICHEM_DIR}/UC_XREF.txt.gz
${CURL_GET} ${UNICHEM_FTP_SITE}/oracleDumps/UDRI${UNICHEM_VER}/UC_SOURCE.txt.gz > ${UNICHEM_DIR}/UC_SOURCE.txt.gz

CHEMBL_SRC_ID=`zcat ${UNICHEM_DIR}/UC_SOURCE.txt.gz | awk '{if ($2 == "chembl") {printf "%s", $1}}'`
CHEBI_SRC_ID=`zcat ${UNICHEM_DIR}/UC_SOURCE.txt.gz | awk '{if ($2 == "chebi") {printf "%s", $1}}'`

zcat ${UNICHEM_DIR}/UC_XREF.txt.gz | awk '{if ($2 == '${CHEBI_SRC_ID}') {print $1 "\tCHEBI:" $3}}' | sort -k1 > ${UNICHEM_DIR}/chebi.txt
zcat ${UNICHEM_DIR}/UC_XREF.txt.gz | awk '{if ($2 == '${CHEMBL_SRC_ID}') {print $1 "\tCHEMBL.COMPOUND:" $3}}' | sort -k1 > ${UNICHEM_DIR}/chembl.txt

join ${UNICHEM_DIR}/chembl.txt ${UNICHEM_DIR}/chebi.txt | sed 's/ /\t/g' | cut -f2-3 > ${OUTPUT_TSV_FILE}

date
echo "================= script finished ================="
