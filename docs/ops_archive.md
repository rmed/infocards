The following examples suppose a SQLite connection, however they are exactly the same for the other database types:

~~~python
from infocards.archive import Archive

arc = Archive(
    db_name='/path/to/db',
    db_type='sqlite',
)
~~~

---

## Creating a card

Make sure that you use a unique title!

~~~python
my_new_card = ar.new_card(
    'My title',
    'My short description',
    'My main content. Can be very long.',
    'my space separated tags',
    'rmed'
)
~~~

When creating a new card, a `CardObj` instance with the information you entered is returned. Also note that the last argument is completely optional, and if left empty it will default to `'UNKNOWN'`.

---

## Creating a section

Again, make sure you use a unique name!

~~~python
my_new_section = ar.new_section('Section name')
~~~

Similar to [creating a card](#Creating a card), returns a `SectionObj` instance of the newly created section.

---

## Deleting a card

In order to delete a card, you may identify it by `id` which has higher priority,or by `title`:

~~~python
# Deleting a card by id
ar.delete_card(cid=23)

# Deleting a card by title
ar.delete_card(title='My title')

# You can also specify both, but id will take preference
ar.delete_card(title='My title', cid=23)
~~~

Deleting a card will also delete all the `Relations` the card appeared in.

---

## Deleting a section

Pretty similar to [deleting a card](#Deleting a card), but instead of `title`, you can identify a section by `name`:

~~~python
# Deleting a section by id
ar.delete_section(sid=23)

# Deleting a card by title
ar.delete_section(name='My title')

# You can also specify both, but id will take preference
ar.delete_section(name='My title', sid=23)
~~~

Deleting a section will also delete all the `Relations` the section appeared in.

---

## Adding a card to a section

~~~python
# Card and Section can be specified by id
ar.add_card_to_section(self, cid=23, sid=2)

# or by title and name
ar.add_card_to_section(self, ctitle='My title', sname='Section name')
~~~

---

## Removing a card from a section

Pretty similar to the [addition case](#Adding a card to a section):

~~~python
# Card and Section can be specified by id
ar.remove_card_from_section(self, cid=23, sid=2)

# or by title and name
ar.remove_card_from_section(self, ctitle='My title', sname='Section name')
~~~

---

## Getting a list of cards

~~~python
# This is a generator!
cards = ar.cards()

for c in cards:
    print(c.id, c.title)
~~~

Note that this **returns a generator**!

---

## Getting a list of sections

~~~python
# This is a generator!
sections = ar.sections()

for s in sections:
    print(s.id, s.name)
~~~

Note that this **returns a generator**!

---

## Getting a single card

A single card is obtained either by `id` or by `title`, although priority is given to the `id`:

~~~python
# Getting by id
card = ar.get_card(cid=23)

# Getting by title
card = ar.get_card(title='My title')
~~~

### Getting the sections a card appears in

Once you obtain a card, you can find out which sections it appears in very easily:

~~~python
# This is a generator!
sections = card.sections()

for s in sections:
    print(s.id, s.name)
~~~

Note that this **returns a generator**!

---

## Getting a single section

In this case, a section can be obtained either by `id` or `name`, although priority is given to the `name`:

~~~python
# Getting by name
section = ar.get_section(name='My section')

# Getting by id
section = ar.get_section(sid=23)
~~~


### Getting the cards present in a given section

Once you obtain a section, you can also find out the cards contained in that specific section:

~~~python
# This is a generator!
cards = section.cards()

for c in cards:
    print(c.id, c.title)
~~~

Note that this **returns a generator**!

---

## Modifying a card

In order to modify a card in the archive, you may follow a couple of approaches:

- **Object approach**: from a previously obtained card, edit its fields and use them to update the card. Note that all the fields present in the object will be used in the update.

~~~python
# First we obtain a card
card = ar.get_card(cid=23)

# Modify some values
card.title = 'New title'
card.content = 'Now with more content than ever!'
card.tags += ' new tags for my list'

# Update the card
card = ar.modify_card(card=card, author='rmed')
~~~

- **Argument approach**: specify the arguments to update manually. Only those arguments passed to the function will be updated.

~~~python
# Specify the values
title = 'New title'
content = 'Noew with more content than ever!'
tags = 'a few tags to substitute'

# We may also specify the card by title
card = ar.modify_card(cid=23, title=title, content=content, tags=tags)
~~~

Note that both of these return the updated instance of the card, or `None` if the card to modify does not exist.

---

## Renaming a section

As before, you can identify the section to modify either by `id` or `name`:

~~~python
# By id
newsec = ar.rename_section('New name', sid=13)

# By name
newsec = ar.rename_section('New name', oldname='My section')
~~~

This returns a `SectionObj` instance with the new name.

---

## Searching for cards

When searching for cards in the archive, you may do so in the whole archive or narrow the search to a specific section. The search query should be a string of whitespace separated terms that will be compared against each card.

There are two additional arguments here:

- `likelihood`: indicates percentage for which to words are considered similar
- `relevance`: indicates percentage of query terms that should be present in a card for it to be considered relevant

Generally speaking, default values `likelihood=80` and `relevance=50` should suffice most of the cases, but feel free to play with it to adapt it to your needs.

~~~python
# Simple search in all the archive
result = ar.search('my search query')

# Search in a specific section by id
result = ar.search('my search query', sid=13)

# Search in a specific section by name
result = ar.search('my search query', sname='My section')

# Modify search relevance arguments
result = ar.search('my search query', likelihood=50, relevance=10)

for card in result:
    print(card.id, card.title)
~~~

Note that this **returns a generator**!
