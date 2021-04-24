#!/usr/bin/env python3

''' Generages a Snakemake readable YAML config file from the
    master-config.shinc script and a pseudo-YAML file with
    the variables that Snakemake is expecting.

    Usage: generate_snakemake_config_file.py <master-config.shinc>
                                             <snakemake-config-var.yaml>
                                             <snakemake-config-output.yaml>
'''

import argparse


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood', 'Lindsey Kvarfordt']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('masterConfig', type=str)
    parser.add_argument('snakemakeVariablesYaml', type=str)
    parser.add_argument('outputFile', type=str)
    parser.add_argument('--test',
                        dest='test',
                        action='store_true',
                        default=False)

    return parser.parse_args()


def dictionaryify_file(filename: str, existing_dictionary, divider):
    # Uuse the existing dictionary to strip the variables out of
    # the file and replace it with the actual values

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if len(line) > 1 and line.startswith("if") is False:
                key = line.split(divider)[0].upper()
                value = line.split(divider)[1].strip()
                value = value.replace("~", "/home/ubuntu")
                if '$' in value:

                    # If the Bash variable structure is used, take out the
                    # actual variable part to use as a key (for the
                    # variable_storage dictionary) and retrieve its actual
                    # value, so that the resulting YAML
                    # file is Snakemake readable

                    value_split = value.split('$')[1:]
                    for variable in value_split:
                        start = variable.find('{') + 1
                        end = variable.find('}')
                        variable = variable[start:end]
                        value = value.replace("${" + variable + "}", existing_dictionary[variable.upper()])
                existing_dictionary[key] = value
    return existing_dictionary


if __name__ == '__main__':
    args = get_args()
    test = args.test
    if test is True:
        test_suffix = "-test"
        test_flag = "test"
        test_arg = "--test"
    else:
        test_suffix = ''
        test_flag = ''
        test_arg = ''

    variable_storage = dict()

    # We have to put the test arguments into the variable storage
    # dictionary first because some of the variables within
    # master-config.shinc depend on them

    variable_storage["TEST_SUFFIX"] = test_suffix
    variable_storage["TEST_FLAG"] = test_flag
    variable_storage["TEST_ARG"] = test_arg

    # We dictionarify master-config.shinc first
    # because most of the variables within the snakemake
    # variables YAML file depend on them (particularly
    # ${KG2_BUILD}).
    variable_storage = dictionaryify_file(args.masterConfig,
                                          variable_storage,
                                          '=')
    variable_storage = dictionaryify_file(args.snakemakeVariablesYaml,
                                          variable_storage,
                                          ':')

    if test is False:
        variable_storage["TEST_SUFFIX"] = '""'
        variable_storage["TEST_FLAG"] = '""'
        variable_storage["TEST_ARG"] = '""'

    with open(args.outputFile, 'w+') as output:
        for key, value in variable_storage.items():
            line = key + ": " + value + "\n"
            output.write(line)
