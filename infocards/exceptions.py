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
.. module:: exceptions
    :platform: Unix, Windows
    :synopsis: Custom library exceptions

.. moduleauthor:: Rafael Medina García <rafamedgar@gmail.com>
"""


class ArchiveError(Exception):
    """ Base class for the archive exceptions. """
    pass


class InsertError(ArchiveError):
    """ Raised when an error occurs whilst trying to insert a new card
        in the archive.

        :param str message: error explanation
    """

    def __init__(self, message):
        self.message = message


class NoCardFound(ArchiveError):
    """ Raised when a specific card does not exist.

        :param str message: error explanation
    """

    def __init__(self, message):
        self.message = message

class ParamError(ArchiveError):
    """ Raised when function parameters are not valid.

        :param str message: error explanation
    """

    def __init__(self, message):
        self.message = message

class SearchError(ArchiveError):
    """ Raised when an error occurs when searching.

        :param str message: error explanation
    """

    def __init__(self, message):
        self.message = message