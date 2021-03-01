# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

IMAGE
Image widget class, adds a simple image.

NOTE: pygame-menu v3 will not provide new widgets or functionalities, consider
upgrading to the latest version.

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

from pygame_menu.baseimage import BaseImage
from pygame_menu.widgets.core import Widget


# noinspection PyMissingOrEmptyDocstring
class Image(Widget):
    """
    Image widget.

    :param image_path: Path of the image or BaseImage object. If BaseImage object is provided drawing mode is not considered. It can be a string or :py:class:`pathlib.Path` on ``Python 3+``
    :type image_path: str, :py:class:`pathlib.Path`, BaseImage
    :param image_id: Image ID
    :type image_id: str
    :param angle: Angle of the image in degrees (clockwise)
    :type angle: int, float
    :param scale: Scale of the image *(x,y)*
    :type scale: tuple, list
    :param scale_smooth: Scale is smoothed
    :type scale_smooth: bool
    """

    def __init__(self,
                 image_path,
                 image_id='',
                 angle=0,
                 scale=(1, 1),
                 scale_smooth=True
                 ):
        assert isinstance(angle, (int, float))
        assert isinstance(scale, (tuple, list))
        assert isinstance(scale_smooth, bool)
        super(Image, self).__init__(widget_id=image_id)

        if isinstance(image_path, BaseImage):
            self._image = image_path
        else:
            self._image = BaseImage(image_path)
            self._image.rotate(angle)
            self._image.scale(scale[0], scale[1], smooth=scale_smooth)

        self.selection_effect_enabled = False

    def get_image(self):
        """
        Gets the BaseImage object from widget.

        :return: Widget image
        :rtype: BaseImage
        """
        return self._image

    def set_image(self, image):
        """
        Set the BaseImage object from widget.

        :param image: BaseImage object
        :type image: BaseImage
        :return: None
        """
        self._image = image
        self._surface = None
        self._render()

    def _apply_font(self):
        pass

    def rotate(self, angle):
        self._image.rotate(angle)
        self._surface = None

    def flip(self, x, y):
        if x or y:
            self._image.flip(x, y)
            self._surface = None

    def scale(self, width, height, smooth=False):
        self._image.scale(width, height, smooth)
        self._surface = None

    def resize(self, width, height, smooth=False):
        self._image.resize(width, height, smooth)
        self._surface = None

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface):
        self._render()
        surface.blit(self._surface, self._rect.topleft)

    def _render(self):
        if self._surface is not None:
            return True
        self._surface = self._image.get_surface()
        self._rect.width, self._rect.height = self._surface.get_size()
        if not self._render_hash_changed(self.visible):
            return True
        self._menu_surface_needs_update = True  # Force menu update

    # noinspection PyMissingOrEmptyDocstring
    def update(self, events):
        return False
