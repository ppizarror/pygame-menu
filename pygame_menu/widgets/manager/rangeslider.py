"""
pygame-menu
https://github.com/ppizarror/pygame-menu

RANGE SLIDER
Slider bar between one/two numeric ranges.
"""

from __future__ import annotations

__all__ = ["RangeSliderManager"]

from abc import ABC
from typing import TYPE_CHECKING, Any

from pygame_menu._types import (
    CallbackType,
    NumberInstance,
    NumberType,
)
from pygame_menu.utils import assert_vector
from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.rangeslider import (
    RangeSlider,
    RangeSliderRangeValueType,
    RangeSliderValueFormatType,
    RangeSliderValueType,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    import pygame_menu
    from pygame_menu.widgets.core.widget import Widget


class RangeSliderManager(AbstractWidgetManager, ABC):
    """
    RangeSlider manager.
    """

    def range_slider(
        self,
        title: str,
        default: RangeSliderValueType,
        range_values: RangeSliderRangeValueType,
        increment: NumberType | None = None,
        onchange: CallbackType = None,
        onreturn: CallbackType = None,
        onselect: Callable[[bool, Widget, pygame_menu.Menu], Any] | None = None,
        rangeslider_id: str = "",
        value_format: RangeSliderValueFormatType = lambda x: str(round(x, 3)),
        width: int = 150,
        **kwargs,
    ) -> RangeSlider:
        """
        Add a range slider to the Menu: Offers 1 or 2 sliders for defining a unique
        value or a range of numeric ones.

        If the state of the widget changes the ``onchange`` callback is called. The
        state can change by pressing LEFT/RIGHT, or by mouse/touch events.

        .. code-block:: python

            onchange(range_value, **kwargs)

        If pressing return (apply) on the widget:

        .. code-block:: python

            onreturn(range_value, **kwargs)

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
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``range_box_color_readonly``      (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the range box if widget in readonly state
            - ``range_box_color``               (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the range box between the sliders
            - ``range_box_enabled``             (bool) - Enables a range box between two sliders
            - ``range_box_height_factor``       (int, float) - Height of the range box (factor of the range title height)
            - ``range_box_single_slider``       (bool) - Enables range box if there's only 1 slider instead of 2
            - ``range_line_color``              (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the range line
            - ``range_line_height``             (int) - Height of the range line in px
            - ``range_margin``                  (tuple, list) - Range margin on x-axis and y-axis (x, y) from title in px
            - ``range_text_value_color``        (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the range values text
            - ``range_text_value_enabled``      (bool) - Enables the range values text
            - ``range_text_value_font_height``  (int, float) - Height factor of the range value font (factor of the range title height)
            - ``range_text_value_font``         (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) - Font of the ranges value. If ``None`` the same font as the widget is used
            - ``range_text_value_margin_f``     (int, float) - Margin of the range text values (factor of the range title height)
            - ``range_text_value_position``     (str) - Position of the range text values, can be NORTH or SOUTH. See :py:mod:`pygame_menu.locals`
            - ``range_text_value_tick_color``   (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the range text value tick
            - ``range_text_value_tick_enabled`` (bool) - Range text value tick enabled
            - ``range_text_value_tick_hfactor`` (bool) Height factor of the range text value tick (factor of the range title height)
            - ``range_text_value_tick_number``  (int) - Number of range value text, the values are placed uniformly distributed
            - ``range_text_value_tick_thick``   (int) - Thickness of the range text value tick in px
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``repeat_keys``                   (bool) - Enable key repeat. ``True`` by default
            - ``repeat_keys_initial_ms``        (int) - Time in milliseconds before keys are repeated when held in milliseconds. ``400`` by default
            - ``repeat_keys_interval_ms``       (int) - Interval between key press repetition when held in milliseconds. ``50`` by default
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``slider_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) - Slider color
            - ``slider_height_factor``          (int, float) - Height of the slider (factor of the range title height)
            - ``slider_sel_highlight_color``    (tuple, list, str, int, :py:class:`pygame.Color`) - Color of the selected slider highlight box effect
            - ``slider_sel_highlight_enabled``  (bool) - Selected slider is highlighted
            - ``slider_sel_highlight_thick``    (int) - Thickness of the selected slider highlight
            - ``slider_selected_color``         (tuple, list, str, int, :py:class:`pygame.Color`) - Selected slider color
            - ``slider_text_value_bgcolor``     (tuple, list, str, int, :py:class:`pygame.Color`) - Background color of the value text on each slider
            - ``slider_text_value_color``       (tuple, list, str, int, :py:class:`pygame.Color`) - Color of value text on each slider
            - ``slider_text_value_enabled``     (bool) - Enables a value text on each slider
            - ``slider_text_value_font_height`` (int, float) - Height factor of the slider font (factor of the range title height)
            - ``slider_text_value_font``        (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) - Font of the slider value. If ``None`` the same font as the widget is used
            - ``slider_text_value_margin_f``    (int, float) - Margin of the slider text values (factor of the range title height)
            - ``slider_text_value_padding``     (int, float, tuple, list) – Padding of the slider text values
            - ``slider_text_value_position``    (str) - Position of the slider text values, can be NORTH or SOUTH. See :py:mod:`pygame_menu.locals`
            - ``slider_text_value_triangle``    (bool) - Draws a triangle between slider text value and slider
            - ``slider_thickness``              (int) - Slider thickness in px
            - ``slider_vmargin``                (int, float) - Vertical margin of the slider (factor of the range title height)
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

        :param title: Title of the range slider
        :param default: Default range value, can accept a number or a tuple/list of 2 elements (min, max). If a single number is provided the rangeslider only accepts 1 value, if 2 are provided, the range is enabled (2 values)
        :param range_values: Tuple/list of 2 elements of min/max values of the range slider. Also range can accept a list of numbers, in which case the values of the range slider will be discrete. List must be sorted
        :param increment: Increment of the value if using left/right keys; used only if the range values are not discrete
        :param onchange: Callback executed when changing the value of the range slider
        :param onreturn: Callback executed when pressing return (apply) on the range slider
        :param onselect: Callback executed when selecting the widget
        :param rangeslider_id: ID of the range slider
        :param value_format: Function that format the value and returns a string that is used in the range and slider text
        :param width: Width of the range in px
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.RangeSlider`
        """
        assert_vector(range_values, 0)
        if len(range_values) == 2:
            assert isinstance(increment, NumberInstance), (
                "increment must be defined if the range values are not discrete"
            )
        else:
            if increment is None:
                increment = 1

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        range_margin = kwargs.pop("range_margin", self._theme.widget_box_margin)
        range_line_color = kwargs.pop("range_line_color", self._theme.widget_font_color)
        range_text_value_color = kwargs.pop(
            "range_text_value_color", self._theme.widget_font_color
        )
        range_text_value_font_height = kwargs.pop("range_text_value_font_height", 0.6)
        range_text_value_tick_hfactor = kwargs.pop("range_text_value_tick_hfactor", 0.5)
        slider_text_value_font_height = kwargs.pop("slider_text_value_font_height", 0.6)

        widget = RangeSlider(
            title=title,
            rangeslider_id=rangeslider_id,
            default_value=default,
            range_values=range_values,
            range_width=width,
            increment=increment,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            range_line_color=range_line_color,
            range_margin=range_margin,
            range_text_value_color=range_text_value_color,
            range_text_value_font_height=range_text_value_font_height,
            range_text_value_tick_hfactor=range_text_value_tick_hfactor,
            slider_text_value_font_height=slider_text_value_font_height,
            value_format=value_format,
            **kwargs,
        )
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
