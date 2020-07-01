#!/usr/bin/env bash
# extract-uniprotkb.sh: download UniProtKB dat distribution and extract to a dat file
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <uniprot_output_file.dat>"
    exit 2
fi

echo "================= starting extract-uniprotkb.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

UNIPROTKB_DAT_FILE=${1:-"${BUILD_DIR}/uniprot_sprot.dat"}

UNIPROTKB_DIR=`dirname ${UNIPROTKB_DAT_FILE}`

mkdir -p ${UNIPROTKB_DIR}
${CURL_GET} ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz  \
            > ${UNIPROTKB_DIR}/uniprot_sprot.dat.gz

zcat ${UNIPROTKB_DIR}/uniprot_sprot.dat.gz > /tmp/uniprot_sprot.dat
mv /tmp/uniprot_sprot.dat ${UNIPROTKB_DAT_FILE}

date
echo "================= finished extract-uniprotkb.sh ================="
