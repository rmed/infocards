infocards
=========

A small Python library that allows storing *information cards* in an archive. Supports MySQL, PostgreSQL and SQLite databases.

Compatible with **Python 2 and 3**

.. _GitHub: https://github.com/RMed/infocards

Source code available on GitHub_

License: **LGPLv3**

Requirements
------------
.. _fuzzywuzzy: https://github.com/seatgeek/fuzzywuzzy
.. _pg8000: https://github.com/mfenniak/pg8000
.. _PyMySQL: https://github.com/PyMySQL/PyMySQL
.. _SQLAlchemy: http://www.sqlalchemy.org/

- fuzzywuzzy_ >= 0.2.1
- pg8000_ >= 1.9.13
- PyMySQL_ >= 0.6.2
- SQLALchemy_ >= 0.9.7

Installation
------------

Installing from source archive file (Windows or UNIX)::

    $ pip install path/to/archive

Installing from the package index (Windows or UNIX)::

    $ pip install infocards

The 0.2.1 version of the fuzzywuzzy_ package is not available on PyPI, please install it from its GitHub repository.

Documentation
-------------


Documentation is available online at Read the Docs http://infocards.readthedocs.org

Building the documentation from source requires that *Sphinx* be installed in the machine. In the **docs** directory::

    $ make html

The documentation will be placed in the **docs/_build/html** directory.
