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

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

ensembl_release=97

ensembl_json_file=${1:-"${BUILD_DIR}/ensembl/ensembl_genes_homo_sapiens.json"}
output_dir=`dirname ${ensembl_json_file}`

mkdir -p ${output_dir}

${curl_get} ftp://ftp.ensembl.org/pub/release-${ensembl_release}/json/homo_sapiens/homo_sapiens.json > ${ensembl_json_file}

date
echo  "================= finished extract-ensembl.sh ================="
