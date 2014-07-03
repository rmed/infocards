Getting Started
=================

.. _pip: https://pypi.python.org/pypi/pip
.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _setuptools: https://pypi.python.org/pypi/setuptools

This document will show you a quick introduction on how to easily install and use the infocards library.

Installation
------------

*infocards* has been tested on **Python 2.7** and **3.4**, although it should work in other versions such as **2.5**. The library can be installed from source by downloading and extracting the compressed file and then running::

    $ python setup.py install

`setuptools`_ will also try to download the additional libraries required in the code (`SQLAlchemy`_).

However, the **recommended installation method** is to directly use `pip`_ to download and install the package (including dependencies) from the package index::

    $ pip install infocards


Creating an archive
-------------------

Once installed, creating a new archive (or connecting to an already existing one) is as easy as this::

    from infocards import Archive

    ar = Archive('myarchive.dat') # Be creative with your archive name!
    ar.create_archive() # Use this only if you are creating an archive from scratch

Done, your archive is ready and awaiting its cards. Also note that the library is based around an SQLite database, so you can have as many different archive database files as you want.


Inserting a new card
--------------------

:doc:`cards` contain very little information, so creating a new card is very easy::

    from infocards import Archive

    ar = Archive('myarchive.dat')

    title = 'This is my new card'
    description = 'What a nice little description'
    content = 'You can be as creative as you want when writing your content!!'
    tags = 'tags are simply words separated by a whitespace'

    are.new_card(title, description, content, tags)

You must take into account, however, that there cannot be two cards with the same title in the archive.


Retrieving a card
-----------------

:doc:`cards` have a unique title. In order to get the information on a specific card, simply ask the archive for that title::

    from infocards import Archive

    ar = Archive('myarchive.dat')

    my_card = ar.get_card('This is my new card') # If a card with that title exists, now you can access all its information


Retrieving a list of all the cards
----------------------------------

If you want a complete list of all the :doc:`cards` in the archive, simply do::

    from infocards import Archive

    ar = Archive('myarchive.dat')

    all_cards = ar.all()


Updating a card
---------------

:doc:`cards` can also be modified/updated easily so that you can add that information you forgot when creating the card!::

    from infocards import Archive

    ar = Archive('myarchive.dat')

    my_card = ar.get_card('This is my new card') # Need to modify the original card
    my_card.title = 'I like this title better' # You can even change the title!
    my_card.content = 'Cards are easy to use'

    ar.update_card('This is my new card', my_card) # Card updated!

As renaming a card is possible, modifications require the old title as well as the new card information.


Removing a card
---------------

Of course, you can even remove :doc:`cards` from your archive. Simply use the card title, exactly the same as when retrieving a card::

    from infocards import Archive

    ar = Archive('myarchive.dat')

    ar.remove_card('This is my new card') # Gone!


Searching for cards
-------------------

Having to know all the card titles by heart can (and will) become frustrating. For that reason, the library includes a simple search functionality::

    from infocards import Archive

    ar = Archive('myarchive.dat')

    # Search for 'Python' using submatch algorithm
    result = ar.search('Python') 

    # Search for 'Python' using distance algorithm
    result = ar.search('Python', alg='distance')

    # In both cases, the result is a list of Card objects

For more information on the search algorithms, have a look at the :doc:`cards` document.
