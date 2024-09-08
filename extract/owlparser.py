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
    """
        Custom enum for identifying which element is currently being read in an XML Line
    """
    NONE = 0
    TAG = 1
    ATTRIBUTE_TAG = 2
    ATTRIBUTE_TEXT = 3
    MAIN = 4
    END_TAG = 5


class XMLParser():
    """
        General XML to JSON Lines parser optimized for XML consisting of many short nests
    """
    def __init__(self, skip_tags, ignored_attributes, processing_func):
        # Defining the types of lines which will be skipped by the processor
        self.COMMENT = "!--"
        self.OUTMOST_TAGS_SKIP = skip_tags # To avoid one large JSON Line, the outmost tags should be skipped
        self.IGNORED_ATTRIBUTES = ignored_attributes

        # Function for processing each nest
        self.processing_func = processing_func

        # Line categorization labels
        self.LINE_TYPE_IGNORE = "ignore"
        self.LINE_TYPE_START_NEST = "start nest"
        self.LINE_TYPE_START_NEST_WITH_ATTR = "start nest with attributes"
        self.LINE_TYPE_ENTRY = "entry"
        self.LINE_TYPE_ENTRY_WITH_ATTR = "entry with attributes"
        self.LINE_TYPE_ENTRY_ONLY_ATTR = "entry with only attributes"
        self.LINE_TYPE_END_NEST = "end nest"

        # Processing labels for components of each line
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
        """
            Logic for determining which type of line is being processed based on the content of its attributes
        """
        # Categorize the type of line
        line_type = str()
        out = dict()

        # If it is one of these first line types, skip it
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
                        # This type of line has everything
                        line_type = self.LINE_TYPE_ENTRY_WITH_ATTR
                        out[self.KEY_TAG] = self.tag
                        out[self.KEY_ATTRIBUTES] = self.attributes
                        out[self.KEY_TEXT] = self.main_text
                    elif end_tag_exists:
                        # This type of line acts an an entry, but doesn't have text. There is not another end_tag coming for it.
                        line_type = self.LINE_TYPE_ENTRY_ONLY_ATTR
                        out[self.KEY_TAG] = self.tag
                        out[self.KEY_ATTRIBUTES] = self.attributes
                    else:
                        # This type of line does not have an entry and acts as the start of an inner nest
                        line_type = self.LINE_TYPE_START_NEST_WITH_ATTR
                        out[self.KEY_TAG] = self.tag
                        out[self.KEY_ATTRIBUTES] = self.attributes
                elif text_exists:
                    # This type of line does not have attributes and only contains an entry
                    line_type = self.LINE_TYPE_ENTRY
                    out[self.KEY_TAG] = self.tag
                    out[self.KEY_TEXT] = self.main_text
                else:
                    # This type of line is only starting a nest and does not contain any of its own information
                    line_type = self.LINE_TYPE_START_NEST
                    out[self.KEY_TAG] = self.tag
            elif end_tag_exists:
                # This type of line ends a started nest
                line_type = self.LINE_TYPE_END_NEST
                out[self.KEY_TAG] = self.end_tag

        # Assign the key type based on the determined line type
        out[self.KEY_TYPE] = line_type

        return out


    def get_letters(self, letter_index):
        """
            Get the current letter, previous letter, and next letter in the line and count the brackets status (in case there are brackets inside of brackets)
        """
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
        """
            Depending on the presence of a "/" character, determine whether this is an end tag
        """
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
        """
            Determine the tag of an XML line
        """
        changed = True

        # Once you hit a space or bracket, switch to the next type of line element
        # If not, keep adding to the tag
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
        """
            Clean and save an attribute for later processing
        """
        # Only save desired attributes
        if self.attribute_tag not in self.IGNORED_ATTRIBUTES:
            self.attributes[self.attribute_tag] = self.attribute_text.strip('/').strip('"')

        # Reset our attribute trackers
        self.attribute_tag = ""
        self.attribute_text = ""


    def read_attributes(self):
        """
            Determine the attributes of an XML line
        """
        changed = True

        # Identify whether it is time to process the attributes of the line
        start_reading_attributes = (self.type_to_read == LineElementRead.ATTRIBUTE_TAG or self.type_to_read == LineElementRead.ATTRIBUTE_TEXT)

        # At the end of the attributes section, save the attributes and switch to the text portion of the line
        if self.letter == '>' and start_reading_attributes and self.start_brackets == 0:
            self.type_to_read = LineElementRead.MAIN
            
            self.store_attribute()

            if self.prev_letter == '/':
                self.end_tag = self.tag
        # Otherwise, read the correct part of the line and switch parts based on the delimiter ('=' and ' ')
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
        """
            Determine the main textual entry of an XML line
        """
        changed = True

        # Stop reading and switch to reading the end tag once you hit a start bracket
        if self.letter == '<' and self.type_to_read == LineElementRead.MAIN:
            self.type_to_read = LineElementRead.END_TAG
        elif self.type_to_read == LineElementRead.MAIN:
            self.main_text += self.letter
        else:
            changed = False

        return changed


    def read_end_tag(self):
        """
            Determine the end tag of an XML line
        """
        changed = True

        # Stop once you've reached the end of the line
        if self.letter == '>' and self.type_to_read == LineElementRead.END_TAG and self.start_brackets == 0:
            pass
        # Otherwise, add to the end tag
        elif self.type_to_read == LineElementRead.END_TAG:
            self.end_tag += self.letter
        else:
            changed = False

        return changed


    def convert_line(self):
        """
            Using a streaming reading technique, convert a line into its tag, attributes, text, and type
        """
        # Initialize all of the line elements for the new line
        self.tag = ""
        self.attributes = dict()
        self.attribute_tag = ""
        self.attribute_text = ""
        self.main_text = ""
        self.end_tag = ""
        self.type_to_read = LineElementRead.NONE
        self.only_tag = False
        self.start_brackets = 0

        # Read the line letter by letter
        for letter_index in range(len(self.line)):
            # Get the letters required for analysis regardless of the element type
            self.get_letters(letter_index)

            # Start by determining if it is a start or end tag
            if self.identify_tag_type(letter_index):
                # If this was the work done on this letter, move to the next
                continue

            # Determine the tag of the line
            if self.read_tag():
                # If this was the work done on this letter, move to the next
                continue

            # Determine the attributes of the line (if applicable)
            if self.read_attributes():
                # If this was the work done on this letter, move to the next
                continue

            # Determine the main text given in the line (if applicable)
            if self.read_main():
                # If this was the work done on this letter, move to the next
                continue

            # Determine the end tag of the line (if applicable)
            if self.read_end_tag():
                # If this was the work done on this letter, move to the next
                continue

        # Categorize the line based on the saved characteristics
        return self.categorize_line()


    def convert_nest(self, nest, start_index):
        """
            Recursively the set of lines (from the first start tag to its pairing end tag) into a dictionary (nested as necessary)
        """
        # Initialize the current dictionary in the nest
        nest_dict = dict()

        # Start at the given index
        curr_index = start_index

        # Iterate linearly (without repeat) through every element in the nest
        while curr_index < len(nest):
            # Get the basic characteristics of the nest element
            element = nest[curr_index]
            line_type = element[self.KEY_TYPE]
            line_tag = element[self.KEY_TAG]
            line_text = element.get(self.KEY_TEXT, None)
            line_attributes = element.get(self.KEY_ATTRIBUTES, None)

            # If we are starting a new nest, we need to recurse
            if line_type in [self.LINE_TYPE_START_NEST, self.LINE_TYPE_START_NEST_WITH_ATTR]:
                # Initialize every element to a list to simplify later processing (don't have to deal with some entries being strings and some being lists then)
                if line_tag not in nest_dict:
                    nest_dict[line_tag] = list()

                # Recurse to build the inner dictionary
                converted_nest, ret_index = self.convert_nest(nest, curr_index + 1)

                # If we have line attributes, we need to save them in the dictionary
                if line_attributes is not None:
                    for attribute in line_attributes:
                        converted_nest[attribute] = line_attributes[attribute]

                # Add this converted nest to the overall list
                nest_dict[line_tag].append(converted_nest)

                # Set the new index to prevent duplication
                curr_index = ret_index + 1
                continue

            # If we're not starting a new nest, process additively
            if line_type in [self.LINE_TYPE_ENTRY, self.LINE_TYPE_ENTRY_WITH_ATTR, self.LINE_TYPE_ENTRY_ONLY_ATTR]:
                # Initialize every element to a list to simplify later processing (don't have to deal with some entries being strings and some being lists then)
                if line_tag not in nest_dict:
                    nest_dict[line_tag] = list()

                curr_dict = dict()

                # If we have line text, we need to save it in the dictionary
                if line_text is not None:
                    curr_dict[self.KEY_TEXT] = line_text

                # If we have line attributes, we need to save them in the dictionary
                if line_attributes is not None:
                    for attribute in line_attributes:
                        curr_dict[attribute] = line_attributes[attribute]

                # Add this converted nest to the overall list
                nest_dict[line_tag].append(curr_dict)

                # Move to the next element
                curr_index += 1
                continue

            # Recursive base case, to exit the nest building when we hit the end of a nest
            if line_type in [self.LINE_TYPE_END_NEST]:
                return nest_dict, curr_index

        # Once we reach the end, we need to return the nest
        return nest_dict, curr_index


    def divide_into_lines(self, input_file_name):
        """
            Split a given XML file into sets of lines representing a nest (at a given level within the overall XML nest, based on the ignored lines) and process these nests
        """
        # Initialize the current nest
        curr_str = ""
        curr_nest = list()
        curr_nest_tags = list() # Treating it as a stack, since some tags will be identical within a nest and we want to make sure start and end tags match
        start_brackets = 0

        with open(input_file_name) as input_file:
            # Iterate linearly through the file
            for line in input_file:
                line_str = line.strip()

                # Process each letter in the line linearly
                for letter_index in range(len(line_str)):
                    letter = line_str[letter_index]

                    # In case of nested brackets ("<<>>"), need to maintain matching brackets
                    if letter == '<':
                        start_brackets += 1
                    if letter == '>':
                        start_brackets -= 1

                    # Identify the next letter, to aid in identifying the end of the line
                    next_letter = ""
                    if letter_index + 1 < len(line_str):
                        next_letter = line_str[letter_index + 1]

                    # Build up the current line
                    curr_str += letter

                    # Determine when we have reached the end of the line and process accordingly 
                    if letter == '>' and (next_letter == '<' or next_letter == "") and start_brackets == 0:
                        # Assign the class variable the current string to facilitate processing
                        self.line = curr_str
                        # Process the line
                        line_parsed = self.convert_line()

                        # Determine important traits of the line to build the nest
                        tag = line_parsed.get(self.KEY_TAG, None)
                        assert tag != self.KEY_TEXT # This could cause a massive conflict, but it is unlikely
                        line_type = line_parsed.get(self.KEY_TYPE, None)

                        # Add non-ignore lines to the nest
                        if line_type != self.LINE_TYPE_IGNORE:
                            curr_nest.append(line_parsed)

                        # Initialize the output_file criteria
                        output_nest = (line_type in [self.LINE_TYPE_ENTRY, self.LINE_TYPE_ENTRY_WITH_ATTR, self.LINE_TYPE_ENTRY_ONLY_ATTR] and len(curr_nest_tags) == 0)

                        # If we are starting a new internal nest, push the current tag to the stack to ensure it has a matching end tag
                        if line_type in [self.LINE_TYPE_START_NEST, self.LINE_TYPE_START_NEST_WITH_ATTR]:
                            curr_nest_tags.append(tag)
                        # Ensure that the reached end tag matches the last start tag
                        elif line_type == self.LINE_TYPE_END_NEST:
                            popped_curr_nest_tag = curr_nest_tags.pop()
                            assert popped_curr_nest_tag == tag, curr_nest

                            # The nest is ready to process once we have matched the original start tag
                            if len(curr_nest_tags) == 0:
                                output_nest = True

                        # Once the nest has been finished, convert it into a dictionary and process it
                        if output_nest: 
                            nest_dict, _ = self.convert_nest(curr_nest, 0)

                            # Process the given nest dictionary based on a given processing function
                            self.processing_func(nest_dict)

                            # Reinitialize variables for the next loop
                            curr_nest = list()
                            curr_nest_tag = str()

                        curr_str = ""

                # If we have to go to the next line to finish processing one XML line, add a delimiting space
                if curr_str != "":
                    curr_str += ' '


