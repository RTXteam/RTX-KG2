#!/usr/bin/env bash
# build-kg2-snakemake.sh: Create KG2 JSON file from scratch using snakemake
# Copyright 2019 Stephen A. Ramsey
# Author Erica C. Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [test]"
    exit 2
fi

# Usage: build-kg2-snakemake.sh [test]

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

{
echo "================= starting build-kg2-snakemake.sh =================="
date

BUILD_FLAG=${1-""}

if [[ "${BUILD_FLAG}" == "test" ]]
then
    # The test argument for bash scripts (ex. extract-semmeddb.sh test)
    TEST_ARG="test"
    # The test argument for file names (ex. kg2-ont-test.json)
    TEST_ARG_D="-test"
    # The test argument for python scripts (ex. python3 uniprotkb_dat_to_json.py --test)
    TEST_ARG_DD="--test"
else
    TEST_ARG=""
    TEST_ARG_D=""
    TEST_ARG_DD=""
fi

# Change directories into the home directory because snakemake doesn't like ~ in input/output names, so paths are respective
# Run snakemake from the virtualenv but run the snakefile in kg2-code
# -R Finish: Run all of the rules in the snakefile
# -j: Run the rules in parallel
# -config: give the test arguments to the snakefile
cd ~ && ${VENV_DIR}/bin/snakemake --snakefile /home/ubuntu/kg2-code/Snakefile -R Finish -j --config test="${TEST_ARG}" testd="${TEST_ARG_D}" testdd="${TEST_ARG_DD}"

date
echo "================ script finished ============================"
} >${BUILD_DIR}/build-kg2-snakemake.log 2>&1
