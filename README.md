# i3lockcomics
Python script to fetch the newest edition of a comic strip and use it in i3lock. *Highly* inspired by [xkcd-lock](https://github.com/angs/xkcd-lock) by [@angs](https://github.com/angs).

&nbsp;

![Screenshot](https://cloud.githubusercontent.com/assets/265139/21699961/50057f3a-d39e-11e6-9825-b7f561e9cc14.png)

&nbsp;

## Short description

This script gets the latest strip of a comic which is added on top of a pixelated screenshot of your desktop. This image is then used as a background image when running i3lock.

Comics supported:

- Bestis (no) (new)
- Calvin & Hobbes
- CommitStrip
- Dilbert
- Dinosaur Comics
- Fagprat (no)
- Get Fuzzy
- Intet Nytt fra Hjemmefronten (no)
- Lunch (no)
- Nemi (no)
- PvP
- xkcd

&nbsp;

## Install

Easy peasy: `pip install i3lockcomics`

&nbsp;

## How to use

Run `i3lockcomics` to lock your screen with i3lock and show a random comic strip. You can also chose a specific comic and use a pixellation distort on your lockscreen instead of the blurring. Check out `i3lockcomics -h` for more info.

If you use multiple displays, the script will only place the comic strip on your primary screen.

If the script can't fetch a comic because of connection issues, it will use a previous strip from the same comic, if it can find one in the `strips`-folder.
If there is no net and no cached comic strip available, the script will use XKCD's password-strip as default.

(This seems to be OK according to [Mr. xkcd himself](https://xkcd.com/about):
>"Can we print xkcd in our magazine/newspaper/other publication?"

>"You can post xkcd in your blog (whether ad-supported or not) with no need to get my permission."

But Randall, if I'm mistaken, please let me know.)

When using xkcd, it will also get the alt-text for the image and paste it underneath the comic.

&nbsp;

## Dependencies:

These dependencies are required besides the modules installed by pip:

- i3lock
- maim
- curl (called by the subprocess module)
