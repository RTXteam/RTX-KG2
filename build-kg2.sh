#!/bin/bash
set -euxo pipefail
# Usage: build-kg2.sh [all]
# The 'all' argument means that the script will build the UMLS and SemMedDB files

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

OUTPUT_FILE_BASE=kg2-owl.json.gz
FINAL_OUTPUT_FILE_BASE=kg2.json.gz
OUTPUT_NODES_FILE_BASE=kg2-nodes.json.gz
REPORT_FILE_BASE=kg2-report.json
OUTPUT_FILE_FULL=${BUILD_DIR}/${OUTPUT_FILE_BASE}
OUTPUT_NODES_FILE_FULL=${BUILD_DIR}/${OUTPUT_NODES_FILE_BASE}
REPORT_FILE_FULL=${BUILD_DIR}/${REPORT_FILE_BASE}
STDOUT_LOG_FILE=build-kg2-from-owl-stdout.log
STDERR_LOG_FILE=build-kg2-from-owl-stderr.log
OWL_LOAD_INVENTORY_FILE=${CODE_DIR}/owl-load-inventory.yaml
FINAL_OUTPUT_FILE_FULL=${BUILD_DIR}/${FINAL_OUTPUT_FILE_BASE}

cd ${BUILD_DIR}

MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

export OWLTOOLS_MEMORY=${MEM_GB}G
export DEBUG=1  ## for owltools

if [ $1 == 'all' ]
then
## Build UMLS TTL files
   ${CODE_DIR}/build-umls.sh > ${BUILD_DIR}/build-umls.log 2>&1
fi

## run the build_kg2_from_owl.py script
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/build_kg2_from_owl.py \
           ${CODE_DIR}/curies-to-categories.yaml \
           ${CODE_DIR}/curies-to-urls-lookaside-list.yaml \
           ${OWL_LOAD_INVENTORY_FILE} \
           ${OUTPUT_FILE_FULL} \
           2>${BUILD_DIR}/${STDERR_LOG_FILE} \
           1>${BUILD_DIR}/${STDOUT_LOG_FILE}

if [ $1 == 'all' ]
then
## Build kg2-semmeddb.json.gz
    ${CODE_DIR}/build-semmeddb.sh > ${BUILD_DIR}/build-semmeddb.log 2>&1
fi

${VENV_DIR}/bin/python3 ${CODE_DIR}/kg2_merge.py ${OUTPUT_FILE_FULL} ${BUILD_DIR}/kg2-semmeddb.json.gz ${FINAL_OUTPUT_FILE_FULL}

${VENV_DIR}/bin/python3 ${CODE_DIR}/get_nodes_json_from_graph_json.py \
           ${FINAL_OUTPUT_FILE_FULL} ${OUTPUT_NODES_FILE_FULL}

${VENV_DIR}/bin/python3 ${CODE_DIR}/report_stats_on_kg.py \
           ${FINAL_OUTPUT_FILE_FULL} ${REPORT_FILE_FULL}

## copy the KG to the public S3 bucket
aws s3 cp --no-progress --region ${S3_REGION} ${FINAL_OUTPUT_FILE_FULL} s3://${S3_BUCKET_PUBLIC}/
aws s3 cp --no-progress --region ${S3_REGION} ${OUTPUT_NODES_FILE_FULL} s3://${S3_BUCKET_PUBLIC}/
aws s3 cp --no-progress --region ${S3_REGION} ${REPORT_FILE_FULL} s3://${S3_BUCKET_PUBLIC}/

## copy the log files to the public S3 bucket
aws s3 cp --no-progress --region ${S3_REGION} ${BUILD_DIR}/build-kg2-stderr.log s3://${S3_BUCKET_PUBLIC}/
aws s3 cp --no-progress --region ${S3_REGION} ${BUILD_DIR}/${STDOUT_LOG_FILE} s3://${S3_BUCKET_PUBLIC}/

## copy the config files to the public S3 bucket
aws s3 cp --no-progress --region ${S3_REGION} ${OWL_LOAD_INVENTORY_FILE} s3://${S3_BUCKET_PUBLIC}/

# copy the index.html file to the public S3 bucket
aws s3 cp --no-progress --region ${S3_REGION} ${CODE_DIR}/s3/index.html s3://${S3_BUCKET_PUBLIC}/

echo "================= script finished ================="
