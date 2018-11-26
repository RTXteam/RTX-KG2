#!/bin/bash
export PATH=$PATH:.
cd ~/kg2-build && ~/kg2-venv/bin/python3 -u ~/kg2-code/build-kg2.py 2>stderr.log 1>stdout.log
