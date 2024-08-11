import json
import argparse
import datetime

COMMENT = "!--"
XML_TAG = "?xml"
RDF_TAG = "rdf:RDF"
DOCTYPE_TAG = "!DOCTYPE"
CLASS_TAG = "owl:Class"
RESTRICTION_TAG = "owl:Restriction"
SUBCLASS_TAG = "rdfs:subClassOf"
NODEID_TAG = "rdf:nodeID"
RDF_ABOUT_TAG = "rdf:about"
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

class LineElementRead():
	TAG = 1
	ATTRIBUTE_TAG = 2
	ATTRIBUTE_TEXT = 3
	MAIN = 4
	END_TAG = 5


def categorize_line(tag, attributes, main_text, end_tag, only_tag):
	# Categorize the type of line
	line_type = str()
	out = dict()

	# Putting "only_tag" here isn't necessarily the best idea, but I don't know what else to do with it
	if tag == COMMENT or tag in OUTMOST_TAGS_SKIP or end_tag in OUTMOST_TAGS_SKIP or only_tag:
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

def get_letters(line, letter_index, start_brackets):
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

	return letter, next_letter, prev_letter, start_brackets


def identify_tag_type(letter_index, letter, next_letter, prev_letter, type_to_read):
	changed = True

	if letter == '<' and letter_index == 0:
		if next_letter != '/':
			type_to_read = LineElementRead.TAG
	elif letter == '/' and prev_letter == '<':
		type_to_read = LineElementRead.END_TAG
	else:
		changed = False

	return changed, type_to_read


def read_tag(letter, prev_letter, type_to_read, start_brackets, tag, line):
	only_tag = False
	changed = True

	if letter == ' ' and type_to_read == LineElementRead.TAG:
		type_to_read = LineElementRead.ATTRIBUTE_TAG
	elif letter == '>' and type_to_read == LineElementRead.TAG and start_brackets == 0:
		type_to_read = LineElementRead.MAIN

		if prev_letter == '/':
			print("Warning - strange tag, ignoring", line)
			only_tag = True
	elif type_to_read == LineElementRead.TAG:
		tag += letter
	else:
		changed = False

	return changed, type_to_read, (only_tag, tag)


def store_attribute(attributes, attribute_tag, attribute_text):
	if attribute_tag not in IGNORED_ATTRIBUTES:
		attributes[attribute_tag] = attribute_text.strip('/').strip('"')
	attribute_tag = ""
	attribute_text = ""

	return attributes, attribute_tag, attribute_text


def read_attributes(letter, prev_letter, type_to_read, start_brackets, attributes, attribute_tag, attribute_text, tag, end_tag):
	changed = True
	start_reading_attributes = (type_to_read == LineElementRead.ATTRIBUTE_TAG or type_to_read == LineElementRead.ATTRIBUTE_TEXT)

	if letter == '>' and start_reading_attributes and start_brackets == 0:
		type_to_read = LineElementRead.MAIN
		attributes, attribute_tag, attribute_text = store_attribute(attributes, attribute_tag, attribute_text)

		if prev_letter == '/':
			end_tag = tag
	elif start_reading_attributes:
		if letter == '=' and type_to_read == LineElementRead.ATTRIBUTE_TAG:
			type_to_read = LineElementRead.ATTRIBUTE_TEXT
		elif type_to_read == LineElementRead.ATTRIBUTE_TAG:
			attribute_tag += letter
		elif letter == ' ' and type_to_read == LineElementRead.ATTRIBUTE_TEXT:
			type_to_read = LineElementRead.ATTRIBUTE_TAG
			attributes, attribute_tag, attribute_text = store_attribute(attributes, attribute_tag, attribute_text)
		elif type_to_read == LineElementRead.ATTRIBUTE_TEXT:
			attribute_text += letter
	else:
		changed = False

	return changed, type_to_read, (attributes, attribute_tag, attribute_text, end_tag)


def read_main(letter, type_to_read, main_text):
	changed = True
	if letter == '<' and type_to_read == LineElementRead.MAIN:
		type_to_read = LineElementRead.END_TAG
	elif type_to_read == LineElementRead.MAIN:
		main_text += letter
	else:
		changed = False

	return changed, type_to_read, (main_text)


def read_end_tag(letter, type_to_read, start_brackets, end_tag):
	changed = True
	if letter == '>' and type_to_read == LineElementRead.END_TAG and start_brackets == 0:
		pass
	elif type_to_read == LineElementRead.END_TAG:
		end_tag += letter
	else:
		changed = False

	return changed, type_to_read, (end_tag)


def convert_line(line):
	tag = ""
	attributes = dict()
	attribute_tag = ""
	attribute_text = ""
	main_text = ""
	end_tag = ""

	type_to_read = 0

	only_tag = False

	start_brackets = 0

	for letter_index in range(len(line)):
		letter, next_letter, prev_letter, start_brackets = get_letters(line, letter_index, start_brackets)

		# First <
		tag_identified, type_to_read = identify_tag_type(letter_index, letter, next_letter, prev_letter, type_to_read)
		if tag_identified:
			continue

		tag_read, type_to_read, tag_read_data = read_tag(letter, prev_letter, type_to_read, start_brackets, tag, line)
		if tag_read:
			(only_tag, tag) = tag_read_data
			continue

		attributes_read, type_to_read, attributes_read_data = read_attributes(letter, prev_letter, type_to_read, start_brackets, attributes, attribute_tag, attribute_text, tag, end_tag)
		if attributes_read:
			(attributes, attribute_tag, attribute_text, end_tag) = attributes_read_data
			continue

		main_read, type_to_read, main_read_data = read_main(letter, type_to_read, main_text)
		if main_read:
			(main_text) = main_read_data
			continue

		end_tag_read, type_to_read, end_tag_read_data = read_end_tag(letter, type_to_read, start_brackets, end_tag)
		if end_tag_read:
			(end_tag) = end_tag_read_data
			continue

	return categorize_line(tag, attributes, main_text, end_tag, only_tag)


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


