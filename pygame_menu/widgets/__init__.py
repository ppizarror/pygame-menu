"""
pygame-menu
https://github.com/ppizarror/pygame-menu

WIDGETS
Widgets elements that can be added to the Menu.
"""

# Widgets core
import pygame_menu.widgets.core  # lgtm [py/import-and-import-from]
from pygame_menu.widgets.core import Widget

# Selection
from pygame_menu.widgets.selection import HighlightSelection, LeftArrowSelection, \
    NoneSelection, RightArrowSelection, SimpleSelection

# Widgets
from pygame_menu.widgets.widget import Button, ColorInput, DropSelect, \
    DropSelectMultiple, Frame, HMargin, Image, Label, MenuBar, MenuLink, NoneWidget, \
    ProgressBar, RangeSlider, ScrollBar, Selector, SurfaceWidget, Table, TextInput, \
    ToggleSwitch, VMargin

# Widget constants
from pygame_menu.widgets.widget.colorinput import COLORINPUT_TYPE_RGB, \
    COLORINPUT_TYPE_HEX, COLORINPUT_HEX_FORMAT_UPPER, COLORINPUT_HEX_FORMAT_NONE, \
    COLORINPUT_HEX_FORMAT_LOWER

from pygame_menu.widgets.widget.dropselect_multiple import \
    DROPSELECT_MULTIPLE_SFORMAT_TOTAL, DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA, \
    DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN

from pygame_menu.widgets.widget.frame import FRAME_DEFAULT_TITLE_BACKGROUND_COLOR, \
    FRAME_TITLE_BUTTON_CLOSE, FRAME_TITLE_BUTTON_MAXIMIZE, FRAME_TITLE_BUTTON_MINIMIZE

from pygame_menu.widgets.widget.menubar import MENUBAR_STYLE_ADAPTIVE, \
    MENUBAR_STYLE_SIMPLE, MENUBAR_STYLE_TITLE_ONLY, MENUBAR_STYLE_TITLE_ONLY_DIAGONAL, \
    MENUBAR_STYLE_NONE, MENUBAR_STYLE_UNDERLINE, MENUBAR_STYLE_UNDERLINE_TITLE

from pygame_menu.widgets.widget.selector import SELECTOR_STYLE_CLASSIC, \
    SELECTOR_STYLE_FANCY
