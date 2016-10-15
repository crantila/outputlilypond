#!/usr/bin/env python
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Filename:               setup.py
# Purpose:                Configuration for installation with setuptools.
#
# Copyright (C) 2016 Christopher Antila
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------
'''
Configuration for installation with setuptools.
'''

from setuptools import setup, Command


setup(
    name = 'OutputLilyPond',
    version = '1.0.0',
    packages = ['outputlilypond'],

    install_requires = (
        'music21 == 2.1.2',
    ),
    tests_require = (
        'pytest',
    ),
    extras_require = {
        'devel': (
            'mock',
            'pytest',
        ),
    },

    # metadata for upload to PyPI
    author = 'Christopher Antila',
    author_email = 'christopher@antila.ca',
    description = 'An HTTP server that executes Python code.',
    license = 'GPLv3+',
    keywords = 'lilypond',
    url = 'https://github.com/crantila/outputlilypond',
    classifiers =[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
)
