#!/usr/bin/env bash
# build-umls.sh:  download the UMLS release and convert it to a series of TTL files
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [output_dir]"
    exit 2
fi

# Usage: build-umls.sh [output_dir]

echo "================= starting build-umls.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

output_dir=${1:-${BUILD_DIR}}

umls_ver=2018AB
umls_file_base=${umls_ver}-full
umls_dir=${BUILD_DIR}/umls
mmsys_dir=${umls_dir}/${umls_file_base}
umls_dest_dir=${umls_dir}/META
umls2rdf_release=rtx-1.6
umls2rdf_pkgname=umls2rdf-${umls2rdf_release}
umls2rdf_dir=${umls_dir}/${umls2rdf_pkgname}
config_file=${umls_dir}/config.prop
mysql_dbname=umls

sudo apt-get update -y

## make directories that we need
rm -r -f ${umls_dir}
mkdir -p ${umls_dir}
mkdir -p ${umls_dest_dir}

## copy UMLS distribution files and MetamorphoSys config files from S3 to local dir
aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/umls-${umls_file_base}.zip ${umls_dir}/
cp ${CODE_DIR}/umls-config.prop ${config_file}

## unpack UMLS and MetamorphoSys zip archives
unzip ${umls_dir}/umls-${umls_file_base}.zip -d ${umls_dir}/
unzip ${umls_dir}/${umls_file_base}/mmsys.zip -d ${umls_dir}/${umls_file_base}

## setup environment for running MetamorphoSys
export METADIR=${umls_dir}
export DESTDIR=${umls_dest_dir}
export MMSYS_HOME=${umls_dir}/${umls_file_base}
export CLASSPATH=${mmsys_dir}:${mmsys_dir}/lib/jpf-boot.jar
export JAVA_HOME=${mmsys_dir}/jre/linux
cd ${MMSYS_HOME}

## this is a workaround for a strange runtime warning I was getting from apache log4j
cp ${MMSYS_HOME}/etc/subset.log4j.properties ${MMSYS_HOME}/log4j.properties

## estimate amount of system ram, in GB
mem_gb=`${CODE_DIR}/get-system-memory-gb.sh`

## export UMLS to Rich Release Format (RRF)
${JAVA_HOME}/bin/java -Djava.awt.headless=true \
                      -Djpf.boot.config=${MMSYS_HOME}/etc/subset.boot.properties \
                      -Dinput.uri=${METADIR} \
                      -Doutput.uri=${DESTDIR} \
                      -Dmmsys.config.uri=${config_file} \
                      -Xms300M -Xmx${mem_gb}G org.java.plugin.boot.Boot

mysql_user=`grep 'user = ' ${MYSQL_CONF} | sed 's/user = //g'`
mysql_password=`grep 'password = ' ${MYSQL_CONF} | sed 's/password = //g'`

## if a "umls" database already exists, delete it
mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "DROP DATABASE IF EXISTS ${mysql_dbname}"

## create the "umls" database
mysql --defaults-extra-file=${MYSQL_CONF} \
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
cd ${umls_dest_dir} && ./populate_mysql_db_configured.sh

## download and unpack the umls2rdf software
${CURL_GET} https://github.com/RTXteam/umls2rdf/archive/${umls2rdf_release}.tar.gz > ${umls2rdf_pkgname}.tar.gz
tar xzf ${umls2rdf_pkgname}.tar.gz -C ${umls_dir}

## make the umls2rdf config file
cat ${umls2rdf_dir}/conf_sample.py | sed 's/your-host/localhost/g' | \
    sed "s/umls2015ab/${mysql_dbname}/g" | \
    sed "s/your db user/${mysql_user}/g" | \
    sed "s/your db pass/${mysql_password}/g" | \
    sed "s|http://purl.bioontology.org/ontology|https://identifiers.org/umls|g" | \
    sed "s|output|${output_dir}|g" | \
    sed "s/2015ab/${umls_ver}/g" > ${umls2rdf_dir}/conf.py

cp ${CODE_DIR}/umls2rdf-umls.conf ${umls2rdf_dir}/umls.conf

## umls2rdf is legacy software written to run in python2.7; set up the virtualenv
umls_venv_dir=${umls_dir}/venv27
virtualenv --python=python2.7 ${umls_venv_dir}

## need libssl for installing mysqlclient; it is installed in setup-kg2-build.sh
${umls_venv_dir}/bin/pip install mysqlclient

## change to the umls2rdf_dir directory
cd ${umls2rdf_dir}

## run umls2rdf
${umls_venv_dir}/bin/python2.7 umls2rdf.py

## verify the output files
./checkOutputSyntax.sh  # uses "rapper" command from the "raptor" package

date
echo "================= script finished ================="
