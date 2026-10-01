"""
pygame-menu
https://github.com/ppizarror/pygame-menu

COLOR INPUT
Color input class, Widget created in top of TextInput that provides a textbox
for entering and previewing colors in RGB and HEX format.
"""

from __future__ import annotations

__all__ = ["ColorInputManager"]

from abc import ABC
from typing import TYPE_CHECKING, Any

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.colorinput import (
    COLORINPUT_HEX_FORMAT_NONE,
    ColorInput,
    ColorInputColorType,
    ColorInputHexFormatType,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    import pygame_menu
    from pygame_menu._types import CallbackType, Tuple3IntType
    from pygame_menu.widgets.core.widget import Widget


class ColorInputManager(AbstractWidgetManager, ABC):
    """
    ColorInput manager.
    """

    def color_input(
        self,
        title: str | Any,
        color_type: ColorInputColorType,
        color_id: str = "",
        default: str | Tuple3IntType = "",
        hex_format: ColorInputHexFormatType = COLORINPUT_HEX_FORMAT_NONE,
        input_separator: str = ",",
        input_underline: str = "_",
        onchange: CallbackType = None,
        onreturn: CallbackType = None,
        onselect: Callable[[bool, Widget, pygame_menu.Menu], Any] | None = None,
        **kwargs,
    ) -> ColorInput:
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
            - ``dynamic_width``                 (bool) – If ``True`` the widget width changes if the pre-visualization color box is active or not
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
            - ``input_underline_vmargin``       (int) – Vertical margin of underline in px
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``maxwidth_dynamically_update``   (bool) - Dynamically update maxwidth depending on char size. ``True`` by default
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``previsualization_margin``       (int) – Pre-visualization left margin from text input in px. Default is ``0``
            - ``previsualization_width``        (int, float) – Pre-visualization width as a factor of the height. Default is ``3``
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

        :param title: Title of the color input
        :param color_type: Type of the color input
        :param color_id: ID of the color input
        :param default: Default value to display, if RGB type it must be a tuple ``(r, g, b)``, if HEX must be a string ``"#XXXXXX"``
        :param hex_format: Hex format string mode
        :param input_separator: Divisor between RGB channels, not valid in HEX format
        :param input_underline: Underline character
        :param onchange: Callback executed when changing the values of the color text
        :param onreturn: Callback executed when pressing return (apply) on the color input
        :param onselect: Callback executed when selecting the widget
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.ColorInput`
        """
        assert isinstance(default, (str, tuple))

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        dynamic_width = kwargs.pop("dynamic_width", True)
        input_underline_vmargin = kwargs.pop("input_underline_vmargin", 0)
        prev_margin = kwargs.pop("previsualization_margin", 10)
        prev_width = kwargs.pop("previsualization_width", 3)

        widget = ColorInput(
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
            **kwargs,
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        widget.set_default_value(default)

        return widget
