#!/usr/bin/env bash
# setup-kg2.sh:  setup the environment for building the KG2 knowledge graph for the RTX biomedical reasoning system
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

# Usage: setup-kg2-build.sh
echo "================= starting setup-kg2.sh ================="

## setup the shell variables for various directories
CONFIG_DIR=`dirname "$0"`

MYSQL_USER=ubuntu
MYSQL_PASSWORD=1337

source ${CONFIG_DIR}/master-config.shinc
SETUP_LOG_FILE=${BUILD_DIR}/setup-kg2-build.log
mkdir -p ${BUILD_DIR}

date

## sym-link into RTX/code/kg2
if [ ! -L ${CODE_DIR} ]; then
    ln -sf ~/RTX/code/kg2 ${CODE_DIR}
fi

## install the Linux distro packages that we need (python3-minimal is for docker installations)
sudo apt-get update
sudo apt-get install -y python3-minimal \
     python3-pip \
     python-dev \
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

## the only python package we need to install into the native python3 is virtualenv
sudo -H pip3 install virtualenv

## create a virtualenv for building KG2
virtualenv ${VENV_DIR}

## Install python3 packages that we will need (Note: we are not using pymongo
## directly, but installing it silences a runtime warning from ontobio):
## (maybe we should eventually move this to a requirements.txt file?)
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

## setup AWS CLI
if ! aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/test /tmp/; then
    aws configure
else
    rm /tmp/test
fi

# setup raptor (used by the "checkOutputSyntax.sh" script in the umls2rdf package)
wget -nv -P ${BUILD_DIR} http://download.librdf.org/source/raptor2-2.0.15.tar.gz
rm -r -f ${BUILD_DIR}/raptor2-2.0.15
tar xzf ${BUILD_DIR}/raptor2-2.0.15.tar.gz -C ${BUILD_DIR} 
cd ${BUILD_DIR}/raptor2-2.0.15
./autogen.sh --prefix=/usr/local
make
make check
sudo make install
sudo ldconfig

# setup MySQL
MYSQL_PWD=${MYSQL_PASSWORD} mysql -u root -e "CREATE USER '${MYSQL_USER}'@'localhost' IDENTIFIED BY '${MYSQL_PASSWORD}'"
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
