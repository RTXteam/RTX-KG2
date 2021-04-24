#!/usr/bin/env bash
# run-validation-tests.sh:  runs python scripts that validate various YAML files and config information for the RTX KG2 system.
# Copyright 2020 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [travisci]"
    exit 2
fi

## load the master config file

build_flag=${1:-""}

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

echo "================= starting run-validation-tests.sh ================="
date

biolink_base_url_no_version=https://raw.githubusercontent.com/biolink/biolink-model/
biolink_raw_base_url=${biolink_base_url_no_version}${biolink_model_version}/
curies_urls_map_replace_string="\    biolink_download_source: ${biolink_raw_base_url}"
ont_load_inventory_replace_string="\  url: ${biolink_raw_base_url}"
biolink_url_context_jsonld=${biolink_raw_base_url}context.jsonld
biolink_model_owl=biolink-model.owl.ttl
biolink_model_owl_local_file=${BUILD_DIR}/${biolink_model_owl}
biolink_model_owl_url=${biolink_raw_base_url}${biolink_model_owl}
biolink_model_yaml=biolink-model.yaml
biolink_model_yaml_url=${biolink_raw_base_url}${biolink_model_yaml}
biolink_model_yaml_local_file=${BUILD_DIR}/${biolink_model_yaml}

sed -i "\@${biolink_base_url_no_version}@c${curies_urls_map_replace_string}" \
        ${curies_to_urls_file}

sed -i "\@${biolink_base_url_no_version}@c${ont_load_inventory_replace_string}" \
        ${ont_load_inventory_file}


if [[ ${build_flag} != "travisci" ]]
then
    python_command="${VENV_DIR}/bin/python3"
else
    python_command="python"
fi

${python_command} -u ${CODE_DIR}/validate_curies_to_categories_yaml.py \
           ${curies_to_categories_file} \
           ${curies_to_urls_file} \
           ${biolink_model_owl_url} \
           ${biolink_model_owl_local_file}

${python_command} -u ${CODE_DIR}/validate_curies_to_urls_map_yaml.py \
           ${curies_to_urls_file} \
           ${biolink_url_context_jsonld}

${python_command} -u ${CODE_DIR}/validate_kg2_util_curies_urls_categories.py \
           ${curies_to_urls_file} \
           ${biolink_model_owl_url} \
           ${biolink_model_owl_local_file}

${python_command} -u ${CODE_DIR}/validate_predicate_remap_yaml.py \
           ${curies_to_urls_file} \
           ${predicate_mapping_file} \
           ${biolink_model_yaml_url} \
           ${biolink_model_yaml_local_file}

${python_command} -u ${CODE_DIR}/validate_ont_load_inventory.py \
           ${ont_load_inventory_file} \
           ${curies_to_urls_file} \
           ${umls2rdf_config_master} \
           ${biolink_model_owl_url} \
           ${biolink_model_owl_local_file}

date
echo "================= finished run-validation-tests.sh ================="

