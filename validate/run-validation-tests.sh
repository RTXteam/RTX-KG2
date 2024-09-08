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

{
echo "================= starting run-validation-tests.sh ================="
date

export PATH=$PATH:${BUILD_DIR}

biolink_base_url_no_version=https://raw.githubusercontent.com/biolink/biolink-model/
biolink_raw_base_url=${biolink_base_url_no_version}v${biolink_model_version}/
biolink_model_yaml=biolink_model.yaml
biolink_model_yaml_url=${biolink_raw_base_url}src/biolink_model/schema/${biolink_model_yaml}
biolink_model_yaml_local_file=${BUILD_DIR}/${biolink_model_yaml}

infores_registry_base_url_no_version=https://raw.githubusercontent.com/biolink/information-resource-registry/
infores_registry_base_url=${infores_registry_base_url_no_version}v${infores_registry_version}/
infores_catalog_yaml=infores_catalog.yaml
infores_catalog_yaml_url=${infores_registry_base_url}${infores_catalog_yaml}

cat ${config_dir}/master-config.shinc
echo ${VALIDATE_CODE_DIR}
echo ${curies_to_urls_file}

rm -f ${biolink_model_yaml_local_file}

cd ${BUILD_DIR}

${curl_get} ${infores_catalog_yaml_url} -o ${infores_catalog_yaml}

${python_command} -u ${VALIDATE_CODE_DIR}/validate_curies_to_categories_yaml.py \
           ${curies_to_categories_file} \
           ${curies_to_urls_file} \
           ${biolink_model_yaml_url} \
           ${biolink_model_yaml_local_file}

${python_command} -u ${VALIDATE_CODE_DIR}/validate_curies_to_urls_map_yaml.py \
           ${curies_to_urls_file} \
           ${biolink_model_yaml_url} \
           ${biolink_model_yaml_local_file}

${python_command} -u ${VALIDATE_CODE_DIR}/validate_kg2_util_curies_urls_categories.py \
           ${curies_to_urls_file} \
           ${biolink_model_yaml_url} \
           ${biolink_model_yaml_local_file}

${python_command} -u ${VALIDATE_CODE_DIR}/validate_predicate_remap_yaml.py \
           ${curies_to_urls_file} \
           ${predicate_mapping_file} \
           ${biolink_model_yaml_url} \
           ${biolink_model_yaml_local_file}

${python_command} -u ${VALIDATE_CODE_DIR}/validate_provided_by_to_infores_map_yaml.py \
           ${infores_mapping_file} \
           ${infores_catalog_yaml}

date
echo "================= finished run-validation-tests.sh ================="
}
