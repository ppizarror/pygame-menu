# coding=utf-8
"""
LOCALS
Local constants.

Copyright (C) 2017-2018 Pablo Pizarro @ppizarror

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""


class PymenuAction(object):
    """
    Pymenu event.
    """

    def __init__(self, action):
        assert isinstance(action, int)
        self._action = action

    def __eq__(self, other):
        if isinstance(other, PymenuAction):
            return self._action == other._action
        return False


# Events
PYGAME_MENU_BACK = PymenuAction(0)  # Menu back
PYGAME_MENU_CLOSE = PymenuAction(1)  # Close menu
PYGAME_MENU_DISABLE_CLOSE = PymenuAction(10)  # Menu disable closing
PYGAME_MENU_EXIT = PymenuAction(3)  # Menu exit program
PYGAME_MENU_RESET = PymenuAction(4)  # Menu reset

# Other
PYGAMEMENU_PYMENUACTION = "<class 'pygameMenu.locals._PymenuAction'>"
PYGAMEMENU_TEXT_NEWLINE = ''  # Text newline on TextMenu object
PYGAMEMENU_TYPE_SELECTOR = PymenuAction(2)  # Type of selector

# Joypad
JOY_DEADZONE = 0.5
JOY_AXIS_Y = 1
JOY_AXIS_X = 0

JOY_CENTERED = (0, 0)
JOY_UP = (0, 1)
JOY_DOWN = (0, -1)
JOY_RIGHT = (1, 0)
JOY_LEFT = (-1, 0)

JOY_BUTTON_SELECT = 0
JOY_BUTTON_BACK = 1
