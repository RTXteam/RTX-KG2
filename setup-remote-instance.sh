#!/bin/bash

## remove kg2.saramsey.org from the ~/.ssh/known_hosts file
ssh-keygen -R kg2.saramsey.org

scp -i /Volumes/WorkEncrypted/ramseyst-new-aws-login.pem \
    -o StrictHostKeyChecking=no \
    ~/.ssh/id_rsa.pub \
    ubuntu@kg2.saramsey.org:

ssh -i /Volumes/WorkEncrypted/ramseyst-new-aws-login.pem \
    ubuntu@kg2.saramsey.org \
    'cat id_rsa.pub >> ~/.ssh/authorized_keys && rm id_rsa.pub'

