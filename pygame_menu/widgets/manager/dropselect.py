"""
pygame-menu
https://github.com/ppizarror/pygame-menu

DROP SELECT MANAGER
Base class for DropSelectManager.
"""

from __future__ import annotations

__all__ = ["DropSelectManager"]

from abc import ABC
from typing import TYPE_CHECKING, Any

from pygame_menu._types import (
    CallbackType,
    NumberInstance,
)
from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.dropselect import DropSelect

if TYPE_CHECKING:
    from collections.abc import Callable

    import pygame_menu
    from pygame_menu.widgets.core.widget import Widget


class DropSelectManager(AbstractWidgetManager, ABC):
    """
    DropSelect manager.
    """

    def dropselect(
        self,
        title: Any,
        items: list[tuple[Any, ...]] | list[str],
        default: int | None = None,
        dropselect_id: str = "",
        onchange: CallbackType = None,
        onreturn: CallbackType = None,
        onselect: Callable[[bool, Widget, pygame_menu.Menu], Any] | None = None,
        open_middle: bool = False,
        placeholder: str = "Select an option",
        placeholder_add_to_selection_box: bool = True,
        **kwargs,
    ) -> DropSelect:
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
            - ``selection_box_height``                  (int) – Number of the options which can be packed before showing scroll
            - ``selection_box_inflate``                 (tuple) – Selection box inflate on x-axis and y-axis (x, y) in px
            - ``selection_box_margin``                  (tuple, list) – Selection box on x-axis and y-axis (x, y) margin from title in px
            - ``selection_box_text_margin``             (int) – Left margin of the text inside the selection box in px
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
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Drop select title
        :param items: Item list of the drop select; format ``[('Item1', a, b, c...), ('Item2', d, e, f...)]``
        :param default: Index of default item to display. If ``None`` no item is selected
        :param dropselect_id: ID of the dropselect
        :param onchange: Callback when changing the drop select item
        :param onreturn: Callback when pressing return (apply) on the selected item
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
        selection_box_arrow_color = kwargs.pop(
            "selection_box_arrow_color", self._theme.widget_box_arrow_color
        )
        selection_box_arrow_margin = kwargs.pop(
            "selection_box_arrow_margin", self._theme.widget_box_arrow_margin
        )
        selection_box_bgcolor = kwargs.pop(
            "selection_box_bgcolor", self._theme.widget_box_background_color
        )
        selection_box_border_color = kwargs.pop(
            "selection_box_border_color", self._theme.widget_box_border_color
        )
        selection_box_border_width = kwargs.pop(
            "selection_box_border_width", self._theme.widget_box_border_width
        )
        selection_box_height = kwargs.pop("selection_box_height", 3)
        selection_box_inflate = kwargs.pop(
            "selection_box_inflate", self._theme.widget_border_inflate
        )
        selection_box_margin = kwargs.pop(
            "selection_box_margin", self._theme.widget_box_margin
        )
        selection_box_text_margin = kwargs.pop(
            "selection_box_text_margin", self._theme.widget_box_arrow_margin[0]
        )
        selection_box_width = kwargs.pop("selection_box_width", 0)
        selection_infinite = kwargs.pop("selection_infinite", False)
        selection_option_border_color = kwargs.pop(
            "selection_option_border_color", self._theme.scrollbar_color
        )
        selection_option_border_width = kwargs.pop(
            "selection_option_border_width", self._theme.widget_box_border_width
        )
        # selection_option_cursor = kwargs.pop('selection_option_cursor', None)
        selection_option_font = kwargs.pop("selection_option_font", None)
        selection_option_font_color = kwargs.pop(
            "selection_option_font_color", (0, 0, 0)
        )
        selection_option_font_size = kwargs.pop("selection_option_font_size", None)
        selection_option_padding = kwargs.pop("selection_option_padding", (2, 5))
        selection_option_selected_bgcolor = kwargs.pop(
            "selection_option_selected_bgcolor", (188, 227, 244)
        )
        selection_option_selected_font_color = kwargs.pop(
            "selection_option_selected_font_color", (0, 0, 0)
        )

        # Get selection box scrollbar properties
        scrollbar_color = kwargs.pop("scrollbar_color", self._theme.scrollbar_color)
        scrollbar_cursor = kwargs.pop("scrollbar_cursor", self._theme.scrollbar_cursor)
        scrollbar_shadow_color = kwargs.pop(
            "scrollbar_shadow_color", self._theme.scrollbar_shadow_color
        )
        scrollbar_shadow_offset = kwargs.pop(
            "scrollbar_shadow_offset", self._theme.scrollbar_shadow_offset
        )
        scrollbar_shadow_position = kwargs.pop(
            "scrollbar_shadow_position", self._theme.scrollbar_shadow_position
        )
        scrollbar_shadow = kwargs.pop("scrollbar_shadow", self._theme.scrollbar_shadow)
        scrollbar_slider_color = kwargs.pop(
            "scrollbar_slider_color", self._theme.scrollbar_slider_color
        )
        scrollbar_slider_hover_color = kwargs.pop(
            "scrollbar_slider_hover_color", self._theme.scrollbar_slider_hover_color
        )
        scrollbar_slider_pad = kwargs.pop(
            "scrollbar_slider_pad", self._theme.scrollbar_slider_pad
        )
        scrollbar_thick = kwargs.pop("scrollbar_thick", self._theme.scrollbar_thick)
        scrollbars = kwargs.pop("scrollbars", self._theme.scrollarea_position)

        # Convert to tuple if enabled
        if isinstance(selection_box_margin, NumberInstance):
            selection_box_margin = (selection_box_margin, selection_box_margin)

        widget = DropSelect(
            default=default,
            dropselect_id=dropselect_id,
            items=items,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            open_middle=open_middle,
            placeholder=placeholder,
            placeholder_add_to_selection_box=placeholder_add_to_selection_box,
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
            **kwargs,
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
