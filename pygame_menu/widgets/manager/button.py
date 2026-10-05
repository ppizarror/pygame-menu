"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BUTTON MANAGER
Base class for ButtonManager.
"""

from __future__ import annotations

__all__ = ["ButtonManager"]

import re
import webbrowser
from abc import ABC
from typing import TYPE_CHECKING, Any

import pygame

import pygame_menu
import pygame_menu.events as _events
from pygame_menu.locals import CURSOR_HAND
from pygame_menu.utils import warn
from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.button import Button

if TYPE_CHECKING:
    from collections.abc import Callable

# Module-level compiled regex for URL validation
_URL_REGEX = re.compile(
    r"^(?:http|ftp)s?://"  # http:// or https://
    r"(?:(?:[A-Z\d](?:[A-Z\d-]{0,61}[A-Z\d])?\.)+(?:[A-Z]{2,6}\.?|[A-Z\d-]{2,}\.?)|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


class ButtonManager(AbstractWidgetManager, ABC):
    """
    Button manager.
    """

    # noinspection PyProtectedMember
    def banner(
        self,
        image: pygame_menu.BaseImage | pygame.Surface,
        action: pygame_menu.Menu | _events.MenuAction | Callable | int | None = None,
        *args,
        **kwargs,
    ) -> Button:
        """
        Adds a clickeable image to the Menu with same behavior as a Button.

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
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``button_id``                     (str) – Widget ID
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``onselect``                      (callable, None) – Callback executed when selecting the widget
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            Using ``action=None`` is the same as using ``action=pygame_menu.events.NONE``.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param image: Image or surface to display as the clickable banner.
        :param action: Action of the button, can be a Menu, an event, or a function
        :param args: Additional arguments used by a function
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Button`
        """
        if isinstance(image, pygame.Surface):
            image = pygame_menu.BaseImage(image)

        # We use setdefault so we don't overwrite the user
        # but WE provide the values for the filter to "pop"
        kwargs.setdefault("padding", 0)

        # This prevents the theme selection effect from overwriting the banner
        kwargs.setdefault("selection_effect", pygame_menu.widgets.NoneSelection())

        # Ensure the selection color doesn't show up on the ' ' character
        kwargs.setdefault("selection_color", (0, 0, 0, 0))

        # Set image as background
        kwargs["background_color"] = image

        # Call button - this will now "pop" our custom padding and selection_effect
        btn = self.button(" ", action, *args, **kwargs)

        return btn.resize(*image.get_size())

    def _normalize_button_action(
        self,
        action: pygame_menu.Menu | _events.MenuAction | Callable | int | None,
    ) -> pygame_menu.Menu | _events.MenuAction | Callable | int:
        """
        Normalize special button actions.
        """
        if action in (_events.PYGAME_QUIT, _events.PYGAME_WINDOWCLOSE):
            return _events.EXIT
        if action is None:
            return _events.NONE
        return action

    def _create_event_button(
        self,
        title: Any,
        button_id: str,
        action: _events.MenuAction | int,
        total_back: int,
    ) -> Button:
        """
        Create button from menu event.
        """
        if action == _events.BACK:
            return Button(title, button_id, self._menu.reset, total_back)

        if action == _events.CLOSE:
            return Button(title, button_id, self._menu._close)

        if action == _events.EXIT:
            return Button(title, button_id, self._menu._exit)

        if action == _events.NONE:
            return Button(title, button_id)

        if action == _events.RESET:
            return Button(title, button_id, self._menu.full_reset)

        raise ValueError(f"unsupported event action {action}")

    def _create_menu_button(
        self,
        title: Any,
        button_id: str,
        menu: pygame_menu.Menu,
    ) -> Button:
        """
        Create submenu button.
        """
        if menu == self._menu or menu.in_submenu(self._menu, recursive=True):
            raise ValueError(
                f'{menu.get_class_id()} title "{menu.get_title()}" is '
                f"already on submenu structure, recursive menus lead to "
                f"unexpected behaviours. For returning to previous menu "
                f"use pygame_menu.events.BACK event defining an optional "
                f"back_count number of menus to return from, default is 1"
            )

        widget = Button(title, button_id, self._menu._open, menu)
        widget.to_menu = True
        return widget

    def _create_button_from_action(
        self,
        title: Any,
        button_id: str,
        action: pygame_menu.Menu | _events.MenuAction | Callable | int | None,
        total_back: int,
        accept_kwargs: bool,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> Button:
        """
        Orchestrate button creation by normalizing and evaluating action types.
        """
        action = self._normalize_button_action(action)

        if isinstance(action, (pygame_menu.Menu, type(self._menu))):
            return self._create_menu_button(title, button_id, action)

        if action in (
            _events.BACK,
            _events.CLOSE,
            _events.EXIT,
            _events.NONE,
            _events.RESET,
        ):
            return self._create_event_button(
                title,
                button_id,
                action,
                total_back,
            )

        if callable(action):
            if accept_kwargs:
                return Button(title, button_id, action, *args, **kwargs)
            return Button(title, button_id, action, *args)

        raise ValueError(
            "action must be a Menu, a MenuAction (event), "
            "a function (callable), or None"
        )

    # noinspection PyProtectedMember
    def button(
        self,
        title: Any,
        action: pygame_menu.Menu | _events.MenuAction | Callable | int | None = None,
        *args,
        **kwargs,
    ) -> Button:
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
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``leading``                       (int) - Font leading for ``wordwrap``. If ``None`` retrieves from widget font
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``max_nlines``                    (int) - Number of maximum lines for ``wordwrap``. If ``None`` the number is dynamically computed. If exceeded, ``get_overflow_lines()`` will return the non-displayed lines
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
            - ``wordwrap``                      (bool) – Wraps button text if newline (\n) is found on text, or it exceeds the maximum width from its container. If ``False`` the manager splits the string and creates a list of widgets, else, the widget itself splits and updates the height

        .. note::

            All theme-related optional kwargs use the default Menu theme if not defined.

        .. note::

            Using ``action=None`` is the same as using ``action=pygame_menu.events.NONE``.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
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
        total_back = kwargs.pop("back_count", 1)
        assert isinstance(total_back, int) and 1 <= total_back

        # Get ID
        button_id = kwargs.pop("button_id", "")
        assert isinstance(button_id, str), "id must be a string"

        # Accept kwargs
        accept_kwargs = kwargs.pop("accept_kwargs", False)
        assert isinstance(accept_kwargs, bool)

        # Onselect callback
        onselect = kwargs.pop("onselect", None)

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        # Button underline
        underline = kwargs.pop("underline", False)
        underline_color = kwargs.pop("underline_color", attributes["font_color"])
        underline_offset = kwargs.pop("underline_offset", 1)
        underline_width = kwargs.pop("underline_width", 1)

        # Wordwrap
        wordwrap = kwargs.pop("wordwrap", False)
        assert isinstance(wordwrap, bool)
        leading = kwargs.pop("leading", None)
        assert isinstance(leading, (type(None), int))
        max_nlines = kwargs.pop("max_nlines", None)
        assert isinstance(max_nlines, (type(None), int))

        # Check kwargs validity if not accepting kwargs
        if not accept_kwargs:
            try:
                self._check_kwargs(kwargs)
            except ValueError:
                if self._menu._verbose:
                    warn(
                        "button cannot accept kwargs. If you want to use kwargs "
                        "options set accept_kwargs=True"
                    )
                raise

        widget = self._create_button_from_action(
            title=title,
            button_id=button_id,
            action=action,
            total_back=total_back,
            accept_kwargs=accept_kwargs,
            args=args,
            kwargs=kwargs,
        )

        # Configure and add the button
        self._configure_widget(widget=widget, **attributes)
        if underline:
            widget.add_underline(underline_color, underline_offset, underline_width)
        widget.set_selection_callback(onselect)
        widget._leading = leading  # Configure wordwrap
        widget._max_nlines = max_nlines
        widget._wordwrap = wordwrap
        self._append_widget(widget)

        # Add to submenu using normalized action
        if widget.to_menu:
            normalized_action = self._normalize_button_action(action)
            self._add_submenu(normalized_action, widget)  # type: ignore

        return widget

    def url(self, href: str, title: str = "", **kwargs: Any) -> Button:
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
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over. By default, is ``HAND``
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
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
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param href: Link to open
        :param title: Alternative title of the link
        :param kwargs: Optional keyword arguments
        :return: Widget object, or List of widgets if the text overflows
        :rtype: :py:class:`pygame_menu.widgets.Button`
        """
        # Validate link
        assert isinstance(href, str) and len(href) > 0
        assert re.match(_URL_REGEX, href) is not None, "invalid link format"

        # Configure kwargs consistently using setdefault
        url_color = self._theme.widget_url_color
        kwargs.setdefault("cursor", CURSOR_HAND)
        kwargs.setdefault("font_color", url_color)
        kwargs.setdefault("selection_color", url_color)
        kwargs.setdefault("selection_effect", pygame_menu.widgets.NoneSelection())
        kwargs.setdefault("underline", True)

        # Clear callback helper avoiding anonymous lambda
        def _open_url() -> None:
            webbrowser.open(href)

        # Return new button
        return self.button(title or href, _open_url, **kwargs)
