#!/usr/bin/env python3

"""
    The file generated from kg2.json, edges.tsv, is much too large at ~34 GB
    to upload to Git LFS
    The best compression ratio I get from xz is ~13.9, resulting in ~4.7 GB, still too large.
    I propose splitting `edges.tsv` into two files.
    Currently, this is set to create two files of equal line size.

    Usage: python3 split_kgx_tsv.py
"""
import os

__author__ = 'Liliana Acevedo'
__copyright__ = 'Oregon State University'
__credits__ = ''
__license__ = 'MIT'
__version__ = '0.1.0'
__maintainer__ = ''
__status__ = 'Prototype'

INPUT_FILE_PATH = "/Users/lilianaacevedo/kg2-files/rtx-kg2.7.6pre-kgx-edges.tsv"


def get_header(file):
    # Read the header row from the file
    header = file.readline()
    return header


def split_tsv():

    inputfilepath = INPUT_FILE_PATH
    filename, ext = inputfilepath.rsplit('.', 1)
    ii = 1
    cmd = "wc -l {}"
    process = os.popen(cmd.format(inputfilepath))
    preprocessed = process.read()
    chunksize = (int(preprocessed.replace(inputfilepath, "").strip()) // 2) + 1
    process.close()

    written = False
    with open(inputfilepath, "r") as fp:
        header = get_header(fp)
        while True:
            outfilepath = "{}{}.{}".format(filename, ii, ext)
            with open(outfilepath, "w") as outfile:
                outfile.write(header)
                for line in (fp.readline() for _ in range(chunksize)):
                    outfile.write(line)
                written = bool(line)
            if not written:
                break
            ii += 1


if __name__ == "__main__":
    split_tsv()
