#!/usr/bin/env bash
# extract-drugapprovalskg.sh: Download the Drug Approvals Knowledge Graph
# Copyright 2024 Stephen A. Ramsey
# Author Stephen Ramsey (adapted from a script written by Erica Wood)

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <drugapprovalskg-edges.tsv>"
    exit 2
fi

# Usage: extract-drugapprovalskg.sh <drugapprovalskg-edges.tsv>

echo "================= starting extract-drugapprovalskg.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

drugapprovalskg_output_file=${1:-"${BUILD_DIR}/drugapprovalskg-edges.tsv"}
version="0.3.5"

drugapprovalskg_download_link="https://db.systemsbiology.net/gestalt/KG/drug_approvals_kg_edges_v${version}.tsv"

echo "# ${version}" > ${drugapprovalskg_output_file}
${curl_get} ${drugapprovalskg_download_link} >> ${drugapprovalskg_output_file}

date
echo "================= finishing extract-drugapprovalskg.sh =================="
