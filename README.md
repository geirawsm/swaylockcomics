# i3lock-comics
Python script to fetch the newest edition of a comic strip and use it in i3lock.

&nbsp;

![Screenshot](https://cloud.githubusercontent.com/assets/265139/21699961/50057f3a-d39e-11e6-9825-b7f561e9cc14.png)

&nbsp;

## Short description

This script gets the latest strip of a comic which is added on top of a pixelated screenshot of your desktop. This image is then used in i3lock.

Comics included:
- Lunch (no)
- Pondus (no)

Comics to be included in later releases:
- xkcd

If you use multiple displays, the script will only place the comic strip on your primary screen.

Only tested in Arch Manjaro i3 4.8.15-1, but should work on others as well as long as the dependencies is in place.


## Dependencies:
- PythonMagick v0.9.16-1
- pendulum v0.8.0
- i3lock v2.8
- scrot v0.8
- screeninfo v0.2.1
- curl (called by the subprocess module)
