#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''`_timing` gives several functions to process time in any fashion'''

import atexit
from time import time, strftime, localtime
from datetime import timedelta
from i3lockcomics._args import args


def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime('%Y-%m-%d %H:%M:%S', localtime())
    else:
        return str(timedelta(seconds=elapsed))


def log(_text, elapsed=None):
    out = ''
    temp_out = ''
    if 'start' not in _text.lower():
        out += '\n'
    temp_out += '{time} - {_text}'.format(time=secondsToStr(), _text=_text)
    if elapsed:
        temp_out += ' - elapsed time: {}\n'.format(elapsed)
    else:
        temp_out += '\n'
    line = '{}'.format('=' * len(temp_out))
    out += '{line}\n'.format(line=line)
    out += temp_out
    out += '{line}'.format(line=line)
    if 'end' not in _text.lower():
        out += '\n'
    print(out)


def endlog():
    end = time()
    elapsed = end - start
    log('End Program', secondsToStr(elapsed))


def midlog(text):
    if args.debug:
        end = time()
        elapsed = end - start
        log(text, secondsToStr(elapsed))


if args.debug:
    start = time()
    atexit.register(endlog)
    log('Start Program')


if __name__ == '__main__':
    pass
