#!/bin/bash

# Deletes MySQL from an Ubuntu system, including the database(s)

# DANGEROUS: only run this script if you know what you are doing

sudo apt-get remove --purge -y mysql*
sudo apt-get autoremove -y
sudo apt-get autoclean
sudo apt-get remove dbconfig-mysql
sudo rm -r -f /etc/mysql
