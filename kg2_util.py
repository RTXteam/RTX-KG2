#!/usr/bin/env python3
'''Utility functions used by various python scripts KG2 build system

   Usage:  import kg2_util
   (then call a function like kg2_util.log_message(), etc.)
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import copy
import datetime
import io
import os
import pprint
import re
import sys
import time
import yaml


def get_file_last_modified_timestamp(file_name: str):
    return time.gmtime(os.path.getmtime(file_name))


def read_file_to_string(local_file_name: str):
    with open(local_file_name, 'r') as myfile:
        file_contents_string = myfile.read()
    myfile.close()
    return file_contents_string


def head_list(x: list, n: int = 3):
    pprint.pprint(x[0:n])


def head_dict(x: dict, n: int = 3):
    pprint.pprint(dict(list(x.items())[0:(n-1)]))


def purge(dir, pattern):
    exp_dir = os.path.expanduser(dir)
    for f in os.listdir(exp_dir):
        if re.search(pattern, f):
            os.remove(os.path.join(exp_dir, f))


def safe_load_yaml_from_string(yaml_string: str):
    return yaml.safe_load(io.StringIO(yaml_string))


def log_message(message: str,
                ontology_name: str = None,
                node_curie_id: str = None,
                output_stream=sys.stdout):
    if node_curie_id is not None:
        node_str = ": " + node_curie_id
    else:
        node_str = ""
    if ontology_name is not None:
        ont_str = '[' + ontology_name + '] '
    else:
        ont_str = ''
    print(ont_str + message + node_str, file=output_stream)


def merge_two_dicts(x: dict, y: dict):
    ret_dict = copy.deepcopy(x)
    for key, value in y.items():
        stored_value = ret_dict.get(key, None)
        if stored_value is None:
            if value is not None:
                ret_dict[key] = value
        else:
            if value is not None and value != stored_value:
                if type(value) == str and type(stored_value) == str:
                    if value.lower() != stored_value.lower():
                        if key == 'description' or key == 'update date':
                            if len(value) > len(stored_value):  # use the longer of the two descriptions or update date fields
                                ret_dict[key] = value
                        elif key == 'ontology node type':
                            log_message("warning:  for key: " + key + ", dropping second value: " + value + '; keeping first value: ' + stored_value,
                                        output_stream=sys.stderr)
                            ret_dict[key] = stored_value
                        elif key == 'provided by':
                            if value.endswith('/STY'):
                                ret_dict[key] = value
                        elif key == 'category label':
                            if value != 'unknown category' and stored_value == 'unknown category':
                                stored_desc = ret_dict.get('description', None)
                                new_desc = y.get('description', None)
                                if stored_desc is not None and new_desc is not None:
                                    if len(new_desc) > len(stored_desc):
                                        ret_dict[key] = value
                        elif key == 'category':
                            if not value.endswith('/UnknownCategory') and stored_value.endswith('/UnknownCategory'):
                                stored_desc = ret_dict.get('description', None)
                                new_desc = y.get('description', None)
                                if stored_desc is not None and new_desc is not None:
                                    if len(new_desc) > len(stored_desc):
                                        ret_dict[key] = value
                        elif key == 'name' or key == 'full name':
                            if value.replace(' ', '_') != stored_value.replace(' ', '_'):
                                stored_desc = ret_dict.get('description', None)
                                new_desc = y.get('description', None)
                                if stored_desc is not None and new_desc is not None:
                                    if len(new_desc) > len(stored_desc):
                                        ret_dict[key] = value
                        else:
                            log_message("warning:  for key: " + key + ", dropping second value: " + value + '; keeping first value: ' + stored_value,
                                        output_stream=sys.stderr)
                elif type(value) == list and type(stored_value) == list:
                    ret_dict[key] = list(set(value + stored_value))
                elif type(value) == list and type(stored_value) == str:
                    ret_dict[key] = list(set(value + [stored_value]))
                elif type(value) == str and type(stored_value) == list:
                    ret_dict[key] = list(set([value] + stored_value))
                elif type(value) == dict and type(stored_value) == dict:
                    ret_dict[key] = merge_two_dicts(value, stored_value)
                elif key == 'deprecated' and type(value) == bool:
                    ret_dict[key] = True  # special case for deprecation; True always trumps False for this property
                else:
                    assert False
    return ret_dict


def compose_two_multinode_dicts(node1: dict, node2: dict):
    ret_dict = copy.deepcopy(node1)
    for key, value in node2.items():
        stored_value = ret_dict.get(key, None)
        if stored_value is None:
            ret_dict[key] = value
        else:
            if value is not None:
                ret_dict[key] = merge_two_dicts(node1[key], value)
    return ret_dict


def format_timestamp(timestamp: datetime):
    return time.strftime('%Y-%m-%d %H:%M:%S %Z', timestamp)
