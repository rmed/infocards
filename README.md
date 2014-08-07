infocards
=========

[![PyPI version](https://img.shields.io/pypi/v/infocards.svg)](https://pypi.python.org/pypi/infocards)

A small Python library that allows storing *information cards* in an archive. Supports MySQL, PostgreSQL and SQLite databases.

**Compatible with Python 2 and 3.**

License: **LGPLv3**

Requirements
------------

- [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) >= 0.2.1
- [pg8000](https://github.com/mfenniak/pg8000) >= 1.9.13
- [PyMySQL](https://github.com/PyMySQL/PyMySQL) >= 0.6.2
- [SQLAlchemy](http://www.sqlalchemy.org/) >= 0.9.7


Installation
------------

Installing from source:

```
$ pip install /path/to/archive
```

Installing from the Package Index (recommended):
```
$ pip install infocards
```

The 0.2.1 version of the `fuzzywuzzy` package is not available on PyPI, please install it from its [GitHub repository](https://github.com/seatgeek/fuzzywuzzy).

Documentation
-------------

Documentation is [available online at Read the Docs](http://infocards.readthedocs.org)

In order to build the documentation, you need to have Sphinx installed:

```
$ pip install Sphinx
```

Then go to the *docs* directory and run:

```
$ make html
```

The html documentation will be inside the *docs/_build/html* directory.
