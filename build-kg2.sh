#!/bin/bash
set -euxo pipefail

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

OUTPUT_FILE_BASE=kg2.json
REPORT_FILE_BASE=kg2-report.json
OUTPUT_FILE_FULL=${BUILD_DIR}/${OUTPUT_FILE_BASE}
REPORT_FILE_FULL=${BUILD_DIR}/${REPORT_FILE_BASE}
STDOUT_LOG_FILE=build-kg2-stdout.log
STDERR_LOG_FILE=build-kg2-stderr.log
OWL_LOAD_INVENTORY_FILE=${CODE_DIR}/owl-load-inventory.yaml

cd ${BUILD_DIR}

MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

export OWLTOOLS_MEMORY=${MEM_GB}G
export DEBUG=1  ## for owltools

## run the build-kg2.py script
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/build_kg2.py \
           ${CODE_DIR}/curies-to-categories.yaml \
           ${CODE_DIR}/curies-to-urls-lookaside-list.yaml \
           ${OWL_LOAD_INVENTORY_FILE} \
           ${OUTPUT_FILE_FULL} \
           2>${BUILD_DIR}/${STDERR_LOG_FILE} \
           1>${BUILD_DIR}/${STDOUT_LOG_FILE}

${VENV_DIR}/bin/report_stats_on_kg.py \
           ${OUTPUT_FILE_FULL} > ${REPORT_FILE_FULL}

## copy the KG to the public S3 bucket
aws s3 cp --no-progress --region ${S3_REGION} ${OUTPUT_FILE_FULL} s3://${S3_BUCKET_PUBLIC}/

## copy the log files to the public S3 bucket
aws s3 cp --no-progress --region ${S3_REGION} ${BUILD_DIR}/build-kg2-stderr.log s3://${S3_BUCKET_PUBLIC}/
aws s3 cp --no-progress --region ${S3_REGION} ${BUILD_DIR}/${STDOUT_LOG_FILE} s3://${S3_BUCKET_PUBLIC}/

## copy the config files to the public S3 bucket
aws s3 cp --no-progress --region ${S3_REGION} ${OWL_LOAD_INVENTORY_FILE} s3://${S3_BUCKET_PUBLIC}/

aws s3 cp --no-progress --regino ${S3_REGION} ${REPORT_FILE_FULL} s3://${S3_BUCKET_PUBLIC}/

echo "================= script finished ================="
