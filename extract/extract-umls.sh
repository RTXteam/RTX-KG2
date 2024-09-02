#!/usr/bin/env bash
# extract-umls.sh:  download the UMLS release and convert it to a series of TTL files
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [umls_cui_file]"
    exit 2
fi

# Usage: extract-umls.sh [UMLS_CUI_FILE]

echo "================= starting extract-umls.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

output_file=${2:-${BUILD_DIR}/umls.jsonl}

umls_dir=${BUILD_DIR}/umls
umls_dest_dir=${umls_dir}/META
umls_ver=2023AA
umls_file_base=umls-${umls_ver}-metathesaurus-full
config_file=${umls_dir}/config.prop
mysql_dbname=umls

mysql_user=`grep 'user = ' ${mysql_conf} | sed 's/user = //g'`
mysql_password=`grep 'password = ' ${mysql_conf} | sed 's/password = //g'`


sudo apt-get update -y

## make directories that we need
rm -r -f ${umls_dir}
mkdir -p ${umls_dir}
mkdir -p ${umls_dest_dir}

## copy UMLS distribution files and MetamorphoSys config files from S3 to local dir
${s3_cp_cmd} s3://${s3_bucket}/${umls_file_base}.zip ${umls_dir}/
cp ${EXTRACT_CODE_DIR}/umls-config.prop ${config_file}

## unpack UMLS zip archive
unzip ${umls_dir}/${umls_file_base}.zip -d ${umls_dir}/

mv ${umls_dir}/${umls_ver}/META/* ${umls_dest_dir} 

mysql_user=`grep 'user = ' ${mysql_conf} | sed 's/user = //g'`
mysql_password=`grep 'password = ' ${mysql_conf} | sed 's/password = //g'`

## if a "umls" database already exists, delete it
mysql --defaults-extra-file=${mysql_conf} \
      -e "DROP DATABASE IF EXISTS ${mysql_dbname}"

## create the "umls" database
mysql --defaults-extra-file=${mysql_conf} \
      -e "CREATE DATABASE IF NOT EXISTS ${mysql_dbname} CHARACTER SET utf8 COLLATE utf8_unicode_ci"

mysql --defaults-extra-file=${mysql_conf} \
      -e "SET GLOBAL local_infile = true"

## fill in the authentication and database variables in the shell script for populating the mysql database
cat ${umls_dest_dir}/populate_mysql_db.sh | \
    sed "s/<username>/${mysql_user}/g" | \
    sed 's|<path to MYSQL_HOME>|/usr|g' | \
    sed "s/<password>/${mysql_password}/g" | \
    sed "s/<db_name>/${mysql_dbname}/g" | \
    sed "s/-vvv/-vvv --local-infile=1/g" > ${umls_dest_dir}/populate_mysql_db_configured.sh

## enable the loading script to be runnable
chmod +x ${umls_dest_dir}/populate_mysql_db_configured.sh

cp ${umls_dest_dir}/mysql_tables.sql ${umls_dest_dir}/mysql_tables.sql-original
cat ${umls_dest_dir}/mysql_tables.sql-original | sed 's/\\r\\n/\\n/g' > ${umls_dest_dir}/mysql_tables.sql
sed -i "s/@LINE_TERMINATION@/'\n'/g" ${umls_dest_dir}/mysql_tables.sql
cd ${umls_dest_dir}
bash -x populate_mysql_db_configured.sh

${python_command} ${EXTRACT_CODE_DIR}/umls_mysql_to_list_jsonl.py ${mysql_conf} ${mysql_dbname} ${output_file}

date
echo "================= finished extract-umls.sh ================="
