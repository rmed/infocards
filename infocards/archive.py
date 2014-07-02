# -*- coding: utf-8 -*-
#
# Simple information card archive library
# https://github.com/RMed/infocards
#
# Copyright (C) 2014  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
.. module:: archive
    :platform: Unix, Windows
    :synopsis: Archive operations

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

from __future__ import absolute_import
from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from .card import Card
from .exceptions import InsertError, NoCardFound, ParamError

_Base = declarative_base()


class _Card(_Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    title = Column(Text, unique=True)
    description = Column(Text)
    content = Column(Text)
    tags = Column(Text)
    modified = Column(DateTime, nullable=False)


class Archive(object):
    """ Database connection. For the moment, only SQLite3 is supported.

        :param str db_path: path to the database
    """

    def __init__(self, db_path):
        self.db_path = db_path
        self._engine = create_engine('sqlite:////' + db_path)
        factory = sessionmaker(bind=self._engine)
        self._scope = scoped_session(factory)
        self._session = self._scope()

    def _insert(self, card):
        """ Insert the new card into the archive database.

            :param _Card card: new card to insert
        """
        self._session.add(card)

    def _delete(self, card):
        """ RDelete the specified card from the archive database.

            :param _Card card: card to delete
        """
        self._session.delete(card)

    @event.listens_for(_Card, 'before_insert')
    @event.listens_for(_Card, 'before_update')
    def _set_date(mapper, connection, target):
        """ Automatically set the modification date on the record. """
        target.modified = datetime.now()

    def _update(self, card, new_card):
        """ Updates the content of a card with the new card.

            :param _Card card: card to update
            :param Card new_card: new card info
        """
        card.title = new_card.title
        card.description = new_card.description
        card.content = new_card.content
        card.tags = Card.tag_string(new_card.tags)

    def all(self):
        """ Obtain a list of all the cards stored in the archive.

            :returns list: list of Card objects
        """
        card_list = []
        for c in self._session.query(_Card).all():
            new_card = Card(
                title=c.title,
                description=c.description,
                content=c.content,
                tags=c.tags,
                modified=c.modified
                )
            card_list.append(new_card)

        return card_list

    def create_archive(self):
        """ Create the corresponding schemas in the database. Must be used
            when connecting to an empty database.
        """
        _Base.metadata.create_all(self._engine)

    @staticmethod
    def distance(a, b):
        """ Compute the Levenshtein distance between two words.

            Implementation by Magnus Lie Hetland.

            :param str a: first string to compare (input)
            :param str b: second string to compare (tag)

            :returns int: Levenshtein distance for the two words
        """
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a, b = b, a
            n, m = m, n

        current = range(n+1)
        for i in range(1, m+1):
            previous, current = current, [i] + [0]*n
            for j in range(1, n+1):
                add, delete = previous[j]+1, current[j-1]+1
                change = previous[j-1]
                if a[j-1] != b[i-1]:
                    change = change + 1
                current[j] = min(add, delete, change)

        return current[n]

    def get_card(self, title):
        """ Obtain a card from the archive.

            This is a direct search, so the title (or the row id) must
            be written as in the stored card.

            :param str title: title of the card to get

            :raises NoCardFound: raised when the card does not exist
        """
        try:
            c = self._session.query(_Card).filter(_Card.title == title).one()
            result = Card(
                title=c.title,
                description=c.description,
                content=c.content,
                tags=c.tags,
                modified=c.modified
                )
            return result
        except NoResultFound:
            raise NoCardFound("Card '%s' does not exist" % title)

    def new_card(self, title="", description="", content="", tags=""):
        """ Create a new card for the archive.

            :param str title: title of the card
            :param str description: description of the card
            :param str content: plain text content of the card
            :param str tags: sequence of tags identifying the card separated
                by whitespaces

            :raises InsertError: raised when a card already exists in
                the archive
        """
        try:
            new_card = _Card(
                title=title,
                description=description,
                content=content,
                tags=Card.normalize(tag_string=tags)
                )
            self._insert(new_card)
            self._session.commit()
        except IntegrityError:
            raise InsertError("Card '%s' already exists" % title)

    def remove_card(self, title):
        """ Remove a card from the archive.

            :param str title: title of the card to remove

            :raises NoCardFound: raised when the card cannot be found
        """
        try:
            c = self._session.query(_Card).filter(_Card.title == title).one()
            self._delete(c)
            self._session.commit()
        except NoResultFound:
            raise NoCardFound("Card '%s' does not exist" % title)

    def search(self, query, alg="submatch", dist=1):
        """ Search for cards by using the specified query.

            A list of tags is created from the title and tags of the card
            and then one of the two algorithms are used in the search.

            If the *submatch* algorithm is used, the archive will try
            to match both the current query word and tag so that either
            of them is contained within the other.

            If the *distance* algorithm is used, the archive will
            compute the Levenshtein distance and consider the result as
            a match given the *dist* parameter.

            Uses the *Card.tag_list()* static method so that the query has
            the same format rules as the stored tags.

            :param str query: search query
            :param str alg: search algorithm to use. Possible values are
                *substring* (default) and *distance*
            :param int dist: distance value upon which the query words and
                the tags are considered to match

            :returns list: list of **Card** objects
        """
        if alg not in ["submatch", "distance"]:
            raise ParamError("Invalid algorithm: '%s'" % alg)

        words = Card.tag_list(query)
        if not words:
            return self.all()

        result = []
        for c in self._session.query(_Card).order_by(_Card.title):
            common = []

            for tag in Card.tag_list(' '.join([c.title, c.tags])):
                for word in words:
                    # Distance algorithm
                    if alg is 'distance' and self.distance(word, tag) <= dist:
                        common.append(word)
                        common = list(set(common))
                        break
                    # Submatch algorithm
                    elif alg is 'submatch' and self.submatch(word, tag):
                        common.append(word)
                        common = list(set(common))
                        break

            if len(common) >= (len(words)/2):
                new_card = Card(
                    title=c.title,
                    description=c.description,
                    content=c.content,
                    tags=c.tags,
                    modified=c.modified
                    )
                result.append(new_card)

        return result

    @staticmethod
    def submatch(a, b):
        """ Check if a contains b or b contains a

            :param str a: first string to check (input)
            :param str b: second string to check (tag)

            :returns: True if either of the conditions is met,
                otherwise False
        """
        return (a in b) or (b in a)

    def update_card(self, title, new_card):
        """ Update the information of a card.

            :param str title: title of the card to update
            :param Card new_card: *Card* object with the updated information

            :raises NoCardFound: raised when the card to update is not found
        """
        try:
            c = self._session.query(_Card).filter(_Card.title == title).one()
            self._update(c, new_card)
            self._session.commit()
        except NoResultFound:
            raise NoCardFound("Card '%s' does not exist" % title)
