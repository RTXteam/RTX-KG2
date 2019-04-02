#!/bin/bash
set -euxo pipefail

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

## run the build-kg2.py script
cd ${BUILD_DIR} && ${VENV_DIR}/bin/python3 -u ${CODE_DIR}/build-kg2.py \
                              curies-to-categories.yaml \
                              curies-to-urls-lookaside-list.yaml \
                              owl-load-inventory.yaml \
                              ${OUTPUT_DIR}/kg2.json \
                              2>build-kg2-stderr.log 1>build-kg2-stdout.log
