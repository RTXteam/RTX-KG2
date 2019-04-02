#!/bin/bash
set -euxo pipefail

## setup the shell variables for various directories
CONFIG_DIR=`dirname "$0"`

source ${CONFIG_DIR}/master-config.shinc

## sym-link into RTX/code/kg2
if [ ! -L ${CODE_DIR} ]; then
    ln -s ~/RTX/code/kg2 ${CODE_DIR}
fi

## install the Linux distro packages that we need (python3-minimal is for docker installations)
sudo apt-get update
sudo apt-get install -y python3-minimal \
     python3-pip \
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
     automake

## this is for convenience when I am remote working
sudo apt-get install -y emacs

## the only python package we need to install into the native python3 is virtualenv
sudo -H pip3 install virtualenv

## create a virtualenv for building KG2
virtualenv ${VENV_DIR}

## make output directory
mkdir -p ${OUTPUT_DIR}

## Install python3 packages that we will need (Note: we are not using pymongo
## directly, but installing it silences a runtime warning from ontobio):
${VENV_DIR}/bin/pip3 install ontobio pymongo

mkdir -p ${BUILD_DIR}

## make local copies of the config files in the build dir
cp ${CODE_DIR}/curies-to-categories.yaml ${BUILD_DIR}
cp ${CODE_DIR}/curies-to-urls-lookaside-list.yaml ${BUILD_DIR}
cp ${CODE_DIR}/owl-load-inventory.yaml ${BUILD_DIR}

## install ROBOT (software: ROBOT is an OBO Tool) by downloading the jar file
## distribution and cURLing the startup script (note github uses URL redirection
## so we need the "-L" command-line option, and cURL doesn't like JAR files by
## default so we need the "application/zip")
curl -s -L -H "Accept: application/zip" https://github.com/RTXteam/robot/releases/download/v1.3.0/robot.jar > ${BUILD_DIR}/robot.jar 
curl https://raw.githubusercontent.com/RTXteam/robot/v1.3.0/bin/robot > ${BUILD_DIR}/robot
chmod +x ${BUILD_DIR}/robot

## setup owltools
curl -s -L ${BUILD_DIR} https://github.com/RTXteam/owltools/releases/download/v0.3.0/owltools > ${BUILD_DIR}/owltools
chmod +x ${BUILD_DIR}/owltools

## setup AWS CLI
if ! aws s3 cp --region ${S3_REGION} s3://${S3_BUCKET}/test /tmp/; then
    aws configure
else
    rm /tmp/test
fi

# setup raptor
wget -P ${BUILD_DIR} http://download.librdf.org/source/raptor2-2.0.15.tar.gz
rm -r -f ${BUILD_DIR}/raptor2-2.0.15
tar xzf ${BUILD_DIR}/raptor2-2.0.15.tar.gz -C ${BUILD_DIR} 
cd ${BUILD_DIR}/raptor2-2.0.15
./autogen.sh --prefix=/usr/local
make
make check
sudo make install
sudo ldconfig
