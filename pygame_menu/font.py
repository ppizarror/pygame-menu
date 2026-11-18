"""
pygame-menu
https://github.com/ppizarror/pygame-menu

FONTS
Menu fonts.
"""

from __future__ import annotations

__all__ = [
    # Fonts path included in resources
    "FONT_8BIT",
    "FONT_BEBAS",
    "FONT_COMIC_NEUE",
    "FONT_DIGITAL",
    "FONT_FRANCHISE",
    "FONT_FIRACODE",
    "FONT_FIRACODE_BOLD",
    "FONT_FIRACODE_BOLD_ITALIC",
    "FONT_FIRACODE_ITALIC",
    "FONT_HELVETICA",
    "FONT_MUNRO",
    "FONT_NEVIS",
    "FONT_OPEN_SANS",
    "FONT_OPEN_SANS_BOLD",
    "FONT_OPEN_SANS_ITALIC",
    "FONT_OPEN_SANS_LIGHT",
    "FONT_PT_SERIF",
    "FONT_EXAMPLES",
    # Typing
    "FontType",
    "FontInstance",
    # Utils
    "assert_font",
    "clear_font_cache",
    "get_font",
    "load_font_file",
    "load_system_font",
]

from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import pygame.font as __font

# Path resolution for built-in font resources
_FONTS_DIR: Path = Path(__file__).resolve().parent / "resources" / "fonts"

FONT_8BIT = (_FONTS_DIR / "8bit.ttf").as_posix()
FONT_BEBAS = (_FONTS_DIR / "bebas.ttf").as_posix()
FONT_COMIC_NEUE = (_FONTS_DIR / "comic_neue.ttf").as_posix()
FONT_DIGITAL = (_FONTS_DIR / "digital.ttf").as_posix()
FONT_FIRACODE = (_FONTS_DIR / "FiraCode-Regular.ttf").as_posix()
FONT_FIRACODE_BOLD = (_FONTS_DIR / "FiraCode-Bold.ttf").as_posix()
FONT_FIRACODE_BOLD_ITALIC = (_FONTS_DIR / "FiraMono-BoldItalic.ttf").as_posix()
FONT_FIRACODE_ITALIC = (_FONTS_DIR / "FiraMono-Italic.ttf").as_posix()
FONT_FRANCHISE = (_FONTS_DIR / "franchise.ttf").as_posix()
FONT_HELVETICA = (_FONTS_DIR / "helvetica.ttf").as_posix()
FONT_MUNRO = (_FONTS_DIR / "munro.ttf").as_posix()
FONT_NEVIS = (_FONTS_DIR / "nevis.ttf").as_posix()
FONT_OPEN_SANS = (_FONTS_DIR / "opensans_regular.ttf").as_posix()
FONT_OPEN_SANS_BOLD = (_FONTS_DIR / "opensans_bold.ttf").as_posix()
FONT_OPEN_SANS_ITALIC = (_FONTS_DIR / "opensans_italic.ttf").as_posix()
FONT_OPEN_SANS_LIGHT = (_FONTS_DIR / "opensans_light.ttf").as_posix()
FONT_PT_SERIF = (_FONTS_DIR / "ptserif_regular.ttf").as_posix()

FONT_EXAMPLES = (
    FONT_8BIT,
    FONT_BEBAS,
    FONT_COMIC_NEUE,
    FONT_DIGITAL,
    FONT_FRANCHISE,
    FONT_HELVETICA,
    FONT_MUNRO,
    FONT_NEVIS,
    FONT_OPEN_SANS,
    FONT_OPEN_SANS_BOLD,
    FONT_OPEN_SANS_ITALIC,
    FONT_OPEN_SANS_LIGHT,
    FONT_PT_SERIF,
    FONT_FIRACODE,
    FONT_FIRACODE_BOLD,
    FONT_FIRACODE_ITALIC,
    FONT_FIRACODE_BOLD_ITALIC,
)

FontType = str | __font.Font | Path
FontInstance = (str, __font.Font, Path)

