#!/bin/bash
set -euxo pipefail

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

UMLS_FILE_BASE=2018AB-full
BUILD_DIR=~/kg2-build
UMLS_DIR=${BUILD_DIR}/umls
MYSQL_USER=ubuntu
MYSQL_PASSWORD=1337
MMSYS_DIR=${UMLS_DIR}/${UMLS_FILE_BASE}
UMLS_RRDIST_DIR=${UMLS_DIR}
UMLS_DEST_DIR=${UMLS_RRDIST_DIR}/META
MYSQL_CONF=${UMLS_DIR}/mysql-config.conf

sudo apt-get update
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password your_password'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password your_password'
sudo apt-get install -y mysql-server \
     mysql-client \
     git \
     libmysqlclient-dev \
     python-dev 

## make directories that we need
mkdir -p ${UMLS_DIR}
mkdir -p ${UMLS_RRDIST_DIR}
mkdir -p ${UMLS_DEST_DIR}

## copy UMLS distribution files and MetamorphoSys config files from S3 to local dir
aws s3 cp --region ${S3_REGION} s3://${S3_BUCKET}/umls-2018AB-full.zip ${UMLS_DIR}/
aws s3 cp --region ${S3_REGION} s3://${S3_BUCKET}/umls-config.prop ${UMLS_DIR}/config.prop
aws s3 cp --region ${S3_REGION} s3://${S3_BUCKET}/umls-user.b.prop ${UMLS_DIR}/user.b.prop

## unpack UMLS and MetamorphoSys zip archives
unzip ${UMLS_DIR}/umls-${UMLS_FILE_BASE}.zip -d ${UMLS_DIR}/
unzip ${UMLS_DIR}/${UMLS_FILE_BASE}/mmsys.zip -d ${UMLS_DIR}/${UMLS_FILE_BASE}

## setup environment for running MetamorphoSys
export METADIR=${UMLS_RRDIST_DIR}
export DESTDIR=${UMLS_DEST_DIR}
export MMSYS_HOME=${UMLS_DIR}/${UMLS_FILE_BASE}
export CLASSPATH=${MMSYS_DIR}:${MMSYS_DIR}/lib/jpf-boot.jar
export JAVA_HOME=${MMSYS_DIR}/jre/linux
CONFIG_FILE=${UMLS_DIR}/config.prop
cd ${MMSYS_HOME}
## export UMLS to Rich Release Format (RRF)
${JAVA_HOME}/bin/java -Djava.awt.headless=true \
                      -Djpf.boot.config=${MMSYS_HOME}/etc/subset.boot.properties \
                      -Dlog4j.configuration=${MMSYS_HOME}/etc/subset.log4j.properties \
                      -Dinput.uri=${METADIR} \
                      -Doutput.uri=${DESTDIR} \
                      -Dmmsys.config.uri=${CONFIG_FILE} \
                      -Xms300M -Xmx1000M org.java.plugin.boot.Boot

sudo mysql -u root -e "CREATE USER 'ubuntu'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}'"
sudo mysql -u root -e "GRANT ALL PRIVILEGES ON *.* to 'ubuntu'@'localhost'"
cat >${MYSQL_CONF} <<EOL
[client]
user = ${MYSQL_USER}
password = ${MYSQL_PASSWORD}
host = localhost
EOL

mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "CREATE DATABASE IF NOT EXISTS umls CHARACTER SET utf8 COLLATE utf8_unicode_ci"

mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "set global local_infile=1"

cat ${UMLS_DEST_DIR}/populate_mysql_db.sh | \
    sed 's/<username>/ubuntu/g' | \
    sed 's|<path to MYSQL_HOME>|/usr|g' | \
    sed "s/<password>/${MYSQL_PASSWORD}/g" | \
    sed 's/<db_name>/umls/g' > ${UMLS_DEST_DIR}/populate_mysql_db_configured.sh

chmod +x ${UMLS_DEST_DIR}/populate_mysql_db_configured.sh

cp ${UMLS_DEST_DIR}/mysql_tables.sql ${UMLS_DEST_DIR}/mysql_tables.sql-original
cat ${UMLS_DEST_DIR}/mysql_tables.sql-original | sed 's/\\r\\n/\\n/g' > ${UMLS_DEST_DIR}/mysql_tables.sql
${UMLS_DEST_DIR}/populate_mysql_db_configured.sh

cd ${UMLS_DIR}
curl -s -L https://github.com/RTXteam/umls2rdf/archive/umls2rdf-rtx-1.0.tar.gz > umls2rdf-rtx-1.0.tar.gz
tar xvzf umls2rdf-rtx-1.0.tar.gz
cat umls2rdf/conf_sample.py | sed 's/your-host/localhost/g' | \
    sed 's/umls2015ab/umls/g' | \
    sed 's/your db user/ubuntu/g' | \
    sed 's/your db pass/1337/g' | \
    sed 's/2015ab/2018ab/g' > umls2rdf/conf.py

export UMLS_VENV_DIR=${UMLS_DIR}/venv27
virtualenv --python=python2.7 ${UMLS_VENV_DIR}
${UMLS_VENV_DIR}/bin/pip install mysqlclient
cd umls2rdf
${UMLS_VENV_DIR}/bin/python2.7 umls2rdf.py

cd ${UMLS_DIR}/umls2rdf
./checkOutputSyntax.sh
