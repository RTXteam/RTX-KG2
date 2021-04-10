#!/usr/bin/env bash
# finish-snakemake.sh: Run the commands for Snakemake's Finish rule
# Copyright 2020 Stephen A. Ramsey
# Author Erica C. Wood


# NOTE:
# This file does not use source master-config.shinc.
# This was a purposeful decision to minimize the different inputs.
# All of the inputs come from Snakemake, through the system build-kg2-snakemake.sh->Snakefile->finish-snakemake.sh
# This file is triggered last in the build system. By running it through this system, this ensures that the values 
# passed into this file are the same as they were are the start of the build. In general, it means that there is one
# streamlined input.

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [final_output_file_full] [output_file_orphan_edges] [report_file_full] [output_nodes_file_full] [simplified_output_file_full] [simplified_report_file_full]"
    echo "[simplified_output_nodes_file_full] [slim_output_file_full] [kg2_tsv_dir] [s3_cp_cmd]"
    echo "[kg2_tsv_tarball] [s3_bucket] [s3_bucket_public] [output_file_base] [ont_load_inventory_file]"
    echo "[CODE_DIR] [s3_bucket_versioned] [BUILD_DIR] [simplified_report_file_base] [VENV_DIR]"
    exit 2
fi

final_output_file_full=${1}
output_file_orphan_edges=${2}
report_file_full=${3}
output_nodes_file_full=${4}
simplified_output_file_full=${5}
simplified_report_file_full=${6}
simplified_output_nodes_file_full=${7}
slim_output_file_full=${8}
kg2_tsv_dir=${9}
s3_cp_cmd=${10}
kg2_tsv_tarball=${11}
s3_bucket=${12}
s3_bucket_public=${13}
output_file_base=${14}
ont_load_inventory_file=${15}
CODE_DIR=${16}
s3_bucket_versioned=${17}
BUILD_DIR=${18}
simplified_report_file_base=${19}
VENV_DIR=${20}
previous_simplified_report_base="previous-${simplified_report_file_base}"

echo "================= starting finish-snakemake.sh =================="
date

gzip -fk ${final_output_file_full}
tar -C ${kg2_tsv_dir} -czvf ${kg2_tsv_tarball} nodes.tsv nodes_header.tsv edges.tsv edges_header.tsv
${s3_cp_cmd} ${kg2_tsv_tarball} s3://${s3_bucket}/

gzip -fk ${simplified_output_file_full}
gzip -fk ${simplified_output_nodes_file_full}
gzip -fk ${output_nodes_file_full}
gzip -fk ${output_file_orphan_edges}
gzip -fk ${slim_output_file_full}

${s3_cp_cmd} ${final_output_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${simplified_output_file_full}.gz s3://${s3_bucket_public}/
${s3_cp_cmd} ${output_nodes_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${report_file_full} s3://${s3_bucket_public}/
${s3_cp_cmd} s3://${s3_bucket_public}/${simplified_report_file_base} ${BUILD_DIR}/${previous_simplified_report_base}
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/compare_edge_reports.py ${BUILD_DIR}/${previous_simplified_report_base} ${simplified_report_file_full}
${s3_cp_cmd} ${simplified_report_file_full} s3://${s3_bucket_public}/
${s3_cp_cmd} ${output_file_orphan_edges}.gz s3://${s3_bucket_public}/
${s3_cp_cmd} ${slim_output_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${simplified_output_nodes_file_full}.gz s3://${s3_bucket}/

build_multi_owl_stderr_file="${BUILD_DIR}/build-${output_file_base%.*}"-stderr.log

${s3_cp_cmd} ${build_multi_owl_stderr_file} s3://${s3_bucket_public}/
${s3_cp_cmd} ${ont_load_inventory_file} s3://${s3_bucket_public}/
${s3_cp_cmd} ${CODE_DIR}/s3-index.html s3://${s3_bucket_public}/index.html

${s3_cp_cmd} ${report_file_full} s3://${s3_bucket_versioned}/
${s3_cp_cmd} ${simplified_report_file_full} s3://${s3_bucket_versioned}/
${s3_cp_cmd} ${build_multi_owl_stderr_file} s3://${s3_bucket_versioned}/

date
echo "================ script finished ============================"
