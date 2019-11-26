#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path
from io import open
from i3lockcomics.__version__ import version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='i3lockcomics',    # Required
    version=version,
    description=('Gets the newest edition of a comic strip and use it in '
                 'i3lock'),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/armandg/i3lockcomics',
    license='GPL-v3.0',
    author='armandg',
    author_email='armandg@gmail.com',
    entry_points={
        'console_scripts': [
            'i3lockcomics = i3lockcomics.__main__:main'
        ]
    },
    packages=find_packages(),
    install_requires=[
        'screeninfo',
        'requests',
        'pendulum',
        'Pillow',
        'bs4',
        'colorama'
        'html5lib'
    ],
    package_data={
        'i3lockcomics': [
            'xkcd.png',
            'fonts/OpenSans-Italic.ttf'
        ]
    },
)
