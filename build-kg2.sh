#!/bin/bash
set -euxo pipefail

BUILD_DIR=~/kg2-build
VENV_DIR=~/kg2-venv
CODE_DIR=~/kg2-code

export PATH=$PATH:${BUILD_DIR}
cd ${BUILD_DIR} && ${VENV_DIR}/bin/python3 -u ${CODE_DIR}/build-kg2.py \
                              curies-to-categories.yaml \
                              curies-to-urls-lookaside-list.yaml \
                              owl-load-inventory.yaml \
                              2>build-kg2-stderr.log 1>build-kg2-stdout.log
