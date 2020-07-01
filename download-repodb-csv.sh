#!/usr/bin/env bash
# build-kg2.sh:  script for downloading and importing repoDB 

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_csv_dir>"
    exit 2
fi

echo "================= starting doenload-repodb-csv.sh ================="
date

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

REPODB_DIR=${1:-"${BUILD_DIR}/repodb/"}
REPODB_FILE=repodb.csv

mkdir -p ${REPODB_DIR}

aws s3 cp --no-progress --region ${S3_REGION} s3://${S3_BUCKET}/${REPODB_FILE} ${REPODB_DIR}/${REPODB_FILE}

date
echo "================= script finished ================="