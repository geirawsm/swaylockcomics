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
mon_w = 0
mon_h = 0
# Check which monitor is biggest
for monitor in monitors:
    temp_mon_w = int(re.search(r'monitor\((\d+)x\d+.*',
                     str(monitor)).group(1))
    temp_mon_h = int(re.search(r'monitor\(\d+x(\d+).*',
                     str(monitor)).group(1))
    if temp_mon_w > mon_w:
        mon_w = temp_mon_w
    if temp_mon_h > mon_h:
        mon_h = temp_mon_h
# Setting max width for strips
max_screen_estate = 0.8
max_w = int(int(mon_w) * max_screen_estate)
max_h = int(int(mon_h) * max_screen_estate)


def ratio_check(img_w, img_h):
    '''Calculate if the image is too wide or high. Based on this, find out how
    much the image has to be resized for it to fit within the maximum screen
    estate.'''
    global max_w
    global max_h
    img_w = int(img_w * 1.75)
    img_h = int(img_h * 1.75)
    ratio = min(max_w / img_w, max_h / img_h)
    if ratio < 1:
        img_w = int(img_w * ratio)
        img_h = int(img_h * ratio)
    return img_w, img_h


def getcomic_xkcd():
    '''
    Gets the most recent xkcd comic strip.
    '''
    try:
        req = requests.get('http://xkcd.com')
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        strip = soup.find('div', attrs={'id': 'comic'})
        link = strip.find('img')['src'].replace('//', '')
    except(requests.ConnectionError):
        link = False
    now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    return link, now


def getcomic_lunch():
    '''
    Gets the most recent Lunch comic strip.
    '''
    try:
        req = requests.get('http://www.dagbladet.medialaben.no'
                           '/tegneserie/lunch/')
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        link = soup.find('a', attrs={'class': 'strip-container'})\
            .find('img')['src']
    except(requests.ConnectionError):
        link = False
    now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    return link, now


def getcomic_pondus():
    '''
    Gets the most recent Rocky comic strip.
    '''
    try:
        req = requests.get('http://www.dagbladet.medialaben.no'
                           '/tegneserie/pondus/')
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        link = soup.find('a', attrs={'class': 'strip-container'})\
            .find('img')['src']
    except(requests.ConnectionError):
        link = False
    now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    return link, now


def getcomic_dilbert():
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
    except(requests.ConnectionError):
        link = False
    return link, now


def getcomic_rocky():
    '''
    Gets the most recent Rocky comic strip.
    '''
    try:
        req = requests.get('http://www.dagbladet.medialaben.no'
                           '/tegneserie/rocky/')
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        link = soup.find('a', attrs={'class': 'strip-container'})\
            .find('img')['src']
    except(requests.ConnectionError):
        link = False
    now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    return link, now


def getcomic_nemi():
    '''
    Gets the most recent Nemi comic strip.
    '''
    try:
        req = requests.get('http://www.dagbladet.medialaben.no'
                           '/tegneserie/nemi/')
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        link = soup.find('a', attrs={'class': 'strip-container'})\
            .find('img')['src']
    except(requests.ConnectionError):
        link = False
    now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    return link, now


def getcomic_zelda():
    '''
    Gets the most recent Zelda comic strip.
    '''
    try:
        req = requests.get('http://www.dagbladet.medialaben.no'
                           '/tegneserie/zelda-lille-berlin/')
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        link = soup.find('a', attrs={'class': 'strip-container'})\
            .find('img')['src']
    except(requests.ConnectionError):
        link = False
    now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    return link, now


def getcomic_fagprat():
    '''
    Gets the most recent Fagprat comic strip.
    '''
    try:
        req = requests.get('http://www.dagbladet.medialaben.no'
                           '/tegneserie/fagprat/')
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        link = soup.find('a', attrs={'class': 'strip-container'})\
            .find('img')['src']
    except(requests.ConnectionError):
        link = False
    now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    return link, now


