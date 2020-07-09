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

BIOLINK_MODEL_OWL_FILE=/tmp/biolink-model.owl
BIOLINK_CONTEXT_JSONLD_FILE=/tmp/context.jsonld
BIOLINK_RAW_BASE_URL=https://raw.githubusercontent.com/biolink/biolink-model/master/

${CURL_GET} ${BIOLINK_RAW_BASE_URL}biolink-model.owl > ${BIOLINK_MODEL_OWL_FILE}
${CURL_GET} ${BIOLINK_RAW_BASE_URL}context.jsonld > ${BIOLINK_CONTEXT_JSONLD_FILE}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_curies_to_categories_yaml.py \
           ${CURIES_TO_CATEGORIES_FILE} \
           ${CURIES_TO_URLS_FILE} \
           ${BIOLINK_MODEL_OWL_FILE}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_curies_to_urls_map_yaml.py \
           ${CURIES_TO_URLS_FILE} \
           ${BIOLINK_CONTEXT_JSONLD_FILE}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_rtx_kg1_curie_mappings.py \
           ${CURIES_TO_URLS_FILE}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_kg2_util_curies_urls_categories.py \
           ${BIOLINK_MODEL_OWL_FILE} \
           ${CURIES_TO_URLS_FILE}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_predicate_remap_yaml.py \
           ${CURIES_TO_URLS_FILE} \
           ${PREDICATE_MAPPING_FILE}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_owl_load_inventory.py \
           ${OWL_LOAD_INVENTORY_FILE} \
           ${CURIES_TO_URLS_FILE} \
           ${UMLS2RDF_CONFIG_MASTER}

date
echo "================= finished run-validation-tests.sh ================="

