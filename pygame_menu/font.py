"""
pygame-menu
https://github.com/ppizarror/pygame-menu

FONTS
Menu fonts.
"""

__all__ = [

    # Fonts path included in resources
    'FONT_8BIT',
    'FONT_BEBAS',
    'FONT_COMIC_NEUE',
    'FONT_DIGITAL',
    'FONT_FRANCHISE',
    'FONT_FIRACODE',
    'FONT_FIRACODE_BOLD',
    'FONT_FIRACODE_BOLD_ITALIC',
    'FONT_FIRACODE_ITALIC',
    'FONT_HELVETICA',
    'FONT_MUNRO',
    'FONT_NEVIS',
    'FONT_OPEN_SANS',
    'FONT_OPEN_SANS_BOLD',
    'FONT_OPEN_SANS_ITALIC',
    'FONT_OPEN_SANS_LIGHT',
    'FONT_PT_SERIF',
    'FONT_EXAMPLES',

    # Typing
    'FontType',
    'FontInstance',

    # Utils
    'assert_font',
    'get_font'

]

from pathlib import Path
from typing import Union, Optional, Any
import os.path as path

import pygame.font as __font

# Available fonts path
__fonts_path__ = path.join(path.dirname(path.abspath(__file__)), 'resources', 'fonts', '{0}')

FONT_8BIT = __fonts_path__.format('8bit.ttf')
FONT_BEBAS = __fonts_path__.format('bebas.ttf')
FONT_COMIC_NEUE = __fonts_path__.format('comic_neue.ttf')
FONT_DIGITAL = __fonts_path__.format('digital.ttf')
FONT_FIRACODE = __fonts_path__.format('FiraCode-Regular.ttf')
FONT_FIRACODE_BOLD = __fonts_path__.format('FiraCode-Bold.ttf')
FONT_FIRACODE_BOLD_ITALIC = __fonts_path__.format('FiraMono-BoldItalic.ttf')
FONT_FIRACODE_ITALIC = __fonts_path__.format('FiraMono-Italic.ttf')
FONT_FRANCHISE = __fonts_path__.format('franchise.ttf')
FONT_HELVETICA = __fonts_path__.format('helvetica.ttf')
FONT_MUNRO = __fonts_path__.format('munro.ttf')
FONT_NEVIS = __fonts_path__.format('nevis.ttf')
FONT_OPEN_SANS = __fonts_path__.format('opensans_regular.ttf')
FONT_OPEN_SANS_BOLD = __fonts_path__.format('opensans_bold.ttf')
FONT_OPEN_SANS_ITALIC = __fonts_path__.format('opensans_italic.ttf')
FONT_OPEN_SANS_LIGHT = __fonts_path__.format('opensans_light.ttf')
FONT_PT_SERIF = __fonts_path__.format('ptserif_regular.ttf')

FONT_EXAMPLES = (FONT_8BIT, FONT_BEBAS, FONT_COMIC_NEUE, FONT_DIGITAL, FONT_FRANCHISE,
                 FONT_HELVETICA, FONT_MUNRO, FONT_NEVIS, FONT_OPEN_SANS,
                 FONT_OPEN_SANS_BOLD, FONT_OPEN_SANS_ITALIC, FONT_OPEN_SANS_LIGHT,
                 FONT_PT_SERIF, FONT_FIRACODE, FONT_FIRACODE_BOLD, FONT_FIRACODE_ITALIC,
                 FONT_FIRACODE_BOLD_ITALIC)

# Stores font cache
_cache = {}

FontType = Union[str, __font.Font, Path]
FontInstance = (str, __font.Font, Path)


def assert_font(font: Any) -> None:
    """
    Asserts if the given object is a font type.

    :param font: Font object
    :return: None
    """
    assert isinstance(font, FontInstance), \
        'value must be a font type (str, Path, pygame.Font)'


def get_font(name: FontType, size: int) -> '__font.Font':
    """
    Return a :py:class:`pygame.font.Font` object from a name or file.

    :param name: Font name or path
    :param size: Font size in px
    :return: Font object
    """
    assert_font(name)
    assert isinstance(size, int)

    font: Optional['__font.Font']
    if isinstance(name, __font.Font):
        font = name
        return font

    else:
        name = str(name)

        if name == '':
            raise ValueError('font name cannot be empty')

        if size <= 0:
            raise ValueError('font size cannot be lower or equal than zero')

        # Font is not a file, then use a system font
        if not path.isfile(name):
            font_name = name
            name = __font.match_font(font_name)

            if name is None:  # Show system available fonts
                from difflib import SequenceMatcher
                from random import randrange
                system_fonts = __font.get_fonts()

                # Get the most similar example
                most_similar = 0
                most_similar_index = 0
                for i in range(len(system_fonts)):
                    # noinspection PyArgumentEqualDefault
                    sim = SequenceMatcher(None, system_fonts[i], font_name).ratio()
                    if sim > most_similar:
                        most_similar = sim
                        most_similar_index = i
                sys_font_sim = system_fonts[most_similar_index]
                sys_suggestion = f'system font "{font_name}" unknown, use "{sys_font_sim}" instead'
                sys_message = 'check system fonts with pygame.font.get_fonts() function'

                # Get examples
                examples_number = 3
                examples = []
                j = 0
                for i in range(len(system_fonts)):
                    font_random = system_fonts[randrange(0, len(system_fonts))]
                    if font_random not in examples:
                        examples.append(font_random)
                        j += 1
                    if j >= examples_number:
                        break
                examples.sort()
                fonts_random = ', '.join(examples)
                sys_message_2 = f'some examples: {fonts_random}'

                # Raise the exception
                raise ValueError(f'{sys_suggestion}\n{sys_message}\n{sys_message_2}')

        # Try to load the font
        font = None
        if (name, size) in _cache:
            return _cache[(name, size)]
        try:
            font = __font.Font(name, size)
        except IOError:
            pass

        # If font was not loaded throw an exception
        if font is None:
            raise IOError(f'font file "{font}" cannot be loaded')
        _cache[(name, size)] = font
        return font
