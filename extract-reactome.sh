#!/usr/bin/env bash
# extract-reactome.sh: download the Reactome MySQL dump and import it into MySQL
# Copyright 2021 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_file.json> [test]"
    exit 2
fi

# Usage: extract-reactome.sh

echo "==============starting extract-reactome.sh==============="
date

config_dir=`dirname $0`
source ${config_dir}/master-config.shinc

mysql_dbname=reactome
mysql_file=reactome.sql.gz

${curl_get} https://reactome.org/download/current/databases/gk_current.sql.gz \
            > ${BUILD_DIR}/${mysql_file}

mysql --defaults-extra-file=${mysql_conf} \
      -e "DROP DATABASE IF EXISTS ${mysql_dbname}"

mysql --defaults-extra-file=${mysql_conf} \
      -e "CREATE DATABASE IF NOT EXISTS ${mysql_dbname} CHARACTER SET utf8 COLLATE utf8_unicode_ci"

zcat ${BUILD_DIR}/${mysql_file} | mysql --defaults-extra-file=${mysql_conf} --database=${mysql_dbname}

date
echo "==============finished extract-reactome.sh==============="