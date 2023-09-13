__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import json

if __name__ == '__main__':
	combos = dict()
	with open('tui_combo_mappings.tsv') as combo_file:
		line_count = 0
		for line in combo_file:
			line_count += 1
			if line_count == 1:
				continue
			line = line.split('\t')
			mapping = line[2]
			tuis = list()
			item_count = 0
			for item in line:
				if item_count > 2 and item_count % 2 == 1 and len(item) > 0:
					tuis.append(item)
				item_count += 1
			tuis = str(tuple(tuis))
			if len(mapping) > 0:
				combos[tuis] = mapping
		print(json.dumps(combos, indent=4, sort_keys=True))