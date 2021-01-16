"""
pygame-menu
https://github.com/ppizarror/pygame-menu

UTILS
Test suite utility functions and classes.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

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

from pygame_menu.custom_types import NumberType, Union, List, Tuple, \
    MenuColumnMaxWidthType, MenuColumnMinWidthType, Any, MenuRowsType

EventListType = Union['pygame.event.Event', List['pygame.event.Event']]

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


def test_reset_surface() -> None:
    """
    Reset test surface.

    :return: None
    """
    global surface
    surface = pygame.display.set_mode((W_SIZE, H_SIZE))


class PygameUtils(object):
    """
    Static class for pygame testing.
    """

    @staticmethod
    def joy_motion(x: NumberType = 0, y: NumberType = 0, inlist: bool = True, testmode: bool = True
                   ) -> EventListType:
        """
        Create a pygame joy controller motion event.

        :param x: X axis movement
        :param y: Y axis movement
        :param inlist: Return event in a list
        :param testmode: Key event is in test mode
        :return: Event
        """
        if x != 0 and y != 0:
            return [PygameUtils.joy_motion(x=x, inlist=False, testmode=testmode),
                    PygameUtils.joy_motion(y=y, inlist=False, testmode=testmode)]
        event_obj = None
        if x != 0:
            event_obj = pygame.event.Event(pygame.JOYAXISMOTION,
                                           {
                                               'value': x,
                                               'axis': pygame_menu.controls.JOY_AXIS_X,
                                               'test': testmode
                                           })
        if y != 0:
            event_obj = pygame.event.Event(pygame.JOYAXISMOTION,
                                           {
                                               'value': y,
                                               'axis': pygame_menu.controls.JOY_AXIS_Y,
                                               'test': testmode
                                           })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def test_widget_key_press(widget: 'pygame_menu.widgets.core.Widget') -> None:
        """
        Test keypress widget.

        :param widget: Widget object
        :return: None
        """
        widget.update(PygameUtils.key(pygame.K_BACKSPACE, keydown=True))
        widget.update(PygameUtils.key(pygame.K_DELETE, keydown=True))
        widget.update(PygameUtils.key(pygame.K_LEFT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_RIGHT, keydown=True))
        widget.update(PygameUtils.key(pygame.K_END, keydown=True))
        widget.update(PygameUtils.key(pygame.K_HOME, keydown=True))

    @staticmethod
    def joy_key(key: bool, inlist: bool = True, testmode: bool = True) -> EventListType:
        """
        Create a pygame joy controller key event.

        :param key: Key to press
        :param inlist: Return event in a list
        :param testmode: Key event is in test mode
        :return: Event
        """
        event_obj = pygame.event.Event(pygame.JOYHATMOTION,
                                       {
                                           'value': key,
                                           'test': testmode
                                       })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def keydown_mod_ctrl(key: int, inlist: bool = True) -> EventListType:
        """
        Create a mod ctrl keydown event (Ctrl+Key).

        :param key: Key to press
        :param inlist: Return event in a list
        :return: Event
        """
        # noinspection PyArgumentList
        pygame.key.set_mods(pygame.KMOD_CTRL)
        event_obj = pygame.event.Event(pygame.KEYDOWN,
                                       {
                                           'key': key,
                                           'test': True
                                       })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def key(key: int, char: str = ' ', inlist: bool = True,
            keydown: bool = False, keyup: bool = False, testmode: bool = True
            ) -> EventListType:
        """
        Create a keyboard event.

        :param key: Key to press
        :param char: Char representing the key
        :param inlist: Return event in a list
        :param keydown: Event is keydown
        :param keyup: Event is keyup
        :param testmode: Key event is in test mode
        :return: Event
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
                                       {
                                           'key': key,
                                           'test': testmode
                                       })
        if len(char) == 1:
            event_obj.dict['unicode'] = char
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def mouse_click(x: NumberType, y: NumberType, inlist: bool = True, evtype: int = pygame.MOUSEBUTTONUP
                    ) -> EventListType:
        """
        Generate a mouse click event.

        :param x: X coordinate (px)
        :param y: Y coordinate (px)
        :param inlist: Return event in a list
        :param evtype: event type
        :return: Event
        """
        event_obj = pygame.event.Event(evtype,
                                       {
                                           'pos': [float(x), float(y)],
                                           'test': True,
                                           'button': 3
                                       })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def touch_click(x: NumberType, y: NumberType, inlist: bool = True, evtype: int = pygame.FINGERUP,
                    normalize: bool = True, menu: Union['pygame_menu.Menu', None] = None) -> EventListType:
        """
        Generate a mouse click event.

        :param x: X coordinate
        :param y: Y coordinate
        :param inlist: Return event in a list
        :param evtype: Event type, it can be FINGERUP, FINGERDOWN or FINGERMOTION
        :param normalize: Normalize event position
        :param menu: Menu reference
        :return: Event
        """
        vmajor, _, _ = pygame.version.vernum
        assert vmajor >= 2, 'function only available in pygame v2+'
        if normalize:
            assert menu is not None, 'menu reference must be provided if normalize is used'
            display_size = menu.get_window_size()
            x /= float(display_size[0])
            y /= float(display_size[1])
        event_obj = pygame.event.Event(evtype,
                                       {
                                           'test': True,
                                           'x': float(x),
                                           'y': float(y)
                                       })
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def get_middle_rect(rect: 'pygame.Rect') -> Tuple[float, float]:
        """
        Get middle position from a rect.

        :param rect: Pygame rect
        :return: Position as a tuple
        """
        rect_obj = rect
        x1, y1 = rect_obj.bottomleft
        x2, y2 = rect_obj.topright

        x = float(x1 + x2) / 2
        y = float(y1 + y2) / 2
        return x, y


