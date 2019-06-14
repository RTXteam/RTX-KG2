#!/usr/bin/env bash
# build-kg2.sh:  main build script for the KG2 knowledge graph for the RTX biomedical reasoning system
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [all|test]"
    exit 2
fi

# Usage: build-kg2.sh [all|test]
# * If no argument, then by default only the OWL-based KG2 is generated from scratch. It is then merged
#   with the pre-existing SemMedDB JSON file. 
# 
# * The 'all' argument means that the script will build the UMLS and SemMedDB files. Complete KG2 build.
#
# * The 'test' argument means that the OWL inventory is read from "owl-load-inventory-test.yaml"
#   and all KG JSON files generated will have the string "-test" appended before their JSON suffixes.

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

BUILD_FLAG=${1:-""}
echo "${BUILD_FLAG}"

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

if [ "${BUILD_FLAG}" == 'test' ]
then
    echo "********** TEST MODE **********"
    TEST_SUFFIX='-test'
    TEST_ARG='--test'
else
    TEST_SUFFIX=''
    TEST_ARG=''
fi

BUILD_KG2_LOG_FILE=${BUILD_DIR}/build-kg2${TEST_SUFFIX}.log

{

echo "================= starting build-kg2.sh ================="
date
    
## supply a default value for the BUILD_FLAG string

SEMMED_TUPLELIST_FILE=${BUILD_DIR}/kg2-semmeddb${TEST_SUFFIX}-tuplelist.json
SEMMED_OUTPUT_FILE=${BUILD_DIR}/kg2-semmeddb${TEST_SUFFIX}-edges.json

OUTPUT_FILE_BASE=kg2-owl${TEST_SUFFIX}.json
OUTPUT_FILE_FULL=${BUILD_DIR}/${OUTPUT_FILE_BASE}

OUTPUT_FILE_ORPHAN_EDGES=${BUILD_DIR}/kg2-orphans${TEST_SUFFIX}-edges.json

FINAL_OUTPUT_FILE_BASE=kg2${TEST_SUFFIX}.json
FINAL_OUTPUT_FILE_FULL=${BUILD_DIR}/${FINAL_OUTPUT_FILE_BASE}

OUTPUT_NODES_FILE_BASE=kg2${TEST_SUFFIX}-nodes.json
OUTPUT_NODES_FILE_FULL=${BUILD_DIR}/${OUTPUT_NODES_FILE_BASE}

REPORT_FILE_BASE=kg2-report${TEST_SUFFIX}.json
REPORT_FILE_FULL=${BUILD_DIR}/${REPORT_FILE_BASE}

OWL_LOAD_INVENTORY_FILE=${CODE_DIR}/owl-load-inventory${TEST_SUFFIX}.yaml

cd ${BUILD_DIR}

MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

if [ "${BUILD_FLAG}" == 'all' ]
then
## Build UMLS knowledge sources at TTL files:
   bash -x ${CODE_DIR}/build-umls.sh ${BUILD_DIR}
fi

## Build SemMedDB tuplelist file as JSON:
bash -x ${CODE_DIR}/build-semmeddb.sh ${SEMMED_TUPLELIST_FILE} ${BUILD_FLAG}

## Build SemMedDB KG2 edges file as JSON:
${VENV_DIR}/bin/python3 ${CODE_DIR}/semmeddb_tuple_list_json_to_edges_json.py \
           ${TEST_ARG} \
           --inputFile ${SEMMED_TUPLELIST_FILE} \
           --outputFile ${SEMMED_OUTPUT_FILE}

## Combine all the TTL files and OBO Foundry OWL files into KG and save as JSON:
bash -x ${CODE_DIR}/build-multi-owl-kg.sh \
     ${OUTPUT_FILE_FULL} ${BUILD_FLAG}

${VENV_DIR}/bin/python3 ${CODE_DIR}/add_edges_to_kg_json.py \
           ${TEST_ARG} \
           --kgFile ${OUTPUT_FILE_FULL} \
           --kgFileNewEdges ${SEMMED_OUTPUT_FILE} \
           --outputFile ${FINAL_OUTPUT_FILE_FULL} \
           --kgFileOrphanEdges ${OUTPUT_FILE_ORPHAN_EDGES}

${VENV_DIR}/bin/python3 ${CODE_DIR}/get_nodes_json_from_kg_json.py \
           --inputFile ${FINAL_OUTPUT_FILE_FULL} \
           --outputFile ${OUTPUT_NODES_FILE_FULL}

${VENV_DIR}/bin/python3 ${CODE_DIR}/report_stats_on_kg.py \
           --inputFile ${FINAL_OUTPUT_FILE_FULL} \
           --outputFile ${REPORT_FILE_FULL}

gzip -f ${FINAL_OUTPUT_FILE_FULL}
gzip -f ${OUTPUT_NODES_FILE_FULL}
gzip -f ${OUTPUT_FILE_ORPHAN_EDGES}

## copy the KG to the public S3 bucket
aws s3 cp --no-progress --region ${S3_REGION} ${FINAL_OUTPUT_FILE_FULL}.gz s3://${S3_BUCKET_PUBLIC}/
aws s3 cp --no-progress --region ${S3_REGION} ${OUTPUT_NODES_FILE_FULL}.gz s3://${S3_BUCKET_PUBLIC}/
aws s3 cp --no-progress --region ${S3_REGION} ${REPORT_FILE_FULL} s3://${S3_BUCKET_PUBLIC}/
aws s3 cp --no-progress --region ${S3_REGION} ${OUTPUT_FILE_ORPHAN_EDGES}.gz s3://${S3_BUCKET_PUBLIC}/

## copy the log files to the public S3 bucket
BUILD_MULTI_OWL_STDERR_FILE="${BUILD_DIR}/build-${OUTPUT_FILE_BASE%.*}"-stderr.log

aws s3 cp --no-progress --region ${S3_REGION} ${BUILD_MULTI_OWL_STDERR_FILE} s3://${S3_BUCKET_PUBLIC}/

## copy the config files to the public S3 bucket
aws s3 cp --no-progress --region ${S3_REGION} ${OWL_LOAD_INVENTORY_FILE} s3://${S3_BUCKET_PUBLIC}/

# copy the index.html file to the public S3 bucket
aws s3 cp --no-progress --region ${S3_REGION} ${CODE_DIR}/s3-index.html s3://${S3_BUCKET_PUBLIC}/index.html

date
} >${BUILD_KG2_LOG_FILE} 2>&1

aws s3 cp --no-progress --region ${S3_REGION} ${BUILD_KG2_LOG_FILE} s3://${S3_BUCKET_PUBLIC}/

echo "================= script finished ================="
