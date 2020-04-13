# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

WIDGET
Base class for widgets.

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

import pygame as _pygame
import pygameMenu.font as _fonts
import pygameMenu.locals as _locals

from pygameMenu.sound import Sound as _Sound
from pygameMenu.utils import make_surface, assert_alignment, assert_color, assert_position
from uuid import uuid4


class Widget(object):
    """
    Widget abstract class.

    :param widget_id: Widget identifier
    :type widget_id: basestring
    :param onchange: Callback when changing the selector
    :type onchange: callable, NoneType
    :param onreturn: Callback when pressing return button
    :type onreturn: callable, NoneType
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword-arguments for callbacks
    """

    def __init__(self,
                 widget_id='',
                 onchange=None,
                 onreturn=None,
                 args=None,
                 kwargs=None
                 ):
        assert isinstance(widget_id, str)
        if onchange:
            assert callable(onchange), 'onchange must be callable or None'
        if onreturn:
            assert callable(onreturn), 'onreturn must be callable or None'

        # Store id, if None or empty create new ID based on UUID
        if widget_id is None or len(widget_id) == 0:
            widget_id = uuid4()
        self._alignment = _locals.ALIGN_CENTER
        self._id = str(widget_id)
        self._last_selected_surface = None  # type: (_pygame.Surface,None)
        self._selected_rect = None  # type: (_pygame.rect.Rect,None)
        self._rect = _pygame.Rect(0.0, 0.0, 0.0, 0.0)  # type: (_pygame.Rect,None)
        self._margin = (0.0, 0.0)  # type: tuple
        self._max_width = None  # type: (int,float)

        self._args = args or []  # type: list
        self._kwargs = kwargs or {}  # type: dict
        self._on_change = onchange  # type: callable
        self._on_return = onreturn  # type: callable

        # Surface of the widget
        self._surface = None  # type: (_pygame.Surface,None)

        # Menu reference
        self._menu = None

        # If this is True then the widget forces the Menu to update because the
        # widget render has changed
        self._menu_surface_needs_update = False

        # Modified in set_font() method
        self._font = None  # type: (_pygame.font.Font,None)
        self._font_name = ''  # type: str
        self._font_size = 0  # type: int
        self._font_color = (0, 0, 0)  # type: tuple
        self._font_selected_color = (0, 0, 0)  # type: tuple
        self._font_antialias = True  # type: bool

        # Text shadow
        self._shadow = False  # type: bool
        self._shadow_color = (0, 0, 0)  # type: tuple
        self._shadow_offset = 2.0  # type: float
        self._shadow_position = _locals.POSITION_NORTHWEST
        self._shadow_tuple = None  # (x px offset, y px offset)
        self._create_shadow_tuple()

        # Rendering, this variable may be used by render() method
        # If the hash of the variables change respect to the last render hash
        # (hash computed using self._hash_variables() method)
        # then the widget should render and update the hash
        self._last_render_hash = 0  # type: int

        # Stores the last render surface size, updated by
        # self._check_render_size_changed()
        self._last_render_surface_size = (0.0, 0.0)

        # Public attributes
        self.is_selectable = True  # Some widgets cannot be selected like labels
        self.joystick_enabled = True  # type: bool
        self.mouse_enabled = True  # type: bool
        self.selected = False  # type: bool
        self.sound = _Sound()  # type: _Sound

    @staticmethod
    def _hash_variables(*args):
        """
        Compute hash from a series of variables.

        :param args: Variables to compute hash
        :type args: Object
        :return: Hash data
        :rtype: int
        """
        return hash(args)

    def _render_hash_changed(self, *args):
        """
        This method checks if the widget must render because the inner variables changed.
        This method should include all the variables.
        If the render changed,

        :param args: Variables to checkl the hash
        :type args: Object
        :return: Hash data
        :rtype: int
        """
        _hash = self._hash_variables(*args)
        if _hash != self._last_render_hash:
            self._last_render_hash = _hash
            return True
        return False

    def apply(self, *args):
        """
        Run ``on_return`` callback when return event. A callback function
        receives the following arguments:

            callback_func( value, \*args, \*widget._args, \*\*widget._kwargs )

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
        Run ``on_change`` callback after change event is triggered. A callback function
        receives the following arguments:

            callback_func( value, \*args, \*widget._args, \*\*widget._kwargs )

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
        :param inflatex: Pixels to inflate the rect (x axis), used by highlight
        :type inflatex: int, float
        :param inflatey: Pixels to inflate the rect (y axis), used by highlight
        :type inflatey: int, float
        :param border_width: Border rect width
        :type border_width: int, float
        :return: None
        """
        if not self.is_selectable:
            return

        # Generate new rect if it's different
        rect = self._selected_rect

        if self._last_selected_surface != self._surface:  # If surface changed
            self._selected_rect = self._rect.copy()

            # Inflate rect
            self._selected_rect = self._selected_rect.inflate(inflatex, inflatey)

            # Translate rect
            self._selected_rect = self._selected_rect.move(0, -1)

            # Update rect
            rect = self._selected_rect
            self._last_selected_surface = self._surface

        # Draw rect
        _pygame.draw.rect(surface,
                          selected_color,
                          rect,
                          int(border_width))

    def set_max_width(self, width):
        """
        Set widget max width (column support) if force_fit_text is enabled.

        :param width: Width in px, None if max width is disabled
        :type width: int, float, NoneType
        :return: None
        """
        if width is not None:
            assert isinstance(width, (int, float))
        self._max_width = width

    def get_margin(self):
        """
        :return: Widget margin
        :rtype: tuple
        """
        return self._margin

    def set_margin(self, x, y):
        """
        Set Widget margin.

        :param x: Margin on x axis
        :type x: int, float
        :param y: Margin on y axis
        :type y: int, float
        :return: None
        """
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        self._margin = (x, y)

    def get_rect(self):
        """
        :return: Return the Rect object, this forces the widget rendering
        :rtype: pygame.rect.RectType
        """
        self._render()
        return self._rect

    def get_value(self):
        """
        Return the value. If exception ``ValueError`` is raised,
        no value will be passed to the callbacks.

        :return: Value
        :rtype: Object
        """
        raise ValueError('{}({}) does not accept value'.format(self.__class__.__name__,
                                                               self.get_id()))

    def get_id(self):
        """
        :return: Returns widget ID.
        :rtype: basestring
        """
        return self._id

    def _render(self):
        """
        Render the widget surface.

        This method shall update the attribute ``_surface`` with a pygame.Surface
        representing the outer borders of the widget.

        :return: None
        """
        raise NotImplementedError('Override is mandatory')

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

    def _check_render_size_changed(self):
        """
        Check the size changed after rendering, if so, set
        self._menu_surface_needs_update as True. This method should be used only on
        widgets that can change in size.

        :return: Boolean, if True the size changed
        :rtype: bool
        """
        sz = self._surface.get_size()
        if sz[0] != self._last_render_surface_size[0] or sz[1] != self._last_render_surface_size[1]:
            self._last_render_surface_size = sz
            self._menu_surface_needs_update = True
            return True
        return False

    def _render_string(self, string, color):
        """
        Render text and turn it into a surface.

        :param string: Text to render
        :type string: basestring
        :param color: Text color
        :type color: tuple
        :return: Text surface
        :rtype: pygame.surface.SurfaceType
        """
        text = self.font_render_string(string, color)

        # Create surface
        surface = make_surface(text.get_width(), text.get_height(), alpha=True)

        # Draw shadow first
        if self._shadow:
            text_bg = self._font.render(string, self._font_antialias, self._shadow_color)
            surface.blit(text_bg, self._shadow_tuple)

        surface.blit(text, (0, 0))
        new_width = surface.get_size()[0]
        new_height = surface.get_size()[1]

        if self._max_width is not None and new_width > self._max_width:
            surface = _pygame.transform.smoothscale(surface, (self._max_width, new_height))

        return surface

    def surface_needs_update(self):
        """
        Checks if the widget width/height has changed because events. If so, return true and
        set the status of the widget (menu widget position needs update) as false. This method
        is used by .update() from Menu class.

        :return: True if the widget position has changed by events after the rendering.
        :rtype: bool
        """
        if self._menu_surface_needs_update:
            self._menu_surface_needs_update = False
            return True
        return False

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
        self._font_name = font
        self._font = _fonts.get_font(font, font_size)
        self._font_size = font_size
        self._font_color = color
        self._font_selected_color = selected_color
        self._font_antialias = antialias
        self._apply_font()

    def get_font_info(self):
        """
        Return a dict with the information of the widget font.

        :return: Dict, keys: size (int), name (str), color (tuple), selected_color (tuple), antialias (bool)
        :rtype: dict
        """
        return {
            'size': self._font_size,
            'name': self._font_name,
            'color': self._font_color,
            'selected_color': self._font_selected_color,
            'antialias': self._font_antialias,
        }

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
        self._last_selected_surface = None

    def get_position(self):
        """
        Return a tuple containing the top left and bottom right positions in
        the format of (x leftmost, y uppermost, x rightmost, y lowermost).

        :return: Tuple of 4 elements
        :rtype: tuple
        """
        return self._rect.x, self._rect.y, self._rect.x + self._rect.width, self._rect.y + self._rect.height

    def set_alignment(self, align):
        """
        Set the alignment of the widget.

        :param align: Widget align, see locals
        :type align: basestring
        :return: None
        """
        assert_alignment(align)
        self._alignment = align

    def get_alignment(self):
        """
        Returns widget alignment.

        :return: Widget align, see locals
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
        self._render()

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
        :type offset: int, float, NoneType
        :return: None
        """
        self._shadow = enabled
        if color is not None:
            assert_color(color)
            self._shadow_color = color
        if position is not None:
            assert_position(position)
            self._shadow_position = position
        if offset is not None:
            assert isinstance(offset, (int, float))
            if offset <= 0:
                raise ValueError('shadow offset must be greater than zero')
            self._shadow_offset = offset

        # Create shadow tuple position
        self._create_shadow_tuple()

    def set_sound(self, sound):
        """
        Set sound engine to the widget.

        :param sound: Sound object
        :type sound: pygameMenu.sound.SoundType
        :return: None
        """
        self.sound = sound

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

        .. warning:: This method does not fire the callbacks as it is
                     called programmatically. This behavior is deliberately
                     chosen to avoid infinite loops.

        :param value: Value to be set on the widget
        :type value: Object
        :return: None
        """
        raise ValueError('{}({}) does not accept value'.format(self.__class__.__name__,
                                                               self.get_id()))

    def update(self, events):
        """
        Update internal variable according to the given events list
        and fire the callbacks.

        :param events: List of pygame events
        :type events: list
        :return: True if updated
        :rtype: bool
        """
        raise NotImplementedError('Override is mandatory')
