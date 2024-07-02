#!/usr/bin/env bash
# extract-disgenet.sh: Download the DisGeNET Gene-Disease associations with PMIDs
# Copyright 2021 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <disgenet.tsv>"
    exit 2
fi

# Usage: extract-disgenet.sh <disgenet.tsv>

echo "================= starting extract-disgenet.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

disgenet_output_file=${1:-"${BUILD_DIR}/all_gene_disease_pmid_associations.tsv"}

disgenet_download_link="https://www.disgenet.org/static/disgenet_ap1/files/downloads/all_gene_disease_pmid_associations.tsv.gz"

${curl_get} ${disgenet_download_link} > ${disgenet_output_file}.gz

gzip -d ${disgenet_output_file}.gz


date
echo "================= finishing extract-disgenet.sh =================="