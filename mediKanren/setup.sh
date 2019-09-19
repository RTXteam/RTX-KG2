#!/usr/bin/env bash
# setup.sh: Setup a fresh ubuntu 18.04 system for import of the rtx kg2 into mediKanren

# Download required applications
apt-get update
apt-get install -y x11-apps 
apt-get install -y git 
apt-get install -y racket 
apt-get install -y python3-pip 
apt-get install -y python3-venv 
apt-get install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update
apt-get install -y python3.7

# Clone the repositories for kgx and mediKanren
git clone https://github.com/webyrd/mediKanren.git
git clone https://github.com/NCATS-Tangerine/kgx.git

# checkout the correct kgx branch
cd kgx
git checkout source-sink

# install python modules
python3.7 -m pip install -r requirements.txt

# Copy over the config.yml file
cd ..
cp config.yml kgx/config.yml