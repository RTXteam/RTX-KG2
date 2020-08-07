#!/usr/bin/env bash
# extract-smpdb.sh: Download the Small Molecule Pathway Database
# Copyright 2019 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output-dir>"
    exit 2
fi

# Usage: extract-smpdb.sh <output-dir>

echo "================= starting extract-smpdb.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

output_dir=${1:-"${BUILD_DIR}/smpdb"}
smpdb_output_file="pathbank_pathways.csv"
pw_output_file="pathbank_all_pwml.zip"

mkdir -p ${output_dir}
smpdb_link="https://pathbank.org/downloads/pathbank_all_pathways.csv.zip"
pwml_link="https://pathbank.org/downloads/pathbank_all_pwml.zip"
smpdb_pmids_file="SMPDB_pubmed_IDs.csv"

${curl_get} ${output_dir}/ ${smpdb_link} > ${output_dir}/${smpdb_output_file}.zip
${curl_get} ${output_dir}/ ${pwml_link} > ${output_dir}/${pw_output_file}

unzip -o ${output_dir}/${smpdb_output_file}.zip -d ${output_dir}/
unzip -o -q ${output_dir}/${pw_output_file} -d ${output_dir}/

for individ_file in $(ls ${output_dir}/pathbank_all_pwml)
do
	mv ${output_dir}/pathbank_all_pwml/${individ_file} ${output_dir}
done

${s3_cp_cmd} s3://${s3_bucket}/${smpdb_pmids_file} ${output_dir}

date
echo "================= finishing extract-smpdb.sh =================="
