#!/usr/bin/env bash
# build-uniprotkb.sh: download UniProtKB dat distribution and extract to a JSON file
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [all|test]"
    exit 2
fi

echo "================= starting build-uniprotkb.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

UNIPROTKB_DAT_FILE=${1:-"${BUILD_DIR}/uniprot_sprot.dat"}

## supply a default value for the BUILD_FLAG string
BUILD_FLAG=${1:-""}

UNIPROTKB_DIR=${BUILD_DIR}/uniprotkb
CURL_GET="curl -s -L"

mkdir -p ${UNIPROTKB_DIR}
${CURL_GET} ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz  \
            > ${UNIPROTKB_DIR}/uniprot_sprot.dat.gz

gunzip -f -c ${UNIPROTKB_DIR}/uniprot_sprot.dat.gz > ${UNIPROTKB_DAT_FILE}


date
echo "================= script finished ================="
