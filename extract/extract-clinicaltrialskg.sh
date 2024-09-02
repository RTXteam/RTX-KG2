#!/usr/bin/env bash
# extract-clinicaltrialskg.sh: Download the ClinicalTrials Knowledge Graph
# Copyright 2024 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <clinicaltrialskg-edges.tsv>"
    exit 2
fi

# Usage: extract-clinicaltrialskg.sh <clinicaltrialskg-edges.tsv>

echo "================= starting extract-clinicaltrialskg.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

clinicaltrialskg_output_file=${1:-"${BUILD_DIR}/clinicaltrialskg-edges.tsv"}
version="2.2.6"

clinicaltrialskg_download_link="https://db.systemsbiology.net/gestalt/KG/clinical_trials_kg_edges_v${version}.tsv"

echo "# ${version}" > ${clinicaltrialskg_output_file}
${curl_get} ${clinicaltrialskg_download_link} >> ${clinicaltrialskg_output_file}

date
echo "================= finishing extract-clinicaltrialskg.sh =================="