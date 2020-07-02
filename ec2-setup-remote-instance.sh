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

public_key_file=id_rsa.pub

echo "Enter path to your AWS PEM file: "
read aws_pem_file
#aws_pem_file=/Volumes/WorkEncrypted/ramseyst-new-aws-login.pem

echo "Enter hostname of your instance: "
read instance_hostname
#instance_hostname=kg2dev.rtx.ai

if ! ssh -q -o StrictHostKeyChecking=no ubuntu@${instance_hostname} exit; then
    ## remove kg2.saramsey.org from the ~/.ssh/known_hosts file
    ssh-keygen -R ${instance_hostname}
    ## copy the id_rsa.pub file to the instance
    scp -i ${aws_pem_file} \
        -o StrictHostKeyChecking=no \
        ~/.ssh/${public_key_file} \
        ubuntu@${instance_hostname}:
    ## append the id_rsa.pub file to the authorized_keys file
    ssh -i ${aws_pem_file} \
        ubuntu@${instance_hostname} \
        'cat ${public_key_file} >> ~/.ssh/authorized_keys && rm ${public_key_file}'
fi
    
## clone the RTX repo into the instance
ssh ubuntu@${instance_hostname} git clone https://github.com/RTXteam/RTX.git

ssh -t ubuntu@${instance_hostname}

