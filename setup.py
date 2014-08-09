# -*- coding: utf-8 -*-
#
# Simple information card archive library
# https://github.com/RMed/infocards
#
# Copyright (C) 2014  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='infocards',
    version='0.2.1',

    description='Simple information card archive library',
    long_description=long_description,

    url='https://github.com/RMed/infocards',

    author='Rafael Medina García',
    author_email='rafamedgar@gmail.com',

    license='LGPLv3',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Database',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='information card archive database',

    packages=['infocards'],

    install_requires=[
        'fuzzywuzzy >= 0.2.1',
        'PyMySQL >= 0.6.2',
        'pg8000 >= 1.9.13',
        'SQLAlchemy >= 0.9.7',
    ],
)
