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

## supply a default value for the BUILD_FLAG string
BUILD_FLAG=${1:-""}

UNIPROTKB_DIR=${BUILD_DIR}/uniprotkb
CURL_GET="curl -s -L"
UNIPROTKB_DAT_FILE=${UNIPROTKB_DIR}/uniprotkb_sprot.dat
UNIPROTKB_JSON_FILE=${BUILD_DIR}/kg-uniprotkb.json

mkdir -p ${UNIPROTKB_DIR}
${CURL_GET} ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz  \
            > ${UNIPROTKB_DIR}/uniprot_sprot.dat.gz

gunzip -f ${UNIPROTKB_DAT_FILE}.gz

if [ "${BUILD_FLAG}" == 'test' ]
then
    TEST_ARG='--test'
else
    TEST_ARG=''
fi

${VENV_DIR}/bin/python3 ${CODE_DIR}/uniprotkb_dat_to_json.py \
           ${TEST_ARG} \
	   --inputFile ${UNIPROTKB_DAT_FILE} \
	   --outputFile ${UNIPROTKB_JSON_FILE} 

date
echo "================= script finished ================="
