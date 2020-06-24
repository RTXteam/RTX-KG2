#!/usr/bin/env bash
# extract-unichem.sh: download UniChem and extract TSV of (chembl,chebi) pairs
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_tsv_file>"
    exit 2
fi

echo "================= starting build-unichem.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc
output_tsv_file=${1:-"${BUILD_DIR}/unichem/chembl-to-curies.tsv"}
unichem_dir=${BUILD_DIR}/unichem
unichem_output_dir=`dirname ${output_tsv_file}`
unichem_ver=280
unichem_ftp_site=ftp://ftp.ebi.ac.uk/pub/databases/chembl/UniChem/data

rm -r -f ${unichem_dir}
mkdir -p ${unichem_dir}
mkdir -p ${unichem_output_dir}

${CURL_GET} ${unichem_ftp_site}/oracleDumps/UDRI${unichem_ver}/UC_XREF.txt.gz > ${unichem_dir}/UC_XREF.txt.gz
${CURL_GET} ${unichem_ftp_site}/oracleDumps/UDRI${unichem_ver}/UC_SOURCE.txt.gz > ${unichem_dir}/UC_SOURCE.txt.gz
${CURL_GET} ${unichem_ftp_site}/oracleDumps/UDRI${unichem_ver}/UC_RELEASE.txt.gz > ${unichem_dir}/UC_RELEASE.txt.gz

chembl_src_id=`zcat ${unichem_dir}/UC_SOURCE.txt.gz | awk '{if ($2 == "chembl") {printf "%s", $1}}'`
chebi_src_id=`zcat ${unichem_dir}/UC_SOURCE.txt.gz | awk '{if ($2 == "chebi") {printf "%s", $1}}'`
drugbank_src_id=`zcat ${unichem_dir}/UC_SOURCE.txt.gz | awk '{if ($2 == "drugbank") {printf "%s", $1}}'`

update_date=`zcat ${unichem_dir}/UC_RELEASE.txt.gz | tail -1 | cut -f3`
echo "# ${update_date}" > ${output_tsv_file}

zcat ${unichem_dir}/UC_XREF.txt.gz | awk '{if ($2 == '${chebi_src_id}') {print $1 "\tCHEBI:" $3}}' | sort -k1 > ${unichem_dir}/chebi.txt
zcat ${unichem_dir}/UC_XREF.txt.gz | awk '{if ($2 == '${chembl_src_id}') {print $1 "\tCHEMBL.COMPOUND:" $3}}' | sort -k1 > ${unichem_dir}/chembl.txt
zcat ${unichem_dir}/UC_XREF.txt.gz | awk '{if ($2 == '${drugbank_src_id}') {print $1 "\tDRUGBANK:" $3}}' | sort -k1 > ${unichem_dir}/drugbank.txt

join ${unichem_dir}/chembl.txt ${unichem_dir}/chebi.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/chembl.txt ${unichem_dir}/drugbank.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}

date
echo "================= script finished ================="
