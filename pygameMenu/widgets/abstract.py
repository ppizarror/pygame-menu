# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

WIDGET
Base class for widgets.

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

import os.path
import pygame as _pygame
import pygameMenu.config_menu as _cfg
from pygameMenu.locals import PYGAME_MENU_NOT_A_VALUE, PYGAME_ALIGN_CENTER, \
    PYGAME_ALIGN_LEFT, PYGAME_ALIGN_RIGHT
from uuid import uuid4


class Widget(object):
    """
    Widget abstract class.
    """

    def __init__(self,
                 widget_id='',
                 onchange=None,
                 onreturn=None,
                 args=None,
                 kwargs=None
                 ):
        """
        :param widget_id: Widget identifier
        :param onchange: callback when changing the selector
        :param onreturn: callback when pressing return button
        :param args: Optional arguments for callbacks
        :param kwargs: Optional keyword-arguments for callbacks
        :type widget_id: basestring
        :type onchange: function, NoneType
        :type onreturn: function, NoneType
        """

        # Store id, if None or empty create new ID based on UUID
        if widget_id is None or len(widget_id) == 0:
            widget_id = str(uuid4())
        self._id = widget_id
        self._surface = None  # Rendering surface
        self._rect = _pygame.Rect(0, 0, 0, 0)
        self._alignment = PYGAME_ALIGN_CENTER

        self._on_change = onchange
        self._on_return = onreturn
        self._args = args or []
        self._kwargs = kwargs or {}

        self._font = _cfg.MENU_FONT_SIZE_TITLE
        self._font_size = _cfg.MENU_FONT_SIZE
        self._font_color = _cfg.MENU_FONT_COLOR
        self._font_selected_color = _cfg.MENU_SELECTEDCOLOR

        self._shadow = _cfg.MENU_OPTION_SHADOW
        self._shadow_color = _cfg.SHADOW_COLOR

        # Public attributs
        self.joystick_enabled = True
        self.mouse_enabled = True
        self.selected = False

    def apply(self, *args):
        """
        Run 'on_return' callaback when return event. A callback function
        recieves the following arguments:

            callback_func( value, *args, *widget._args, **widget._kwargs )

        with:
            - ``value`` (if something is returned by ``get_value()``)
            - ``args`` given to this method
            - ``args`` of the widget
            - ``kwargs`` of the widget

        :param args: extra arguments passed to the callback
        :return: None
        """
        if self._on_return:
            args = list(args) + list(self._args)
            value = self.get_value()
            if value != '__not_a_value__':
                args.insert(0, value)
            self._on_return(*args, **self._kwargs)

    def change(self, *args):
        """
        Run 'on_change' callaback after change event is triggered. A callback function
        recieves the following arguments:

            callback_func( value, *args, *widget._args, **widget._kwargs )

        with:
            - ``value`` (if something is returned by ``get_value()``)
            - ``args`` given to this method
            - ``args`` of the widget
            - ``kwargs`` of the widget

        :param args: extra arguments passed to the callback
        :return: None
        """
        if self._on_change:
            args = list(args) + list(self._args)
            value = self.get_value()
            if value != '__not_a_value__':
                args.insert(0, value)
            self._on_change(*args, **self._kwargs)

    def draw(self, surface):
        """
        Draw the widget shape.

        :param surface: Surface to draw
        :return: None
        """
        raise NotImplementedError('Override is mandatory')

    def get_rect(self):
        """
        Return the Rect object.

        :return: pygame.Rect
        """
        self._render()

        self._rect.width, self._rect.height = self._surface.get_size()
        return self._rect

    def get_value(self):
        """
        Return the value. The string '__not_a_value__' is returned
        if this method has not been overwritten, this means no value
        will be passed to the callbacks.

        :return: value
        """
        return PYGAME_MENU_NOT_A_VALUE

    def get_id(self):
        """
        Returns widget id.

        :return: id
        """
        return self._id

    def _render(self):
        """
        Render the widget surface.

        This method shall update the attribute ``_surface`` with a pygame.Surface
        representing the outer borders of the widget.
        """
        raise NotImplementedError('Override is mandatory')

    def set_font(self, font, font_size, color, selected_color):
        """
        Set the texts font.

        :param font: Name or list of names for font (see pygame.font.match_font for precise format)
        :param font_size:  Size of font in pixels
        :param color: Text color
        :param selected_color: Text color when widget is selected
        """
        if isinstance(font, _pygame.font.Font):
            self._font = font
        else:
            if not os.path.isfile(font):
                font = _pygame.font.match_font(font)
            self._font = _pygame.font.Font(font, font_size)
        self._font_size = font_size
        self._font_color = color
        self._font_selected_color = selected_color

    def set_position(self, posx, posy):
        """
        Set the position.

        :param posx: X position
        :param posy: Y position
        """
        self._rect.x = posx
        self._rect.y = posy

    def set_alignment(self, align):
        """
        Set the alignment of the widget.

        :param align: center, left, right
        :type align: basestring
        :return: None
        """
        align = align.lower()
        if align not in [PYGAME_ALIGN_LEFT, PYGAME_ALIGN_CENTER, PYGAME_ALIGN_RIGHT]:
            raise Exception('Incorrect alignment of the widget')
        self._alignment = align

    def get_alignment(self):
        """
        Returns widget alignment.

        :return: Widget align
        :rtype: basestring
        """
        return self._alignment

    def set_selected(self, selected=True):
        """
        Mark the widget as selected.

        :param selected: Set item as selected
        :type selected: bool
        """
        self.selected = selected

    def set_shadow(self, enabled=True, color=None):
        """
        Show text shadow.

        :param enabled: Shadow is enabled or not
        :param color: Shadow color
        :type enabled: bool
        :type color: list, NoneType
        """
        self._shadow = enabled
        if color:
            self._shadow_color = color

    def set_controls(self, joystick=True, mouse=True):
        """
        Enable interfaces to control the widget.

        :param joystick: Use joystick
        :param mouse: Use mouse
        :type joystick: bool
        :type mouse: bool
        """
        self.joystick_enabled = joystick
        self.mouse_enabled = mouse

    def set_value(self, value):
        """
        Set the value.

        :param value: value to be set on the widget.
        :return: None
        """
        raise ValueError('Widget does not accept value')

    def update(self, events):
        """
        Update internal varibale according to the given events list.

        :param events: list of pygame events
        :return: True if updated
        """
        raise NotImplementedError('Override is mandatory')
