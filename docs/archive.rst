Archive
=======

This document contains some more detailed information on the archive.

Structure
---------

The archive consists of a SQLite database file (you decide the name) with a single table named *cards*. This table has the following columns::

    id (Integer)[primary key] -> row id
    title (Text)[unique] -> card title
    description (Text) -> card description
    content (Text) -> card content
    tags (Text) -> card tags
    modified (DateTime) -> last modification date and time

The *id* and *modified* columns don't need to be taken into account when dealing with the cards. The *id* is there just for convenience, while the *modified* column is automatically set to the date and time in which the card is inserted/modified automatically by the archive.

Connection
----------
.. _pg8000: https://github.com/mfenniak/pg8000
.. _PyMySQL: https://github.com/PyMySQL/PyMySQL

As of version 0.2.0, *infocards* supports archives based on MySQL, PostgreSQL and SQLite databases. You can find the information required for each database type below.

MySQL
#####

*infocards* uses the `PyMySQL`_ module in order to connect to MySQL databases. The parameters for the connection are passed to the *Archive* constructor like so::

    from infocards.archive import Archive

    ar = Archive(
        mysql = DATABASE_HOST,
        user = DATABASE_USER,
        passwd = DATABASE_PASSWORD,
        port = DATABASE_PORT,
        db = DATABASE_NAME)


PostgreSQL
##########

For PostgreSQL databases, the `pg8000`_ module is used. It's parameters are similar to those of the MySQL database::

    from infocards.archive import Archive

    ar = Archive(
        postgresql = DATABASE_HOST
        user = DATABASE_USER,
        passwd = DATABASE_PASSWORD,
        port = DATABASE_PORT,
        db = DATABASE_NAME,
        ssl = USE_SSL) # Boolean value

The main difference is the included *ssl* parameter, which is used to indicate whether the connector should use SSL or not (default is false). Some databases, such as the Heroku ones, may need the SSL set to *True*.


SQLite
######

Connection to SQLite databases is done through the builtin *sqlite* module in Python::

    from infocards.archive import Archive

    ar = Archive(
        sqlite = DATABASE_PATH)

SQLite databases are file-based, therefore you have to specify the absolute path of the file to connect to. If the file does not exist, it may be created by the Archive.

Search
------

The *search* functionality of the archive can be tunned a bit in order to obtain different results. Modyfing the *likelihood* parameter (default is 80) allows you to specify the percentage on which two words are considered similar. The *relevance* represents the percentage (default is 50) of search query words that must be included in the card tag list in order to consider that card as relevant to the search::

    from infocards.archive import Archive

    # ar = Archive(...)

    cards = ar.search("this is my search query", likelihood=80, relevance=50)
