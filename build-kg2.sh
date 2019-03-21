#!/bin/bash
set -euxo pipefail

BUILD_DIR=~/kg2-build
VENV_DIR=~/kg2-venv
CODE_DIR=~/kg2-code

export PATH=$PATH:${BUILD_DIR}
cd ${BUILD_DIR} && ${VENV_DIR}/bin/python3 -u ${CODE_DIR}/build-kg2.py \
                              ${BUILD_DIR}/curies-to-categories.yaml \
                              ${BUILD_DIR}/owl-load-inventory.yaml \
                              2>stderr.log 1>stdout.log
