#!/usr/bin/env bash
# build-semmeddb.sh: download the SemMedDB release and convert it to a tuple-list JSON file
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_file.json> [all]"
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

SEMMED_VER=VER31
SEMMED_DATE=06302018
SEMMED_DIR=`dirname "${SEMMED_OUTPUT_FILE}"`
SEMMED_SQL_FILE=semmed${SEMMED_VER}_R_WHOLEDB_${SEMMED_DATE}.sql
MYSQL_DBNAME=semmeddb

mkdir -p ${SEMMED_DIR}

## estimate amount of system ram, in GB
MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/${SEMMED_SQL_FILE}.gz ${SEMMED_DIR}/

## create the "umls" database
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
	   --mysqlConfigFile ${MYSQL_CONF} \
	   --mysqlDBName ${MYSQL_DBNAME} \
	   --outputFile ${SEMMED_OUTPUT_FILE}

date
echo "================= script finished ================="


