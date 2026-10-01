"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERTICAL MARGIN
Vertical box margin.
"""

from __future__ import annotations

__all__ = ["VMargin"]

from typing import TYPE_CHECKING, Any

from pygame_menu._types import NumberInstance, NumberType
from pygame_menu.widgets.widget.none import NoneWidget

if TYPE_CHECKING:
    import pygame


class VMargin(NoneWidget):
    """
    Vertical margin widget. VMargin only accepts margin, not padding.

    .. note::

        VMargin does not accept transformations.

    :param margin: Vertical margin in px
    :param widget_id: ID of the widget
    """

    def __init__(self, margin: NumberType, widget_id: str = "") -> None:
        assert isinstance(margin, NumberInstance)
        assert margin > 0, "negative or zero margin is not valid"
        super().__init__(widget_id=widget_id)
        self._rect.width = 0
        self._rect.height = int(margin)

    def get_rect(self, *args: Any, **kwargs: Any) -> pygame.Rect:
        return self._rect.copy()
