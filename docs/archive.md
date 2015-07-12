# Structure

The Archive is structured using three tables:

Table        | Data
---          | ---
**card**     | contains all the cards stored in the Archive
**section**  | contains all sections stored in the Archive
**relation** | contains relations between cards and sections

Relation management is automatically done by the Archive, so you should not need using it directly. It is simply used to determine what cards belong to which section (if any) and what sections a card is present in.

## Cards

Card objects are the ones used to represent the relevant information, their structure is as follows:

Field           | Type      | Data
---             | ---       | ---
**id**          | int       | unique id of the card in the database
**title**       | str       | unique title of the card
**desc**        | str       | small description showing the contents, or topic, of the card
**content**     | str       | main text of the card, may be several lines long
**tags**        | str       | whitespace separated words that will be used when searching
**modified**    | timestamp | timestamp of the latest modification of the card
**modified_by** | str       | displays who has performed the latest modification and is completely optional

## Sections

Sections are far more simple in comparison:

Field    | Type | Data
---      | ---  | ---
**id**   | int  | unique id of the section in the database
**name** | str  | unique name of the section

## Relations

Relations are formed by a unique composite key using *section id* and *card id*.