def check_for_class_genids(nest_dict):
	genids = list()

	nest_dict_classes = nest_dict.get(CLASS_TAG, list())
	for nest_class_index in range(len(nest_dict_classes)):
		nest_class = nest_dict_classes[nest_class_index]
		nest_subclasses = nest_class.get(SUBCLASS_TAG, list())
		for nest_subclass_index in range(len(nest_subclasses)):
			nest_subclass = nest_subclasses[nest_subclass_index]
			potential_genid = nest_subclass.get(NODEID_TAG, str())
			if potential_genid.startswith(GENID_PREFIX):
				genids.append(potential_genid)

	return genids


def check_for_restriction_genids(nest_dict):
	for nest_restriction in nest_dict.get(RESTRICTION_TAG, dict()):
		potential_genid = nest_restriction.get(NODEID_TAG, str())
		if potential_genid.startswith(GENID_PREFIX):
				return potential_genid
	return None

def extract_class_id(nest_dict):
	nest_dict_classes = nest_dict.get(CLASS_TAG, list())
	# Can't have competing class_ids
	assert len(nest_dict_classes) <= 1

	for nest_class_index in range(len(nest_dict_classes)):
		nest_class = nest_dict_classes[nest_class_index]
		return nest_class.get(RDF_ABOUT_TAG, str())

def store_genid_nest_in_class_nest(genid, genid_nest, class_nest):
	output_class_nest = class_nest
	
	nest_dict_classes = class_nest.get(CLASS_TAG, list())
	for nest_class_index in range(len(nest_dict_classes)):
		nest_class = nest_dict_classes[nest_class_index]
		nest_subclasses = nest_class.get(SUBCLASS_TAG, list())
		for nest_subclass_index in range(len(nest_subclasses)):
			nest_subclass = nest_subclasses[nest_subclass_index]
			potential_genid = nest_subclass.get(NODEID_TAG, str())
			if potential_genid == genid:
				output_class_nest[CLASS_TAG][nest_class_index][SUBCLASS_TAG][nest_subclass_index][RESTRICTION_TAG] = genid_nest[RESTRICTION_TAG]

	return output_class_nest


def triage_nest_dict(nest_dict):
	genids = check_for_class_genids(nest_dict)
	restriction_genid = check_for_restriction_genids(nest_dict)
	class_id = extract_class_id(nest_dict)

	if len(genids) > 0:
		for genid in genids:
			GENID_TO_ID[genid] = class_id
		ID_TO_GENIDS[class_id] = genids
		GENID_REMAINING_NESTS[class_id] = nest_dict
	elif restriction_genid is not None:
		class_id = GENID_TO_ID.get(restriction_genid, str())
		if len(class_id) == 0:
			print("WARNING WITH:", restriction_genid, "- NO CLASS_ID FOUND")
			OUTPUT_NESTS.append(nest_dict)
			return
		class_nest = GENID_REMAINING_NESTS[class_id]
		ID_TO_GENIDS[class_id].remove(restriction_genid)
		updated_class_nest = store_genid_nest_in_class_nest(restriction_genid, nest_dict, class_nest)

		if len(ID_TO_GENIDS[class_id]) > 0:
			GENID_REMAINING_NESTS[class_id] = updated_class_nest
		else:
			OUTPUT_NESTS.append(updated_class_nest)
			GENID_REMAINING_NESTS[class_id] = None
	else:
		OUTPUT_NESTS.append(nest_dict)


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
						assert popped_curr_nest_tag == tag, curr_nest
						if len(curr_nest_tags) == 0:
							output_nest = True
					if output_nest: 
						nest_dict, _ = convert_nest(curr_nest, 0)
						# genids = check_for_class_genids(nest_dict)
						triage_nest_dict(nest_dict)
						# restriction_genid = check_for_restriction_genids(nest_dict)

						# if len(genids) > 0:
						# 	nest_dict['genids'] = genids
						# print(json.dumps(nest_dict, indent=4))
						curr_nest = list()
						curr_nest_tag = str()

					curr_str = ""

			if curr_str != "":
				# divide lines by a space
				curr_str += ' '

	print(json.dumps(OUTPUT_NESTS, indent=4))

	print("=========")

	print("Remaining:")
	for item in GENID_REMAINING_NESTS:
		if GENID_REMAINING_NESTS[item] != None:
			print(item)
			print(json.dumps(GENID_REMAINING_NESTS[item], indent=4))

if __name__ == '__main__':
	args = get_args()
	input_file_name = args.inputFile

	print("File:", input_file_name)
	print("Start Time:", date())
	divide_into_lines(input_file_name)
	print("End Time:", date())