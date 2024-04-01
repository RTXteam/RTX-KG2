#!/usr/bin/env bash
# build-multi-ont-kg.sh:  merge multiple OWL or TTL files for the KG2 knowledge graph for the RTX biomedical reasoning system
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_nodes_file.jsonl> <output_edges_file.jsonl> [test]"
    exit 2
fi

# Usage: build-multi-ont-kg.sh <input_file.tsv> <output_nodes_file.jsonl> <output_edges_file.jsonl> [test]
#        build-multi-ont-kg.sh /home/ubuntu/kg2-build/umls_cuis.jsonl /home/ubuntu/kg2-build/kg2-ont-nodes.jsonl /home/ubuntu/kg2-build/kg2-ont-edges.jsonl test

echo "================= starting build-multi-ont-kg.sh ================="
date

## load the master config file
config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

## supply a default value for the build_flag string
build_flag=${3:-""}
biolink_base_url_no_version=https://raw.githubusercontent.com/biolink/biolink-model/

# Issue #300: Need "v" before version number for URL to resolve
biolink_raw_base_url=${biolink_base_url_no_version}v${biolink_model_version}/project/owl/biolink_model.owl.ttl
biolink_raw_base_url_curies_urls_map=${biolink_base_url_no_version}v${biolink_model_version}/project/owl/biolink_model.owl.ttl
curies_urls_map_replace_string="\    biolink_download_source: ${biolink_raw_base_url_curies_urls_map}"
ont_load_inventory_replace_string="\  url: ${biolink_raw_base_url}"

sed -i "\@${biolink_base_url_no_version}@c${ont_load_inventory_replace_string}" \
        ${ont_load_inventory_file}

sed -i "\@${biolink_base_url_no_version}@c${curies_urls_map_replace_string}" \
         ${curies_to_urls_file}

if [[ "${build_flag}" == 'test' ]]
then
    test_suffix='-test'
    test_arg='--test'
else
    test_suffix=''
    test_arg=''
fi

output_nodes_file=${1:-"${BUILD_DIR}/kg2-ont-nodes${test_suffix}.json"}
output_edges_file=${2:-"${BUILD_DIR}/kg2-ont-edges${test_suffix}.json"}

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

mem_gb=`${CODE_DIR}/get-system-memory-gb.sh`

export OWLTOOLS_MEMORY=${mem_gb}G
export DEBUG=1  ## for owltools

${s3_cp_cmd} s3://${s3_bucket}/foodon.pickle ${BUILD_DIR}/

## run the multi_ont_to_json_kg.py script
cd ${BUILD_DIR} && ${python_command} ${CODE_DIR}/multi_ont_to_kg_jsonl.py \
           ${test_arg} \
           ${curies_to_categories_file} \
           ${curies_to_urls_file} \
           ${ont_load_inventory_file} \
           ${output_nodes_file} \
           ${output_edges_file}

date
echo "================= finished build-multi-ont-kg.sh ================="
