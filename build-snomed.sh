#!/bin/bash
set -euxo pipefail

## setup the shell variables for various directories
BUILD_DIR=~/kg2-build
source ${BUILD_DIR}/master-config.shinc

## build OWL-XML representation of SNOMED CT
${VENV_DIR}/bin/pip3 install SNOMEDToOWL
SNOMEDCT_FILE_BASE=SnomedCT_USEditionRF2_PRODUCTION_20180901T120000Z
aws s3 cp --region ${S3_REGION} s3://${S3_BUCKET}/${SNOMEDCT_FILE_BASE}.zip ${BUILD_DIR}/
unzip ${BUILD_DIR}/${SNOMEDCT_FILE_BASE}.zip -d ${BUILD_DIR}
${VENV_DIR}/bin/SNOMEDToOWL -f xml ${BUILD_DIR}/${SNOMEDCT_FILE_BASE}/Snapshot \
           ${VENV_DIR}/lib/python3.6/site-packages/SNOMEDCTToOWL/conf/sct_core_us_gb.json \
           -o ${BUILD_DIR}/snomed.owl
${BUILD_DIR}/robot relax --input ${BUILD_DIR}/snomed.owl --output ${BUILD_DIR}/snomed-relax.owl
