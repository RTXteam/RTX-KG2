#!/bin/bash

## setup the shell variables for various directories
BUILD_DIR=~/kg2-build
VENV_DIR=~/kg2-venv
CODE_DIR=~/kg2-code

## sym-link into RTX/code/kg2
ln -s ~/RTX/code/kg2 ${CODE_DIR}

## install the Linux distro packages that we need
sudo apt-get update
sudo apt-get install -y python3-minimal python3-pip default-jre
sudo -H pip3 install virtualenv

## setup a python virtualenv for building KG2
virtualenv ${VENV_DIR}

## build OWL-XML representation of SNOMED CT
${VENV_DIR}/bin/pip3 install SNOMEDToOWL
unzip SnomedCT_USEditionRF2_PRODUCTION_20180901T120000Z.zip
SNOMEDToOWL -f xml SnomedCT_USEditionRF2_PRODUCTION_20180901T120000Z/Snapshot SNOMEDToOWL/sct_core_us_gb.json -o snomed.owl
./robot relax --input snomed.owl --output snomed-relax.owl

mkdir -p ${BUILD_DIR}
cp ${CODE_DIR}/snomed-relax.owl ${BUILD_DIR}/

## we are not using pymongo but having it silences a runtime warning from ontobio:
${VENV_DIR}/bin/pip3 install ontobio pymongo

## get owltools and set its permissions to executable
wget -P ${BUILD_DIR} http://build.berkeleybop.org/userContent/owltools/owltools
chmod a+x ${BUILD_DIR}/owltools
