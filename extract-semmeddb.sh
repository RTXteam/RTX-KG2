#!/usr/bin/env bash
# extract-semmeddb.sh: download the SemMedDB release and convert it to a tuple-list JSON file
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_file.json> [test]"
    exit 2
fi

# Usage: extract-semmeddb.sh <output_file.json>

echo "================= starting extract-semmeddb.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

semmed_output_file=${1:-"${BUILD_DIR}/kg2-semmeddb-tuplelist.json"}

## supply a default value for the build_flag string
build_flag=${2:-""}

semmed_ver=VER43
semmed_year=2023
semmed_dir=${BUILD_DIR}/semmeddb
semmed_output_dir=`dirname "${semmed_output_file}"`

## SQL files
base_filename=semmed${semmed_ver}_${semmed_year}_R_

citations_sql_file=${base_filename}CITATIONS.sql.gz
generic_concept_sql_file=${base_filename}GENERIC_CONCEPT.sql.gz
predication_sql_file=${base_filename}PREDICATION.sql.gz
predication_aux_sql_file=${base_filename}PREDICATION_AUX.sql.gz
sentence_sql_file=${base_filename}SENTENCE.sql.gz

semmed_dump=${base_filename}WHOLEDB.tar.gz

mysql_dbname=semmeddb

mkdir -p ${semmed_dir}
mkdir -p ${semmed_output_dir}

## estimate amount of system ram, in GB
mem_gb=`${CODE_DIR}/get-system-memory-gb.sh`

${s3_cp_cmd} s3://${s3_bucket}/${semmed_dump} ${semmed_dir}/

tar -xf ${semmed_dir}/${semmed_dump}

## if a "semmeddb" database already exists, delete it
    mysql --defaults-extra-file=${mysql_conf} \
          -e "DROP DATABASE IF EXISTS ${mysql_dbname}"
    
## create the "semmeddb" database
    mysql --defaults-extra-file=${mysql_conf} \
          -e "CREATE DATABASE IF NOT EXISTS ${mysql_dbname} CHARACTER SET utf8 COLLATE utf8_unicode_ci"

zcat ${semmed_dir}/${citations_sql_file} | mysql --defaults-extra-file=${mysql_conf} --database=${mysql_dbname}
zcat ${semmed_dir}/${generic_concept_sql_file} | mysql --defaults-extra-file=${mysql_conf} --database=${mysql_dbname}
zcat ${semmed_dir}/${predication_sql_file} | mysql --defaults-extra-file=${mysql_conf} --database=${mysql_dbname}
zcat ${semmed_dir}/${predication_aux_sql_file} | mysql --defaults-extra-file=${mysql_conf} --database=${mysql_dbname}
zcat ${semmed_dir}/${sentence_sql_file} | mysql --defaults-extra-file=${mysql_conf} --database=${mysql_dbname}

if [[ "${build_flag}" == "test" || "${build_flag}" == 'alltest' ]]
then
   test_arg=" --test"
else
   test_arg=""
fi


${VENV_DIR}/bin/python3 ${CODE_DIR}/semmeddb_mysql_to_tuple_list_json.py \
           ${test_arg} \
           ${mysql_conf} \
           ${mysql_dbname} \
           ${semmed_ver} \
           ${semmed_year} \
           ${semmed_output_file}

date
echo "================= finished extract-semmeddb.sh ================="


