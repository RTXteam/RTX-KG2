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
dgidb_base_url="https://www.dgidb.org/"
mkdir -p ${dgidb_dir}

# not the most future proof, but finds the first table entry of interactions.tsv and grabs url from href
dgidb_path=`${curl_get} http://www.dgidb.org/downloads | grep -m 1 'interactions.tsv' | sed 's:<td><a href="\(.*\)">.*</a></td>:\1:'`
update_date=`echo ${dgidb_path} | grep -i -o -E '[0-9]{4}-[a-z]{3}'`
dgidb_url="${dgidb_base_url}${dgidb_path}"

${curl_get} ${dgidb_url} > /tmp/${dgidb_file}

echo ${update_date}
echo "#${update_date}" > ${dgidb_dir}/${dgidb_file}
cat /tmp/${dgidb_file} >> ${dgidb_dir}/${dgidb_file}

date
echo "================= finished extract-dgidb.sh ================="
