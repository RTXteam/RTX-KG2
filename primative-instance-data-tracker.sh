#!/bin/bash
# Get the memory usage every minute
# Copyright 2023 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>
# Author Erica Wood

start_time=`date +"%Y-%m-%d"`
{
echo "================= starting primative-instance-data-tracker.sh ================="
date

while [[ true ]]; do
	date

	memory_data=`landscape-sysinfo | grep "Memory usage" | sed "s/Memory usage://" | sed "s/IPv4 address for ens5: .*//" | sed "s/ //"`

	echo ${memory_data}

	sleep 60
done


date
echo "================= finished primative-instance-data-tracker.sh ================="
} > instance-data-${start_time}.log