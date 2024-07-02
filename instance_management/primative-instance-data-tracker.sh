#!/bin/bash
# Get the memory usage every minute
# Copyright 2023 Stephen A. Ramsey <stephen.ramsey@oregonstate.edu>
# Author Erica Wood

start_time=`date +"%Y-%m-%d-%H-%M-%S"`
{
echo "================= starting primative-instance-data-tracker.sh ================="

while [[ true ]]; do
	current_time=`date +"%Y-%m-%d-%H-%M-%S"`

	memory_data=`landscape-sysinfo | grep "Memory usage" | sed "s/Memory usage://" | sed "s/IPv4 address for ens5: .*//" | sed "s/^[ ]*//" | sed "s/[ ]*$//"`
	disk_space_data=`landscape-sysinfo | grep "Usage of /" | sed "s/Usage of \/://" | sed "s/Users logged in: .*//" | sed "s/^[ ]*//"| sed "s/[ ]*$//"`
	echo "Time: ${current_time}; Memory: ${memory_data}; Disk: ${disk_space_data}"

	sleep 60
done


date
echo "================= finished primative-instance-data-tracker.sh ================="
} > instance-data-${start_time}.log