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

from datetime import datetime
from sqlalchemy import *
from sqlalchemy import event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from .card import Card

_Base = declarative_base()


class _Card(_Base):
    __tablename__ = 'cards'

    id = Column(INTEGER, primary_key=True)
    title = Column(TEXT, unique=True)
    description = Column(TEXT)
    content = Column(TEXT)
    tags = Column(TEXT)
    modified = Column(DATETIME, nullable=False)


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
        
    @event.listens_for(_Card, 'before_insert')
    @event.listens_for(_Card, 'before_update')
    def _set_date(mapper, connection, target):
        """ Automatically set the modification date on the record. """
        target.modified = datetime.now()

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

            :param str input: first string to compare (input)
            :param str tag: second string to compare (tag)

            :returns int: Levenshtein distance for the two words
        """
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n,m)) space
            a,b = b,a
            n,m = m,n
            
        current = range(n+1)
        for i in range(1,m+1):
            previous, current = current, [i]+[0]*n
            for j in range(1,n+1):
                add, delete = previous[j]+1, current[j-1]+1
                change = previous[j-1]
                if a[j-1] != b[i-1]:
                    change = change + 1
                current[j] = min(add, delete, change)
                
        return current[n]

    def new_card(self, title="", description="", content="", tags=""):
        """ Create a new card for the archive.

            :param str title: title of the card
            :param str description: description of the card
            :param str content: plain text content of the card
            :param str tags: sequence of tags identifying the card separated
                by whitespaces
        """
        new_card = _Card(
                title=title,
                description=description,
                content=content,
                tags=Card.tag_string(Card.tag_list(tags))
                )
        self._insert(new_card)
        self._session.commit()
    
    def search(self, query, dist=1):
        """ Search for cards by using the specified query.

            Create a complete tag list from the title and the tags of a card
            and compare the words in the query with those in this list by
            calculating their Levenshtein distance.

            Uses the *Card.tag_list()* static method so that the query has
            the same format rules as the stored tags.

            :param str query: search query
            :param int distance: distance value upon which the query words and
                the tags are considered to match

            :returns list: list of **Card** objects
        """
        words = Card.tag_list(query)
        result = []
        for c in self._session.query(_Card).order_by(_Card.title):
            common = []
            c_tags = Card.tag_list(' '.join([c.title, c.tags]))
            for tag in c_tags:
                for word in words:
                    if self.distance(word, tag) <= dist:
                        print(word, tag, self.distance(word,tag))
                        common.append(word)
                        common = list(set(common))
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