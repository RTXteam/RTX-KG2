#!/usr/bin/env bash

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [test]"
    exit 2
fi

## supply a default value for the build_flag string
build_flag=${1:-""}
if [[ "${build_flag}" == 'test' || "${build_flag}" == 'alltest' ]]
then
    test_suffix='-test'
    test_arg='--test'
else
    test_suffix=''
    test_arg=''
fi

echo "================= starting make-kgx-export.sh ================="
date

## load the master config file
config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

tsv_dir=${BUILD_DIR}/kgx-tsv${test_suffix}

rm -r -f ${tsv_dir}
mkdir -p ${tsv_dir}

${VENV_DIR}/bin/python3 -u kg2_json_to_kgx_tsv.py \
           --logFile ${BUILD_DIR}/kg2_json_to_kgx_tsv.log \
           ${BUILD_DIR}/kg2-simplified${test_suffix}.json \
           ${tsv_dir}

${VENV_DIR}/bin/kgx --input-format tsv \
           --output ${BUILD_DIR}/content_metadata.json \
           --report-type meta-knowledge-graph \
           --error-log ${BUILD_DIR}/kgx_build_graph_stats.err \
           ${tsv_dir}/nodes.tsv \
           ${tsv_dir}/edges.tsv

date
echo "================= finished make-kgx-export.sh ================="
