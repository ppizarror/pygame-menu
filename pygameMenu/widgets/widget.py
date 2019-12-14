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

import pygame as _pygame
from uuid import uuid4

from pygameMenu.sound import Sound as _Sound
import pygameMenu.config as _cfg
import pygameMenu.locals as _locals
import pygameMenu.font as _fonts


# noinspection PyTypeChecker
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
        :type widget_id: basestring
        :param onchange: Callback when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Callback when pressing return button
        :type onreturn: function, NoneType
        :param args: Optional arguments for callbacks
        :param kwargs: Optional keyword-arguments for callbacks
        """

        assert isinstance(widget_id, str)
        if onchange:
            assert callable(onchange), 'onchange must be a function or None'
        if onreturn:
            assert callable(onreturn), 'onreturn must be a function or None'

        # Store id, if None or empty create new ID based on UUID
        if widget_id is None or len(widget_id) == 0:
            widget_id = uuid4()
        self._alignment = _locals.ALIGN_CENTER
        self._fps = 0
        self._id = str(widget_id)
        self._last_selected_surface = None  # type: _pygame.SurfaceType
        self._selected_rect = None  # type: _pygame.rect.RectType
        self._rect = _pygame.Rect(0, 0, 0, 0)
        self._render_string_cache = 0
        self._render_string_cache_surface = None
        self._surface = None  # type: _pygame.SurfaceType

        self._args = args or []
        self._kwargs = kwargs or {}
        self._on_change = onchange
        self._on_return = onreturn

        # Menu reference
        self._menu = None

        # Modified in set_font() method
        self._font = _cfg.MENU_FONT_SIZE_TITLE
        self._font_size = _cfg.MENU_FONT_SIZE
        self._font_color = _cfg.MENU_FONT_COLOR
        self._font_selected_color = _cfg.MENU_SELECTEDCOLOR
        self._font_antialias = True

        # Text shadow
        self._shadow = _cfg.MENU_OPTION_SHADOW
        self._shadow_color = _cfg.MENU_SHADOW_COLOR
        self._shadow_offset = _cfg.MENU_SHADOW_OFFSET
        self._shadow_position = _cfg.MENU_SHADOW_POSITION
        self._create_shadow_tuple()

        # Public attributs
        self.joystick_enabled = True
        self.mouse_enabled = True
        self.selected = False
        self.sound = _Sound()

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

        :param args: Extra arguments passed to the callback
        :return: None
        """
        if self._on_return:
            args = list(args) + list(self._args)
            try:
                args.insert(0, self.get_value())
            except ValueError:
                pass
            return self._on_return(*args, **self._kwargs)

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

        :param args: Extra arguments passed to the callback
        :return: None
        """
        if self._on_change:
            args = list(args) + list(self._args)
            try:
                args.insert(0, self.get_value())
            except ValueError:
                pass
            return self._on_change(*args, **self._kwargs)

    def draw(self, surface):
        """
        Draw the widget shape.

        :param surface: Surface to draw
        :type surface: pygame.surface.SurfaceType
        :return: None
        """
        raise NotImplementedError('Override is mandatory')

    def draw_selected_rect(self, surface, selected_color, inflatex, inflatey, border_width):
        """
        Draw selected rect around widget.

        :param surface: Surface to draw
        :type surface: pygame.surface.SurfaceType
        :param selected_color: Selected color
        :type selected_color: tuple
        :param inflatex: Pixels to inflate the rect (x axis)
        :type inflatex: int
        :param inflatey: Pixels to inflate the rect (y axis)
        :type inflatey: int
        :param border_width: Border rect width
        :type border_width: int
        :return: None
        """
        # Generate new rect if it's different
        rect = self._selected_rect

        if self._last_selected_surface != self._surface:  # If surface changed
            self._last_selected_surface = self._surface
            self._selected_rect = self._rect.copy()

            # Inflate rect
            self._selected_rect = self._selected_rect.inflate(inflatex, inflatey)

            # Translate rect
            self._selected_rect = self._selected_rect.move(0, -1)

            # Update rect
            rect = self._selected_rect

        # Draw rect
        _pygame.draw.rect(surface,
                          selected_color,
                          rect,
                          border_width)

    def get_rect(self):
        """
        Return the Rect object.

        :return: pygame.Rect
        :rtype: pygame.rect.RectType
        """
        self._render()
        self._rect.width, self._rect.height = self._surface.get_size()
        return self._rect

    def get_value(self):
        """
        Return the value. If exception ``ValueError`` is raised,
        no value will be passed to the callbacks.

        :return: value
        :rtype: Object
        """
        raise ValueError('{}({}) does not accept value'.format(self.__class__.__name__,
                                                               self.get_id()))

    def get_id(self):
        """
        Returns widget ID.

        :return: ID
        :rtype: basestring
        """
        return self._id

    def _render(self):
        """
        Render the widget surface.

        This method shall update the attribute ``_surface`` with a pygame.Surface
        representing the outer borders of the widget.
        """
        raise NotImplementedError('Override is mandatory')

    @staticmethod
    def hash_variables(*args):
        """
        Compute hash from a series of variables.

        :param args: Variables to compute hash
        :type args: Object
        :return: hash data
        :rtype: int
        """
        return hash(args)

    def font_render_string(self, text, color=(0, 0, 0)):
        """
        Render text.

        :param text: Text to render
        :type text: basestring
        :param color: Text color
        :type color: tuple
        :return: Text surface
        :rtype: pygame.surface.SurfaceType
        """
        assert isinstance(color, tuple)
        return self._font.render(text, self._font_antialias, color)

    def render_string(self, string, color):
        """
        Render text and turn it into a surface.

        :param string: Text to render
        :type string: basestring
        :param color: Text color
        :type color: tuple
        :return: Text surface
        :rtype: pygame.surface.SurfaceType
        """
        render_hash = self.hash_variables(string, color)
        if render_hash != self._render_string_cache:  # If render changed

            text = self.font_render_string(string, color)

            # Create surface
            size = (text.get_width() + 2, text.get_height() + 2)
            surface = _pygame.Surface(size, _pygame.SRCALPHA, 32)  # lgtm [py/call/wrong-arguments]
            surface = _pygame.Surface.convert_alpha(surface)  # type: _pygame.SurfaceType

            # Draw shadow first
            if self._shadow:
                text_bg = self._font.render(string, self._font_antialias, self._shadow_color)
                surface.blit(text_bg, self._shadow_tuple)
            surface.blit(text, (0, 0))

            self._render_string_cache = render_hash
            self._render_string_cache_surface = surface

        # Return rendered surface
        return self._render_string_cache_surface

    def set_font(self, font, font_size, color, selected_color, antialias=True):
        """
        Set the text font.

        :param font: Name or list of names for font (see pygame.font.match_font for precise format)
        :type font: basestring, list
        :param font_size: Size of font in pixels
        :type font_size: int
        :param color: Text color
        :type color: tuple
        :param selected_color: Text color when widget is selected
        :type selected_color: tuple
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :type antialias: bool
        :return: None
        """
        assert isinstance(font, str)
        assert isinstance(font_size, int)
        assert isinstance(color, tuple)
        assert isinstance(selected_color, tuple)
        assert isinstance(antialias, bool)
        self._font = _fonts.get_font(font, font_size)
        self._font_size = font_size
        self._font_color = color
        self._font_selected_color = selected_color
        self._font_antialias = antialias
        self._apply_font()

    def set_menu(self, menu):
        """
        Set menu reference.

        :param menu: Menu object
        :type menu: pygameMenu.menu.Menu
        :return: None
        """
        self._menu = menu

    def get_menu(self):
        """
        Return menu reference (if exists).

        :return: Menu reference
        :rtype: pygameMenu.menu.Menu
        """
        return self._menu

    def _apply_font(self):
        """
        Function triggered after a font is applied to the widget.

        :return: None
        """
        raise NotImplementedError('Override is mandatory')

    def set_position(self, posx, posy):
        """
        Set the position.

        :param posx: X position
        :type posx: int, float
        :param posy: Y position
        :type posy: int, float
        :return: None
        """
        self._rect.x = posx
        self._rect.y = posy

    def set_alignment(self, align):
        """
        Set the alignment of the widget.

        :param align: Widget align, could be ALIGN_LEFT/CENTER/RIGHT
        :type align: basestring
        :return: None
        """
        align = str(align)
        if align not in [_locals.ALIGN_LEFT,
                         _locals.ALIGN_CENTER,
                         _locals.ALIGN_RIGHT]:
            raise ValueError('Incorrect alignment of the widget')
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
        :return: None
        """
        self.selected = selected
        if selected:
            self._focus()
        else:
            self._blur()

    @staticmethod
    def check_key_pressed_valid(event):
        """
        Checks if the pressed key is valid.

        :param event: Key press event
        :type event: pygame.event.EventType
        :return: True if a key is pressed
        :rtype: bool
        """
        # If the system detects that any key event has been pressed but
        # there's not any key pressed then this method raises a KEYUP
        # flag
        bad_event = not (True in _pygame.key.get_pressed())
        if bad_event:
            if 'test' in event.dict and event.dict['test']:
                return True
            ev = _pygame.event.Event(_pygame.KEYUP, {'key': event.key})
            _pygame.event.post(ev)
        return not bad_event

    def _focus(self):
        """
        Function that is executed when the widget receives a focus (is selected).

        :return: None
        """
        pass

    def _blur(self):
        """
        Function that is executed when the widget loses the focus.

        :return: None
        """
        pass

    def set_shadow(self, enabled=True, color=None, position=None, offset=None):
        """
        Show text shadow.

        :param enabled: Shadow is enabled or not
        :type enabled: bool
        :param color: Shadow color
        :type color: list, NoneType
        :param position: Shadow position
        :type position: basestring, NoneType
        :param offset: Shadow offset
        :type offset: int, NoneType
        :return: None
        """
        self._shadow = enabled
        if color is not None:
            self._shadow_color = color
        if position is not None:
            if position not in [_locals.POSITION_WEST, _locals.POSITION_SOUTHWEST,
                                _locals.POSITION_SOUTH, _locals.POSITION_SOUTHEAST,
                                _locals.POSITION_EAST, _locals.POSITION_NORTH,
                                _locals.POSITION_NORTHWEST, _locals.POSITION_NORTHEAST]:
                raise ValueError('Incorrect shadow position of the widget')
            self._shadow_position = position
        if offset is not None:
            try:
                offset = int(offset)
            except ValueError:
                raise TypeError('Shadow offset must be integer')
            if offset <= 0:
                raise ValueError('Shadow offset must be greater than zero')
            self._shadow_offset = offset

        # Create shadow tuple position
        self._create_shadow_tuple()

    def set_fps(self, fps):
        """
        Set the FPS limit of the widget.

        :param fps: FPS (Frames Per Second) limit of the widget
        :type fps: float, int
        :return: None
        """
        self._fps = float(fps)

    def set_sound(self, sound):
        """
        Set sound engine to the widget.

        :param sound: Sound object
        :type sound: pygameMenu.sound.Sound
        :return: None
        """
        self.sound = sound

    def get_fps(self):
        """
        Return the FPS limit of the widget.

        :return: FPS limit
        :rtype: float
        """
        return self._fps

    def _create_shadow_tuple(self):
        """
        Create shadow position tuple.

        :return: None
        """
        x = 0
        y = 0
        if self._shadow_position == _locals.POSITION_NORTHWEST:
            x = -1
            y = -1
        elif self._shadow_position == _locals.POSITION_NORTH:
            y = -1
        elif self._shadow_position == _locals.POSITION_NORTHEAST:
            x = 1
            y = -1
        elif self._shadow_position == _locals.POSITION_EAST:
            x = 1
        elif self._shadow_position == _locals.POSITION_SOUTHEAST:
            x = 1
            y = 1
        elif self._shadow_position == _locals.POSITION_SOUTH:
            y = 1
        elif self._shadow_position == _locals.POSITION_SOUTHWEST:
            x = -1
            y = 1
        elif self._shadow_position == _locals.POSITION_WEST:
            x = -1
        self._shadow_tuple = (x * self._shadow_offset, y * self._shadow_offset)

    def set_controls(self, joystick=True, mouse=True):
        """
        Enable interfaces to control the widget.

        :param joystick: Use joystick
        :type joystick: bool
        :param mouse: Use mouse
        :type mouse: bool
        :return: None
        """
        self.joystick_enabled = joystick
        self.mouse_enabled = mouse

    def set_value(self, value):
        """
        Set the value.

        :param value: Value to be set on the widget
        :type value: Object
        :return: None
        """
        raise ValueError('{}({}) does not accept value'.format(self.__class__.__name__,
                                                               self.get_id()))

    def update(self, events):
        """
        Update internal varibale according to the given events list.

        :param events: List of pygame events
        :type events: list
        :return: True if updated
        :rtype: bool
        """
        raise NotImplementedError('Override is mandatory')


WidgetType = Widget
