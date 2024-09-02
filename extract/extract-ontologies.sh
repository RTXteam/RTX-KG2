#!/usr/bin/env bash
# extract-ontologies.sh: Download OWL files and convert them into a JSONLines file
# Copyright 2024 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <parsing_script> <ontologies_load_inventory> <output_file> <ontologies_dir>"
    exit 2
fi

# Usage: extract-ontologies.sh <parsing_script> <ontologies_load_inventory> <output_file> <ontologies_dir>

echo "================= starting extract-ontologies.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

parsing_script=${1-"${EXTRACT_CODE_DIR}/owlparser.py"}
ontologies_load_inventory=${2-"${MAPS_CODE_DIR}/ont-load-inventory.yaml"}
output_file=${3-"${BUILD_DIR}/ontologies.jsonl"}
ontologies_dir=${4-"${BUILD_DIR}/owl_files"}

rm -rf ${ontologies_dir}
mkdir -p ${ontologies_dir}

# Temporary adjustment for https://github.com/HUPO-PSI/psi-mi-CV/issues/456
${s3_cp_cmd} s3://${s3_bucket}/mi.owl ${ontologies_dir}/mi.owl

# Temporary adjustment due to lack of resolution of chebi PURL
${s3_cp_cmd} s3://${s3_bucket}/chebi.owl ${ontologies_dir}/chebi.owl

# Generate the ontologies.jsonl file
${python_command} ${parsing_script} ${ontologies_load_inventory} ${ontologies_dir} ${output_file}

date
echo "================= finished extract-ontologies.sh =================="
