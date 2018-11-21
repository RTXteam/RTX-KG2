#!/bin/bash
apt-get update
apt-get install -y python3-minimal python3-pip git
pip3 install virtualenv
useradd rtx -m -s /bin/bash

