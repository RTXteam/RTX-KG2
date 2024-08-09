import json
import argparse
import datetime

COMMENT = "!--"
XML_TAG = "?xml"
RDF_TAG = "rdf:RDF"
DOCTYPE_TAG = "!DOCTYPE"
CLASS_TAG = "owl:Class"
SUBCLASS_TAG = "rdfs:subClassOf"
NODEID_TAG = "rdf:nodeID"
GENID_PREFIX = "genid"

OUTMOST_TAGS_SKIP = [XML_TAG, RDF_TAG, DOCTYPE_TAG]

LINE_TYPE_IGNORE = "ignore"
LINE_TYPE_START_NEST = "start nest"
LINE_TYPE_START_NEST_WITH_ATTR = "start nest with attributes"
LINE_TYPE_ENTRY = "entry"
LINE_TYPE_ENTRY_WITH_ATTR = "entry with attributes"
LINE_TYPE_ENTRY_ONLY_ATTR = "entry with only attributes"
LINE_TYPE_END_NEST = "end nest"

KEY_TAG = "tag"
KEY_ATTRIBUTES = "attributes"
KEY_TEXT = "ENTRY_TEXT"
KEY_TYPE = "type"

IGNORED_ATTRIBUTES = ["xml:lang"]

OUTPUT_NESTS = []
GENID_REMAINING_NESTS = dict()
GENID_TO_ID = dict()
ID_TO_GENIDS = dict()

def get_args():
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('--test', dest='test',
							action="store_true", default=False)
	arg_parser.add_argument('inputFile', type=str)
	return arg_parser.parse_args()

def date():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def convert_line(line):
	tag = ""
	attributes = dict()
	attribute_tag = ""
	attribute_text = ""
	main_text = ""
	end_tag = ""

	start_reading_tag = False
	start_reading_attributes = False
	start_reading_attribute_tag = False
	start_reading_attribute_text = False
	start_reading_main = False
	start_reading_end_tag = False

	start_brackets = 0

	for letter_index in range(len(line)):
		letter = line[letter_index]
		next_letter = ""
		prev_letter = ""
		if letter_index + 1 < len(line):
			next_letter = line[letter_index + 1]
		if letter_index - 1 >= 0:
			prev_letter = line[letter_index - 1]

		if letter == '<':
			start_brackets += 1
		if letter == '>':
			start_brackets -= 1

		# First <
		if letter == '<' and letter_index == 0:
			if next_letter != '/':
				start_reading_tag = True
			continue
		if letter == '/' and prev_letter == '<':
			start_reading_end_tag = True
			continue

		if letter == ' ' and start_reading_tag:
			start_reading_tag = False
			start_reading_attributes = True
			start_reading_attribute_tag = True
			continue
		elif letter == '>' and start_reading_tag and start_brackets == 0:
			start_reading_tag = False
			start_reading_main = True
			continue
		elif start_reading_tag:
			tag += letter

		if letter == '>' and start_reading_attributes and start_brackets == 0:
			start_reading_attributes = False
			start_reading_attribute_tag = False
			start_reading_attribute_text = False
			start_reading_main = True
			if attribute_tag not in IGNORED_ATTRIBUTES:
				attributes[attribute_tag] = attribute_text.strip('/').strip('"')
			attribute_tag = ""
			attribute_text = ""

			if prev_letter == '/':
				end_tag = tag
			continue
		elif start_reading_attributes:
			if letter == '=' and start_reading_attribute_tag:
				start_reading_attribute_text = True
				start_reading_attribute_tag = False
				continue
			elif start_reading_attribute_tag:
				attribute_tag += letter

			if letter == ' ' and start_reading_attribute_text:
				start_reading_attribute_tag = True
				start_reading_attribute_text = False
				if attribute_tag not in IGNORED_ATTRIBUTES:
					attributes[attribute_tag] = attribute_text.strip('/').strip('"')
				attribute_tag = ""
				attribute_text = ""
				continue
			elif start_reading_attribute_text:
				attribute_text += letter

		if letter == '<' and start_reading_main:
			start_reading_main = False
			start_reading_end_tag = True
			continue
		elif start_reading_main:
			main_text += letter

		if letter == '>' and start_reading_end_tag and start_brackets == 0:
			continue
		elif start_reading_end_tag:
			end_tag += letter

	# Categorize the type of line
	line_type = str()
	out = dict()

	if tag == COMMENT or tag in OUTMOST_TAGS_SKIP or end_tag in OUTMOST_TAGS_SKIP:
		line_type = LINE_TYPE_IGNORE
	else:
		start_tag_exists = (tag != str())
		attributes_exist = (attributes != dict())
		text_exists = (main_text != str())
		end_tag_exists = (end_tag != str())

		if start_tag_exists:
			if attributes_exist:
				if text_exists:
					line_type = LINE_TYPE_ENTRY_WITH_ATTR
					out[KEY_TAG] = tag
					out[KEY_ATTRIBUTES] = attributes
					out[KEY_TEXT] = main_text
				elif end_tag_exists:
					line_type = LINE_TYPE_ENTRY_ONLY_ATTR
					out[KEY_TAG] = tag
					out[KEY_ATTRIBUTES] = attributes
				else:
					line_type = LINE_TYPE_START_NEST_WITH_ATTR
					out[KEY_TAG] = tag
					out[KEY_ATTRIBUTES] = attributes
			elif text_exists:
				line_type = LINE_TYPE_ENTRY
				out[KEY_TAG] = tag
				out[KEY_TEXT] = main_text
			else:
				line_type = LINE_TYPE_START_NEST
				out[KEY_TAG] = tag
		elif end_tag_exists:
			line_type = LINE_TYPE_END_NEST
			out[KEY_TAG] = end_tag

	out[KEY_TYPE] = line_type

	return out


