#!/bin/bash
set -euxo pipefail

BUILD_DIR=~/kg2-build
VENV_DIR=~/kg2-venv
CODE_DIR=~/kg2-code

export PATH=$PATH:${BUILD_DIR}
cd ${BUILD_DIR} && ${VENV_DIR}/bin/python3 -u ${CODE_DIR}/build-kg2.py \
                              ${CODE_DIR}/curies-to-categories.yaml \
                              ${CODE_DIR}/ontology-load-config.yaml \
                              2>stderr.log 1>stdout.log
