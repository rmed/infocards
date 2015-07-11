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

# This module simply contains simple exceptions for use in the archive

class ArchiveException(Exception):

    def __init__(self, msg):
        self.message = msg

    def __str__(self):
        return self.message


class ArchiveConfigException(ArchiveException): pass
class ArchiveConnectionException(ArchiveException): pass
class ArchiveIntegrityException(ArchiveException): pass
class ArchiveOperationException(ArchiveException): pass
