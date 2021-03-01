# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

WIDGET
Base class for widgets.

NOTE: pygame-menu v3 will not provide new widgets or functionalities, consider
upgrading to the latest version.

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

import pygame
import pygame_menu.baseimage as _baseimage
import pygame_menu.font as _fonts
import pygame_menu.locals as _locals
from pygame_menu.widgets.core.selection import Selection
from pygame_menu.sound import Sound
from pygame_menu.utils import make_surface, assert_alignment, assert_color, assert_position, assert_vector2, \
    to_string, is_callable, isinstance_str

from uuid import uuid4
import time
import warnings


class Widget(object):
    """
    Widget abstract class.

    :param title: Widget title
    :type title: str
    :param widget_id: Widget identifier
    :type widget_id: str
    :param onchange: Callback when updating the status of the widget, executed in ``widget.change()``
    :type onchange: callable, None
    :param onreturn: Callback when applying on the widget (return), executed in ``widget.apply()``
    :type onreturn: callable, None
    :param args: Optional arguments for callbacks
    :type args: any
    :param kwargs: Optional keyword arguments
    :type kwargs: dict, any
    """

    def __init__(self,
                 title='',
                 widget_id='',
                 onchange=None,
                 onreturn=None,
                 args=None,
                 kwargs=None
                 ):
        if onchange:
            assert is_callable(onchange), 'onchange must be callable or None'
        if onreturn:
            assert is_callable(onreturn), 'onreturn must be callable or None'

        # Store id, if None or empty create new ID based on UUID
        if widget_id is None or len(widget_id) == 0:
            widget_id = str(uuid4())
        assert isinstance_str(widget_id), \
            'widget id must be a string, but received {0}'.format(widget_id)

        self._alignment = _locals.ALIGN_CENTER
        self._attributes = {}  # Stores widget attributes
        self._background_color = None
        self._background_inflate = (0, 0)
        self._events = []  # type: list
        self._id = widget_id
        self._margin = (0.0, 0.0)  # type: tuple
        self._max_width = None  # type: (int,float)
        self._padding = (0, 0, 0, 0)  # top, right, bottom, left
        self._selection_time = 0  # type: float
        self._title = to_string(title)

        # Widget transforms
        self._angle = 0  # Rotation angle (degrees)
        self._flip = (False, False)  # x, y
        self._scale = [False, 1, 1, False, False]  # do_scale, x, y, smooth, use_same_xy
        self._translate = (0.0, 0.0)  # type: tuple

        # Widget rect. This object does not contain padding. For getting the widget+padding
        # use .get_rect() Widget method instead
        self._rect = pygame.Rect(0, 0, 0, 0)  # type: pygame.Rect

        # Callbacks
        self._draw_callbacks = {}  # type: dict
        self._update_callbacks = {}  # type: dict

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

        # Selection effect, for avoiding exception while getting object rect, NullSelection
        # was created. Initially it was None
        self._selection_effect = _NullSelection()  # type: Selection

        # Public attributes
        self.active = False  # Widget requests focus
        self.is_selectable = True  # Some widgets cannot be selected like labels
        self.joystick_enabled = True
        self.lock_position = False  # If True, locks position after first call to .set_position(x,y) method
        self.mouse_enabled = True
        self.selected = False
        self.selection_effect_enabled = True  # Some widgets cannot have selection effect
        self.selection_expand_background = False  # If True, the widget background will inflate to match selection margin if selected
        self.sound = Sound()  # type: Sound
        self.touchscreen_enabled = True
        self.visible = True  # Use .show() or .hide() to modify this status

    def set_attribute(self, key, value):
        """
        Set widget attribute.

        :param key: Key of the attribute
        :type key: str
        :param value: Value of the attribute
        :type value: any
        :return: None
        """
        assert isinstance_str(key)
        self._attributes[key] = value

    def get_attribute(self, key, default=None):
        """
        Get attribute value.

        :param key: Key of the attribute
        :type key: str
        :param default: Value if does not exists
        :type default: any
        :return: Attribute data
        :rtype: any
        """
        assert isinstance_str(key)
        if not self.has_attribute(key):
            return default
        return self._attributes[key]

    def has_attribute(self, key):
        """
        Returns true if widget has the given attribute.

        :param key: Key of the attribute
        :type key: str
        :return: True if exists
        :rtype: bool
        """
        assert isinstance_str(key)
        return key in self._attributes.keys()

    def remove_attribute(self, key):
        """
        Removes the given attribute from the widget. Throws ``IndexError`` if given key does not exist.

        :param key: Key of the attribute
        :type key: str
        :return: None
        """
        if not self.has_attribute(key):
            raise IndexError('attribute "{0}" does not exists on widget'.format(key))
        del self._attributes[key]

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
        This method should include all the variables used by the render method, for example,
        visibility, selected, etc.

        :param args: Variables to check the hash
        :type args: any
        :return: ``True`` if render has changed the widget
        :rtype: bool
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
        self._last_render_hash = 0  # Force widget render
        self._render()

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
        :param inflate: Inflate background in *(x,y)*. If ``None``, the widget value is not updated
        :type inflate: tuple, list, None
        :return: None
        """
        if color is not None:
            if isinstance(color, _baseimage.BaseImage):
                assert color.get_drawing_mode() == _baseimage.IMAGE_MODE_FILL, \
                    'currently widget only supports IMAGE_MODE_FILL drawing mode'
            else:
                assert_color(color)
        if inflate is None:
            inflate = self._background_inflate
        assert_vector2(inflate)
        assert inflate[0] >= 0 and inflate[1] >= 0, \
            'widget background inflate must be equal or greater than zero in both axis'
        self._background_color = color
        self._background_inflate = tuple(inflate)
        self._last_render_hash = 0  # Force widget render

    def expand_background_inflate_to_selection_effect(self):
        """
        Expand background inflate to match the selection effect
        (the widget don't require to be selected).

        This is a permanent change; for dynamic purposes, depending if the widget
        is selected or not, setting ``widget.selection_expand_background`` to ``True`` may help.

        .. note::

            This method may have unexpected results with certain selection effects.

        :return: None
        """
        self._background_inflate = self._selection_effect.get_xy_margin()

    def _fill_background_color(self, surface):
        """
        Fill a surface with the widget background color.

        :param surface: Surface to fill
        :type surface: :py:class:`pygame.Surface`
        :return: None
        """
        if self._background_color is None:
            return
        if not (self.selection_expand_background and self.selected):
            inflate = self._background_inflate
        else:
            inflate = self._selection_effect.get_xy_margin()
        rect = self.get_rect(inflate=inflate)
        if isinstance(self._background_color, _baseimage.BaseImage):
            self._background_color.draw(
                surface=surface,
                area=rect,
                position=(rect.x, rect.y)
            )
        else:
            surface.fill(self._background_color, rect)

    def get_selection_effect(self):
        """
        Return the selection effect.

        .. warning::

            Use with caution.

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
        self._last_render_hash = 0  # Force widget render

    def apply(self, *args):
        """
        Run ``on_return`` callback when return event. A callback function
        receives the following arguments:

        .. code-block:: python

            callback_func(value, *args, *widget._args, **widget._kwargs)

        with:
            - ``value`` (if something is returned by ``get_value()``)
            - ``args`` given to this method
            - ``args`` of the widget
            - ``kwargs`` of the widget

        :param args: Extra arguments passed to the callback
        :param args: any
        :return: Callback return value
        :rtype: any
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

            callback_func(value, *args, *widget._args, **widget._kwargs)

        with:
            - ``value`` (if something is returned by ``get_value()``)
            - ``args`` given to this method
            - ``args`` of the widget
            - ``kwargs`` of the widget

        :param args: Extra arguments passed to the callback
        :param args: any
        :return: Callback return value
        :rtype: any
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
        Set widget max width (column support) if ``force_fit_text`` is enabled.

        :param width: Width in px, None if max width is disabled
        :type width: int, float, None
        :return: None
        """
        if width is not None:
            assert isinstance(width, (int, float)), 'width must be numeric'
        self._max_width = width

    def get_margin(self):
        """
        Return the widget margin.

        :return: Widget margin *(left,bottom)*
        :rtype: tuple
        """
        return self._margin

    def set_margin(self, x, y):
        """
        Set Widget margin (left, bottom).

        :param x: Margin on x axis (left)
        :type x: int, float
        :param y: Margin on y axis (bottom)
        :type y: int, float
        :return: None
        """
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        self._margin = (x, y)
        self._last_render_hash = 0  # Force widget render

    def get_padding(self):
        """
        Return the widget padding.

        :return: Widget padding *(top,right,bottom,left)*
        :rtype: tuple
        """
        return self._padding

    def set_padding(self, padding):
        """
        Set the Widget padding according to CSS rules.

        - If an integer or float is provided: top, right, bottom and left values will be the same
        - If 2-item tuple is provided: top and bottom takes the first value, left and right the second
        - If 3-item tuple is provided: top will take the first value, left and right the second, and bottom the third
        - If 4-item tuple is provided: padding will be (top, right, bottom, left)

        .. note::

            See `CSS W3Schools <https://www.w3schools.com/css/css_padding.asp>`_ for more info about padding.

        :param padding: Can be a single number, or a tuple of 2, 3 or 4 elements following CSS style
        :type padding: int, float, tuple, list
        :return: None
        """
        assert isinstance(padding, (int, float, tuple, list))
        if isinstance(padding, (int, float)):
            assert padding >= 0, 'padding cant be a negative number'
            self._padding = (padding, padding, padding, padding)
        else:
            assert 1 <= len(padding) <= 4, 'padding must be a tuple of 2, 3 or 4 elements'
            for i in range(len(padding)):
                assert isinstance(padding[i], (int, float)), 'all padding elements must be integers or floats'
                assert padding[i] >= 0, 'all padding elements must be equal or greater than zero'
            if len(padding) == 1:
                self._padding = (padding[0], padding[0], padding[0], padding[0])
            elif len(padding) == 2:
                self._padding = (padding[0], padding[1], padding[0], padding[1])
            elif len(padding) == 3:
                self._padding = (padding[0], padding[1], padding[2], padding[1])
            else:
                self._padding = (padding[0], padding[1], padding[2], padding[3])
        self._last_render_hash = 0  # Force widget render

    def get_rect(self, apply_padding=True, inflate=None):
        """
        Return the Rect object, this forces the widget rendering.

        .. note::

            This is the only method that returns the rect with the padding applied.
            If widget._rect is used, the padding has not been applied.

        :param apply_padding: Apply widget padding
        :type apply_padding: bool
        :param inflate: Inflate rect *(x,y)* in px
        :type inflate: None, tuple, list
        :return: Widget rect
        :rtype: :py:class:`pygame.Rect`
        """
        self._render()

        # Padding + inflate
        if inflate is None:
            inflate = (0, 0)

        pad_top = self._padding[0] * apply_padding + inflate[1] / 2
        pad_right = self._padding[1] * apply_padding + inflate[0] / 2
        pad_bottom = self._padding[2] * apply_padding + inflate[1] / 2
        pad_left = self._padding[3] * apply_padding + inflate[0] / 2

        return pygame.Rect(int(self._rect.x - pad_left),
                           int(self._rect.y - pad_top),
                           int(self._rect.width + pad_left + pad_right),
                           int(self._rect.height + pad_bottom + pad_top))

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

    def change_id(self, widget_id):
        """
        Change widget id.

        :param widget_id: Widget ID
        :type widget_id: str
        :return: None
        """
        assert isinstance_str(widget_id)
        if self._menu is not None:
            # noinspection PyProtectedMember
            self._menu._check_id_duplicated(widget_id)
        self._id = widget_id

    def _render(self):
        """
        Render the widget surface.

        This method shall update the attribute ``_surface`` with a :py:class:`pygame.Surface`
        representing the outer borders of the widget.

        :return: True if widget has rendered a new state, None if the widget has not changed, so render used a cache
        :rtype: bool, None
        """
        raise NotImplementedError('override is mandatory')

    def _font_render_string(self, text, color=(0, 0, 0), use_background_color=True):
        """
        Render text. If the font is not defined returns a zero-width surface.

        :param text: Text to render
        :type text: str, None
        :param color: Text color
        :type color: tuple
        :param use_background_color: Use default background color
        :type use_background_color: bool
        :return: Text surface
        :rtype: :py:class:`pygame.Surface`
        """
        if text is not None:
            assert isinstance_str(text)
        assert isinstance(color, tuple), 'invalid color'
        assert isinstance(use_background_color, bool), 'use_background_color must be boolean'
        bgcolor = self._font_background_color

        # Disable
        if not use_background_color:
            bgcolor = None

        if self._font is None:
            return make_surface(0, 0)

        surface = self._font.render(text, self._font_antialias, color, bgcolor)
        return surface

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
        surface = make_surface(
            width=text.get_width(),
            height=text.get_height(),
            alpha=True
        )

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

    def _apply_surface_transforms(self):
        """
        Apply surface transforms.

        :return: None
        """
        if self._angle != 0:
            self._surface = pygame.transform.rotate(self._surface, self._angle)

        if self._flip[0] or self._flip[1]:
            self._surface = pygame.transform.flip(self._surface, self._flip[0], self._flip[1])

        if self._scale[0] and (self._scale[1] != 1 or self._scale[2] != 1):
            w = self._scale[1]
            if w != 1:
                warnings.warn('widget _max_width is not None, scaling factor in x-axes should be equal to 1')
            h = self._scale[2]
            width = self._surface.get_width()
            height = self._surface.get_height()
            use_same_xy = self._scale[4]
            if not use_same_xy:
                w = int(w * width)
                h = int(h * height)
            if not self._scale[3]:  # smooth
                self._surface = pygame.transform.scale(self._surface, (w, h))
            else:
                self._surface = pygame.transform.smoothscale(self._surface, (w, h))

    def surface_needs_update(self):
        """
        Checks if the widget width/height has changed because events. If so, return true and
        set the status of the widget (menu widget position needs update) as false. This method
        is used by ``Menu.update()``.

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

        :param font: Font name (see :py:class:`pygame.font.match_font` for precise format)
        :type font: str
        :param font_size: Size of font in pixels
        :type font_size: int
        :param color: Text color
        :type color: tuple
        :param selected_color: Text color when widget is selected
        :type selected_color: tuple
        :param background_color: Font background color
        :type background_color: tuple, None
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :type antialias: bool
        :return: None
        """
        assert isinstance_str(font)
        assert isinstance(font_size, (int, float))
        assert isinstance(antialias, bool)
        assert_color(color)
        assert_color(selected_color)

        if background_color is not None:
            assert_color(background_color)

            # If background is a color and it's transparent raise a warning
            # Font background color must be opaque, otherwise the results are quite bad
            if len(background_color) == 4 and background_color[3] != 255:
                background_color = None
                msg = 'font background color must be opaque, alpha channel must be 255'
                warnings.warn(msg)

        font_size = int(font_size)

        self._font = _fonts.get_font(font, font_size)
        self._font_antialias = antialias
        self._font_background_color = background_color
        self._font_color = color
        self._font_name = font
        self._font_selected_color = selected_color
        self._font_size = font_size

        self._last_render_hash = 0  # Force widget render
        self._apply_font()

    def update_font(self, style):
        """
        Updates font. This method receives a style dict (non empty) containing the following keys:

        - ``antialias``             Font antialias (bool)
        - ``background_color``      Background color (tuple)
        - ``color``                 Font color (tuple)
        - ``name``                  Name of the font (str)
        - ``selected_color``        Selected color (tuple)
        - ``size``                  Size of the font (int)

        .. note::

            If a key is not defined it will be rewritten using current font style from ``Widget.get_font_info()`` method.

        :param style: Font style dict
        :type style: dict
        :return: None
        """
        assert isinstance(style, dict)
        assert 1 <= len(style.keys()) <= 6
        current_font = self.get_font_info()
        for k in current_font.keys():
            if k not in style.keys():
                style[k] = current_font[k]
        self.set_font(
            font=style['name'],
            font_size=style['size'],
            color=style['color'],
            selected_color=style['selected_color'],
            background_color=style['background_color'],
            antialias=style['antialias']
        )

    def get_font_info(self):
        """
        Return a dict with the information of the widget font.

        Dict values:

        - ``antialias``             Font antialias (bool)
        - ``background_color``      Background color (tuple)
        - ``color``                 Font color (tuple)
        - ``name``                  Name of the font (str)
        - ``selected_color``        Selected color (tuple)
        - ``size``                  Size of the font (int)

        :return: Dict
        :rtype: dict
        """
        return {
            'antialias': self._font_antialias,
            'background_color': self._font_background_color,
            'color': self._font_color,
            'name': self._font_name,
            'selected_color': self._font_selected_color,
            'size': self._font_size
        }

    def set_menu(self, menu):
        """
        Set the menu reference.

        :param menu: Menu object
        :type menu: :py:class:`pygame_menu.Menu`, None
        :return: None
        """
        self._menu = menu

    def get_menu(self):
        """
        Return the menu reference (if exists).

        .. warning::

            Use with caution.

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
        Set the widget position.

        :param posx: X position
        :type posx: int, float
        :param posy: Y position
        :type posy: int, float
        :return: None
        """
        assert isinstance(posx, (int, float))
        assert isinstance(posy, (int, float))
        if self.lock_position:
            return
        self._rect.x = int(posx) + self._translate[0]
        self._rect.y = int(posy) + self._translate[1]

    def get_position(self):
        """
        Return the widget position tuple *(x, y)*.

        :return: Widget position
        :rtype: tuple
        """
        return self._rect.x, self._rect.y

    def get_width(self, apply_padding=True, apply_selection=False):
        """
        Return the widget width.

        .. warning::

            If the widget is not rendered, this method will return ``0``.

        :param apply_padding: Apply padding
        :type apply_selection: bool
        :param apply_selection: Apply selection
        :type apply_padding: bool
        :return: Widget width (px)
        :rtype: float
        """
        assert isinstance(apply_padding, bool)
        assert isinstance(apply_selection, bool)
        rect = self.get_rect(apply_padding=apply_padding)
        width = rect.width
        if apply_selection:
            width += self._selection_effect.get_width()
        return float(width)

    def get_height(self, apply_padding=True, apply_selection=False):
        """
        Return the widget height.

        .. warning::

            If the widget is not rendered, this method will return ``0``.

        :param apply_padding: Apply padding
        :type apply_selection: bool
        :param apply_selection: Apply selection
        :type apply_padding: bool
        :return: Widget height (px)
        :rtype: float
        """
        assert isinstance(apply_padding, bool)
        assert isinstance(apply_selection, bool)
        rect = self.get_rect(apply_padding=apply_padding)
        height = rect.height
        if apply_selection:
            height += self._selection_effect.get_height()
        return float(height)

    def get_size(self, apply_padding=True, apply_selection=False):
        """
        Return the widget size.

        .. warning::

            If the widget is not rendered this method might return ``(0,0)``.

        :param apply_padding: Apply padding
        :type apply_selection: bool
        :param apply_selection: Apply selection
        :type apply_padding: bool
        :return: Widget *(width, height)*
        :rtype: tuple
        """
        return self.get_width(apply_padding=apply_padding, apply_selection=apply_selection), \
               self.get_height(apply_padding=apply_padding, apply_selection=apply_selection)

    def flip(self, x, y):
        """
        This method can flip the widget either vertically, horizontally, or both.
        Flipping a widget is non-destructive and does not change the dimensions.

        .. note::

            Flip is only applied after widget rendering. Thus, the changes are
            not immediate.

        :param x: Flip in x axis
        :type x: bool
        :param y: Flip on y axis
        :type y: bool
        :return: None
        """
        assert isinstance(x, bool)
        assert isinstance(y, bool)
        self._flip = (x, y)
        self._last_render_hash = 0  # Force widget render

    def scale(self, width, height, smooth=True):
        """
        Scale the widget to a desired width and height factor.

        .. note::

            Not all widgets are affected by scale.

        .. note::

            Scale is only applied after widget rendering. Thus, the changes are
            not immediate.

        :param width: Scale factor of the width
        :type width: int, float
        :param height: Scale factor of the height
        :type height: int, float
        :param smooth: Smooth scaling
        :type smooth: bool
        :return: None
        """
        assert isinstance(width, (int, float))
        assert isinstance(height, (int, float))
        assert isinstance(smooth, bool)
        assert width > 0 and height > 0, 'width and height must be greater than zero'
        self._scale = [True, width, height, smooth, False]
        if width == 1 and height == 1:  # Disables scaling
            self._scale[0] = False
        self._last_render_hash = 0  # Force widget render

    def resize(self, width, height, smooth=False):
        """
        Set the widget size to another size.

        .. note ::

            This method calls ``widget.scale`` method; thus, some widgets
            may not support this transformation.

        .. note::

            Resize is only applied after widget rendering. Thus, the changes are
            not immediate.

        :param width: New width of the widget in px
        :type width: int, float
        :param height: New height of the widget in px
        :type height: int, float
        :param smooth: Smooth scaling
        :type smooth: bool
        :return: None
        """
        self.scale(int(width), int(height), smooth)
        self._scale[4] = True  # enables use_same_xy

    def translate(self, x, y):
        """
        Translate to *(+x,+y)* according to default position.

        .. note::

            To revert changes, only set to *(0,0)*.

        .. note::

            Translate is only applied when updating the widget position (calling
            :py:meth:`pygame_menu.widgets.core.Widget.set_position`. This is done
            by Menu when rendering the surface. Thus, the position change is not
            immediate.

        :param x: +X in px
        :type x: int, float
        :param y: +Y in px
        :type y: int, float
        :return: None
        """
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        self._translate = (int(x), int(y))
        self._menu_surface_needs_update = True

    def rotate(self, angle):
        """
        Unfiltered counterclockwise rotation. The angle argument represents degrees
        and can be any floating point value. Negative angle amounts will rotate clockwise.

        .. note::

            Not all widgets accepts rotation. Also this rotation only affects the text or images,
            the selection or background is not rotated.

        .. note::

            Rotation is only applied after widget rendering. Thus, the changes are
            not immediate.

        :param angle: Rotation angle (degrees 0-360)
        :type angle: int, float
        :return: None
        """
        assert isinstance(angle, (int, float))
        self._angle = angle
        self._last_render_hash = 0  # Force widget render

    def set_alignment(self, align):
        """
        Set the alignment of the widget.

        .. note::

            Alignment is only applied when updating the widget position, done
            by Menu when rendering the surface. Thus, the alignment change is not
            immediate.

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
        self._last_render_hash = 0  # Force widget render
        if selected:
            self._focus()
            self._selection_time = time.time()
        else:
            self._blur()
            self._events = []  # Remove events

    def get_selected_time(self):
        """
        Return time the widget has been selected in milliseconds.
        If the widget is not currently selected, return 0.

        :return: Time in ms
        :rtype: float
        """
        if not self.selected:
            return 0
        return (time.time() - self._selection_time) * 1000

    def get_surface(self):
        """
        Return widget surface.

        .. warning::

            Use with caution.

        :return: Widget surface
        :rtype: :py:class:`pygame.Surface`
        """
        return self._surface

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

    def set_shadow(self, enabled=True, color=None, position=None, offset=2):
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
        assert isinstance(offset, (int, float))
        if offset <= 0:
            raise ValueError('shadow offset must be greater than zero')
        self._shadow_offset = offset

        self._create_shadow_tuple()  # Create shadow tuple position
        self._last_render_hash = 0  # Force widget render

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
        Set the widget value.

        .. warning::

            This method does not fire the callbacks as it is
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

        :param events: List/Tuple of pygame events
        :type events: list[:py:class:`pygame.event.Event`], tuple[:py:class:`pygame.event.Event`]
        :return: True if updated
        :rtype: bool
        """
        raise NotImplementedError('override is mandatory')

    def add_draw_callback(self, draw_callback):
        """
        Adds a function to the widget to be executed each time the widget is drawn.

        The function that this method receives receives two objects: the widget itself and
        the menu reference.

        .. code-block:: python

            import math

            def draw_update_function(widget, menu):
                t = widget.get_attribute('t', 0)
                t += menu.get_clock().get_time()
                widget.set_padding(10*(1 + math.sin(t)))) # Oscillating padding

            button = menu.add_button('This button updates its padding', None)
            button.set_draw_callback(draw_update_function)

        After creating a new callback, this functions returns the ID of the call. It can be removed
        anytime using ``widget.remove_draw_callback(id)``.

        :param draw_callback: Function
        :type draw_callback: callable
        :return: Callback ID
        :rtype: str
        """
        assert is_callable(draw_callback), 'draw callback must be a function type'
        callback_id = str(uuid4())
        self._draw_callbacks[callback_id] = draw_callback
        return callback_id

    def remove_draw_callback(self, callback_id):
        """
        Removes draw callback from ID.

        :param callback_id: Callback ID
        :type callback_id: str
        :return: None
        """
        assert isinstance_str(callback_id)
        if callback_id not in self._draw_callbacks.keys():
            raise IndexError('callback ID "{0}" does not exist'.format(callback_id))
        del self._draw_callbacks[callback_id]

    def apply_draw_callbacks(self):
        """
        Apply callbacks on widget draw.

        :return: None
        """
        if len(self._draw_callbacks) == 0:
            return
        for callback in self._draw_callbacks.values():
            callback(self, self._menu)

    def add_update_callback(self, update_callback):
        """
        Adds a function to the widget to be executed each time the widget is updated.

        The function that this method receives receives two objects: the widget itself and
        the menu reference. It is similar to ``add_draw_callback``.

        After creating a new callback, this functions returns the ID of the call. It can be removed
        anytime using ``widget.remove_update_callback(id)``.

        .. note::

            Not all widgets are updated, so the provided function may never be executed.

        :param update_callback: Function
        :type update_callback: callable
        :return: Callback ID
        :rtype: str
        """
        assert is_callable(update_callback), 'update callback must be a function type'
        callback_id = str(uuid4())
        self._update_callbacks[callback_id] = update_callback
        return callback_id

    def remove_update_callback(self, callback_id):
        """
        Removes update callback from ID.

        :param callback_id: Callback ID
        :type callback_id: str
        :return: None
        """
        assert isinstance_str(callback_id)
        if callback_id not in self._update_callbacks.keys():
            raise IndexError('callback ID "{0}" does not exist'.format(callback_id))
        del self._update_callbacks[callback_id]

    def apply_update_callbacks(self):
        """
        Apply callbacks on widget update.

        :return: None
        """
        if len(self._update_callbacks) == 0:
            return
        for callback in self._update_callbacks.values():
            callback(self, self._menu)

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

    def show(self):
        """
        Set widget visible.

        :return: None
        """
        self.visible = True
        self._render()
        if self._menu is not None:
            # noinspection PyProtectedMember
            self._menu._update_selection_if_hidden()

    def hide(self):
        """
        Hides widget.

        :return: None
        """
        self.visible = False
        self._render()
        if self._menu is not None:
            # noinspection PyProtectedMember
            self._menu._update_selection_if_hidden()


class _NullSelection(Selection):
    """
    Null selection. It redefines NoneSelection because that class cannot be
    imported.
    """

    def __init__(self):
        super(_NullSelection, self).__init__(
            margin_left=0, margin_right=0, margin_top=0, margin_bottom=0
        )

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface, widget):
        return
