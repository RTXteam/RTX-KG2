#!/usr/bin/env bash
# extract-umls.sh:  download the UMLS release and convert it to a series of TTL files
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [output_dir]"
    exit 2
fi

# Usage: extract-umls.sh [OUTPUT_DIR]

echo "================= starting extract-umls.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

output_dir=${1:-${BUILD_DIR}}

umls_ver=2020AA
umls_file_base=${umls_ver}-metathesaurus
umls2rdf_release=rtx-2.1
umls2rdf_pkgname=umls2rdf-${umls2rdf_release}
umls2rdf_dir=${umls_dir}/${umls2rdf_pkgname}
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
${s3_cp_cmd} s3://${s3_bucket}/umls-${umls_file_base}.zip ${umls_dir}/
cp ${CODE_DIR}/umls-config.prop ${config_file}

## unpack UMLS zip archive
unzip ${umls_dir}/umls-${umls_file_base}.zip -d ${umls_dir}/

mv ${umls_dir}/2020AA/META/* ${umls_dest_dir} 

mysql_user=`grep 'user = ' ${mysql_conf} | sed 's/user = //g'`
mysql_password=`grep 'password = ' ${mysql_conf} | sed 's/password = //g'`

## if a "umls" database already exists, delete it
mysql --defaults-extra-file=${mysql_conf} \
      -e "DROP DATABASE IF EXISTS ${mysql_dbname}"

## create the "umls" database
mysql --defaults-extra-file=${mysql_conf} \
      -e "CREATE DATABASE IF NOT EXISTS ${mysql_dbname} CHARACTER SET utf8 COLLATE utf8_unicode_ci"

## fill in the authentication and database variables in the shell script for populating the mysql database
cat ${umls_dest_dir}/populate_mysql_db.sh | \
    sed "s/<username>/${mysql_user}/g" | \
    sed 's|<path to MYSQL_HOME>|/usr|g' | \
    sed "s/<password>/${mysql_password}/g" | \
    sed "s/<db_name>/${mysql_dbname}/g" > ${umls_dest_dir}/populate_mysql_db_configured.sh

## enable the loading script to be runnable
chmod +x ${umls_dest_dir}/populate_mysql_db_configured.sh

cp ${umls_dest_dir}/mysql_tables.sql ${umls_dest_dir}/mysql_tables.sql-original
cat ${umls_dest_dir}/mysql_tables.sql-original | sed 's/\\r\\n/\\n/g' > ${umls_dest_dir}/mysql_tables.sql
sed -i "s/@LINE_TERMINATION@/'\n'/g" ${umls_dest_dir}/mysql_tables.sql
cd ${umls_dest_dir}
bash -x populate_mysql_db_configured.sh

## download and unpack the umls2rdf software
${curl_get} https://github.com/RTXteam/umls2rdf/archive/${umls2rdf_release}.tar.gz > ${umls2rdf_pkgname}.tar.gz
tar xzf ${umls2rdf_pkgname}.tar.gz -C ${umls_dir}

## make the umls2rdf config file
cat ${umls2rdf_dir}/conf_sample.py | sed 's/your-host/localhost/g' | \
    sed "s/umls2015ab/${mysql_dbname}/g" | \
    sed "s/your db user/${mysql_user}/g" | \
    sed "s/your db pass/${mysql_password}/g" | \
    sed "s|output|${output_dir}|g" | \
    sed "s/2015ab/${umls_ver}/g" > ${umls2rdf_dir}/conf.py

cp ${umls2rdf_config_master} ${umls2rdf_dir}/umls.conf

## change to the umls2rdf_dir directory
cd ${umls2rdf_dir}

## run umls2rdf
${VENV_DIR}/bin/python3 umls2rdf.py

## verify the output files
./checkOutputSyntax.sh  ${output_dir} # uses "rapper" command from the "raptor" package

date
echo "================= finished extract-umls.sh ================="
