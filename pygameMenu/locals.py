# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

LOCALS
Local constants.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

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

__all__ = ['PYGAME_MENU_BACK', 'PYGAME_MENU_CLOSE', 'PYGAME_MENU_DISABLE_CLOSE',
           'PYGAME_MENU_EXIT', 'PYGAME_MENU_RESET', 'PYGAMEMENU_PYMENUACTION',
           'PYGAMEMENU_TEXT_NEWLINE', 'PYGAMEMENU_TYPE_BUTTON',
           'PYGAMEMENU_TYPE_SELECTOR', 'PYGAMEMENU_TYPE_TEXTINPUT', 'JOY_AXIS_X',
           'JOY_AXIS_Y', 'JOY_BUTTON_BACK', 'JOY_BUTTON_SELECT', 'JOY_CENTERED',
           'JOY_DEADZONE', 'JOY_DOWN', 'JOY_LEFT', 'JOY_RIGHT', 'JOY_UP',
           'PYGAME_ALIGN_CENTER', 'PYGAME_ALIGN_LEFT', 'PYGAME_ALIGN_RIGHT',
           'PYGAME_INPUT_FLOAT', 'PYGAME_INPUT_INT', 'PYGAME_INPUT_TEXT']


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
PYGAMEMENU_TYPE_BUTTON = PymenuAction(6)  # Type of button
PYGAMEMENU_TYPE_SELECTOR = PymenuAction(2)  # Type of selector
PYGAMEMENU_TYPE_TEXTINPUT = PymenuAction(5)  # Type of text input

# Joypad
JOY_AXIS_X = 0
JOY_AXIS_Y = 1
JOY_BUTTON_BACK = 1
JOY_BUTTON_SELECT = 0
JOY_CENTERED = (0, 0)
JOY_DEADZONE = 0.5
JOY_DOWN = (0, -1)
JOY_LEFT = (-1, 0)
JOY_RIGHT = (1, 0)
JOY_UP = (0, 1)

# Alignment
PYGAME_ALIGN_CENTER = '__pygameMenu_align_center__'
PYGAME_ALIGN_LEFT = '__pygameMenu_align_left__'
PYGAME_ALIGN_RIGHT = '__pygameMenu_align_right__'

# Input data type
PYGAME_INPUT_FLOAT = '__pygameMenu_input_float__'
PYGAME_INPUT_INT = '__pygameMenu_input_int__'
PYGAME_INPUT_TEXT = '__pygameMenu_input_text__'
