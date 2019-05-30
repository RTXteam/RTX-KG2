#!/bin/bash
set -euxo pipefail

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

SEMMED_VER=VER31
SEMMED_DATE=06302018
SEMMED_DIR=${BUILD_DIR}/semmeddb
SEMMED_SQL_FILE=semmed${SEMMED_VER}_R_PREDICATION_${SEMMED_DATE}.sql
SEMMED_OUTPUT_FILE=${BUILD_DIR}/kg2-semmeddb.json.gz
MYSQL_DBNAME=semmeddb

mkdir -p ${SEMMED_DIR}

## estimate amount of system ram, in GB
MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/${SEMMED_SQL_FILE}.gz ${SEMMED_DIR}/
gunzip ${SEMMED_DIR}/${SEMMED_SQL_FILE}.gz

## create the "umls" database
mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DBNAME} CHARACTER SET utf8 COLLATE utf8_unicode_ci"

mysql --defaults-extra-file=${MYSQL_CONF} --database=${MYSQL_DBNAME} < ${SEMMED_DIR}/${SEMMED_SQL_FILE}

${VENV_DIR}/bin/python3 ${CODE_DIR}/semmeddb_mysql_to_json.py \
	   ${MYSQL_CONF} \
	   ${MYSQL_DBNAME} \
	   ${SEMMED_OUTPUT_FILE} > ${BUILD_DIR}/build-semmeddb.log 2>&1



