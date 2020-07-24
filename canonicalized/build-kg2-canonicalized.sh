#!/usr/bin/env bash

slim_kg2_file_name=kg2-slim.json.gz
canonicalized_kg2_file_name=kg2-canonicalized.json

# Grab the latest "slim" KG2 from S3
aws s3 cp --no-progress --region us-west-2 s3://rtx-kg2/${slim_kg2_file_name} ${slim_kg2_file_name}

# Create the canonicalized KG from the slim KG (represented as json)
python3 -u create_canonicalized_kg_json.py ${slim_kg2_file_name} ${canonicalized_kg2_file_name}

# Convert the json file into TSV files and upload to S3 TODO
#tsv_dir = canonicalized_tsvs
#rm -r -f ${tsv_dir}
#mkdir -p ${tsv_dir}
#python3 -u kg_canonicalized_json_to_tsv.py ${canonicalized_kg2_file_name} ${tsv_dir}
#tar -czvf kg2-canonicalized-tsv.tar.gz nodes_c.tsv nodes_c_header.tsv edges_c.tsv edges_c_header.tsv
#aws s3 cp --no-progress --region us-west-2 kg2-canonicalized-tsv.tar.gz s3://rtx-kg2/
