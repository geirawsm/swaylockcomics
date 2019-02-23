#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pendulum
import requests
from bs4 import BeautifulSoup as bs
import json
import re

now = pendulum.now().format('YYYY-MM-DD')
comic_names = []


def comics(comic=False):
    def getcomic_xkcd():
        '''
        Gets the link to the most recent xkcd comic strip.
        '''
        try:
            current_strip = requests.get('https://xkcd.com/info.0.json',
                                         timeout=3)
            current_json = json.loads(current_strip.text)
            link = current_json['img']
        except:
            link = False
        return link

    def getcomic_lunch():
        '''
        Gets the link to the most recent Lunch comic strip.
        '''
        global now
        try:
            req = requests.get('https://www.dagbladet.no/tegneserie/lunch',
                               timeout=3)
            soup = bs(req.content, 'html5lib', from_encoding="utf-8")
            link = soup.find('article', attrs={'class': 'todays'})\
                .find('a', attrs={'class': 'strip-container'})\
                .find('img')['src']
        except:
            link = False
        return link

    def getcomic_pondus():
        '''
        Gets the link to the most recent Pondus comic strip.
        '''
        global now
        try:
            req = requests.get('https://www.dagbladet.no/tegneserie/pondus',
                               timeout=3)
            soup = bs(req.content, 'html5lib', from_encoding="utf-8")
            link = soup.find('article', attrs={'class': 'todays'})\
                .find('a', attrs={'class': 'strip-container'})\
                .find('img')['src']
        except:
            link = False
        return link

    def getcomic_dilbert():
        '''
        Gets the link to the most recent Dilbert comic strip.
        '''
        global now
        try:
            req = requests.get('http://dilbert.com/strip/{}'.format(now),
                               timeout=3)
            soup = bs(req.content, 'html5lib', from_encoding="utf-8")
            strip = soup.find('div', attrs={'class': 'img-comic-container'})
            link = strip.find('img', attrs={'class':
                              'img-responsive img-comic'})['src']
        except:
            link = False
        return link

    def getcomic_nemi():
        '''
        Gets the link to the most recent Nemi comic strip.
        '''
        global now
        try:
            req = requests.get('https://www.dagbladet.no/tegneserie/nemi',
                               timeout=3)
            soup = bs(req.content, 'html5lib', from_encoding="utf-8")
            link = soup.find('article', attrs={'class': 'todays'})\
                .find('a', attrs={'class': 'strip-container'})\
                .find('img')['src']
        except:
            link = False
        return link

    def getcomic_fagprat():
        '''
        Gets the link to the most recent Fagprat comic strip.
        '''
        global now
        try:
            req = requests.get('https://www.dagbladet.no/tegneserie/fagprat',
                               timeout=3)
            soup = bs(req.content, 'html5lib', from_encoding="utf-8")
            link = soup.find('article')\
                .find('a', attrs={'class': 'strip-container'})\
                .find('img')['src']
        except:
            link = False
        return link

    def getcomic_commitstrip():
        '''
        Gets the link to the most recent CommitStrip comic strip.
        '''
        try:
            req = requests.get('http://www.commitstrip.com/en/feed/',
                               timeout=3)
            soup = bs(req.content, 'html5lib', from_encoding="utf-8")\
                .find_all('item')[0]
            link = soup.find('content:encoded').find('img')['src']
        except:
            link = False
        return link

    def getcomic_pvp():
        '''
        Gets the link to the most recent PvP comic strip.
        '''
        global now
        try:
            req = requests.get('http://pvponline.com/comic',
                               timeout=3)
            soup = bs(req.content, 'html5lib', from_encoding="utf-8")
            link = soup.find('section', attrs={'class': 'comic-art'})\
                .find('img')['src']
        except:
            link = False
        return link

    def getcomic_dinosaurcomics():
        '''
        Gets the link to the most recent Dinosaur Comics comic strip.
        '''
        global now
        try:
            req = requests.get('http://www.qwantz.com/rssfeed.php',
                               timeout=3)
            soup = bs(req.content, 'html5lib', from_encoding="iso-5589-1")
            imgs = soup.find_all('item')
            link = re.search(r'img src=\"(.*\.png)', str(imgs[0])).group(1)
        except:
            link = False
        return link

    def getcomic_lilleberlin():
        '''
        Gets the link to the most recent Lille Berlin comic strip.
        '''
        global now
        try:
            url = 'https://www.dagbladet.no/tegneserie/lille-berlin'
            req = requests.get(url, timeout=3)
            soup = bs(req.content, 'html5lib', from_encoding="utf-8")
            link = soup.find('article', attrs={'class': 'todays'})\
                .find('a', attrs={'class': 'strip-container'})\
                .find('img')['src']
        except:
            link = False
        return link

    def getcomic_getfuzzy():
        '''
        Gets the link to the most recent Get Fuzzy comic strip.
        '''
        try:
            req = requests.get('https://www.gocomics.com/getfuzzy/',
                               timeout=3)
            soup = bs(req.content, 'html5lib', from_encoding="utf-8")
            div = soup.find('div', attrs={'class': 'gc-deck--cta-0'})
            imgs = div.find_all('img')
            for img in imgs:
                if 'assets.amuniversal.com/' in img['src']:
                    link = img['src']
                    pass
        except:
            link = False
        return link

    if comic:
        link = eval('getcomic_{}()'.format(comic))
        return link
    else:
        # Get all the available functions that is comic-related
        comic_names = []
        for func in dir():
            if 'getcomic_' in func:
                func = func.replace('getcomic_', '')
                comic_names.append(func)
        return comic_names


def print_comic_list():
    _comics = comics()
    out = 'Comics found: '
    for comic in _comics:
        if comic == _comics[-1]:
            out += 'and \'{}\''.format(comic)
        else:
            out += '\'{}\', '.format(comic)
    print(out)


if __name__ == '__main__':
    print_comic_list()
    