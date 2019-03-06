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
from i3lockcomics._printv import printv
import i3lockcomics._getcomics as _getcomics
from i3lockcomics._check_network import is_there_internet as is_there_internet

if args.verbose:
    import i3lockcomics._timing

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

# Before _ANYTHING_, we check that `i3lock` is installed
check_i3lock = call(['which', 'i3lock'], stdout=open(os.devnull, 'w'),
                    stderr=open(os.devnull, 'w'))
if check_i3lock == 1:
    raise Exception('Could not find that `i3lock` is installed. Please '
                    'make sure that this is installed as it is required'
                    ' for `i3lockcomics` to run.')
    sys.exit()

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
    # Take screenshot of screen and pixelize it, save it
    temp_folder = '{}/temp'.format(cachedir)
    if not os.path.exists(temp_folder):
            call(['mkdir', temp_folder])
    temp_out = '{}/out.png'.format(temp_folder)
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
            scrot.paste(img, (placement_w, placement_h))
            scrot.save(temp_out)
    return temp_out


def main():
    global args, _getcomics
    # Check if the script can get internet connection
    if not is_there_internet:
        args.offline
        printv('Could\'t get internet connection.')
    now = _getcomics.now
    if args.list:
        _getcomics.print_comic_list()
        sys.exit()
    # Fetch the newest comic, either the chosen one or a random one
    if not args.comic:
        args.comic = _getcomics.comics()[randint(0, len(
            _getcomics.comics()) - 1)]
        printv('Comic not chosen, but randomly chose `{}`'.format(args.comic))
    link = _getcomics.comics(comic=args.comic)
    printv('Comic: {}\nGot link: {}'.format(args.comic, link))

    # Set folder for the images saved by the script
    strips_folder = '{}/strips/'.format(cachedir)
    all_strips_files = glob.glob('{}/strips/*'.format(cachedir))

    backup_strip = _getcomics.get_backup_strip(args.comic, cachedir, sysdir)

    # Set filename for comic strip to be saved
    strip = '{}{}-{}.jpg'.format(strips_folder, args.comic, now)

    # Make a failsafe in case it can't fetch a comic strip at all
    if link is False:
        printv('Comic returns `False` in link. Using XKCD-fallback strip')
        strip = backup_strip
    else:
        # ...but if all is ok, continue.
        # Check to see if the latest comic is already in place
        if not os.path.exists(strip):
            if not os.path.exists(strips_folder):
                call(['mkdir', strips_folder])
            curl = call(['curl', '-f', link, '-o', strip, '--connect-timeout',
                         '5', '--max-time', '5'])
            # If curl fails in any way, use the latest strip from same
            # comic.
            # Code 6 from curl is 'Could not resolve host'. Not much to
            # do about this, but the script should have a failsafe
            # Code 28 is a timeout that is triggered based on the
            # `--max-time` variable
            if curl is 6 or curl is 28:
                strip = backup_strip
                # Debug
                printv('curl error 6: using XKCD-fallback strip')
                strip = backup_strip
            # If curl get code 22 (basically a 404), try previous dates
            if curl == 22:
                # Debug
                print('curl error 22: 404, check earlier strips')
                i = 0
                while curl is 22:
                    i += 1
                    link = eval('get_{}(days={})[0]'.format(args.comic, i))
                    now = eval('get_{}(days={})[1]'.format(args.comic, i))
                    strip = '{}{}-{}.jpg'.format(strips_folder,
                                                 args.comic, now)
                    curl = call(['curl', '-f', link, '-o', strip])
                    continue

    # Run lock file
    call(['i3lock', '-i', scrot(strip)])

    # Maintain all the strips: keep max 5 strips at a time
    # Make sure that only the images are deleted, not other files/folders
    for file in strips_files:
        if '.jpg' not in file:
            strips_files.remove(file)
    # Only keep the 5 newest files
    if len(strips_files) > 5:
        clean_number = len(strips_files) - 5 - 1
        for i in strips_files[0:clean_number]:
            os.remove(i)


if __name__ == '__main__':
    main()
