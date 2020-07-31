#!/usr/bin/env bash
# build-kg2.sh:  main build script for the KG2 knowledge graph for the RTX biomedical reasoning system
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [all|test]"
    exit 2
fi

# Usage: build-kg2.sh [all|test]
# * If no argument, then by default only the OWL-based KG2 is generated from scratch. It is then merged
#   with the pre-existing SemMedDB JSON file. 
# 
# * The 'all' argument means that the script will build the UMLS and SemMedDB files. Complete KG2 build.
#
# * The 'test' argument means that the OWL inventory is read from "ont-load-inventory-test.yaml"
#   and all KG JSON files generated will have the string "-test" appended before their JSON suffixes.

build_flag=${1:-""}
echo "${build_flag}"

if [ "${build_flag}" == 'test' ]
then
    echo "********** TEST MODE **********"
    test_suffix='-test'
    test_arg='--test'
else
    test_suffix=''
    test_arg=''
fi

## load the master config file
config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

build_kg2_log_file=${BUILD_DIR}/build-kg2${test_suffix}.log

{

echo "================= starting build-kg2.sh ================="
date

echo `hostname`

echo "running validation tests on KG2 config files"

bash -x ${CODE_DIR}/run-validation-tests.sh

## supply a default value for the build_flag string

semmed_tuplelist_file=${BUILD_DIR}/semmeddb/kg2-semmeddb${test_suffix}-tuplelist.json
semmed_output_file=${BUILD_DIR}/kg2-semmeddb${test_suffix}-edges.json

uniprotkb_dat_file=${BUILD_DIR}/uniprotkb/uniprot_sprot.dat
uniprotkb_output_file=${BUILD_DIR}/kg2-uniprotkb${test_suffix}.json

output_file_base=kg2-ont${test_suffix}.json
output_file_full=${BUILD_DIR}/${output_file_base}

output_file_orphan_edges=${BUILD_DIR}/kg2-orphans${test_suffix}-edges.json

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
chembl_mysql_dbname=chembl

unichem_output_tsv_file=${BUILD_DIR}/unichem/chembl-to-curies.tsv
unichem_output_file=${BUILD_DIR}/kg2-unichem${test_suffix}.json

ncbi_tsv_gene_file=${BUILD_DIR}/ncbigene/Homo_sapiens_gene_info.tsv
ncbi_gene_output_file=${BUILD_DIR}/kg2-ncbigene${test_suffix}.json

dgidb_dir=${BUILD_DIR}/dgidb
dgidb_output_file=${BUILD_DIR}/kg2-dgidb${test_suffix}.json

repodb_dir=${BUILD_DIR}/repodb
repodb_input_file=${BUILD_DIR}/repodb/repodb.csv
repodb_output_file=${BUILD_DIR}/kg2-repodb${test_suffix}.json

smpdb_dir=${BUILD_DIR}/smpdb
smpdb_output_file=${BUILD_DIR}/kg2-smpdb.json

drugbank_input_file=${BUILD_DIR}/drugbank.xml
drugbank_output_file=${BUILD_DIR}/kg2-drugbank${test_suffix}.json

hmdb_input_file=${BUILD_DIR}/hmdb_metabolites.xml
hmdb_output_file=${BUILD_DIR}/kg2-hmdb${test_suffix}.json

kg1_output_file=${BUILD_DIR}/kg2-rtx-kg1${test_suffix}.json

kg2_tsv_dir=${BUILD_DIR}/TSV
kg2_tsv_tarball=${BUILD_DIR}/kg2-tsv${test_suffix}.tar.gz

version_file=${BUILD_DIR}/kg2-version.txt

cd ${BUILD_DIR}

mem_gb=`${CODE_DIR}/get-system-memory-gb.sh`

if [ "${build_flag}" == 'all' ]
then
## Build UMLS knowledge sources at TTL files:
    echo "running extract-umls.sh"
    bash -x ${CODE_DIR}/extract-umls.sh ${BUILD_DIR}
## Extract UniprotKB
    echo "running extract-uniprotkb.sh"
    bash -x ${CODE_DIR}/extract-uniprotkb.sh ${uniprotkb_dat_file}
## Extract SemMedDB to tuple-list JSON
    echo "running extract-semmeddb.sh"
    bash -x ${CODE_DIR}/extract-semmeddb.sh ${semmed_tuplelist_file}
## Extract Ensembl
    echo "running extract-ensembl.sh"
    bash -x ${CODE_DIR}/extract-ensembl.sh ${ensembl_source_json_file}
## Extract ChEMBL
    echo "running extract-chembl.sh"
    bash -x ${CODE_DIR}/extract-chembl.sh ${chembl_mysql_dbname}
## Extract UniChem chembl-to-chebi mappings
    echo "running extract-unichem.sh"
    bash -x ${CODE_DIR}/extract-unichem.sh ${unichem_output_tsv_file}
## Extract NCBI Gene
    echo "running extract-ncbigene.sh"
    bash -x ${CODE_DIR}/extract-ncbigene.sh ${ncbi_tsv_gene_file}
## Extract DGIDB
    echo "running extract-dgidb.sh"
    bash -x ${CODE_DIR}/extract-dgidb.sh ${dgidb_dir}
## Download REPODB
    echo "running download-repodb-csv.sh"
    bash -x ${CODE_DIR}/download-repodb-csv.sh ${repodb_dir}

## Download SMPDB
    echo "running extract-smpdb.sh"
    bash -x ${CODE_DIR}/extract-smpdb.sh ${smpdb_dir}

## Download DrugBank
    echo "running extract-drugbank.sh"
    bash -x ${CODE_DIR}/extract-drugbank.sh ${drugbank_input_file}

## Download HMDB
  echo "running extract-hmdb.sh"
  bash -x ${CODE_DIR}/extract-hmdb.sh
fi

echo "running uniprotkb_dat_to_json.py"

## extract JSON file for UniProtKB
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/uniprotkb_dat_to_json.py \
           ${test_arg} \
	   ${uniprotkb_dat_file} \
	   ${uniprotkb_output_file} 

echo "running semmeddb_tuple_list_json_to_kg_json.py"

mrcui_rrf_file=${umls_dest_dir}/MRCUI.RRF
if [ -f "${mrcui_rrf_file}" ]
then
    mrcui_arg="--mrcuiFile ${mrcui_rrf_file}"
else
    echo "WARNING: the MRCUI.RRF file is not found! proceeding withoutthe MRCUI.RRF-based CUI mapping"
    mrcui_arg=""
fi
## Build SemMedDB KG2 edges file as JSON:
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/semmeddb_tuple_list_json_to_kg_json.py \
           ${test_arg} \
           ${mrcui_arg} \
           ${semmed_tuplelist_file} \
           ${semmed_output_file}

echo "running ensembl_json_to_kg_json.py"

## Build Ensembl KG2 edges file as JSON:
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/ensembl_json_to_kg_json.py \
           ${test_arg} \
           ${ensembl_source_json_file} \
           ${ensembl_output_file}

echo "running chembl_mysql_to_kg_json.py"

## Build Chembl KG2 edges file as JSON:
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/chembl_mysql_to_kg_json.py \
           ${test_arg} \
           ${mysql_conf} \
           ${chembl_mysql_dbname} \
           ${chembl_output_file}

echo "running build-multi-ont-kg.sh"

## Combine all the TTL files and OBO Foundry OWL files into KG and save as JSON:
bash -x ${CODE_DIR}/build-multi-ont-kg.sh \
           ${output_file_full} ${build_flag}

echo "running unichem_tsv_to_edges_json.py"

## Make JSON file for UniChem

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/unichem_tsv_to_edges_json.py \
           ${test_arg} \
           ${unichem_output_tsv_file} \
           ${unichem_output_file}

echo "running ncbigene_tsv_to_kg_json.py"

## Make JSON file for NCBI Gene

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/ncbigene_tsv_to_kg_json.py \
           ${test_arg} \
           ${ncbi_tsv_gene_file} \
           ${ncbi_gene_output_file}

echo "running dgidb_tsv_to_kg_json.py"

## Make JSON file for DGIDB

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/dgidb_tsv_to_kg_json.py \
           ${test_arg} \
           ${dgidb_dir}/interactions.tsv \
           ${dgidb_output_file} 2> ${dgidb_dir}/dgidb-tsv-to-kg-json-stderr.log

echo "running repodb_csv_to_kg_json.py"

## Make JSON file for REPODB

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/repodb_csv_to_kg_json.py \
           ${test_arg} \
           ${repodb_input_file} \
           ${repodb_output_file} 2> ${repodb_dir}/repodb-csv-to-kg-json-stderr.log

echo "running drugbank_xml_to_kg_json.py"

## Make JSON file for DrugBank

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/drugbank_xml_to_kg_json.py \
           ${test_arg} \
           ${drugbank_input_file} \
           ${drugbank_output_file} 2> ${BUILD_DIR}/drugbank-xml-to-kg-json-stderr.log

echo "running smpdb_csv_to_kg_json.py"

## Make JSON file for SMPDB

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/smpdb_csv_to_kg_json.py \
           ${test_arg} \
           ${smpdb_dir} \
           ${smpdb_output_file}

echo "running hmdb_xml_to_kg_json.py"

## Make JSON file for HMDB

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/hmdb_xml_to_kg_json.py \
           ${test_arg} \
           ${hmdb_input_file} \
           ${hmdb_output_file}

echo "copying RTX Configuration JSON file from S3"

${s3_cp_cmd} s3://${s3_bucket}/${rtx_config_file} ${BUILD_DIR}/${rtx_config_file}

echo "extracting KG JSON representation of RTX KG1, from the Neo4j endpoint"

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/rtx_kg1_neo4j_to_kg_json.py \
           ${test_arg} \
           --configFile ${BUILD_DIR}/${rtx_config_file} \
           ${curies_to_urls_file} \
           ${kg1_output_file}

echo "running merge_graphs.py"

## Merge all the KG JSON files

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/merge_graphs.py \
           ${test_arg} \
           --kgFiles ${output_file_full} \
                     ${semmed_output_file} \
                     ${uniprotkb_output_file} \
                     ${ensembl_output_file} \
                     ${unichem_output_file} \
                     ${chembl_output_file} \
                     ${ncbi_gene_output_file} \
                     ${dgidb_output_file} \
                     ${repodb_output_file} \
                     ${smpdb_output_file} \
                     ${drugbank_output_file} \
                     ${hmdb_output_file} \
                     ${kg1_output_file} \
           --kgFileOrphanEdges ${output_file_orphan_edges} \
           ${final_output_file_full}

echo "running get_nodes_json_from_kg_json.py"

## Get a JSON file with just the nodes in it

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/get_nodes_json_from_kg_json.py \
           ${test_arg} \
           ${final_output_file_full} \
           ${output_nodes_file_full}

echo "report_stats_on_json_kg.py (full KG)"

## Generate a JSON report of statistics on the KG

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/report_stats_on_json_kg.py \
           ${final_output_file_full} \
           ${report_file_full}


echo "increase version of KG2"

## Increase the version of KG2

bash -x ${CODE_DIR}/version.sh ${VERSION_FILE}

echo "filter the JSON KG and remap predicates"

## Filter the JSON KG and remap predicates:

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/filter_kg_and_remap_predicates.py \
           ${test_arg} \
           --dropNegated \
           --dropSelfEdgesExcept interacts_with,positively_regulates,inhibits,increase \
           ${predicate_mapping_file} \
           ${curies_to_urls_file} \
           ${final_output_file_full} \
           ${simplified_output_file_full} \
           ${version_file}

echo "running get_nodes_json_from_kg_json.py (for simplified KG)"

## Get a JSON file with just the nodes in it

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/get_nodes_json_from_kg_json.py \
           ${test_arg} \
           ${simplified_output_file_full} \
           ${simplified_output_nodes_file_full}

echo "generating slimmed-down kg2 (issue #597)"

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/slim_kg2.py \
           ${test_arg} \
           ${simplified_output_file_full} \
           ${slim_output_file_full} 

echo "report_stats_on_json_kg.py (simplified KG)"

## Generate a JSON report of statistics on the KG

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/report_stats_on_json_kg.py \
           --useSimplifiedPredicates \
           ${simplified_output_file_full} \
           ${simplified_report_file_full}

gzip -f ${final_output_file_full}

## build the TSV files
rm -r -f ${kg2_tsv_dir}
mkdir -p ${kg2_tsv_dir}
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/kg_json_to_tsv.py \
           ${simplified_output_file_full} \
           ${kg2_tsv_dir}

tar -C ${kg2_tsv_dir} -czvf ${kg2_tsv_tarball} nodes.tsv nodes_header.tsv edges.tsv edges_header.tsv
${s3_cp_cmd} ${kg2_tsv_tarball} s3://${s3_bucket}/

## Compress the huge files
gzip -f ${simplified_output_file_full}
gzip -f ${simplified_output_nodes_file_full}
gzip -f ${output_nodes_file_full}
gzip -f ${output_file_orphan_edges}
gzip -f ${slim_output_file_full}

## copy the KG and various build artifacts to the public S3 bucket
${s3_cp_cmd} ${final_output_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${simplified_output_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${output_nodes_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${report_file_full} s3://${s3_bucket_public}/
${s3_cp_cmd} ${simplified_report_file_full} s3://${s3_bucket_public}/
${s3_cp_cmd} ${output_file_orphan_edges}.gz s3://${s3_bucket_public}/
${s3_cp_cmd} ${slim_output_file_full}.gz s3://${s3_bucket}/
${s3_cp_cmd} ${simplified_output_nodes_file_full}.gz s3://${s3_bucket}/

## copy the log files to the public S3 bucket
build_multi_owl_stderr_file="${BUILD_DIR}/build-${output_file_base%.*}"-stderr.log

${s3_cp_cmd} ${build_multi_owl_stderr_file} s3://${s3_bucket_public}/

## copy the config files to the public S3 bucket
${s3_cp_cmd} ${ont_load_inventory_file} s3://${s3_bucket_public}/

# copy the index.html file to the public S3 bucket
${s3_cp_cmd} ${CODE_DIR}/s3-index.html s3://${s3_bucket_public}/index.html


date
echo "================= finished build-kg2.sh ================="

} >${build_kg2_log_file} 2>&1

# copy the KG2 build log file to the S3 bucket
${s3_cp_cmd} ${build_kg2_log_file} s3://${s3_bucket_public}/

# copy the log files and reports to the versioned S3 bucket
${s3_cp_cmd} ${build_kg2_log_file} s3://${s3_bucket_versioned}/
${s3_cp_cmd} ${report_file_full} s3://${s3_bucket_versioned}/
${s3_cp_cmd} ${simplified_report_file_full} s3://${s3_bucket_versioned}/
${s3_cp_cmd} ${build_multi_owl_stderr_file} s3://${s3_bucket_public_versioned}/
