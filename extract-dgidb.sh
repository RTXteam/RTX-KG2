#!/usr/bin/env bash
# extract-dgidb.sh: download DGIDB interactions dataset to local TSV file
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_tsv_dir>"
    exit 2
fi

echo "================= starting extract-dgidb.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

DGIDB_DIR=${1:-"${BUILD_DIR}/dgidb/"}
DGIDB_FILE=interactions.tsv

mkdir -p ${DGIDB_DIR}

${CURL_GET} http://www.dgidb.org/data/${DGIDB_FILE} > /tmp/${DGIDB_FILE}
UPDATE_DATE=`${CURL_GET} http://www.dgidb.org/downloads | grep 'Last updated' | sed 's/Last updated //g'`
echo "#${UPDATE_DATE}" > ${DGIDB_DIR}/${DGIDB_FILE}
cat /tmp/${DGIDB_FILE} >> ${DGIDB_DIR}/${DGIDB_FILE}

date
echo "================= finished extract-dgidb.sh ================="