class OWLParser():
    """
        Custom parser (into JSON Lines) for XML-style OWL files
    """
    def __init__(self, input_files, input_file_names, owl_file_path, output_file_name):
        # Important tags within OWL files for processing
        self.XML_TAG = "?xml"
        self.RDF_TAG = "rdf:RDF"
        self.DOCTYPE_TAG = "!DOCTYPE"
        self.CLASS_TAG = "owl:Class"
        self.RESTRICTION_TAG = "owl:Restriction"
        self.SUBCLASS_TAG = "rdfs:subClassOf"
        self.NODEID_TAG = "rdf:nodeID"
        self.RDF_ABOUT_TAG = "rdf:about"

        # Generic OWL ID prefix
        self.GENID_PREFIX = "genid"

        # Custom additions to JSON Lines output to propagate ont-load-inventory.yaml information
        self.OWL_SOURCE_KEY = "owl_source"
        self.OWL_SOURCE_NAME_KEY = "owl_source_name"

        # Tags to exclude from JSON Lines representation, to be passed into XML Parser
        self.skip_tags = [self.XML_TAG, self.RDF_TAG, self.DOCTYPE_TAG]

        # Attributes to ignore for JSON Lines representation (due to overcrowding)
        self.ignored_attributes = ["xml:lang"]

        # XML Parser for OWL Parser, using triage_nest_dict as the processing_func
        self.xml_parser = XMLParser(self.skip_tags, self.ignored_attributes, self.triage_nest_dict)

        # Initialize the genid processing dictionaries required
        self.GENID_REMAINING_NESTS = dict()
        self.GENID_TO_ID = dict()
        self.ID_TO_GENIDS = dict()

        # File names for input/output
        self.input_files = input_files
        self.input_file_names = input_file_names
        self.owl_file_path = owl_file_path
        self.output_file_name = output_file_name

        # Output writer
        self.output_info = kg2_util.create_single_jsonlines()
        self.output = self.output_info[0]


    def check_for_class_genids(self, nest_dict):
        """
            Scanner for genids within an "owl:Class", to prepare them for later matching
        """
        genids = list()

        nest_dict_classes = nest_dict.get(self.CLASS_TAG, list())
        for nest_class_index in range(len(nest_dict_classes)):
            nest_class = nest_dict_classes[nest_class_index]

            # genids are contained within "rdfs:subClassOf" elements
            nest_subclasses = nest_class.get(self.SUBCLASS_TAG, list())
            for nest_subclass_index in range(len(nest_subclasses)):
                nest_subclass = nest_subclasses[nest_subclass_index]
                potential_genid = nest_subclass.get(self.NODEID_TAG, str())
                if potential_genid.startswith(self.GENID_PREFIX):
                    genids.append(potential_genid)

        return genids


    def check_for_restriction_genids(self, nest_dict):
        """
            Check a nest for possibly containing a "genid" term within an "owl:Restriction" element
        """
        for nest_restriction in nest_dict.get(self.RESTRICTION_TAG, dict()):
            potential_genid = nest_restriction.get(self.NODEID_TAG, str())
            if potential_genid.startswith(self.GENID_PREFIX):
                    return potential_genid
        return None


    def extract_class_id(self, nest_dict):
        """
            Determine the id of an "owl:Class", for use as a key
        """
        nest_dict_classes = nest_dict.get(self.CLASS_TAG, list())
        # Can't have competing class_ids
        assert len(nest_dict_classes) <= 1

        for nest_class_index in range(len(nest_dict_classes)):
            nest_class = nest_dict_classes[nest_class_index]
            return nest_class.get(self.RDF_ABOUT_TAG, str())


    def store_genid_nest_in_class_nest(self, genid, genid_nest, class_nest):
        """
            Replace a genid entry in an "rdfs:subClassOf" element with its corresponding "owl:Restriction" definition (which contains an actual identifier)
        """
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
        """
            Save other information to an output dictionary before writing it to the output JSON Lines file
        """
        output_dict[self.OWL_SOURCE_KEY] = source_file
        output_dict[self.OWL_SOURCE_NAME_KEY] = self.input_file_names[source_file]
        self.output.write(output_dict)


    def triage_nest_dict(self, nest_dict):
        """
            Process a nest dictionary by outputting it if it's ready (no outstanding "genid" terms)
        """
        # Check for elements which complicate save pattern
        genids = self.check_for_class_genids(nest_dict)
        restriction_genid = self.check_for_restriction_genids(nest_dict)
        class_id = self.extract_class_id(nest_dict)

        # If there are class genids, save these for future identification and store the nest to be outputted later
        if len(genids) > 0:
            for genid in genids:
                self.GENID_TO_ID[genid] = class_id
            self.ID_TO_GENIDS[class_id] = genids
            self.GENID_REMAINING_NESTS[class_id] = nest_dict
        # If this nest contains a genid definition to be placed in its "owl:Class", place it, then output the nest
        elif restriction_genid is not None:
            class_id = self.GENID_TO_ID.get(restriction_genid, str())

            # Issue a warning if genid doesn't correspond to an "owl:Class"
            if len(class_id) == 0:
                print("WARNING WITH:", restriction_genid, "- NO CLASS_ID FOUND")

                # Save to output despite not matching with an existing class
                self.write_to_output(nest_dict, self.input_file)
                return

            # Store the genid and remove it from the list of outstanding genids
            class_nest = self.GENID_REMAINING_NESTS[class_id]
            self.ID_TO_GENIDS[class_id].remove(restriction_genid)
            updated_class_nest = self.store_genid_nest_in_class_nest(restriction_genid, nest_dict, class_nest)

            # We must wait until all of the genids in the "owl:Class" have been matched to finally output
            if len(self.ID_TO_GENIDS[class_id]) > 0:
                self.GENID_REMAINING_NESTS[class_id] = updated_class_nest
            else:
                self.write_to_output(nest_dict, self.input_file)
                self.GENID_REMAINING_NESTS[class_id] = None
        # Otherwise, it is a normal situation
        else:
            # There are no genids that need to be worked with, so just output
            self.write_to_output(nest_dict, self.input_file)


    def parse_OWL_file(self):
        """
            Handler for parsing the owl files
        """
        # Iterate through the input files, processing them
        for input_file in self.input_files:
            # Set the current OWLParser input file to this input file
            self.input_file = input_file
            print("Reading:", input_file, "starting at", date())

            # Process the file
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
    """
        Download all of the input files in ont-load-inventory.yaml
    """
    input_files = list()
    input_file_names = dict()
    owl_file_path = path_to_owl_files.rstrip('/') + "/"

    # Download every file in the file and store the file name and title for later use as provenance
    for item in ont_load_inventory:
        input_files.append(item['file'])
        input_file_names[item['file']] = item['title']
        print("Downloading:", item['file'], "starting at", date())
        kg2_util.download_file_if_not_exist_locally(item['url'], owl_file_path + item['file'])
        print("Download of:", item['file'], "finished at", date())

    # Return, providing the file path so the files can be opened by the XMLParser later
    return input_files, input_file_names, owl_file_path

if __name__ == '__main__':
    print("Start Time:", date())
    args = get_args()

    # Obtain all arguments
    input_file_name = args.inputFile
    owl_path = args.owlFilePath
    output_file_name = args.outputFile

    # Read ont-load-inventory.yaml to prepare for OWL processing
    ont_load_inventory = kg2_util.safe_load_yaml_from_string(kg2_util.read_file_to_string(input_file_name))
    input_files, input_file_names, owl_file_path = identify_and_download_input_files(ont_load_inventory, owl_path)

    print("Files:", input_files)
    # Initialize the OWLParser
    owl_parser = OWLParser(input_files, input_file_names, owl_file_path, output_file_name)

    # Run parsing on all of the OWL files
    owl_parser.parse_OWL_file()
    print("End Time:", date())
