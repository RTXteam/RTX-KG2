#!/bin/bash
set -euxo pipefail

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

export PATH=$PATH:${BUILD_DIR}
cd ${BUILD_DIR} && ${VENV_DIR}/bin/python3 -u ${CODE_DIR}/build-kg2.py \
                              curies-to-categories.yaml \
                              curies-to-urls-lookaside-list.yaml \
                              owl-load-inventory.yaml \
                              ${OUTPUT_DIR} \
                              2>build-kg2-stderr.log 1>build-kg2-stdout.log
