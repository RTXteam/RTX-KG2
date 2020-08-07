#!/usr/bin/env bash
# version.sh: Increment the version of KG2
# Copyright 2020 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [version_filename]"
    exit 2
fi

# Usage: version.sh

echo "================= starting version.sh =================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

local_version_filename=${1:-"${BUILD_DIR}/kg2-version.txt"}
s3_version_filename="kg2-version.txt"


${s3_cp_cmd} s3://${s3_bucket_public}/${s3_version_filename} ${local_version_filename}

${VENV_DIR}/bin/python3 ${CODE_DIR}/update_version.py --increment ${local_version_filename}

${s3_cp_cmd} ${local_version_filename} s3://${s3_bucket_public}/${s3_version_filename}

date
echo "================= finishing version.sh =================="
