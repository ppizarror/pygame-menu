# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

WIDGET
This module contains the widgets of pygame-menu.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

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

# Widgets
from pygame_menu.widgets.widget.button import Button
from pygame_menu.widgets.widget.colorinput import ColorInput
from pygame_menu.widgets.widget.image import Image
from pygame_menu.widgets.widget.label import Label
from pygame_menu.widgets.widget.scrollbar import ScrollBar
from pygame_menu.widgets.widget.selector import Selector
from pygame_menu.widgets.widget.textinput import TextInput
from pygame_menu.widgets.widget.vmargin import VMargin

# Menubar and positions
from pygame_menu.widgets.widget.menubar import MenuBar, MENUBAR_STYLE_ADAPTIVE, MENUBAR_STYLE_SIMPLE, \
    MENUBAR_STYLE_TITLE_ONLY, MENUBAR_STYLE_TITLE_ONLY_DIAGONAL, MENUBAR_STYLE_NONE, MENUBAR_STYLE_UNDERLINE, \
    MENUBAR_STYLE_UNDERLINE_TITLE
