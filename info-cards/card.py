# -*- coding: utf-8 -*-
#
# Simple information card archive library
# https://github.com/RMed/info-cards
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


class Card:
    """ Cards have a simple structure and contain a small amount of
        information stored as plain text in the *Archive*.

        :param str title: title of the card
        :param str description: a small description of the card
        :param str content: content of the card
        :param str tags: tags are stored as a sequence of words and/or
            sentences separated by commas. However, the *Card* object
            will store the tags as a list for easier access.

        Note that in order to be able to search for cards, it is necessary
        to include relevant information such as title, brief description
        and some tags.
    """

    def __init__(self, title, description, content, tags):
        self.title = title
        self.description = description
        self.content = content
        self.tags = self.tag_list(tags)

    def tag_list(self, tag_string):
        """ Obtain a tag list from a string.

            :param str tag_string: string of tags separated by commas
        """
        return [t.trim() for t in tags.split(',')]

    def tag_string(self, tag_list):
        """ Obtain a string of tags from a list. Each tag will be separated
            by a comma.

            :param list tag_list: list of tags to convert
        """
        return ','.join(tag_list)
