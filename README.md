# i3lock-comics
Python script to fetch the newest edition of a comic strip and use it in i3lock. *Highly* inspired by [xkcd-lock](https://github.com/angs/xkcd-lock) by [@angs](https://github.com/angs).

&nbsp;

![Screenshot](https://cloud.githubusercontent.com/assets/265139/21699961/50057f3a-d39e-11e6-9825-b7f561e9cc14.png)

&nbsp;

## Short description

This script gets the latest strip of a comic which is added on top of a pixelated screenshot of your desktop. This image is then used as a background image when running i3lock.

Comics supported:

- Lunch (no)
- Pondus (no)
- xkcd
- Dilbert
- Rocky (no)
- Nemi (no)
- Zelda (no)
- Fagprat (no)
- Dunce (no)
- CommitStrip
- PvP
- VG Cats
- Dinosaur Comics
- Livet Blant Dyrene (no) - new!

## How to use

Run the script by passing a comic as the first variable, like so: `./i3lock_comics.py lunch`
If you don't have any preference, just run `./i3lock_comics.py` to get a random comic.

If you use multiple displays, the script will only place the comic strip on your primary screen.

If the script can't fetch a comic because of connection issues, it will use a previous strip from the same comic, if it can find one in the `strips`-folder.
If there is no net and no cached comic strip available, the script will use XKCD's password-strip as default.

(This seems to be OK according to [Mr. xkcd himself](https://xkcd.com/about):
>"Can we print xkcd in our magazine/newspaper/other publication?"

>"You can post xkcd in your blog (whether ad-supported or not) with no need to get my permission."

But Randall, if I'm mistaken, please let me know.)



## Dependencies:
- i3lock
- scrot
- json
- curl (called by the subprocess module)
- pendulum
- requests
- screeninfo
- Pillow
- beautifulsoup4
- html5lib
