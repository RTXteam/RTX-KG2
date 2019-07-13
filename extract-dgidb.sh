#!/usr/bin/env bash
# extract-dgidb.sh: download DGIDB interactions dataset to local TSV file
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_tsv_dir>"
    exit 2
fi

DGIDB_DIR=${1:-"${BUILD_DIR}/dgidb/"}

echo "================= starting build-unichem.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

mkdir -p ${DGIDB_DIR}

${CURL_GET} http://www.dgidb.org/data/interactions.tsv > ${DGIDB_DIR}/interactions.tsv
${CURL_GET} http://www.dgidb.org/data/genes.tsv > ${DGIDB_DIR}/genes.tsv

date
echo "================= script finished ================="
