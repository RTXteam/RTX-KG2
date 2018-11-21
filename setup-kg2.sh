#!/bin/bash
sudo apt-get update
sudo apt-get install -y python3-minimal python3-pip
sudo pip3 install virtualenv
virtualenv ~/kg2-venv
~/kg2-venv/bin/pip3 install ontobio
mkdir -p ~/kg2-build
