#!/bin/bash
set -euxo pipefail

BUILD_DIR=~/kg2-build
source ${BUILD_DIR}/master-config.shinc
rm -r -f ${BUILD_DIR}
rm -r -f ${VENV_DIR}
rm -r -f ${CODE_DIR}
rm -r -f ${SHARE_DIR}
