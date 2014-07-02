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

Search
------

As noted in the :doc:`getting_started` document, there are two simple search algorithms. The two have in common that a **complete tag list** is generated from the *title* and the *tags* of the card and then compares the search query with that. Which algorithm to choose is completely up to the user.

Submatch
########

This is the simplest algorithm and the default when performing a search. After obtaining the lists, **compares pairs of elements in the two lists** by checking if either of them is **contained** within the other. For instance:

===================== ================
Match                 Don't match
===================== ================
(tag, tags)           (tag, python)
(tag, taglist)        (python, potato)
(python, superpython) (i, robot)
(i, list)             (potato, robot)
===================== ================

As you can see, this works nicely for general cases (such as *tag* and *tags*), but see that *i* matches *list* because that **i** in the middle.

If there is a match in the pair, the archive adds the term from the query into a **list of common words** and continues with the next. In order to consider the current card as a match, the **common list should have a length of at least half of the query terms**. If that is the case, the *Card* object is added to the result list.

Distance
########

.. _Levenshtein distance: http://en.wikipedia.org/wiki/Levenshtein_distance

After obtaining the lists, this algorithm computes the `Levenshtein distance`_ of pairs of elements in the two lists. In order to use this algorithm, you need to specify it when calling the *search()* method::

    from infocards import Archive

    ar = Archive('myarchive.dat')

    result = ar.search('Python', alg='distance', dist=1)

The **dist** parameter is used to specify what is the maximum distance that can be considered a match (default is 1). An example with match distance 1:

===================== ================
Match                 Don't match
===================== ================
(tag, tags)           (tag, python)
(cpython, python)     (tag, taglist)
(cat, bat)            (a, aaaa)
(a, 2)                (potato, robot)
===================== ================

As you can see, the `Levenshtein distance`_ shows the number of edits required in a string to make it equal to the other. This is very useful in cases such as comparing singular and plural words, but a drawback is that words that are one character long will always show a match with other words that have the same length.
