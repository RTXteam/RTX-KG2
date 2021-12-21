#!/usr/bin/env bash

set -o nounset -o pipefail -o errexit

echo "================= starting make-kgx-export.sh ================="
date

## load the master config file
config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

${VENV_DIR}/bin/python3 -u kg2_json_to_kgx_tsv.py \
           --logFile ${BUILD_DIR}/kg2_json_to_kgx_tsv.log \
           ${BUILD_DIR}/kg2-simplified.json \
           ${BUILD_DIR}

${VENV_DIR}/bin/kgx --input-format tsv \
           --output ${BUILD_DIR}/content_metadata.json \
           --report-type meta-knowledge-graph \
           --error-log ${BUILD_DIR}/kgx_build_graph_stats.err \
           ${BUILD_DIR}/nodes.tsv \
           ${BUILD_DIR}/edges.tsv

date
echo "================= finished make-kgx-export.sh ================="
