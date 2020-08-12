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

BIOLINK_RAW_BASE_URL=https://raw.githubusercontent.com/biolink/biolink-model/master/
BIOLINK_URL_CONTEXT_JSONLD=${BIOLINK_RAW_BASE_URL}context.jsonld
BIOLINK_MODEL_OWL=biolink-model.owl
BIOLINK_MODEL_LOCAL_FILE=${BUILD_DIR}/${BIOLINK_MODEL_OWL}
BIOLINK_MODEL_URL=${BIOLINK_RAW_BASE_URL}${BIOLINK_MODEL_OWL}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_curies_to_categories_yaml.py \
           ${curies_to_categories_file} \
           ${curies_to_urls_file} \
           ${BIOLINK_MODEL_URL} \
           ${BIOLINK_MODEL_LOCAL_FILE}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_curies_to_urls_map_yaml.py \
           ${curies_to_urls_file} \
           ${BIOLINK_URL_CONTEXT_JSONLD}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_rtx_kg1_curie_mappings.py \
           ${curies_to_urls_file}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_kg2_util_curies_urls_categories.py \
           ${curies_to_urls_file} \
           ${BIOLINK_MODEL_URL} \
           ${BIOLINK_MODEL_LOCAL_FILE}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_predicate_remap_yaml.py \
           ${curies_to_urls_file} \
           ${predicate_mapping_file} \
           ${BIOLINK_MODEL_URL} \
           ${BIOLINK_MODEL_LOCAL_FILE}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_ont_load_inventory.py \
           ${ont_load_inventory_file} \
           ${curies_to_urls_file} \
           ${umls2rdf_config_master} \
           ${BIOLINK_MODEL_URL} \
           ${BIOLINK_MODEL_LOCAL_FILE}

date
echo "================= finished run-validation-tests.sh ================="

