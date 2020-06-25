#!/usr/bin/env bash
# extract-chembl.sh: download ChEMBL MySQL dump and load into a MySQL DB
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <mysql_db_name>"
    exit 2
fi

mysql_dbname=${1:-"chembl"}

echo "================= starting build-chembl.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

chembl_dir=${BUILD_DIR}/chembl
chembl_version=25
chembl_db_tarball=chembl_${chembl_version}_mysql.tar.gz
chembl_sql_file=${chemble_dir}/chembl_${chembl_version}/chembl_${chembl_version}_mysql/chembl_${chembl_version}_mysql.dmp

rm -r -f ${chembl_dir}
mkdir -p ${chembl_dir}

${CURL_GET} ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/latest/${chembl_db_tarball} > ${chembl_dir}/${chembl_db_tarball}

tar xzf ${chembl_dir}/${chembl_db_tarball} -C ${chembl_dir}
rm -f ${chembl_dir}/${chembl_db_tarball}
gzip {CHEMBL_SQL_FILE}

## if a "chembl" database already exists, delete it
mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "DROP DATABASE IF EXISTS ${mysql_dbname}"

mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "CREATE DATABASE IF NOT EXISTS ${mysql_dbname} DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"

zcat ${chembl_sql_file}.gz | mysql --defaults-extra-file=${MYSQL_CONF} --database=${mysql_dbname}

date
echo "================= script finished ================="
