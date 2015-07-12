# Archive API reference

Package: `infocards.archive`

The following shows relevant information on the Archive and its functions.

## Archive(**kwargs)

Main component of the library, performs all the operations in the database.

### Parameters

Common parameters:

- `db_name` (str): name of the database. Will be passed directly to the database connector. In the case of SQLite, it should be the path to the database file.
- `db_type` (str): either `mysql`, `postgres` or `sqlite`

Specific parameters for MySQL and PostgreSQL connectors:

- `host` (str): host of the database
- `user` (str): username of the database host
- `password` (str): password used to connect to the host
- `port` (int): port of the database system

Additional parameters may be required depending on the connector used. Check the documentations for [PyMySQL](https://github.com/PyMySQL/PyMySQL) and [psycopg2](http://initd.org/psycopg/).

### Returns

`Archive` object.

### Raises

`ArchiveConnectionException` or `ArchiveConfigException`.

---

### Functions

#### _**add_card_to_section(cid=0, ctitle="", sid=0, sname="")**_

Creates a *card-section* relation.

##### Parameters

- `cid` (int): card id used to identify the card for the relation
- `ctitle` (str): unique title of the card
- `sid` (int): section id used to identify the section for the relation
- `sname` (str): unique name of the section

In both cases, either the id or the title/name can be used to perform the identification.

##### Returns

`True` if the relation was created, otherwise `False`

---

#### cards()

Obtain all the cards in the archive

##### Returns

Generator: `CardObj` for each of the cards in the archive.

---

#### _**delete_card(cid=0, title="")**_

Deletes a card from the archive, as well as all the `Relation`s the card was present int.

##### Parameters

- `cid` (int): card id
- `title` (str): unique card title

Either the id or the title can be used to perform the identification.

##### Returns

`True` if the card was deleted, otherwise `False`

---


#### _**delete_section(name="", sid=0)**_

Delete a section from the archive, as well as all the `Relation`s the section was present in.

##### Parameters

- `name` (str): unique section name
- `sid` (int): section id

Either the name or the id can be used to perform the identification.

##### Returns

`True` if the section was deleted, otherwise `False`

---

#### _**get_card(cid=0, title="")**_

Obtains a single card from the archive.

##### Parameters

- `cid` (int): card id
- `title` (str): unique card title

Either the id or the title can be used to perform the identification.

##### Returns

`CardObj` with the card information or `None` if the card was not found.

---

#### _**get_section(name="", sid=0)**_

Obtains a single section from the archive.

##### Parameters

- `name` (str): unique section name
- `sid` (int): section id

Either the name or the id can be used to perform the identification.

##### Returns

`SectionObj` with the section information or `None` if the section was not found.

---

#### _**modify_card(card=None, cid=0, ctitle="", title="", desc="", content="", tags="", author="UNKNOWN")**_

Updates a card in the database.

##### Parameters

- `card` (`CardObj`): card from which to obtain all the information for the modification (has higher priority than the rest of the parameters)
- `cid` (int): id of the card to modify
- `ctitle` (str): unique title of the card to modify
- `title` (str): new title for the card
- `desc` (str): new description for the card
- `content` (str): new content for the card
- `tags` (str): whitespace separated tags for the card
- `author` (str): name of the author of the modification

Note that if `card` is not used, only the parameters that have been specificed will be overwritten. The modification timestamp of the card will be automatically set to the current date and time.

##### Returns

New `CardObj` instance of the updated card.

##### Raises

`ArchiveIntegrityException`

---

#### _**new_card(title, desc, content, tags, author="UNKNOWN")**_

Creates a new card in the archive.

##### Parameters

- `title` (str): unique title for the new card
- `desc` (str): short description for the card
- `content` (str): main content of the card, may be multiline
- `tags` (str): whitespace separated tags for the card
- `author` (str): name of the author of the new card

The modification timestamp will be automatically set to the current date and time.

##### Returns

New `CardObj` instance of the created card.

##### Raises

`ArchiveIntegrityException`

---

#### _**new_section(name)**_

Creates a new section in the archive.

##### Parameters

- `name` (str): unique name for the new section

##### Returns

New `SectionObj` instance of the created section.

##### Raises

`ArchiveIntegrityException`

---

#### _**remove_card_from_section(cid=0, ctitle="", sid=0, sname="")**_

Removes a *card-section* relation.

##### Parameters

- `cid` (int): card id used to identify the card for the relation
- `ctitle` (str): unique title of the card
- `sid` (int): section id used to identify the section for the relation
- `sname` (str): unique name of the section

In both cases, either the id or the title/name can be used to perform the identification.

##### Returns

`True` if the relation was deleted, otherwise `False`

---

#### _**rename_section(newname, oldname="", sid=0)**_

Rename a section of the archive

##### Parameters

- `newname` (str): new name for the section (should not exist already)
- `oldname` (str): old name of the section, used for identification
- `sid` (int): section id

In order to identify the section, either its old name or id can be used.

##### Returns

New `SectionObj` instance with the updated name.

##### Raises

`ArchiveIntegrityException`

---

#### _**search(query, sname="", sid=0, likelihood=80, relevance=50)**_

Perform a search in the archive to find relevant cards. By default, it performs the search through all the cards of the archive, but it is also possible to narrow the search to those cards present in the specified section.

##### Parameters

- `query` (str): whitespace separated query terms
- `sname` (str): name of the section in which to perform the search
- `sid` (int): unique id of the section in which to perform the search
- `likelihood` (int): percentage for which two words are considered similar
- `relevance` (int): percentage of query terms that a card must contain for it to be considered relevant to the search.

##### Returns

Generator: cards relevant to the search, or an empty list if no cards were found.

---

#### sections()

Obtain all the sections in the archive

##### Returns

Generator: `SectionObj` for each of the sections in the archive.
