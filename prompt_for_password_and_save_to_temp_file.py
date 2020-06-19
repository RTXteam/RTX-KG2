#!/usr/bin/env python3
''' Prompts the user to enter a password on standard input and saves the password to a temporary file. Prints the temp file name.

    Usage: prompt_for_password_and_save_to_temp_file.py
'''

__author__ = 'Stephen Ramsey'
__copyright__ = 'Oregon State University'
__credits__ = ['Stephen Ramsey']
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__email__ = ''
__status__ = 'Prototype'

import getpass
import os
import tempfile
os.sys.path.append("..") #make modules in the code/ directory accessible
from RTXConfiguration import RTXConfiguration

if __name__ == '__main__':
    try:
        rtxc = RTXConfiguration()
        password = rtxc.neo4j_password
    except Exception as e:
        #catch and print error if RTXConfigure fails
        print(e)
        #then prompt for manual entry
        password = getpass.getpass("Please enter the password manually: ")
    tempfile = tempfile.mkstemp()[1]
    with open(os.open(tempfile, os.O_CREAT | os.O_WRONLY, 0o600), 'w') as output_file:
        print(password, file=output_file)
    print(tempfile)
