#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pendulum
import os
from subprocess import call
from PIL import Image
import re
import requests
from bs4 import BeautifulSoup as bs
import sys

from screeninfo import get_monitors
monitors = get_monitors()
mon_w = re.search(r'monitor\((\d+)x\d+.*', str(monitors[0])).group(1)
mon_h = re.search(r'monitor\(\d+x(\d+).*', str(monitors[0])).group(1)

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
        now = str(pendulum.now().subtract(days=days)\
            .format('DDMMYY', formatter='alternative'))
    link = 'https://cartoon-prod.schibsted.tech/pondus/{}.gif'.format(now)
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
        'Couldn\'t find a comic. Run the script like this \'python {}'
        ' lunch\'. You can chose between {}.'
        .format(os.path.basename(__file__), comics))
    sys.exit()

filedir = os.path.dirname(os.path.abspath(__file__))

# Fetch the newest comic
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

strips = '{}/strips/{}-{}.jpg'.format(filedir, comic, now)
temp_strip = '{}/temp_strip.jpg'.format(filedir)
# Check to see if the latest comic is already in place
if not os.path.exists(strips):
    if not os.path.exists('{}/strip'.format(filedir)):
        call(['mkdir', '{}/strips'.format(filedir)])
    curl = call(['curl', '-f', link, '-o', strips, '--connect-timeout', '3'])
    i = 0
    # If curl get code 28 (timeout), use another random image from same comic
    if curl == 28:
        backup_strip = '{}/strips/{}-{}.jpg'.format(filedir, comic, now)
    # If curl get code 22 (basically a 404), try previous dates
    while curl == 22:
        i += 1
        link = eval('get_{}(days={})[0]'.format(comic, i))
        now = eval('get_{}(days={})[1]'.format(comic, i))
        strips = '{}/strips/{}-{}.jpg'.format(filedir, comic, now)
        curl = call(['curl', '-f', link, '-o', strips])
        continue

# Change the size of the comic strip
img = Image.open(strips)
img_w = int(float(img.size[0] * 1.75))
img_h = int(float(img.size[1] * 1.75))
img = img.resize((img_w, img_h), Image.ANTIALIAS)
img.convert('RGB').save(temp_strip)

# Take screenshot of screen and pixellize it
temp_out = '{}/out.png'.format(filedir)
call(['scrot', temp_out])
scrot = Image.open(temp_out)
scrot_w = int(float(scrot.size[0] * 0.1))
scrot_h = int(float(scrot.size[1] * 0.1))
scrot.save(temp_out)
scrot = scrot.resize((scrot_w, scrot_h), Image.BOX)
scrot_w = int(float(scrot_w * 10))
scrot_h = int(float(scrot_h * 10))
scrot = scrot.resize((scrot_w, scrot_h), Image.BOX)
scrot.save(temp_out)

# Make sure comic is placed on the primary screen
img_w = img.size[0]
img_h = img.size[1]
img_w = img_w // 2
img_h = img_h // 2
placement_w = (int(mon_w) // 2) - img_w
placement_h = (int(mon_h) // 2) - img_h
scrot.paste(img, (placement_w, placement_h))
scrot.save(temp_out)

# Run lock file
call(['i3lock', '-i', temp_out])

# Maintain all the strips: keep max 5 strips at a time
temp_files = sorted(os.listdir('{}/strips'.format(filedir)))
# Make sure that only the images are deleted, not other files/folders
for file in temp_files:
    if '.jpg' not in file:
        temp_files.remove(file)
# Only keep the 5 newest files
if len(temp_files) > 5:
    clean_number = len(temp_files) - 5 - 1
    for i in temp_files[0:clean_number]:
        os.remove('{}/strips/{}'.format(filedir, i))