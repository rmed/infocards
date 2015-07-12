infocards
=========

A small Python library for managing **information cards** in an archive.
Supports MySQL, PostgreSQL and SQLite databases for the backend.

**Compatible with Python 2 and 3.**

License: **GPLv2**

**Note: from version 0.5.0 and onwards, infocards is not backwards
compatible.**

Requirements
============

Basic requirements (installed automatically with ``pip``) are:

-  `fuzzywuzzy <https://github.com/seatgeek/fuzzywuzzy>`__ 0.5.0
-  `peewee <https://github.com/coleifer/peewee>`__ 2.6.3
-  `python-Levenshtein <https://github.com/ztane/python-Levenshtein/>`__
   0.12.0

If you want to use MySQL or PostgreSQL for the backend, you will also
need:

-  `psycopg2 <http://initd.org/psycopg/>`__ 2.6.1
-  `PyMySQL <https://github.com/PyMySQL/PyMySQL>`__ 0.6.6

Installation
============

Installing from source:

::

    $ setup.py install

Installing from the Package Index (recommended):

::

    $ pip install infocards

Documentation
=============

Documentation is `available online <http://infocards.readthedocs.org>`__
and contains the API reference as well as examples.

You may also build the documentation source in the ``docs/`` directory using MKDocs.
