from __future__ import annotations

__all__ = ["TimerManager"]

from abc import ABC
from typing import TYPE_CHECKING

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.timer import Timer

if TYPE_CHECKING:
    import pygame_menu


class TimerManager(AbstractWidgetManager, ABC):
    """
    Timer manager.
    """

    def timer(
        self,
        title_format: str = "{0:02d}:{1:02d}",
        **kwargs,
    ) -> pygame_menu.widgets.Timer:
        """
        Adds a timer label to the Menu.

        kwargs (Optional)
            - ``align`` (str) – Widget alignment
            - ``font_color`` (tuple, list, str, int, pygame.Color) – Widget font color
            - ``font_size`` (int) – Font size of the widget
            - ``label_id`` (str) – Widget ID
            - ``margin`` (tuple, list) – Widget (left, bottom) margin in px
            - ``padding`` (int, float, tuple, list) – Widget padding according to CSS rules

        :param title_format: Format string, e.g. "{0:02d}:{1:02d}"
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Timer`
        """
        assert isinstance(title_format, str)

        label_id = kwargs.pop("label_id", "")
        attributes = self._filter_widget_attributes(kwargs)

        # Do not pass attributes directly to Timer().
        widget = Timer(
            title_format=title_format,
            label_id=label_id,
        )

        # Apply generic widget options through the widget manager.
        self._configure_widget(widget=widget, **attributes)

        # Attach the widget to the menu.
        self._append_widget(widget)

        # Register the title generator after the widget has a menu.
        widget.set_title_generator(widget._generate_title)

        return widget
