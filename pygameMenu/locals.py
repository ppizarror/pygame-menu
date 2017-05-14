# coding=utf-8
"""
LOCALS
Local constants.

Copyright (C) 2017 Pablo Pizarro @ppizarror

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""


class _PymenuAction(object):
    def __init__(self, action):
        assert isinstance(action, int)
        self._action = action

    # noinspection PyProtectedMember
    def __eq__(self, other):
        if isinstance(other, _PymenuAction):
            return self._action == other._action
        return False


# noinspection PyProtectedMember
def _eq_action(action1, action2):
    return action1._action == action2._action


# Menu back
PYGAME_MENU_BACK = _PymenuAction(0)

# Close menu
PYGAME_MENU_CLOSE = _PymenuAction(1)

# Menu exit program
PYGAME_MENU_EXIT = _PymenuAction(3)

# Menu disable closing
PYGAME_MENU_DISABLE_CLOSE = _PymenuAction(10)

# Menu reset
PYGAME_MENU_RESET = _PymenuAction(4)

# Type of selector
_PYGAME_TYPE_SELECTOR = _PymenuAction(2)

# Text newline on TextMenu object
TEXT_NEWLINE = ''
