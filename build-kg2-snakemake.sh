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
    test_flag="test"
    # The test argument for file names (ex. kg2-owl-test.json)
    test_suffix="-test"
    # The test argument for python scripts (ex. python3 uniprotkb_dat_to_json.py --test)
    test_arg="--test"
else
    test_flag=""
    test_suffix=""
    test_arg=""
fi

semmed_tuplelist_file=${BUILD_DIR}/semmeddb/kg2-semmeddb${test_suffix}-tuplelist.json
semmed_output_file=${BUILD_DIR}/kg2-semmeddb${test_suffix}-edges.json

uniprotkb_dat_file=${BUILD_DIR}/uniprotkb/uniprot_sprot.dat
uniprotkb_output_file=${BUILD_DIR}/kg2-uniprotkb${test_suffix}.json

output_file_base=kg2-owl${test_suffix}.json
output_file_full=${BUILD_DIR}/${output_file_base}

output_file_orphan_edge=${BUILD_DIR}/kg2-orphans${test_suffix}-edges.json

final_output_file_base=kg2${test_suffix}.json
final_output_file_full=${BUILD_DIR}/${final_output_file_base}

simplified_output_file_base=kg2-simplified${test_suffix}.json
simplified_output_file_full=${BUILD_DIR}/${simplified_output_file_base}

simplified_output_nodes_file_base=kg2-simplified${test_suffix}-nodes.json
simplified_output_nodes_file_full=${BUILD_DIR}/${simplified_output_nodes_file_base}

output_nodes_file_base=kg2${test_suffix}-nodes.json
output_nodes_file_full=${BUILD_DIR}/${output_nodes_file_base}

report_file_base=kg2-report${test_suffix}.json
report_file_full=${BUILD_DIR}/${report_file_base}

simplified_report_file_base=kg2-simplified-report${test_suffix}.json
simplified_report_file_full=${BUILD_DIR}/${simplified_report_file_base}

slim_output_file_full=${BUILD_DIR}/kg2-slim${test_suffix}.json

ensembl_source_json_file=${BUILD_DIR}/ensembl/ensembl_genes_homo_sapiens.json
ensembl_output_file=${BUILD_DIR}/kg2-ensembl${test_suffix}.json

chembl_output_file=${BUILD_DIR}/kg2-chembl${test_suffix}.json

owl_load_inventory_file=${CODE_DIR}/ont-load-inventory${test_suffix}.yaml

chembl_mysql_dbname=chembl

unichem_output_tsv_file=${BUILD_DIR}/unichem/chembl-to-curies.tsv
unichem_output_file=${BUILD_DIR}/kg2-unichem${test_suffix}.json

ncbi_gene_tsv_file=${BUILD_DIR}/ncbigene/Homo_sapiens_gene_info.tsv
ncbi_gene_output_file=${BUILD_DIR}/kg2-ncbigene${test_suffix}.json

dgidb_dir=${BUILD_DIR}/dgidb
dgidb_output_file=${BUILD_DIR}/kg2-dgidb${test_suffix}.json

repodb_dir=${BUILD_DIR}/repodb
repodb_input_file=${BUILD_DIR}/repodb/repodb.csv
repodb_output_file=${BUILD_DIR}/kg2-repodb${test_suffix}.json

smpdb_dir=${BUILD_DIR}/smpdb
smpdb_input_file=${smpdb_dir}/pathbank_pathways.csv
smpdb_output_file=${BUILD_DIR}/kg2-smpdb${test_suffix}.json

drugbank_input_file=${BUILD_DIR}/drugbank.xml
drugbank_output_file=${BUILD_DIR}/kg2-drugbank${test_suffix}.json

hmdb_input_file=${BUILD_DIR}/hmdb_metabolites.xml
hmdb_output_file=${BUILD_DIR}/kg2-hmdb${test_suffix}.json

kg1_output_file=${BUILD_DIR}/kg2-rtx-kg1${test_suffix}.json

kg2_tsv_dir=${BUILD_DIR}/TSV
kg2_tsv_tarball=${BUILD_DIR}/kg2-tsv${test_suffix}.tar.gz

version_file=${BUILD_DIR}/kg2-version.txt

# Run snakemake from the virtualenv but run the snakefile in kg2-code
# -F: Run all of the rules in the snakefile
# -R Finish: Run all of the rules in the snakefile
# -j: Run the rules in parallel
# -config: give the test arguments to the snakefile
# -n: dry run REMOVE THIS LATER

