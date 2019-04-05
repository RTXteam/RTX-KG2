#!/bin/bash
## estimate amount of system ram, in GB
MEM_BYTES=`cat /proc/meminfo | grep MemTotal | cut -f2 -d\: | cut -f1 -dk | sed 's/ //g'`
DIVISOR=1048576
MEM_GB=$((MEM_BYTES/DIVISOR))
echo ${MEM_GB}
