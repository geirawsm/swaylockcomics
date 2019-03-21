#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from i3lockcomics._args import args
from colorama import init, Fore, Style
init(autoreset=True)


def printv(text):
    '''
    Instead of normal print, print to stdout with a specific format to
    differentiate the verbose text from normal text
    '''
    if args.verbose:
        print('{color}{style}{}{reset}'.format(text,
                                               color=Fore.YELLOW,
                                               style=Style.BRIGHT,
                                               reset=Style.RESET_ALL))


def printd(text):
    '''
    Instead of normal print, print to stdout with a specific format to
    differentiate the verbose text from normal text
    '''
    if args.debug:
        print('{color}{style}{}{reset}'.format(text,
                                               color=Fore.RED,
                                               style=Style.BRIGHT,
                                               reset=Style.RESET_ALL))
