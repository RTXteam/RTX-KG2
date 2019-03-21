#!/bin/bash
INSTANCE_HOSTNAME=kg2.saramsey.org
PUBLIC_KEY_FILE=id_rsa.pub
AWS_PEM_FILE=/Volumes/WorkEncrypted/ramseyst-new-aws-login.pem

## remove kg2.saramsey.org from the ~/.ssh/known_hosts file
ssh-keygen -R ${INSTANCE_HOSTNAME}

## copy the id_rsa.pub file to the instance
scp -i ${AWS_PEM_FILE} \
    -o StrictHostKeyChecking=no \
    ~/.ssh/${PUBLIC_KEY_FILE} \
    ubuntu@${INSTANCE_HOSTNAME}:

ssh -i /Volumes/WorkEncrypted/ramseyst-new-aws-login.pem \
    ubuntu@${INSTANCE_HOSTNAME} \
    'cat ${PUBLIC_KEY_FILE} >> ~/.ssh/authorized_keys && rm ${PUBLIC_KEY_FILE}'

ssh ubuntu@${INSTANCE_HOSTNAME} git clone https://github.com/RTXteam/RTX.git

