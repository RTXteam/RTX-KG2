#!/usr/bin/env bash
# clear-instance.sh:  clears out an Ubuntu EC2 instance so that you can reinstall the KG2 build system from scratch
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>
#
# DANGEROUS: this script wipes an Ubuntu EC2 instance clean

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

## setup the shell variables for various directories
config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

read -p "Are you sure you are running this command in the KG2 build instance and not on your laptop? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
    cd ~
    bash -x ${CODE_DIR}/delete-mysql-ubuntu.sh
    rm -r -f ${BUILD_DIR}
    rm -r -f ${CODE_DIR}
    rm -r -f ${VENV_DIR}
    rm -r -f ~/RTX
    rm -r -f ~/.cachier
    rm -r -f ~/*.log
fi

echo "================= script finished ================="
