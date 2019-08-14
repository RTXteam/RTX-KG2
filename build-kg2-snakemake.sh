#!/usr/bin/env bash
# build-kg2-snakemake.sh: Create KG2 JSON file from scratch
# Copyright 2019 Stephen A. Ramsey
# Author Erica C. Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [test]"
    exit 2
fi

# Usage: build-kg2-snakemake.sh [test]

{
echo "================= starting build-kg2-snakemake.sh =================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

BUILD_FLAG=${1-""}

if [[ "${BUILD_FLAG}" == "test" ]]
then
    TEST_ARG="test"
    TEST_ARG_D="-test"
    TEST_ARG_DD="--test"
else
    TEST_ARG=""
    TEST_ARG_D=""
    TEST_ARG_DD=""
fi

# change into the root director
cd ~

# activate the virtualenv and start running snakemake with the Snakefile in kg2-code
source ${VENV_DIR}/bin/activate
snakemake --snakefile /home/ubuntu/kg2-code/Snakefile -R Finish -j --config test="${TEST_ARG}" testd="${TEST_ARG_D}" testdd="${TEST_ARG_DD}"

date
echo "================ script finished ============================"
} >~/snakemake.log 2>&1
