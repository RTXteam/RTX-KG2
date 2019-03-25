#!/bin/bash
set -euxo pipefail

S3_REGION=us-west-2
S3_BUCKET=rtx-kg2
UMLS_FILE_BASE=2018AB-full
BUILD_DIR=~/kg2-build
UMLS_DIR=${BUILD_DIR}/umls
VENV_DIR=~/kg2-venv
MYSQL_PASSWORD=1337
MMSYS_DIR=${UMLS_DIR}/${UMLS_FILE_BASE}
UMLS_RRDIST_DIR=${UMLS_DIR}
UMLS_DEST_DIR=${UMLS_RRDIST_DIR}/METASUBSET

## build UMLS

# mkdir -p ${UMLS_DIR}
mkdir -p ${UMLS_RRDIST_DIR}
mkdir -p ${UMLS_DEST_DIR}

# aws s3 cp --region ${S3_REGION} s3://${S3_BUCKET}/umls-2018AB-full.zip ${UMLS_DIR}/
aws s3 cp --region ${S3_REGION} s3://${S3_BUCKET}/umls-config.prop ${UMLS_DIR}/config.prop
# unzip ${UMLS_DIR}/umls-${UMLS_FILE_BASE}.zip -d ${UMLS_DIR}/
# unzip ${UMLS_DIR}/${UMLS_FILE_BASE}/mmsys.zip -d ${UMLS_DIR}/${UMLS_FILE_BASE}

# sudo apt-get install -y mysql-server mysql-client
sudo mysql -u root -e CREATE USER 'ubuntu'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}'
mysql -u ubuntu -p ${MYSQL_PASSWORD} -e CREATE DATABASE IF NOT EXISTS umls CHARACTER SET utf8 COLLATE utf8_unicode_ci
mysql -u ubuntu -p ${MYSQL_PASSWORD} -e set global local_infile=1

export METADIR=${UMLS_RRDIST_DIR}
export DESTDIR=${UMLS_DEST_DIR}
export MMSYS_HOME=${UMLS_DIR}/{UMLS_FILE_BASE}
export CLASSPATH=${MMSYS_DIR}:${MMSYS_DIR}/lib/jpf-boot.jar
export JAVA_HOME=${MMSYS_DIR}/jre/linux
CONFIG_FILE=${UMLS_DIR}/config.prop

cd ${MMSYS_HOME}

${JAVA_HOME}/bin/java -Djava.awt.headless=true \
                      -Djpf.boot.config=${MMSYS_HOME}/etc/subset.boot.properties \
                      -Dlog4j.configuration=${MMSYS_HOME}/etc/subset.log4j.properties \
                      -Dinput.uri=${METADIR} \
                      -Doutput.uri=${DESTDIR} \
                      -Dmmsys.config.uri=${CONFIG_FILE} \
                      -Xms300M -Xmx1000M org.java.plugin.boot.Boot

