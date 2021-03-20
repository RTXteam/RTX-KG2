#!/usr/bin/env bash
# tsv_to_neo4j.sh: Import TSV files generated from JSON KG into Neo4j
# Copyright 2020 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [test]"
    exit 2
fi

# Usage: tsv_to_neo4j.sh [test]

echo "================= starting tsv-to-neo4j-canonicalized.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/../master-config.shinc

neo4j_config=/etc/neo4j/neo4j.conf
database_path=`grep dbms.directories.data ${neo4j_config} | cut -f2 -d=`
database="graph.db"
build_flag=${1:-""}
tsv_dir=${BUILD_DIR}/TSV_Canonicalized

if [[ "${build_flag}" == "test" ]]
then
    test_arg="-test"
    test_prefix="test_"
else
    test_arg=""
    test_prefix=""
fi

tsv_tarball_base=kg2c-tsv${test_arg}.tar.gz
tsv_tarball=${tsv_dir}/${tsv_tarball_base}

echo "copying RTX Configuration JSON file from S3"

rtx_config_file_full=${BUILD_DIR}/${rtx_config_file}
${s3_cp_cmd} s3://${s3_bucket}/${rtx_config_file} ${rtx_config_file_full}

# change database and database paths to current database and database path in config file
sudo sed -i '/dbms.active_database/c\dbms.active_database='${database}'' ${neo4j_config}
    
# restart neo4j 
sudo service neo4j restart

# delete the old TSV tarball if it exists
rm -f ${tsv_tarball}

# create a folder for the TSV files and move the TSV files into them
rm -r -f ${tsv_dir}
mkdir -p ${tsv_dir}

# download the latest TSV files from the S3 Bucket
${s3_cp_cmd} s3://${s3_bucket}/${tsv_tarball_base} ${tsv_tarball}

# unpack the TSV tarball
tar -xvzf ${tsv_tarball} -C ${tsv_dir}

# delete the TSV tarball since we successfully unpacked it
rm -f ${tsv_tarball}

# delete the old log file and create a new one
rm -rf ${tsv_dir}/import.report
touch ${tsv_dir}/import.report
sudo chown neo4j:adm ${tsv_dir}/import.report

# stop Neo4j database before deleting the database
sudo service neo4j stop
sudo rm -rf ${database_path}/databases/${database}

mem_gb=`${CODE_DIR}/get-system-memory-gb.sh`

# import TSV files into Neo4j as Neo4j
sudo -u neo4j neo4j-admin import --nodes "${tsv_dir}/${test_prefix}nodes_c_header.tsv,${tsv_dir}/${test_prefix}nodes_c.tsv" \
    --relationships "${tsv_dir}/${test_prefix}edges_c_header.tsv,${tsv_dir}/${test_prefix}edges_c.tsv" \
    --max-memory=${mem_gb}G --multiline-fields=true --delimiter "\009" \
    --array-delimiter="ǂ" --report-file="${tsv_dir}/import.report" \
    --database=${database} --ignore-missing-nodes=true

# change read only to false so that indexes and constraints can be added
sudo sed -i '/dbms.read_only/c\dbms.read_only=false' ${neo4j_config}
sudo service neo4j start

# wait while neo4j boots up
sleep 1m

# add indexes and constraints to the graph database
${VENV_DIR}/bin/python3 -u ${config_dir}/create_indexes_constraints_canonicalized.py --configFile ${rtx_config_file_full}

sleep 5m

sudo service neo4j restart

# change the database to read only
sudo sed -i '/dbms.read_only/c\dbms.read_only=true' ${neo4j_config}

sudo service neo4j restart

# create a neo4j dump file for use downstream in building the DTD database
sudo service neo4j stop
dump_name=kg2c.dump
sudo neo4j-admin dump --database=graph.db --to=${BUILD_DIR}/${dump_name}
sudo service neo4j start

date
echo "================ script finished ============================"
