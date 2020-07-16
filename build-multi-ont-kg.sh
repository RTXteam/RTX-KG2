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

## supply a default value for the BUILD_FLAG string
BUILD_FLAG=${2:-""}

if [ "${BUILD_FLAG}" == 'test' ]
then
    TEST_SUFFIX='-test'
    TEST_ARG='--test'
else
    TEST_SUFFIX=''
    TEST_ARG=''
fi

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

OUTPUT_FILE=${1:-"${BUILD_DIR}/kg2-ont${TEST_SUFFIX}.json"}
OUTPUT_FILE_BASE=`basename ${OUTPUT_FILE}`
LOG_FILE=`dirname ${OUTPUT_FILE}`/build-${OUTPUT_FILE_BASE%.*}-stderr.log

OUTPUT_FILE_BASE="${OUTPUT_FILE%.*}"

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

export OWLTOOLS_MEMORY=${MEM_GB}G
export DEBUG=1  ## for owltools

## run the multi_ont_to_json_kg.py script
cd ${BUILD_DIR} && ${VENV_DIR}/bin/python3 -u ${CODE_DIR}/multi_ont_to_json_kg.py \
           ${TEST_ARG} \
           ${CURIES_TO_CATEGORIES_FILE} \
           ${CURIES_TO_URLS_FILE} \
           ${OWL_LOAD_INVENTORY_FILE} \
           ${OUTPUT_FILE} \
           2>${LOG_FILE}

date
echo "================= finished build-multi-ont-kg.sh ================="
