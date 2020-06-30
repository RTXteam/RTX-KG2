#!/usr/bin/env bash
# run-validation-tests.sh:  runs python scripts that validate various YAML files and config information for the RTX KG2 system.
# Copyright 2020 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc


echo "================= starting run-validation-tests.sh ================="
date

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_curies_to_categories_yaml.py
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_curies_to_urls_map_yaml.py
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_rtx_kg1_curie_mappings.py
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_kg2_util_curies_urls_categories.py

date
echo "================= script finished ================="

