#!/bin/bash
set -euxo pipefail

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

UMLS_FILE_BASE=2018AB-full
UMLS_DIR=${BUILD_DIR}/umls
MYSQL_USER=ubuntu
MYSQL_PASSWORD=1337
MMSYS_DIR=${UMLS_DIR}/${UMLS_FILE_BASE}
UMLS_RRDIST_DIR=${UMLS_DIR}
UMLS_DEST_DIR=${UMLS_RRDIST_DIR}/META
MYSQL_CONF=${UMLS_DIR}/mysql-config.conf

sudo apt-get update
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password ${MYSQL_PASSWORD}"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password ${MYSQL_PASSWORD}"
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
aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/umls-2018AB-full.zip ${UMLS_DIR}/
aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/umls-config.prop ${UMLS_DIR}/config.prop
aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/umls-user.b.prop ${UMLS_DIR}/user.b.prop

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

## create log4j properties file
cat >${MMSYS_HOME}/log4j.properties <<EOF
applicationRoot = .
log4j.rootLogger = ALL,console
log4j.logger.gov.nih.nlm.umls = WARN,umls
log4j.logger.org.java.plugin = ALL,console
log4j.appender.console = org.apache.log4j.ConsoleAppender
log4j.appender.console.layout = org.apache.log4j.PatternLayout
log4j.appender.console.layout.conversionPattern = %d [%t] %-5p %c %m%n
log4j.appender.umls = org.apache.log4j.ConsoleAppender
log4j.appender.umls.layout = org.apache.log4j.PatternLayout
log4j.appender.umls.layout.conversionPattern = %d [%t] %-5p %c %m%n
EOF

## export UMLS to Rich Release Format (RRF)
${JAVA_HOME}/bin/java -Djava.awt.headless=true \
                      -Djpf.boot.config=${MMSYS_HOME}/etc/subset.boot.properties \
                      -Dinput.uri=${METADIR} \
                      -Doutput.uri=${DESTDIR} \
                      -Dmmsys.config.uri=${CONFIG_FILE} \
                      -Xms300M -Xmx1000M org.java.plugin.boot.Boot

MYSQL_PWD=${MYSQL_PASSWORD} mysql -u root -e "CREATE USER 'ubuntu'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}'"
MYSQL_PWD=${MYSQL_PASSWORD} mysql -u root -e "GRANT ALL PRIVILEGES ON *.* to 'ubuntu'@'localhost'"
cat >${MYSQL_CONF} <<EOF
[client]
user = ${MYSQL_USER}
password = ${MYSQL_PASSWORD}
host = localhost
EOF

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

## download and unpack the umls2rdf software
cd ${UMLS_DIR}
curl -s -L https://github.com/RTXteam/umls2rdf/archive/umls2rdf-rtx-1.0.tar.gz > umls2rdf-rtx-1.0.tar.gz
tar xvzf umls2rdf-rtx-1.0.tar.gz
cat umls2rdf/conf_sample.py | sed 's/your-host/localhost/g' | \
    sed 's/umls2015ab/umls/g' | \
    sed 's/your db user/ubuntu/g' | \
    sed 's/your db pass/1337/g' | \
    sed 's/2015ab/2018ab/g' > umls2rdf/conf.py

## umls2rdf is legacy software written to run in python2.7
export UMLS_VENV_DIR=${UMLS_DIR}/venv27
virtualenv --python=python2.7 ${UMLS_VENV_DIR}
${UMLS_VENV_DIR}/bin/pip install mysqlclient
cd umls2rdf
${UMLS_VENV_DIR}/bin/python2.7 umls2rdf.py

cd ${UMLS_DIR}/umls2rdf
./checkOutputSyntax.sh

echo "================= script finished ================="
