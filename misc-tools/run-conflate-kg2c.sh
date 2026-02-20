#!/usr/bin/env bash
set -eua pipefail
DB_DIR=/home/ubuntu/SET_TO_DATABASE_DIR
venv/bin/python conflate_kg2c.py \
    ${DB_DIR}/babel-20250901-p1.sqlite \
    ${DB_DIR}/kg2-normalized-2.10.3-edges.jsonl \
    ${DB_DIR}/kg2.10.3-conflated-edges.jsonl \
    ${DB_DIR}/kg2-normalized-2.10.3-nodes.jsonl \
    ${DB_DIR}/kg2.10.3-conflated-nodes.jsonl
