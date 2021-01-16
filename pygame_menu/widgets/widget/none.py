# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERTICAL MARGIN
Vertical box margin.

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

from pygame_menu.utils import make_surface
from pygame_menu.widgets.core import Widget

import pygame


# noinspection PyMissingOrEmptyDocstring
class NoneWidget(Widget):
    """
    None widget. Usefull if used for filling column/row layout.

    .. note::

        This widget does not implement any transformation.

    :param widget_id: ID of the widget
    :type widget_id: str
    """

    def __init__(self, widget_id=''):
        super(NoneWidget, self).__init__(widget_id=widget_id)
        self.is_selectable = False
        self._surface = make_surface(0, 0, alpha=True)

    def _apply_font(self):
        pass

    def set_padding(self, padding):  # Don't accept padding
        pass

    def set_title(self, title):
        pass

    def get_rect(self, inflate=None, apply_padding=True, use_transformed_padding=True):
        return pygame.Rect(0, 0, 0, 0)

    def set_background_color(self, color, inflate=(0, 0)):
        pass

    def _fill_background_color(self, surface):
        pass

    def set_selection_effect(self, selection):
        pass

    def apply(self, *args):
        pass

    def change(self, *args):
        pass

    def draw(self, surface):
        self.apply_draw_callbacks()

    def _render(self):
        pass

    def draw_selection(self, surface):
        pass

    def set_margin(self, x, y):
        pass

    def _apply_transforms(self):
        pass

    def set_font(self, font, font_size, color, selected_color, background_color, antialias=True):
        pass

    def update_font(self, style):
        pass

    def set_position(self, posx, posy):
        pass

    def flip(self, x, y):
        pass

    def set_max_width(self, width, scale_height=False, smooth=True):
        pass

    def set_max_height(self, height, scale_width=False, smooth=True):
        pass

    def scale(self, width, height, smooth=True):
        pass

    def resize(self, width, height, smooth=False):
        pass

    def translate(self, x, y):
        pass

    def rotate(self, angle):
        pass

    def set_alignment(self, align):
        pass

    def select(self, select=True, update_menu=False):
        pass

    def set_shadow(self, enabled=True, color=None, position=None, offset=None):
        pass

    def set_sound(self, sound):
        pass

    def set_controls(self, joystick=True, mouse=True, touchscreen=True):
        pass

    def set_value(self, value):
        pass

    def update(self, events):
        return False

    def add_update_callback(self, update_callback):
        pass

    def remove_update_callback(self, callback_id):
        pass

    def apply_update_callbacks(self):
        pass
