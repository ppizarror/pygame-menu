# coding=utf-8
"""
FONTS
Menu avaiable fonts.

Copyright (C) 2017-2018 Pablo Pizarro @ppizarror

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

# Get actual folder
import os

__actualpath = str(os.path.abspath(
    os.path.dirname(__file__))).replace('\\', '/')
__fontdir = '{0}/fonts/{1}.ttf'

# Avaiable fonts
FONT_8BIT = __fontdir.format(__actualpath, '8bit')
FONT_BEBAS = __fontdir.format(__actualpath, 'bebas')
FONT_FRANCHISE = __fontdir.format(__actualpath, 'franchise')
FONT_MUNRO = __fontdir.format(__actualpath, 'munro')
FONT_NEVIS = __fontdir.format(__actualpath, 'nevis')
