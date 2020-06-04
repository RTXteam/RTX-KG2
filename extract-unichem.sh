#!/usr/bin/env bash
# extract-unichem.sh: download UniChem and extract TSV of (chembl,chebi) pairs
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_tsv_file>"
    exit 2
fi

echo "================= starting build-unichem.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc
OUTPUT_TSV_FILE=${1:-"${BUILD_DIR}/unichem/chembl-to-curies.tsv"}
UNICHEM_DIR=${BUILD_DIR}/unichem
UNICHEM_OUTPUT_DIR=`dirname ${OUTPUT_TSV_FILE}`
UNICHEM_VER=280
UNICHEM_FTP_SITE=ftp://ftp.ebi.ac.uk/pub/databases/chembl/UniChem/data

rm -r -f ${UNICHEM_DIR}
mkdir -p ${UNICHEM_DIR}
mkdir -p ${UNICHEM_OUTPUT_DIR}

${CURL_GET} ${UNICHEM_FTP_SITE}/oracleDumps/UDRI${UNICHEM_VER}/UC_XREF.txt.gz > ${UNICHEM_DIR}/UC_XREF.txt.gz
${CURL_GET} ${UNICHEM_FTP_SITE}/oracleDumps/UDRI${UNICHEM_VER}/UC_SOURCE.txt.gz > ${UNICHEM_DIR}/UC_SOURCE.txt.gz
${CURL_GET} ${UNICHEM_FTP_SITE}/oracleDumps/UDRI${UNICHEM_VER}/UC_RELEASE.txt.gz > ${UNICHEM_DIR}/UC_RELEASE.txt.gz

CHEMBL_SRC_ID=`zcat ${UNICHEM_DIR}/UC_SOURCE.txt.gz | awk '{if ($2 == "chembl") {printf "%s", $1}}'`
CHEBI_SRC_ID=`zcat ${UNICHEM_DIR}/UC_SOURCE.txt.gz | awk '{if ($2 == "chebi") {printf "%s", $1}}'`
DRUGBANK_SRC_ID=`zcat ${UNICHEM_DIR}/UC_SOURCE.txt.gz | awk '{if ($2 == "drugbank") {printf "%s", $1}}'`

UPDATE_DATE=`zcat ${UNICHEM_DIR}/UC_RELEASE.txt.gz | tail -1 | cut -f3`
echo "# ${UPDATE_DATE}" > ${OUTPUT_TSV_FILE}

zcat ${UNICHEM_DIR}/UC_XREF.txt.gz | awk '{if ($2 == '${CHEBI_SRC_ID}') {print $1 "\tCHEBI:" $3}}' | sort -k1 > ${UNICHEM_DIR}/chebi.txt
zcat ${UNICHEM_DIR}/UC_XREF.txt.gz | awk '{if ($2 == '${CHEMBL_SRC_ID}') {print $1 "\tCHEMBL.COMPOUND:" $3}}' | sort -k1 > ${UNICHEM_DIR}/chembl.txt
zcat ${UNICHEM_DIR}/UC_XREF.txt.gz | awk '{if ($2 == '${DRUGBANK_SRC_ID}') {print $1 "\tDRUGBANK:" $3}}' | sort -k1 > ${UNICHEM_DIR}/drugbank.txt

join ${UNICHEM_DIR}/chembl.txt ${UNICHEM_DIR}/chebi.txt | sed 's/ /\t/g' | cut -f2-3 >> ${OUTPUT_TSV_FILE}
join ${UNICHEM_DIR}/chembl.txt ${UNICHEM_DIR}/drugbank.txt | sed 's/ /\t/g' | cut -f2-3 >> ${OUTPUT_TSV_FILE}

date
echo "================= script finished ================="
