import json
import argparse
import datetime
import kg2_util

def get_args():
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('--test', dest='test',
							action="store_true", default=False)
	arg_parser.add_argument('inputFile', type=str)
	arg_parser.add_argument('outputFile', type=str)
	return arg_parser.parse_args()

def date():
	return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class LineElementRead():
	TAG = 1
	ATTRIBUTE_TAG = 2
	ATTRIBUTE_TEXT = 3
	MAIN = 4
	END_TAG = 5

class XMLParser():
	def __init__(self, skip_tags, ignored_attributes, processing_func):
		self.COMMENT = "!--"
		self.OUTMOST_TAGS_SKIP = skip_tags
		self.IGNORED_ATTRIBUTES = ignored_attributes
		self.processing_func = processing_func

		self.LINE_TYPE_IGNORE = "ignore"
		self.LINE_TYPE_START_NEST = "start nest"
		self.LINE_TYPE_START_NEST_WITH_ATTR = "start nest with attributes"
		self.LINE_TYPE_ENTRY = "entry"
		self.LINE_TYPE_ENTRY_WITH_ATTR = "entry with attributes"
		self.LINE_TYPE_ENTRY_ONLY_ATTR = "entry with only attributes"
		self.LINE_TYPE_END_NEST = "end nest"

		self.KEY_TAG = "tag"
		self.KEY_ATTRIBUTES = "attributes"
		self.KEY_TEXT = "ENTRY_TEXT"
		self.KEY_TYPE = "type"


	def categorize_line(self, tag, attributes, main_text, end_tag, only_tag):
		# Categorize the type of line
		line_type = str()
		out = dict()

		# Putting "only_tag" here isn't necessarily the best idea, but I don't know what else to do with it
		if tag == self.COMMENT or tag in self.OUTMOST_TAGS_SKIP or end_tag in self.OUTMOST_TAGS_SKIP or only_tag:
			line_type = self.LINE_TYPE_IGNORE
		else:
			start_tag_exists = (tag != str())
			attributes_exist = (attributes != dict())
			text_exists = (main_text != str())
			end_tag_exists = (end_tag != str())

			if start_tag_exists:
				if attributes_exist:
					if text_exists:
						line_type = self.LINE_TYPE_ENTRY_WITH_ATTR
						out[self.KEY_TAG] = tag
						out[self.KEY_ATTRIBUTES] = attributes
						out[self.KEY_TEXT] = main_text
					elif end_tag_exists:
						line_type = self.LINE_TYPE_ENTRY_ONLY_ATTR
						out[self.KEY_TAG] = tag
						out[self.KEY_ATTRIBUTES] = attributes
					else:
						line_type = self.LINE_TYPE_START_NEST_WITH_ATTR
						out[self.KEY_TAG] = tag
						out[self.KEY_ATTRIBUTES] = attributes
				elif text_exists:
					line_type = self.LINE_TYPE_ENTRY
					out[self.KEY_TAG] = tag
					out[self.KEY_TEXT] = main_text
				else:
					line_type = self.LINE_TYPE_START_NEST
					out[self.KEY_TAG] = tag
			elif end_tag_exists:
				line_type = self.LINE_TYPE_END_NEST
				out[self.KEY_TAG] = end_tag

		out[self.KEY_TYPE] = line_type

		return out

	def get_letters(self, line, letter_index, start_brackets):
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


	def identify_tag_type(self, letter_index, letter, next_letter, prev_letter, type_to_read):
		changed = True

		if letter == '<' and letter_index == 0:
			if next_letter != '/':
				type_to_read = LineElementRead.TAG
		elif letter == '/' and prev_letter == '<':
			type_to_read = LineElementRead.END_TAG
		else:
			changed = False

		return changed, type_to_read


	def read_tag(self, letter, prev_letter, type_to_read, start_brackets, tag, line):
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


	def store_attribute(self, attributes, attribute_tag, attribute_text):
		if attribute_tag not in self.IGNORED_ATTRIBUTES:
			attributes[attribute_tag] = attribute_text.strip('/').strip('"')
		attribute_tag = ""
		attribute_text = ""

		return attributes, attribute_tag, attribute_text


	def read_attributes(self, letter, prev_letter, type_to_read, start_brackets, attributes, attribute_tag, attribute_text, tag, end_tag):
		changed = True
		start_reading_attributes = (type_to_read == LineElementRead.ATTRIBUTE_TAG or type_to_read == LineElementRead.ATTRIBUTE_TEXT)

		if letter == '>' and start_reading_attributes and start_brackets == 0:
			type_to_read = LineElementRead.MAIN
			attributes, attribute_tag, attribute_text = self.store_attribute(attributes, attribute_tag, attribute_text)

			if prev_letter == '/':
				end_tag = tag
		elif start_reading_attributes:
			if letter == '=' and type_to_read == LineElementRead.ATTRIBUTE_TAG:
				type_to_read = LineElementRead.ATTRIBUTE_TEXT
			elif type_to_read == LineElementRead.ATTRIBUTE_TAG:
				attribute_tag += letter
			elif letter == ' ' and type_to_read == LineElementRead.ATTRIBUTE_TEXT:
				type_to_read = LineElementRead.ATTRIBUTE_TAG
				attributes, attribute_tag, attribute_text = self.store_attribute(attributes, attribute_tag, attribute_text)
			elif type_to_read == LineElementRead.ATTRIBUTE_TEXT:
				attribute_text += letter
		else:
			changed = False

		return changed, type_to_read, (attributes, attribute_tag, attribute_text, end_tag)


	def read_main(self, letter, type_to_read, main_text):
		changed = True
		if letter == '<' and type_to_read == LineElementRead.MAIN:
			type_to_read = LineElementRead.END_TAG
		elif type_to_read == LineElementRead.MAIN:
			main_text += letter
		else:
			changed = False

		return changed, type_to_read, (main_text)


	def read_end_tag(self, letter, type_to_read, start_brackets, end_tag):
		changed = True
		if letter == '>' and type_to_read == LineElementRead.END_TAG and start_brackets == 0:
			pass
		elif type_to_read == LineElementRead.END_TAG:
			end_tag += letter
		else:
			changed = False

		return changed, type_to_read, (end_tag)


	def convert_line(self, line):
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
			letter, next_letter, prev_letter, start_brackets = self.get_letters(line, letter_index, start_brackets)

			# First <
			tag_identified, type_to_read = self.identify_tag_type(letter_index, letter, next_letter, prev_letter, type_to_read)
			if tag_identified:
				continue

			tag_read, type_to_read, tag_read_data = self.read_tag(letter, prev_letter, type_to_read, start_brackets, tag, line)
			if tag_read:
				(only_tag, tag) = tag_read_data
				continue

			attributes_read, type_to_read, attributes_read_data = self.read_attributes(letter, prev_letter, type_to_read, start_brackets, attributes, attribute_tag, attribute_text, tag, end_tag)
			if attributes_read:
				(attributes, attribute_tag, attribute_text, end_tag) = attributes_read_data
				continue

			main_read, type_to_read, main_read_data = self.read_main(letter, type_to_read, main_text)
			if main_read:
				(main_text) = main_read_data
				continue

			end_tag_read, type_to_read, end_tag_read_data = self.read_end_tag(letter, type_to_read, start_brackets, end_tag)
			if end_tag_read:
				(end_tag) = end_tag_read_data
				continue

		return self.categorize_line(tag, attributes, main_text, end_tag, only_tag)


	def convert_nest(self, nest, start_index):
		nest_dict = dict()
		curr_index = start_index

		while curr_index < len(nest):
			element = nest[curr_index]
			line_type = element[self.KEY_TYPE]
			line_tag = element[self.KEY_TAG]
			line_text = element.get(self.KEY_TEXT, None)
			line_attributes = element.get(self.KEY_ATTRIBUTES, None)

			if line_type in [self.LINE_TYPE_START_NEST, self.LINE_TYPE_START_NEST_WITH_ATTR]:
				if line_tag not in nest_dict:
					nest_dict[line_tag] = list()

				converted_nest, ret_index = self.convert_nest(nest, curr_index + 1)

				if line_attributes is not None:
					for attribute in line_attributes:
						converted_nest[attribute] = line_attributes[attribute]

				nest_dict[line_tag].append(converted_nest)

				curr_index = ret_index + 1
				continue

			if line_type in [self.LINE_TYPE_ENTRY, self.LINE_TYPE_ENTRY_WITH_ATTR, self.LINE_TYPE_ENTRY_ONLY_ATTR]:
				if line_tag not in nest_dict:
					nest_dict[line_tag] = list()

				curr_dict = dict()

				if line_text is not None:
					curr_dict[self.KEY_TEXT] = line_text

				if line_attributes is not None:
					for attribute in line_attributes:
						curr_dict[attribute] = line_attributes[attribute]

				nest_dict[line_tag].append(curr_dict)

				curr_index += 1
				continue

			if line_type in [self.LINE_TYPE_END_NEST]:
				return nest_dict, curr_index

		return nest_dict, curr_index


	def divide_into_lines(self, input_file_name):
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
						line_parsed = self.convert_line(curr_str)

						tag = line_parsed.get(self.KEY_TAG, None)
						assert tag != self.KEY_TEXT # This could cause a massive conflict, but it is unlikely
						line_type = line_parsed.get(self.KEY_TYPE, None)
						attribute_keys = line_parsed.get(self.KEY_ATTRIBUTES, dict()).keys()

						if line_type != self.LINE_TYPE_IGNORE:
							curr_nest.append(line_parsed)

						output_nest = (line_type in [self.LINE_TYPE_ENTRY, self.LINE_TYPE_ENTRY_WITH_ATTR, self.LINE_TYPE_ENTRY_ONLY_ATTR] and len(curr_nest_tags) == 0)

						if line_type in [self.LINE_TYPE_START_NEST, self.LINE_TYPE_START_NEST_WITH_ATTR]:
							curr_nest_tags.append(tag)
						elif line_type == self.LINE_TYPE_END_NEST:
							popped_curr_nest_tag = curr_nest_tags.pop()
							assert popped_curr_nest_tag == tag, curr_nest
							if len(curr_nest_tags) == 0:
								output_nest = True
						if output_nest: 
							nest_dict, _ = self.convert_nest(curr_nest, 0)

							self.processing_func(nest_dict)

							curr_nest = list()
							curr_nest_tag = str()

						curr_str = ""

				if curr_str != "":
					# divide lines by a space
					curr_str += ' '


