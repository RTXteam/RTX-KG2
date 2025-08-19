#!/usr/bin/env bash
# download-babel.sh: Download the correct Babel SQLite file
# Copyright 2025 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <babel_sqlite> <local_babel_destination>"
    exit 2
fi

# Usage: download-babel.sh <local_babel_destination>

echo "================= starting download-babel.sh =================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

babel_sqlite_local=${1:-"${BUILD_DIR}/${babel_db}"}

${s3_cp_cmd} s3://${s3_bucket_public}/${babel_db} ${babel_sqlite_local}

date
echo "================= finishing download-babel.sh =================="
