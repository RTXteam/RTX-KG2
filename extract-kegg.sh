#!/usr/bin/env bash
# extract-kegg.sh: Create a flat file from the KEGG API
# Copyright 2021 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output-xml-file>"
    exit 2
fi

# Usage: extract-kegg.sh <output_xml_file>

echo "================= starting extract-kegg.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

output_file=${1:-"${BUILD_DIR}/kegg.json"}

cache_control_helper_link="https://raw.githubusercontent.com/RTXteam/RTX/master/code/reasoningtool/kg-construction/cache_control_helper.py"

curl -L ${cache_control_helper_link} > ${CODE_DIR}/cache_control_helper.py

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/query_kegg.py ${output_file}

date
echo "================= finished extract-kegg.sh =================="