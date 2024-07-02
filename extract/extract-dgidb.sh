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

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

dgidb_dir=${1:-"${BUILD_DIR}/dgidb/"}
dgidb_file=interactions.tsv
dgidb_latest_download_url="https://www.dgidb.org/data/2022-Feb/interactions.tsv"
update_date="2022-Feb"

mkdir -p ${dgidb_dir}

${curl_get} ${dgidb_latest_download_url} > /tmp/${dgidb_file}

echo ${update_date}
echo "#${update_date}" > ${dgidb_dir}/${dgidb_file}
cat /tmp/${dgidb_file} >> ${dgidb_dir}/${dgidb_file}

date
echo "================= finished extract-dgidb.sh ================="
