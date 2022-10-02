#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path
from io import open
from swaylockcomics.__version__ import version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='swaylockcomics',    # Required
    version=version,
    description=('Gets the newest edition of a comic strip and use it in '
                 'swaylock'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/armandg/swaylockcomics',
    license='GPL-v3.0',
    author='geirawsm',
    author_email='geirawsm@pm.me',
    entry_points={
        'console_scripts': [
            'swaylockcomics = swaylockcomics.__main__:main'
        ]
    },
    packages=find_packages(),
    install_requires=[
        'screeninfo',
        'requests',
        'pendulum',
        'Pillow',
        'bs4',
        'colorama',
        'html5lib'
    ],
    package_data={
        'swaylockcomics': [
            'xkcd.png',
            'fonts/OpenSans-Italic.ttf'
        ]
    },
)
