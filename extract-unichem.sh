#!/usr/bin/env bash
# extract-unichem.sh: download UniChem and extract TSV of (chembl,chebi) pairs
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0 <output_tsv_file>"
    exit 2
fi

echo "================= starting extract-unichem.sh ================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc
output_tsv_file=${1:-"${BUILD_DIR}/unichem/unichem-mappings.tsv"}
unichem_dir=${BUILD_DIR}/unichem
unichem_output_dir=`dirname ${output_tsv_file}`
unichem_ftp_site=ftp://ftp.ebi.ac.uk/pub/databases/chembl/UniChem/data/table_dumps

uc_xref_filename=reference.tsv.gz
uc_source_filename=source.tsv.gz

rm -r -f ${unichem_dir}
mkdir -p ${unichem_dir}
mkdir -p ${unichem_output_dir}

${curl_get} ${unichem_ftp_site}/${uc_xref_filename} -o ${unichem_dir}/${uc_xref_filename}
${curl_get} ${unichem_ftp_site}/${uc_source_filename} -o ${unichem_dir}/${uc_source_filename}

chembl_src_id=`zcat ${unichem_dir}/${uc_source_filename} | awk '{if ($2 == "chembl") {printf "%s", $1}}'`
chebi_src_id=`zcat ${unichem_dir}/${uc_source_filename} | awk '{if ($2 == "chebi") {printf "%s", $1}}'`
drugbank_src_id=`zcat ${unichem_dir}/${uc_source_filename} | awk '{if ($2 == "drugbank") {printf "%s", $1}}'`
kegg_src_id=`zcat ${unichem_dir}/${uc_source_filename} | awk '{if ($2 == "kegg_ligand") {printf "%s", $1}}'`
drugcentral_src_id=`zcat ${unichem_dir}/${uc_source_filename} | awk '{if ($2 == "drugcentral") {printf "%s", $1}}'`
hmdb_src_id=`zcat ${unichem_dir}/${uc_source_filename} | awk '{if ($2 == "hmdb") {printf "%s", $1}}'`

zcat ${unichem_dir}/${uc_xref_filename} | awk '{if ($2 == '${chebi_src_id}') {print $1 "\tCHEBI:" $3}}' | sort -k1 > ${unichem_dir}/chebi.txt
zcat ${unichem_dir}/${uc_xref_filename} | awk '{if ($2 == '${chembl_src_id}') {print $1 "\tCHEMBL.COMPOUND:" $3}}' | sort -k1 > ${unichem_dir}/chembl.txt
zcat ${unichem_dir}/${uc_xref_filename} | awk '{if ($2 == '${drugbank_src_id}') {print $1 "\tDRUGBANK:" $3}}' | sort -k1 > ${unichem_dir}/drugbank.txt
zcat ${unichem_dir}/${uc_xref_filename} | awk '{if ($2 == '${kegg_src_id}') {print $1 "\tKEGG:" $3}}' | sort -k1 > ${unichem_dir}/kegg.txt
zcat ${unichem_dir}/${uc_xref_filename} | awk '{if ($2 == '${drugcentral_src_id}') {print $1 "\tDrugCentral:" $3}}' | sort -k1 > ${unichem_dir}/drugcentral.txt
zcat ${unichem_dir}/${uc_xref_filename} | awk '{if ($2 == '${hmdb_src_id}') {print $1 "\tHMDB:" $3}}' | sort -k1 > ${unichem_dir}/hmdb.txt

join ${unichem_dir}/chembl.txt ${unichem_dir}/chebi.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/chembl.txt ${unichem_dir}/drugbank.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/chembl.txt ${unichem_dir}/kegg.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/chembl.txt ${unichem_dir}/drugcentral.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/chembl.txt ${unichem_dir}/hmdb.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/chebi.txt ${unichem_dir}/drugbank.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/chebi.txt ${unichem_dir}/kegg.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/chebi.txt ${unichem_dir}/drugcentral.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/chebi.txt ${unichem_dir}/hmdb.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/drugbank.txt ${unichem_dir}/kegg.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/drugbank.txt ${unichem_dir}/drugcentral.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/drugbank.txt ${unichem_dir}/hmdb.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/kegg.txt ${unichem_dir}/drugcentral.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/kegg.txt ${unichem_dir}/hmdb.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}
join ${unichem_dir}/drugcentral.txt ${unichem_dir}/hmdb.txt | sed 's/ /\t/g' | cut -f2-3 >> ${output_tsv_file}

date
echo "================= finished extract-unichem.sh ================="
