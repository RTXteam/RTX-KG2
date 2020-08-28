#!/usr/bin/env bash
# run-validation-tests.sh:  runs python scripts that validate various YAML files and config information for the RTX KG2 system.
# Copyright 2020 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

## load the master config file
config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

echo "================= starting run-validation-tests.sh ================="
date

biolink_raw_base_url=https://raw.githubusercontent.com/biolink/biolink-model/master/
biolink_url_context_jsonld=${biolink_raw_base_url}context.jsonld
biolink_model_owl=biolink-model.owl
biolink_model_owl_local_file=${BUILD_DIR}/${biolink_model_owl}
biolink_model_owl_url=${biolink_raw_base_url}${biolink_model_owl}
biolink_model_yaml=biolink-model.yaml
biolink_model_yaml_url=${biolink_raw_base_url}${biolink_model_yaml}
biolink_model_yaml_local_file=${BUILD_DIR}/${biolink_model_yaml}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_curies_to_categories_yaml.py \
           ${curies_to_categories_file} \
           ${curies_to_urls_file} \
           ${biolink_model_owl_url} \
           ${biolink_model_owl_local_file}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_curies_to_urls_map_yaml.py \
           ${curies_to_urls_file} \
           ${biolink_url_context_jsonld}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_rtx_kg1_curie_mappings.py \
           ${curies_to_urls_file}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_kg2_util_curies_urls_categories.py \
           ${curies_to_urls_file} \
           ${biolink_model_owl_url} \
           ${biolink_model_owl_local_file}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_predicate_remap_yaml.py \
           ${curies_to_urls_file} \
           ${predicate_mapping_file} \
           ${biolink_model_yaml_url} \
           ${biolink_model_yaml_local_file}

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/validate_ont_load_inventory.py \
           ${ont_load_inventory_file} \
           ${curies_to_urls_file} \
           ${umls2rdf_config_master} \
           ${biolink_model_owl_url} \
           ${biolink_model_owl_local_file}

date
echo "================= finished run-validation-tests.sh ================="

