#!/bin/bash
# install neo4j into an Ubuntu 18.04 instance
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

sudo apt-get update -y
sudo apt-get install -y emacs
wget --no-check-certificate -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
echo 'deb http://debian.neo4j.org/repo stable/' > neo4j.list
sudo mv neo4j.list /etc/apt/sources.list.d/neo4j.list
sudo apt-get update -y
sudo apt-get install -y neo4j
sudo cp /etc/neo4j/neo4j.conf /etc/neo4j/neo4j.conf.ori
cat /etc/neo4j/neo4j.conf.ori | sed 's/#dbms.connectors.default_listen_address/dbms.connectors.default_listen_address/g' > /tmp/neo4j.conf
sudo service neo4j stop
sudo mv /tmp/neo4j.conf /etc/neo4j
sudo service neo4j start

echo "Now you need to go to http://<hostname>:7474 in your browser and set a default password for the database"
