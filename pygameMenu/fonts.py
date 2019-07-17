# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

FONTS
Menu available fonts.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

# Get actual folder
import os
import pygame as _pygame

__actualpath = str(os.path.abspath(
    os.path.dirname(__file__))).replace('\\', '/')
__fontdir = '{0}/fonts/{1}.ttf'

# Avaiable fonts
FONT_8BIT = __fontdir.format(__actualpath, '8bit')
FONT_BEBAS = __fontdir.format(__actualpath, 'bebas')
FONT_COMIC_NEUE = __fontdir.format(__actualpath, 'comic_neue')
FONT_FRANCHISE = __fontdir.format(__actualpath, 'franchise')
FONT_HELVETICA = __fontdir.format(__actualpath, 'helvetica')
FONT_MUNRO = __fontdir.format(__actualpath, 'munro')
FONT_NEVIS = __fontdir.format(__actualpath, 'nevis')
FONT_OPEN_SANS = __fontdir.format(__actualpath, 'open_sans')
FONT_PT_SERIF = __fontdir.format(__actualpath, 'pt_serif')


def get_font(name, size):
    """
    Return a pygame.Font from a name.

    :param name: font name or path
    :param size: font size
    :type name: Font or str
    :type size: int
    """
    if isinstance(name, _pygame.font.Font):
        return name
    else:
        if not os.path.isfile(name):
            name = _pygame.font.match_font(name)
        return _pygame.font.Font(name, size)
