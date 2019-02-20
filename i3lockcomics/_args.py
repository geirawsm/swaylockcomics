#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

parser = argparse.ArgumentParser()
parser.prog = 'i3lockcomics'
parser.description = 'Lock your screen AND show a comic at the same '\
                     'time'
parser.add_argument('-c', '--comic',
                    help='Chose what comic to use. '
                    'If no comic is called it will randomize.',
                    action='store',
                    default=False,
                    dest='comic')
args = parser.parse_args()

if __name__ == '__main__':
    print('These arguments are used:')
    print(vars(args))
