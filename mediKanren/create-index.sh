#!/usr/bin/env bash
# create-index.sh: Generate the indexes for mediKanren


cd mediKanren/biolink
racket csv-graph-to-db.rkt data rtx_kg2
racket build-string-index.rkt data rtx_kg2


