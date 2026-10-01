"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEXT INPUT
Text input class, this widget lets user write text.
"""

from __future__ import annotations

__all__ = ["TextInputManager"]

from abc import ABC
from typing import TYPE_CHECKING, Any

from pygame_menu._types import (
    CallbackType,
    NumberInstance,
    Tuple2IntType,
)
from pygame_menu.locals import INPUT_TEXT
from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.textinput import TextInput

if TYPE_CHECKING:
    from collections.abc import Callable

    import pygame_menu
    from pygame_menu.widgets.core.widget import Widget


class TextInputManager(AbstractWidgetManager, ABC):
    """
    TextInput manager.
    """

    def text_input(
        self,
        title: Any,
        default: str | int | float = "",
        copy_paste_enable: bool = True,
        cursor_selection_enable: bool = True,
        cursor_size: Tuple2IntType | None = None,
        input_type: str = INPUT_TEXT,
        input_underline: str = "",
        input_underline_len: int = 0,
        maxchar: int = 0,
        maxwidth: int = 0,
        onchange: CallbackType = None,
        onreturn: CallbackType = None,
        onselect: Callable[[bool, Widget, pygame_menu.Menu], Any] | None = None,
        password: bool = False,
        textinput_id: str = "",
        valid_chars: list[str] | None = None,
        **kwargs,
    ) -> TextInput:
        """
        Add a text input to the Menu: free text area and two functions that
        execute when changing the text and pressing return (apply) on the element.

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
            - ``history``                       (int) - Maximum number of editions stored. If ``0`` the feature is disabled. ``50`` by default
            - ``input_underline_vmargin``       (int) – Vertical margin of underline in px
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``maxwidth_dynamically_update``   (bool) - Dynamically update maxwidth depending on char size. ``True`` by default
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``password_char``                 (str) - Character used by password type. ``"*"`` by default
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``repeat_keys``                   (bool) - Enable key repeat. ``True`` by default
            - ``repeat_keys_initial_ms``        (int, float) - Time in milliseconds before keys are repeated when held in milliseconds. ``400`` by default
            - ``repeat_keys_interval_ms``       (int, float) - Interval between key press repetition when held in milliseconds. ``50`` by default
            - ``repeat_mouse_interval_ms``      (int, float) - Interval between mouse events when held in milliseconds. ``400`` by default
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``tab_size``                      (int) – Width of a tab character
            - ``text_ellipsis``                 (str) - Ellipsis text when overflow occurs (input length exceeds maxwidth). ``"..."`` by default

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the text input
        :param default: Default value to display
        :param copy_paste_enable: Enable text copy, paste and cut
        :param cursor_selection_enable: Enable text selection on input
        :param cursor_size: Size of the cursor (width, height) in px. If ``None`` uses the default sizing
        :param input_type: Data type of the input. See :py:mod:`pygame_menu.locals`
        :param input_underline: Underline character
        :param input_underline_len: Total of characters to be drawn under the input. If ``0`` this number is computed automatically to fit the font
        :param maxchar: Maximum length of string, if 0 there's no limit
        :param maxwidth: Maximum size of the text widget (in number of chars), if ``0`` there's no limit
        :param onchange: Callback executed when changing the text input
        :param onreturn: Callback executed when pressing return (apply) on the text input
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
        input_underline_vmargin = kwargs.pop("input_underline_vmargin", 0)

        # If password is active no default value should exist
        if password and default != "":
            raise ValueError("default value must be empty if the input is a password")

        widget = TextInput(
            copy_paste_enable=copy_paste_enable,
            cursor_color=self._theme.cursor_color,
            cursor_selection_color=self._theme.cursor_selection_color,
            cursor_selection_enable=cursor_selection_enable,
            cursor_size=cursor_size,
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
            **kwargs,
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        widget.set_default_value(default)

        return widget
