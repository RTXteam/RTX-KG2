#!/usr/bin/env python3
''' update_version.py: increments the version of KG2

    Usage: update_version.py [--increment] <versionFile.txt>
    <outputFile.json>
'''

import argparse


__author__ = 'Erica Wood'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey', 'Erica Wood']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'


def get_args():
    arg_parser = argparse.ArgumentParser(description='update_version.py: \
                                         increments the version of KG2')
    arg_parser.add_argument('--increment_major',
                            dest='increment_major',
                            action="store_true",
                            default=False)
    arg_parser.add_argument('--increment_minor',
                            dest='increment_minor',
                            action='store_true',
                            default=False)
    arg_parser.add_argument('versionFile', type=str)
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    input_file_name = args.versionFile
    increment_major = args.increment_major
    increment_minor = args.increment_minor
    assert not (increment_major and increment_minor), "cannot specify both --increment_major and --increment_minor at the same time"
    input_file = open(input_file_name, "r")
    for line in input_file:
        input_file.close()
        output_file = open(input_file_name, "w")
        old_version = line.split(".")

        old_version[1] = str(int(old_version[1]) + increment_major)
        old_version[2] = str((int(old_version[2]) + increment_minor) * (not increment_major))

        new_version = ".".join(old_version)

        output_file.write(new_version)
        output_file.close()
        print("KG2 version: " + new_version)

        break
