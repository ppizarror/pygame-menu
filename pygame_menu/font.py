"""
pygame-menu
https://github.com/ppizarror/pygame-menu

FONTS
Menu fonts.
"""

from __future__ import annotations

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
    'get_font',
    'load_font_file',
    'load_system_font'

]

from pathlib import Path
from typing import Any, Union

import pygame.font as __font

# Available fonts path
__fonts_path__ = (Path(__file__).resolve().parent / 'resources' / 'fonts' / '{0}').as_posix()

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

FontType = Union[str, __font.Font, Path]
FontInstance = (str, __font.Font, Path)

# Stores font cache
_cache: dict[tuple[FontType, int], '__font.Font'] = {}


def assert_font(font: Any) -> None:
    """
    Asserts if the given object is a font type.

    :param font: Font object
    """
    if not isinstance(font, FontInstance):
        raise AssertionError('value must be a font type (str, Path, pygame.Font)')


def get_font(name: FontType, size: int) -> '__font.Font':
    """
    Return a :py:class:`pygame.font.Font` object from a name or file.

    This is the backward-compatible smart loader. It delegates to:
    - load_font_file() for explicit file paths
    - load_system_font() for system font names
    - returns pygame.Font instances unchanged
    """
    assert_font(name)
    assert isinstance(size, int)

    # Case 1: direct pygame.Font instance
    if isinstance(name, __font.Font):
        return name

    # Normalize
    name_str = str(name)
    if not name_str:
        raise ValueError('font name cannot be empty')
    if size <= 0:
        raise ValueError('font size cannot be lower or equal than zero')

    # Case 2: explicit file path
    font_path = Path(name_str)
    if font_path.is_file():
        return load_font_file(font_path, size)

    # Case 3: system font
    return load_system_font(name_str, size)


def load_font_file(path: Union[str, Path], size: int) -> '__font.Font':
    """
    Explicitly load a font from a file path.

    :param path: Path to a .ttf/.otf font file
    :param size: Font size in px
    :return: pygame.font.Font instance
    """
    if size <= 0:
        raise ValueError('font size cannot be lower or equal than zero')

    font_path = Path(path)
    if not font_path.is_file():
        raise OSError(f'font file \"{font_path}\" does not exist')

    key = (font_path.as_posix(), size)
    if key in _cache:
        return _cache[key]

    try:
        font = __font.Font(font_path.as_posix(), size)
    except OSError:
        raise OSError(f'font file \"{font_path}\" cannot be loaded')

    _cache[key] = font
    return font


def load_system_font(name: str, size: int) -> '__font.Font':
    """
    Explicitly load a system font by name.

    :param name: System font name (e.g. 'arial', 'freesans', etc.)
    :param size: Font size in px
    :return: pygame.font.Font instance
    """
    if not isinstance(name, str):
        raise TypeError('system font name must be a string')

    if not name:
        raise ValueError('system font name cannot be empty')

    if size <= 0:
        raise ValueError('font size cannot be lower or equal than zero')

    matched = __font.match_font(name)
    if matched is None:
        from difflib import SequenceMatcher
        from random import randrange

        system_fonts = __font.get_fonts()

        # Find the closest match
        best = max(system_fonts, key=lambda f: SequenceMatcher(None, f, name).ratio())
        suggestion = f'system font "{name}" unknown, use "{best}" instead'

        # Random examples
        examples = sorted({system_fonts[randrange(len(system_fonts))] for _ in range(3)})
        examples_str = ', '.join(examples)

        raise ValueError(
            f'{suggestion}\n'
            f'check system fonts with pygame.font.get_fonts() function\n'
            f'some examples: {examples_str}'
        )

    key = (matched, size)
    if key in _cache:
        return _cache[key]

    try:
        font = __font.Font(matched, size)
    except OSError:
        raise OSError(f'system font file "{matched}" cannot be loaded')

    _cache[key] = font
    return font
