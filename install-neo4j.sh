#!/bin/bash
# install neo4j into an Ubuntu 18.04 instance and configure it for external network access
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

sudo apt-get update
sudo apt-get install -y software-properties-common wget

# install Zulu OpenJDK Java
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9
sudo apt-add-repository 'deb http://repos.azulsystems.com/ubuntu stable main'
sudo apt-get update
sudo apt-get install -y zulu-8

# install Neo4j
wget --no-check-certificate -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
echo 'deb http://debian.neo4j.org/repo stable/' > /tmp/neo4j.list
sudo mv /tmp/neo4j.list /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
sudo apt-get install -y neo4j=1:3.5.13
sudo cp /etc/neo4j/neo4j.conf /etc/neo4j/neo4j.conf.ori

# note: by default, Neo4j is configured as read-only (this is a good thing, we want to keep it that way)

# configure Neo4j for external network access
cat /etc/neo4j/neo4j.conf | sed 's/#dbms.connectors.default_listen_address/dbms.connectors.default_listen_address/g' > /tmp/neo4j.conf
sudo mv /tmp/neo4j.conf /etc/neo4j

# install APOC
cd /tmp
wget https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/3.5.0.4/apoc-3.5.0.4-all.jar
wget https://github.com/neo4j-contrib/neo4j-graph-algorithms/releases/download/3.5.4.0/graph-algorithms-algo-3.5.4.0.jar
sudo mv /tmp/graph-algorithms-algo-3.5.4.0.jar /var/lib/neo4j/plugins
sudo mv /tmp/apoc-3.5.0.4-all.jar /var/lib/neo4j/plugins
cat /etc/neo4j/neo4j.conf | sed 's/#dbms.security.procedures.unrestricted=my.extensions.example,my.procedures.*/dbms.security.procedures.unrestricted=apoc.*,algo.*/g' > \
                                /tmp/neo4j.conf
sudo mv /tmp/neo4j.conf /etc/neo4j

echo "Not starting Neo4j so that you can configure its initial password using neo4j-admin set-initial-password <PWD>"
