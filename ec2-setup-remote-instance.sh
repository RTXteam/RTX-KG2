#!/usr/bin/env bash
# ec2-setup-remote-instance.sh:  configures an EC2 remote instance for KG2 installation (ssh key exchange, etc.)
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>
#
# NOTE: requires user input at the terminal

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

PUBLIC_KEY_FILE=id_rsa.pub

echo "Enter path to your AWS PEM file: "
read AWS_PEM_FILE
#AWS_PEM_FILE=/Volumes/WorkEncrypted/ramseyst-new-aws-login.pem

echo "Enter hostname of your instance: "
read INSTANCE_HOSTNAME
#INSTANCE_HOSTNAME=kg2dev.rtx.ai

ssh-keygen -R ${INSTANCE_HOSTNAME}

if ! ssh -q -o StrictHostKeyChecking=no ubuntu@${INSTANCE_HOSTNAME} exit
then
    ## remove kg2.saramsey.org from the ~/.ssh/known_hosts file
    ## copy the id_rsa.pub file to the instance
    scp -i ${AWS_PEM_FILE} \
        -o StrictHostKeyChecking=no \
        ~/.ssh/${PUBLIC_KEY_FILE} \
        ubuntu@${INSTANCE_HOSTNAME}:
    ## append the id_rsa.pub file to the authorized_keys file
    ssh -i ${AWS_PEM_FILE} \
        ubuntu@${INSTANCE_HOSTNAME} \
        'cat ${PUBLIC_KEY_FILE} >> ~/.ssh/authorized_keys && rm ${PUBLIC_KEY_FILE}'
fi
    
## clone the RTX repo into the instance
ssh ubuntu@${INSTANCE_HOSTNAME} git clone https://github.com/RTXteam/RTX.git

ssh -t ubuntu@${INSTANCE_HOSTNAME}

