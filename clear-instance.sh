#!/bin/bash
set -euxo pipefail

## setup the shell variables for various directories
CONFIG_DIR=`dirname \"$0\"`
source ${CONFIG_DIR}/master-config.shinc

rm -r -f ${BUILD_DIR}
rm -r -f ${CODE_DIR}
rm -r -f ${VENV_DIR}

sudo apt-get purge mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-*
sudo rm -rf /etc/mysql /var/lib/mysql
sudo apt-get autoremove
sudo apt-get autoclean

