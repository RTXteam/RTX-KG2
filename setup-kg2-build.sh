#!/usr/bin/env bash
# setup-kg2.sh:  setup the environment for building the KG2 knowledge graph for the RTX biomedical reasoning system
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

# Usage: setup-kg2-build.sh


## setup the shell variables for various directories
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

MYSQL_USER=ubuntu
MYSQL_PASSWORD=1337

mkdir -p ${BUILD_DIR}
SETUP_LOG_FILE=${BUILD_DIR}/setup-kg2-build.log

{
echo "================= starting setup-kg2.sh ================="
date

## sym-link into RTX/code/kg2
if [ ! -L ${CODE_DIR} ]; then
    ln -sf ~/RTX/code/kg2 ${CODE_DIR}
fi

## install the Linux distro packages that we need (python3-minimal is for docker installations)
sudo apt-get update

## handle weird tzdata install (this makes UTC the timezone)
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

# we want python3.7 (also need python3.7-dev or else pip cannot install the python package "mysqlclient")
sudo apt-get install -y python3.7 python3.7-dev python3.7-venv

# install various other packages used by the build system
#  - curl is generally used for HTTP downloads
#  - wget is used by the neo4j installation script (some special "--no-check-certificate" mode)
sudo apt-get install -y \
     default-jre \
     awscli \
     zip \
     curl \
     wget \
     flex \
     bison \
     libxml2-dev \
     gtk-doc-tools \
     libtool \
     automake \
     git \
     libssl-dev
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password ${MYSQL_PASSWORD}"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password ${MYSQL_PASSWORD}"
sudo apt-get install -y mysql-server \
     mysql-client \
     libmysqlclient-dev

## this is for convenience when I am remote working
sudo apt-get install -y emacs

# some shenanigans required in order to install pip into python3.7 (not into python3.6!)
curl -s https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
apt-get download python3-distutils
mv python3-distutils_3.6.9-1~18.04_all.deb /tmp
sudo dpkg-deb -x /tmp/python3-distutils_3.6.9-1~18.04_all.deb /
sudo python3.7 /tmp/get-pip.py

## create a virtualenv for building KG2
python3.7 -m venv ${VENV_DIR}

## Install python3 packages that we will need (Note: we are not using pymongo
## directly, but installing it silences a runtime warning from ontobio):
## (maybe we should eventually move this to a requirements.txt file?)
${VENV_DIR}/bin/pip3 install wheel
${VENV_DIR}/bin/pip3 install -r ${CODE_DIR}/requirements-kg2-build.txt

## install ROBOT (software: ROBOT is an OBO Tool) by downloading the jar file
## distribution and cURLing the startup script (note github uses URL redirection
## so we need the "-L" command-line option, and cURL doesn't like JAR files by
## default so we need the "application/zip")
${CURL_GET} -H "Accept: application/zip" https://github.com/RTXteam/robot/releases/download/v1.3.0/robot.jar > ${BUILD_DIR}/robot.jar 
curl -s https://raw.githubusercontent.com/RTXteam/robot/v1.3.0/bin/robot > ${BUILD_DIR}/robot
chmod +x ${BUILD_DIR}/robot

## setup owltools
${CURL_GET} ${BUILD_DIR} https://github.com/RTXteam/owltools/releases/download/v0.3.0/owltools > ${BUILD_DIR}/owltools
chmod +x ${BUILD_DIR}/owltools
} >${SETUP_LOG_FILE} 2>&1

## setup AWS CLI
if ! aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/test /tmp/; then
    aws configure
else
    rm /tmp/test
fi

{
RAPTOR_NAME=raptor2-2.0.15
# setup raptor (used by the "checkOutputSyntax.sh" script in the umls2rdf package)
${CURL_GET} -o ${BUILD_DIR}/${RAPTOR_NAME}.tar.gz http://download.librdf.org/source/${RAPTOR_NAME}.tar.gz
rm -r -f ${BUILD_DIR}/${RAPTOR_NAME}
tar xzf ${BUILD_DIR}/${RAPTOR_NAME}.tar.gz -C ${BUILD_DIR} 
cd ${BUILD_DIR}/${RAPTOR_NAME}
./autogen.sh --prefix=/usr/local
make
make check
sudo make install
sudo ldconfig

# setup MySQL
MYSQL_PWD=${MYSQL_PASSWORD} mysql -u root -e "CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}'"
MYSQL_PWD=${MYSQL_PASSWORD} mysql -u root -e "GRANT ALL PRIVILEGES ON *.* to '${MYSQL_USER}'@'localhost'"
cat >${MYSQL_CONF} <<EOF
[client]
user = ${MYSQL_USER}
password = ${MYSQL_PASSWORD}
host = localhost
EOF

## set mysql server variable to allow loading data from a local file
mysql --defaults-extra-file=${MYSQL_CONF} \
      -e "set global local_infile=1"

date

echo "================= script finished ================="
} >> ${SETUP_LOG_FILE} 2>&1

${S3_CP_CMD} ${SETUP_LOG_FILE} s3://${S3_BUCKET_PUBLIC}/
