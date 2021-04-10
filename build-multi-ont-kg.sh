#!/usr/bin/env bash
# build-multi-ont-kg.sh:  merge multiple OWL or TTL files for the KG2 knowledge graph for the RTX biomedical reasoning system
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_file.json> [test]"
    exit 2
fi

# Usage: build-multi-ont-kg.sh <output_file.json> [test]
#        build-multi-ont-kg.sh /home/ubuntu/kg2-build/kg2-ont.json test

echo "================= starting build-multi-ont-kg.sh ================="
date

## supply a default value for the build_flag string
build_flag=${2:-""}

if [[ "${build_flag}" == 'test' || "${build_flag}" == 'alltest' ]]
then
    test_suffix='-test'
    test_arg='--test'
else
    test_suffix=''
    test_arg=''
fi

## load the master config file
config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

output_file=${1:-"${BUILD_DIR}/kg2-ont${test_suffix}.json"}
output_file_base=`basename ${output_file}`
log_file=`dirname ${output_file}`/build-${output_file_base%.*}-stderr.log

output_file_base="${output_file%.*}"

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

mem_gb=`${CODE_DIR}/get-system-memory-gb.sh`

export OWLTOOLS_MEMORY=${mem_gb}G
export DEBUG=1  ## for owltools

node_datatype_properties_file="${BUILD_DIR}/node_datatype_properties.json"

## temporary work around for ontobio issue (see biolink issue #507)
${BUILD_DIR}/robot convert --input ${BUILD_DIR}/umls-hgnc.ttl --output u${BUILD_DIR}/mls-hgnc.owl
${BUILD_DIR}/robot convert --input ${BUILD_DIR}/umls-omim.ttl --output ${BUILD_DIR}/umls-omim.owl
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/save_owl_datatypeproperties.py \
           ${BUILD_DIR}/umls-hgnc.owl \
           ${BUILD_DIR}/umls-omim.owl \
           --outputFile ${node_datatype_properties_file}

## run the multi_ont_to_json_kg.py script
cd ${BUILD_DIR} && ${VENV_DIR}/bin/python3 -u ${CODE_DIR}/multi_ont_to_json_kg.py \
           ${test_arg} \
           ${curies_to_categories_file} \
           ${curies_to_urls_file} \
           ${ont_load_inventory_file} \
           ${output_file} \
           ${node_datatype_properties_file} \
           2>${log_file}

date
echo "================= finished build-multi-ont-kg.sh ================="
