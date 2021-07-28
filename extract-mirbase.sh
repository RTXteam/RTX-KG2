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

output_dir=${BUILD_DIR}/mirbase
output_file=${1:-"${BUILD_DIR}/miRNA.dat"}

mkdir -p ${output_dir}

${curl_get} ftp://mirbase.org/pub/mirbase/CURRENT/miRNA.dat.gz > ${output_dir}/miRNA.dat.gz
${curl_get} ftp://mirbase.org/pub/mirbase/CURRENT/README > ${output_dir}/miRBase_README.txt

version_number=`grep -m 1 "The miRBase Sequence Database -- Release" ${output_dir}/miRBase_README.txt | cut -f7 -d ' '`

zcat ${output_dir}/miRNA.dat.gz > /tmp/miRNA.dat
echo "# Version: ${version_number}" > ${output_file}
cat /tmp/miRNA.dat >> ${output_file}

date
echo "================= finished extract-mirbase.sh =================="
