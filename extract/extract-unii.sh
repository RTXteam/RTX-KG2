#!/usr/bin/env bash
# extract-unii.sh: download FDA UNII node identifiers dataset to local TSV file
# Copyright 2024 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_tsv_dir>"
    exit 2
fi

echo "================= starting extract-unii.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

unii_dir="${BUILD_DIR}/unii/"
unii_latest_download_url="https://precision.fda.gov/uniisearch/archive/latest/UNIIs.zip"
unii_zip_file="UNIIs.zip"
unii_file='unii.tsv'

rm -r -f ${unii_dir}
mkdir -p ${unii_dir}

${curl_get} ${unii_latest_download_url} > /tmp/${unii_zip_file}
unzip /tmp/${unii_zip_file} -d ${unii_dir}

unii_source_file=`ls ${unii_dir} | grep UNII_Names_`
update_date=`echo ${unii_source_file} | rev | cut -f1 -d_ | rev | cut -f1 -d.`
echo ${update_date}
echo "#${update_date}" > ${unii_dir}/${unii_file}
cat ${unii_dir}/${unii_source_file} >> ${unii_dir}/${unii_file}

date
echo "================= finished extract-unii.sh ================="
