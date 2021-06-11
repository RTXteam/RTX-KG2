#!/usr/bin/env bash
# build-kg2-snakemake.sh: Create KG2 JSON file from scratch using snakemake
# Copyright 2019 Stephen A. Ramsey
# Author Erica C. Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [test|alltest|all|-n] [-n] [travisci]"
    exit 2
fi

# Usage: build-kg2-snakemake.sh [test|alltest|all|-n] [-n]

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

build_flag=${1-""}
secondary_build_flag=${2-""}
travisci_flag=${3-""}

if [[ "${build_flag}" == "test" || "${build_flag}" == "alltest" ]]
then
    # The test argument for bash scripts (ex. extract-semmeddb.sh test)
    test_flag="test"
    # The test argument for file names (ex. kg2-ont-test.json)
    test_suffix="-test"
    # The test argument for python scripts (ex. python3 uniprotkb_dat_to_json.py --test)
    test_arg="--test"
else
    test_flag=""
    test_suffix=""
    test_arg=""
fi

build_kg2_log_file=${BUILD_DIR}/build-kg2-snakemake${test_suffix}.log
if [[ "${travisci_flag}" == "travisci" ]]
then
    trap "cat ${build_kg2_log_file}" EXIT
fi
{
echo "================= starting build-kg2-snakemake.sh =================="
date

snakemake_config_file=${CODE_DIR}/snakemake-config.yaml
snakefile=${CODE_DIR}/Snakefile

if [[ "${travisci_flag}" != "travisci" ]]
then
    ${VENV_DIR}/bin/python3 -u generate_snakemake_config_file.py ${test_arg} ${config_dir}/master-config.shinc \
                            ${CODE_DIR}/snakemake-config-var.yaml ${snakemake_config_file}
else
    python3 -u generate_snakemake_config_file.py ${test_arg} ${config_dir}/master-config.shinc \
            ${CODE_DIR}/snakemake-config-var.yaml ${snakemake_config_file}
fi

# Run snakemake from the virtualenv but run the snakefile in kg2-code
# -F: Run all of the rules in the snakefile
# -R Finish: Run all of the rules in the snakefile that generate an unmet dependency
# -R Merge: Generate any missing KG2 JSON files (ex. kg2-ont.json), merge them, then finish the workflow
#           (more likely to be the flag you need than -R Finish depending on the fail point)
# -j: Run the rules in parallel
# -config: Give the test arguments to the snakefile (NO LONGER USED)
# --dag | dot -Tpng > ~/kg2-build/snakemake_diagram.png: Creates Snakemake workflow diagram (when combined with -F and -j)
# -n: dry run REMOVE THIS BEFORE BUILDING

export PATH=$PATH:${BUILD_DIR}

echo configfile: \"${snakemake_config_file}\" > ${snakefile}

cat ${CODE_DIR}/Snakefile-finish >> ${snakefile}

echo 'include: "Snakefile-pre-etl"' >> ${snakefile}

echo 'include: "Snakefile-conversion"' >> ${snakefile}

echo 'include: "Snakefile-post-etl"' >> ${snakefile}

if [[ "${build_flag}" == "all" || "${build_flag}" == "alltest" ]]
then
    echo 'include: "Snakefile-semmeddb-extraction"' >> ${snakefile}
fi

if [[ "${build_flag}" == "all" ]]
then
    echo 'include: "Snakefile-extraction"' >> ${snakefile}
fi

dryrun=""
if [[ "${build_flag}" == "-n" || "${secondary_build_flag}" == "-n" ]]
then
    dryrun="-n"
fi

if [[ "${travisci_flag}" != "travisci" ]]
then
    cd ~ && ${VENV_DIR}/bin/snakemake --snakefile ${snakefile} -F -j ${dryrun}
else
    cd ~ && snakemake --snakefile ${snakefile} -F -j ${dryrun}
fi

date
echo "================ script finished ============================"
} > ${build_kg2_log_file} 2>&1

if [[ "${travisci_flag}" != "travisci" ]]
then
    ${s3_cp_cmd} ${build_kg2_log_file} s3://${s3_bucket_public}/
    ${s3_cp_cmd} ${build_kg2_log_file} s3://${s3_bucket_versioned}/
fi

