#!/bin/bash
export PATH=$PATH:/home/ubuntu/kg2-build
~/kg2-venv/bin/python3 -u ~/kg2-code/build-kg2.py 2>~/kg2-build/stderr.log 1>~/kg2-build/stdout.log
