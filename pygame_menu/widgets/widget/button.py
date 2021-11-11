"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUTTON
Button class, manage elements and adds entries to Menu.
"""

__all__ = [
    'Button',
    'ButtonManager'
]

import pygame
import pygame_menu
import pygame_menu.controls as ctrl
import pygame_menu.events as _events
import re
import webbrowser

from abc import ABC
from pygame_menu.locals import FINGERUP, CURSOR_HAND
from pygame_menu.utils import is_callable, assert_color, get_finger_pos, warn
from pygame_menu.widgets.core.widget import AbstractWidgetManager, Widget

from pygame_menu._types import Any, CallbackType, Callable, Union, List, Tuple, \
    Optional, ColorType, ColorInputType, EventVectorType


# noinspection PyMissingOrEmptyDocstring
class Button(Widget):
    """
    Button widget.

    The arguments and unknown keyword arguments are passed to the ``onreturn``
    function:

    .. code-block:: python

        onreturn(*args, **kwargs)

    .. note::

        Button accepts all transformations.

    :param title: Button title
    :param button_id: Button ID
    :param onreturn: Callback when pressing the button
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments
    """
    _last_underline: List[Union[str, Optional[Tuple[ColorType, int, int]]]]  # deco id, (color, offset, width)
    to_menu: bool

    def __init__(
            self,
            title: Any,
            button_id: str = '',
            onreturn: CallbackType = None,
            *args,
            **kwargs
    ) -> None:
        super(Button, self).__init__(
            args=args,
            kwargs=kwargs,
            onreturn=onreturn,
            title=title,
            widget_id=button_id
        )
        self._accept_events = True
        self._last_underline = ['', None]
        self.to_menu = False  # True if the button opens a new Menu

    def _apply_font(self) -> None:
        pass

    def set_selection_callback(
            self,
            callback: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]]
    ) -> None:
        """
        Update the button selection callback, once button is selected, the callback
        function is executed as follows:

        .. code-block:: python

            callback(selected, widget, menu)

        :param callback: Callback when selecting the widget, executed in :py:meth:`pygame_menu.widgets.core.widget.Widget.set_selected`
        :return: None
        """
        if callback is not None:
            assert is_callable(callback), \
                'callback must be callable (function-type) or None'
        self._onselect = callback

    def update_callback(self, callback: Callable, *args) -> None:
        """
        Update function triggered by the button; ``callback`` cannot point to a Menu, that
        behaviour is only valid using :py:meth:`pygame_menu.menu.Menu.add.button` method.

        .. note::

            If button points to a submenu, and the callback is changed to a
            function, the submenu will be removed from the parent Menu. Thus
            preserving the structure.

        :param callback: Function
        :param args: Arguments used by the function once triggered
        :return: None
        """
        assert is_callable(callback), \
            'only callable (function-type) are allowed'

        # If return is a Menu object, remove it from submenus list
        if self._menu is not None and self._onreturn is not None and self.to_menu:
            assert len(self._args) == 1
            submenu = self._args[0]  # Menu
            assert self._menu.in_submenu(submenu), \
                'pointed menu is not in submenu list of parent container'
            # noinspection PyProtectedMember
            assert self._menu._remove_submenu(submenu, self), \
                'submenu could not be removed'
            self.to_menu = False

        self._args = args or []
        self._onreturn = callback

    def add_underline(
            self,
            color: ColorInputType,
            offset: int,
            width: int,
            force_render: bool = False
    ) -> 'Button':
        """
        Adds a underline to text. This is added if widget is rendered.

        :param color: Underline color
        :param offset: Underline offset
        :param width: Underline width
        :param force_render: If ``True`` force widget render after addition
        :return: Self reference
        """
        color = assert_color(color)
        assert isinstance(offset, int)
        assert isinstance(width, int) and width > 0
        self._last_underline[1] = (color, offset, width)
        if force_render:
            self._force_render()
        return self

    def remove_underline(self) -> 'Button':
        """
        Remove underline of the button.

        :return: Self reference
        """
        if self._last_underline[0] != '':
            self._decorator.remove(self._last_underline[0])
            self._last_underline[0] = ''
        return self

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface, self._rect.topleft)

    def _render(self) -> Optional[bool]:
        if not self._render_hash_changed(
                self._selected, self._title, self._visible, self.readonly,
                self._last_underline[1]):
            return True

        # Render surface
        self._surface = self._render_string(self._title, self.get_font_color_status())
        self._apply_transforms()
        self._rect.width, self._rect.height = self._surface.get_size()

        # Add underline if enabled
        self.remove_underline()
        if self._last_underline[1] is not None:
            w = self._surface.get_width()
            h = self._surface.get_height()
            color, offset, width = self._last_underline[1]
            if w > 0 and h > 0:
                self._last_underline[0] = self._decorator.add_line(
                    pos1=(-w / 2, h / 2 + offset),
                    pos2=(w / 2, h / 2 + offset),
                    color=color,
                    width=width
                )

        self.force_menu_surface_update()

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)
        rect = self.get_rect(to_real_position=True)

        if self.readonly or not self.is_visible():
            self._readonly_check_mouseover(events, rect)
            return False

        for event in events:

            # Check mouse over
            self._check_mouseover(event, rect)

            # User applies with key
            if event.type == pygame.KEYDOWN and self._keyboard_enabled and \
                    event.key == ctrl.KEY_APPLY or \
                    event.type == pygame.JOYBUTTONDOWN and self._joystick_enabled and \
                    event.button == ctrl.JOY_BUTTON_SELECT:
                if self.to_menu:
                    self._sound.play_open_menu()
                else:
                    self._sound.play_key_add()
                self.apply()
                return True

            # User clicks the button; don't consider the mouse wheel (button 4 & 5)
            elif event.type == pygame.MOUSEBUTTONUP and self._mouse_enabled and \
                    event.button in (1, 2, 3) or \
                    event.type == FINGERUP and self._touchscreen_enabled and \
                    self._menu is not None:
                if event.type == pygame.MOUSEBUTTONUP:
                    self._sound.play_click_mouse()
                else:
                    self._sound.play_click_touch()

                event_pos = get_finger_pos(self._menu, event)
                if rect.collidepoint(*event_pos):
                    self.apply()
                    return True

        return False


class ButtonManager(AbstractWidgetManager, ABC):
    """
    Button manager.
    """

    # noinspection PyProtectedMember
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
            - ``float``                         (bool) - If ``True`` the widget don't contributes width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
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
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
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
                    f'{action.get_class_id()} title "{action.get_title()}" is '
                    f'already on submenu structure, recursive menus lead to '
                    f'unexpected behaviours. For returning to previous menu'
                    f'use pygame_menu.events.BACK event defining an optional '
                    f'back_count number of menus to return from, default is 1'
                )

            widget = Button(title, button_id, self._menu._open, action)
            widget.to_menu = True

        # If element is a MenuAction
        elif action == _events.BACK:  # Back to Menu
            widget = Button(title, button_id, self._menu.reset, total_back)

        elif action == _events.CLOSE:  # Close Menu
            widget = Button(title, button_id, self._menu._close)

        elif action == _events.EXIT:  # Exit program
            widget = Button(title, button_id, self._menu._exit)

        elif action == _events.NONE:  # None action
            widget = Button(title, button_id)

        elif action == _events.RESET:  # Back to Top Menu
            widget = Button(title, button_id, self._menu.full_reset)

        # If element is a function or callable
        elif is_callable(action):
            if not accept_kwargs:
                widget = Button(title, button_id, action, *args)
            else:
                widget = Button(title, button_id, action, *args, **kwargs)

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

        # Add to submenu
        if widget.to_menu:
            self._add_submenu(action, widget)

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
            - ``float``                         (bool) - If ``True`` the widget don't contributes width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
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
        return self.button(title if title != '' else href, lambda: webbrowser.open(href), **kwargs)