def convert_nest(nest, start_index):
	nest_dict = dict()
	curr_index = start_index

	while curr_index < len(nest):
		element = nest[curr_index]
		line_type = element[KEY_TYPE]
		line_tag = element[KEY_TAG]
		line_text = element.get(KEY_TEXT, None)
		line_attributes = element.get(KEY_ATTRIBUTES, None)

		if line_type in [LINE_TYPE_START_NEST, LINE_TYPE_START_NEST_WITH_ATTR]:
			if line_tag not in nest_dict:
				nest_dict[line_tag] = list()

			converted_nest, ret_index = convert_nest(nest, curr_index + 1)

			if line_attributes is not None:
				for attribute in line_attributes:
					converted_nest[attribute] = line_attributes[attribute]

			nest_dict[line_tag].append(converted_nest)

			curr_index = ret_index + 1
			continue

		if line_type in [LINE_TYPE_ENTRY, LINE_TYPE_ENTRY_WITH_ATTR, LINE_TYPE_ENTRY_ONLY_ATTR]:
			if line_tag not in nest_dict:
				nest_dict[line_tag] = list()

			curr_dict = dict()

			if line_text is not None:
				curr_dict[KEY_TEXT] = line_text

			if line_attributes is not None:
				for attribute in line_attributes:
					curr_dict[attribute] = line_attributes[attribute]

			nest_dict[line_tag].append(curr_dict)

			curr_index += 1
			continue

		if line_type in [LINE_TYPE_END_NEST]:
			return nest_dict, curr_index

	return nest_dict, curr_index


def check_for_genids(nest_dict):
	CLASS_TAG = "owl:Class"
	SUBCLASS_TAG = "rdfs:subClassOf"
	NODEID_TAG = "rdf:nodeID"
	GENID_PREFIX = "genid"

	genids = list()

	for nest_class in nest_dict.get(CLASS_TAG, dict()):
		for nest_subclass in nest_class.get(SUBCLASS_TAG, dict()):
			potential_genid = nest_subclass.get(NODEID_TAG, str())
			if potential_genid.startswith(GENID_PREFIX):
				genids.append(potential_genid)

	return genids

def divide_into_lines(input_file_name):
	curr_str = ""
	curr_nest = list()
	curr_nest_tags = list() # Treating it as a stack
	start_brackets = 0

	with open(input_file_name) as input_file:
		for line in input_file:
			line_str = line.strip()

			for letter_index in range(len(line_str)):
				letter = line_str[letter_index]
				if letter == '<':
					start_brackets += 1
				if letter == '>':
					start_brackets -= 1

				next_letter = ""
				if letter_index + 1 < len(line_str):
					next_letter = line_str[letter_index + 1]

				curr_str += letter

				if letter == '>' and (next_letter == '<' or next_letter == "") and start_brackets == 0:
					# Only return if nesting
					line_parsed = convert_line(curr_str)

					tag = line_parsed.get(KEY_TAG, None)
					assert tag != KEY_TEXT # This could cause a massive conflict, but it is unlikely
					line_type = line_parsed.get(KEY_TYPE, None)
					attribute_keys = line_parsed.get(KEY_ATTRIBUTES, dict()).keys()

					if line_type != LINE_TYPE_IGNORE:
						curr_nest.append(line_parsed)

					output_nest = (line_type in [LINE_TYPE_ENTRY, LINE_TYPE_ENTRY_WITH_ATTR, LINE_TYPE_ENTRY_ONLY_ATTR] and len(curr_nest_tags) == 0)

					if line_type in [LINE_TYPE_START_NEST, LINE_TYPE_START_NEST_WITH_ATTR]:
						curr_nest_tags.append(tag)
					elif line_type == LINE_TYPE_END_NEST:
						popped_curr_nest_tag = curr_nest_tags.pop()
						assert popped_curr_nest_tag == tag
						if len(curr_nest_tags) == 0:
							output_nest = True
					if output_nest: 
						nest_dict, _ = convert_nest(curr_nest, 0)
						genids = check_for_genids(nest_dict)
						if len(genids) > 0:
							nest_dict['genids'] = genids
						print(json.dumps(nest_dict, indent=4))
						curr_nest = list()
						curr_nest_tag = str()

					curr_str = ""

			if curr_str != "":
				# divide lines by a space
				curr_str += ' '

if __name__ == '__main__':
	args = get_args()
	input_file_name = args.inputFile

	print("File:", input_file_name)
	print("Start Time:", date())
	divide_into_lines(input_file_name)
	print("End Time:", date())