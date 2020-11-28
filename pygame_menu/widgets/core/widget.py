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

import pygame
import pygame_menu.baseimage as _baseimage
import pygame_menu.font as _fonts
import pygame_menu.locals as _locals
from pygame_menu.widgets.core.selection import Selection
from pygame_menu.sound import Sound
from pygame_menu.utils import make_surface, assert_alignment, assert_color, assert_position, assert_vector2, to_string

from uuid import uuid4
import time


class Widget(object):
    """
    Widget abstract class.

    :param title: Widget title
    :type title: str
    :param widget_id: Widget identifier
    :type widget_id: str
    :param onchange: Callback when changing the selector
    :type onchange: function, None
    :param onreturn: Callback when pressing return button
    :type onreturn: callable, None
    :param args: Optional arguments for callbacks
    :type args: any
    :param kwargs: Optional keyword arguments
    :type kwargs: dict
    """

    def __init__(self,
                 title='',
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
        self._attributes = {}  # Stores widget attributes
        self._alignment = _locals.ALIGN_CENTER
        self._background_color = None
        self._background_inflate = (0, 0)
        self._events = []  # type: list
        self._id = str(widget_id)
        self._margin = (0.0, 0.0)  # type: tuple
        self._max_width = None  # type: (int,float)
        self._rect = pygame.Rect(0, 0, 0, 0)  # type: (pygame.Rect,None)
        self._selected_rect = None  # type: (pygame.rect.Rect,None)
        self._selection_time = 0  # type: float
        self._title = to_string(title)

        self._args = args or []  # type: list
        self._kwargs = kwargs or {}  # type: dict
        self._on_change = onchange  # type: callable
        self._on_return = onreturn  # type: callable

        # Surface of the widget
        self._surface = None  # type: (pygame.Surface,None)

        # Menu reference
        self._menu = None

        # If this is True then the widget forces the Menu to update because the
        # widget render has changed
        self._menu_surface_needs_update = False

        # Modified in set_font() method
        self._font = None  # type: (pygame.font.Font,None)
        self._font_antialias = True  # type: bool
        self._font_background_color = None  # type: (tuple, None)
        self._font_color = (0, 0, 0)  # type: tuple
        self._font_name = ''  # type: str
        self._font_selected_color = (255, 255, 255)  # type: tuple
        self._font_size = 0  # type: int

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

        # Stores the last render surface size, updated by _check_render_size_changed()
        self._last_render_surface_size = (0, 0)

        self._selection_effect = None  # type: Selection

        # Public attributes
        self.active = False  # Widget requests focus
        self.is_selectable = True  # Some widgets cannot be selected like labels
        self.joystick_enabled = True
        self.mouse_enabled = True
        self.selected = False
        self.selection_effect_enabled = True  # Some widgets cannot have selection effect
        self.sound = Sound()  # type: Sound
        self.touchscreen_enabled = True

    def set_attribute(self, key, value):
        """
        Set widget attribute.

        :param key: Key of the attribute
        :type key: str
        :param value: Value of the attribute
        :type value: any
        :return: None
        """
        assert isinstance(key, str)
        self._attributes[key] = value

    def get_attribute(self, key, default):
        """
        Get attribute value.

        :param key: Key of the attribute
        :type key: str
        :param default: Value if does not exists
        :type default: any
        :return: Attribute data
        :rtype: any
        """
        assert isinstance(key, str)
        if key not in self._attributes.keys():
            return default
        return self._attributes[key]

    @staticmethod
    def _hash_variables(*args):
        """
        Compute hash from a series of variables.

        :param args: Variables to compute hash
        :type args: any
        :return: Hash data
        :rtype: int
        """
        return hash(args)

    def _render_hash_changed(self, *args):
        """
        This method checks if the widget must render because the inner variables changed.
        This method should include all the variables.
        If the render changed,

        :param args: Variables to check the hash
        :type args: any
        :return: Hash data
        :rtype: int
        """
        _hash = self._hash_variables(*args)
        if _hash != self._last_render_hash:
            self._last_render_hash = _hash
            return True
        return False

    def set_title(self, title):  # lgtm [py/inheritance/incorrect-overridden-signature]
        """
        Update the widget title.

        :param title: New title
        :type title: str
        :return: None
        """
        self._title = to_string(title)
        self._apply_font()
        self._render()
        self._check_render_size_changed()

    def get_title(self):
        """
        Return the widget title.

        :return: Widget title
        :rtype: str
        """
        return self._title

    def set_background_color(self, color, inflate=(0, 0)):
        """
        Set widget background color.

        :param color: Widget background color
        :type color: tuple, list, :py:class:`pygame_menu.baseimage.BaseImage`, None
        :param inflate: Inflate background in x,y
        :type inflate: tuple, list
        :return: None
        """
        if color is not None:
            if isinstance(color, _baseimage.BaseImage):
                assert color.get_drawing_mode() == _baseimage.IMAGE_MODE_FILL, \
                    'currently widget only support IMAGE_MODE_FILL drawing mode'
            else:
                assert_color(color)
        assert_vector2(inflate)
        assert inflate[0] >= 0 and inflate[1] >= 0, \
            'widget background inflate must be equal or greater than zero in both axis'
        self._background_color = color
        self._background_inflate = inflate

    def _fill_background_color(self, surface):
        """
        Fill a surface with the widget background color.

        :param surface: Surface to fill
        :type surface: :py:class:`pygame.Surface`
        :return: None
        """
        if self._background_color is None:
            return
        if isinstance(self._background_color, _baseimage.BaseImage):
            self._background_color.draw(
                surface=surface,
                area=self._rect.inflate(*self._background_inflate),
                position=(self._rect.x - self._background_inflate[0] / 2,
                          self._rect.y - self._background_inflate[1] / 2)
            )
        else:
            surface.fill(self._background_color, self._rect.inflate(*self._background_inflate))

    def get_selection_effect(self):
        """
        Return the selection effect.

        :return: Selection effect
        :rtype: :py:class:`pygame_menu.widgets.core.Selection`
        """
        return self._selection_effect

    def set_selection_effect(self, selection):
        """
        Set the selection effect handler.

        :param selection: Selection effect class
        :type selection: :py:class:`pygame_menu.widgets.core.Selection`
        :return: None
        """
        assert isinstance(selection, Selection)
        self._selection_effect = selection

    def apply(self, *args):
        """
        Run ``on_return`` callback when return event. A callback function
        receives the following arguments:

        .. code-block:: python

            callback_func( value, *args, *widget._args, **widget._kwargs )

        with:
            - ``value`` (if something is returned by ``get_value()``)
            - ``args`` given to this method
            - ``args`` of the widget
            - ``kwargs`` of the widget

        :param args: Extra arguments passed to the callback
        :param args: any
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

        .. code-block:: python

            callback_func( value, *args, *widget._args, **widget._kwargs )

        with:
            - ``value`` (if something is returned by ``get_value()``)
            - ``args`` given to this method
            - ``args`` of the widget
            - ``kwargs`` of the widget

        :param args: Extra arguments passed to the callback
        :param args: any
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
        :type surface: :py:class:`pygame.Surface`
        :return: None
        """
        raise NotImplementedError('override is mandatory')

    def draw_selection(self, surface):
        """
        Draw selection effect on widget.

        :param surface: Surface to draw
        :type surface: :py:class:`pygame.Surface`
        :return: None
        """
        if not self.is_selectable or self._selection_effect is None or not self.selection_effect_enabled:
            return
        self._selection_effect.draw(surface, self)

    def set_max_width(self, width):
        """
        Set widget max width (column support) if force_fit_text is enabled.

        :param width: Width in px, None if max width is disabled
        :type width: int, float, None
        :return: None
        """
        if width is not None:
            assert isinstance(width, (int, float))
        self._max_width = width

    def get_margin(self):
        """
        Return the widget margin.

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
        Return the Rect object, this forces the widget rendering.

        :return: Widget rect
        :rtype: :py:class:`pygame.Rect`
        """
        self._render()
        return self._rect.copy()

    def get_value(self):
        """
        Return the value. If exception ``ValueError`` is raised,
        no value will be passed to the callbacks.

        :return: Widget data value
        :rtype: Object
        """
        raise ValueError('{}({}) does not accept value'.format(self.__class__.__name__,
                                                               self.get_id()))

    def get_id(self):
        """
        Return the widget ID.

        :return: Widget ID
        :rtype: str
        """
        return self._id

    def _render(self):
        """
        Render the widget surface.

        This method shall update the attribute ``_surface`` with a pygame.Surface
        representing the outer borders of the widget.

        :return: None
        """
        raise NotImplementedError('override is mandatory')

    def _font_render_string(self, text, color=(0, 0, 0), use_background_color=True):
        """
        Render text.

        :param text: Text to render
        :type text: str
        :param color: Text color
        :type color: tuple
        :param use_background_color: Use default background color
        :type use_background_color: bool
        :return: Text surface
        :rtype: :py:class:`pygame.Surface`
        """
        # assert isinstance(text, str)
        assert isinstance(color, tuple)
        assert isinstance(use_background_color, bool)
        bgcolor = self._font_background_color

        # Background color must be opaque, otherwise the results are quite bad
        if isinstance(bgcolor, (tuple, list)) and len(bgcolor) == 4 and bgcolor[3] != 255:
            bgcolor = None

        # Disable
        if not use_background_color:
            bgcolor = None

        return self._font.render(text, self._font_antialias, color, bgcolor)

    def _check_render_size_changed(self):
        """
        Check the size changed after rendering.
        This method should be used only on widgets that can change in size, or if the size
        is changed during execution time (like set_title).
        The update status (needs update if render size changed) is returned by
        Widget.surface_needs_update() method.

        :return: Boolean, if True the size changed
        :rtype: bool
        """
        if self._rect.size != self._last_render_surface_size:
            self._last_render_surface_size = self._rect.size
            self._menu_surface_needs_update = True
            return True
        return False

    def _render_string(self, string, color):
        """
        Render text and turn it into a surface.

        :param string: Text to render
        :type string: str
        :param color: Text color
        :type color: tuple
        :return: Text surface
        :rtype: :py:class:`pygame.Surface`
        """
        text = self._font_render_string(string, color)

        # Create surface
        surface = make_surface(width=text.get_width(),
                               height=text.get_height(),
                               alpha=True)

        # Draw shadow first
        if self._shadow:
            text_bg = self._font_render_string(string, self._shadow_color)
            surface.blit(text_bg, self._shadow_tuple)

        surface.blit(text, (0, 0))
        new_width = surface.get_size()[0]
        new_height = surface.get_size()[1]

        if self._max_width is not None and new_width > self._max_width:
            surface = pygame.transform.smoothscale(surface, (self._max_width, new_height))

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

    def set_font(self, font, font_size, color, selected_color, background_color, antialias=True):
        """
        Set the text font.

        :param font: Name or list of names for font (see pygame.font.match_font for precise format)
        :type font: str, list
        :param font_size: Size of font in pixels
        :type font_size: int
        :param color: Text color
        :type color: tuple
        :param selected_color: Text color when widget is selected
        :type selected_color: tuple
        :param background_color: Font background color
        :type background_color: tuple
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :type antialias: bool
        :return: None
        """
        assert isinstance(font, str)
        assert isinstance(font_size, int)
        assert isinstance(color, tuple)
        assert isinstance(selected_color, tuple)
        assert isinstance(background_color, (tuple, type(None)))
        assert isinstance(antialias, bool)

        self._font = _fonts.get_font(font, font_size)
        self._font_antialias = antialias
        self._font_background_color = background_color
        self._font_color = color
        self._font_name = font
        self._font_selected_color = selected_color
        self._font_size = font_size

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
        Set the menu reference.

        :param menu: Menu object
        :type menu: :py:class:`pygame_menu.Menu`
        :return: None
        """
        self._menu = menu

    def get_menu(self):
        """
        Return the menu reference (if exists).

        :return: Menu reference
        :rtype: :py:class:`pygame_menu.Menu`, None
        """
        return self._menu

    def _apply_font(self):
        """
        Function triggered after a font is applied to the widget.

        :return: None
        """
        raise NotImplementedError('override is mandatory')

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

        :param align: Widget align, see locals
        :type align: str
        :return: None
        """
        assert_alignment(align)
        self._alignment = align

    def get_alignment(self):
        """
        Return the widget alignment.

        :return: Widget align, see locals
        :rtype: str
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
        self.active = False
        if selected:
            self._focus()
            self._selection_time = time.time()
        else:
            self._blur()
            self._events = []  # Remove events
        self._render()

    def get_selected_time(self):
        """
        Return time the widget has been selected in miliseconds.
        If the widget is not currently selected, return 0.

        :return: Time in ms
        :rtype: float
        """
        if not self.selected:
            return 0
        return (time.time() - self._selection_time) * 1000

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
        :type color: list, None
        :param position: Shadow position
        :type position: str, None
        :param offset: Shadow offset
        :type offset: int, float, None
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
        :type sound: :py:class:`pygame_menu.sound.Sound`
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

    def set_controls(self, joystick=True, mouse=True, touchscreen=True):
        """
        Enable interfaces to control the widget.

        :param joystick: Use joystick
        :type joystick: bool
        :param mouse: Use mouse
        :type mouse: bool
        :param touchscreen: Use touchscreen
        :type touchscreen: bool
        :return: None
        """
        self.joystick_enabled = joystick
        self.mouse_enabled = mouse
        self.touchscreen_enabled = touchscreen

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
        :type events: list[:py:class:`pygame.event.Event`]
        :return: True if updated
        :rtype: bool
        """
        raise NotImplementedError('override is mandatory')

    def _add_event(self, event):
        """
        Add a custom event to the widget for the next update().

        :param event: Custom event
        :type event: :py:class:`pygame.event.Event`
        :return: None
        """
        self._events.append(event)

    def _merge_events(self, events):
        """
        Append widget events to events list.

        :param events: Event list
        :type events: list[:py:class:`pygame.event.Event`]
        :return: Augmented event list
        :rtype: list[:py:class:`pygame.event.Event`]
        """
        if len(self._events) == 0:
            return events
        copy_events = []
        for e in events:
            copy_events.append(e)
        for e in self._events:
            copy_events.append(e)
        self._events = []
        return copy_events
