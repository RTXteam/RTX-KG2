#!/usr/bin/env bash
# extract-intact.sh: Download the IntAct Dataset
# Copyright 2021 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <intact.txt>"
    exit 2
fi

# Usage: extract-intact.sh <intact.txt>

echo "================= starting extract-intact.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

intact_output_file=${1:-"${BUILD_DIR}/intact.txt"}

intact_link="ftp://ftp.ebi.ac.uk/pub/databases/intact/current/psimitab/intact.zip"

${curl_get} ${intact_link} > ${intact_output_file}.zip

unzip -o ${intact_output_file}.zip -d ${BUILD_DIR}

mv ${BUILD_DIR}/intact.txt ${intact_output_file}

date
echo "================= finishing extract-intact.sh =================="