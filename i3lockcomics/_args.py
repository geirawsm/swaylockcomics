#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from i3lockcomics.__version__ import version

parser = argparse.ArgumentParser()
parser.prog = 'i3lockcomics'
parser.description = 'Lock your screen AND show a comic at the same '\
                     'time, you lucky dog you'
parser.add_argument('--version', '-V',
                    action='version',
                    version='%(prog)s {version}'.
                    format(version=version))
parser.add_argument('-v', '--verbose',
                    help='Verbose mode',
                    action='store_true',
                    default=False,
                    dest='verbose')
parser.add_argument('-c', '--comic',
                    help='Chose what comic to use. '
                    'If no comic is called it will randomize.',
                    action='store',
                    default=False,
                    dest='comic')
parser.add_argument('-f', '--filter',
                    help='Chose what obfuscation filter to use, either '
                         '`pixel` or `blur`. `blur` is default.',
                    action='store',
                    default='blur',
                    dest='filter')
args = parser.parse_args()

if __name__ == '__main__':
    print('These arguments are used:')
    print(vars(args))
