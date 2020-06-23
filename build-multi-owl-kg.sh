#!/usr/bin/env bash
# build-multi-owl-kg.sh:  merge multiple OWL/TTL files for the KG2 knowledge graph for the RTX biomedical reasoning system
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_file.json> [test]"
    exit 2
fi

# Usage: build-multi-owl-kg.sh <output_file.json> [test]
#        build-multi-owl-kg.sh /home/ubuntu/kg2-build/kg2-owl.json test

echo "================= starting build-multi-owl-kg.sh ================="
date

## load the master config file
config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

## supply a default value for the build_flag string
build_flag=${2:-""}

if [ "${build_flag}" == 'test' ]
then
    test_suffix='-test'
    test_arg='--test'
else
    test_suffix=''
    test_arg=''
fi

output_file=${1:-"${BUILD_DIR}/kg2-owl${test_suffix}.json"}
output_file_base=`basename ${output_file}`
log_file=`dirname ${output_file}`/build-${output_file_base%.*}-stderr.log

output_file_base="${output_file%.*}"

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

mem_gb=`${CODE_DIR}/get-system-memory-gb.sh`

export OWLTOOLS_MEMORY=${mem_gb}G
export DEBUG=1  ## for owltools


owl_load_inventory_file=${CODE_DIR}/owl-load-inventory${test_suffix}.yaml

## run the multi_owl_to_json_kg.py script
cd ${BUILD_DIR} && ${VENV_DIR}/bin/python3 -u ${CODE_DIR}/multi_owl_to_json_kg.py \
           ${test_arg} \
           ${CODE_DIR}/curies-to-categories.yaml \
           ${CURIES_TO_URLS_FILE} \
           ${owl_load_inventory_file} \
           ${output_file} \
           2>${log_file}

date
echo "================= script finished ================="
