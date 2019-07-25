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
import os.path as _path
import pygame.font as _font

__actualpath = str(_path.abspath(_path.dirname(__file__))).replace('\\', '/')
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
    :return: Font object
    :rtype: pygame.font.Font
    """
    if isinstance(name, _font.Font):
        return name
    else:

        if name == '':
            raise ValueError('Font name cannot be empty')

        # Font is not a file, then use a system font
        if not _path.isfile(name):
            font_name = name
            name = _font.match_font(font_name)

            if name is None:  # Show system avaiable fonts
                from difflib import SequenceMatcher
                system_fonts = _font.get_fonts()
                most_similar = 0
                most_similar_index = 0
                for i in range(len(system_fonts)):
                    # noinspection PyArgumentEqualDefault
                    sim = SequenceMatcher(None, system_fonts[i], font_name).ratio()  # Similarity
                    if sim > most_similar:
                        most_similar = sim
                        most_similar_index = i
                sys_font_sim = system_fonts[most_similar_index]
                sys_message = 'Check system fonts with pygame.font.get_fonts() function'
                raise ValueError('System font "{0}" unknown, use "{1}" instead\n{2}'.format(font_name,
                                                                                            sys_font_sim,
                                                                                            sys_message))

        # Try to load the font
        font = None
        try:
            font = _font.Font(name, size)
        except IOError:
            pass

        # If font was not loadad throw an exception
        if font is None:
            raise IOError('Font file "{0}" cannot be loaded'.format(font))
        return font
