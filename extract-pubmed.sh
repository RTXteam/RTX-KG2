#!/usr/bin/env bash
# extract-pubmed.sh: Download the PubMed's XML Dump
# Copyright 2020 Stephen A. Ramsey
# Author Erica Wood

set -o nounset -o pipefail -o errexit

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

# Usage: extract-pubmed.sh

echo "================= starting extract-pubmed.sh =================="
date

config_dir=`dirname "$0"`
source ${config_dir}/master-config.shinc

pubmed_dir="${BUILD_DIR}/pubmed"
pubmed_link="ftp://ftp.ncbi.nlm.nih.gov/pubmed/baseline/"
pubmed_recent_link="ftp://ftp.ncbi.nlm.nih.gov/pubmed/updatefiles/"

mkdir -p ${pubmed_dir}
for file in $(curl -l ${pubmed_link})
do
	if [[ ${file} == *.gz ]]
	then
		echo ${file}
		curl -s -L ${pubmed_link}${file} > ${pubmed_dir}/${file}
	fi
done

for file in $(curl -l ${pubmed_recent_link})
do
	if [[ ${file} == *.gz ]]
	then
		echo ${file}
		curl -s -L ${pubmed_recent_link}${file} > ${pubmed_dir}/${file}
	fi
done

date
echo "================= finishing extract-pubmed.sh =================="