#!/usr/bin/env bash
# setup-kg2.sh:  setup the environment for building the KG2 knowledge graph for the RTX biomedical reasoning system
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [travisci]" 
    exit 2
fi

# Usage: setup-kg2-build.sh [travisci]

build_flag=${1:-""}

## setup the shell variables for various directories
config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

mysql_user=ubuntu
mysql_password=1337
if [[ "${build_flag}" != "travisci" ]]
then

    psql_user=ubuntu
fi

mkdir -p ${BUILD_DIR}
setup_log_file=${BUILD_DIR}/setup-kg2-build.log

{
echo "================= starting setup-kg2.sh ================="
date

echo `hostname`

## sym-link into RTX/code/kg2
if [ ! -L ${CODE_DIR} ]; then
    ln -sf ~/RTX/code/kg2 ${CODE_DIR}
fi

## install the Linux distro packages that we need (python3-minimal is for docker installations)
sudo apt-get update

## handle weird tzdata install (this makes UTC the timezone)
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

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

sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password ${mysql_password}"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password ${mysql_password}"

sudo apt-get install -y mysql-server \
     mysql-client \
     libmysqlclient-dev \
     python3-mysqldb

sudo service mysql start
if [[ "${build_flag}" != "travisci" ]]
then
    ## this is for convenience when I am remote working
    sudo apt-get install -y emacs
fi

# we want python3.7 (also need python3.7-dev or else pip cannot install the python package "mysqlclient")
source ${CODE_DIR}/setup-python37-in-ubuntu18.shinc

${VENV_DIR}/bin/pip3 install -r ${CODE_DIR}/requirements-kg2-build.txt

## install ROBOT (software: ROBOT is an OBO Tool) by downloading the jar file
## distribution and cURLing the startup script (note github uses URL redirection
## so we need the "-L" command-line option, and cURL doesn't like JAR files by
## default so we need the "application/zip")
${curl_get} -H "Accept: application/zip" https://github.com/RTXteam/robot/releases/download/v1.3.0/robot.jar > ${BUILD_DIR}/robot.jar 
curl -s https://raw.githubusercontent.com/RTXteam/robot/v1.3.0/bin/robot > ${BUILD_DIR}/robot
chmod +x ${BUILD_DIR}/robot

## setup owltools
${curl_get} ${BUILD_DIR} https://github.com/RTXteam/owltools/releases/download/v0.3.0/owltools > ${BUILD_DIR}/owltools
chmod +x ${BUILD_DIR}/owltools

} >${setup_log_file} 2>&1

if [[ "${build_flag}" != "travisci" ]]
then
    ## setup AWS CLI
    if ! ${s3_cp_cmd} s3://${s3_bucket}/test-file-do-not-delete /tmp/; then
        aws configure
    else
        rm -f /tmp/test-file-do-not-delete
    fi
fi

{
RAPTOR_NAME=raptor2-2.0.15
# setup raptor (used by the "checkOutputSyntax.sh" script in the umls2rdf package)
${curl_get} -o ${BUILD_DIR}/${RAPTOR_NAME}.tar.gz http://download.librdf.org/source/${RAPTOR_NAME}.tar.gz
rm -r -f ${BUILD_DIR}/${RAPTOR_NAME}
tar xzf ${BUILD_DIR}/${RAPTOR_NAME}.tar.gz -C ${BUILD_DIR} 
cd ${BUILD_DIR}/${RAPTOR_NAME}
./autogen.sh --prefix=/usr/local
make
make check
sudo make install
sudo ldconfig

if [[ "${build_flag}" != "travisci" ]]
then
    # setup MySQL
    MYSQL_PWD=${mysql_password} mysql -u root -e "CREATE USER '${mysql_user}'@'localhost' IDENTIFIED BY '${mysql_password}'"
    MYSQL_PWD=${mysql_password} mysql -u root -e "GRANT ALL PRIVILEGES ON *.* to '${mysql_user}'@'localhost'"

    cat >${mysql_conf} <<EOF
[client]
user = ${mysql_user}
password = ${mysql_password}
host = localhost
EOF

    ## set mysql server variable to allow loading data from a local file
    mysql --defaults-extra-file=${mysql_conf} \
          -e "set global local_infile=1"

    ## setup PostGreSQL
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt-get update
    sudo apt-get -y install postgresql
    sudo -u postgres createuser ${psql_user}
    sudo -u postgres psql -c "ALTER USER ${psql_user} WITH password null"
fi

if [[ "${build_flag}" == "travisci" ]]
then
    export PATH=$PATH:${BUILD_DIR}
fi

date

echo "================= script finished ================="
} >> ${setup_log_file} 2>&1

if [[ "${build_flag}" != "travisci" ]]
then
    ${s3_cp_cmd} ${setup_log_file} s3://${s3_bucket_versioned}/
fi