export PATH=$PATH:${BUILD_DIR}

cd ~ && ${VENV_DIR}/bin/snakemake --snakefile ${CODE_DIR}/Snakefile \
     -F -j --config TEST_FLAG="${test_flag}" TEST_SUFFIX="${test_suffix}" \
     TEST_ARG="${test_arg}" SEMMED_TUPLELIST_FILE="${semmed_tuplelist_file}" \
     SEMMED_OUTPUT_FILE="${semmed_output_file}" UNIPROTKB_DAT_FILE="${uniprotkb_dat_file}" \
     UNIPROTKB_OUTPUT_FILE="${uniprotkb_output_file}" OUTPUT_FILE_BASE="${output_file_base}" \
     OUTPUT_FILE_FULL="${output_file_full}" OUTPUT_FILE_ORPHAN_EDGES="${output_file_orphan_edge}" \
     FINAL_OUTPUT_FILE_BASE="${final_output_file_base}" FINAL_OUTPUT_FILE_FULL="${final_output_file_full}" \
     SIMPLIFIED_OUTPUT_FILE_BASE="${simplified_output_file_base}" \
     SIMPLIFIED_OUTPUT_FILE_FULL="${simplified_output_file_full}" \
     SIMPLIFIED_OUTPUT_NODES_FILE_BASE="${simplified_output_nodes_file_base}" \
     SIMPLIFIED_OUTPUT_NODES_FILE_FULL="${simplified_output_nodes_file_full}" \
     OUTPUT_NODES_FILE_BASE="${output_nodes_file_base}" OUTPUT_NODES_FILE_FULL="${output_nodes_file_full}" \
     REPORT_FILE_BASE="${report_file_base}" REPORT_FILE_FULL="${report_file_full}" \
     SIMPLIFIED_REPORT_FILE_BASE="${simplified_report_file_base}" SIMPLIFIED_REPORT_FILE_FULL="${simplified_report_file_full}" \
     SLIM_OUTPUT_FILE_FULL="${slim_output_file_full}" ENSEMBL_SOURCE_JSON_FILE="${ensembl_source_json_file}" \
     ENSEMBL_OUTPUT_FILE="${ensembl_output_file}" CHEMBL_OUTPUT_FILE="${chembl_output_file}" \
     OWL_LOAD_INVENTORY_FILE="${owl_load_inventory_file}" CHEMBL_MYSQL_DBNAME="${chembl_mysql_dbname}" \
     UNICHEM_OUTPUT_TSV_FILE="${unichem_output_tsv_file}" UNICHEM_OUTPUT_FILE="${unichem_output_file}" \
     NCBI_GENE_TSV_FILE="${ncbi_gene_tsv_file}" NCBI_GENE_OUTPUT_FILE="${ncbi_gene_output_file}" \
     DGIDB_DIR="${dgidb_dir}" DGIDB_OUTPUT_FILE="${dgidb_output_file}" \
     REPODB_DIR="${repodb_dir}" REPODB_INPUT_FILE="${repodb_input_file}" REPODB_OUTPUT_FILE="${repodb_output_file}" \
     SMPDB_DIR="${smpdb_dir}" SMPDB_INPUT_FILE="${smpdb_input_file}" SMPDB_OUTPUT_FILE="${smpdb_output_file}" \
     DRUGBANK_INPUT_FILE="${drugbank_input_file}" DRUGBANK_OUTPUT_FILE="${drugbank_output_file}" \
     HMDB_INPUT_FILE="${hmdb_input_file}" HMDB_OUTPUT_FILE="${hmdb_output_file}" \
     KG1_OUTPUT_FILE="${kg1_output_file}" RTX_CONFIG_FILE="${rtx_config_file}" \
     KG2_TSV_DIR="${kg2_tsv_dir}" KG2_TSV_TARBALL="${kg2_tsv_tarball}" \
     PREDICATE_MAPPING_FILE="${predicate_mapping_file}" \
     VENV_DIR="${VENV_DIR}" BUILD_DIR="${BUILD_DIR}" CODE_DIR="${CODE_DIR}" CURIES_TO_URLS_FILE="${curies_to_urls_file}" \
     MYSQL_CONF="${mysql_conf}" S3_CP_CMD="${s3_cp_cmd}" VERSION_FILE="${version_file}"

date
echo "================ script finished ============================"
} >${BUILD_DIR}/build-kg2-snakemake.log 2>&1
