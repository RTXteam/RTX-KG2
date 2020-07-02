#!/usr/bin/env bash
# extract-ensembl.sh: download Ensembl datafile of annotated human genes
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

echo "================= starting build-ensembl.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

ncbi_gene_tsv_file=${1:-"${BUILD_DIR}/ncbigene/Homo_sapiens_gene_info.tsv"}
output_dir=`dirname ${ncbi_gene_tsv_file}`

mkdir -p ${output_dir}

${CURL_GET} ftp://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz > \
            ${ncbi_gene_tsv_file}.gz
gunzip -f ${ncbi_gene_tsv_file}.gz

date
echo  "================= script finished ================="
