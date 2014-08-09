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
from fuzzywuzzy import fuzz
from sqlalchemy import Column, DateTime, Integer, Text
from sqlalchemy import create_engine, event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import VARCHAR
from .card import Card
from .exceptions import InsertError, NoCardFound, ParamError

_Base = declarative_base()


class _Card(_Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR(256), unique=True)
    description = Column(Text)
    content = Column(Text)
    tags = Column(Text)
    modified = Column(DateTime, nullable=False)


class Archive(object):
    """ Database connection. 

        **kwargs contains the database connection information. Check the
        documentation on the *_create_engine()* method for details.
    """

    def __init__(self, **kwargs):
        self._engine = self._create_engine(**kwargs)
        factory = sessionmaker(bind=self._engine)
        self._scope = scoped_session(factory)
        self._session = self._scope()

    def _insert(self, card):
        """ Insert the new card into the archive database.

            :param _Card card: new card to insert
        """
        self._session.add(card)

    def _delete(self, card):
        """ Delete the specified card from the archive database.

            :param _Card card: card to delete
        """
        self._session.delete(card)

    def _create_engine(self, **info):
        """ Set the corresponding engine conenction depending on the supplied
            **info.

            Currently supports MySQL, PostgreSQL, SQLite.

            Below are the parameters you should provide in order to connect
            to the databases.

            MySQL - requires 'pymysql' module
                mysql = database host
                user = database user
                passwd = database password (if any)
                port = database port (if any)
                db = database name

            PostgreSQL - requires 'pg8000' module
                postgresql = database host
                user = database user
                passwd = database password (if any)
                port = database port (if any)
                db = database name
                ssl = whether to use SSL or not (defaults to false)

            SQLite
                sqlite = absolute path to the database file

            :returns: SQLAlchemy engine
        """
        conn_str = ""
        if "mysql" in info.keys():
            user = info["user"]
            passwd = ""
            if "passwd" in info.keys():
                passwd = ":" + info["passwd"]
            host = "@" + info["mysql"]
            port = ""
            if "port" in info.keys():
                port = ":" + info["port"]
            db = "/" + info["db"]

            conn_str = "mysql+pymysql://" + user + passwd + host + port + db

        elif "postgresql" in info.keys():
            user = info["user"]
            passwd = ""
            if "passwd" in info.keys():
                passwd = ":" + info["passwd"]
            host = "@" + info["postgresql"]
            port = ""
            if "port" in info.keys():
                port = ":" + info["port"]
            db = "/" + info["db"]
            ssl = ""
            if "ssl" in info.keys():
                if info["ssl"]:
                    ssl = "?ssl=true"
                else:
                    ssl = ""

            conn_str = "postgresql+pg8000://" + user + passwd + host + port + db + ssl

        elif "sqlite" in info.keys():
            conn_str = "sqlite:////" + info["sqlite"]

        return create_engine(conn_str)

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

            :returns: list of Card objects
        """
        card_list = []
        for c in self._session.query(_Card).all():
            new_card = Card(
                c.title,
                c.description,
                c.content,
                c.tags,
                c.modified)
            card_list.append(new_card)

        return card_list

    def create_archive(self):
        """ Create the corresponding schemas in the database. Must be used
            when connecting to an empty database.
        """
        _Base.metadata.create_all(self._engine)

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
                c.title,
                c.description,
                c.content,
                c.tags,
                c.modified)
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
                tags=Card.normalize(tag_string=tags))
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

    def search(self, query, likelihood=80, relevance=50):
        """ Search for cards using the specified query.

            A list of tags is created from the *title* and *tags* of the
            card and then compared with the query. If the percentage of
            query words present in the card list is greater or equal
            than *relevance*, then that card is added to the result.

            If the query is empty, then a list of all the cards in the
            archive is returned.

            :param str query: search query
            :param int likelihood: percentage for which two words are
                considered to be alike (0-100)
            :param int relevance: percentage for which a search query is
                considered relevant to the card. (0-100)

            :returns: list of **Card**
        """
        if likelihood not in range(0, 100) or relevance not in range(0, 100):
            raise ParamError(
                    "likelihood and relevance must be in range 0-100")

        words = Card.tag_list(query)
        if not words:
            return self.all()

        result = []
        for c in self._session.query(_Card).order_by(_Card.title):
            common = []

            for tag in Card.tag_list(' '.join([c.title, c.tags])):
                for word in words:
                    if fuzz.ratio(word, tag) >= likelihood:
                        common.append(word)
                        common = list(set(common))
                        break

            if int((len(common) / len(words)) * 100) >= relevance:
                new_card = Card(
                    c.title,
                    c.description,
                    c.content,
                    c.tags,
                    c.modified)
                result.append(new_card)

        return result

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
