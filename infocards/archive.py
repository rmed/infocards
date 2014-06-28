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
    title = Column(TEXT)
    description = Column(TEXT)
    content = Column(TEXT)
    tags = Column(TEXT)
    modified = Column(DATETIME, nullable=False)


class Archive:
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

    def new_db(self):
        """ Create the corresponding schemas in the database. Used when
            connecting to an empty database.
        """
        _Base.metadata.create_all(self._engine)

    def new_card(self, title="", description="", content="", tags=""):
        """ Create a new card for the archive.

            :param str title: title of the card
            :param str description: description of the card
            :param str content: plain text content of the card
            :param str tags: sequence of tags identifying the card separated
                by commas
        """
        new_card = _Card(
                title=title,
                description=description,
                content=content,
                tags=','.join([t.strip() for t in tags.split(',')])
                )
        self._insert(new_card)
        self._session.commit()
    
    
