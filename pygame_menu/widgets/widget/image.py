# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

IMAGE
Image widget class, adds a simple image.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

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

from pygame_menu.baseimage import BaseImage
from pygame_menu.widgets.core import Widget


class Image(Widget):
    """
    Image widget.

    :param image_path: Path of the image
    :type image_path: str
    :param image_id: Image ID
    :type image_id: str
    :param angle: Angle of the image in degrees (clockwise)
    :type angle: int, float
    :param scale: Scale of the image (x,y), float or int
    :type scale: tuple, list
    :param scale_smooth: Scale is smoothed
    :type scale_smooth: bool
    """

    def __init__(self, image_path, image_id='', angle=0, scale=(1, 1), scale_smooth=True):
        assert isinstance(image_path, str)
        assert isinstance(image_id, str)
        assert isinstance(angle, (int, float))
        assert isinstance(scale, (tuple, list))
        assert isinstance(scale_smooth, bool)
        super(Image, self).__init__(widget_id=image_id)

        self._image = BaseImage(image_path)
        self._image.rotate(angle)
        self._image.scale(scale[0], scale[1], smooth=scale_smooth)
        self.selection_effect_enabled = False

    def _apply_font(self):
        pass

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface):
        self._render()
        surface.blit(self._surface, self._rect.topleft)

    def _render(self):
        if self._surface is not None:
            return
        self._surface = self._image.get_surface()
        self._rect.width, self._rect.height = self._surface.get_size()

    # noinspection PyMissingOrEmptyDocstring
    def update(self, events):
        return False
