#!/usr/bin/env python3

import yaml

output_dict = dict()

with open('kg2-edge-labels-stats-annotated.txt', 'r') as file:
    first_line = True
    for line in file:
        if first_line:
            first_line = False
            continue
        fields = line.rstrip().split('\t')
        orig_curie = fields[0]
        command = fields[3]
        if len(fields) > 4:
            new_edge_label = fields[4]
            new_curie = fields[5]
        extra_list = None
        if command != 'keep' and command != 'delete':
            extra_list = [new_edge_label, new_curie]
        output_dict[orig_curie] = {command: extra_list}

with open('predicate-remap-new.yaml', 'w') as outfile:
    yaml.dump(output_dict, outfile)
