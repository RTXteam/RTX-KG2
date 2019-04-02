#!/bin/bash
set -euxo pipefail

## setup the shell variables for various directories
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

rm -r -f ${BUILD_DIR}
rm -r -f ${CODE_DIR}
rm -r -f ${VENV_DIR}
rm -r -f ${OUTPUT_DIR}
rm -r -f ~/RTX

sudo apt-get purge -y mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-*
sudo rm -rf /etc/mysql /var/lib/mysql
sudo apt-get -y autoremove
sudo apt-get -y autoclean
rm -r -f ~/.cachier
