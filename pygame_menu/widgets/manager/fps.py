from __future__ import annotations

__all__ = ["FPSManager"]

from abc import ABC
from typing import TYPE_CHECKING

import pygame

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.fps import FPS

if TYPE_CHECKING:
    import pygame_menu


class FPSManager(AbstractWidgetManager, ABC):
    """
    FPS manager.
    """

    def fps(
        self,
        clock: pygame.time.Clock,
        title_format: str = "FPS: {0:.0f}",
        **kwargs,
    ) -> pygame_menu.widgets.FPS:
        """
        Adds an FPS label to the Menu.

        kwargs (Optional)
            - ``align`` (str) – Widget alignment
            - ``font_color`` (tuple, list, str, int, pygame.Color) – Widget font color
            - ``font_size`` (int) – Font size of the widget
            - ``label_id`` (str) – Widget ID
            - ``margin`` (tuple, list) – Widget (left, bottom) margin in px
            - ``padding`` (int, float, tuple, list) – Widget padding according to CSS rules

        :param clock: Pygame clock object
        :param title_format: Format string, e.g. "FPS: {0:.0f}"
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.FPS`
        """
        assert isinstance(clock, pygame.time.Clock)
        assert isinstance(title_format, str)

        label_id = kwargs.pop("label_id", "")
        attributes = self._filter_widget_attributes(kwargs)

        widget = FPS(
            clock=clock,
            title_format=title_format,
            label_id=label_id,
        )
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        return widget
