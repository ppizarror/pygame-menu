"""
pygame-menu
https://github.com/ppizarror/pygame-menu

WIDGETS
Widgets elements that can be added to the Menu.

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

# Widgets core
import pygame_menu.widgets.core  # lgtm [py/import-and-import-from]
from pygame_menu.widgets.core import Widget

# Selection
from pygame_menu.widgets.selection import HighlightSelection, LeftArrowSelection, \
    NoneSelection, RightArrowSelection

# Widgets
from pygame_menu.widgets.widget import Button, ColorInput, DropSelect, \
    DropSelectMultiple, Frame, HMargin, Image, Label, MenuBar, NoneWidget, ScrollBar, \
    Selector, SurfaceWidget, Table, TextInput, ToggleSwitch, VMargin

# Widget constants
from pygame_menu.widgets.widget.colorinput import COLORINPUT_TYPE_RGB, \
    COLORINPUT_TYPE_HEX, COLORINPUT_HEX_FORMAT_UPPER, COLORINPUT_HEX_FORMAT_NONE, \
    COLORINPUT_HEX_FORMAT_LOWER

from pygame_menu.widgets.widget.frame import FRAME_DEFAULT_TITLE_BACKGROUND_COLOR, \
    FRAME_TITLE_BUTTON_CLOSE, FRAME_TITLE_BUTTON_MAXIMIZE, FRAME_TITLE_BUTTON_MINIMIZE

from pygame_menu.widgets.widget.menubar import MENUBAR_STYLE_ADAPTIVE, \
    MENUBAR_STYLE_SIMPLE, MENUBAR_STYLE_TITLE_ONLY, MENUBAR_STYLE_TITLE_ONLY_DIAGONAL, \
    MENUBAR_STYLE_NONE, MENUBAR_STYLE_UNDERLINE, MENUBAR_STYLE_UNDERLINE_TITLE

from pygame_menu.widgets.widget.selector import SELECTOR_STYLE_CLASSIC, \
    SELECTOR_STYLE_FANCY
