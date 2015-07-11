# -*- coding: utf-8 -*-
#
# Simple information card archive library
# https://github.com/rmed/infocards
#
# Copyright (C) 2015  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from peewee import *


# Database information can only be known at run-time
_db_proxy = Proxy()

class BaseModel(Model):
    class Meta:
        database = _db_proxy


class Card(BaseModel):
    title = CharField(unique=True)
    desc = CharField()
    content = TextField()
    tags = CharField()
    modified = DateTimeField()
    modified_by = CharField()


class CardObj(object):

    def __init__(self, card):
        """ Create a dummy card object in order to prevent
            modifications in the database from outside the
            archive.
        """
        self.id = card.id
        self.title = card.title
        self.desc = card.desc
        self.content = card.content
        self.tags = card.tags
        self.modified = card.modified
        self.modified_by = card.modified_by

    def sections(self):
        """ Get all the the sections this card appears in. """
        sections = (Section
            .select()
            .join(Relation)
            .join(Card)
            .where(Card.id == self.id))

        for section in sections:
            yield SectionObj(section)


class Section(BaseModel):
    name = CharField(unique=True)


class SectionObj(object):

    def __init__(self, section):
        """ Create a dummy section object in order to prevent
            modifications in the database from outside the
            the archive.
        """
        self.id = section.id
        self.name = section.name

    def cards(self):
        """ Get all the cards in the section. """
        cards = (Card
            .select()
            .join(Relation)
            .join(Section)
            .where(Section.id == self.id))

        for card in cards:
            yield CardObj(card)


class Relation(BaseModel):
    section = ForeignKeyField(Section)
    card = ForeignKeyField(Card)

    class Meta:
        primary_key = CompositeKey('section', 'card')
