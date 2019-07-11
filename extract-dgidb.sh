#!/usr/bin/env bash
# extract-dgidb.sh: download DGIDB interactions dataset to local TSV file
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_tsv_file>"
    exit 2
fi

OUTPUT_TSV_FILE=${1:-"${BUILD_DIR}/dgidb/interations.tsv"}

echo "================= starting build-unichem.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

DGIDB_DIR=`dirname ${OUTPUT_TSV_FILE}`

mkdir -p ${DGIDB_DIR}

${CURL_GET} http://www.dgidb.org/data/interactions.tsv > ${OUTPUT_TSV_FILE}

date
echo "================= script finished ================="
