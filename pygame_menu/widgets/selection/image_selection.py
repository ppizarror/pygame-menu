"""
pygame-menu

IMAGE SELECTION
Widget selection image indicator.
"""

from __future__ import annotations

__all__ = ["ImageSelection"]

from typing import TYPE_CHECKING

from pygame_menu._types import NumberInstance, NumberType
from pygame_menu.baseimage import BaseImage
from pygame_menu.widgets.core import Selection

if TYPE_CHECKING:
    import pygame

    import pygame_menu


class ImageSelection(Selection):
    _image: BaseImage
    _margin: int
    _vertical_offset: int

    def __init__(
        self,
        image: BaseImage,
        margin: NumberType = 5,
        vertical_offset: NumberType = 0,
    ) -> None:

        assert isinstance(image, BaseImage)
        assert isinstance(margin, NumberInstance)
        assert margin >= 0

        super().__init__(
            margin_left=image.get_width() + int(margin),
            margin_right=0,
            margin_top=0,
            margin_bottom=0,
        )

        self._image = image.copy()
        self._margin = int(margin)
        self._vertical_offset = int(vertical_offset)

    def _repr_attrs(self) -> dict[str, object]:
        attrs = super()._repr_attrs()

        attrs.update(
            {
                "image_width": self._image.get_width(),
                "image_height": self._image.get_height(),
                "margin": self._margin,
                "vertical_offset": self._vertical_offset,
            }
        )

        return attrs

    def draw(
        self,
        surface: pygame.Surface,
        widget: pygame_menu.widgets.Widget,
    ) -> ImageSelection:

        rect = widget.get_rect()

        x = rect.left - self._image.get_width() - self._margin

        y = rect.centery - self._image.get_height() // 2 + self._vertical_offset

        self._image.draw(
            surface,
            position=(x, y),
        )

        return self
