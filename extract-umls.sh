#!/usr/bin/env bash
# build-umls.sh:  download the UMLS release and convert it to a series of TTL files
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [OUTPUT_DIR]"
    exit 2
fi

# Usage: build-umls.sh [OUTPUT_DIR]

echo "================= starting build-umls.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

OUTPUT_DIR=${1:-${BUILD_DIR}}

UMLS_VER=2018AB
UMLS_FILE_BASE=${UMLS_VER}-full
UMLS_DIR=${BUILD_DIR}/umls
MMSYS_DIR=${UMLS_DIR}/${UMLS_FILE_BASE}
UMLS_DEST_DIR=${UMLS_DIR}/META
UMLS2RDF_RELEASE=rtx-2.0
UMLS2RDF_PKGNAME=umls2rdf-${UMLS2RDF_RELEASE}
UMLS2RDF_DIR=${UMLS_DIR}/${UMLS2RDF_PKGNAME}
CONFIG_FILE=${UMLS_DIR}/config.prop
MYSQL_DBNAME=umls

sudo apt-get update -y

## make directories that we need
rm -r -f ${UMLS_DIR}
mkdir -p ${UMLS_DIR}
mkdir -p ${UMLS_DEST_DIR}

## copy UMLS distribution files and MetamorphoSys config files from S3 to local dir
aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/umls-${UMLS_FILE_BASE}.zip ${UMLS_DIR}/
cp ${CODE_DIR}/umls-config.prop ${CONFIG_FILE}

## unpack UMLS and MetamorphoSys zip archives
unzip ${UMLS_DIR}/umls-${UMLS_FILE_BASE}.zip -d ${UMLS_DIR}/
unzip ${UMLS_DIR}/${UMLS_FILE_BASE}/mmsys.zip -d ${UMLS_DIR}/${UMLS_FILE_BASE}

## setup environment for running MetamorphoSys
export METADIR=${UMLS_DIR}
export DESTDIR=${UMLS_DEST_DIR}
export MMSYS_HOME=${UMLS_DIR}/${UMLS_FILE_BASE}
export CLASSPATH=${MMSYS_DIR}:${MMSYS_DIR}/lib/jpf-boot.jar
export JAVA_HOME=${MMSYS_DIR}/jre/linux
cd ${MMSYS_HOME}

## this is a workaround for a strange runtime warning I was getting from apache log4j
cp ${MMSYS_HOME}/etc/subset.log4j.properties ${MMSYS_HOME}/log4j.properties

## estimate amount of system ram, in GB
MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

## export UMLS to Rich Release Format (RRF)
${JAVA_HOME}/bin/java -Djava.awt.headless=true \
                      -Djpf.boot.config=${MMSYS_HOME}/etc/subset.boot.properties \
                      -Dinput.uri=${METADIR} \
                      -Doutput.uri=${DESTDIR} \
                      -Dmmsys.config.uri=${CONFIG_FILE} \
                      -Xms300M -Xmx${MEM_GB}G org.java.plugin.boot.Boot

MYSQL_USER=`grep 'user = ' ${MYSQL_CONF} | sed 's/user = //g'`
MYSQL_PASSWORD=`grep 'password = ' ${MYSQL_CONF} | sed 's/password = //g'`

## if a "umls" database already exists, delete it
mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "DROP DATABASE IF EXISTS ${MYSQL_DBNAME}"

## create the "umls" database
mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DBNAME} CHARACTER SET utf8 COLLATE utf8_unicode_ci"

## fill in the authentication and database variables in the shell script for populating the mysql database
cat ${UMLS_DEST_DIR}/populate_mysql_db.sh | \
    sed "s/<username>/${MYSQL_USER}/g" | \
    sed 's|<path to MYSQL_HOME>|/usr|g' | \
    sed "s/<password>/${MYSQL_PASSWORD}/g" | \
    sed "s/<db_name>/${MYSQL_DBNAME}/g" > ${UMLS_DEST_DIR}/populate_mysql_db_configured.sh

## enable the loading script to be runnable
chmod +x ${UMLS_DEST_DIR}/populate_mysql_db_configured.sh

cp ${UMLS_DEST_DIR}/mysql_tables.sql ${UMLS_DEST_DIR}/mysql_tables.sql-original
cat ${UMLS_DEST_DIR}/mysql_tables.sql-original | sed 's/\\r\\n/\\n/g' > ${UMLS_DEST_DIR}/mysql_tables.sql
cd ${UMLS_DEST_DIR} && ./populate_mysql_db_configured.sh

## download and unpack the umls2rdf software
${CURL_GET} https://github.com/RTXteam/umls2rdf/archive/${UMLS2RDF_RELEASE}.tar.gz > ${UMLS2RDF_PKGNAME}.tar.gz
tar xzf ${UMLS2RDF_PKGNAME}.tar.gz -C ${UMLS_DIR}

## make the umls2rdf config file
cat ${UMLS2RDF_DIR}/conf_sample.py | sed 's/your-host/localhost/g' | \
    sed "s/umls2015ab/${MYSQL_DBNAME}/g" | \
    sed "s/your db user/${MYSQL_USER}/g" | \
    sed "s/your db pass/${MYSQL_PASSWORD}/g" | \
    sed "s|output|${OUTPUT_DIR}|g" | \
    sed "s/2015ab/${UMLS_VER}/g" > ${UMLS2RDF_DIR}/conf.py

cp ${CODE_DIR}/umls2rdf-umls.conf ${UMLS2RDF_DIR}/umls.conf

## need libssl for installing mysqlclient; it is installed in setup-kg2-build.sh
${VENV_DIR}/bin/pip3 install mysqlclient

## change to the UMLS2RDF_DIR directory
cd ${UMLS2RDF_DIR}

## run umls2rdf
${VENV_DIR}/bin/python3 umls2rdf.py

## verify the output files
./checkOutputSyntax.sh  # uses "rapper" command from the "raptor" package

date
echo "================= script finished ================="
