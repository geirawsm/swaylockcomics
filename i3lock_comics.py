#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pendulum
import os
from subprocess import call
import PythonMagick
import re
import requests
from bs4 import BeautifulSoup as bs
import sys

from screeninfo import get_monitors
monitors = get_monitors()
monitor_w = re.search(r'monitor\((\d+)x\d+.*', str(monitors[0])).group(1)
monitor_h = re.search(r'monitor\(\d+x(\d+).*', str(monitors[0])).group(1)


def get_xkcd():
    '''
    Gets the most recent xkcd comic strip.
    '''
    try:
        req = requests.get('http://xkcd.com')
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        strip = soup.find('div', attrs={'id': 'comic'})
        link = strip.find('img')['src'].replace('//', '')
    except(ConnectionError):
        link = False
    now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    return link, now


def get_lunch(days=None):
    '''
    Gets the most recent lunch comic strip. If given 'days', it goes that
    number of days back in time.
    '''
    if days is None:
        now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    else:
        now = pendulum.now().subtract(days=days).to_date_string()
    link = 'https://www.tu.no/tegneserier/lunch/?module=TekComics&service'\
        '=image&id=lunch&key={}'.format(now)
    return link, now


def get_pondus(days=None):
    '''
    Gets the most recent pondus comic strip. If given 'days', it goes that
    number of days back in time.
    '''
    if days is None:
        now = pendulum.now().format('DDMMYY', formatter='alternative')
    else:
        now = pendulum.now().subtract(days=days)\
            .format('DDMMYY', formatter='alternative').to_date_string()
    link = 'http://www.bt.no/external/cartoon/pondus/{}.gif'.format(now)
    return link, now


def get_dilbert():
    '''
    Gets the most recent xkcd comic strip.
    '''
    now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    try:
        req = requests.get('http://dilbert.com/strip/{}'.format(now))
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        strip = soup.find('div', attrs={'class': 'img-comic-container'})
        link = strip.find(
            'img',
            attrs={'class': 'img-responsive img-comic'}
        )['src']
    except(ConnectionError):
        link = False
    return link, now


comicname = ['lunch', 'pondus', 'xkcd', 'dilbert']
try:
    comic = str(sys.argv[1])
except:
    comics = ''
    for comic in comicname:
        if comic == comicname[-1]:
            comics += 'and \'{}\''.format(comic)
        else:
            comics += '\'{}\', '.format(comic)
    print(
        'No comic has been entered. Run the script like this \'python {}'
        ' lunch\'. You can chose between {}.'
        .format(os.path.basename(__file__), comics))
    sys.exit()

filedir = os.path.dirname(os.path.abspath(__file__))

# Hent nyeste stripe
if comic == 'lunch':
    link = get_lunch()[0]
    now = get_lunch()[1]
if comic == 'pondus':
    link = get_pondus()[0]
    now = get_pondus()[1]
if comic == 'xkcd':
    link = get_xkcd()[0]
    now = get_xkcd()[1]
if comic == 'dilbert':
    link = get_dilbert()[0]
    now = get_dilbert()[1]

stripe = '{}/striper/{}-{}.jpg'.format(filedir, comic, now)
temp_stripe = '{}/temp_stripe.jpg'.format(filedir)
# Sjekk om siste fil allerede er henta
if not os.path.exists(stripe):
    if not os.path.exists('{}/striper'.format(filedir)):
        call(['mkdir', '{}/striper'.format(filedir)])
    curl = call(['curl', '-f', link, '-o', stripe])
    i = 0
    while curl == 22:
        i += 1
        link = eval('get_{}(days={})[0]'.format(comic, i))
        now = eval('get_{}(days={})[1]'.format(comic, i))
        stripe = '{}/striper/{}-{}.jpg'.format(filedir, comic, now)
        curl = call(['curl', '-f', link, '-o', stripe])
        continue
# Endre på størrelsen på bildet
img = PythonMagick.Image(stripe)
img.resize('175%')
img.write(temp_stripe)

temp_out = '{}/out.png'.format(filedir)
call(['scrot', '-z', temp_out])

scrot = PythonMagick.Image(temp_out)
scrot.scale('10%')
scrot.scale('1000%')
scrot.write(temp_out)

img = PythonMagick.Image(temp_stripe)
img.font('/usr/share/fonts/TTF/LiberationSans-Bold.ttf')
img.annotate(
    'github.com/armandg/i3lock-comics',
    PythonMagick.GravityType.SouthEastGravity
)
img_w = img.size().width()
img_h = img.size().height()
img_w = img_w // 2
img_h = img_h // 2
placement_w = (int(monitor_w) // 2) - img_w
placement_h = (int(monitor_h) // 2) - img_h
scrot.composite(
    img,
    placement_w,
    placement_h,
    PythonMagick.CompositeOperator.SrcOverCompositeOp
)
scrot.write(temp_out)

# Kjør lock-fil
call(['i3lock', '-i', temp_out])

# Vedlikehold av mellomlagring av striper
temp_files = sorted(os.listdir('{}/striper'.format(filedir)))
# Sørg for at man ved sletting kun tar hensyn
# til bildene og ikke andre filer/mapper
for file in temp_files:
    if '.jpg' not in file:
        temp_files.remove(file)
# Behold kun de 5 nyeste stripene
if len(temp_files) > 5:
    clean_number = len(temp_files) - 5 - 1
    for i in temp_files[0:clean_number]:
        os.remove('{}/striper/{}'.format(filedir, i))
