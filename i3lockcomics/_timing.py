#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import atexit
from time import time, strftime, localtime
from datetime import timedelta


def secondsToStr(elapsed=None):
    if elapsed is None:
        return strftime('%Y-%m-%d %H:%M:%S', localtime())
    else:
        return str(timedelta(seconds=elapsed))


def log(s, elapsed=None):
    line = '{}'.format('=' * 40)
    print(line)
    print(secondsToStr(), '-', s)
    if elapsed:
        print('Elapsed time:', elapsed)
    print(line)
    print()


def endlog():
    end = time()
    elapsed = end - start
    log('End Program', secondsToStr(elapsed))


start = time()
atexit.register(endlog)
log('Start Program')


if __name__ == '__main__':
    pass