#!/usr/bin/env python3
''' owlparser.py: Converts OWL (XML) Files into JSON Lines Representations

    Usage: owlparser.py [--test] <inputFile.yaml> <owlFilePath> <outputFile.jsonl>
'''

import json
import argparse
import datetime
import kg2_util

__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def get_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--test', dest='test',
                            action="store_true", default=False)
    arg_parser.add_argument('inputFile', type=str)
    arg_parser.add_argument('owlFilePath', type=str)
    arg_parser.add_argument('outputFile', type=str)
    return arg_parser.parse_args()

def date():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class LineElementRead():
    NONE = 0
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

        # Variables for line reading
        self.tag = ""
        self.attributes = dict()
        self.attribute_tag = ""
        self.attribute_text = ""
        self.main_text = ""
        self.end_tag = ""
        self.only_tag = False
        self.start_brackets = 0
        self.line = ""
        self.letter = ""
        self.next_letter = ""
        self.prev_letter = ""
        self.type_to_read = LineElementRead.NONE

    def categorize_line(self):
        # Categorize the type of line
        line_type = str()
        out = dict()

        # Putting "only_tag" here isn't necessarily the best idea, but I don't know what else to do with it
        if self.tag == self.COMMENT or self.tag in self.OUTMOST_TAGS_SKIP or self.end_tag in self.OUTMOST_TAGS_SKIP or self.only_tag:
            line_type = self.LINE_TYPE_IGNORE
        else:
            start_tag_exists = (self.tag != str())
            attributes_exist = (self.attributes != dict())
            text_exists = (self.main_text != str())
            end_tag_exists = (self.end_tag != str())

            if start_tag_exists:
                if attributes_exist:
                    if text_exists:
                        line_type = self.LINE_TYPE_ENTRY_WITH_ATTR
                        out[self.KEY_TAG] = self.tag
                        out[self.KEY_ATTRIBUTES] = self.attributes
                        out[self.KEY_TEXT] = self.main_text
                    elif end_tag_exists:
                        line_type = self.LINE_TYPE_ENTRY_ONLY_ATTR
                        out[self.KEY_TAG] = self.tag
                        out[self.KEY_ATTRIBUTES] = self.attributes
                    else:
                        line_type = self.LINE_TYPE_START_NEST_WITH_ATTR
                        out[self.KEY_TAG] = self.tag
                        out[self.KEY_ATTRIBUTES] = self.attributes
                elif text_exists:
                    line_type = self.LINE_TYPE_ENTRY
                    out[self.KEY_TAG] = self.tag
                    out[self.KEY_TEXT] = self.main_text
                else:
                    line_type = self.LINE_TYPE_START_NEST
                    out[self.KEY_TAG] = self.tag
            elif end_tag_exists:
                line_type = self.LINE_TYPE_END_NEST
                out[self.KEY_TAG] = self.end_tag

        out[self.KEY_TYPE] = line_type

        return out

    def get_letters(self, letter_index):
        self.letter = self.line[letter_index]
        self.next_letter = ""
        self.prev_letter = ""
        if letter_index + 1 < len(self.line):
            self.next_letter = self.line[letter_index + 1]
        if letter_index - 1 >= 0:
            self.prev_letter = self.line[letter_index - 1]

        if self.letter == '<':
            self.start_brackets += 1
        if self.letter == '>':
            self.start_brackets -= 1


    def identify_tag_type(self, letter_index):
        changed = True

        if self.letter == '<' and letter_index == 0:
            if self.next_letter != '/':
                self.type_to_read = LineElementRead.TAG
        elif self.letter == '/' and self.prev_letter == '<':
            self.type_to_read = LineElementRead.END_TAG
        else:
            changed = False

        return changed


    def read_tag(self):
        changed = True

        if self.letter == ' ' and self.type_to_read == LineElementRead.TAG:
            self.type_to_read = LineElementRead.ATTRIBUTE_TAG
        elif self.letter == '>' and self.type_to_read == LineElementRead.TAG and self.start_brackets == 0:
            self.type_to_read = LineElementRead.MAIN

            if self.prev_letter == '/':
                print("Warning - strange tag, ignoring", self.line)
                self.only_tag = True
        elif self.type_to_read == LineElementRead.TAG:
            self.tag += self.letter
        else:
            changed = False

        return changed


    def store_attribute(self):
        if self.attribute_tag not in self.IGNORED_ATTRIBUTES:
            self.attributes[self.attribute_tag] = self.attribute_text.strip('/').strip('"')
        self.attribute_tag = ""
        self.attribute_text = ""


    def read_attributes(self):
        changed = True
        start_reading_attributes = (self.type_to_read == LineElementRead.ATTRIBUTE_TAG or self.type_to_read == LineElementRead.ATTRIBUTE_TEXT)

        if self.letter == '>' and start_reading_attributes and self.start_brackets == 0:
            self.type_to_read = LineElementRead.MAIN
            
            self.store_attribute()

            if self.prev_letter == '/':
                self.end_tag = self.tag
        elif start_reading_attributes:
            if self.letter == '=' and self.type_to_read == LineElementRead.ATTRIBUTE_TAG:
                self.type_to_read = LineElementRead.ATTRIBUTE_TEXT
            elif self.type_to_read == LineElementRead.ATTRIBUTE_TAG:
                self.attribute_tag += self.letter
            elif self.letter == ' ' and self.type_to_read == LineElementRead.ATTRIBUTE_TEXT:
                self.type_to_read = LineElementRead.ATTRIBUTE_TAG
                self.store_attribute()
            elif self.type_to_read == LineElementRead.ATTRIBUTE_TEXT:
                self.attribute_text += self.letter
        else:
            changed = False

        return changed


    def read_main(self):
        changed = True
        if self.letter == '<' and self.type_to_read == LineElementRead.MAIN:
            self.type_to_read = LineElementRead.END_TAG
        elif self.type_to_read == LineElementRead.MAIN:
            self.main_text += self.letter
        else:
            changed = False

        return changed


    def read_end_tag(self):
        changed = True
        if self.letter == '>' and self.type_to_read == LineElementRead.END_TAG and self.start_brackets == 0:
            pass
        elif self.type_to_read == LineElementRead.END_TAG:
            self.end_tag += self.letter
        else:
            changed = False

        return changed


    def convert_line(self):
        self.tag = ""
        self.attributes = dict()
        self.attribute_tag = ""
        self.attribute_text = ""
        self.main_text = ""
        self.end_tag = ""

        self.type_to_read = LineElementRead.NONE

        self.only_tag = False

        self.start_brackets = 0

        for letter_index in range(len(self.line)):
            self.get_letters(letter_index)

            # First <
            if self.identify_tag_type(letter_index):
                continue

            if self.read_tag():
                continue

            if self.read_attributes():
                continue

            if self.read_main():
                continue

            if self.read_end_tag():
                continue

        return self.categorize_line()


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
                        self.line = curr_str
                        line_parsed = self.convert_line()

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
    def __init__(self, input_files, input_file_names, owl_file_path, output_file_name):
        self.XML_TAG = "?xml"
        self.RDF_TAG = "rdf:RDF"
        self.DOCTYPE_TAG = "!DOCTYPE"
        self.CLASS_TAG = "owl:Class"
        self.RESTRICTION_TAG = "owl:Restriction"
        self.SUBCLASS_TAG = "rdfs:subClassOf"
        self.NODEID_TAG = "rdf:nodeID"
        self.RDF_ABOUT_TAG = "rdf:about"
        self.GENID_PREFIX = "genid"

        self.OWL_SOURCE_KEY = "owl_source"
        self.OWL_SOURCE_NAME_KEY = "owl_source_name"

        self.skip_tags = [self.XML_TAG, self.RDF_TAG, self.DOCTYPE_TAG]

        self.ignored_attributes = ["xml:lang"]

        self.xml_parser = XMLParser(self.skip_tags, self.ignored_attributes, self.triage_nest_dict)

        self.GENID_REMAINING_NESTS = dict()
        self.GENID_TO_ID = dict()
        self.ID_TO_GENIDS = dict()

        self.input_files = input_files
        self.input_file_names = input_file_names
        self.owl_file_path = owl_file_path
        self.output_file_name = output_file_name

        self.output_info = kg2_util.create_single_jsonlines()
        self.output = self.output_info[0]

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


    def write_to_output(self, output_dict, source_file):
        output_dict[self.OWL_SOURCE_KEY] = source_file
        output_dict[self.OWL_SOURCE_NAME_KEY] = self.input_file_names[source_file]
        self.output.write(output_dict)

        return


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
                self.write_to_output(nest_dict, self.input_file)
                return
            class_nest = self.GENID_REMAINING_NESTS[class_id]
            self.ID_TO_GENIDS[class_id].remove(restriction_genid)
            updated_class_nest = self.store_genid_nest_in_class_nest(restriction_genid, nest_dict, class_nest)

            if len(self.ID_TO_GENIDS[class_id]) > 0:
                self.GENID_REMAINING_NESTS[class_id] = updated_class_nest
            else:
                # Since all of the genids used in this class have been matched, output
                self.write_to_output(nest_dict, self.input_file)
                self.GENID_REMAINING_NESTS[class_id] = None
        else:
            # There are no genids that need to be worked with, so just output
            self.write_to_output(nest_dict, self.input_file)


    def parse_OWL_file(self):
        for input_file in self.input_files:
            self.input_file = input_file
            print("Reading:", input_file, "starting at", date())
            self.xml_parser.divide_into_lines(self.owl_file_path + input_file)

            # Genid wasn't filled, still want to include them though
            for item in self.GENID_REMAINING_NESTS:
                if self.GENID_REMAINING_NESTS[item] != None:
                    self.write_to_output(self.GENID_REMAINING_NESTS[item], self.input_file)

            # Refresh everything for the next file
            self.GENID_REMAINING_NESTS = dict()
            self.GENID_TO_ID = dict()
            self.ID_TO_GENIDS = dict()

        kg2_util.close_single_jsonlines(self.output_info, self.output_file_name)


def identify_and_download_input_files(ont_load_inventory, path_to_owl_files):
    input_files = list()
    input_file_names = dict()
    owl_file_path = path_to_owl_files.rstrip('/') + "/"
    for item in ont_load_inventory:
        input_files.append(item['file'])
        input_file_names[item['file']] = item['title']
        print("Downloading:", item['file'], "starting at", date())
        kg2_util.download_file_if_not_exist_locally(item['url'], owl_file_path + item['file'])
        print("Download of:", item['file'], "finished at", date())

    return input_files, input_file_names, owl_file_path

if __name__ == '__main__':
    args = get_args()
    input_file_name = args.inputFile
    owl_path = args.owlFilePath
    output_file_name = args.outputFile

    ont_load_inventory = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(input_file_name))
    input_files, input_file_names, owl_file_path = identify_and_download_input_files(ont_load_inventory, owl_path)

    print("Files:", input_files)
    print("Start Time:", date())
    owl_parser = OWLParser(input_files, input_file_names, owl_file_path, output_file_name)
    owl_parser.parse_OWL_file()
    print("End Time:", date())