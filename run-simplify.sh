#!/usr/bin/env bash
# run-simplify.sh: Remap relations to biolink predicates, and increment the version of the graph.
# Copyright 2020 Stephen A. Ramsey
# Author Erica Wood, Lindsey Kvarfordt

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <input_nodes_json> <input_edges_json> <output_nodes_json> <output_edges_json> [version_filename] [test]"
    exit 2
fi

# Usage: run-simplify.sh <input_nodes_json> <input_edges_json> <output_nodes_json> <output_edges_json> [version_filename] [test]

echo "================= starting run-simplify.sh =================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

trigger_file_is_major_release=${BUILD_DIR}/major-release
trigger_file_is_minor_release=${BUILD_DIR}/minor-release

input_nodes_json=${1:-}
input_edges_json=${2:-}
output_nodes_json=${3:-}
output_edges_json=${4:-}
local_version_filename=${5:-"${BUILD_DIR}/kg2-version.txt"}
build_flag=${6:-""}
s3_version_filename="kg2-version.txt"

${s3_cp_cmd} s3://${s3_bucket_public}/${s3_version_filename} ${local_version_filename}
test_flag=''
increment_flag=''
if [[ "${build_flag}" == 'test' ]]
then
   test_flag='--test'
else
    if [ -e ${trigger_file_is_major_release} ]
    then
        increment_flag='--increment_major'
    else
        if [ -e ${trigger_file_is_minor_release} ]
        then
            increment_flag='--increment_minor'
        fi
    fi
fi

if [[ "${increment_flag}" != '' ]]
then
    ${VENV_DIR}/bin/python3 ${CODE_DIR}/update_version.py ${increment_flag} ${local_version_filename}
else
    echo "*** TEST MODE -- NO INCREMENT ***"
fi

# TODO: Inhibits and increase are not in biolink model anymore - Find out what that should be now
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/filter_kg_and_remap_predicates.py ${test_flag} --dropNegated \
                        --dropSelfEdgesExcept interacts_with,regulates,inhibits,increase \
                        ${predicate_mapping_file} ${infores_mapping_file} ${curies_to_urls_file} ${input_nodes_json} ${input_edges_json} \
                        ${output_nodes_json} ${output_edges_json} ${local_version_filename}
${s3_cp_cmd} ${local_version_filename} s3://${s3_bucket_public}/${s3_version_filename}

if [[ -f ${trigger_file_is_major_release} ]]
then
   rm -f ${trigger_file_is_major_release}
fi

date
echo "================= finishing run-simplify.sh =================="
