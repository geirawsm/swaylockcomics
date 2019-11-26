#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
import i3lockcomics._timing


def is_there_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    i3lockcomics._timing.midlog('Checking network connection')
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except Exception as ex:
        print(ex.message)
        return False


if __name__ == '__main__':
    print(is_there_internet())
