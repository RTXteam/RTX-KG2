#!/usr/bin/env bash
# setup-kg2.sh:  setup the environment for building the KG2 knowledge graph for the RTX biomedical reasoning system
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

# Options:
# ./setup-kg2-build.sh ci   Accommodate Travis CI's special runtime environment

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [ci]" 
    exit 2
fi

# Usage: setup-kg2-build.sh [ci]

build_flag=${1:-""}

## setup the shell variables for various directories
config_dir=`dirname "$0"`
if [[ "${build_flag}" == "ci" ]]
then
    sed -i "\@CODE_DIR=~/kg2-code@cCODE_DIR=/home/runner/work/RTX-KG2/RTX-KG2/RTX-KG2" ${config_dir}/master-config.shinc
fi
source ${config_dir}/master-config.shinc

mysql_user=ubuntu
mysql_password=1337
if [[ "${build_flag}" != "ci" ]]
then
    psql_user=ubuntu
fi

mkdir -p ${BUILD_DIR}
setup_log_file=${BUILD_DIR}/setup-kg2-build.log
touch ${setup_log_file}

if [[ "${build_flag}" == "ci" ]]
then
    trap "cat ${setup_log_file}" EXIT
fi

function setup_kg2_build_part1 () {
echo "================= starting setup-kg2-build.sh ================="
date

echo `hostname`

## sym-link into RTX-KG2/
if [ ! -L ${CODE_DIR} ]; then
    if [[ "${build_flag}" != "ci" ]]
    then
        ln -sf ~/RTX-KG2 ${CODE_DIR}
    fi
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
     libssl-dev \
     make

sudo debconf-set-selections <<< "mysql-server mysql-server/root_password password ${mysql_password}"
sudo debconf-set-selections <<< "mysql-server mysql-server/root_password_again password ${mysql_password}"

sudo apt-get install -y mysql-server \
     mysql-client \
     libmysqlclient-dev \
     python3-mysqldb

sudo service mysql start
if [[ "${build_flag}" != "ci" ]]
then
    ## this is for convenience when I am remote working
    sudo apt-get install -y emacs
fi

# we want python3.7 (also need python3.7-dev or else pip cannot install the python package "mysqlclient")
source ${SETUP_CODE_DIR}/setup-python37-with-pip3-in-ubuntu.shinc
${VENV_DIR}/bin/pip3 install -r ${SETUP_CODE_DIR}/requirements-kg2-build.txt

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
}

function setup_kg2_build_part2 () {
if [[ "${build_flag}" != "ci" ]]
then
    # setup MySQL
    MYSQL_PWD=${mysql_password} mysql -u root -e "CREATE USER IF NOT EXISTS '${mysql_user}'@'localhost' IDENTIFIED BY '${mysql_password}'"
    MYSQL_PWD=${mysql_password} mysql -u root -e "GRANT ALL PRIVILEGES ON *.* to '${mysql_user}'@'localhost'"

    cat >${mysql_conf} <<EOF
[client]
user = ${mysql_user}
password = ${mysql_password}
host = localhost
[mysqld]
skip-log-bin
EOF

    ## set mysql server variable to allow loading data from a local file
    mysql --defaults-extra-file=${mysql_conf} \
          -e "set global local_infile=1"

    ## setup PostGreSQL
    sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    sudo apt-get update
    sudo apt-get -y install postgresql
    
    # Addresses permission issues
    # https://stackoverflow.com/questions/38470952/postgres-can-not-change-directory-in-ubuntu-14-04
    cd ~postgres/

    sudo -u postgres psql -c "DO \$do\$ BEGIN IF NOT EXISTS ( SELECT FROM pg_catalog.pg_roles WHERE rolname = '${psql_user}' ) THEN CREATE ROLE ${psql_user} LOGIN PASSWORD null; END IF; END \$do\$;"
    sudo -u postgres psql -c "ALTER USER ${psql_user} WITH password null"
else
    export PATH=$PATH:${BUILD_DIR}
fi

date

echo "================= script finished ================="
}

setup_kg2_build_part1 > ${setup_log_file} 2>&1

if [[ "${build_flag}" != "ci" ]]
then
    ## setup AWS CLI
    if ! ${s3_cp_cmd} s3://${s3_bucket}/test-file-do-not-delete /tmp/; then
        aws configure
    else
        rm -f /tmp/test-file-do-not-delete
    fi
fi

setup_kg2_build_part2 >> ${setup_log_file} 2>&1

if [[ "${build_flag}" != "ci" ]]
then
    ${s3_cp_cmd} ${setup_log_file} s3://${s3_bucket_versioned}/
fi

cat master-config.shinc
cat ../master-config.shinc
cat ../validate/master-config.shinc