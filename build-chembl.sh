#!/usr/bin/env bash
# build-chembl.sh: download ChEMBL TTL files and gunzip them
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 [all|test]"
    exit 2
fi

echo "================= starting build-chembl.sh ================="
date

CONFIG_DIR=`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

CHEMBL_DIR=${BUILD_DIR}/chembl
CHEMBL_BASE_URI=ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBL-RDF
CHEMBL_VERSION=25.0
JENA_DIR=${BUILD_DIR}/apache-jena
JENA_DB_DIR=${CHEMBL_DIR}/jena-db/
CURL_GET="curl -s -L"
CHEMBL_FILES=""

# mkdir -p ${CHEMBL_DIR}

for base_file_type in \
    molecule \
	moa \
	indication \
	document \
	molecule_chebi_ls \
	target \
	targetcmpt \
	targetcmpt_uniprot_ls \
	targetrel \
	unichem \
	singletarget_targetcmpt_ls \
	protclass \
	molhierarchy \
	complextarget_targetcmpt_ls \
	assay \
	activity
do
    CHEMBL_FILE=chembl_${CHEMBL_VERSION}_${base_file_type}.ttl
    if [ ! -f ${CHEMBL_FILE} ]
    then
	${CURL_GET} ${CHEMBL_BASE_URI}/${CHEMBL_VERSION}/chembl_${CHEMBL_VERSION}_${base_file_type}.ttl.gz > \
		    ${CHEMBL_DIR}/chembl_${CHEMBL_VERSION}_${base_file_type}.ttl.gz
	gunzip -f ${CHEMBL_DIR}/chembl_${CHEMBL_VERSION}_${base_file_type}.ttl.gz
    fi
    CHEMBL_FILES="${CHEMBL_FILES} ${CHEMBL_FILE}"
done

rm -r -f ${JENA_DB_DIR}
${JENA_DIR}/bin/tdbloader2 --loc ${JENA_DB_DIR} ${CHEMBL_FILES}

# sudo apt-get -y update
# sudo apt-get 


date
echo "================= script finished ================="
