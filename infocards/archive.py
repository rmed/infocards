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

from __future__ import absolute_import
from datetime import datetime
from fuzzywuzzy import fuzz
from peewee import *
from .exceptions import ArchiveConfigException, ArchiveConnectionException
from .exceptions import ArchiveIntegrityException, ArchiveOperationException
from .models import _db_proxy, Card, CardObj, Section, SectionObj, Relation


class Archive(object):

    def __init__(self, **kwargs):
        """ Initialize the archive according to the parameters passed.

            These parameters vary from one DBMS to another.
        """
        # Need to initialize the database for the models
        self.db = self._init_db(**kwargs)
        _db_proxy.initialize(self.db)

        try:
            # Create tables
            self.db.create_tables([Card, Section, Relation], True)

        except ImproperlyConfigured as e:
            raise ArchiveConfigException(str(e))

    def _init_db(self, **kwargs):
        """ Parse the arguments and initialize the proper database.

            The parameters used for each database are given directly to
            their specific connectors:

            - MySQL: PyMySQL
            - SQLite: sqlite3
            - PostgreSQL: psycopg2

            Check their documentation for more information on the available
            parameters.

            Here we only care about the database type, which could be either
            'mysql', 'sqlite' or 'postgres'

            Returns an already initialized databased.
        """
        db_name = kwargs.pop('db_name')
        db_type = kwargs.pop('db_type')

        try:
            if db_type == 'mysql':
                return MySQLDatabase(db_name, **kwargs)

            elif db_type == 'postgres':
                return PostgresqlDatabase(db_name, **kwargs)

            elif db_type == 'sqlite':
                return SqliteDatabase(db_name)

        except OperationalError as e:
            raise ArchiveConnectionException(str(e))

        raise ArchiveConnectionException('Invalid database type')

    def add_card_to_section(self, cid=0, ctitle="", sid=0, sname=""):
        """ Create a card-section relation.

            cid     -- card id to add
            ctitle  -- title of the card add
            sid     -- section id
            sname   -- section name

            Returns boolean for success or failure
        """
        attrs = {
            'card': None,
            'section': None
        }

        if cid:
            attrs['card'] = cid
        else:
            attrs['card'] = self.get_card(title=ctitle).id

        if sid:
            attrs['section'] = sid
        else:
            attrs['section'] = self.get_section(name=sname).id

        try:
            rel = Relation.create(**attrs)

        except DoesNotExist as e:
            return False

        return True

    def cards(self):
        """ Return a generator for all the cards in the archive. """
        cards = Card.select()

        for card in cards:
            yield CardObj(card)

    def delete_card(self, cid=0, title=""):
        """ Delete a card from the archive.

            This will also delete any dependent relation.

            Returns boolean for success or failure.
        """
        try:
            if cid:
                card = Card.get(Card.id == cid)

            elif title:
                card = Card.get(Card.title == title)

            else:
                return False

        except DoesNotExist:
            return False

        deleted = card.delete_instance(recursive=True, delete_nullable=True)

        if deleted > 0:
            return True

        return False

    def delete_section(self, name="", sid=0):
        """ Delete a section from the archive.

            This will also delete any dependent relation.

            Returns boolean for success or failure.
        """
        try:
            if name:
                section = Section.get(Section.name == name)

            elif sid:
                section = Section.get(Section.id == sid)

            else:
                return False

        except DoesNotExist:
            return False

        deleted = section.delete_instance(recursive=True, delete_nullable=True)

        if deleted > 0:
            return True

        return False

    def get_card(self, cid=0, title=""):
        """ Obtain a specific card from the archive.

            The card is fetched by its unique id for simplicity, but is
            also possible to do it by title, given it is also unique.

            In case both of them are present, card id has higher priority.
        """
        try:
            if cid:
                return CardObj(Card.get(Card.id == cid))

            elif title:
                return CardObj(Card.get(Card.title == title))

        except DoesNotExist:
            return None

        return None

    def get_section(self, name="", sid=0):
        """ Obtain a specific section from the archive.

            In this case, sections should have a simple name that easily
            identifies them, therefore priority is given to the name rather
            than to the section id.
        """
        try:
            if name:
                return SectionObj(Section.get(Section.name == name))

            elif sid:
                return SectionObj(Section.get(Section.id == sid))

        except DoesNotExist:
            return None

        return None

    def modify_card(self, card=None, cid=0, ctitle="",
        title="", desc="", content="", tags="", author="UNKNOWN"):
        """ Modifies an already existing card overwriting its information
            with the one provided.

            card    -- CardObj instance from which to obtain the new
                information. It is given priority if present.
                Will also obtain the card id from here.
            cid     -- id of the card to modify
            ctitle  -- title of the card to modify

            title   -- new title for the card
            desc    -- new description for the card
            content -- new content for the card
            tags    -- new tags for the card
            author  -- author of the modification, defaults to 'UNKNOWN'.
                This one is not obtained from the card object

            Note that if the card argument is not provided, only the
            arguments present will be overwritten, meaning that it is
            only necessary to pass the relevant information to modify.

            Returns the updated card
        """
        if card:
            cid = card.id
            title = card.title
            desc = card.desc
            content = card.content
            tags = card.tags

        try:
            if cid:
                modcard = Card.get(Card.id == cid)

            elif title:
                modcard = Card.get(Card.title == title)

        except DoesNotExist:
            return None

        modcard.title = title if title else modcard.title
        modcard.desc = desc if desc else modcard.desc
        modcard.content = content if content else modcard.content
        modcard.tags = tags if tags else modcard.tags
        modcard.modified = datetime.now()
        modcard.modified_by = author

        try:
            modcard.save()

        except IntegrityError as e:
            self.db.rollback()
            raise ArchiveIntegrityException(str(e))

        return CardObj(modcard)

    def new_card(self, title, desc, content, tags, author="UNKNOWN"):
        """ Add a new card to the archive.

            title   -- title of the card, must be unique
            desc    -- short description of the card
            content -- main content of the card
            tags    -- space-separated tags for the card
            author  -- optional name of the author of the card

            Returns the newly created card
        """
        attrs = {
            'title': title,
            'desc': desc,
            'content': content,
            'tags': tags,
            'modified': datetime.now(),
            'modified_by': author
        }

        try:

            return CardObj(Card.create(**attrs))

        except IntegrityError as e:
            self.db.rollback()
            raise ArchiveIntegrityException(str(e))

    def new_section(self, name):
        """ Create a new section in the archive.

            name -- name of the section, must be unique

            Returns the newly created section
        """
        attrs = {
            'name': name
        }

        try:
            return SectionObj(Section.create(**attrs))

        except IntegrityError as e:
            self.db.rollback()
            raise ArchiveIntegrityException(str(e))

    def remove_card_from_section(self, cid=0, ctitle="", sid=0, sname=""):
        """ Remove a card-section relation.

            cid     -- card id to add
            ctitle  -- title of the card add
            sid     -- section id
            sname   -- section name

            Returns boolean for success or failure
        """
        if cid:
            card = cid
        else:
            card = self.get_card(title=ctitle).id

        if sid:
            section = sid
        else:
            section = self.get_section(name=sname).id

        try:
            rel = Relation.get(
                Relation.card == card,
                Relation.section == section)

        except DoesNotExist as e:
            return False

        deleted = rel.delete_instance()

        if deleted > 0:
            return True

        return False

    def rename_section(self, newname, oldname="", sid=0):
        """ Rename a section.

            Returns the new section
        """
        try:
            if oldname:
                section = Section.get(Section.name == name)

            elif sid:
                section = Section.get(Section.id == sid)

            else:
                return None

        except DoesNotExist:
            raise ArchiveOperationException('section does not exist')

        section.name = newname
        try:
            section.save()

        except IntegrityError as e:
            self.db.rollback()
            raise ArchiveIntegrityException(str(e))

        return SectionObj(section)

    def search(self, query, sname="", sid=0, likelihood=80, relevance=50):
        """ Search for relevant cards in the archive.

            query      -- search terms, separated by blankspace
            section    -- section to perform the search in. If not provided,
                    will search the whole archive.
            likelihood -- percentage for which to words should be considered
                    similar.
            relevance  -- percentage of query terms that must be present in
                    a card for it to be considered relevant

            Returns a generator.
        """
        search_terms = set([t.lower() for t in query.split()])
        if not search_terms:
            return []

        # Get the list of cards to iterate
        if section_id or section_name:
            section = self.get_section(section_name, section_id)

            if not section:
                return []

            # Raw card search
            cards = (Card
                .select()
                .join(Relation)
                .join(Section)
                .where(Section.id == section.id))

        else:
            cards = Card.select()

        # Compare each card
        for card in cards:
            s_card = "%s %s %s %s" % (
                str(card.id), card.title, card.desc, card.tags)

            card_terms = set([t.lower() for t in s_card.split()])

            common = set()

            for c_term in card_terms:
                # Check each search term with those from card
                for s_term in search_terms:
                    if fuzz.partial_ratio(s_term, c_term) >= 80:
                        common.add(s_term)
                        break

            # Check if the card is relevant
            if int((len(common) / len(search_terms)) * 100) < 50:
                continue

            yield CardObj(card)

    def sections(self):
        """ Return a generator for all the sections in the archive. """
        sections = Section.select()

        for section in sections:
            yield SectionObj(section)
