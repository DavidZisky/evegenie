#!/usr/bin/env python
"""
Tool for generating Eve schemas from JSON.
"""

import os.path
import sys

from evegenie import EveGenie


def main(filename):
    """
    Create an instance of EveGenie from a json file. Then write it to file.

    :param filename: input filename
    :return:
    """
    print 'converting contents of {}'.format(filename)
    eg = EveGenie(filename=filename)
    outfile = '{}.settings.py'.format(filename.split('.')[0])
    eg.write_file(outfile)
    print 'settings file written to {}'.format(outfile)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        filename = sys.argv[1]
        if os.path.isfile(filename):
            main(filename)
        else:
            print 'file does not exist'