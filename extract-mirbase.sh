#!/usr/bin/env bash
# extract-mirbase.sh: Download the gzipped miRBase DAT file and extract it
# Copyright 2021 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output-dat-file>"
    exit 2
fi

# Usage: extract-mirbase.sh <output-dat-file>

echo "================= starting extract-mirbase.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

output_file=${1:-"${BUILD_DIR}/miRNA.dat"}

${curl_get} ftp://mirbase.org/pub/mirbase/CURRENT/miRNA.dat.gz > ${output_file}.gz
gzip -cdf ${output_file}.gz > ${output_file}

date
echo "================= finished extract-mirbase.sh =================="
