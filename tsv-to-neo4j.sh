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

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

neo4j_config=/etc/neo4j/neo4j.conf
database_path=`grep dbms.directories.data ${neo4j_config} | cut -f2 -d=`
database=${1:-"graph.db"}
user=${2:-"neo4j"}
build_flag=${3:-""}
tsv_dir=${BUILD_DIR}/TSV

if [[ "${build_flag}" == "test" ]]
then
    test_arg="-test"
else
    test_arg=""
fi

password_filename=`${VENV_DIR}/bin/python3 -u ${CODE_DIR}/prompt_for_password_and_save_to_temp_file.py`

cleanup() {
    rm -f ${password_filename}
}
trap cleanup 0

# change database and database paths to current database and database path in config file
sudo sed -i '/dbms.active_database/c\dbms.active_database='${database}'' ${neo4j_config}
    
# restart neo4j 
sudo service neo4j restart

# delete the old TSV files if it exists
rm -f kg2-tsv${test_arg}.tar.gz

# create a folder for the TSV files and move the TSV files into them
rm -r -f ${tsv_dir}
mkdir -p ${tsv_dir}

# download the latest TSV files from the S3 Bucket
${S3_CP_CMD} s3://${S3_BUCKET}/kg2-tsv${test_arg}.tar.gz ${tsv_dir}/kg2-tsv${test_arg}.tar.gz

tar -xvzf ${tsv_dir}/kg2-tsv${test_arg}.tar.gz -C ${tsv_dir}

# delete the old log file and create a new one
rm -rf ${tsv_dir}/import.report
touch ${tsv_dir}/import.report
sudo chown neo4j:adm ${tsv_dir}/import.report

# stop Neo4j database before deleting the database
sudo service neo4j stop
sudo rm -rf ${database_path}/databases/${database}

mem_gb=`${CODE_DIR}/get-system-memory-gb.sh`

# import TSV files into Neo4j as Neo4j
sudo -u neo4j neo4j-admin import --nodes "${tsv_dir}/nodes_header.tsv,${tsv_dir}/nodes.tsv" \
    --relationships "${tsv_dir}/edges_header.tsv,${tsv_dir}/edges.tsv" \
    --max-memory=${mem_gb}G --multiline-fields=true --delimiter "\009" \
    --array-delimiter="," --report-file="${tsv_dir}/import.report" \
    --database=${database} --ignore-missing-nodes=true

# change read only to false so that indexes and constraints can be added
sudo sed -i '/dbms.read_only/c\dbms.read_only=false' ${neo4j_config}
sudo service neo4j start

# wait while neo4j boots up
sleep 1m

# add indexes and constraints to the graph database
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/create_indexes_constraints.py --passwordFile ${password_filename} ${user}

rm -f ${password_filename}

# wait for indexing to complete
sleep 5m
sudo service neo4j restart

# change the database to read only
sudo sed -i '/dbms.read_only/c\dbms.read_only=true' ${neo4j_config}

sudo service neo4j restart

date
echo "================ script finished ============================"
