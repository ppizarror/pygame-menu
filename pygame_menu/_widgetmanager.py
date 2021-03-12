"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENU WIDGET MANAGER
Easy widget add/remove to Menus.

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

__all__ = ['WidgetManager']

from io import BytesIO
from pathlib import Path
import re
import textwrap
import time
import webbrowser

import pygame

import pygame_menu
import pygame_menu.events as _events

from pygame_menu._base import Base
from pygame_menu.locals import CURSOR_HAND, INPUT_TEXT, ORIENTATION_VERTICAL, \
    ORIENTATION_HORIZONTAL
from pygame_menu.font import assert_font
from pygame_menu._scrollarea import get_scrollbars_from_position
from pygame_menu.utils import assert_vector, assert_color, assert_cursor, is_callable, \
    uuid4, parse_padding, assert_position_vector, warn
from pygame_menu.widgets.core.widget import Widget, check_widget_mouseleave
from pygame_menu.widgets.widget.colorinput import ColorInputColorType, ColorInputHexFormatType
from pygame_menu.widgets.widget.selector import SelectorStyleType, SELECTOR_STYLE_CLASSIC

from pygame_menu._types import Any, Union, Callable, Dict, Optional, CallbackType, \
    PaddingInstance, NumberType, Vector2NumberType, List, Tuple, NumberInstance, \
    Tuple3IntType


