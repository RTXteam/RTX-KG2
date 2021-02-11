#!/usr/bin/env bash

set -o nounset -o pipefail -o errexit

python3 biolink_yaml_to_schema_documentation.py ../biolink-model.yaml ../biolink-kg-schema.md

