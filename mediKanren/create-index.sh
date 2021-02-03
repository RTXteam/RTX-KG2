#!/usr/bin/env bash
# create-index.sh: Generate the indexes for mediKanren

set -o nounset -o pipefail -o errexit


cd mediKanren/biolink
racket csv-graph-to-db.rkt data rtx_kg2
echo "======finished csv-graph-to-db.racket======"
racket build-string-index.rkt data rtx_kg2
echo "======script finished====="