class MenuUtils(object):
    """
    Static class for utility pygame-menu methods.
    """

    @staticmethod
    def get_font(name: str, size: int) -> 'pygame.font.Font':
        """
        Returns a font.

        :param name: Font name
        :param size: Font size
        :return: Font
        """
        return pygame_menu.font.get_font(name, size)

    @staticmethod
    def get_library_fonts() -> List[str]:
        """
        Return a test font from the library.

        :return: Font file
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
    def random_font() -> str:
        """
        Return a random font from the library.

        :return: Font file
        """
        fonts = MenuUtils.get_library_fonts()
        opt = random.randrange(0, len(fonts))
        return fonts[opt]

    @staticmethod
    def load_font(font: str, size: int) -> 'pygame.font.Font':
        """
        Load font from file.

        :param font: Font name
        :param size: Font size
        :return: Font object
        """
        return pygame_menu.font.get_font(font, size)

    @staticmethod
    def random_system_font() -> str:
        """
        Return random system font.

        :return: System font name
        """
        fonts = pygame.font.get_fonts()
        fonts.sort()
        fonts.pop(0)
        return fonts[int(random.randrange(0, len(fonts)))]

    @staticmethod
    def generic_menu(
            center_content: bool = True,
            columns: int = 1,
            column_max_width: MenuColumnMaxWidthType = None,
            column_min_width: MenuColumnMinWidthType = 0,
            height: NumberType = 400,
            onclose: Any = None,
            position_x: NumberType = 50,
            position_y: NumberType = 50,
            rows: MenuRowsType = None,
            theme: 'pygame_menu.themes.Theme' = pygame_menu.themes.THEME_DEFAULT,
            title: str = '',
            width: NumberType = 600,
            *args,
            **kwargs
    ) -> 'pygame_menu.Menu':
        """
        Generate a generic test menu.

        :param center_content: Center menu content
        :param columns: Number of columns
        :param column_max_width: List/Tuple representing the maximum width of each column in px, ``None`` equals no limit. For example ``column_max_width=500`` (each column width can be 500px max), or ``column_max_width=(400, 500)`` (first column 400px, second 500). If ``0` is given uses the menu width. This method does not resize the widgets, only determines the dynamic width of the column layout
        :param column_min_width: List/Tuple representing the minimum width of each column in px. For example ``column_min_width=500`` (each column width is 500px min), or ``column_max_width=(400, 500)`` (first column 400px, second 500). By default it's ``0``. Negative values are not accepted
        :param height: Menu height (px)
        :param onclose: Event or function applied when closing the Menu
        :param position_x: X position of the menu
        :param position_y: Y position of the menu
        :param rows: Number of rows
        :param theme: Menu theme
        :param title: Menu title
        :param width: Menu width (px)
        :param args: Additional args
        :param kwargs: Optional keyword arguments
        :return: Menu
        """
        return pygame_menu.Menu(
            center_content=center_content,
            columns=columns,
            column_max_width=column_max_width,
            column_min_width=column_min_width,
            enabled=False,
            height=height,
            menu_position=(position_x, position_y),
            onclose=onclose,
            rows=rows,
            theme=theme,
            title=title,
            width=width,
            *args,
            **kwargs
        )

    @staticmethod
    def get_large_surface() -> 'pygame.Surface':
        """
        Create a large surface to test scrolls.

        :return: Surface
        """
        world = pygame.Surface((W_SIZE * 2, H_SIZE * 3))
        world.fill((200, 200, 200))
        for x in range(100, world.get_width(), 200):
            for y in range(100, world.get_height(), 200):
                pygame.draw.circle(world, (225, 34, 43), (x, y), 100, 10)
        return world
