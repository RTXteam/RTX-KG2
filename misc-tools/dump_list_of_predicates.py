#!/usr/bin/env python

import pprint
import yaml

preds = set()
topdata = yaml.safe_load(open('predicate-remap.yaml', 'r'))
for toppred, topitem in topdata.items():
    cmd, subitem = next(iter(topitem.items()))
    if cmd == 'keep':
        preds.add(toppred)
    elif cmd == 'delete':
        continue
    elif cmd == 'invert':
        preds.add(subitem[1])
    elif cmd == 'rename':
        preds.add(subitem[1])
    else:
        assert False

pprint.pprint(preds)
                    
print(len(topdata))
