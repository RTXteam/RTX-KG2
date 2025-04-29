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

# To determine what version of UniProtKB was downloaded in the KG2pre build, 
# it may be helpful to view the release date of uniprot_sprot.dat on this
# web page: https://ftp.uniprot.org/pub/databases/uniprot/current_release/
mkdir -p ${uniprotkb_dir}
${curl_get} ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz  \
            > ${uniprotkb_dir}/uniprot_sprot.dat.gz

${curl_get} ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/relnotes.txt \
            > ${uniprotkb_dir}/relnotes.txt

version_number=`grep -m 1 "UniProt Release" ${uniprotkb_dir}/relnotes.txt | cut -f3 -d ' '`
update_date=`grep -m 1 "${version_number} (" ${uniprotkb_dir}/relnotes.txt | cut -f2 -d ' ' | cut -f2 -d '(' | cut -f1 -d ')'`

start_string="# Version: ${version_number}, Date: ${update_date}"

zcat ${uniprotkb_dir}/uniprot_sprot.dat.gz > /tmp/uniprot_sprot.dat
echo ${start_string} > ${uniprotkb_dat_file}
cat /tmp/uniprot_sprot.dat >> ${uniprotkb_dat_file}

date
echo "================= finished extract-uniprotkb.sh ================="
