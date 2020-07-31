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

LOCAL_VERSION_FILENAME=${1:-"${BUILD_DIR}/kg2-version.txt"}
S3_VERSION_FILENAME="kg2-version.txt"


${S3_CP_CMD} s3://${S3_BUCKET_PUBLIC}/${S3_VERSION_FILENAME} ${LOCAL_VERSION_FILENAME}

${VENV_DIR}/bin/python3 ${CODE_DIR}/update_version.py --increment ${LOCAL_VERSION_FILENAME}

${S3_CP_CMD} ${LOCAL_VERSION_FILENAME} s3://${S3_BUCKET_PUBLIC}/${S3_VERSION_FILENAME}

date
echo "================= finishing version.sh =================="