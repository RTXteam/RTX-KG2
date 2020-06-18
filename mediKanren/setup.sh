#!/usr/bin/env bash
# setup.sh: Setup a fresh ubuntu 18.04 system for import of the rtx kg2 into mediKanren

set -o nounset -o pipefail -o errexit

# Download required applications
sudo apt-get update
sudo apt-get install -y x11-apps 
sudo apt-get install -y git 
sudo apt-get install -y racket 
sudo apt-get install -y python3-pip 
sudo apt-get install -y python3-venv 
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.7

# Clone the repositories for kgx and mediKanren
git clone https://github.com/RTXteam/mediKanren.git
git clone https://github.com/RTXteam/kgx.git

# checkout the correct kgx branch
cd kgx
git checkout source-sink

# install python modules
python3.7 -m pip install -r requirements.txt

# Copy over the config.yml file
cd ..
cp config.yml kgx/config.yml
