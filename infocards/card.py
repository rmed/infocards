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
.. module:: card
    :platform: Unix, Windows
    :synopsis: Card operations

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""

from __future__ import absolute_import
from .exceptions import ParamError


class Card(object):
    """ Cards have a simple structure and contain a small amount of
        information stored as plain text in the *Archive*.

        :param str title: title of the card
        :param str description: a small description of the card
        :param str content: content of the card
        :param str tags: tags are stored as a sequence of words and/or
            sentences separated by whitespaces in the archive. However,
            the *Card* object will store the tags as a list for
            easier access.
        :param datetime modified: last modification's date and time

        Note that in order to be able to search for cards, it is necessary
        to include tags.
    """

    def __init__(self, title, description, content, tags, modified):
        self.title = title
        self.description = description
        self.content = content
        self.tags = self.tag_list(tags)
        self.modified = modified

    @staticmethod
    def normalize(tag_list=None, tag_string=None):
        """ Normalize a tag string or list.

            Normalization is achieved by removing repeated words and
            transforming every word into lowercase.

            :param list tag_list: tag list to normalize
                (useful when modifying card tags)
            :param str tag_string: tag string to normalize
        """
        if tag_list and tag_string:
            raise ParamError("Only one parameter type may be normalized")

        elif tag_list:
            return sorted(set([t.lower() for t in tag_list]))

        elif tag_string:
            return ' '.join(sorted(set(
                [t.lower() for t in tag_string.split()])))

        else:
            # Nothing to normalize
            return

    @staticmethod
    def tag_list(tag_string):
        """ Obtain a tag list from a string.

            This method is called when a new card is created. It will
            remove duplicate tags, set the tags to lowercase and sort
            the list when created.

            :param str tag_string: string of tags separated by whitespaces
        """
        return Card.normalize(tag_list=tag_string.split())

    @staticmethod
    def tag_string(tag_list):
        """ Obtain a string of tags from a list. Each tag will be separated
            by a whitespace.

            :param list tag_list: list of tags to convert
        """
        return Card.normalize(tag_string=' '.join(tag_list))
