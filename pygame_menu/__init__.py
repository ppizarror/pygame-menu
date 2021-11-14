"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PYGAME-MENU
A menu for pygame. Simple, and easy to use.
"""

__all__ = [

    # Common classes
    'BaseImage',
    'Menu',
    'Sound',
    'Theme'

]

# Check if pygame exists, if not maybe the module is being used by setup.py
__pygame_version__ = None
try:
    from pygame import version as __pygame_version__

    __pygame_version__ = __pygame_version__.vernum
except (ModuleNotFoundError, ImportError):
    pass

# Import modules that require pygame
if __pygame_version__ is not None:
    """
    BaseImage: Provides basic image loading and manipulation with pygame
    """
    import pygame_menu.baseimage  # lgtm [py/import-and-import-from]
    from pygame_menu.baseimage import BaseImage

    """
    Controls: Default controls of menu object and key definition
    """
    import pygame_menu.controls

    """
    Events: Menu events definition and locals
    """
    import pygame_menu.events

    """
    Fonts: Menu fonts
    """
    import pygame_menu.font

    """
    Locals: Local constants
    """
    import pygame_menu.locals

    """
    Menu: Menu class
    """
    from pygame_menu.menu import Menu

    """
    ScrollArea: Scrollarea class
    """
    import pygame_menu._scrollarea

    """
    Sound: Sound class
    """
    import pygame_menu.sound  # lgtm [py/import-and-import-from]
    from pygame_menu.sound import Sound

    """
    Themes: Menu themes
    """
    import pygame_menu.themes  # lgtm [py/import-and-import-from]
    from pygame_menu.themes import Theme

    """
    Widgets: Menu widgets
    """
    import pygame_menu.widgets

"""
Version: Library version
"""
import pygame_menu.version

"""
Metadata: Information about the project
"""
__author__ = 'Pablo Pizarro R.'
__contributors__ = [

    # Author
    'ppizarror',

    # Contributors
    'anxuae',
    'apuly',
    'arpruss',
    'asierrayk',
    'DA820',
    'eforgacs',
    'i96751414',
    'ironsmile',
    'jwllee',
    'maditnerd',
    'mrkprdo',
    'notrurs',
    'NullP01nt',
    'PandaRoux8',
    'Rifqi31',
    'thisIsMikeKane',
    'werdeil',
    'zPaw'

]
__copyright__ = 'Copyright 2017-2021 Pablo Pizarro R. @ppizarror'
__description__ = 'A menu for pygame. Simple, and easy to use'
__email__ = 'pablo@ppizarror.com'
__keywords__ = 'pygame menu menus gui widget input button pygame-menu image sound ui'
__license__ = 'MIT'
__module_name__ = 'pygame-menu'
__url__ = 'https://pygame-menu.readthedocs.io'
__url_bug_tracker__ = 'https://github.com/ppizarror/pygame-menu/issues'
__url_documentation__ = 'https://pygame-menu.readthedocs.io'
__url_source_code__ = 'https://github.com/ppizarror/pygame-menu'
__version__ = pygame_menu.version.ver

"""
Print pygame-menu version.
"""
import os

if 'PYGAME_MENU_HIDE_VERSION' not in os.environ and \
        'PYGAME_HIDE_SUPPORT_PROMPT' not in os.environ:
    print(f'{__module_name__} {__version__}')

# Cleanup namespace
del os
