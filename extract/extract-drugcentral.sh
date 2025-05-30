#!/usr/bin/env bash
# extract-drugcentral.sh: Download the DrugCentral PostgreSQL database and convert it into JSON
# Copyright 2021 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_file> <drugcentral_dir>"
    exit 2
fi

# Usage: extract-drugcentral.sh <output_file> <drugcentral_dir>

echo "================= starting extract-drugcentral.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

drugcentral_dir=${2-"${BUILD_DIR}/drugcentral"}
output_file=${1-"${drugcentral_dir}/drugcentral_psql.json"}

drugcentral_database=drugcentral

mkdir -p ${drugcentral_dir}

# It appears that you can get release history information for Drug Central on this
# web page: https://unmtid-shinyapps.net/download/
drugcentral_date=08222022
source="https://unmtid-shinyapps.net/download/drugcentral.dump.${drugcentral_date}.sql.gz"
download_filename=${drugcentral_dir}/drugcentral.sql.gz

psql_dump_file="${drugcentral_dir}/psql_dump_file.txt"
user="ubuntu"
role="jjyang"

cd ~postgres/

${curl_get} ${source} > ${download_filename}
sudo -u postgres psql -c "DROP DATABASE IF EXISTS ${drugcentral_database}"
sudo -u postgres psql -c "CREATE DATABASE ${drugcentral_database}"
sudo -u postgres psql -c "DROP ROLE IF EXISTS ${role}"
sudo -u postgres psql -c "CREATE ROLE ${role}"
gunzip -c ${download_filename} | sudo -u postgres psql -v ON_ERROR_STOP=1 ${drugcentral_database}
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ${drugcentral_database} TO ${user}"
sudo -u postgres psql -d ${drugcentral_database} -c "GRANT ALL PRIVILEGES ON SCHEMA public TO ${user}"
sudo -u postgres psql -d ${drugcentral_database} -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ${user}"

psql_run_command="psql -U ${user} -d ${drugcentral_database} -t --output ${psql_dump_file} --no-align -c "

rm -f ${output_file}
touch ${output_file}

external_ids_query="SELECT id_type, identifier, struct_id FROM public.identifier"
${psql_run_command} "${external_ids_query}" -F $'\t'
${VENV_DIR}/bin/python3 ${EXTRACT_CODE_DIR}/drugcentral_psql_to_drugcentral_json.py ${psql_dump_file} ${output_file} external_ids --query ${external_ids_query}

omop_relations_query="SELECT DISTINCT struct_id, relationship_name, snomed_full_name, snomed_conceptid, umls_cui, doid FROM public.omop_relationship_doid_view"
${psql_run_command} "${omop_relations_query}" -F $'\t'
${VENV_DIR}/bin/python3 ${EXTRACT_CODE_DIR}/drugcentral_psql_to_drugcentral_json.py ${psql_dump_file} ${output_file} omop_relations --query ${omop_relations_query}

faers_query="SELECT DISTINCT struct_id, meddra_name, meddra_code, llr, llr_threshold FROM public.faers"
${psql_run_command} "${faers_query}" -F $'\t'
${VENV_DIR}/bin/python3 ${EXTRACT_CODE_DIR}/drugcentral_psql_to_drugcentral_json.py ${psql_dump_file} ${output_file} faers_data --query ${faers_query}

atc_query="SELECT DISTINCT struct_id, atc_code FROM public.struct2atc"
${psql_run_command} "${atc_query}" -F $'\t'
${VENV_DIR}/bin/python3 ${EXTRACT_CODE_DIR}/drugcentral_psql_to_drugcentral_json.py ${psql_dump_file} ${output_file} atc_ids --query ${atc_query}

drugcentral_ids_query="SELECT DISTINCT id, name, preferred_name FROM public.synonyms"
${psql_run_command} "${drugcentral_ids_query}" -F $'\t'
${VENV_DIR}/bin/python3 ${EXTRACT_CODE_DIR}/drugcentral_psql_to_drugcentral_json.py ${psql_dump_file} ${output_file} drugcentral_ids --query ${drugcentral_ids_query}

bioactivities_query="SELECT DISTINCT action_type, moa_source, moa_source_url, struct_id, act_source, act_source_url, accession FROM public.act_table_full"
${psql_run_command} "${bioactivities_query}" -F $'\t'
${VENV_DIR}/bin/python3 ${EXTRACT_CODE_DIR}/drugcentral_psql_to_drugcentral_json.py ${psql_dump_file} ${output_file} bioactivities --query ${bioactivities_query}

pharmacologic_action_query="SELECT DISTINCT struct_id, type, class_code, source FROM public.pharma_class"
${psql_run_command} "${pharmacologic_action_query}" -F $'\t'
${VENV_DIR}/bin/python3 ${EXTRACT_CODE_DIR}/drugcentral_psql_to_drugcentral_json.py ${psql_dump_file} ${output_file} pharmacologic_action --query ${pharmacologic_action_query}

version_query="SELECT version as version_number, dtime FROM public.dbversion"
${psql_run_command} "${version_query}" -F $'\t'
${VENV_DIR}/bin/python3 ${EXTRACT_CODE_DIR}/drugcentral_psql_to_drugcentral_json.py ${psql_dump_file} ${output_file} version --query ${version_query}

date
echo "================= finished extract-drugcentral.sh =================="
