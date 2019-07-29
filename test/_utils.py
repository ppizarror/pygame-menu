"""
Test suite utils.
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
    def joy_motion(x=0.0, y=0.0, inlist=True):
        """
        Create a pygame joy controller motion event.

        :param x: X axis movement
        :type x: float
        :param y: Y axis movement
        :type y: float
        :param inlist: Return event in a list
        :type inlist: bool
        :return: Event
        :rtype: pygame.event.Event
        """
        if x != 0 and y != 0:
            return [PygameUtils.joy_motion(x=x, y=0, inlist=False),
                    PygameUtils.joy_motion(x=0, y=y, inlist=False)]
        event_obj = None
        if x != 0:
            event_obj = pygame.event.Event(pygame.JOYAXISMOTION,
                                           {"value": x,
                                            "axis": pygameMenu.controls.JOY_AXIS_X
                                            }
                                           )
        if y != 0:
            event_obj = pygame.event.Event(pygame.JOYAXISMOTION,
                                           {"value": y,
                                            "axis": pygameMenu.controls.JOY_AXIS_Y
                                            }
                                           )
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def joy_key(key, inlist=True):
        """
        Create a pygame joy controller key event.

        :param key: Key to press
        :type key: bool
        :param inlist: Return event in a list
        :type inlist: bool
        :return: Event
        :rtype: pygame.event.Event
        """
        event_obj = pygame.event.Event(pygame.JOYHATMOTION, {"value": key})
        if inlist:
            event_obj = [event_obj]
        return event_obj

    @staticmethod
    def key(key, inlist=True, keydown=False, keyup=False):
        """
        Create a keyboard event.

        :param key: Key to press
        :type key: int
        :param inlist: Return event in a list
        :type inlist: bool
        :param keydown: Event is keydown
        :type keydown: bool
        :param keyup: Event is keyup
        :type keyup: bool
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
        event_obj = pygame.event.Event(event, {"key": key})
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
        event_obj = pygame.event.Event(pygame.MOUSEBUTTONUP, {"pos": [float(x), float(y)]})
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

    @staticmethod
    def get_system_font():
        """
        Return random system font.

        :return: System font name
        :rtype: basestring
        """
        fonts = pygame.font.get_fonts()
        default_font = pygameMenu.fonts.FONT_8BIT
        if len(fonts) == 0:
            return default_font

        # Find a good font:
        i = 0
        while True:
            opt = random.randrange(0, len(fonts))
            font = str(fonts[opt])
            if len(font) > 0:
                return font
            else:
                i += 1
            if i == 10:  # In case anything fails
                return default_font


def create_generic_menu(title=''):
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
                           font=pygameMenu.fonts.FONT_NEVIS,
                           fps=FPS,
                           menu_alpha=90,
                           title=title,
                           window_height=H_SIZE,
                           window_width=W_SIZE
                           )
