#!/usr/bin/env bash
# extract-ensembl.sh: download Ensembl datafile of annotated human genes 
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

echo "================= starting extract-ncbigene.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

NCBI_GENE_TSV_FILE=${1:-"${BUILD_DIR}/ncbigene/Homo_sapiens_gene_info.tsv"}
OUTPUT_DIR=`dirname ${NCBI_GENE_TSV_FILE}`

mkdir -p ${OUTPUT_DIR}

${CURL_GET} ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz > \
            ${NCBI_GENE_TSV_FILE}.gz
gunzip -f ${NCBI_GENE_TSV_FILE}.gz

date
echo  "================= finished extract-ncbigene.sh ================="
