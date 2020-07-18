#!/usr/bin/env bash
# setup-kg2-neo4j.sh: setup the environment for hosting the KG2 knowledge graph
# for the RTX biomedical reasoning system, in the Neo4j graph database
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

# Usage: setup-kg2-neo4j.sh

{
echo "================= starting setup-kg2.sh ================="
date

## setup the shell variables for various directories
CONFIG_DIR=`dirname "$0"`

source ${CONFIG_DIR}/master-config.shinc

## sym-link into RTX/code/kg2
if [ ! -L ${CODE_DIR} ]; then
    ln -sf ~/RTX/code/kg2 ${CODE_DIR}
fi

## install the Linux distro packages that we need (python3-minimal is for docker installations)
sudo apt-get update

## handle weird tzdata install (this makes UTC the timezone)
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata

sudo apt-get install -y python3-minimal \
     python3-pip \
     python-dev \
     awscli \
     zip \
     curl \
     software-properties-common

## this is for convenience when I am remote working
sudo apt-get install -y emacs

## the only python package we need to install into the native python3 is virtualenv
sudo -H pip3 install virtualenv

## create a virtualenv for building KG2
virtualenv ${VENV_DIR}

## Install python3 packages that we will need (Note: we are not using pymongo
## directly, but installing it silences a runtime warning from ontobio):
## (maybe we should eventually move this to a requirements.txt file?)
${VENV_DIR}/bin/pip3 install -r ${CODE_DIR}/requirements-kg2-neo4j.txt

mkdir -p ${BUILD_DIR}

} >~/setup-kg2-neo4j.log 2>&1

## setup AWS CLI
if ! aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/test /tmp/; then
    aws configure
else
    rm /tmp/test
fi


{
    bash -x ${CODE_DIR}/install-neo4j.sh
    
    date
    echo "================= script finished ================="
} >>~/setup-kg2-neo4j.log 2>&1
