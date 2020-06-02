#!/usr/bin/env bash
# build-semmeddb.sh: download the SemMedDB release and convert it to a tuple-list JSON file
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_file.json> [test]"
    exit 2
fi

# Usage: build-semmeddb.sh <output_file.json>

echo "================= starting build-semmeddb.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

SEMMED_OUTPUT_FILE=${1:-"${BUILD_DIR}/kg2-semmeddb-tuplelist.json"}

## supply a default value for the BUILD_FLAG string
BUILD_FLAG=${2:-""}

SEMMED_VER=VER42
SEMMED_YEAR=2020
SEMMED_DIR=${BUILD_DIR}/semmeddb
SEMMED_OUTPUT_DIR=`dirname "${SEMMED_OUTPUT_FILE}"`
SEMMED_SQL_FILE=semmed${SEMMED_VER}_${SEMMED_YEAR}_R_WHOLEDB.sql
MYSQL_DBNAME=semmeddb

rm -r -f ${SEMMED_DIR}
mkdir -p ${SEMMED_DIR}
mkdir -p ${SEMMED_OUTPUT_DIR}

## estimate amount of system ram, in GB
MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/${SEMMED_SQL_FILE}.gz ${SEMMED_DIR}/

## if a "semmeddb" database already exists, delete it
    mysql --defaults-extra-file=${MYSQL_CONF} \
          -e "DROP DATABASE IF EXISTS ${MYSQL_DBNAME}"
    
## create the "semmeddb" database
    mysql --defaults-extra-file=${MYSQL_CONF} \
          -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DBNAME} CHARACTER SET utf8 COLLATE utf8_unicode_ci"
	
zcat ${SEMMED_DIR}/${SEMMED_SQL_FILE}.gz | mysql --defaults-extra-file=${MYSQL_CONF} --database=${MYSQL_DBNAME}

if [[ "${BUILD_FLAG}" == "test" ]]
then
   TEST_ARG=" --test"
else
   TEST_ARG=""
fi


${VENV_DIR}/bin/python3 ${CODE_DIR}/semmeddb_mysql_to_tuple_list_json.py \
           ${TEST_ARG} \
	   ${MYSQL_CONF} \
	   ${MYSQL_DBNAME} \
	   ${SEMMED_OUTPUT_FILE}

date
echo "================= script finished ================="


