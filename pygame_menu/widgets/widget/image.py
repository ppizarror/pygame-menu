"""
pygame-menu
https://github.com/ppizarror/pygame-menu

IMAGE
Image widget class, adds a simple image.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

from pathlib import Path

import pygame
from pygame_menu.baseimage import BaseImage
from pygame_menu.widgets.core import Widget
from pygame_menu.custom_types import Union, List, NumberType, CallbackType, Tuple2NumberType, Tuple, Optional
from pygame_menu.utils import assert_vector2


# noinspection PyMissingOrEmptyDocstring
class Image(Widget):
    """
    Image widget.

    .. note::

        This class redefines all widget transformations.

    :param image_path: Path of the image or :py:class:`pygame_menu.baseimage.BaseImage` object. If :py:class:`pygame_menu.baseimage.BaseImage` object is provided drawing mode is not considered
    :param image_id: Image ID
    :param angle: Angle of the image in degrees (clockwise)
    :param onselect: Function when selecting the widget
    :param scale: Scale of the image *(x, y)*
    :param scale_smooth: Scale is smoothed
    """
    _image: 'BaseImage'

    def __init__(self,
                 image_path: Union[str, BaseImage, Path],
                 image_id: str = '',
                 angle: NumberType = 0,
                 onselect: CallbackType = None,
                 scale: Tuple2NumberType = (1, 1),
                 scale_smooth: bool = True
                 ) -> None:
        assert isinstance(image_path, (str, Path, BaseImage))
        assert isinstance(image_id, str)
        assert isinstance(angle, (int, float))
        assert isinstance(scale_smooth, bool)
        assert_vector2(scale)

        super(Image, self).__init__(
            onselect=onselect,
            widget_id=image_id
        )

        if isinstance(image_path, BaseImage):
            self._image = image_path
        else:
            self._image = BaseImage(image_path)
            self._image.rotate(angle)
            self._image.scale(scale[0], scale[1], smooth=scale_smooth)

    def set_title(self, title: str) -> None:
        pass

    def get_image(self) -> 'BaseImage':
        """
        Gets the :py:class:`pygame_menu.baseimage.BaseImage` object from widget.

        :return: Widget image
        """
        return self._image

    def set_image(self, image: 'BaseImage') -> None:
        """
        Set the :py:class:`pygame_menu.baseimage.BaseImage` object from widget.

        :param image: Image object
        :return: None
        """
        self._image = image
        self._surface = None
        self._render()

    def _apply_font(self) -> None:
        pass

    def rotate(self, angle: NumberType) -> None:
        self._image.rotate(angle)
        self._surface = None

    def flip(self, x: bool, y: bool) -> None:
        if x or y:
            self._image.flip(x, y)
            self._surface = None

    def scale(self, width: NumberType, height: NumberType, smooth: bool = False) -> None:
        self._image.scale(width, height, smooth)
        self._surface = None

    def resize(self, width: NumberType, height: NumberType, smooth: bool = False) -> None:
        self._image.resize(width, height, smooth)
        self._surface = None

    def draw(self, surface: 'pygame.Surface') -> None:
        self._render()
        surface.blit(self._surface, self._rect.topleft)
        self.apply_draw_callbacks()

    def _render(self) -> Optional[bool]:
        if self._surface is not None:
            return True
        self._surface = self._image.get_surface()
        self._rect.width, self._rect.height = self._surface.get_size()
        if not self._render_hash_changed(self.visible):
            return True
        self._menu_surface_needs_update = True  # Force Menu update

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        return False
