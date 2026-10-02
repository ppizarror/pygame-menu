"""
pygame-menu
https://github.com/ppizarror/pygame-menu

SELECTOR MANAGER
Base class for SelectorManager.
"""

from __future__ import annotations

__all__ = ["SelectorManager"]

from abc import ABC
from typing import TYPE_CHECKING, Any

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.selector import (
    SELECTOR_STYLE_CLASSIC,
    Selector,
    SelectorStyleType,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    import pygame_menu
    from pygame_menu._types import CallbackType
    from pygame_menu.widgets.core.widget import Widget


class SelectorManager(AbstractWidgetManager, ABC):
    """
    Selector manager.
    """

    def selector(
        self,
        title: Any,
        items: list[tuple[Any, ...]] | list[str],
        default: int = 0,
        onchange: CallbackType = None,
        onreturn: CallbackType = None,
        onselect: Callable[[bool, Widget, pygame_menu.Menu], Any] | None = None,
        selector_id: str = "",
        style: SelectorStyleType = SELECTOR_STYLE_CLASSIC,
        **kwargs,
    ) -> Selector:
        """
        Add a selector to the Menu: several items and two functions that are
        executed when changing the selector (left/right) and pressing return
        (apply) on the selected item.

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
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
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
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the selector
        :param items: Item list of the selector; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :param default: Index of default item to display
        :param onchange: Callback executed when changing the selector
        :param onreturn: Callback executed when pressing return (apply)
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
        style_fancy_arrow_color = kwargs.pop(
            "style_fancy_arrow_color", self._theme.widget_box_arrow_color
        )
        style_fancy_arrow_margin = kwargs.pop(
            "style_fancy_arrow_margin", self._theme.widget_box_arrow_margin
        )
        style_fancy_bgcolor = kwargs.pop(
            "style_fancy_bgcolor", self._theme.widget_box_background_color
        )
        style_fancy_bordercolor = kwargs.pop(
            "style_fancy_bordercolor", self._theme.widget_box_border_color
        )
        style_fancy_borderwidth = kwargs.pop(
            "style_fancy_borderwidth", self._theme.widget_box_border_width
        )
        style_fancy_box_inflate = kwargs.pop(
            "style_fancy_box_inflate", self._theme.widget_box_inflate
        )
        style_fancy_box_margin = kwargs.pop(
            "style_fancy_box_margin", self._theme.widget_box_margin
        )

        widget = Selector(
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
            **kwargs,
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
