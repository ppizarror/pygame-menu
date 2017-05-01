# coding=utf-8
"""
FONTS
Menu avaiable fonts.

Copyright (C) 2017 Pablo Pizarro @ppizarror

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

_actualpath = str(os.path.abspath(os.path.dirname(__file__))).replace('\\', '/')
_fontdir = '{0}/fonts/{1}.ttf'

# Avaiable fonts
FONT_8BIT = _fontdir.format(_actualpath, '8bit')
FONT_BEBAS = _fontdir.format(_actualpath, 'bebas')
FONT_FRANCHISE = _fontdir.format(_actualpath, 'franchise')
FONT_MUNRO = _fontdir.format(_actualpath, 'munro')
FONT_NEVIS = _fontdir.format(_actualpath, 'nevis')
