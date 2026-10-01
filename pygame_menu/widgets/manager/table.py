"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TABLE
The table widget is a Frame which packs widgets in a structured way.
"""

from __future__ import annotations

__all__ = ["TableManager"]

from abc import ABC
from typing import Any

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.table import Table


class TableManager(AbstractWidgetManager, ABC):
    """
    Table manager.
    """

    def table(self, table_id: str = "", **kwargs: Any) -> Table:
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
            - ``max_height``                    (int) – Max height in px. If lower than the frame height a scrollbar will appear on vertical axis. ``None`` by default (same height)
            - ``max_width``                     (int) – Max width in px. If lower than the frame width a scrollbar will appear on horizontal axis. ``None`` by default (same width)
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param table_id: ID of the table
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Table`
        """
        attributes = self._filter_widget_attributes(kwargs)

        widget = Table(table_id=table_id)

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        self._check_kwargs(kwargs)

        return widget
