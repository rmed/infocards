Cards
=====

This document contains some more detailed information on cards.

Structure
---------

*Card* objects have the same structure that is shown in the :doc:`archive` model structure, and hence you can access all of its parameters easily::

    # card = Card(...)

    title = card.title
    description = card.description
    content = card.content
    tags = card.tags
    modified = card.modified

The *title*, *description* and *content* attributes are strings, while *tags* is a list of strings and *modified* is a datetime stamp.


Tag strings and lists
---------------------

Although tags are stored in the archive as a single string, in which each tag is separated by a whitespace, the *Card* object has its tags accesible as a list of strings. This list is alphabetically sorted, in lowercase and does not contain any repeated values (the library will make sure all of the three rules are present when creating a new card).

In order to convert a *tag string* to a *tag list* or viceversa, you can use the following static methods in the :doc:`infocards/card`::

    from infocards.card import Card

    my_tag_string = "This is my tag list and it is awesome"

    my_tag_list = Card.tag_list(my_tag_string)
    # ['and', 'awesome', 'is', 'it', 'list', 'my', 'tag', 'this']

    my_new_tag_string = Card.tag_string(my_tag_list)
    # 'and awesome is it list my tag this'


Modify values of a card
-----------------------

As shown in the :doc:`getting_started` document, editing a card is as simple as changing the value of its attributes. For example::

    from infocards.card import Card

    # card = Card(...)

    # Changing card title
    card.title = 'This is the new title'

    # Changing description
    card.description = 'This is the new description'

    # Deleting content
    card.content = ''

    # Adding a tag
    card.tags.append('python')

It would not make much sense to modify the *modified* attribute, as it is set automatically when inserting or modifying the card.

