#!/bin/bash

set -euxo pipefail

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

## supply a default value for the BUILD_FLAG string
BUILD_FLAG=${1:-""}

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

export OWLTOOLS_MEMORY=${MEM_GB}G
export DEBUG=1  ## for owltools

if [ ${BUILD_FLAG} == 'test' ]
then
    TEST_SUFFIX='-test'
else
    TEST_SUFFIX=''
fi

OWL_LOAD_INVENTORY_FILE=${CODE_DIR}/owl-load-inventory${TEST_SUFFIX}.yaml
OUTPUT_FILE_BASE=kg2-owl${TEST_SUFFIX}.json
OUTPUT_FILE_FULL=${BUILD_DIR}/${OUTPUT_FILE_BASE}
STDERR_LOG_FILE=build-kg2-from-owl-stderr${TEST_SUFFIX}.log


## run the build_kg2_from_owl.py script
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/multi_owl_to_json_kg.py \
           ${CODE_DIR}/curies-to-categories.yaml \
           ${CODE_DIR}/curies-to-urls-lookaside-list.yaml \
           ${OWL_LOAD_INVENTORY_FILE} \
           ${OUTPUT_FILE_FULL} \
           2>${BUILD_DIR}/${STDERR_LOG_FILE}
