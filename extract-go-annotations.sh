#!/usr/bin/env bash
# extract-go-annotations.sh: Download the Gene Ontology Annotations to UniprotKB
# Copyright 2020 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [output_file]"
    exit 2
fi

# Usage: extract-go-annotation.sh

echo "================= starting extract-go-annotations.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

go_file=goa_human.gpa.gz

output_file=${1-"${BUILD_DIR}/goa_human.gpa"}

go_link="ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/HUMAN/goa_human.gpa.gz"

${curl_get} ${go_link} > ${BUILD_DIR}/${go_file}

gunzip -c ${BUILD_DIR}/${go_file} > ${output_file}

rm ${BUILD_DIR}/${go_file}

date
echo "================= finishing extract-go-annotations.sh =================="