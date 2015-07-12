# Overview

*infocards* is a small library that can be used to manage information archives in the form of data cards.

The library supports Python 2.7 and 3.4, and is released under the **GPLv2** license.

# Installation

The **recommended** way of installing infocards is by running:

~~~bash
$ pip install infocards
~~~

This will download the necessary dependencies:

- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) ~> 0.5.0
- [peewee](https://github.com/coleifer/peewee) ~> 2.6.3
- [python-Levenshtein](https://github.com/ztane/python-Levenshtein/) ~> 0.12.0

If you want to use MySQL or PostgreSQL for the archive backend, you will also need:

- [psycopg2](http://initd.org/psycopg/) ~> 2.6.1
- [PyMySQL](https://github.com/PyMySQL/PyMySQL) ~> 0.6.6
