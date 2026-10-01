"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TOGGLE SWITCH
Switch between several states.
"""

from __future__ import annotations

__all__ = ["ToggleSwitchManager"]

from abc import ABC
from typing import TYPE_CHECKING, Any

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.toggleswitch import ToggleSwitch

if TYPE_CHECKING:
    from collections.abc import Callable

    import pygame_menu
    from pygame_menu._types import CallbackType
    from pygame_menu.widgets.core.widget import Widget


class ToggleSwitchManager(AbstractWidgetManager, ABC):
    """
    ToggleSwitch manager.
    """

    def toggle_switch(
        self,
        title: Any,
        default: int | bool = 0,
        onchange: CallbackType = None,
        onselect: Callable[[bool, Widget, pygame_menu.Menu], Any] | None = None,
        toggleswitch_id: str = "",
        single_click: bool = True,
        state_text: tuple[str, ...] = ("Off", "On"),
        state_values: tuple[Any, ...] = (False, True),
        width: int = 150,
        **kwargs,
    ) -> ToggleSwitch:
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
            - ``infinite``                      (bool) – The state can rotate. ``False`` by default
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``single_click_dir``              (bool) - Direction of the change if only 1 click is pressed. ``True`` for left direction (default), ``False`` for right
            - ``slider_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider
            - ``slider_height_factor``          (int, float) - Height of the slider (factor of the switch height). ``1`` by default
            - ``slider_thickness``              (int) – Slider thickness in px. ``20`` px by default
            - ``slider_vmargin``                (int, float) - Vertical margin of the slider (factor of the switch height). ``0`` by default
            - ``state_color``                   (tuple) – 2-item color tuple for each state
            - ``state_text_font``               (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`, None) - Font of the state text. If ``None`` uses the widget font. ``None`` by default
            - ``state_text_font_color``         (tuple) – 2-item color tuple for each font state text color
            - ``state_text_font_size``          (str, None) – Font size of the state text. If ``None`` uses the widget font size
            - ``state_text_position``           (tuple) - Position of the state text respect to the switch rect. ``(0.5, 0.5)`` by default
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
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the toggle switch
        :param default: Default state index of the switch; it can be ``0 (False)`` or ``1 (True)``
        :param onchange: Callback executed when changing the state of the toggle switch
        :param onselect: Callback executed when selecting the widget
        :param toggleswitch_id: Widget ID
        :param single_click: Changes the state of the switch with 1 click instead of finding the closest position
        :param state_text: Text of each state
        :param state_values: Value of each state of the switch
        :param width: Width of the switch box in px
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.ToggleSwitch`
        """
        if isinstance(default, (int, bool)):
            assert 0 <= default <= 1, "default value can be 0 or 1"
        else:
            raise ValueError(
                f"invalid value type, default can be 0, False, 1, or True, but"
                f'received "{default}"'
            )

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)
        default_state_text_fcolor = (
            self._theme.widget_box_background_color,
            self._theme.widget_box_background_color,
        )

        infinite = kwargs.pop("infinite", False)
        slider_color = kwargs.pop(
            "slider_color", self._theme.widget_box_background_color
        )
        slider_thickness = kwargs.pop("slider_thickness", self._theme.scrollbar_thick)
        state_color = kwargs.pop("state_color", ((178, 178, 178), (117, 185, 54)))
        state_text_font_color = kwargs.pop(
            "state_text_font_color", default_state_text_fcolor
        )
        state_text_font_size = kwargs.pop("state_text_font_size", None)
        switch_border_color = kwargs.pop(
            "switch_border_color", self._theme.widget_box_border_color
        )
        switch_border_width = kwargs.pop(
            "switch_border_width", self._theme.widget_box_border_width
        )
        switch_height = kwargs.pop("switch_height", 1)
        switch_margin = kwargs.pop("switch_margin", self._theme.widget_box_margin)

        widget = ToggleSwitch(
            default_state=default,
            infinite=infinite,
            onchange=onchange,
            onselect=onselect,
            single_click=single_click,
            single_click_dir=kwargs.pop("single_click_dir", True),
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
            **kwargs,
        )
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
