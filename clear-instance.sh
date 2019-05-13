#!/bin/bash
set -euxo pipefail

## DANGER: this script wipes an Ubuntu EC2 instance clean

## setup the shell variables for various directories
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

read -p "Are you sure you are running this command in the KG2 build instance and not on your laptop? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    cd ~
    rm -r -f ${BUILD_DIR}
    rm -r -f ${CODE_DIR}
    rm -r -f ${VENV_DIR}
    rm -r -f ~/RTX
    sudo apt-get purge -y mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-*
    sudo rm -rf /etc/mysql /var/lib/mysql
    sudo apt-get -y autoremove
    sudo apt-get -y autoclean
    rm -r -f ~/.cachier
    rm -r -f ~/*.log
fi

echo "================= script finished ================="
