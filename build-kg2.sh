#!/bin/bash
set -euxo pipefail

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

OUTPUT_FILE_BASE=kg2.json
OUTPUT_FILE_FULL=${OUTPUT_DIR}/${OUTPUT_FILE_BASE}

## run the build-kg2.py script
cd ${BUILD_DIR} && ${VENV_DIR}/bin/python3 -u ${CODE_DIR}/build-kg2.py \
                              curies-to-categories.yaml \
                              curies-to-urls-lookaside-list.yaml \
                              owl-load-inventory.yaml \
                              ${OUTPUT_FILE_FULL} \
                              2>build-kg2-stderr.log 1>build-kg2-stdout.log

## copy the KG to the public S3 bucket
aws s3 cp --region ${S3_REGION} ${OUTPUT_FILE_FULL} s3://${S3_BUCKET_PUBLIC}/${OUTPUT_FILE_BASE}
