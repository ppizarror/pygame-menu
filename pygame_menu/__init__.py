"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PYGAME-MENU
A menu for pygame. Simple, and easy to use.
"""

import logging
import os
from datetime import datetime
from importlib.metadata import PackageNotFoundError, metadata

logger = logging.getLogger(__name__)

__all__ = ["BaseImage", "Menu", "Sound", "Theme"]

# Metadata
try:
    _meta = metadata("pygame-menu")
    __version__ = _meta.get("Version")
    __author__ = _meta.get("Author-email").split("<")[0][1:-2].strip()
    __email__ = _meta.get("Author-email").split("<")[1][:-1].strip()
    __description__ = _meta.get("Summary")
    __license__ = _meta.get("License")
    __url__ = _meta.get("Home-page")
    __module_name__ = _meta.get("Name")
except PackageNotFoundError:
    __version__ = "4.4.3"
    __author__ = "Pablo Pizarro R."
    __email__ = "pablo@ppizarror.com"
    __description__ = "A menu for pygame. Simple, and easy to use"
    __license__ = "MIT"
    __url__ = "https://pygame-menu.readthedocs.io"
    __module_name__ = "pygame-menu"

# Extra metadata not provided by importlib
__url_documentation__ = "https://pygame-menu.readthedocs.io"
__url_source_code__ = "https://github.com/ppizarror/pygame-menu"
__url_bug_tracker__ = "https://github.com/ppizarror/pygame-menu/issues"
__keywords__ = "pygame menu menus gui widget input button pygame-menu image sound ui"
__copyright__ = f"Copyright 2017-{datetime.now().year} Pablo Pizarro R."

__contributors__ = [
    # Author
    "ppizarror",
    # Contributors
    "anxuae",
    "apuly",
    "arpruss",
    "asierrayk",
    "DA820",
    "eforgacs",
    "i96751414",
    "ironsmile",
    "jwllee",
    "maditnerd",
    "MayuSakurai",
    "mrkprdo",
    "neilsimp1",
    "notrurs",
    "NullP01nt",
    "PandaRoux8",
    "Rifqi31",
    "ThePeeps191",
    "thisIsMikeKane",
    "vnmabus",
    "werdeil",
    "zPaw",
]

# Pygame check
__pygame_version__ = None
try:
    from pygame import version as __pv

    __pygame_version__ = __pv.vernum
except (ModuleNotFoundError, ImportError):
    # Pygame is not installed; skip pygame-dependent imports
    pass

# Conditional imports
if __pygame_version__ is not None:
    from pygame_menu import (
        _scrollarea,  # type: ignore
        baseimage,
        controls,  # type: ignore
        events,  # type: ignore
        font,  # type: ignore
        locals,  # type: ignore
        menu,
        sound,
        themes,
        version,  # type: ignore
        widgets,  # type: ignore
    )

    BaseImage = baseimage.BaseImage
    Menu = menu.Menu
    Sound = sound.Sound
    Theme = themes.Theme

# Version print
if (
    "PYGAME_MENU_HIDE_VERSION" not in os.environ
    and "PYGAME_HIDE_SUPPORT_PROMPT" not in os.environ
):
    logger.info(f"{__module_name__} {__version__}")
