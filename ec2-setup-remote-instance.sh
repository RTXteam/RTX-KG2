#!/bin/bash
set -euxo pipefail

INSTANCE_HOSTNAME=kg2dev.saramsey.org
PUBLIC_KEY_FILE=id_rsa.pub
AWS_PEM_FILE=/Volumes/WorkEncrypted/ramseyst-new-aws-login.pem

if ! ssh -q -o StrictHostKeyChecking=no ubuntu@${INSTANCE_HOSTNAME} exit; then
    ## remove kg2.saramsey.org from the ~/.ssh/known_hosts file
    ssh-keygen -R ${INSTANCE_HOSTNAME}
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

