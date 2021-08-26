#!/usr/bin/env bash
# get-system-memory-gb.sh:  prints the amount of system RAM, in gigibytes (Ubuntu only)
# Copyright 2019 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>

set -o nounset -o pipefail -o errexit

if [[ $# != 0 || "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo Usage: "$0"
    exit 2
fi

## estimate the amount of system ram, in GB (Linux-only script)
if [[ $OSTYPE == 'linux-gnu' ]];
then
    mem_bytes=`cat /proc/meminfo | grep MemTotal | cut -f2 -d\: | cut -f1 -dk | sed 's/ //g'`
else
    if [[ $OSTYPE == 'darwin'* ]];
    then
        mem_bytes=`sysctl -a | grep hw.memsize | cut -f2 -d\ `
    else
        echo "unsupported OS type for get-system-memory-gb.sh"
        exit 1
    fi
fi
divisor=1048576
mem_gb=$((mem_bytes/divisor))
echo ${mem_gb}

