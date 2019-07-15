#!/bin/bash

sudo apt-get update -y
sudo apt-get install -y emacs
wget --no-check-certificate -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
echo 'deb http://debian.neo4j.org/repo stable/' > neo4j.list
sudo mv neo4j.list /etc/apt/sources.list.d/neo4j.list
sudo apt-get update -y
sudo apt-get install -y neo4j
