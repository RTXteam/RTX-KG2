#!/usr/bin/env bash
# extract-semmeddb.sh: download the SemMedDB release and convert it to a tuple-list JSON file
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_file.json> <output_exclude_list.yaml> <output_versioning.txt>"
    exit 2
fi

# Usage: extract-semmeddb.sh <output_file.json> <output_exclude_list.yaml> <output_versioning.txt>

echo "================= starting extract-semmeddb.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

semmed_output_file=${1:-"${BUILD_DIR}/kg2-semmeddb-tuplelist.json"}
domain_range_exclusion_file=${2:-"${BUILD_DIR}/${domain_range_exclusion_filename}"}
semmeddb_version_file=${3:-"${BUILD_DIR}/semmeddb-version.txt"}

semmed_ver=VER43
semmed_year=2023
semmed_dir=${BUILD_DIR}/semmeddb
semmed_output_dir=`dirname "${semmed_output_file}"`

echo -e "Version: ${semmed_ver}\nYear: ${semmed_year}" > ${semmeddb_version_file}

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

${s3_cp_cmd} s3://${s3_bucket}/${semmed_dump} ${semmed_dir}/

# We have to extract into the semmeddb directory, then move all of the extracted files (which
# end up in a subfolder) into that directory
tar -xf ${semmed_dir}/${semmed_dump} -C ${semmed_dir}
mv ${semmed_dir}/semmeddb/* ${semmed_dir}

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

# We need to free up space for the temp file for semmeddb_mysql_to_tuplelist_jsonl.py 
rm -rf ${semmed_dir}

## handle domain-range exclusion list (#281)
biolink_base_url_no_version=https://raw.githubusercontent.com/biolink/biolink-model/
biolink_raw_base_url=${biolink_base_url_no_version}v${biolink_model_version}/
domain_range_exclusion_filename=semmed-exclude-list.yaml
domain_range_exclusion_link=${biolink_raw_base_url}${domain_range_exclusion_filename}

${curl_get} ${domain_range_exclusion_link} -o ${domain_range_exclusion_file}

${python_command} ${EXTRACT_CODE_DIR}/semmeddb_mysql_to_tuplelist_jsonl.py \
                    ${mysql_conf} \
                    ${mysql_dbname} \
                    ${semmed_output_file}

date
echo "================= finished extract-semmeddb.sh ================="


