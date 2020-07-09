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
# * The 'test' argument means that the OWL inventory is read from "owl-load-inventory-test.yaml"
#   and all KG JSON files generated will have the string "-test" appended before their JSON suffixes.

BUILD_FLAG=${1:-""}
echo "${BUILD_FLAG}"

if [ "${BUILD_FLAG}" == 'test' ]
then
    echo "********** TEST MODE **********"
    TEST_SUFFIX='-test'
    TEST_ARG='--test'
else
    TEST_SUFFIX=''
    TEST_ARG=''
fi

## load the master config file
CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

## set the path to include ${BUILD_DIR}
export PATH=$PATH:${BUILD_DIR}

BUILD_KG2_LOG_FILE=${BUILD_DIR}/build-kg2${TEST_SUFFIX}.log

{

echo "================= starting build-kg2.sh ================="
date

echo "running validation tests on KG2 config files"

bash -x ${CODE_DIR}/run-validation-tests.sh

## supply a default value for the BUILD_FLAG string

SEMMED_TUPLELIST_FILE=${BUILD_DIR}/semmeddb/kg2-semmeddb${TEST_SUFFIX}-tuplelist.json
SEMMED_OUTPUT_FILE=${BUILD_DIR}/kg2-semmeddb${TEST_SUFFIX}-edges.json

UNIPROTKB_DAT_FILE=${BUILD_DIR}/uniprotkb/uniprot_sprot.dat
UNIPROTKB_OUTPUT_FILE=${BUILD_DIR}/kg2-uniprotkb${TEST_SUFFIX}.json

OUTPUT_FILE_BASE=kg2-owl${TEST_SUFFIX}.json
OUTPUT_FILE_FULL=${BUILD_DIR}/${OUTPUT_FILE_BASE}

OUTPUT_FILE_ORPHAN_EDGES=${BUILD_DIR}/kg2-orphans${TEST_SUFFIX}-edges.json

FINAL_OUTPUT_FILE_BASE=kg2${TEST_SUFFIX}.json
FINAL_OUTPUT_FILE_FULL=${BUILD_DIR}/${FINAL_OUTPUT_FILE_BASE}

SIMPLIFIED_OUTPUT_FILE_BASE=kg2-simplified${TEST_SUFFIX}.json
SIMPLIFIED_OUTPUT_FILE_FULL=${BUILD_DIR}/${SIMPLIFIED_OUTPUT_FILE_BASE}

SIMPLIFIED_OUTPUT_NODES_FILE_BASE=kg2-simplified${TEST_SUFFIX}-nodes.json
SIMPLIFIED_OUTPUT_NODES_FILE_FULL=${BUILD_DIR}/${SIMPLIFIED_OUTPUT_NODES_FILE_BASE}

OUTPUT_NODES_FILE_BASE=kg2${TEST_SUFFIX}-nodes.json
OUTPUT_NODES_FILE_FULL=${BUILD_DIR}/${OUTPUT_NODES_FILE_BASE}

REPORT_FILE_BASE=kg2-report${TEST_SUFFIX}.json
REPORT_FILE_FULL=${BUILD_DIR}/${REPORT_FILE_BASE}

SIMPLIFIED_REPORT_FILE_BASE=kg2-simplified-report${TEST_SUFFIX}.json
SIMPLIFIED_REPORT_FILE_FULL=${BUILD_DIR}/${SIMPLIFIED_REPORT_FILE_BASE}

SLIM_OUTPUT_FILE_FULL=${BUILD_DIR}/kg2-slim${TEST_SUFFIX}.json

ENSEMBL_SOURCE_JSON_FILE=${BUILD_DIR}/ensembl/ensembl_genes_homo_sapiens.json
ENSEMBL_OUTPUT_FILE=${BUILD_DIR}/kg2-ensembl${TEST_SUFFIX}.json

CHEMBL_OUTPUT_FILE=${BUILD_DIR}/kg2-chembl${TEST_SUFFIX}.json
CHEMBL_MYSQL_DBNAME=chembl

UNICHEM_OUTPUT_TSV_FILE=${BUILD_DIR}/unichem/chembl-to-curies.tsv
UNICHEM_OUTPUT_FILE=${BUILD_DIR}/kg2-unichem${TEST_SUFFIX}.json

NCBI_GENE_TSV_FILE=${BUILD_DIR}/ncbigene/Homo_sapiens_gene_info.tsv
NCBI_GENE_OUTPUT_FILE=${BUILD_DIR}/kg2-ncbigene${TEST_SUFFIX}.json

DGIDB_DIR=${BUILD_DIR}/dgidb
DGIDB_OUTPUT_FILE=${BUILD_DIR}/kg2-dgidb${TEST_SUFFIX}.json

REPODB_DIR=${BUILD_DIR}/repodb
REPODB_INPUT_FILE=${BUILD_DIR}/repodb/repodb.csv
REPODB_OUTPUT_FILE=${BUILD_DIR}/kg2-repodb${TEST_SUFFIX}.json

SMPDB_DIR=${BUILD_DIR}/smpdb/
SMPDB_INPUT_FILE=${SMPDB_DIR}/smpdb_pathways.csv
SMPDB_OUTPUT_FILE=${BUILD_DIR}/kg2-smpdb.json

DRUGBANK_INPUT_FILE=${BUILD_DIR}/drugbank.xml
DRUGBANK_OUTPUT_FILE=${BUILD_DIR}/kg2-drugbank${TEST_SUFFIX}.json

KG1_OUTPUT_FILE=${BUILD_DIR}/kg2-rtx-kg1${TEST_SUFFIX}.json
RTX_CONFIG_FILE=${BUILD_DIR}/RTXConfiguration-config.json

KG2_TSV_DIR=${BUILD_DIR}/TSV
KG2_TSV_TARBALL=${BUILD_DIR}/kg2-tsv${TEST_SUFFIX}.tar.gz

cd ${BUILD_DIR}

MEM_GB=`${CODE_DIR}/get-system-memory-gb.sh`

if [ "${BUILD_FLAG}" == 'all' ]
then
## Build UMLS knowledge sources at TTL files:
    echo "running extract-umls.sh"
    bash -x ${CODE_DIR}/extract-umls.sh ${BUILD_DIR}
## Extract UniprotKB
    echo "running extract-uniprotkb.sh"
    bash -x ${CODE_DIR}/extract-uniprotkb.sh ${UNIPROTKB_DAT_FILE}
## Extract SemMedDB to tuple-list JSON
    echo "running extract-semmeddb.sh"
    bash -x ${CODE_DIR}/extract-semmeddb.sh ${SEMMED_TUPLELIST_FILE}
## Extract Ensembl
    echo "running extract-ensembl.sh"
    bash -x ${CODE_DIR}/extract-ensembl.sh ${ENSEMBL_SOURCE_JSON_FILE}
## Extract ChEMBL
    echo "running extract-chembl.sh"
    bash -x ${CODE_DIR}/extract-chembl.sh ${CHEMBL_MYSQL_DBNAME}
## Extract UniChem chembl-to-chebi mappings
    echo "running extract-unichem.sh"
    bash -x ${CODE_DIR}/extract-unichem.sh ${UNICHEM_OUTPUT_TSV_FILE}
## Extract NCBI Gene
    echo "running extract-ncbigene.sh"
    bash -x ${CODE_DIR}/extract-ncbigene.sh ${NCBI_GENE_TSV_FILE}
## Extract DGIDB
    echo "running extract-dgidb.sh"
    bash -x ${CODE_DIR}/extract-dgidb.sh ${DGIDB_DIR}
## Download REPODB
    echo "running download-repodb-csv.sh"
    bash -x ${CODE_DIR}/download-repodb-csv.sh ${REPODB_DIR}

## Download SMPDB
    echo "running extract-smpdb.sh"
    bash -x ${CODE_DIR}/extract-smpdb.sh ${SMPDB_DIR}

## Download DrugBank
    echo "running extract-drubank.sh"
    bash -x ${CODE_DIR}/extract-smpdb.sh ${DRUGBANK_INPUT_FILE}
fi

echo "running uniprotkb_dat_to_json.py"

## extract JSON file for UniProtKB
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/uniprotkb_dat_to_json.py \
           ${TEST_ARG} \
	   ${UNIPROTKB_DAT_FILE} \
	   ${UNIPROTKB_OUTPUT_FILE} 

echo "running semmeddb_tuple_list_json_to_kg_json.py"

MRCUI_RRF_FILE=${UMLS_DEST_DIR}/MRCUI.RRF
if [ -f "${MRCUI_RRF_FILE}" ]
then
    MRCUI_ARG="--mrcuiFile ${MRCUI_RRF_FILE}"
else
    echo "WARNING: the MRCUI.RRF file is not found! proceeding withoutthe MRCUI.RRF-based CUI mapping"
    MRCUI_ARG=""
fi
## Build SemMedDB KG2 edges file as JSON:
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/semmeddb_tuple_list_json_to_kg_json.py \
           ${TEST_ARG} \
           ${MRCUI_ARG} \
           ${SEMMED_TUPLELIST_FILE} \
           ${SEMMED_OUTPUT_FILE}

echo "running ensembl_json_to_kg_json.py"

## Build Ensembl KG2 edges file as JSON:
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/ensembl_json_to_kg_json.py \
           ${TEST_ARG} \
           ${ENSEMBL_SOURCE_JSON_FILE} \
           ${ENSEMBL_OUTPUT_FILE}

echo "running chembl_mysql_to_kg_json.py"

## Build Chembl KG2 edges file as JSON:
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/chembl_mysql_to_kg_json.py \
           ${TEST_ARG} \
           ${MYSQL_CONF} \
           ${CHEMBL_MYSQL_DBNAME} \
           ${CHEMBL_OUTPUT_FILE}

echo "running build-multi-owl-kg.sh"

## Combine all the TTL files and OBO Foundry OWL files into KG and save as JSON:
bash -x ${CODE_DIR}/build-multi-owl-kg.sh \
           ${OUTPUT_FILE_FULL} ${BUILD_FLAG}

echo "running unichem_tsv_to_edges_json.py"

## Make JSON file for UniChem

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/unichem_tsv_to_edges_json.py \
           ${TEST_ARG} \
           ${UNICHEM_OUTPUT_TSV_FILE} \
           ${UNICHEM_OUTPUT_FILE}

echo "running ncbigene_tsv_to_kg_json.py"

## Make JSON file for NCBI Gene

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/ncbigene_tsv_to_kg_json.py \
           ${TEST_ARG} \
           ${NCBI_GENE_TSV_FILE} \
           ${NCBI_GENE_OUTPUT_FILE}

echo "running dgidb_tsv_to_kg_json.py"

## Make JSON file for DGIDB

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/dgidb_tsv_to_kg_json.py \
           ${TEST_ARG} \
           ${DGIDB_DIR}/interactions.tsv \
           ${DGIDB_OUTPUT_FILE} 2> ${DGIDB_DIR}/dgidb-tsv-to-kg-json.log

echo "running repodb_csv_to_kg_json.py"

## Make JSON file for REPODB

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/repodb_csv_to_kg_json.py \
           ${TEST_ARG} \
           ${REPODB_INPUT_FILE} \
           ${REPODB_OUTPUT_FILE} 2> ${REPODB_DIR}/repodb-csv-to-kg-json.log

echo "running drugbank_xml_to_kg_json.py"

## Make JSON file for DrugBank

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/drugbank_xml_to_kg_json.py \
           ${TEST_ARG} \
           ${DRUGBANK_INPUT_FILE} \
           ${DRUGBANK_OUTPUT_FILE} 2> ${BUILD_DIR}/drugbank-xml-to-kg-json.log

## Make JSON file for DrugBank

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/smpdb_csv_to_kg_json.py \
           ${TEST_ARG} \
           ${SMPDB_INPUT_FILE} \
           ${SMPDB_OUTPUT_FILE}

echo "copying RTX Configuration JSON file from S3"

${S3_CP_CMD} s3://${S3_BUCKET}/${RTX_CONFIG_FILE} ${BUILD_DIR}/${RTX_CONFIG_FILE}

echo "extracting KG JSON representation of RTX KG1, from the Neo4j endpoint"

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/rtx_kg1_neo4j_to_kg_json.py \
           ${TEST_ARG} \
           --configFile ${BUILD_DIR}/${RTX_CONFIG_FILE} \
           ${KG1_OUTPUT_FILE}

echo "running merge_graphs.py"

## Merge all the KG JSON files

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/merge_graphs.py \
           ${TEST_ARG} \
           --kgFiles ${OUTPUT_FILE_FULL} \
                     ${SEMMED_OUTPUT_FILE} \
                     ${UNIPROTKB_OUTPUT_FILE} \
                     ${ENSEMBL_OUTPUT_FILE} \
                     ${UNICHEM_OUTPUT_FILE} \
                     ${CHEMBL_OUTPUT_FILE} \
                     ${NCBI_GENE_OUTPUT_FILE} \
                     ${DGIDB_OUTPUT_FILE} \
                     ${REPODB_OUTPUT_FILE} \
                     ${KG1_OUTPUT_FILE} \
		     ${SMPDB_OUTPUT_FILE} \
		     ${DRUGBANK_OUTPUT_FILE} \
           --kgFileOrphanEdges ${OUTPUT_FILE_ORPHAN_EDGES} \
           ${FINAL_OUTPUT_FILE_FULL}

echo "running get_nodes_json_from_kg_json.py"

## Get a JSON file with just the nodes in it

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/get_nodes_json_from_kg_json.py \
           ${TEST_ARG} \
           ${FINAL_OUTPUT_FILE_FULL} \
           ${OUTPUT_NODES_FILE_FULL}

echo "report_stats_on_json_kg.py (full KG)"

## Generate a JSON report of statistics on the KG

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/report_stats_on_json_kg.py \
           ${FINAL_OUTPUT_FILE_FULL} \
           ${REPORT_FILE_FULL}

echo "filter the JSON KG and remap predicates"

## Filter the JSON KG and remap predicates:

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/filter_kg_and_remap_predicates.py \
           ${TEST_ARG} \
           --dropNegated \
           --dropSelfEdgesExcept interacts_with,positively_regulates,inhibits,increase \
           ${PREDICATE_MAPPING_FILE} \
           ${CURIES_TO_URLS_FILE} \
           ${FINAL_OUTPUT_FILE_FULL} \
           ${SIMPLIFIED_OUTPUT_FILE_FULL}

echo "running get_nodes_json_from_kg_json.py (for simplified KG)"

## Get a JSON file with just the nodes in it

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/get_nodes_json_from_kg_json.py \
           ${TEST_ARG} \
           ${SIMPLIFIED_OUTPUT_FILE_FULL} \
           ${SIMPLIFIED_OUTPUT_NODES_FILE_FULL}

echo "generating slimmed-down kg2 (issue #597)"

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/slim_kg2.py \
           ${TEST_ARG} \
           ${SIMPLIFIED_OUTPUT_FILE_FULL} \
           ${SLIM_OUTPUT_FILE_FULL} 

echo "report_stats_on_json_kg.py (simplified KG)"

## Generate a JSON report of statistics on the KG

${VENV_DIR}/bin/python3 -u ${CODE_DIR}/report_stats_on_json_kg.py \
           --useSimplifiedPredicates \
           ${SIMPLIFIED_OUTPUT_FILE_FULL} \
           ${SIMPLIFIED_REPORT_FILE_FULL}

gzip -f ${FINAL_OUTPUT_FILE_FULL}

## build the TSV files
rm -r -f ${KG2_TSV_DIR}
mkdir -p ${KG2_TSV_DIR}
${VENV_DIR}/bin/python3 -u ${CODE_DIR}/kg_json_to_tsv.py \
           ${SIMPLIFIED_OUTPUT_FILE_FULL} \
           ${KG2_TSV_DIR}

tar -C ${KG2_TSV_DIR} -czvf ${KG2_TSV_TARBALL} nodes.tsv nodes_header.tsv edges.tsv edges_header.tsv
${S3_CP_CMD} ${KG2_TSV_TARBALL} s3://${S3_BUCKET}/

## Compress the huge files
gzip -f ${SIMPLIFIED_OUTPUT_FILE_FULL}
gzip -f ${SIMPLIFIED_OUTPUT_NODES_FILE_FULL}
gzip -f ${OUTPUT_NODES_FILE_FULL}
gzip -f ${OUTPUT_FILE_ORPHAN_EDGES}
gzip -f ${SLIM_OUTPUT_FILE_FULL}

## copy the KG and various build artifacts to the public S3 bucket
${S3_CP_CMD} ${FINAL_OUTPUT_FILE_FULL}.gz s3://${S3_BUCKET}/
${S3_CP_CMD} ${SIMPLIFIED_OUTPUT_FILE_FULL}.gz s3://${S3_BUCKET}/
${S3_CP_CMD} ${OUTPUT_NODES_FILE_FULL}.gz s3://${S3_BUCKET}/
${S3_CP_CMD} ${REPORT_FILE_FULL} s3://${S3_BUCKET_PUBLIC}/
${S3_CP_CMD} ${SIMPLIFIED_REPORT_FILE_FULL} s3://${S3_BUCKET_PUBLIC}/
${S3_CP_CMD} ${OUTPUT_FILE_ORPHAN_EDGES}.gz s3://${S3_BUCKET_PUBLIC}/
${S3_CP_CMD} ${SLIM_OUTPUT_FILE_FULL}.gz s3://${S3_BUCKET}/
${S3_CP_CMD} ${SIMPLIFIED_OUTPUT_NODES_FILE_FULL}.gz s3://${S3_BUCKET}/

## copy the log files to the public S3 bucket
BUILD_MULTI_OWL_STDERR_FILE="${BUILD_DIR}/build-${OUTPUT_FILE_BASE%.*}"-stderr.log

${S3_CP_CMD} ${BUILD_MULTI_OWL_STDERR_FILE} s3://${S3_BUCKET_PUBLIC}/

## copy the config files to the public S3 bucket
${S3_CP_CMD} ${OWL_LOAD_INVENTORY_FILE} s3://${S3_BUCKET_PUBLIC}/

# copy the index.html file to the public S3 bucket
${S3_CP_CMD} ${CODE_DIR}/s3-index.html s3://${S3_BUCKET_PUBLIC}/index.html


date
echo "================= finished build-kg2.sh ================="

} >${BUILD_KG2_LOG_FILE} 2>&1

# copy the KG2 build log file to the S3 bucket
${S3_CP_CMD} ${BUILD_KG2_LOG_FILE} s3://${S3_BUCKET_PUBLIC}/

