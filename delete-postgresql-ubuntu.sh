#!/usr/bin/env bash
# delete-postgresql-ubuntu.sh: deletes PostgreSQL from an Ubuntu system, including the database(s)
# Copyright 2021 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>
#
# DANGEROUS: only run this script if you know what you are doing

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

sudo DEBIAN_FRONTEND=noninteractive apt-get remove --purge -y postgresql* pgdg-keyring
sudo apt-get -y autoremove
sudo apt-get -y autoclean
sudo rm -r -f /var/lib/postgresql/ /var/log/postgresql/ /etc/postgresql/
sudo delgroup postgres
sudo deluser postgres
