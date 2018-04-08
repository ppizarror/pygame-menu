# coding=utf-8
"""
CONTROLS
Default controls of Menu object.

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

# Import locals
import pygame.locals as __locals

# Controls
MENU_CTRL_BACK = __locals.K_BACKSPACE
MENU_CTRL_CLOSE_MENU = __locals.K_ESCAPE
MENU_CTRL_DOWN = __locals.K_UP
MENU_CTRL_ENTER = __locals.K_RETURN
MENU_CTRL_LEFT = __locals.K_LEFT
MENU_CTRL_RIGHT = __locals.K_RIGHT
MENU_CTRL_UP = __locals.K_DOWN

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
