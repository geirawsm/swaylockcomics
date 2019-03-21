#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from subprocess import check_call, Popen, PIPE


_xrandr = Popen(['xrandr'], stdout=PIPE, stderr=PIPE, universal_newlines=True)
xrandr, err = _xrandr.communicate()


def get_screens_info():
    global xrandr
    out = {}
    for line in xrandr.split('\n'):
        temp_out = {'state': '', 'primary': '', 'res': '',
                    'offset': ''}
        if 'unknown' in line or 'disconnected' in line:
            continue
        if 'connected' in line:
            try:
                # Try to get following line:
                # DP2-2 connected primary 1920x1080+1600+0 (normal left
                # inverted right x axis y axis) 600mm x 340mm
                re_screen = re.search(r'^([a-zA-Z0-9\-]+)\s+(connected|disconnected)\sprimary\s(\d+x\d+)\+(\d+\+\d+) \(.*', line)
                temp_out['state'] = re_screen.group(2)
                temp_out['primary'] = True
                temp_out['res'] = re_screen.group(3)
                temp_out['offset'] = re_screen.group(4)
            except(AttributeError):
                re_screen = re.search(r'^([a-zA-Z0-9\-]+)\s+(connected|disconnected)\s(\d+x\d+)\+(\d+\+\d+) \(.*', line)
                temp_out['state'] = re_screen.group(2)
                temp_out['primary'] = False
                temp_out['res'] = re_screen.group(3)
                temp_out['offset'] = re_screen.group(4)
            except:
                pass
            out[re_screen.group(1)] = temp_out
    return out


if __name__ == '__main__':
    print(get_screens_info())
