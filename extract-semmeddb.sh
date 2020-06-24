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

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

semmed_output_file=${1:-"${BUILD_DIR}/kg2-semmeddb-tuplelist.json"}

## supply a default value for the build_flag string
build_flag=${2:-""}

semmed_ver=VER31
semmed_date=06302018
semmed_dir=${BUILD_DIR}/semmeddb
semmed_output_dir=`dirname "${semmed_output_file}"`
semmed_sql_file=semmed${semmed_ver}_R_WHOLEDB_${semmed_date}.sql
mysql_dbname=semmeddb

rm -r -f ${semmed_dir}
mkdir -p ${semmed_dir}
mkdir -p ${semmed_output_dir}

## estimate amount of system ram, in GB
mem_gb=`${CODE_DIR}/get-system-memory-gb.sh`

aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/${semmed_sql_file}.gz ${semmed_dir}/

## if a "semmeddb" database already exists, delete it
    mysql --defaults-extra-file=${MYSQL_CONF} \
          -e "DROP DATABASE IF EXISTS ${mysql_dbname}"
    
## create the "semmeddb" database
    mysql --defaults-extra-file=${MYSQL_CONF} \
          -e "CREATE DATABASE IF NOT EXISTS ${mysql_dbname} CHARACTER SET utf8 COLLATE utf8_unicode_ci"
	
zcat ${semmed_dir}/${semmed_sql_file}.gz | mysql --defaults-extra-file=${MYSQL_CONF} --database=${mysql_dbname}

if [[ "${build_flag}" == "test" ]]
then
   test_arg=" --test"
else
   test_arg=""
fi


${VENV_DIR}/bin/python3 ${CODE_DIR}/semmeddb_mysql_to_tuple_list_json.py \
           ${test_arg} \
	   ${MYSQL_CONF} \
	   ${mysql_dbname} \
	   ${semmed_output_file}

date
echo "================= script finished ================="


