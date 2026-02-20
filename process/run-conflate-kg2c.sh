#!/usr/bin/env bash
set -euo pipefail

PATCH_VERSION=${1:?Usage: $0 <patch-version>}

BASE_VERSION="2.10"
FULL_VERSION="${BASE_VERSION}.${PATCH_VERSION}"

DB_DIR="/data"
KG2_BUILD_DIR="/home/ubuntu/kg2-build"

venv/bin/python conflate_kg2c.py \
    "${DB_DIR}/babel-20250901-p1.sqlite" \
    "${KG2_BUILD_DIR}/kg2-normalized-${FULL_VERSION}-edges.jsonl" \
    "${KG2_BUILD_DIR}/kg2.${FULL_VERSION}-conflated-edges.jsonl" \
    "${KG2_BUILD_DIR}/kg2-normalized-${FULL_VERSION}-nodes.jsonl" \
    "${KG2_BUILD_DIR}/kg2.${FULL_VERSION}-conflated-nodes.jsonl"