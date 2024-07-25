import json
import argparse

COMMENT = "!--"
XML_TAG = "?xml"
RDF_TAG = "rdf:RDF"

OUTMOST_TAGS_SKIP = [XML_TAG, RDF_TAG]

LINE_TYPE_IGNORE = "ignore"
LINE_TYPE_START_NEST = "start nest"
LINE_TYPE_START_NEST_WITH_ATTR = "start nest with attributes"
LINE_TYPE_ENTRY = "entry"
LINE_TYPE_ENTRY_WITH_ATTR = "entry with attributes"
LINE_TYPE_ENTRY_ONLY_ATTR = "entry with only attributes"
LINE_TYPE_END_NEST = "end nest"

KEY_TAG = "tag"
KEY_ATTRIBUTES = "attributes"
KEY_TEXT = "text"
KEY_TYPE = "type"

IGNORED_ATTRIBUTES = ["xml:lang"]

def get_args():
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('--test', dest='test',
							action="store_true", default=False)
	arg_parser.add_argument('inputFile', type=str)
	return arg_parser.parse_args()

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

	for letter_index in range(len(line)):
		letter = line[letter_index]
		next_letter = ""
		prev_letter = ""
		if letter_index + 1 < len(line):
			next_letter = line[letter_index + 1]
		if letter_index - 1 >= 0:
			prev_letter = line[letter_index - 1]

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
		elif letter == '>' and start_reading_tag:
			start_reading_tag = False
			start_reading_main = True
			continue
		elif start_reading_tag:
			tag += letter

		if letter == '>' and start_reading_attributes:
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

		if letter == '>' and start_reading_end_tag:
			continue
		elif start_reading_end_tag:
			end_tag += letter

	# Categorize the type of line
	line_type = str()
	out = dict()
	if tag == COMMENT or tag in OUTMOST_TAGS_SKIP:
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


def convert_nest(nest, index, working_dict):
	if index >= len(nest):
		return working_dict

	element = nest[index]
	line_type = element[KEY_TYPE]
	line_tag = element[KEY_TAG]
	line_text = element.get(KEY_TEXT, None)
	line_attributes = element.get(KEY_ATTRIBUTES, None)

	if line_type in [LINE_TYPE_START_NEST, LINE_TYPE_START_NEST_WITH_ATTR]:
		working_dict[line_tag] = dict()

		converted_nest = convert_nest(nest, index + 1, dict())
		working_dict[line_tag] = converted_nest

		if line_type == LINE_TYPE_START_NEST_WITH_ATTR:
			working_dict[line_tag][KEY_ATTRIBUTES] = line_attributes

	if line_type in [LINE_TYPE_ENTRY, LINE_TYPE_ENTRY_WITH_ATTR, LINE_TYPE_ENTRY_ONLY_ATTR]:
		if line_tag not in working_dict:
			working_dict[line_tag] = list()

		curr_dict = dict()

		if line_text is not None:
			curr_dict[KEY_TEXT] = line_text

		if line_attributes is not None:
			for attribute in line_attributes:
				curr_dict[attribute] = line_attributes[attribute]

		working_dict[line_tag].append(curr_dict)

		convert_nest(nest, index + 1, working_dict)

	return working_dict



def divide_into_lines(input_file_name):
	curr_str = ""
	curr_nest = list()
	curr_nest_tag = str()

	with open(input_file_name) as input_file:
		for line in input_file:
			line_str = line.strip()

			for letter_index in range(len(line_str)):
				letter = line_str[letter_index]
				next_letter = ""
				if letter_index + 1 < len(line_str):
					next_letter = line_str[letter_index + 1]

				curr_str += letter

				if letter == '>' and (next_letter == '<' or next_letter == ""):
					# Only return if nesting
					# print(curr_str)
					line_parsed = convert_line(curr_str)

					tag = line_parsed.get(KEY_TAG, None)
					line_type = line_parsed.get(KEY_TYPE, None)
					attribute_keys = line_parsed.get(KEY_ATTRIBUTES, dict()).keys()

					if curr_nest_tag == str():
						if line_type in [LINE_TYPE_START_NEST, LINE_TYPE_START_NEST_WITH_ATTR]:
							curr_nest_tag = tag
							curr_nest.append(line_parsed)
						elif line_type != LINE_TYPE_IGNORE:
							print("THIS VERSION")
							print(json.dumps(line_parsed, indent=4)) # replacement for processing right now
					else:
						if line_type == LINE_TYPE_END_NEST and curr_nest_tag == tag:
							print(json.dumps(curr_nest, indent=4)) # replacement for processing right now
							nest_dict = convert_nest(curr_nest, 0, dict())
							print(json.dumps(nest_dict, indent=4))
							curr_nest = list()
							curr_nest_tag = str()
						else:
							curr_nest.append(line_parsed)

					curr_str = ""

			if curr_str != "":
				# divide lines by a space
				curr_str += ' '


if __name__ == '__main__':
	args = get_args()
	input_file_name = args.inputFile

	divide_into_lines(input_file_name)