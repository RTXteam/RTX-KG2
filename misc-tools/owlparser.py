import json
import argparse

COMMENT = "!--"

LINE_TYPE_COMMENT = "comment"
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
	if tag == COMMENT:
		line_type = "comment"
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


def divide_into_lines(input_file_name):
	curr_str = ""
	keys = set()

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
					attribute_keys = line_parsed.get(KEY_ATTRIBUTES, dict()).keys()

					if tag is not None:
						keys.add(tag)
					for attribute_key in attribute_keys:
						keys.add(attribute_key)
					# print(json.dumps(convert_line(curr_str), indent=4))
					curr_str = ""

			if curr_str != "":
				# divide lines by a space
				curr_str += ' '

	print(json.dumps(list(keys), indent=4))


if __name__ == '__main__':
	args = get_args()
	input_file_name = args.inputFile

	divide_into_lines(input_file_name)