# Internal Font Cache
_cache: dict[tuple[str, int], __font.Font] = {}


def _ensure_font_initialized() -> None:
    """Ensure pygame.font subsystem is initialized prior to loading fonts."""
    if not __font.get_init():
        __font.init()


def clear_font_cache() -> None:
    """Clear cached font instances to release memory."""
    _cache.clear()


def assert_font(font: Any) -> None:
    """
    Asserts if the given object is a valid font representation.

    :param font: Font object or string path
    """
    if not isinstance(font, FontInstance):
        raise AssertionError(
            "value must be a valid font type (str, Path, or pygame.font.Font)"
        )


def get_font(name: FontType, size: int) -> __font.Font:
    """
    Smart loader for font objects. Accepts paths, system font names, or Font instances.

    This is the backward-compatible smart loader. It delegates to:
    - load_font_file() for explicit file paths
    - load_system_font() for system font names
    - returns pygame.Font instances unchanged
    """
    assert_font(name)
    if not isinstance(size, int):
        raise TypeError("font size must be an integer")

    if size <= 0:
        raise ValueError("font size cannot be lower or equal than zero")

    # Case 1: direct pygame.Font instance
    if isinstance(name, __font.Font):
        return name

    # Normalize
    name_str = str(name).strip()
    if not name_str:
        raise ValueError("font name cannot be empty")

    # Case 2: explicit file path
    font_path = Path(name_str)
    if font_path.is_file():
        return load_font_file(font_path, size)

    # Case 3: system font
    return load_system_font(name_str, size)


def load_font_file(path: str | Path, size: int) -> __font.Font:
    """
    Explicitly load a font from a valid file path (.ttf, .otf).

    :param path: Path to font file
    :param size: Font size in px
    :return: pygame.font.Font instance
    """
    if size <= 0:
        raise ValueError("font size cannot be lower or equal than zero")

    font_path = Path(path)
    if not font_path.is_file():
        raise OSError(f'font file "{font_path}" does not exist')

    _ensure_font_initialized()

    resolved_path = font_path.resolve().as_posix()
    cache_key = (resolved_path, size)
    if cache_key in _cache:
        return _cache[cache_key]

    try:
        font = __font.Font(resolved_path, size)
    except OSError as err:
        raise OSError(f'font file "{font_path}" cannot be loaded') from err

    _cache[cache_key] = font
    return font


def load_system_font(name: str, size: int) -> __font.Font:
    """
    Explicitly load a system font by name.

    :param name: System font name (e.g. 'arial', 'freesans', etc.)
    :param size: Font size in px
    :return: pygame.font.Font instance
    """
    if not isinstance(name, str):
        raise TypeError("system font name must be a string")

    clean_name = name.strip()
    if not clean_name:
        raise ValueError("system font name cannot be empty")

    if size <= 0:
        raise ValueError("font size cannot be lower or equal than zero")

    _ensure_font_initialized()

    matched = __font.match_font(clean_name)
    if matched is None:
        system_fonts = __font.get_fonts()
        if not system_fonts:
            raise ValueError(
                f'system font "{clean_name}" unknown; no system fonts available'
            )

        # Deterministic closest match
        best = max(
            system_fonts, key=lambda f: SequenceMatcher(None, f, clean_name).ratio()
        )

        # Deterministic sample examples for error guidance
        examples = sorted(system_fonts)[:3]
        examples_str = ", ".join(examples)

        raise ValueError(
            f'system font "{clean_name}" unknown, use "{best}" instead\n'
            f"check system fonts with pygame.font.get_fonts() function\n"
            f"some examples: {examples_str}"
        )

    resolved_matched = Path(matched).resolve().as_posix()
    cache_key = (resolved_matched, size)
    if cache_key in _cache:
        return _cache[cache_key]

    try:
        font = __font.Font(resolved_matched, size)
    except OSError as err:
        raise OSError(f'system font file "{matched}" cannot be loaded') from err

    _cache[cache_key] = font
    return font
