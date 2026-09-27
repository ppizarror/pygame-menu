"""
pygame-menu
https://github.com/ppizarror/pygame-menu

CONTROLS
Default controls of Menu object and key definition.
"""

from __future__ import annotations

__all__ = [
    # Joy pad
    "JOY_AXIS_X",
    "JOY_AXIS_Y",
    "JOY_BUTTON_BACK",
    "JOY_BUTTON_SELECT",
    "JOY_DEADZONE",
    "JOY_DELAY",
    "JOY_DOWN",
    "JOY_LEFT",
    "JOY_REPEAT",
    "JOY_RIGHT",
    "JOY_UP",
    # Keyboard events
    "KEY_APPLY",
    "KEY_BACK",
    "KEY_CLOSE_MENU",
    "KEY_DELETE",
    "KEY_END",
    "KEY_ESCAPE",
    "KEY_HOME",
    "KEY_LEFT",
    "KEY_MOVE_DOWN",
    "KEY_MOVE_UP",
    "KEY_RIGHT",
    "KEY_TAB",
    # Controller object
    "Controller",
]

from typing import TYPE_CHECKING, Union

# Imports
import pygame.locals as _locals

if TYPE_CHECKING:
    from pygame.event import Event as EventType

    from pygame_menu._types import Tuple2IntType

WidgetType = Union["pygame_menu.Menu", "pygame_menu.widgets.Widget"]  # type: ignore

# Joy pad
JOY_AXIS_X: int = 0
JOY_AXIS_Y: int = 1
JOY_BUTTON_BACK: int = 1
JOY_BUTTON_SELECT: int = 0
JOY_DEADZONE: float = 0.5
JOY_DELAY: int = 300  # ms
# Hat directions are matched exactly; diagonal hat values are ignored.
JOY_DOWN: Tuple2IntType = (0, -1)
JOY_LEFT: Tuple2IntType = (-1, 0)
JOY_REPEAT: int = 100  # ms
JOY_RIGHT: Tuple2IntType = (1, 0)
JOY_UP: Tuple2IntType = (0, 1)

# Keyboard events
KEY_APPLY = _locals.K_RETURN
KEY_BACK = _locals.K_BACKSPACE
KEY_CLOSE_MENU = _locals.K_ESCAPE
KEY_DELETE = _locals.K_DELETE
KEY_END = _locals.K_END
KEY_ESCAPE = _locals.K_ESCAPE
KEY_HOME = _locals.K_HOME
KEY_LEFT = _locals.K_LEFT

# Historical pygame-menu behavior:
# "move_down" is triggered by the physical Up key, and vice versa.
KEY_MOVE_DOWN = _locals.K_UP
KEY_MOVE_UP = _locals.K_DOWN
KEY_RIGHT = _locals.K_RIGHT
KEY_TAB = _locals.K_TAB


# noinspection PyUnusedLocal
class Controller:
    """
    Default keyboard and joystick event predicates used by menus.

    Each public method accepts a pygame event and a widget and returns whether
    the event matches the corresponding control.
    """

    joy_delay: int
    joy_repeat: int

    def __init__(self) -> None:
        self.joy_delay = JOY_DELAY
        self.joy_repeat = JOY_REPEAT

    @staticmethod
    def _key_pressed(event: EventType, key: int) -> bool:
        """Helper to check if an event is a matching KEYDOWN event."""
        return event.type == _locals.KEYDOWN and event.key == key

    @staticmethod
    def _joy_button_pressed(event: EventType, button: int) -> bool:
        """Helper to check if an event is a matching JOYBUTTONDOWN event."""
        return event.type == _locals.JOYBUTTONDOWN and event.button == button

    @staticmethod
    def apply(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts apply key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_APPLY)

    @staticmethod
    def back(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts back key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_BACK)

    @staticmethod
    def close_menu(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts close menu key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_CLOSE_MENU)

    @staticmethod
    def delete(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts delete key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_DELETE)

    @staticmethod
    def end(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts end key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_END)

    @staticmethod
    def escape(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts escape key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_ESCAPE)

    @staticmethod
    def home(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts home key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_HOME)

    @staticmethod
    def joy_axis_x_left(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts joy movement on x-axis (left direction). Requires ``pygame.JOYAXISMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return (
            event.type == _locals.JOYAXISMOTION
            and event.axis == JOY_AXIS_X
            and event.value < -JOY_DEADZONE
        )

    @staticmethod
    def joy_axis_x_right(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts joy movement on x-axis (right direction). Requires ``pygame.JOYAXISMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return (
            event.type == _locals.JOYAXISMOTION
            and event.axis == JOY_AXIS_X
            and event.value > JOY_DEADZONE
        )

    @staticmethod
    def joy_axis_y_down(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts joy movement on y-axis (down direction). Requires ``pygame.JOYAXISMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return (
            event.type == _locals.JOYAXISMOTION
            and event.axis == JOY_AXIS_Y
            and event.value > JOY_DEADZONE
        )

    @staticmethod
    def joy_axis_y_up(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts joy movement on y-axis (up direction). Requires ``pygame.JOYAXISMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return (
            event.type == _locals.JOYAXISMOTION
            and event.axis == JOY_AXIS_Y
            and event.value < -JOY_DEADZONE
        )

    @staticmethod
    def joy_back(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts joy back button. Requires ``pygame.JOYBUTTONDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._joy_button_pressed(event, JOY_BUTTON_BACK)

    @staticmethod
    def joy_down(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts joy movement to down direction. Requires ``pygame.JOYHATMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.type == _locals.JOYHATMOTION and event.value == JOY_DOWN

    @staticmethod
    def joy_left(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts joy movement to left direction. Requires ``pygame.JOYHATMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.type == _locals.JOYHATMOTION and event.value == JOY_LEFT

    @staticmethod
    def joy_right(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts joy movement to right direction. Requires ``pygame.JOYHATMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.type == _locals.JOYHATMOTION and event.value == JOY_RIGHT

    @staticmethod
    def joy_select(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts joy select button. Also used for apply(). Requires ``pygame.JOYBUTTONDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._joy_button_pressed(event, JOY_BUTTON_SELECT)

    @staticmethod
    def joy_up(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts joy movement to up direction. Requires ``pygame.JOYHATMOTION``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return event.type == _locals.JOYHATMOTION and event.value == JOY_UP

    @staticmethod
    def left(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts left key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_LEFT)

    @staticmethod
    def move_down(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts move down key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_MOVE_DOWN)

    @staticmethod
    def move_up(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts move up key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_MOVE_UP)

    @staticmethod
    def right(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts right key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_RIGHT)

    @staticmethod
    def tab(event: EventType, widget: WidgetType) -> bool:
        """
        Accepts tab key. Requires ``pygame.KEYDOWN``.

        :param event: Event
        :param widget: Widget that accepts the event
        :return: True if event matches
        """
        return Controller._key_pressed(event, KEY_TAB)
