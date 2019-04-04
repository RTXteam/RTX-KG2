#!/bin/bash
set -euxo pipefail

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

UMLS_VER=2018AB
UMLS_FILE_BASE=${UMLS_VER}-full
UMLS_DIR=${BUILD_DIR}/umls
MYSQL_USER=ubuntu
MYSQL_PASSWORD=1337
MYSQL_DBNAME=umls
MMSYS_DIR=${UMLS_DIR}/${UMLS_FILE_BASE}
UMLS_RRDIST_DIR=${UMLS_DIR}
UMLS_DEST_DIR=${UMLS_RRDIST_DIR}/META
MYSQL_CONF=${UMLS_DIR}/mysql-config.conf
UMLS2RDF_RELEASE=rtx-1.0
UMLS2RDF_PKGNAME=umls2rdf-${UMLS2RDF_RELEASE}
UMLS2RDF_DIR=${UMLS_DIR}/${UMLS2RDF_PKGNAME}

sudo apt-get update -y
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
aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/umls-${UMLS_FILE_BASE}.zip ${UMLS_DIR}/
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

## this is a workaround for a strange runtime warning I was getting from apache log4j
cp ${MMSYS_HOME}/etc/subset.log4j.properties ${MMSYS_HOME}/log4j.properties

## estimate amount of system ram, in GB
MEM_BYTES=`cat /proc/meminfo | grep MemTotal | cut -f2 -d\: | cut -f1 -dk | sed 's/ //g'`
DIVISOR=1048576
MEM_GB=$((MEM_BYTES/DIVISOR))


## export UMLS to Rich Release Format (RRF)
${JAVA_HOME}/bin/java -Djava.awt.headless=true \
                      -Djpf.boot.config=${MMSYS_HOME}/etc/subset.boot.properties \
                      -Dinput.uri=${METADIR} \
                      -Doutput.uri=${DESTDIR} \
                      -Dmmsys.config.uri=${CONFIG_FILE} \
                      -Xms300M -Xmx${MEM_GB}G org.java.plugin.boot.Boot

MYSQL_PWD=${MYSQL_PASSWORD} mysql -u root -e "CREATE USER '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}'"
MYSQL_PWD=${MYSQL_PASSWORD} mysql -u root -e "GRANT ALL PRIVILEGES ON *.* to '${MYSQL_USER}'@'localhost'"
cat >${MYSQL_CONF} <<EOF
[client]
user = ${MYSQL_USER}
password = ${MYSQL_PASSWORD}
host = localhost
EOF

## create the "umls" database
mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "CREATE DATABASE IF NOT EXISTS ${MYSQL_DBNAME} CHARACTER SET utf8 COLLATE utf8_unicode_ci"

## set mysql server variable to allow loading data from a local file
mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "set global local_infile=1"

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
curl -s -L https://github.com/RTXteam/umls2rdf/archive/${UMLS2RDF_RELEASE}.tar.gz > ${UMLS2RDF_PKGNAME}.tar.gz
tar xzf ${UMLS2RDF_PKGNAME}.tar.gz -C ${UMLS_DIR}

## make the umls2rdf config file
cat ${UMLS2RDF_DIR}/conf_sample.py | sed 's/your-host/localhost/g' | \
    sed "s/umls2015ab/${MYSQL_DBNAME}/g" | \
    sed "s/your db user/${MYSQL_USER}/g" | \
    sed "s/your db pass/${MYSQL_PASSWORD}/g" | \
    sed "s/2015ab/${UMLS_VER}/g" > ${UMLS2RDF_DIR}/conf.py

## umls2rdf is legacy software written to run in python2.7; set up the virtualenv
UMLS_VENV_DIR=${UMLS_DIR}/venv27
virtualenv --python=python2.7 ${UMLS_VENV_DIR}
${UMLS_VENV_DIR}/bin/pip install mysqlclient

## run umls2rdf
cd ${UMLS2RDF_DIR}
${UMLS_VENV_DIR}/bin/python2.7 umls2rdf.py
./checkOutputSyntax.sh

## convert files from Turtle format to OWL/RDF format
for ttl_file_name in `ls ${UMLS2RDF_DIR}/output/*.ttl`
do
    file_path_no_ext=${ttl_file_name%.*}
    file_name_no_ext=`basename ${file_path_no_ext}`
    ${BUILD_DIR}/robot convert --input ${ttl_file_name} --output /tmp/${file_name_no_ext}.owl
    mv /tmp/${file_name_no_ext}.owl ${file_path_no_ext}.owl
done

## merge the UMLS OWL files into a single umls.owl file
OWLTOOLS_MEMORY=${MEM_GB}G ${BUILD_DIR}/owltools $(ls ${UMLS2RDF_DIR}/output/*.owl) \
               --merge-support-ontologies -o ${BUILD_DIR}/umls.owl

echo "================= script finished ================="
