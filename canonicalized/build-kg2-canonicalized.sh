#!/usr/bin/env bash

CONFIG_DIR=../`dirname "$0"`
source ${CONFIG_DIR}/master-config.shinc

SLIM_KG2_FILE_NAME = kg2-slim.json.gz
CANONICALIZED_KG2_FILE_NAME = kg2-canonicalized.json

# Grab the latest "slim" KG2 from S3
${S3_CP_CMD} s3://${S3_BUCKET}/{SLIM_KG2_FILE_NAME}

# Create the canonicalized KG from the slim KG (represented as JSON)
${VENV_DIR}/bin/python3 -u create_canonicalized_kg_json.py ${SLIM_KG2_FILE_NAME} ${CANONICALIZED_KG2_FILE_NAME}

# Convert the json file into TSV files TODO
#TSV_DIR = canonicalized_tsvs
#rm -r -f ${TSV_DIR}
#mkdir -p ${TSV_DIR}
#${VENV_DIR}/bin/python3 -u kg_canonicalized_json_to_tsv.py \
#           kg2-canonicalized.json \
#           ${TSV_DIR}
#tar -czvf kg2-canonicalized-tsv.tar.gz nodes_c.tsv nodes_c_header.tsv edges_c.tsv edges_c_header.tsv
#${S3_CP_CMD} kg2-canonicalized-tsv.tar.gz s3://${S3_BUCKET}/
