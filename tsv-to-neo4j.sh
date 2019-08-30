#!/usr/bin/env bash
# tsv_to_neo4j.sh: Import TSV files generated from JSON KG into Neo4j
# Copyright 2019 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <database-name>=graph.db <neo4j-username>=neo4j [test]"
    exit 2
fi

# Usage: tsv_to_neo4j.sh <path_to_directory_containing_tsv_files> <database-name>

echo "================= starting tsv-to-neo4j.sh =================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

TSV_DIR=/home/ubuntu
DATABASE_PATH=/var/lib/neo4j/data
DATABASE=${1:-"graph.db"}
USER=${2:-"neo4j"}
BUILD_FLAG=${3:-""}

# change database and database paths to current database and database path in config file
sudo sed -i '/dbms.active_database/c\dbms.active_database='${DATABASE}'' /etc/neo4j/neo4j.conf
sudo sed -i '/dbms.directories.data/c\dbms.directories.data='${DATABASE_PATH}'' /etc/neo4j/neo4j.conf
    
# restart neo4j 
sudo service neo4j restart

if [[ "${BUILD_FLAG}" == "test" ]]
then
    TEST_ARG="-test"
else
    TEST_ARG=""
fi

# delete the old TSV files if it exists
rm -f kg2-tsv${TEST_ARG}.tar.gz

TSV_DIR=${BUILD_DIR}/TSV

# create a folder for the TSV files and move the TSV files into them
rm -r -f ${TSV_DIR}
mkdir -p ${TSV_DIR}

# download the latest TSV files from the S3 Bucket
${CURL_GET} https://s3-us-west-2.amazonaws.com/rtx-kg2-public/kg2-tsv${TEST_ARG}.tar.gz > ${TSV_DIR}/kg2-tsv${TEST_ARG}.tar.gz

tar -xvzf ${TSV_DIR}/kg2-tsv${TEST_ARG}.tar.gz -C ${TSV_DIR}

# delete the old log file and create a new one
rm -rf ${TSV_DIR}/import.report
touch ${TSV_DIR}/import.report
sudo chown neo4j:adm ${TSV_DIR}/import.report

# stop Neo4j database before deleting the database
sudo service neo4j stop
sudo rm -rf ${DATABASE_PATH}/databases/${DATABASE}

# import TSV files into Neo4j as Neo4j
sudo -u neo4j neo4j-admin import --nodes "${TSV_DIR}/nodes_header.tsv,${TSV_DIR}/nodes.tsv" \
    --relationships "${TSV_DIR}/edges_header.tsv,${TSV_DIR}/edges.tsv" \
    --max-memory=90G --multiline-fields=true --delimiter "\009" \
    --report-file="${TSV_DIR}/import.report" --database=${DATABASE} --ignore-missing-nodes=true

# change read only to false so that indexes and constraints can be added
sudo sed -i '/dbms.read_only/c\dbms.read_only=false' /etc/neo4j/neo4j.conf
sudo service neo4j start

# wait while neo4j boots up
sleep 1m

# add indexes and constraints to the graph database
${VENV_DIR}/bin/python3 ${CODE_DIR}/create_indexes_constraints.py --user ${USER}

# change the database to read only
sudo sed -i '/dbms.read_only/c\dbms.read_only=true' /etc/neo4j/neo4j.conf

sudo service neo4j restart

date
echo "================ script finished ============================"
