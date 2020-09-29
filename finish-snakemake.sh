#!/usr/bin/env bash
# finish-snakemake.sh: Run the commands for Snakemake's Finish rule
# Copyright 2020 Stephen A. Ramsey
# Author Erica C. Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [final_output_file_full] [output_file_orphan_edges] [report_file_full] [output_nodes_file_full] [simplified_output_file_full] [simplified_report_file_full]"
    echo "[simplified_output_nodes_file_full] [slim_output_file_full] [kg2_tsv_dir] [s3_cp_cmd]"
    echo "[kg2_tsv_tarball] [s3_bucket] [s3_bucket_public] [output_file_base] [ont_load_inventory_file]"
    echo "[CODE_DIR] [s3_bucket_versioned]"
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

echo "================= starting finish-snakemake.sh =================="
date

gzip -f ${final_output_file_full}
tar -C ${kg2_tsv_dir} -czvf ${kg2_tsv_dir} nodes.tsv nodes_header.tsv edges.tsv edges_header.tsv
${s3_cp_cmd} ${kg2_tsv_tarball} s3://${s3_bucket}/

gzip -f ${simplified_output_file_full}
gzip -f ${simplified_output_nodes_file_full}
gzip -f ${output_nodes_file_full}
gzip -f ${output_file_orphan_edges}
gzip -f ${slim_output_file_full}

${s3_cp_cmd} ${final_output_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${simplified_output_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${output_nodes_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${report_file_full} s3://${s3_bucket_public}/
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