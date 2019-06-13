#!/usr/bin/env bash
# get-system-memory-gb.sh:  prints the amount of system RAM, in gigibytes (Ubuntu only)
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

## estimate the amount of system ram, in GB (Linux-only script)
MEM_BYTES=`cat /proc/meminfo | grep MemTotal | cut -f2 -d\: | cut -f1 -dk | sed 's/ //g'`
DIVISOR=1048576
MEM_GB=$((MEM_BYTES/DIVISOR))
echo ${MEM_GB}