# noinspection PyProtectedMember
class WidgetManager(Base):
    """
    Add/Remove widgets to the Menu.

    :param menu: Menu reference
    """
    _menu: 'pygame_menu.Menu'

    def __init__(self, menu: 'pygame_menu.Menu') -> None:
        super(WidgetManager, self).__init__(object_id=menu.get_id() + '+widget-manager')
        self._menu = menu

    @property
    def _theme(self) -> 'pygame_menu.Theme':
        """
        Return menu theme.

        :return: Menu theme reference
        """
        return self._menu.get_theme()

    def _filter_widget_attributes(self, kwargs: Dict) -> Dict[str, Any]:
        """
        Return the valid widgets attributes from a dictionary.

        The valid (key, value) are removed from the initial dictionary.

        :param kwargs: Optional keyword arguments (input attributes)
        :return: Dictionary of valid attributes
        """
        attributes = {}

        # align
        align = kwargs.pop('align', self._theme.widget_alignment)
        assert isinstance(align, str)
        attributes['align'] = align

        # background_color
        background_is_color = False
        background_color = kwargs.pop('background_color',
                                      self._theme.widget_background_color)
        if background_color is not None:
            if isinstance(background_color, pygame_menu.BaseImage):
                pass
            else:
                background_color = assert_color(background_color)
                background_is_color = True
        attributes['background_color'] = background_color

        # background_inflate
        background_inflate = kwargs.pop('background_inflate',
                                        self._theme.widget_background_inflate)
        if background_inflate == 0:
            background_inflate = (0, 0)
        assert_vector(background_inflate, 2, int)
        assert background_inflate[0] >= 0 and background_inflate[1] >= 0, \
            'both background inflate components must be equal or greater than zero'
        attributes['background_inflate'] = background_inflate

        # border_color
        border_color = kwargs.pop('border_color',
                                  self._theme.widget_border_color)
        if border_color is not None:
            border_color = assert_color(border_color)
        attributes['border_color'] = border_color

        # border_inflate
        border_inflate = kwargs.pop('border_inflate',
                                    self._theme.widget_border_inflate)
        if border_inflate == 0:
            border_inflate = (0, 0)
        assert_vector(border_inflate, 2, int)
        assert isinstance(border_inflate[0], int) and border_inflate[0] >= 0
        assert isinstance(border_inflate[1], int) and border_inflate[1] >= 0
        attributes['border_inflate'] = border_inflate

        # border_position
        border_position = kwargs.pop('border_position',
                                     self._theme.widget_border_position)
        assert_position_vector(border_position)
        attributes['border_position'] = border_position

        # border_width
        border_width = kwargs.pop('border_width', self._theme.widget_border_width)
        assert isinstance(border_width, int) and border_width >= 0
        attributes['border_width'] = border_width

        # cursor
        cursor = kwargs.pop('cursor', self._theme.widget_cursor)
        assert_cursor(cursor)
        attributes['cursor'] = cursor

        # font_antialias
        attributes['font_antialias'] = self._theme.widget_font_antialias

        # font_background_color
        font_background_color = kwargs.pop('font_background_color',
                                           self._theme.widget_font_background_color)
        if font_background_color is None and \
                self._theme.widget_font_background_color_from_menu and \
                not background_is_color:
            if not isinstance(self._theme.background_color, pygame_menu.BaseImage):
                font_background_color = assert_color(self._theme.background_color)
        attributes['font_background_color'] = font_background_color

        # font_color
        font_color = kwargs.pop('font_color', self._theme.widget_font_color)
        attributes['font_color'] = assert_color(font_color)

        # font_name
        font_name = kwargs.pop('font_name', self._theme.widget_font)
        assert_font(font_name)
        attributes['font_name'] = str(font_name)

        # font_shadow
        font_shadow = kwargs.pop('font_shadow', self._theme.widget_font_shadow)
        assert isinstance(font_shadow, bool)
        attributes['font_shadow'] = font_shadow

        # font_shadow_color
        font_shadow_color = kwargs.pop('font_shadow_color',
                                       self._theme.widget_font_shadow_color)
        attributes['font_shadow_color'] = assert_color(font_shadow_color)

        # font_shadow_offset
        font_shadow_offset = kwargs.pop('font_shadow_offset',
                                        self._theme.widget_font_shadow_offset)
        assert isinstance(font_shadow_offset, int)
        attributes['font_shadow_offset'] = font_shadow_offset

        # font_shadow_position
        font_shadow_position = kwargs.pop('font_shadow_position',
                                          self._theme.widget_font_shadow_position)
        assert isinstance(font_shadow_position, str)
        attributes['font_shadow_position'] = font_shadow_position

        # font_size
        font_size = kwargs.pop('font_size', self._theme.widget_font_size)
        assert isinstance(font_size, int)
        assert font_size > 0, 'font size must be greater than zero'
        attributes['font_size'] = font_size

        # margin
        margin = kwargs.pop('margin', self._theme.widget_margin)
        if margin == 0:
            margin = (0, 0)
        assert_vector(margin, 2)
        attributes['margin'] = margin

        # padding
        padding = kwargs.pop('padding', self._theme.widget_padding)
        assert isinstance(padding, PaddingInstance)
        attributes['padding'] = padding

        # readonly_color
        readonly_color = kwargs.pop('readonly_color', self._theme.readonly_color)
        attributes['readonly_color'] = assert_color(readonly_color)

        # readonly_selected_color
        readonly_selected_color = kwargs.pop('readonly_selected_color',
                                             self._theme.readonly_selected_color)
        attributes['readonly_selected_color'] = assert_color(readonly_selected_color)

        # selection_color
        selection_color = kwargs.pop('selection_color', self._theme.selection_color)
        attributes['selection_color'] = assert_color(selection_color)

        # selection_effect
        selection_effect = kwargs.pop('selection_effect',
                                      self._theme.widget_selection_effect)
        if selection_effect is None:
            selection_effect = pygame_menu.widgets.NoneSelection()
        else:
            selection_effect = selection_effect.copy()
        assert isinstance(selection_effect, pygame_menu.widgets.core.Selection)
        attributes['selection_effect'] = selection_effect

        # tab_size
        attributes['tab_size'] = kwargs.pop('tab_size',
                                            self._theme.widget_tab_size)

        return attributes

    def _configure_widget(self, widget: 'Widget', **kwargs) -> None:
        """
        Update the given widget with the parameters defined at the Menu level.
        This method does not add widget to Menu.

        :param widget: Widget object
        :param kwargs: Optional keywords arguments
        :return: None
        """
        assert isinstance(widget, Widget)

        widget.set_alignment(
            align=kwargs['align']
        )
        widget.set_background_color(
            color=kwargs['background_color'],
            inflate=kwargs['background_inflate']
        )
        widget.set_border(
            color=kwargs['border_color'],
            inflate=kwargs['border_inflate'],
            position=kwargs['border_position'],
            width=kwargs['border_width']
        )
        widget.set_controls(
            joystick=self._menu._joystick,
            keyboard=self._menu._keyboard,
            mouse=self._menu._mouse,
            touchscreen=self._menu._touchscreen
        )
        widget.set_cursor(
            cursor=kwargs['cursor']
        )
        widget.set_font(
            antialias=kwargs['font_antialias'],
            background_color=kwargs['font_background_color'],
            color=kwargs['font_color'],
            font=kwargs['font_name'],
            font_size=kwargs['font_size'],
            readonly_color=kwargs['readonly_color'],
            readonly_selected_color=kwargs['readonly_selected_color'],
            selected_color=kwargs['selection_color']
        )
        widget.set_font_shadow(
            color=kwargs['font_shadow_color'],
            enabled=kwargs['font_shadow'],
            offset=kwargs['font_shadow_offset'],
            position=kwargs['font_shadow_position']
        )
        widget.set_margin(
            x=kwargs['margin'][0],
            y=kwargs['margin'][1]
        )
        widget.set_padding(
            padding=kwargs['padding']
        )
        widget.set_selection_effect(
            selection=kwargs['selection_effect']
        )
        widget.set_tab_size(
            tab_size=kwargs['tab_size']
        )

        if self._theme.widget_background_inflate_to_selection:
            widget.background_inflate_to_selection_effect()

        widget._update__repr___(self)

        widget.configured = True

    @staticmethod
    def _check_kwargs(kwargs: Dict) -> None:
        """
        Check kwargs after widget addition. It should be empty. Raises ``ValueError``.

        :param kwargs: Kwargs dict
        :return: None
        """
        for invalid_keyword in kwargs.keys():
            raise ValueError(
                'widget addition optional parameter kwargs.{} is not valid'.format(invalid_keyword)
            )

    def _append_widget(self, widget: 'Widget') -> None:
        """
        Add a widget to the list of widgets.

        :param widget: Widget object
        :return: None
        """
        assert isinstance(widget, Widget)
        if widget.get_menu() is None:
            widget.set_menu(self._menu)
        assert widget.get_menu() == self._menu, \
            'widget cannot have a different instance of menu'
        self._menu._check_id_duplicated(widget.get_id())

        if widget.get_scrollarea() is None:
            widget.set_scrollarea(self._menu.get_scrollarea())

        # Unselect
        widget.select(False)

        # Append to lists
        self._menu._widgets.append(widget)

        # Update selection index
        if self._menu._index < 0 and widget.is_selectable:
            widget.select()
            self._menu._index = len(self._menu._widgets) - 1

        # Force menu rendering, this checks if the menu overflows or has sizing}
        # errors; if added on execution time forces the update of the surface
        self._menu._widgets_surface = None
        try:
            self._menu._render()
        except (pygame_menu.menu._MenuSizingException,
                pygame_menu.menu._MenuWidgetOverflow):
            self._menu.remove_widget(widget)
            raise

        # Sort frame widgets, as render position changes frame position/frame
        if len(self._menu._update_frames) > 0:
            self._menu._update_frames[0].sort_menu_update_frames()

        # Update widgets
        check_widget_mouseleave()

    def configure_defaults_widget(self, widget: 'Widget') -> None:
        """
        Apply default menu settings to widget. This method does not add widget to
        the Menu.

        :param widget: Widget to be configured
        :return: None
        """
        self._configure_widget(widget, **self._filter_widget_attributes({}))

    def button(
            self,
            title: Any,
            action: Optional[Union['pygame_menu.Menu', '_events.MenuAction', Callable, int]] = None,
            *args,
            **kwargs
    ) -> 'pygame_menu.widgets.Button':
        """
        Adds a button to the Menu.

        The arguments and unknown keyword arguments are passed to the action, if
        it's a callable object:

        .. code-block:: python

            action(*args)

        If ``accept_kwargs=True`` then the ``**kwargs`` are also unpacked on action
        call:

        .. code-block:: python

            action(*args, **kwargs)

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``accept_kwargs``                 (bool) – Button action accepts ``**kwargs`` if it's a callable object (function-type), ``False`` by default
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``back_count``                    (int) – Number of menus to go back if action is :py:data:`pygame_menu.events.BACK` event, default is ``1``
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``button_id``                     (str) – Widget ID
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``onselect``                      (callable, None) – Callback executed when selecting the widget
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``tab_size``                      (int) – Width of a tab character
            - ``underline_color``               (tuple, list, str, int, :py:class:`pygame.Color`, None) – Color of the underline. If ``None`` use the same color of the text
            - ``underline_offset``              (int) – Vertical offset in px. ``2`` by default
            - ``underline_width``               (int) – Underline width in px. ``2`` by default
            - ``underline``                     (bool) – Enables text underline, using a properly placed decoration. ``False`` by default

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            Using ``action=None`` is the same as using ``action=pygame_menu.events.NONE``.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the button
        :param action: Action of the button, can be a Menu, an event, or a function
        :param args: Additional arguments used by a function
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Button`
        """
        total_back = kwargs.pop('back_count', 1)
        assert isinstance(total_back, int) and 1 <= total_back

        # Get ID
        button_id = kwargs.pop('button_id', '')
        assert isinstance(button_id, str), 'id must be a string'

        # Accept kwargs
        accept_kwargs = kwargs.pop('accept_kwargs', False)
        assert isinstance(accept_kwargs, bool)

        # Onselect callback
        onselect = kwargs.pop('onselect', None)

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        # Button underline
        underline = kwargs.pop('underline', False)
        underline_color = kwargs.pop('underline_color', attributes['font_color'])
        underline_offset = kwargs.pop('underline_offset', 1)
        underline_width = kwargs.pop('underline_width', 1)

        # Change action if certain events
        if action == _events.PYGAME_QUIT or action == _events.PYGAME_WINDOWCLOSE:
            action = _events.EXIT
        elif action is None:
            action = _events.NONE

        # If element is a Menu
        if isinstance(action, type(self._menu)):
            # Check for recursive
            if action == self._menu or action.in_submenu(self._menu, recursive=True):
                raise ValueError(
                    'Menu "{0}" is already on submenu structure, recursive menus'
                    'lead to unexpected behaviours. For returning to previous menu'
                    'use pygame_menu.events.BACK event defining an optional '
                    'back_count number of menus to return from, default is 1'
                    ''.format(action.get_title())
                )

            self._menu._submenus.append(action)
            widget = pygame_menu.widgets.Button(title, button_id, self._menu._open, action)
            widget.to_menu = True

        # If element is a MenuAction
        elif action == _events.BACK:  # Back to Menu
            widget = pygame_menu.widgets.Button(title, button_id, self._menu.reset, total_back)

        elif action == _events.CLOSE:  # Close Menu
            widget = pygame_menu.widgets.Button(title, button_id, self._menu._close)

        elif action == _events.EXIT:  # Exit program
            widget = pygame_menu.widgets.Button(title, button_id, self._menu._exit)

        elif action == _events.NONE:  # None action
            widget = pygame_menu.widgets.Button(title, button_id)

        elif action == _events.RESET:  # Back to Top Menu
            widget = pygame_menu.widgets.Button(title, button_id, self._menu.full_reset)

        # If element is a function or callable
        elif is_callable(action):
            if not accept_kwargs:
                widget = pygame_menu.widgets.Button(title, button_id, action, *args)
            else:
                widget = pygame_menu.widgets.Button(title, button_id, action, *args, **kwargs)

        else:
            raise ValueError('action must be a Menu, a MenuAction (event), a '
                             'function (callable), or None')

        # Configure and add the button
        if not accept_kwargs:
            try:
                self._check_kwargs(kwargs)
            except ValueError:
                warn('button cannot accept kwargs. If you want to use kwargs '
                     'options set accept_kwargs=True')
                raise

        self._configure_widget(widget=widget, **attributes)
        if underline:
            widget.add_underline(underline_color, underline_offset, underline_width)
        widget.set_selection_callback(onselect)
        self._append_widget(widget)
        return widget

    def color_input(
            self,
            title: Union[str, Any],
            color_type: ColorInputColorType,
            color_id: str = '',
            default: Union[str, Tuple3IntType] = '',
            hex_format: ColorInputHexFormatType = pygame_menu.widgets.COLORINPUT_HEX_FORMAT_NONE,
            input_separator: str = ',',
            input_underline: str = '_',
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            **kwargs
    ) -> 'pygame_menu.widgets.ColorInput':
        """
        Add a color widget with RGB or HEX format to the Menu.
        Includes a preview box that renders the given color.

        The callbacks (if defined) receive the current value and all unknown
        keyword arguments, where ``current_color=widget.get_value()``:

        .. code-block:: python

            onchange(current_color, **kwargs)
            onreturn(current_color, **kwargs)

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``dynamic_width``                 (bool) – If ``True`` the widget width changes if the previsualization color box is active or not
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``input_underline_vmargin``       (int) – Vertical margin of underline in px
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``previsualization_margin``       (int) – Previsualization left margin from text input in px. Default is ``0``
            - ``previsualization_width``        (int, float) – Previsualization width as a factor of the height. Default is ``3``
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the color input
        :param color_type: Type of the color input
        :param color_id: ID of the color input
        :param default: Default value to display, if RGB type it must be a tuple ``(r, g, b)``, if HEX must be a string ``"#XXXXXX"``
        :param hex_format: Hex format string mode
        :param input_separator: Divisor between RGB channels, not valid in HEX format
        :param input_underline: Underline character
        :param onchange: Callback executed when changing the values of the color text
        :param onreturn: Callback executed when pressing return on the color text input
        :param onselect: Callback executed when selecting the widget
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.ColorInput`
        """
        assert isinstance(default, (str, tuple))

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        dynamic_width = kwargs.pop('dynamic_width', True)
        input_underline_vmargin = kwargs.pop('input_underline_vmargin', 0)
        prev_margin = kwargs.pop('previsualization_margin', 10)
        prev_width = kwargs.pop('previsualization_width', 3)

        widget = pygame_menu.widgets.ColorInput(
            color_type=color_type,
            colorinput_id=color_id,
            cursor_color=self._theme.cursor_color,
            cursor_switch_ms=self._theme.cursor_switch_ms,
            dynamic_width=dynamic_width,
            hex_format=hex_format,
            input_separator=input_separator,
            input_underline=input_underline,
            input_underline_vmargin=input_underline_vmargin,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            prev_margin=prev_margin,
            prev_width_factor=prev_width,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        widget.set_default_value(default)

        return widget

    def image(
            self,
            image_path: Union[str, 'Path', 'pygame_menu.BaseImage', 'BytesIO'],
            angle: NumberType = 0,
            image_id: str = '',
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            scale: Vector2NumberType = (1, 1),
            scale_smooth: bool = True,
            selectable: bool = False,
            **kwargs
    ) -> 'pygame_menu.widgets.Image':
        """
        Add a simple image to the Menu.

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect. Applied only if ``selectable`` is ``True``

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param image_path: Path of the image (file) or a BaseImage object. If BaseImage object is provided the angle and scale are ignored
        :param angle: Angle of the image in degrees (clockwise)
        :param image_id: ID of the label
        :param onselect: Callback executed when selecting the widget; only executed if ``selectable`` is ``True``
        :param scale: Scale of the image on x-axis and y-axis (x, y)
        :param scale_smooth: Scale is smoothed
        :param selectable: Image accepts user selection
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Image`
        """
        assert isinstance(selectable, bool)

        # Remove invalid keys from kwargs
        for key in list(kwargs.keys()):
            if key not in ('align', 'background_color', 'background_inflate',
                           'border_color', 'border_inflate', 'border_width',
                           'cursor', 'margin', 'padding', 'selection_color',
                           'selection_effect', 'border_position'):
                kwargs.pop(key, None)

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        widget = pygame_menu.widgets.Image(
            angle=angle,
            image_id=image_id,
            image_path=image_path,
            onselect=onselect,
            scale=scale,
            scale_smooth=scale_smooth
        )
        widget.is_selectable = selectable

        self._check_kwargs(kwargs)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget

    def surface(
            self,
            surface: 'pygame.Surface',
            surface_id: str = '',
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            selectable: bool = False,
            **kwargs
    ) -> 'pygame_menu.widgets.SurfaceWidget':
        """
        Add a surface widget to the Menu.

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect. Applied only if ``selectable`` is ``True``

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param surface: Pygame surface object
        :param surface_id: Surface ID
        :param onselect: Callback executed when selecting the widget; only executed if ``selectable`` is ``True``
        :param selectable: Surface accepts user selection
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.SurfaceWidget`
        """
        assert isinstance(selectable, bool)

        # Remove invalid keys from kwargs
        for key in list(kwargs.keys()):
            if key not in ('align', 'background_color', 'background_inflate',
                           'border_color', 'border_inflate', 'border_width',
                           'cursor', 'margin', 'padding', 'selection_color',
                           'selection_effect', 'border_position'):
                kwargs.pop(key, None)

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        widget = pygame_menu.widgets.SurfaceWidget(
            surface=surface,
            surface_id=surface_id,
            onselect=onselect
        )
        widget.is_selectable = selectable

        self._check_kwargs(kwargs)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget

    def clock(
            self,
            clock_format: str = '%Y/%m/%d %H:%M:%S',
            clock_id: str = '',
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            selectable: bool = False,
            title_format: str = '{0}',
            **kwargs
    ) -> 'pygame_menu.widgets.Label':
        """
        Add a clock label to the Menu. This creates a Label with a text generator
        that request a string from ``time.strftime`` module using ``clock_format``.

        Commonly used format codes:
            - **%Y**    – Year with century as a decimal number
            - **%m**    – Month as a decimal number [01, 12]
            - **%d**    – Day of the month as a decimal number [01, 31]
            - **%H**    – Hour (24-hour clock) as a decimal number [00, 23]
            - **%M**    – Minute as a decimal number [00, 59]
            - **%S**    – Second as a decimal number [00, 61]
            - **%z**    – Time zone offset from UTC
            - **%a**    – Locale's abbreviated weekday name
            - **%A**    – Locale's full weekday name
            - **%b**    – Locale's abbreviated month name
            - **%B**    – Locale's full month name
            - **%c**    – Locale's appropriate date and time representation
            - **%I**    – Hour (12-hour clock) as a decimal number [01, 12]
            - **%p**    – Locale's equivalent of either AM or PM

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int,  :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect. Applied only if ``selectable`` is ``True``
            - ``tab_size``                      (int) – Width of a tab character
            - ``underline_color``               (tuple, list, str, int, :py:class:`pygame.Color`, None) – Color of the underline. If ``None`` use the same color of the text
            - ``underline_offset``              (int) – Vertical offset in px. ``2`` by default
            - ``underline_width``               (int) – Underline width in px. ``2`` by default
            - ``underline``                     (bool) – Enables text underline, using a properly placed decoration. ``False`` by default

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param clock_format: Format of clock used by ``time.strftime``
        :param clock_id: ID of the clock
        :param onselect: Callback executed when selecting the widget; only executed if ``selectable`` is ``True``
        :param selectable: Label accepts user selection; useful to move along the Menu using label selection
        :param title_format: Title format which accepts ``{0}`` as the string from ``time.strftime``, for example, ``'My Clock {0}'`` can be a title format
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Label`
        """
        label = self.label(
            title='',
            label_id=clock_id,
            onselect=onselect,
            selectable=selectable,
            **kwargs
        )

        assert isinstance(title_format, str) and '{0}' in title_format
        assert not isinstance(label, list)
        label.set_title_generator(lambda: title_format.format(time.strftime(clock_format)))
        label.update([])

        return label

    def label(
            self,
            title: Any,
            label_id: str = '',
            max_char: int = 0,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            selectable: bool = False,
            **kwargs
    ) -> Union['pygame_menu.widgets.Label', List['pygame_menu.widgets.Label']]:
        """
        Add a simple text to the Menu.

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect. Applied only if ``selectable`` is ``True``
            - ``tab_size``                      (int) – Width of a tab character
            - ``underline_color``               (tuple, list, str, int, :py:class:`pygame.Color`, None) – Color of the underline. If ``None`` use the same color of the text
            - ``underline_offset``              (int) – Vertical offset in px. ``2`` by default
            - ``underline_width``               (int) – Underline width in px. ``2`` by default
            - ``underline``                     (bool) – Enables text underline, using a properly placed decoration. ``False`` by default

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param title: Text to be displayed
        :param label_id: ID of the label
        :param max_char: Split the title in several labels if the string length exceeds ``max_char``; ``0``: don't split, ``-1``: split to Menu width
        :param onselect: Callback executed when selecting the widget; only executed if ``selectable`` is ``True``
        :param selectable: Label accepts user selection; useful to move along the Menu using label selection
        :param kwargs: Optional keyword arguments
        :return: Widget object, or List of widgets if the text overflows
        :rtype: :py:class:`pygame_menu.widgets.Label`, :py:class:`typing.List` [:py:class:`pygame_menu.widgets.Label`]
        """
        assert isinstance(label_id, str)
        assert isinstance(max_char, int)
        assert isinstance(selectable, bool)
        assert max_char >= -1

        title = str(title)
        if len(label_id) == 0:
            label_id = uuid4()

        # If newline detected, split in two new lines
        if '\n' in title:
            title = title.split('\n')
            widgets = []
            for t in title:
                wig = self.label(
                    title=t,
                    label_id=label_id + '+' + str(len(widgets) + 1),
                    max_char=max_char,
                    onselect=onselect,
                    selectable=selectable,
                    **kwargs
                )
                if isinstance(wig, list):
                    for w in wig:
                        widgets.append(w)
                else:
                    widgets.append(wig)
            return widgets

        # Wrap text to Menu width (imply additional calls to render functions)
        if max_char < 0:
            dummy_attrs = self._filter_widget_attributes(kwargs.copy())
            dummy = pygame_menu.widgets.Label(title=title)
            self._configure_widget(dummy, **dummy_attrs)
            max_char = int(1.0 * self._menu.get_width(inner=True) * len(title) / dummy.get_width())

        # If no overflow
        if len(title) <= max_char or max_char == 0:
            attributes = self._filter_widget_attributes(kwargs)

            # Filter additional parameters
            underline = kwargs.pop('underline', False)
            underline_color = kwargs.pop('underline_color', attributes['font_color'])
            underline_offset = kwargs.pop('underline_offset', 1)
            underline_width = kwargs.pop('underline_width', 1)

            widget = pygame_menu.widgets.Label(
                label_id=label_id,
                onselect=onselect,
                title=title
            )
            widget.is_selectable = selectable
            self._check_kwargs(kwargs)
            self._configure_widget(widget=widget, **attributes)

            if underline:
                widget.add_underline(underline_color, underline_offset, underline_width)

            self._append_widget(widget)

        else:
            self._menu._check_id_duplicated(label_id)  # Before adding + LEN
            widget = []
            for line in textwrap.wrap(title, max_char):
                widget.append(
                    self.label(
                        title=line,
                        label_id=label_id + '+' + str(len(widget) + 1),
                        max_char=max_char,
                        onselect=onselect,
                        selectable=selectable,
                        **kwargs
                    )
                )

        return widget

    def url(
            self,
            href: str,
            title: str = '',
            **kwargs
    ) -> 'pygame_menu.widgets.Button':
        """
        Adds a Button url to the Menu. Clicking the widget will open the link.
        If ``title`` is defined, the link will not be written. For example:
        ``href='google.com', title=''`` will write the link, but
        ``href='google.com', title='Google'`` will write 'Google' and opens
        'google.com' if clicked.

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over. By default is ``HAND``
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color. If not defined, uses ``theme.widget_url_color``
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``tab_size``                      (int) – Width of a tab character
            - ``underline_color``               (tuple, list, str, int, :py:class:`pygame.Color`, None) – Color of the underline. If ``None`` use the same color of the text
            - ``underline_offset``              (int) – Vertical offset in px. ``2`` by default
            - ``underline_width``               (int) – Underline width in px. ``2`` by default
            - ``underline``                     (bool) – Enables text underline, using a properly placed decoration. ``True`` by default

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param href: Link to open
        :param title: Alternative title of the link
        :param kwargs: Optional keyword arguments
        :return: Widget object, or List of widgets if the text overflows
        :rtype: :py:class:`pygame_menu.widgets.Button`
        """
        # Validate link
        assert isinstance(href, str) and len(href) > 0

        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        assert re.match(regex, href) is not None, 'invalid link format'

        def action() -> None:
            """
            Opens the link.
            """
            webbrowser.open(href)

        # Configure kwargs
        if 'cursor' not in kwargs.keys():
            kwargs['cursor'] = CURSOR_HAND
        if 'font_color' not in kwargs.keys():
            kwargs['font_color'] = self._theme.widget_url_color
        if 'selection_color' not in kwargs.keys():
            kwargs['selection_color'] = self._theme.widget_url_color
        if 'selection_effect' not in kwargs.keys():
            kwargs['selection_effect'] = pygame_menu.widgets.NoneSelection()
        if 'underline' not in kwargs.keys():
            kwargs['underline'] = True

        # Return new button
        return self.button(title if title != '' else href, action, **kwargs)

    def selector(
            self,
            title: Any,
            items: Union[List[Tuple[Any, ...]], List[str]],
            default: int = 0,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            selector_id: str = '',
            style: SelectorStyleType = SELECTOR_STYLE_CLASSIC,
            **kwargs
    ) -> 'pygame_menu.widgets.Selector':
        """
        Add a selector to the Menu: several items and two functions that are
        executed when changing the selector (left/right) and pressing return
        button on the selected item.

        The items of the selector are like:

        .. code-block:: python

            items = [('Item1', a, b, c...), ('Item2', d, e, f...)]

        The callbacks receive the current selected item, its index in the list,
        the associated arguments, and all unknown keyword arguments, where
        ``selected_item=widget.get_value()`` and ``selected_index=widget.get_index()``:

        .. code-block:: python

            onchange((selected_item, selected_index), a, b, c..., **kwargs)
            onreturn((selected_item, selected_index), a, b, c..., **kwargs)

        For example, if ``selected_index=0`` then ``selected_item=('Item1', a, b, c...)``.

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``style_fancy_arrow_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Arrow color of fancy style
            - ``style_fancy_arrow_margin``      (tuple, list) – Margin of arrows on x-axis and y-axis in px; format: (left, right, vertical)
            - ``style_fancy_bgcolor``           (tuple, list, str, int, :py:class:`pygame.Color`) – Background color of fancy style
            - ``style_fancy_bordercolor``       (tuple, list, str, int, :py:class:`pygame.Color`) – Border color of fancy style
            - ``style_fancy_borderwidth``       (int) – Border width of fancy style; ``1`` by default
            - ``style_fancy_box_inflate``       (tuple, list) – Box inflate of fancy style on x-axis and y-axis (x, y) in px
            - ``style_fancy_box_margin``        (tuple, list) – Box margin on x-axis and y-axis (x, y) in fancy style from title in px
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the selector
        :param items: Item list of the selector; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :param default: Index of default item to display
        :param onchange: Callback executed when when changing the selector
        :param onreturn: Callback executed when pressing return button
        :param onselect: Callback executed when selecting the widget
        :param selector_id: ID of the selector
        :param style: Selector style (visual)
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Selector`
        """
        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        # Get fancy style attributes
        style_fancy_arrow_color = kwargs.pop('style_fancy_arrow_color',
                                             self._theme.widget_box_arrow_color)
        style_fancy_arrow_margin = kwargs.pop('style_fancy_arrow_margin',
                                              self._theme.widget_box_arrow_margin)
        style_fancy_bgcolor = kwargs.pop('style_fancy_bgcolor',
                                         self._theme.widget_box_background_color)
        style_fancy_bordercolor = kwargs.pop('style_fancy_bordercolor',
                                             self._theme.widget_box_border_color)
        style_fancy_borderwidth = kwargs.pop('style_fancy_borderwidth',
                                             self._theme.widget_box_border_width)
        style_fancy_box_inflate = kwargs.pop('style_fancy_box_inflate',
                                             self._theme.widget_box_inflate)
        style_fancy_box_margin = kwargs.pop('style_fancy_box_margin',
                                            self._theme.widget_box_margin)

        widget = pygame_menu.widgets.Selector(
            default=default,
            items=items,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            selector_id=selector_id,
            style=style,
            style_fancy_arrow_color=style_fancy_arrow_color,
            style_fancy_arrow_margin=style_fancy_arrow_margin,
            style_fancy_bgcolor=style_fancy_bgcolor,
            style_fancy_bordercolor=style_fancy_bordercolor,
            style_fancy_borderwidth=style_fancy_borderwidth,
            style_fancy_box_inflate=style_fancy_box_inflate,
            style_fancy_box_margin=style_fancy_box_margin,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget

    def dropselect(
            self,
            title: Any,
            items: Union[List[Tuple[Any, ...]], List[str]],
            default: int = -1,
            dropselect_id: str = '',
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            open_middle: bool = False,
            placeholder: str = 'Select an option',
            placeholder_add_to_selection_box: bool = True,
            **kwargs
    ) -> 'pygame_menu.widgets.DropSelect':
        """
        Add a dropselect to the Menu: Drop select is a selector within a Frame.
        This drops a vertical frame if requested.

        Drop select can contain selectable items (options), but only one can be
        selected.

        The items of the DropSelect are:

        .. code-block:: python

            items = [('Item1', a, b, c...), ('Item2', d, e, f...)]

        The callbacks receive the current selected item, its index in the list,
        the associated arguments, and all unknown keyword arguments, where
        ``selected_item=widget.get_value()`` and ``selected_index=widget.get_index()``:

        .. code-block:: python

            onchange((selected_item, selected_index), a, b, c..., **kwargs)
            onreturn((selected_item, selected_index), a, b, c..., **kwargs)

        For example, if ``selected_index=0`` then ``selected_item=('Item1', a, b, c...)``.

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``tab_size``                      (int) – Width of a tab character

        kwargs for modifying selection box/option style (Optional)
            - ``scrollbar_color``                       (tuple, list, str, int, :py:class:`pygame.Color`) – Scrollbar color
            - ``scrollbar_cursor``                      (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the scrollbars if the mouse is placed over
            - ``scrollbar_shadow_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the shadow of each scrollbar
            - ``scrollbar_shadow_offset``               (int) – Offset of the scrollbar shadow in px
            - ``scrollbar_shadow_position``             (str) – Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
            - ``scrollbar_shadow``                      (bool) – Indicate if a shadow is drawn on each scrollbar
            - ``scrollbar_slider_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the sliders
            - ``scrollbar_slider_hover_color``          (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider if hovered or clicked
            - ``scrollbar_slider_pad``                  (int, float) – Space between slider and scrollbars borders in px
            - ``scrollbar_thick``                       (int) – Scrollbar thickness in px
            - ``scrollbars``                            (str) – Scrollbar position. See :py:mod:`pygame_menu.locals`
            - ``selection_box_arrow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Selection box arrow color
            - ``selection_box_arrow_margin``            (tuple) – Selection box arrow margin (left, right, vertical) in px
            - ``selection_box_bgcolor``                 (tuple, list, str, int, :py:class:`pygame.Color`) – Selection box background color
            - ``selection_box_border_color``            (tuple, list, str, int, :py:class:`pygame.Color`) – Selection box border color
            - ``selection_box_border_width``            (int) – Selection box border width
            - ``selection_box_height``                  (int) – Selection box height, counted as how many options are packed before showing scroll
            - ``selection_box_inflate``                 (tuple) – Selection box inflate on x-axis and y-axis (x, y) in px
            - ``selection_box_margin``                  (tuple, list) – Selection box on x-axis and y-axis (x, y) margin from title in px
            - ``selection_box_text_margin``             (int) – Selection box text margin (left) in px
            - ``selection_box_width``                   (int) – Selection box width in px. If ``0`` compute automatically to fit placeholder
            - ``selection_infinite``                    (bool) – If ``True`` selection can rotate through bottom/top
            - ``selection_option_border_color``         (tuple, list, str, int, :py:class:`pygame.Color`) – Option border color
            - ``selection_option_border_width``         (int) – Option border width
            - ``selection_option_font_color``           (tuple, list, str, int, :py:class:`pygame.Color`) – Option font color
            - ``selection_option_font_size``            (int, None) – Option font size. If ``None`` use the 75% of the widget font size
            - ``selection_option_font``                 (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Option font. If ``None`` use the same font as the widget
            - ``selection_option_padding``              (int, float, tuple, list ) – Selection padding. See padding styling
            - ``selection_option_selected_bgcolor``     (tuple, list, str, int, :py:class:`pygame.Color`) – Selected option background color
            - ``selection_option_selected_font_color``  (tuple, list, str, int, :py:class:`pygame.Color`) – Selected option font color

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Drop select title
        :param items: Item list of the drop select; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :param default: Index of default item to display
        :param dropselect_id: ID of the selector
        :param onchange: Callback when changing the drop select item
        :param onreturn: Callback when pressing return on the selected item
        :param onselect: Function when selecting the widget
        :param open_middle: If ``True`` the selection box is opened in the middle of the menu
        :param placeholder: Text shown if no option is selected yet
        :param placeholder_add_to_selection_box: If ``True`` adds the placeholder button to the selection box
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.DropSelect`
        """
        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        # Get selection box properties
        selection_box_arrow_color = kwargs.pop('selection_box_arrow_color',
                                               self._theme.widget_box_arrow_color)
        selection_box_arrow_margin = kwargs.pop('selection_box_arrow_margin',
                                                self._theme.widget_box_arrow_margin)
        selection_box_bgcolor = kwargs.pop('selection_box_bgcolor',
                                           self._theme.widget_box_background_color)
        selection_box_border_color = kwargs.pop('selection_box_border_color',
                                                self._theme.widget_box_border_color)
        selection_box_border_width = kwargs.pop('selection_box_border_width',
                                                self._theme.widget_box_border_width)
        selection_box_height = kwargs.pop('selection_box_height', 3)
        selection_box_inflate = kwargs.pop('selection_box_inflate',
                                           self._theme.widget_border_inflate)
        selection_box_margin = kwargs.pop('selection_box_margin',
                                          self._theme.widget_box_margin)
        selection_box_text_margin = kwargs.pop('selection_box_text_margin',
                                               self._theme.widget_box_arrow_margin[0])
        selection_box_width = kwargs.pop('selection_box_width', 0)
        selection_infinite = kwargs.pop('selection_infinite', False)
        selection_option_border_color = kwargs.pop('selection_option_border_color',
                                                   self._theme.scrollbar_color)
        selection_option_border_width = kwargs.pop('selection_option_border_width',
                                                   self._theme.widget_box_border_width)
        # selection_option_cursor = kwargs.pop('selection_option_cursor', None)
        selection_option_font = kwargs.pop('selection_option_font', None)
        selection_option_font_color = kwargs.pop('selection_option_font_color',
                                                 (0, 0, 0))
        selection_option_font_size = kwargs.pop('selection_option_font_size',
                                                None)
        selection_option_padding = kwargs.pop('selection_option_padding',
                                              (2, 5))
        selection_option_selected_bgcolor = kwargs.pop('selection_option_selected_bgcolor',
                                                       (188, 227, 244))
        selection_option_selected_font_color = kwargs.pop('selection_option_selected_font_color',
                                                          (0, 0, 0))

        # Get selection box scrollbar properties
        scrollbar_color = kwargs.pop('scrollbar_color',
                                     self._theme.scrollbar_color)
        scrollbar_cursor = kwargs.pop('scrollbar_cursor',
                                      self._theme.scrollbar_cursor)
        scrollbar_shadow_color = kwargs.pop('scrollbar_shadow_color',
                                            self._theme.scrollbar_shadow_color)
        scrollbar_shadow_offset = kwargs.pop('scrollbar_shadow_offset',
                                             self._theme.scrollbar_shadow_offset)
        scrollbar_shadow_position = kwargs.pop('scrollbar_shadow_position',
                                               self._theme.scrollbar_shadow_position)
        scrollbar_shadow = kwargs.pop('scrollbar_shadow',
                                      self._theme.scrollbar_shadow)
        scrollbar_slider_color = kwargs.pop('scrollbar_slider_color',
                                            self._theme.scrollbar_slider_color)
        scrollbar_slider_hover_color = kwargs.pop('scrollbar_slider_hover_color',
                                                  self._theme.scrollbar_slider_hover_color)
        scrollbar_slider_pad = kwargs.pop('scrollbar_slider_pad',
                                          self._theme.scrollbar_slider_pad)
        scrollbar_thick = kwargs.pop('scrollbar_thick',
                                     self._theme.scrollbar_thick)
        scrollbars = get_scrollbars_from_position(
            kwargs.pop('scrollbars', self._theme.scrollarea_position))

        widget = pygame_menu.widgets.DropSelect(
            default=default,
            dropselect_id=dropselect_id,
            items=items,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            open_middle=open_middle,
            placeholder=placeholder,
            placeholder_add_to_selection_box=placeholder_add_to_selection_box,
            selection_box_arrow_color=selection_box_arrow_color,
            selection_box_arrow_margin=selection_box_arrow_margin,
            selection_box_bgcolor=selection_box_bgcolor,
            selection_box_border_color=selection_box_border_color,
            selection_box_border_width=selection_box_border_width,
            selection_box_height=selection_box_height,
            selection_box_inflate=selection_box_inflate,
            selection_box_margin=selection_box_margin,
            selection_box_text_margin=selection_box_text_margin,
            selection_box_width=selection_box_width,
            selection_infinite=selection_infinite,
            selection_option_border_color=selection_option_border_color,
            selection_option_border_width=selection_option_border_width,
            # selection_option_cursor=selection_option_cursor,
            selection_option_font=selection_option_font,
            selection_option_font_color=selection_option_font_color,
            selection_option_font_size=selection_option_font_size,
            selection_option_padding=selection_option_padding,
            selection_option_selected_bgcolor=selection_option_selected_bgcolor,
            selection_option_selected_font_color=selection_option_selected_font_color,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        widget.set_theme(self._theme)
        self._append_widget(widget)

        # After addition, create drop
        widget.make_selection_drop(
            scrollbar_color=scrollbar_color,
            scrollbar_cursor=scrollbar_cursor,
            scrollbar_shadow=scrollbar_shadow,
            scrollbar_shadow_color=scrollbar_shadow_color,
            scrollbar_shadow_offset=scrollbar_shadow_offset,
            scrollbar_shadow_position=scrollbar_shadow_position,
            scrollbar_slider_color=scrollbar_slider_color,
            scrollbar_slider_hover_color=scrollbar_slider_hover_color,
            scrollbar_slider_pad=scrollbar_slider_pad,
            scrollbar_thick=scrollbar_thick,
            scrollbars=scrollbars,
            scrollbars_parsed=True
        )

        return widget

    def dropselect_multiple(
            self,
            title: Any,
            items: Union[List[Tuple[Any, ...]], List[str]],
            default: Optional[Union[int, List[int]]] = None,
            dropselect_multiple_id: str = '',
            max_selected: int = 0,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            open_middle: bool = False,
            placeholder: str = 'Select an option',
            placeholder_add_to_selection_box: bool = True,
            placeholder_selected: str = '{0} selected',
            **kwargs
    ) -> 'pygame_menu.widgets.DropSelectMultiple':
        """
        Add a dropselect multiple to the Menu: Drop select multiple is a drop
        select which can select many options at the same time. This drops a
        vertical frame if requested.

        The items of the DropSelectMultiple are:

        .. code-block:: python

            items = [('Item1', a, b, c...), ('Item2', d, e, f...), ('Item3', g, h, i...)]

        The callbacks receive the current selected items (tuple) and the indices
        (tuple), where ``selected_item=widget.get_value()`` and
        ``selected_index=widget.get_index()``:

        .. code-block:: python

            onchange((selected_item, selected_index), **kwargs)
            onreturn((selected_item, selected_index), **kwargs)

        For example, if ``selected_index=[0, 2]`` then ``selected_item=[('Item1', a, b, c...), ('Item3', g, h, i...)]``.

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``tab_size``                      (int) – Width of a tab character

        kwargs for modifying selection box/option style (Optional)
            - ``scrollbar_color``                       (tuple, list, str, int, :py:class:`pygame.Color`) – Scrollbar color
            - ``scrollbar_cursor``                      (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the scrollbars if the mouse is placed over
            - ``scrollbar_shadow_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the shadow of each scrollbar
            - ``scrollbar_shadow_offset``               (int) – Offset of the scrollbar shadow in px
            - ``scrollbar_shadow_position``             (str) – Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
            - ``scrollbar_shadow``                      (bool) – Indicate if a shadow is drawn on each scrollbar
            - ``scrollbar_slider_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the sliders
            - ``scrollbar_slider_hover_color``          (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider if hovered or clicked
            - ``scrollbar_slider_pad``                  (int, float) – Space between slider and scrollbars borders in px
            - ``scrollbar_thick``                       (int) – Scrollbar thickness in px
            - ``scrollbars``                            (str) – Scrollbar position. See :py:mod:`pygame_menu.locals`
            - ``selection_box_arrow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Selection box arrow color
            - ``selection_box_arrow_margin``            (tuple) – Selection box arrow margin (left, right, vertical) in px
            - ``selection_box_bgcolor``                 (tuple, list, str, int, :py:class:`pygame.Color`) – Selection box background color
            - ``selection_box_border_color``            (tuple, list, str, int, :py:class:`pygame.Color`) – Selection box border color
            - ``selection_box_border_width``            (int) – Selection box border width
            - ``selection_box_height``                  (int) – Selection box height, counted as how many options are packed before showing scroll
            - ``selection_box_inflate``                 (tuple) – Selection box inflate on x-axis and y-axis in px
            - ``selection_box_margin``                  (tuple, list) – Selection box on x-axis and y-axis (x, y) margin from title in px
            - ``selection_box_text_margin``             (int) – Selection box text margin (left) in px
            - ``selection_box_width``                   (int) – Selection box width in px. If ``0`` compute automatically to fit placeholder
            - ``selection_infinite``                    (bool) – If ``True`` selection can rotate through bottom/top
            - ``selection_option_active_bgcolor``       (tuple, list, str, int, :py:class:`pygame.Color`) – Active option(s) background color; active options is the currently active (by user)
            - ``selection_option_active_font_color``    (tuple, list, str, int, :py:class:`pygame.Color`) – Active option(s) font color
            - ``selection_option_border_color``         (tuple, list, str, int, :py:class:`pygame.Color`) – Option border color
            - ``selection_option_border_width``         (int) – Option border width
            - ``selection_option_font_color``           (tuple, list, str, int, :py:class:`pygame.Color`) – Option font color
            - ``selection_option_font_size``            (int, None) – Option font size. If ``None`` use the 75% of the widget font size
            - ``selection_option_font``                 (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Option font. If ``None`` use the same font as the widget
            - ``selection_option_padding``              (int, float, tuple, list) – Selection padding. See padding styling
            - ``selection_option_selected_bgcolor``     (tuple, list, str, int, :py:class:`pygame.Color`) – Selected option background color
            - ``selection_option_selected_box_border``  (int) – Box border width in px
            - ``selection_option_selected_box_color``   (tuple, list, str, int, :py:class:`pygame.Color`) – Box color
            - ``selection_option_selected_box_height``  (int, float) – Height of the selection box relative to the options height
            - ``selection_option_selected_box_margin``  (tuple, list) – Option box margin (left, right, vertical) in px
            - ``selection_option_selected_box``         (bool) – Draws a box in the selected option(s)
            - ``selection_option_selected_font_color``  (tuple, list, str, int, :py:class:`pygame.Color`) – Selected option font color

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Drop select title
        :param items: Item list of the drop select; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :param default: Index(es) of default item(s) to display. If ``None`` no item is selected
        :param dropselect_multiple_id: ID of the selector
        :param max_selected: Max items to be selected. If ``0`` there's no limit
        :param onchange: Callback when changing the drop select item
        :param onreturn: Callback when pressing return on the selected item
        :param onselect: Function when selecting the widget
        :param open_middle: If ``True`` the selection box is opened in the middle of the menu
        :param placeholder: Text shown if no option is selected yet
        :param placeholder_add_to_selection_box: If ``True`` adds the placeholder button to the selection box
        :param placeholder_selected: Text shown if option is selected. Accepts the number of selected options
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.DropSelectMultiple`
        """
        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        # Get selection box properties
        selection_box_arrow_color = kwargs.pop('selection_box_arrow_color',
                                               self._theme.widget_box_arrow_color)
        selection_box_arrow_margin = kwargs.pop('selection_box_arrow_margin',
                                                self._theme.widget_box_arrow_margin)
        selection_box_bgcolor = kwargs.pop('selection_box_bgcolor',
                                           self._theme.widget_box_background_color)
        selection_box_border_color = kwargs.pop('selection_box_border_color',
                                                self._theme.widget_box_border_color)
        selection_box_border_width = kwargs.pop('selection_box_border_width',
                                                self._theme.widget_box_border_width)
        selection_box_height = kwargs.pop('selection_box_height', 3)
        selection_box_inflate = kwargs.pop('selection_box_inflate',
                                           self._theme.widget_border_inflate)
        selection_box_margin = kwargs.pop('selection_box_margin',
                                          self._theme.widget_box_margin)
        selection_box_text_margin = kwargs.pop('selection_box_text_margin',
                                               self._theme.widget_box_arrow_margin[0])
        selection_box_width = kwargs.pop('selection_box_width', 0)
        selection_infinite = kwargs.pop('selection_infinite', False)
        selection_option_active_bgcolor = kwargs.pop('selection_option_active_bgcolor',
                                                     (188, 227, 244))
        selection_option_active_font_color = kwargs.pop('selection_option_active_font_color',
                                                        (0, 0, 0))
        selection_option_border_color = kwargs.pop('selection_option_border_color',
                                                   self._theme.scrollbar_color)
        selection_option_border_width = kwargs.pop('selection_option_border_width',
                                                   self._theme.widget_box_border_width)
        # selection_option_cursor = kwargs.pop('selection_option_cursor', None)
        selection_option_font = kwargs.pop('selection_option_font', None)
        selection_option_font_color = kwargs.pop('selection_option_font_color',
                                                 (0, 0, 0))
        selection_option_font_size = kwargs.pop('selection_option_font_size',
                                                None)
        selection_option_padding = kwargs.pop('selection_option_padding',
                                              (2, 5))
        selection_option_selected_bgcolor = kwargs.pop('selection_option_selected_bgcolor',
                                                       (142, 247, 141))
        selection_option_selected_box = kwargs.pop('selection_option_selected_box',
                                                   True)
        selection_option_selected_box_border = kwargs.pop('selection_option_selected_box_border',
                                                          self._theme.widget_box_border_width)
        selection_option_selected_box_color = kwargs.pop('selection_option_selected_box_color',
                                                         self._theme.widget_box_arrow_color)
        selection_option_selected_box_height = kwargs.pop('selection_option_selected_box_height',
                                                          0.5)
        selection_option_selected_box_margin = kwargs.pop('selection_option_selected_box_margin',
                                                          (0, self._theme.widget_box_arrow_margin[1],
                                                           self._theme.widget_box_arrow_margin[2]))
        selection_option_selected_font_color = kwargs.pop('selection_option_selected_font_color',
                                                          (0, 0, 0))

        # Get selection box scrollbar properties
        scrollbar_color = kwargs.pop('scrollbar_color',
                                     self._theme.scrollbar_color)
        scrollbar_cursor = kwargs.pop('scrollbar_cursor',
                                      self._theme.scrollbar_cursor)
        scrollbar_shadow_color = kwargs.pop('scrollbar_shadow_color',
                                            self._theme.scrollbar_shadow_color)
        scrollbar_shadow_offset = kwargs.pop('scrollbar_shadow_offset',
                                             self._theme.scrollbar_shadow_offset)
        scrollbar_shadow_position = kwargs.pop('scrollbar_shadow_position',
                                               self._theme.scrollbar_shadow_position)
        scrollbar_shadow = kwargs.pop('scrollbar_shadow',
                                      self._theme.scrollbar_shadow)
        scrollbar_slider_color = kwargs.pop('scrollbar_slider_color',
                                            self._theme.scrollbar_slider_color)
        scrollbar_slider_hover_color = kwargs.pop('scrollbar_slider_hover_color',
                                                  self._theme.scrollbar_slider_hover_color)
        scrollbar_slider_pad = kwargs.pop('scrollbar_slider_pad',
                                          self._theme.scrollbar_slider_pad)
        scrollbar_thick = kwargs.pop('scrollbar_thick',
                                     self._theme.scrollbar_thick)
        scrollbars = get_scrollbars_from_position(
            kwargs.pop('scrollbars', self._theme.scrollarea_position))

        widget = pygame_menu.widgets.DropSelectMultiple(
            default=default,
            dropselect_id=dropselect_multiple_id,
            items=items,
            max_selected=max_selected,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            open_middle=open_middle,
            placeholder=placeholder,
            placeholder_add_to_selection_box=placeholder_add_to_selection_box,
            placeholder_selected=placeholder_selected,
            selection_box_arrow_color=selection_box_arrow_color,
            selection_box_arrow_margin=selection_box_arrow_margin,
            selection_box_bgcolor=selection_box_bgcolor,
            selection_box_border_color=selection_box_border_color,
            selection_box_border_width=selection_box_border_width,
            selection_box_height=selection_box_height,
            selection_box_inflate=selection_box_inflate,
            selection_box_margin=selection_box_margin,
            selection_box_text_margin=selection_box_text_margin,
            selection_box_width=selection_box_width,
            selection_infinite=selection_infinite,
            selection_option_active_bgcolor=selection_option_active_bgcolor,
            selection_option_active_font_color=selection_option_active_font_color,
            selection_option_border_color=selection_option_border_color,
            selection_option_border_width=selection_option_border_width,
            # selection_option_cursor=selection_option_cursor,
            selection_option_font=selection_option_font,
            selection_option_font_color=selection_option_font_color,
            selection_option_font_size=selection_option_font_size,
            selection_option_padding=selection_option_padding,
            selection_option_selected_bgcolor=selection_option_selected_bgcolor,
            selection_option_selected_box=selection_option_selected_box,
            selection_option_selected_box_border=selection_option_selected_box_border,
            selection_option_selected_box_color=selection_option_selected_box_color,
            selection_option_selected_box_height=selection_option_selected_box_height,
            selection_option_selected_box_margin=selection_option_selected_box_margin,
            selection_option_selected_font_color=selection_option_selected_font_color,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        widget.set_theme(self._theme)
        self._append_widget(widget)

        # After addition, create drop
        widget.make_selection_drop(
            scrollbar_color=scrollbar_color,
            scrollbar_cursor=scrollbar_cursor,
            scrollbar_shadow=scrollbar_shadow,
            scrollbar_shadow_color=scrollbar_shadow_color,
            scrollbar_shadow_offset=scrollbar_shadow_offset,
            scrollbar_shadow_position=scrollbar_shadow_position,
            scrollbar_slider_color=scrollbar_slider_color,
            scrollbar_slider_hover_color=scrollbar_slider_hover_color,
            scrollbar_slider_pad=scrollbar_slider_pad,
            scrollbar_thick=scrollbar_thick,
            scrollbars=scrollbars,
            scrollbars_parsed=True
        )

        return widget

    def toggle_switch(
            self,
            title: Any,
            default: Union[int, bool] = 0,
            onchange: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            toggleswitch_id: str = '',
            state_text: Tuple[str, ...] = ('Off', 'On'),
            state_values: Tuple[Any, ...] = (False, True),
            width: int = 150,
            **kwargs
    ) -> 'pygame_menu.widgets.ToggleSwitch':
        """
        Add a toggle switch to the Menu: It can switch between two states.

        If user changes the status of the callback, ``onchange`` is fired:

        .. code-block:: python

            onchange(current_state_value, **kwargs)

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``infinite``                      (bool) – The state can rotate. ``False`` by default
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``slider_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider
            - ``slider_thickness``              (int) – Slider thickness in px. ``20`` px by default
            - ``state_color``                   (tuple) – 2-item color tuple for each state
            - ``state_text_font_color``         (tuple) – 2-item color tuple for each font state text color
            - ``state_text_font_size``          (str, None) – Font size of the state text. If ``None`` uses the widget font size
            - ``switch_border_color``           (tuple, list, str, int, :py:class:`pygame.Color`) – Switch border color
            - ``switch_border_width``           (int) – Switch border width
            - ``switch_height``                 (int, float) – Height factor respect to the title font size height
            - ``switch_margin``                 (tuple, list) – Switch on x-axis and y-axis (x, y) margin respect to the title of the widget in px
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            This method only handles two states. If you need more states (for example
            3, or 4), prefer using :py:class:`pygame_menu.widgets.ToggleSwitch`
            and add it as a generic widget.

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the toggle switch
        :param default: Default state index of the switch; it can be ``0 (False)`` or ``1 (True)``
        :param onchange: Callback executed when when changing the state of the toggle switch
        :param onselect: Callback executed when selecting the widget
        :param toggleswitch_id: Widget ID
        :param state_text: Text of each state
        :param state_values: Value of each state of the switch
        :param width: Width of the switch box in px
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.ToggleSwitch`
        """
        if isinstance(default, (int, bool)):
            assert 0 <= default <= 1, 'default value can be 0 or 1'
        else:
            raise ValueError(
                'invalid value type, default can be 0, False, 1, or True, but'
                'received "{0}"'.format(default)
            )

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        infinite = kwargs.pop('infinite', False)
        slider_color = kwargs.pop('slider_color',
                                  self._theme.widget_box_background_color)
        slider_thickness = kwargs.pop('slider_thickness',
                                      self._theme.scrollbar_thick)
        state_color = kwargs.pop('state_color',
                                 ((178, 178, 178), (117, 185, 54)))
        state_text_font_color = kwargs.pop('state_text_font_color',
                                           (self._theme.widget_box_background_color,
                                            self._theme.widget_box_background_color))
        state_text_font_size = kwargs.pop('state_text_font_size', None)
        switch_border_color = kwargs.pop('switch_border_color',
                                         self._theme.widget_box_border_color)
        switch_border_width = kwargs.pop('switch_border_width',
                                         self._theme.widget_box_border_width)
        switch_height = kwargs.pop('switch_height', 1)
        switch_margin = kwargs.pop('switch_margin', self._theme.widget_box_margin)

        widget = pygame_menu.widgets.ToggleSwitch(
            default_state=default,
            infinite=infinite,
            onchange=onchange,
            onselect=onselect,
            slider_color=slider_color,
            slider_thickness=slider_thickness,
            state_color=state_color,
            state_text=state_text,
            state_text_font_color=state_text_font_color,
            state_text_font_size=state_text_font_size,
            state_values=state_values,
            switch_border_color=switch_border_color,
            switch_border_width=switch_border_width,
            switch_height=switch_height,
            switch_margin=switch_margin,
            title=title,
            state_width=int(width),
            toggleswitch_id=toggleswitch_id,
            **kwargs
        )
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        widget.set_default_value(default)

        return widget

    def text_input(
            self,
            title: Any,
            default: Union[str, int, float] = '',
            copy_paste_enable: bool = True,
            cursor_selection_enable: bool = True,
            input_type: str = INPUT_TEXT,
            input_underline: str = '',
            input_underline_len: int = 0,
            maxchar: int = 0,
            maxwidth: int = 0,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            password: bool = False,
            textinput_id: str = '',
            valid_chars: Optional[List[str]] = None,
            **kwargs
    ) -> 'pygame_menu.widgets.TextInput':
        """
        Add a text input to the Menu: free text area and two functions that
        execute when changing the text and pressing return button on the element.

        The callbacks receive the current value and all unknown keyword arguments,
        where ``current_text=widget.get_value``:

        .. code-block:: python

            onchange(current_text, **kwargs)
            onreturn(current_text, **kwargs)

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``input_underline_vmargin``       (int) – Vertical margin of underline in px
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the text input
        :param default: Default value to display
        :param copy_paste_enable: Enable text copy, paste and cut
        :param cursor_selection_enable: Enable text selection on input
        :param input_type: Data type of the input. See :py:mod:`pygame_menu.locals`
        :param input_underline: Underline character
        :param input_underline_len: Total of characters to be drawn under the input. If ``0`` this number is computed automatically to fit the font
        :param maxchar: Maximum length of string, if 0 there's no limit
        :param maxwidth: Maximum size of the text widget (in number of chars), if ``0`` there's no limit
        :param onchange: Callback executed when changing the text input
        :param onreturn: Callback executed when pressing return on the text input
        :param onselect: Callback executed when selecting the widget
        :param password: Text input is a password
        :param textinput_id: ID of the text input
        :param valid_chars: List of authorized chars. ``None`` if all chars are valid
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.TextInput`
        """
        assert isinstance(default, (str, NumberInstance))

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)
        input_underline_vmargin = kwargs.pop('input_underline_vmargin', 0)

        # If password is active no default value should exist
        if password and default != '':
            raise ValueError('default value must be empty if the input is a password')

        widget = pygame_menu.widgets.TextInput(
            copy_paste_enable=copy_paste_enable,
            cursor_color=self._theme.cursor_color,
            cursor_selection_color=self._theme.cursor_selection_color,
            cursor_selection_enable=cursor_selection_enable,
            cursor_switch_ms=self._theme.cursor_switch_ms,
            input_type=input_type,
            input_underline=input_underline,
            input_underline_len=input_underline_len,
            input_underline_vmargin=input_underline_vmargin,
            maxchar=maxchar,
            maxwidth=maxwidth,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            password=password,
            textinput_id=textinput_id,
            title=title,
            valid_chars=valid_chars,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        widget.set_default_value(default)

        return widget

    def _frame(
            self,
            width: NumberType,
            height: NumberType,
            orientation: str,
            frame_id: str = '',
            **kwargs
    ) -> 'pygame_menu.widgets.Frame':
        """
        Adds a frame to the Menu.

        :param width: Frame width in px
        :param height: Frame height in px
        :param orientation: Frame orientation, horizontal or vertical. See :py:mod:`pygame_menu.locals`
        :param frame_id: ID of the frame
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Frame`
        """
        # Remove invalid keys from kwargs
        for key in list(kwargs.keys()):
            if key not in ('align', 'background_color', 'background_inflate',
                           'border_color', 'border_inflate', 'border_width',
                           'cursor', 'margin', 'padding', 'max_height', 'max_width',
                           'scrollbar_color', 'scrollbar_cursor',
                           'scrollbar_shadow_color', 'scrollbar_shadow_offset',
                           'scrollbar_shadow_position', 'scrollbar_shadow',
                           'scrollbar_slider_color', 'scrollbar_slider_pad',
                           'scrollbar_thick', 'scrollbars', 'scrollarea_color',
                           'border_position', 'scrollbar_slider_hover_color',
                           'tab_size'):
                kwargs.pop(key, None)

        attributes = self._filter_widget_attributes(kwargs)
        pad = parse_padding(attributes['padding'])  # top, right, bottom, left
        pad_h = pad[1] + pad[3]
        pad_v = pad[0] + pad[2]

        assert width > pad_h, \
            'frame width ({0}) cannot be lower than horizontal padding size ({1})' \
            ''.format(width, pad_h)
        assert height > pad_v, \
            'frame height ({0}) cannot be lower than vertical padding size ({1})' \
            ''.format(height, pad_v)

        widget = pygame_menu.widgets.Frame(
            width=width - pad_h,
            height=height - pad_v,
            orientation=orientation,
            frame_id=frame_id
        )
        self._configure_widget(widget=widget, **attributes)

        widget.make_scrollarea(
            max_height=kwargs.pop('max_height', height) - pad_v,
            max_width=kwargs.pop('max_width', width) - pad_h,
            scrollarea_color=kwargs.pop('scrollarea_color', None),
            scrollbar_color=kwargs.pop('scrollbar_color',
                                       self._theme.scrollbar_color),
            scrollbar_cursor=kwargs.pop('scrollbar_cursor',
                                        self._theme.scrollbar_cursor),
            scrollbar_shadow=kwargs.pop('scrollbar_shadow',
                                        self._theme.scrollbar_shadow),
            scrollbar_shadow_color=kwargs.pop('scrollbar_shadow_color',
                                              self._theme.scrollbar_shadow_color),
            scrollbar_shadow_offset=kwargs.pop('scrollbar_shadow_offset',
                                               self._theme.scrollbar_shadow_offset),
            scrollbar_shadow_position=kwargs.pop('scrollbar_shadow_position',
                                                 self._theme.scrollbar_shadow_position),
            scrollbar_slider_color=kwargs.pop('scrollbar_slider_color',
                                              self._theme.scrollbar_slider_color),
            scrollbar_slider_hover_color=kwargs.pop('scrollbar_slider_hover_color',
                                                    self._theme.scrollbar_slider_hover_color),
            scrollbar_slider_pad=kwargs.pop('scrollbar_slider_pad',
                                            self._theme.scrollbar_slider_pad),
            scrollbar_thick=kwargs.pop('scrollbar_thick',
                                       self._theme.scrollbar_thick),
            scrollbars=get_scrollbars_from_position(
                kwargs.pop('scrollbars', self._theme.scrollarea_position))
        )

        self._append_widget(widget)
        self._check_kwargs(kwargs)

        return widget

    def frame_h(
            self,
            width: NumberType,
            height: NumberType,
            frame_id: str = '',
            **kwargs
    ) -> 'pygame_menu.widgets.Frame':
        """
        Adds a horizontal frame to the Menu. Frame is a widget container that
        packs many widgets within. All contained widgets have a floating position,
        and use only 1 position in column/row layout.

        .. code-block:: python

            frame.pack(W1, alignment=ALIGN_LEFT, vertical_position=POSITION_NORTH)
            frame.pack(W2, alignment=ALIGN_LEFT, vertical_position=POSITION_CENTER)
            frame.pack(W3, alignment=ALIGN_LEFT, vertical_position=POSITION_SOUTH)
            ...

            ----------------
            |W1            |
            |   W2     ... |
            |      W3      |
            ----------------

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the frame if the mouse is placed over
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``max_height``                    (int) – Max height in px. If lower than the frame height a scrollbar will appear on vertical axis. ``None`` by default (same height)
            - ``max_width``                     (int) – Max width in px. If lower than the frame width a scrollbar will appear on horizontal axis. ``None`` by default (same width)
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``scrollarea_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`,None) – Scroll area color. If ``None`` area is transparent
            - ``scrollbar_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Scrollbar color
            - ``scrollbar_cursor``              (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the scrollbars if the mouse is placed over
            - ``scrollbar_shadow_color``        (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the shadow of each scrollbar
            - ``scrollbar_shadow_offset``       (int) – Offset of the scrollbar shadow in px
            - ``scrollbar_shadow_position``     (str) – Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
            - ``scrollbar_shadow``              (bool) – Indicate if a shadow is drawn on each scrollbar
            - ``scrollbar_slider_color``        (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the sliders
            - ``scrollbar_slider_hover_color``  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider if hovered or clicked
            - ``scrollbar_slider_pad``          (int, float) – Space between slider and scrollbars borders in px
            - ``scrollbar_thick``               (int) – Scrollbar thickness in px
            - ``scrollbars``                    (str) – Scrollbar position. See :py:mod:`pygame_menu.locals`
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            If horizontal frame contains a scrollarea (setting ``max_height`` or
            ``max_width`` less than size) padding will be set at zero.

        .. note::

            Packing applies a virtual translation to the widget, previous translation
            is not modified.

        .. note::

            Widget floating is also considered within frames. If a widget is
            floating, it does not add any size to the respective positioning.

        .. note::

            The Frame size created with this method does consider the padding. Thus,
            if Frame is created with ``width=100``, ``height=200`` and ``padding=25``
            the final internal size is ``width=50`` and ``height=150``.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param width: Frame width in px
        :param height: Frame height in px
        :param frame_id: ID of the horizontal frame
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Frame`
        """
        return self._frame(width, height, ORIENTATION_HORIZONTAL, frame_id, **kwargs)

    def frame_v(
            self,
            width: NumberType,
            height: NumberType,
            frame_id: str = '',
            **kwargs
    ) -> 'pygame_menu.widgets.Frame':
        """
        Adds a vertical frame to the Menu. Frame is a widget container that packs
        many widgets within. All contained widgets have a floating position, and
        use only 1 position in column/row layout.

        .. code-block:: python

            frame.pack(W1, alignment=ALIGN_LEFT)
            frame.pack(W2, alignment=ALIGN_CENTER)
            frame.pack(W3, alignment=ALIGN_RIGHT)
            ...

            --------
            |W1    |
            |  W2  |
            |    W3|
            | ...  |
            --------

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the frame if the mouse is placed over
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``max_height``                    (int) – Max height in px. If lower than the frame height a scrollbar will appear on vertical axis. ``None`` by default (same height)
            - ``max_width``                     (int) – Max width in px. If lower than the frame width a scrollbar will appear on horizontal axis. ``None`` by default (same width)
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``scrollarea_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`,None) – Scroll area color. If ``None`` area is transparent
            - ``scrollbar_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Scrollbar color
            - ``scrollbar_cursor``              (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the scrollbars if the mouse is placed over
            - ``scrollbar_shadow_color``        (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the shadow of each scrollbar
            - ``scrollbar_shadow_offset``       (int) – Offset of the scrollbar shadow in px
            - ``scrollbar_shadow_position``     (str) – Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
            - ``scrollbar_shadow``              (bool) – Indicate if a shadow is drawn on each scrollbar
            - ``scrollbar_slider_color``        (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the sliders
            - ``scrollbar_slider_hover_color``  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider if hovered or clicked
            - ``scrollbar_slider_pad``          (int, float) – Space between slider and scrollbars borders in px
            - ``scrollbar_thick``               (int) – Scrollbar thickness in px
            - ``scrollbars``                    (str) – Scrollbar position. See :py:mod:`pygame_menu.locals`
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            If vertical frame contains a scrollarea (setting ``max_height`` or
            ``max_width`` less than size) padding will be set at zero.

        .. note::

            Packing applies a virtual translation to the widget, previous translation
            is not modified.

        .. note::

            Widget floating is also considered within frames. If a widget is
            floating, it does not add any size to the respective positioning.

        .. note::

            The Frame size created with this method does consider the padding. Thus,
            if Frame is created with ``width=100``, ``height=200`` and ``padding=25``
            the final internal size is ``width=50`` and ``height=150``.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param width: Frame width in px
        :param height: Frame height in px
        :param frame_id: ID of the vertical frame
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Frame`
        """
        return self._frame(width, height, ORIENTATION_VERTICAL, frame_id, **kwargs)

    def table(
            self,
            table_id: str = '',
            **kwargs
    ) -> 'pygame_menu.widgets.Table':
        """
        Adds a Table to the Menu. A table is a frame which can pack widgets in a
        structured way.

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the frame if the mouse is placed over
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``max_height``                    (int) – Max height in px. If lower than the frame height a scrollbar will appear on vertical axis. ``None`` by default (same height)
            - ``max_width``                     (int) – Max width in px. If lower than the frame width a scrollbar will appear on horizontal axis. ``None`` by default (same width)
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param table_id: ID of the table
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Table`
        """
        attributes = self._filter_widget_attributes(kwargs)

        widget = pygame_menu.widgets.Table(
            table_id=table_id
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        self._check_kwargs(kwargs)

        return widget

    def _horizontal_margin(
            self,
            margin: NumberType,
            margin_id: str = ''
    ) -> 'pygame_menu.widgets.HMargin':
        """
        Adds a horizontal margin to the Menu. Only useful in frames.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param margin: Horizontal margin in px
        :param margin_id: ID of the margin
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.HMargin`
        """
        assert isinstance(margin, NumberInstance)
        assert margin > 0, \
            'zero margin is not valid, prefer adding a NoneWidget menu.add.none_widget()'

        attributes = self._filter_widget_attributes({})
        widget = pygame_menu.widgets.HMargin(margin, widget_id=margin_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget

    def vertical_margin(
            self,
            margin: NumberType,
            margin_id: str = ''
    ) -> 'pygame_menu.widgets.VMargin':
        """
        Adds a vertical margin to the Menu.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param margin: Vertical margin in px
        :param margin_id: ID of the margin
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.VMargin`
        """
        assert isinstance(margin, NumberInstance)
        assert margin > 0, 'negative or zero margin is not valid'

        attributes = self._filter_widget_attributes({})
        widget = pygame_menu.widgets.VMargin(margin, widget_id=margin_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget

    def none_widget(
            self,
            widget_id: str = ''
    ) -> 'pygame_menu.widgets.NoneWidget':
        """
        Add a none widget to the Menu.

        .. note::

            This widget is useful to fill column/rows layout without compromising
            any visuals. Also it can be used to store information or even to add
            a ``draw_callback`` function to it for being called on each Menu draw.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param widget_id: Widget ID
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.NoneWidget`
        """
        attributes = self._filter_widget_attributes({})

        widget = pygame_menu.widgets.NoneWidget(widget_id=widget_id)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget

    def generic_widget(
            self,
            widget: 'Widget',
            configure_defaults: bool = False
    ) -> 'Widget':
        """
        Add generic widget to the Menu.

        .. note::

            The widget should be fully configured by the user: font, padding, etc.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Unintended behaviours may happen while using this method, use only with
            caution; specially while creating nested submenus with buttons.

        :param widget: Widget to be added
        :param configure_defaults: Apply defaults widget configuration (for example, theme)
        :return: The added widget object
        :rtype: :py:class:`pygame_menu.widgets.Widget`
        """
        assert isinstance(widget, Widget)
        if widget.get_menu() is not None:
            raise ValueError('widget to be added is already appended to another Menu')

        # Raise warning if adding button with Menu
        if isinstance(widget, pygame_menu.widgets.Button) and widget.to_menu:
            warn(
                'prefer adding nested submenus using add_button method instead, '
                'unintended behaviours may occur'
            )

        # Configure widget
        if configure_defaults:
            self.configure_defaults_widget(widget)
        self._append_widget(widget)

        return widget
