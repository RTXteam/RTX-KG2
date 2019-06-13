#!/bin/bash
# Usage: build-multi-owl-kg.sh <output_file.json> [test]
set -euxo pipefail

echo "================= starting build-multi-owl-kg.sh ================="
date

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

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

OUTPUT_FILE=${1:-"${BUILD_DIR}/kg2-owl${TEST_SUFFIX}.json"}
OUTPUT_FILE_BASE=`basename ${OUTPUT_FILE}`
LOG_FILE=`dirname ${OUTPUT_FILE}`/build-${OUTPUT_FILE_BASE%.*}.log

OUTPUT_FILE_BASE="${OUTPUT_FILE%.*}"

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

export OWLTOOLS_MEMORY=${MEM_GB}G
export DEBUG=1  ## for owltools


OWL_LOAD_INVENTORY_FILE=${CODE_DIR}/owl-load-inventory${TEST_SUFFIX}.yaml

## run the build_kg2_from_owl.py script
cd ${BUILD_DIR} && ${VENV_DIR}/bin/python3 -u ${CODE_DIR}/multi_owl_to_json_kg.py \
           ${TEST_ARG} \
           ${CODE_DIR}/curies-to-categories.yaml \
           ${CODE_DIR}/curies-to-urls-lookaside-list.yaml \
           ${OWL_LOAD_INVENTORY_FILE} \
           ${OUTPUT_FILE} \
           2>build-${OUTPUT_FILE_BASE}-stderr.log

date
echo "================= script finished ================="
