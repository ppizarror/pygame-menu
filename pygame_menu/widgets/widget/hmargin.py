"""
pygame-menu
https://github.com/ppizarror/pygame-menu

HORIZONTAL MARGIN
Horizontal box margin.
"""

from __future__ import annotations

__all__ = ["HMargin"]

from typing import TYPE_CHECKING, Any

from pygame_menu._types import NumberInstance, NumberType
from pygame_menu.widgets.widget.none import NoneWidget

if TYPE_CHECKING:
    import pygame


class HMargin(NoneWidget):
    """
    Horizontal margin widget.

    .. note::

        HMargin does not accept transformations.

    :param margin: Horizontal margin in px
    :param widget_id: ID of the widget
    """

    def __init__(self, margin: NumberType, widget_id: str = "") -> None:
        assert isinstance(margin, NumberInstance)
        assert margin > 0, (
            "zero margin is not valid, prefer adding a NoneWidget menu.add.none_widget()"
        )
        super().__init__(widget_id=widget_id)
        self._rect.width = int(margin)
        self._rect.height = 0

    def get_rect(self, *args: Any, **kwargs: Any) -> pygame.Rect:
        return self._rect.copy()
