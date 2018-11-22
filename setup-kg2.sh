#!/bin/bash
BUILD_DIR=~/kg2-build
VENV_DIR=~/kg2-venv
CODE_DIR=~/kg2-code
ln -s ~/RTX/code/kg2 ${CODE_DIR}
sudo apt-get update
sudo apt-get install -y python3-minimal python3-pip default-jre
sudo -H pip3 install virtualenv
virtualenv ${VENV_DIR}
${VENV_DIR}/bin/pip3 install ontobio
mkdir -p ${BUILD_DIR}
cp ${CODE_DIR}/snomed.owl ${BUILD_DIR}/
cp ${CODE_DIR}/biolink-model--updated-for-kg2.yaml ${BUILD_DIR}/
wget -P ${BUILD_DIR} http://build.berkeleybop.org/userContent/owltools/owltools
chmod a+x ${BUILD_DIR}/owltools
