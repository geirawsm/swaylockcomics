#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from subprocess import call
from PIL import Image, ImageFilter
import re
import glob
from random import randint
from i3lockcomics._args import args as args
from i3lockcomics._printv import printv, printd
import i3lockcomics._getcomics as _getcomics
from i3lockcomics._check_network import is_there_internet as is_there_internet
from i3lockcomics._screen import get_screens_info
import i3lockcomics._timing

# Before _ANYTHING_, we check that `i3lock`, `scrot` and `curl` is
# installed
check_i3lock = call(['which', 'i3lock'], stdout=open(os.devnull, 'w'),
                    stderr=open(os.devnull, 'w'))
check_scrot = call(['which', 'scrot'], stdout=open(os.devnull, 'w'),
                   stderr=open(os.devnull, 'w'))
check_curl = call(['which', 'curl'], stdout=open(os.devnull, 'w'),
                  stderr=open(os.devnull, 'w'))
if check_i3lock == 1:
    raise Exception('Could not find that `i3lock` is installed. Please '
                    'make sure that this is installed as it is required'
                    ' for `i3lockcomics` to run.')
if check_scrot == 1:
    raise Exception('Could not find that `scrot` is installed. Please '
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

# Get the folder for the script's cache
cachedir = os.path.expanduser('~/.cache/i3lockcomics')
if not os.path.exists(cachedir):
    call(['mkdir', cachedir])
printv('Setting script directory to \'{}\''.format(cachedir))
sysdir = os.path.dirname(os.path.realpath(__file__))
printv('Getting sys-directory: \'{}\''.format(sysdir))


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


def scrot(strip=False):
    i3lockcomics._timing.midlog('Starting scrot()')
    # Take screenshot of screen and pixelize it, save it
    temp_folder = '{}/temp'.format(cachedir)
    if not os.path.exists(temp_folder):
        call(['mkdir', temp_folder])
    temp_out = '{}/out.png'.format(temp_folder)
    if os.path.exists(temp_out):
        os.remove(temp_out)
    call(['scrot', temp_out])
    scrot = Image.open(temp_out)
    if args.filter == 'morepixel':
        pixel_scrot = 0.05
        pixel_radius = 20
    else:
        pixel_scrot = 0.1
        pixel_radius = 10
    scrot_w = int(float(scrot.size[0] * pixel_scrot))
    scrot_h = int(float(scrot.size[1] * pixel_scrot))
    scrot.save(temp_out)
    obfusc_filters = ['pixel', 'morepixel', 'blur']
    # Pixellize
    if args.filter not in obfusc_filters:
        printv('Chosen filter `{}` is not accepted. Going for `blur` '
               'instead'.format(args.filter))
        args.filter = 'blur'
    if 'pixel' in args.filter:
        scrot = scrot.resize((scrot_w, scrot_h), Image.BOX)
        scrot_w = int(float(scrot_w * pixel_radius))
        scrot_h = int(float(scrot_h * pixel_radius))
        scrot = scrot.resize((scrot_w, scrot_h), Image.BOX)
    # Blur
    elif args.filter == 'blur':
        scrot = scrot.filter(ImageFilter.GaussianBlur(radius=10))
    else:
        printv('Error when chosing filter')
        sys.exit()
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
            scrot.paste(img, (placement_w, placement_h))
            scrot.save(temp_out)
        i3lockcomics._timing.midlog('scrot() done')
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

    backup_strip = _getcomics.get_backup_strip(args.comic, cachedir, sysdir)

    # Only print a list over available comics
    if args.list:
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
    if os.path.exists(strip):
        printv('Found today\'s file already saved, using that instead '
               'of downloading again.')
        call(['i3lock', '-i', scrot(strip)])
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
            if not os.path.exists(strips_folder):
                call(['mkdir', strips_folder])
            curl = call(['curl', '-f', link, '-o', strip, '--connect-timeout',
                         '3', '--max-time', '3'])
            # If curl fails in any way, use the latest strip from same
            # comic.
            # Code 6 from curl is 'Could not resolve host'. Not much to
            # do about this, but the script should have a failsafe
            # Code 28 is a timeout that is triggered based on the
            # `--max-time` variable
            if curl is 6 or curl is 28:
                strip = backup_strip
                strip = backup_strip
            # If curl get code 22 (basically a 404), try previous dates
            if curl == 22:
                i = 0
                while curl is 22:
                    i += 1
                    link = eval('get_{}(days={})[0]'.format(args.comic, i))
                    now = eval('get_{}(days={})[1]'.format(args.comic, i))
                    strip = '{}{}-{}.png'.format(strips_folder,
                                                 args.comic, now)
                    curl = call(['curl', '-f', link, '-o', strip])
                    continue
            if args.comic == 'xkcd':
                strip = _getcomics.xkcd_alttext(strip, extra_info)
        i3lockcomics._timing.midlog('Downloaded comic')

    # Run lock file
    if args.test:
        Image.open(strip).show()
    else:
        call(['i3lock', '-i', scrot(strip)])

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
