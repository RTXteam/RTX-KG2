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

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

{
echo "================= starting build-kg2-snakemake.sh =================="
date

build_flag=${1-""}

if [[ "${build_flag}" == "test" ]]
then
    # The test argument for bash scripts (ex. extract-semmeddb.sh test)
    test_arg="test"
    # The test argument for file names (ex. kg2-owl-test.json)
    test_arg_d="-test"
    # The test argument for python scripts (ex. python3 uniprotkb_dat_to_json.py --test)
    test_arg_dd="--test"
else
    test_arg=""
    test_arg_d=""
    test_arg_dd=""
fi

# Change directories into the home directory because snakemake doesn't like ~ in input/output names, so paths are respective
# Run snakemake from the virtualenv but run the snakefile in kg2-code
# -R Finish: Run all of the rules in the snakefile
# -j: Run the rules in parallel
# -config: give the test arguments to the snakefile
cd ~ && ${VENV_DIR}/bin/snakemake --snakefile /home/ubuntu/kg2-code/Snakefile -R Finish -j --config test="${test_arg}" testd="${test_arg_d}" testdd="${test_arg_dd}"

date
echo "================ script finished ============================"
} >${BUILD_DIR}/build-kg2-snakemake.log 2>&1
