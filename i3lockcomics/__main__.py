#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from subprocess import call
from PIL import Image, ImageFilter
import re
import glob
from random import randint
import imghdr
import inspect
import requests
from i3lockcomics._args import args as args
from i3lockcomics._printv import printv, printd
import i3lockcomics._getcomics as _getcomics
from i3lockcomics._check_network import is_there_internet as is_there_internet
from i3lockcomics._screen import get_screens_info
import i3lockcomics._timing
import hashlib


def download_file(link, strip):
    if link[0:4] != 'http':
        link = 'https://{}'.format(link)
    try:
        with requests.get(link, stream=True, timeout=(1, 3)) as r:
            r.raise_for_status()
            with open(strip, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    f.write(chunk)
        return True
    except(requests.exceptions.ConnectionError):
        return False


def copy_fallback_xkcd():
    '''
    Check if the fallback strip is in the temp-folder. If it's not,
    copy the original from the module folder.
    If the file is present, do a checksum comparison of both files, and
    if the temp-file deviates, replace it with the original.
    '''
    global sysdir, cachedir
    sys_xkcd = '{}/xkcd.png'.format(sysdir)
    cache_xkcd = '{}/temp/xkcd.png'.format(cachedir)
    if not os.path.exists(cache_xkcd) or\
            not md5(sys_xkcd) != md5(cache_xkcd):
        call(['cp', sys_xkcd, cache_xkcd])


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


# Before _ANYTHING_, we check that `i3lock`, `maim` and `curl` is
# installed
check_i3lock = call(['which', 'i3lock'], stdout=open(os.devnull, 'w'),
                    stderr=open(os.devnull, 'w'))
check_maim = call(['which', 'maim'], stdout=open(os.devnull, 'w'),
                  stderr=open(os.devnull, 'w'))
check_curl = call(['which', 'curl'], stdout=open(os.devnull, 'w'),
                  stderr=open(os.devnull, 'w'))
if check_i3lock == 1:
    raise Exception('Could not find that `i3lock` is installed. Please '
                    'make sure that this is installed as it is required'
                    ' for `i3lockcomics` to run.')
if check_maim == 1:
    raise Exception('Could not find that `maim` is installed. Please '
                    'make sure that this is installed as it is required'
                    ' for `i3lockcomics` to run.')
if check_curl == 1:
    raise Exception('Could not find that `curl` is installed. Please '
                    'make sure that this is installed as it is required'
                    ' for `i3lockcomics` to run.')


# Get screen info
screens = get_screens_info()
for screen in screens:
    if screens[screen]['primary']:
        printd('Found primary screen {}'.format(screen))
        offset = screens[screen]['offset'].split('+')
        res = screens[screen]['res'].split('x')
        mon_w = res[0]
        mon_h = res[1]
        offset_w = int(offset[0])
        offset_h = int(offset[1])
        pass
# Setting max width for strips
max_screen_estate = 0.8
max_w = int(int(mon_w) * max_screen_estate)
max_h = int(int(mon_h) * max_screen_estate)
printd('Got max width {} and max height {} for comic'.format(max_w, max_h))

# Create necessary folders
cachedir = os.path.expanduser('~/.cache/i3lockcomics')
if not os.path.exists(cachedir):
    call(['mkdir', cachedir])
printv('Setting script directory to \'{}\''.format(cachedir))
sysdir = os.path.dirname(os.path.realpath(__file__))
printv('Getting sys-directory: \'{}\''.format(sysdir))
temp_folder = '{}/temp'.format(cachedir)
if not os.path.exists(temp_folder):
    call(['mkdir', temp_folder])

# Copying the XKCD fallback comic to .cache-folder
copy_fallback_xkcd()


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


def screenshot(strip=False):
    '''
    Take screenshot of screen and pixelize it, save it
    '''
    def bg_obfuscation(image_in):
        '''
        Take a pillow_object and obfuscate it as wanted
        '''
        obfusc_filters = ['pixel', 'morepixel', 'blur', 'moreblur']
        if 'pixel' in args.filter:
            if args.filter == 'pixel':
                pixel_size = 0.1
                pixel_radius = 10
            elif args.filter == 'morepixel':
                pixel_size = 0.05
                pixel_radius = 20
            image_in_w = int(float(image_in.size[0] * pixel_size))
            image_in_h = int(float(image_in.size[1] * pixel_size))
            image_in.save(temp_out)
            image_in = image_in.resize((image_in_w, image_in_h), Image.BOX)
            image_in_w = int(float(image_in_w * pixel_radius))
            image_in_h = int(float(image_in_h * pixel_radius))
            image_in = image_in.resize((image_in_w, image_in_h), Image.BOX)
        # Blur
        elif 'blur' in args.filter:
            if args.filter == 'blur':
                blur_radius = 10
            elif args.filter == 'moreblur':
                blur_radius = 20
            image_in = image_in.filter(
                ImageFilter.GaussianBlur(radius=blur_radius)
            )
        # If args.filter is not recognized, use blur
        elif args.filter not in obfusc_filters:
            printv('Filter `{}` is not recognized'.format(args.filter))
            printv('Using `blur` as standard')
            args.filter = 'blur'
        return image_in

    i3lockcomics._timing.midlog('Starting `{}`'.format(inspect.stack()[0][3]))
    temp_out = '{}/out.png'.format(temp_folder)
    # If tempfile already exist, remove it and take new screenshot
    if os.path.exists(temp_out):
        os.remove(temp_out)
    call(['maim', temp_out])
    temp_in = Image.open(temp_out)
    temp_obfuscated = bg_obfuscation(temp_in)
    temp_obfuscated.save(temp_out)

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
            img.convert('RGB').save(strip)
            # Make sure comic is placed on the primary screen
            img_w = img.size[0]
            img_h = img.size[1]
            img_w = img_w // 2
            img_h = img_h // 2
            placement_w = (int(mon_w) // 2) - img_w
            placement_h = (int(mon_h) // 2) - img_h
            # Add offset
            placement_w += offset_w
            placement_h += offset_h
            temp_obfuscated.paste(img, (placement_w, placement_h))
            temp_obfuscated.save(temp_out)
        i3lockcomics._timing.midlog('`{}` done'.format(inspect.stack()[0][3]))
    return temp_out


def sort_filename_by_date(filename):
    '''
    Dirty hack but ok:
    Get a date from a filename in a highly specific format that
    this script makes and return it
    '''
    try:
        _date = re.search(r'.*-(\d{4})-(\d{2})-(\d{2}).*', filename)
        year = _date.group(1)
        month = _date.group(2)
        day = _date.group(3)
        return year, month, day
    except(AttributeError):
        return (str(0), str(0), str(0))


def main():
    global args, _getcomics
    now = _getcomics.now
    # Set folder for the images saved by the script
    strips_folder = '{}/strips/'.format(cachedir)
    if not os.path.exists(strips_folder):
        call(['mkdir', strips_folder])
    backup_strip = _getcomics.get_backup_strip(args.comic, cachedir, sysdir)

    # Only print a list over available comics
    if args.list:
        # Do a test of all the comics
        if args.test:
            for comic in _getcomics.comics():
                link = _getcomics.comics(comic)['link']
                print('{}: {}'.format(comic, link))
            sys.exit()
        _getcomics.print_comic_list()
        sys.exit()
    
    # Fetch the newest comic, either the chosen one or a random one
    i3lockcomics._timing.midlog('Getting comic...')
    if not args.comic:
        args.comic = _getcomics.comics()[randint(0, len(
            _getcomics.comics()) - 1)]
        printv('Comic not chosen, but randomly chose `{}`'.format(args.comic))
    # Set filename for comic strip to be saved
    strip = '{}{}-{}.jpg'.format(strips_folder, args.comic, now)
    # If filename exists, and it is a valid image file, use that
    # instead of redownloading
    if os.path.exists(strip):
        printv('Strip already exists...')
        image_check = imghdr.what(strip)
        if image_check is None:
            printv('...and something is wrong with it. Redownloading.')
            os.remove(strip)
        else:
            printv('...and it is good! Using that file instead of '
                   'redownloading.')
            call(['i3lock', '-i', screenshot(strip)])
            sys.exit()
    if is_there_internet:
        _comics_in = _getcomics.comics(comic=args.comic)
        link = _comics_in['link']
        extra_info = _comics_in['extra_info']
    else:
        link = False
        extra_info = False
    printv('Comic: {}\nGot link: {}\nGot `extra_info`: {}'
           .format(args.comic, link, extra_info))

    # Make a failsafe in case it can't fetch a comic strip at all
    if link is False:
        printv('Comic returns `False` in link. Using XKCD-fallback strip')
        strip = backup_strip
    else:
        i3lockcomics._timing.midlog('Starting check comic or download')
        # ...but if all is ok, continue.
        # Check to see if the latest comic is already in place
        if not os.path.exists(strip):
            dl_comic = download_file(link, strip)
            if dl_comic is False:
                # First try earlier dates
                i = 0
                while dl_comic is False:
                    i += 1
                    link = eval('get_{}(days={})[0]'.format(args.comic, i))
                    now = eval('get_{}(days={})[1]'.format(args.comic, i))
                    strip = '{}{}-{}.png'.format(strips_folder,
                                                 args.comic, now)
                    dl_comic = download_file(link, strip)
                    # We will only try three times before giving up
                    if i == 3:
                        strip = backup_strip
                        break

            if args.comic == 'xkcd':
                strip = _getcomics.xkcd_alttext(strip, extra_info)
        i3lockcomics._timing.midlog('Downloaded comic')

    # Run lock file
    if args.test:
        Image.open(strip).show()
    else:
        call(['i3lock', '-i', screenshot(strip)])

    # Maintain all the strips: keep max 5 strips at a time
    # Make sure that only the images are deleted, not other files/folders
    printv('Removing non-jpg-files...')
    all_strips_files = glob.glob('{}/strips/*'.format(cachedir))
    for file in all_strips_files:
        if '.jpg' not in file:
            printv('Deleting `{}`'.format(file))
            os.remove(file)
    # Only keep the 5 newest files
    printv('Keeping only the ten last images...')
    all_strips_files = sorted(all_strips_files,
                              key=sort_filename_by_date,
                              reverse=True)
    printd('Found {} images in `all_strips_files`'
           .format(len(all_strips_files)))
    if len(all_strips_files) > 10:
        clean_number = len(all_strips_files) - 10
        printd('number of images in `all_strips_files`: {}'.
               format(len(all_strips_files)))
        printd('clean_number: {}'.format(clean_number))
        for file in all_strips_files[9:-1]:
            printd('Deleting this file: {}'.format(file))
            os.remove(file)


if __name__ == '__main__':
    main()
