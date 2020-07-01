#!/usr/bin/env bash
# extract-drugbank.sh: Download the gzipped DrugBank XML file from the S3 Bucket
# Copyright 2019 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output-xml-file>"
    exit 2
fi

# Usage: extract-drugbank.sh <output_xml_file>

echo "================= starting extract-drugbank.sh =================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

OUTPUT_FILE=${1:-"${BUILD_DIR}/drugbank.xml"}

XML_FILENAME="drugbank.xml.gz"

${S3_CP_CMD} s3://${S3_BUCKET}/${XML_FILENAME} ${BUILD_DIR}
gzip -cdf ${BUILD_DIR}/${XML_FILENAME} > ${OUTPUT_FILE}

date
echo "================= finished extract-drugbank.sh =================="
