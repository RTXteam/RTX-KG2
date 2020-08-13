#!/usr/bin/env bash
# version.sh: Increment the version of KG2
# Copyright 2020 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [version_filename] [test]"
    exit 2
fi

# Usage: version.sh

echo "================= starting version.sh =================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

trigger_file_is_major_release=${BUILD_DIR}/major-release

local_version_filename=${1:-"${BUILD_DIR}/kg2-version.txt"}
build_flag=${2:-""}
s3_version_filename="kg2-version.txt"

${s3_cp_cmd} s3://${s3_bucket_public}/${s3_version_filename} ${local_version_filename}

if [ "${build_flag}" == 'test' ]
then
   increment_flag=''
else
    if [ -e ${trigger_file_is_major_release} ]
    then
        increment_flag='--increment_major'
    else
        increment_flag='--increment_minor'
    fi
fi

if [ "${increment_flag}" != '' ]
then
    ${VENV_DIR}/bin/python3 ${CODE_DIR}/update_version.py ${increment_flag} ${local_version_filename}
    ${s3_cp_cmd} ${local_version_filename} s3://${s3_bucket_public}/${s3_version_filename}
else
    echo "*** TEST MODE -- NO INCREMENT ***"
fi

if [ -f ${trigger_file_is_major_release} ]
then
   rm -f ${trigger_file_is_major_release}
fi

date
echo "================= finishing version.sh =================="
