#!/bin/bash
sudo apt-get update
sudo apt-get install -y python3-minimal python3-pip
sudo pip3 install virtualenv
virtualenv ~/kg2
~/kg2/bin/pip3 install ontobio
