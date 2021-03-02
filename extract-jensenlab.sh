#!/usr/bin/env bash
# extract-jensenlab.sh: download Jensen Lab Gene Disease text mining associations 
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [all|test]"
    exit 2
fi

echo "================= starting extract-jensenlab.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

local_dir="${BUILD_DIR}/jensenlab"
local_human_dictionary_dir="${local_dir}/human_dictionary"
local_tsv_file="${local_dir}/human_disease_text_mining_filtered.tsv"
local_dictionary_tarball="${local_dir}/human_dictionary.tar.gz"

mkdir -p ${local_human_dictionary_dir}

# tsv has format gene_id	gene_name	disease_id	disease_name	zscore	confidence(?)	source_url
${curl_get} https://download.jensenlab.org/human_disease_textmining_filtered.tsv > ${local_tsv_file}

# need to get id's we have from gene_id, so download human dictionary
${curl_get}  http://download.jensenlab.org/human_dictionary.tar.gz > ${local_dictionary_tarball}
# unzip into directory
tar -xf ${local_dictionary_tarball} --directory ${local_human_dictionary_dir}

date
echo "================= finished extract-jensenlab.sh ================="
