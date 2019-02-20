#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from i3lockcomics._args import args


def printv(text):
    '''
    Instead of normal print, print to stdout with a specific format to
    differentiate the verbose text from normal text
    '''
    if args.verbose:
        print(text)
