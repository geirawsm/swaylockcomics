#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
from swaylockcomics.__version__ import version

parser = argparse.ArgumentParser()
parser.prog = 'swaylockcomics'
parser.description = 'Lock your screen AND show a comic at the same '\
                     'time, you lucky dog you'
parser.add_argument('--version', '-V',
                    action='version',
                    version='%(prog)s {version}'.
                    format(version=version))
parser.add_argument('--verbose',
                    help='Verbose mode',
                    action='store_true',
                    default=False,
                    dest='verbose')
parser.add_argument('--debug',
                    help='Debug mode',
                    action='store_true',
                    default=False,
                    dest='debug')
parser.add_argument('-l', '--list-comics',
                    help='List the available comics',
                    action='store_true',
                    default=False,
                    dest='list_comics')
parser.add_argument('-c', '--comic',
                    help='Chose what comic to use. '
                    'If no comic is called it will randomize.',
                    action='store',
                    default=False,
                    dest='comic')
parser.add_argument('-f', '--filter',
                    help='Chose what obfuscation filter to use, either '
                         '`pixel`, `morepixel`, `blur`, `moreblur`'
                         '`solid` or `gradient`. '
                         '`solid` is default.',
                    action='store',
                    default='solid',
                    dest='filter')
parser.add_argument('--no-alt-text',
                    help='If getting the xkcd-strip, don\'t add the '
                         'alttext.',
                    action='store_true',
                    default='False',
                    dest='xkcd_no_alttext')
parser.add_argument('-t', '--test',
                    help='Run `swaylockcomics` in testmode',
                    action='store_true',
                    default=False,
                    dest='test')
parser.add_argument('--clean-cache',
                    help='Clean the cache folder and exit',
                    action='store_true',
                    default=False,
                    dest='clean_cache')
parser.add_argument('--delete-cache',
                    help='Delete the cache folder and exit',
                    action='store_true',
                    default=False,
                    dest='delete_cache')
args = parser.parse_args()


if __name__ == '__main__':
    print('These arguments are used:')
    print(vars(args))
