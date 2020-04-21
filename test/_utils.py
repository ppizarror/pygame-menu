# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

UTILS
Test suite utility functions and classes.

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
import pygame_menu
import random

# noinspection PyUnresolvedReferences
from pygame_menu.utils import dummy_function

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
        :rtype: :py:class:`pygame.event.Event`
        """
        if x != 0 and y != 0:
            return [PygameUtils.joy_motion(x=x, y=0, inlist=False, testmode=testmode),
                    PygameUtils.joy_motion(x=0, y=y, inlist=False, testmode=testmode)]
        event_obj = None
        if x != 0:
            event_obj = pygame.event.Event(pygame.JOYAXISMOTION,
                                           {'value': x,
                                            'axis': pygame_menu.controls.JOY_AXIS_X,
                                            'test': testmode
                                            })
        if y != 0:
            event_obj = pygame.event.Event(pygame.JOYAXISMOTION,
                                           {'value': y,
                                            'axis': pygame_menu.controls.JOY_AXIS_Y,
                                            'test': testmode
                                            })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def test_widget_key_press(widget):
        """
        Test keypress widget.

        :param widget: Widget object
        :type widget: :py:class:`pygame_menu.widgets.core.widget.Widget`
        """
        widget.update(PygameUtils.key(pygame.K_BACKSPACE, keydown=True))
        widget.update(PygameUtils.key(pygame.K_DELETE, keydown=True))
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_RIGHT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_END, keydown=True))
        widget.update(PygameUtils.key(pygame.K_HOME, keydown=True))

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
        :rtype: :py:class:`pygame.event.Event`
        """
        event_obj = pygame.event.Event(pygame.JOYHATMOTION,
                                       {'value': key,
                                        'test': testmode
                                        })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def keydown_mod_ctrl(key, inlist=True):
        """
        Create a mod ctrl keydown event (Ctrl+Key).

        :param key: Key to press
        :type key: int
        :param inlist: Return event in a list
        :type inlist: bool
        :return: Event
        :rtype: :py:class:`pygame.event.Event`
        """
        pygame.key.set_mods(pygame.KMOD_CTRL)
        event_obj = pygame.event.Event(pygame.KEYDOWN,
                                       {'key': key,
                                        'test': True,
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
        :type char: str
        :param inlist: Return event in a list
        :type inlist: bool
        :param keydown: Event is keydown
        :type keydown: bool
        :param keyup: Event is keyup
        :type keyup: bool
        :param testmode: Key event is in test mode
        :type testmode: bool
        :return: Event
        :rtype: :py:class:`pygame.event.Event`
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
    def mouse_click(x, y, inlist=True, evtype=pygame.MOUSEBUTTONUP):
        """
        Generate a mouse click event.

        :param x: X coordinate
        :type x: int, float
        :param y: Y coordinate
        :type y: int, float
        :param inlist: Return event in a list
        :type inlist: bool
        :param evtype: event type
        :type evtype: int
        :return: Event
        :rtype: :py:class:`pygame.event.Event`
        """
        event_obj = pygame.event.Event(evtype,
                                       {'pos': [float(x), float(y)],
                                        'test': True,
                                        'button': 3
                                        })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def get_middle_rect(rect):
        """
        Get middle position from a rect.

        :param rect: Pygame rect
        :type rect: :py:class:`pygame.rect.Rect`
        :return: Position as a list
        :rtype: list[float]
        """
        rect_obj = rect  # type: pygame.rect.Rect
        x1, y1 = rect_obj.bottomleft
        x2, y2 = rect_obj.topright

        x = float(x1 + x2) / 2
        y = float(y1 + y2) / 2
        return [x, y]


class MenuUtils(object):
    """
    Static class for utility pygame-menu methods.
    """

    @staticmethod
    def get_font(name, size):
        """
        Returns a font.

        :param name: Font name
        :type name: str
        :param size: Font size
        :type size: int
        :return: Font
        :rtype: :py:class:`pygame.font.Font`
        """
        return pygame_menu.font.get_font(name, size)

    @staticmethod
    def get_library_fonts():
        """
        Return a test font from the library.

        :return: Font file
        :rtype: list[str]
        """
        return [
            pygame_menu.font.FONT_8BIT,
            pygame_menu.font.FONT_BEBAS,
            pygame_menu.font.FONT_COMIC_NEUE,
            pygame_menu.font.FONT_FRANCHISE,
            pygame_menu.font.FONT_HELVETICA,
            pygame_menu.font.FONT_MUNRO,
            pygame_menu.font.FONT_NEVIS,
            pygame_menu.font.FONT_OPEN_SANS,
            pygame_menu.font.FONT_PT_SERIF
        ]

    @staticmethod
    def random_font():
        """
        Return a random font from the library.

        :return: Font file
        :rtype: str
        """
        fonts = MenuUtils.get_library_fonts()
        opt = random.randrange(0, len(fonts))
        return fonts[opt]

    @staticmethod
    def load_font(font, size):
        """
        Load font from file.

        :param font: Font name
        :type font: str
        :param size: Font size
        :type size: int
        :return: Font object
        :rtype: :py:class:`pygame.font.Font`
        """
        return pygame_menu.font.get_font(font, size)

    @staticmethod
    def random_system_font():
        """
        Return random system font.

        :return: System font name
        :rtype: str
        """
        fonts = pygame.font.get_fonts()
        fonts.sort()
        fonts.pop(0)  # Python 2 first item is empty
        return fonts[random.randrange(0, len(fonts))]

    @staticmethod
    def generic_menu(
            title='',
            columns=1,
            rows=None,
            width=600,
            height=400,
            position_x=50,
            position_y=50,
            *args,
            **kwargs):
        """
        Generate a generic test menu.

        :param title: Menu title
        :type title: str
        :param columns: Number of columns
        :type columns: int
        :param rows: Number of rows
        :type rows: int, None
        :param width: Menu width (px)
        :type width: int
        :param height: Menu height (px)
        :type height: int
        :param position_x: X position of the menu
        :type position_x: int, float
        :param position_y: Y position of the menu
        :type position_y: int, float
        :param args: Additional args
        :param kwargs: Additional key parameters
        :type kwargs: dict
        :return: Menu
        :rtype: :py:class:`pygame_menu.Menu`
        """
        return pygame_menu.Menu(
            columns=columns,
            enabled=False,
            height=height,
            menu_position=(position_x, position_y),
            width=width,
            rows=rows,
            title=title,
            *args,
            **kwargs
        )

    @staticmethod
    def get_large_surface():
        """
        Create a large surface to tst scrolls.
        """
        world = pygame.Surface((W_SIZE * 2, H_SIZE * 3))
        world.fill((200, 200, 200))
        for x in range(100, world.get_width(), 200):
            for y in range(100, world.get_height(), 200):
                pygame.draw.circle(world, (225, 34, 43), (x, y), 100, 10)
        return world