class OWLParser():
	def __init__(self, input_file_name, output_file_name):
		self.XML_TAG = "?xml"
		self.RDF_TAG = "rdf:RDF"
		self.DOCTYPE_TAG = "!DOCTYPE"
		self.CLASS_TAG = "owl:Class"
		self.RESTRICTION_TAG = "owl:Restriction"
		self.SUBCLASS_TAG = "rdfs:subClassOf"
		self.NODEID_TAG = "rdf:nodeID"
		self.RDF_ABOUT_TAG = "rdf:about"
		self.GENID_PREFIX = "genid"

		self.skip_tags = [self.XML_TAG, self.RDF_TAG, self.DOCTYPE_TAG]

		self.ignored_attributes = ["xml:lang"]

		self.xml_parser = XMLParser(self.skip_tags, self.ignored_attributes, self.triage_nest_dict)

		self.GENID_REMAINING_NESTS = dict()
		self.GENID_TO_ID = dict()
		self.ID_TO_GENIDS = dict()

		self.input_file = input_file_name
		self.output_file_name = output_file_name

		self.output_info = create_single_jsonlines()
		self.output = output_info[0]


	def check_for_class_genids(self, nest_dict):
		genids = list()

		nest_dict_classes = nest_dict.get(self.CLASS_TAG, list())
		for nest_class_index in range(len(nest_dict_classes)):
			nest_class = nest_dict_classes[nest_class_index]
			nest_subclasses = nest_class.get(self.SUBCLASS_TAG, list())
			for nest_subclass_index in range(len(nest_subclasses)):
				nest_subclass = nest_subclasses[nest_subclass_index]
				potential_genid = nest_subclass.get(self.NODEID_TAG, str())
				if potential_genid.startswith(self.GENID_PREFIX):
					genids.append(potential_genid)

		return genids


	def check_for_restriction_genids(self, nest_dict):
		for nest_restriction in nest_dict.get(self.RESTRICTION_TAG, dict()):
			potential_genid = nest_restriction.get(self.NODEID_TAG, str())
			if potential_genid.startswith(self.GENID_PREFIX):
					return potential_genid
		return None

	def extract_class_id(self, nest_dict):
		nest_dict_classes = nest_dict.get(self.CLASS_TAG, list())
		# Can't have competing class_ids
		assert len(nest_dict_classes) <= 1

		for nest_class_index in range(len(nest_dict_classes)):
			nest_class = nest_dict_classes[nest_class_index]
			return nest_class.get(self.RDF_ABOUT_TAG, str())

	def store_genid_nest_in_class_nest(self, genid, genid_nest, class_nest):
		output_class_nest = class_nest
		
		nest_dict_classes = class_nest.get(self.CLASS_TAG, list())
		for nest_class_index in range(len(nest_dict_classes)):
			nest_class = nest_dict_classes[nest_class_index]
			nest_subclasses = nest_class.get(self.SUBCLASS_TAG, list())
			for nest_subclass_index in range(len(nest_subclasses)):
				nest_subclass = nest_subclasses[nest_subclass_index]
				potential_genid = nest_subclass.get(self.NODEID_TAG, str())
				if potential_genid == genid:
					output_class_nest[self.CLASS_TAG][nest_class_index][self.SUBCLASS_TAG][nest_subclass_index][self.RESTRICTION_TAG] = genid_nest[self.RESTRICTION_TAG]

		return output_class_nest


	def triage_nest_dict(self, nest_dict):
		genids = self.check_for_class_genids(nest_dict)
		restriction_genid = self.check_for_restriction_genids(nest_dict)
		class_id = self.extract_class_id(nest_dict)

		if len(genids) > 0:
			for genid in genids:
				self.GENID_TO_ID[genid] = class_id
			self.ID_TO_GENIDS[class_id] = genids
			self.GENID_REMAINING_NESTS[class_id] = nest_dict
		elif restriction_genid is not None:
			class_id = self.GENID_TO_ID.get(restriction_genid, str())
			if len(class_id) == 0:
				print("WARNING WITH:", restriction_genid, "- NO CLASS_ID FOUND")

				# Save to output despite not matching with an existing class
				self.output.write(nest_dict)
				return
			class_nest = self.GENID_REMAINING_NESTS[class_id]
			self.ID_TO_GENIDS[class_id].remove(restriction_genid)
			updated_class_nest = self.store_genid_nest_in_class_nest(restriction_genid, nest_dict, class_nest)

			if len(self.ID_TO_GENIDS[class_id]) > 0:
				self.GENID_REMAINING_NESTS[class_id] = updated_class_nest
			else:
				# Since all of the genids used in this class have been matched, output
				self.output.write(nest_dict)
				self.GENID_REMAINING_NESTS[class_id] = None
		else:
			# There are no genids that need to be worked with, so just output
			self.output.write(nest_dict)


	def parse_OWL_file(self):
		self.xml_parser.divide_into_lines(self.input_file)

		# Genid wasn't filled, still want to include them though
		for item in self.GENID_REMAINING_NESTS:
			if self.GENID_REMAINING_NESTS[item] != None:
				self.output.write(self.GENID_REMAINING_NESTS[item])

		close_single_jsonlines(self.output_info, self.output_file_name)


if __name__ == '__main__':
	args = get_args()
	input_file_name = args.inputFile
	output_file_name = args.outputFile

	print("File:", input_file_name)
	print("Start Time:", date())
	owl_parser = OWLParser(input_file_name, output_file_name)
	owl_parser.parse_OWL_file()
	print("End Time:", date())