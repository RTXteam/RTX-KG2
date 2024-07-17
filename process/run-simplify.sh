#!/usr/bin/env bash
# run-simplify.sh: Remap relations to biolink predicates, and increment the version of the graph.
# Copyright 2020 Stephen A. Ramsey
# Author Erica Wood, Lindsey Kvarfordt

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <input_nodes_json> <input_edges_json> <output_nodes_json> <output_edges_json> [version_filename] [test]"
    exit 2
fi

# Usage: run-simplify.sh <input_nodes_json> <input_edges_json> <output_nodes_json> <output_edges_json> [test]

echo "================= starting run-simplify.sh =================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

input_nodes_json=${1:-}
input_edges_json=${2:-}
output_nodes_json=${3:-}
output_edges_json=${4:-}
build_flag=${5:-""}

# TODO: Inhibits and increase are not in biolink model anymore - Find out what that should be now
${VENV_DIR}/bin/python3 -u ${PROCESS_CODE_DIR}/filter_kg_and_remap_predicates.py ${test_flag} --dropNegated \
                        --dropSelfEdgesExcept interacts_with,regulates,inhibits,increase \
                        ${predicate_mapping_file} ${infores_mapping_file} ${curies_to_urls_file} \
                        ${knowledge_level_agent_type_mapping_file} ${input_nodes_json} ${input_edges_json} \
                        ${output_nodes_json} ${output_edges_json} ${kg2_version_file_local}

date
echo "================= finishing run-simplify.sh =================="
