#!/usr/bin/env bash
# kgx-validation-and-metagraph.sh: validates the KGX TSV files and generates the JSON metagraph file

# Note: the KGX TSV files `nodes.tsv` and `edges.tsv` should be in the current working directory
# when this scrip is run.

# Copyright 2021 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

## setup for running this script:
##  python3.7 -m venv venv
##  venv/bin/pip3.7 install kgx
##  source venv/bin/activate

## validate the TSV files produced by kg2_tsv_to_kgx_tsv.py
kgx validate \
    --input-format tsv \
    nodes.tsv edges.tsv

## make a "content_metadata.json" file for upload to KGE
kgx graph-summary \
    --report-type meta-knowledge-graph \
    --stream \
    --input-format tsv \
    --output content_metadata.json \
    nodes.tsv edges.tsv
