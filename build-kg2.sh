#!/bin/bash
export PATH=$PATH:/home/ubuntu/kg2-build
cd ~/kg2-build && ~/kg2-venv/bin/python3 -u ~/kg2-code/build-kg2.py 2>stderr.log 1>stdout.log
