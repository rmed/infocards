# Models API Reference

Package: `infocards.models`

The following shows all the relevant information regarding usage of models in *infocards*.

## BaseModel

This is the model that all the ORM-related models use as a base.

~~~python
class BaseModel(Model):
    class Meta:
        database = _db_proxy
~~~

The `database` of the model is specified at the time of creation of an Archive.

---

## Card

This is the model that the ORM uses to store card information in the database.

~~~python
class Card(BaseModel):
    title = CharField(unique=True)
    desc = CharField()
    content = TextField()
    tags = CharField()
    modified = DateTimeField()
    modified_by = CharField()
~~~

You should not access this class directly in order to prevent issues.

---

## CardObj(card)

The object representation of the previous model. This is the object type that is returned in all the functions of the Archive that query for cards and can be easily modified.

### Parameters

- `card`: `Card` instance obtained from querying the database.

When a `CardObj` is created, it copies all the information from the `card` parameter. This object can then modified and used to update a record in the database.

### Functions

#### _**sections()**_

~~~python
sec = card.sections()
~~~

##### Returns

Generator: sections in which this card appears in.

---

## Section

This is the model that the ORM uses to store section information in the database.

~~~python
class Section(BaseModel):
    name = CharField(unique=True)
~~~

You should not access this class directly in order to prevent issues.

---

## SectionObj(section)

The object representation of the previous model. This is the object type that is returned in all the functions of the Archive that query for sections.

### Parameters

- `section`: `Section` instance obtained from querying the database.

When a `SectionObj` is created, it copies all the information from the `section` parameter.

### Functions

#### _**cards()**_

~~~python
cards = section.cards()
~~~

##### Returns

Generator: cards present in this section.

---

## Relation

This is the model that stores relations between cards and sections. Generally, it should not be necessary to access it in any way.

~~~python
class Relation(BaseModel):
    section = ForeignKeyField(Section)
    card = ForeignKeyField(Card)

    class Meta:
        primary_key = CompositeKey('section', 'card')
~~~
