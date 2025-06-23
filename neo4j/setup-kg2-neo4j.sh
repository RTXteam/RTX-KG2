#!/usr/bin/env bash
# setup-kg2-neo4j.sh: setup the environment for hosting the KG2 knowledge graph
# for the RTX biomedical reasoning system, in the Neo4j graph database
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

# Usage: setup-kg2-neo4j.sh

{
echo "================= starting setup-kg2-neo4j.sh ================="
date

## setup the shell variables for various directories
config_dir=`dirname "$0"`

source ${config_dir}/master-config.shinc

## sym-link into RTX-KG2
if [ ! -L ${CODE_DIR} ]; then
    ln -sf ~/RTX-KG2 ${CODE_DIR}
fi

## install the Linux distro packages that we need (python3-minimal is for docker installations)
sudo apt-get update

## handle weird tzdata install (this makes UTC the timezone)
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

## from gcc to gfortran, these are to address the use-case of a "minimal" Ubuntu (bionic)
sudo apt-get install -y \
     awscli \
     zip \
     curl \
     software-properties-common \
     wget \
     gcc \
     g++ \
     libblas3 \
     liblapack3 \
     liblapack-dev \
     libblas-dev \
     gfortran

## this is for convenience when I am remote working
sudo apt-get install -y emacs

# we want python3.13
source ${SETUP_CODE_DIR}/setup-python313-with-pip3-in-ubuntu.shinc

## Install python3 packages that we will need (Note: we are not using pymongo
## directly, but installing it silences a runtime warning from ontobio):
## (maybe we should eventually move this to a requirements.txt file?)
${VENV_DIR}/bin/pip3 install -r ${NEO4J_CODE_DIR}/requirements-kg2-neo4j.txt

mkdir -p ${BUILD_DIR}

} >~/setup-kg2-neo4j.log 2>&1

## setup AWS CLI; this requires manual intervention so auto-logging is turned off here
if ! ${s3_cp_cmd} s3://${s3_bucket}/test-file-do-not-delete /tmp/; then
    aws configure
else
    rm -f /tmp/test-file-do-not-delete
fi

{
    bash -x ${NEO4J_CODE_DIR}/install-neo4j.sh

    # copy the RTX configuration file from S3 to ${BUILD_DIR}
    ${s3_cp_cmd} s3://${s3_bucket}/${rtx_config_file} ${BUILD_DIR}/${rtx_config_file}

} >>~/setup-kg2-neo4j.log 2>&1


# turn off auto-logging since the password is passed to this script on the command-line
kg2_neo4j_password=`${VENV_DIR}/bin/python3 ${NEO4J_CODE_DIR}/read_kg2_password_from_rtxconfig.py -c ${BUILD_DIR}/${rtx_config_file}`
sudo -u neo4j neo4j-admin set-initial-password "${kg2_neo4j_password}"
sudo service neo4j restart
sleep 20

{
    date
    echo "================= script finished ================="
} >>~/setup-kg2-neo4j.log 2>&1

