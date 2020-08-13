#!/usr/bin/env python

import ontobio
import pprint
import re
import yaml

BIDIR_EDGE_LABELS = {'related_to', 'overlaps'}
RO_RE = re.compile(r'RO:\d+')
ont = ontobio.ontol_factory.OntologyFactory().create("ro.owl")
top_data = yaml.safe_load(open('predicate-remap.yaml', 'r'))
for pred_curie_id, pred_inst_data in sorted(top_data.items()):
    if RO_RE.match(pred_curie_id):
        pred_inst, pred_inst_info = next(iter(pred_inst_data.items()))
        if pred_inst_info is not None:
            assert type(pred_inst_info) == list
            edge_label, mapped_curie_id = pred_inst_info
            if edge_label not in BIDIR_EDGE_LABELS:
                pprint.pprint(pred_curie_id + ":")
                print(ont.node(pred_curie_id)['lbl'])
                pprint.pprint(pred_inst_data)
                print("")
