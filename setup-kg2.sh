#!/bin/bash
set -euxo pipefail

## setup the shell variables for various directories
BUILD_DIR=~/kg2-build
VENV_DIR=~/kg2-venv
CODE_DIR=~/kg2-code
SNOMEDCT_FILE_BASE=SnomedCT_USEditionRF2_PRODUCTION_20180901T120000Z

## sym-link into RTX/code/kg2
ln -s ~/RTX/code/kg2 ${CODE_DIR}

## install the Linux distro packages that we need
sudo apt-get update
sudo apt-get install -y python3-minimal python3-pip default-jre awscli zip curl wget

## this is for convenience when I am remote working
sudo apt-get install -y emacs

## the only python package we need to install into the native python3 is virtualenv
sudo -H pip3 install virtualenv

## create a virtualenv for building KG2
virtualenv ${VENV_DIR}

## Install python packages that we will need (Note: we are not using pymongo
## directly, but installing it silences a runtime warning from ontobio):
${VENV_DIR}/bin/pip3 install ontobio pymongo SNOMEDToOWL

## create the "build" directory where we will store the KG2 files:
mkdir -p ${BUILD_DIR}
cd ${BUILD_DIR}

## install robot
wget https://github.com/ontodev/robot/releases/download/v1.3.0/robot.jar
curl https://raw.githubusercontent.com/ontodev/robot/master/bin/robot > robot
chmod a+x robot

## build OWL-XML representation of SNOMED CT
aws configure
aws s3 cp --region us-west-2 s3://rtx-kg2/${SNOMEDCT_FILE_BASE}.zip .
unzip ${SNOMEDCT_FILE_BASE}.zip
${VENV_DIR}/bin/SNOMEDToOWL -f xml ${SNOMEDCT_FILE_BASE}/Snapshot \
           ${VENV_DIR}/lib/python3.6/site-packages/SNOMEDCTToOWL/conf/sct_core_us_gb.json \
           -o snomed.owl
./robot relax --input snomed.owl --output snomed-relax.owl

ln -s ${CODE_DIR}/snomed-relax.owl ${BUILD_DIR}/
ln -s ${CODE_DIR}/curies-to-categories.yaml ${BUILD_DIR}/
ln -s ${CODE_DIR}/ontology-load-config.haml ${BUILD_DIR}/


## get owltools and set its permissions to executable
wget -P ${BUILD_DIR} http://build.berkeleybop.org/userContent/owltools/owltools
chmod a+x ${BUILD_DIR}/owltools
