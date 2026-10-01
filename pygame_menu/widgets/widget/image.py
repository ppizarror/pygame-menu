"""
pygame-menu
https://github.com/ppizarror/pygame-menu

IMAGE
Image widget class, adds a simple image.
"""

from __future__ import annotations

__all__ = ["Image"]

from io import BytesIO
from pathlib import Path
from typing import Any

import pygame

from pygame_menu._types import (
    CallbackType,
    EventVectorType,
    NumberInstance,
    NumberType,
    Tuple2NumberType,
)
from pygame_menu.baseimage import BaseImage
from pygame_menu.utils import assert_vector
from pygame_menu.widgets.core.widget import Widget


class Image(Widget):
    """
    Image widget.

    .. note::

        Image accepts all transformations.

    :param image_path: Path of the image, BytesIO object, a pygame.Surface, or :py:class:`pygame_menu.baseimage.BaseImage` object. If :py:class:`pygame_menu.baseimage.BaseImage` object is provided drawing mode is not considered
    :param image_id: Image ID
    :param angle: Angle of the image in degrees (clockwise)
    :param onselect: Function when selecting the widget
    :param scale: Scaling factors for the x-axis and y-axis, such as (0.5, 0.5)
    :param scale_smooth: Scale is smoothed
    """

    _image: BaseImage
    _flip: tuple[bool, bool]

    def __init__(
        self,
        image_path: str | Path | BaseImage | BytesIO | pygame.Surface,
        angle: NumberType = 0,
        image_id: str = "",
        onselect: CallbackType = None,
        scale: Tuple2NumberType = (1, 1),
        scale_smooth: bool = True,
    ) -> None:
        assert isinstance(image_path, (str, Path, BaseImage, BytesIO, pygame.Surface))
        assert isinstance(image_id, str)
        assert isinstance(angle, NumberInstance)
        assert isinstance(scale_smooth, bool)
        assert_vector(scale, 2)

        super().__init__(onselect=onselect, widget_id=image_id)

        if isinstance(image_path, BaseImage):
            self._image = image_path
        else:
            self._image = BaseImage(image_path)
            self._image.rotate(angle)
            self._image.scale(scale[0], scale[1], smooth=scale_smooth)

    def set_title(self, title: str, *args: Any) -> Image:
        return self

    def get_image(self) -> BaseImage:
        """
        Gets the :py:class:`pygame_menu.baseimage.BaseImage` object from widget.

        :return: Widget image
        """
        return self._image

    def get_angle(self) -> NumberType:
        """
        Return the image angle.

        :return: Angle in degrees
        """
        return self._image.get_angle()

    def set_image(self, image: BaseImage) -> Image:
        """
        Set the :py:class:`pygame_menu.baseimage.BaseImage` object from widget.

        :param image: Image object
        :return: Self reference
        """
        assert isinstance(image, BaseImage)
        self._image = image
        self._flip = (False, False)
        return self._invalidate(render=True)

    def _apply_font(self) -> None:
        pass

    def _invalidate(self, render: bool = True) -> Image:
        """
        Invalidates the cached surface and updates its dimensions.
        """
        self._surface = None

        if render:
            self._render()
        else:
            self._rect.size = self._image.get_size()

        return self

    def scale(
        self,
        width: NumberType,
        height: NumberType,
        smooth: bool = False,
        render: bool = True,
    ) -> Image:
        assert isinstance(smooth, bool)
        assert isinstance(render, bool)
        self._image.scale(width, height, smooth)
        return self._invalidate(render)

    def resize(
        self,
        width: NumberType,
        height: NumberType,
        smooth: bool = False,
        render: bool = True,
    ) -> Image:
        assert isinstance(smooth, bool)
        assert isinstance(render, bool)
        self._image.resize(width, height, smooth)
        return self._invalidate(render)

    def set_max_width(
        self,
        width: NumberType | None,
        scale_height: bool = False,
        smooth: bool = True,
        render: bool = True,
    ) -> Image:
        assert isinstance(scale_height, bool)
        assert isinstance(smooth, bool)
        assert isinstance(render, bool)

        if width is not None and self._image.get_width() > width:
            sx = width / self._image.get_width()
            height = self._image.get_height()
            if scale_height:
                height *= sx
            self._image.resize(width, height, smooth)
            return self._invalidate(render)
        return self

    def set_max_height(
        self,
        height: NumberType | None,
        scale_width: bool = False,
        smooth: bool = True,
        render: bool = True,
    ) -> Image:
        assert isinstance(scale_width, bool)
        assert isinstance(smooth, bool)
        assert isinstance(render, bool)

        if height is not None and self._image.get_height() > height:
            sy = height / self._image.get_height()
            width = self._image.get_width()
            if scale_width:
                width *= sy
            self._image.resize(width, height, smooth)
            return self._invalidate(render)
        return self

    def rotate(self, angle: NumberType, render: bool = True) -> Image:
        assert isinstance(render, bool)
        self._image.rotate(angle)
        return self._invalidate(render)

    def flip(self, x: bool, y: bool, render: bool = True) -> Image:
        assert isinstance(x, bool)
        assert isinstance(y, bool)
        assert isinstance(render, bool)

        old_x, old_y = self._flip
        flip_x = x != old_x
        flip_y = y != old_y

        if flip_x or flip_y:
            self._image.flip(flip_x, flip_y)
            self._flip = (x, y)
            return self._invalidate(render)

        return self

    def _draw(self, surface: pygame.Surface) -> None:
        if self._surface is None:
            self._render()

        if self._surface is not None:
            surface.blit(self._surface, self._rect.topleft)

    def _render(self) -> bool | None:
        if self._surface is not None:
            return True
        self._surface = self._image.get_surface(new=False)
        self._rect.width, self._rect.height = self._surface.get_size()
        if not self._render_hash_changed(self._visible):
            return True
        self.force_menu_surface_update()
        return None

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)
        for event in events:
            if self._check_mouseover(event):
                break
        return False
