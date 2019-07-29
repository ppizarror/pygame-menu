# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

CONTROLS
Default controls of menu object and key definition.

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

# Import pygame locals
import pygame.locals as __locals

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

# Keyboard events
KEY_APPLY = __locals.K_RETURN
KEY_BACK = __locals.K_BACKSPACE
KEY_CLOSE_MENU = __locals.K_ESCAPE
KEY_LEFT = __locals.K_LEFT
KEY_MOVE_DOWN = __locals.K_UP
KEY_MOVE_UP = __locals.K_DOWN
KEY_RIGHT = __locals.K_RIGHT
