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

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [final_output_file_full] [output_file_orphan_edges] [report_file_full] [simplified_output_file_full] [simplified_report_file_full]"
    echo "[slim_output_file_full] [kg2_tsv_dir] [s3_cp_cmd]"
    echo "[kg2_tsv_tarball] [s3_bucket] [s3_bucket_public] "
    echo "[PROCESS_CODE_DIR] [s3_bucket_versioned] [BUILD_DIR] [simplified_report_file_base] [VENV_DIR]"
    exit 2
fi

final_output_nodes_file_full=${1}
final_output_edges_file_full=${2}
output_file_orphan_edges=${3}
report_file_full=${4}
simplified_output_nodes_file_full=${5}
simplified_output_edges_file_full=${6}
simplified_report_file_full=${7}
slim_output_nodes_file_full=${8}
slim_output_edges_file_full=${9}
kg2_tsv_dir=${10}
s3_cp_cmd=${11}
kg2_tsv_tarball=${12}
s3_bucket=${13}
s3_bucket_public=${14}
PROCESS_CODE_DIR=${15}
s3_bucket_versioned=${16}
BUILD_DIR=${17}
simplified_report_file_base=${18}
VENV_DIR=${19}
previous_simplified_report_base="previous-${simplified_report_file_base}"

echo "================= starting finish-snakemake.sh =================="
date

gzip -fk ${final_output_nodes_file_full}
gzip -fk ${final_output_edges_file_full}
tar -C ${kg2_tsv_dir} -czvf ${kg2_tsv_tarball} nodes.tsv nodes_header.tsv edges.tsv edges_header.tsv
${s3_cp_cmd} ${kg2_tsv_tarball} s3://${s3_bucket}/

gzip -fk ${simplified_output_nodes_file_full}
gzip -fk ${simplified_output_edges_file_full}
gzip -fk ${output_file_orphan_edges}
gzip -fk ${slim_output_nodes_file_full}
gzip -fk ${slim_output_edges_file_full}

${s3_cp_cmd} ${final_output_nodes_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${final_output_edges_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${simplified_output_nodes_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${simplified_output_edges_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${report_file_full} s3://${s3_bucket_public}/

# Attempt to compare the report from the previous build to the current build
${s3_cp_cmd} s3://${s3_bucket_public}/${simplified_report_file_base} ${BUILD_DIR}/${previous_simplified_report_base}
if [ $? -eq 0 ]
then
    ${VENV_DIR}/bin/python3 -u ${PROCESS_CODE_DIR}/compare_edge_reports.py ${BUILD_DIR}/${previous_simplified_report_base} ${simplified_report_file_full}
else
    echo "Report from previous build not available."
fi

${s3_cp_cmd} ${simplified_report_file_full} s3://${s3_bucket_public}/

${s3_cp_cmd} ${output_file_orphan_edges}.gz s3://${s3_bucket_public}/
${s3_cp_cmd} ${slim_output_nodes_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${slim_output_edges_file_full}.gz s3://${s3_bucket}/

${s3_cp_cmd} ${report_file_full} s3://${s3_bucket_versioned}/
${s3_cp_cmd} ${simplified_report_file_full} s3://${s3_bucket_versioned}/

date
echo "================ script finished ============================"
