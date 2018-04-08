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


_PYGAME_TYPE_SELECTOR = PymenuAction(2)  # Type of selector
PYGAME_MENU_BACK = PymenuAction(0)  # Menu back
PYGAME_MENU_CLOSE = PymenuAction(1)  # Close menu
PYGAME_MENU_DISABLE_CLOSE = PymenuAction(10)  # Menu disable closing
PYGAME_MENU_EXIT = PymenuAction(3)  # Menu exit program
PYGAME_MENU_RESET = PymenuAction(4)  # Menu reset
TEXT_NEWLINE = ''  # Text newline on TextMenu object