def getcomic_dunce():
    '''
    Gets the most recent Dunce comic strip.
    '''
    try:
        req = requests.get('http://www.dagbladet.medialaben.no'
                           '/tegneserie/dunce/')
        soup = bs(req.content, 'html5lib', from_encoding="utf-8")
        link = soup.find('a', attrs={'class': 'strip-container'})\
            .find('img')['src']
    except(requests.ConnectionError):
        link = False
    now = pendulum.now().format('YYYY-MM-DD', formatter='alternative')
    return link, now


def all_comic_names(functions):
    comicnames = []
    for function in functions:
        if re.search('^getcomic_(.*)', function):
            comicnames.append(re.search('^getcomic_(.*)', function).group(1))
    return comicnames


def scrot(strip=False):
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

    if strip:
        if not os.path.exists(strip):
            pass
        else:
            # Change the size of the comic strip
            img = Image.open(strip)
            img_w = int(img.size[0])
            img_h = int(img.size[1])
            new_size = ratio_check(img_w, img_h)
            img_w = new_size[0]
            img_h = new_size[1]
            img = img.resize((img_w, img_h), Image.ANTIALIAS)
            img.convert('RGB').save(temp_strip)
            # Make sure comic is placed on the primary screen
            img_w = img.size[0]
            img_h = img.size[1]
            img_w = img_w // 2
            img_h = img_h // 2
            placement_w = (int(mon_w) // 2) - img_w
            placement_h = (int(mon_h) // 2) - img_h
            scrot.paste(img, (placement_w, placement_h))
            scrot.save(temp_out)
    return temp_out

# Fetch the newest comic
try:
    comic = str(sys.argv[1])
    link = eval('getcomic_{}()[0]'.format(comic))
    now = eval('getcomic_{}()[1]'.format(comic))
except:
    comicnames = all_comic_names(dir())
    comics = ''
    for comic in comicnames:
        if comic == comicnames[-1]:
            comics += 'and \'{}\''.format(comic)
        else:
            comics += '\'{}\', '.format(comic)
    print('Couldn\'t find a comic. Run the script like this \'python {}'
          ' lunch\'. You can chose between {}.'
          .format(os.path.basename(__file__), comics))
    sys.exit()

filedir = os.path.dirname(os.path.abspath(__file__))
strips_folder = '{}/strips/'.format(filedir)
temp_files = sorted(os.listdir(strips_folder))
try:
    backup_strip = temp_files[0]
    for i in temp_files:
        if comic in i:
            backup_strip = i
            break
except:
    backup_strip = ''

strip = '{}{}-{}.jpg'.format(strips_folder, comic, now)
temp_strip = '{}/temp_strip.jpg'.format(filedir)
if link is False:
    strips = backup_strip
else:
    # Check to see if the latest comic is already in place
    if not os.path.exists(strip):
        if not os.path.exists(strips_folder):
            call(['mkdir', strips_folder])
        else:
            curl = call(['curl', '-f', link, '-o', strip, '--connect-timeout', '3'])
            if curl == 6:
                print('Couldn\'t resolve the host for download comic. Is your '
                      'internet ok?')
                call(['i3lock', '-i', scrot()])
            # If curl get code 28 (timeout), use the latest strip from same comic
            if curl == 28:
                strip = backup_strip
            # If curl get code 22 (basically a 404), try previous dates
            i = 0
            while curl == 22:
                i += 1
                link = eval('get_{}(days={})[0]'.format(comic, i))
                now = eval('get_{}(days={})[1]'.format(comic, i))
                strip = '{}{}-{}.jpg'.format(strips_folder, comic, now)
                curl = call(['curl', '-f', link, '-o', strips])
                continue

temp_out = scrot(strip)

# Run lock file
call(['i3lock', '-i', scrot(strip)])

# Maintain all the strips: keep max 5 strips at a time
# Make sure that only the images are deleted, not other files/folders
for file in temp_files:
    if '.jpg' not in file:
        temp_files.remove(file)
# Only keep the 5 newest files
if len(temp_files) > 5:
    clean_number = len(temp_files) - 5 - 1
    for i in temp_files[0:clean_number]:
        os.remove('{}{}'.format(strips_folder, i))
