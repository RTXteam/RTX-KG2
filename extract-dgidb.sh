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

mkdir -p ${dgidb_dir}

${curl_get} http://www.dgidb.org/data/${dgidb_file} > /tmp/${dgidb_file}
update_date=`${curl_get} http://www.dgidb.org/downloads | grep 'Last updated' | sed 's/Last updated //g'`
echo "#${update_date}" > ${dgidb_dir}/${dgidb_file}
cat /tmp/${dgidb_file} >> ${dgidb_dir}/${dgidb_file}

date
echo "================= finished extract-dgidb.sh ================="
