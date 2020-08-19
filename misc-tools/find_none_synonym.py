#!/usr/bin/env python3

import json
import argparse
import pprint

def make_arg_parser():
    arg_parser = argparse.ArgumentParser(description='merge_graphs.py: merge two or more JSON KG files')
    arg_parser.add_argument('inputFile', type=str)
    return arg_parser


graph = json.load(open(make_arg_parser().parse_args().inputFile, 'r'))
for node in graph['nodes']:
    if None in node['synonym']:
        pprint.pprint(node)
        assert False

