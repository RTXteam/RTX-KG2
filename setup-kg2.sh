#!/bin/bash
set -euxo pipefail

## setup the shell variables for various directories
BUILD_DIR=~/kg2-build
VENV_DIR=~/kg2-venv
CODE_DIR=~/kg2-code
SNOMEDCT_FILE_BASE=SnomedCT_USEditionRF2_PRODUCTION_20180901T120000Z
S3_REGION=us-west-2
S3_BUCKET=rtx-kg2

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

## Install python3 packages that we will need (Note: we are not using pymongo
## directly, but installing it silences a runtime warning from ontobio):
${VENV_DIR}/bin/pip3 install ontobio pymongo SNOMEDToOWL

## create the "build" directory where we will store the KG2 files:
mkdir -p ${BUILD_DIR}

## make local copies of the config files in the build dir
cp ${CODE_DIR}/curies-to-categories.yaml ${BUILD_DIR}
cp ${CODE_DIR}/owl-load-inventory.yaml ${BUILD_DIR}

## install ROBOT (software: ROBOT is an OBO Tool) by downloading the jar file
## distribution and cURLing the startup script
wget -P ${BUILD_DIR} https://github.com/ontodev/robot/releases/download/v1.3.0/robot.jar
curl https://raw.githubusercontent.com/ontodev/robot/master/bin/robot > ${BUILD_DIR}/robot
chmod a+x ${BUILD_DIR}/robot

## get owltools and set its permissions to executable
wget -P ${BUILD_DIR} http://build.berkeleybop.org/userContent/owltools/owltools
chmod a+x ${BUILD_DIR}/owltools

## build OWL-XML representation of SNOMED CT
if ! aws s3 cp --region ${S3_REGION} s3://${S3_BUCKET}/test .; then
    aws configure
else
    rm test
fi
aws s3 cp --region ${S3_REGION} s3://${S3_BUCKET}/${SNOMEDCT_FILE_BASE}.zip ${BUILD_DIR}/
unzip ${BUILD_DIR}/${SNOMEDCT_FILE_BASE}.zip -d ${BUILD_DIR}
${VENV_DIR}/bin/SNOMEDToOWL -f xml ${BUILD_DIR}/${SNOMEDCT_FILE_BASE}/Snapshot \
           ${VENV_DIR}/lib/python3.6/site-packages/SNOMEDCTToOWL/conf/sct_core_us_gb.json \
           -o ${BUILD_DIR}/snomed.owl
${BUILD_DIR}/robot relax --input ${BUILD_DIR}/snomed.owl --output ${BUILD_DIR}/snomed-relax.owl

