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

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

uniprotkb_dat_file=${1:-"${BUILD_DIR}/uniprot_sprot.dat"}

uniprotkb_dir=`dirname ${uniprotkb_dat_file}`

mkdir -p ${uniprotkb_dir}
${CURL_GET} ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz  \
            > ${uniprotkb_dir}/uniprot_sprot.dat.gz

zcat ${uniprotkb_dir}/uniprot_sprot.dat.gz > /tmp/uniprot_sprot.dat
mv /tmp/uniprot_sprot.dat ${uniprotkb_dat_file}

date
echo "================= script finished ================="
