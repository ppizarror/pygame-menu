# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

UTILS
Test suite utilitary functions and classes.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

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

import pygame
import pygameMenu
import random

# noinspection PyUnresolvedReferences
import unittest

# Constants
FPS = 60  # Frames per second of the menu
H_SIZE = 600  # Window height
W_SIZE = 600  # Window width

# Init pygame
pygame.init()
surface = pygame.display.set_mode((W_SIZE, H_SIZE))


class PygameUtils(object):
    """
    Static class for pygame testing.
    """

    @staticmethod
    def joy_motion(x=0.0, y=0.0, inlist=True, testmode=True):
        """
        Create a pygame joy controller motion event.

        :param x: X axis movement
        :type x: float
        :param y: Y axis movement
        :type y: float
        :param inlist: Return event in a list
        :type inlist: bool
        :param testmode: Key event is in test mode
        :type testmode: bool
        :return: Event
        :rtype: pygame.event.Event
        """
        if x != 0 and y != 0:
            return [PygameUtils.joy_motion(x=x, y=0, inlist=False, testmode=testmode),
                    PygameUtils.joy_motion(x=0, y=y, inlist=False, testmode=testmode)]
        event_obj = None
        if x != 0:
            event_obj = pygame.event.Event(pygame.JOYAXISMOTION,
                                           {'value': x,
                                            'axis': pygameMenu.controls.JOY_AXIS_X,
                                            'test': testmode
                                            })
        if y != 0:
            event_obj = pygame.event.Event(pygame.JOYAXISMOTION,
                                           {'value': y,
                                            'axis': pygameMenu.controls.JOY_AXIS_Y,
                                            'test': testmode
                                            })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def joy_key(key, inlist=True, testmode=True):
        """
        Create a pygame joy controller key event.

        :param key: Key to press
        :type key: bool
        :param inlist: Return event in a list
        :type inlist: bool
        :param testmode: Key event is in test mode
        :type testmode: bool
        :return: Event
        :rtype: pygame.event.Event
        """
        event_obj = pygame.event.Event(pygame.JOYHATMOTION,
                                       {'value': key,
                                        'test': testmode
                                        })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def key(key, char=' ', inlist=True, keydown=False, keyup=False, testmode=True):
        """
        Create a keyboard event.

        :param key: Key to press
        :type key: int
        :param char: Char representing the key
        :type char: basestring
        :param inlist: Return event in a list
        :type inlist: bool
        :param keydown: Event is keydown
        :type keydown: bool
        :param keyup: Event is keyup
        :type keyup: bool
        :param testmode: Key event is in test mode
        :type testmode: bool
        :return: Event
        :rtype: pygame.event.Event
        """
        if keyup and keydown:
            raise ValueError('keyup and keydown cannot be active at the same time')
        if keydown == keyup and not keydown:
            raise ValueError('keyup and keydown cannot be false at the same time')
        event = -1
        if keydown:
            event = pygame.KEYDOWN
        if keyup:
            event = pygame.KEYUP
        event_obj = pygame.event.Event(event,
                                       {'key': key,
                                        'test': testmode,
                                        })
        if len(char) == 1:
            event_obj.dict['unicode'] = char
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def mouse_click(x, y, inlist=True):
        """
        Generate a mouse click event.

        :param x: X coordinate
        :type x: int, float
        :param y: Y coordinate
        :type y: int, float
        :param inlist: Return event in a list
        :type inlist: bool
        :return: Event
        :rtype: pygame.event.Event
        """
        event_obj = pygame.event.Event(pygame.MOUSEBUTTONUP,
                                       {'pos': [float(x), float(y)],
                                        'test': True
                                        })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def get_middle_rect(rect):
        """
        Get middle position from a rect.

        :param rect: Pygame rect
        :type rect: pygame.rect.Rect
        :return: Position as a list
        :rtype: list[float]
        """
        rect_obj = rect  # type: pygame.rect.Rect
        x1, y1 = rect_obj.bottomleft
        x2, y2 = rect_obj.topright

        x = float(x1 + x2) / 2
        y = float(y1 + y2) / 2
        return [x, y]


class PygameMenuUtils(object):
    """
    Static class for utilitary pygame-menu methods.
    """

    @staticmethod
    def get_font(name, size):
        """
        Returns a font.

        :param name: Font name
        :type name: basestring
        :param size: Font size
        :type size: int
        :return: Font
        :rtype: pygame.font.FontType
        """
        return pygameMenu.font.get_font(name, size)

    @staticmethod
    def get_library_fonts():
        """
        Return a test font from the library.

        :return: Font file
        :rtype: list[basestring]
        """
        return [
            pygameMenu.font.FONT_8BIT,
            pygameMenu.font.FONT_BEBAS,
            pygameMenu.font.FONT_COMIC_NEUE,
            pygameMenu.font.FONT_FRANCHISE,
            pygameMenu.font.FONT_HELVETICA,
            pygameMenu.font.FONT_MUNRO,
            pygameMenu.font.FONT_NEVIS,
            pygameMenu.font.FONT_OPEN_SANS,
            pygameMenu.font.FONT_PT_SERIF
        ]

    @staticmethod
    def random_font():
        """
        Retunrn a random font from the library.

        :return: Font file
        :rtype: basestring
        """
        fonts = PygameMenuUtils.get_library_fonts()
        opt = random.randrange(0, len(fonts))
        return fonts[opt]

    @staticmethod
    def load_font(font, size):
        """
        Load font from file.

        :param font: Font name
        :type font: basestring
        :param size: Font size
        :type size: int
        :return: Font object
        """
        return pygameMenu.font.get_font(font, size)

    @staticmethod
    def random_system_font():
        """
        Return random system font.

        :return: System font name
        :rtype: basestring
        """
        fonts = pygame.font.get_fonts()
        fonts.sort()
        fonts.pop(0)  # Python 2 first item is empty
        return fonts[random.randrange(0, len(fonts))]

    @staticmethod
    def generic_menu(title=''):
        """
        Generate a generic test menu.

        :param title: Menu title
        :type title: basestring
        :return: Menu
        :rtype: pygameMenu.Menu
        """
        return pygameMenu.Menu(surface,
                               dopause=False,
                               enabled=False,
                               font=pygameMenu.font.FONT_NEVIS,
                               fps=FPS,
                               menu_alpha=90,
                               title=title,
                               window_height=H_SIZE,
                               window_width=W_SIZE
                               )
