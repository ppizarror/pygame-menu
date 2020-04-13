# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BASEIMAGE
Provides a class to perform basic image loading an manipulation with pygame.

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

import os.path as _path

import pygame as _pygame

# https://www.pygame.org/docs/ref/image.html
_VALID_IMAGE_FORMATS = ['.jpg', '.png', '.gif', '.bmp', '.pcx', '.tga', '.tif', '.lbm',
                        '.pbm', '.pgm', '.ppm', '.xpm']

# Available images
__actualpath = str(_path.abspath(_path.dirname(__file__))).replace('\\', '/')
__fontdir = '{0}/resources/images/{1}'

IMAGE_CARBON_FIBER = __fontdir.format(__actualpath, 'carbon_fiber.png')
IMAGE_GRAY_LINES = __fontdir.format(__actualpath, 'gray_lines.png')
IMAGE_METAL = __fontdir.format(__actualpath, 'metal.png')
IMAGE_PYGAME_MENU = __fontdir.format(__actualpath, 'pygame_menu.png')


class BaseImage(object):
    """
    Object that loads an image, stores as a surface, transform it and
    let write the image to an surface.

    :param image_path: Path of the image to be loaded
    :type image_path: basestring
    """

    def __init__(self, image_path):
        assert isinstance(image_path, str)
        _, file_extension = _path.splitext(image_path)
        file_extension = file_extension.lower()

        assert file_extension in _VALID_IMAGE_FORMATS, \
            'file extension {0} not valid, please use: {1}'.format(file_extension, ','.join(_VALID_IMAGE_FORMATS))
        assert _path.isfile(image_path), 'file {0} does not exist or could not be found, please ' \
                                         'check if the path of the image is valid'.format(image_path)

        self._filepath = image_path
        self._filename = _path.splitext(_path.basename(image_path))[0]
        self._extension = file_extension

        # Load the image and store as a surface
        self._surface = _pygame.image.load(image_path)  # type: _pygame.SurfaceType
        self._original_surface = self._surface.copy()

    def get_size(self):
        """
        Return the size in pixels of the image.

        :return: (width,height)
        :rtype: tuple
        """
        return self._surface.get_width(), self._surface.get_height()

    def get_namefile(self):
        """
        :return: Return the name of the image file
        :rtype: basestring
        """
        return self._filename

    def get_extension(self):
        """
        :return: Return the extension of the image file
        :rtype: basestring
        """
        return self._extension

    def equals(self, image):
        """
        Returns true if the image is the same as the object

        :param image: Image object
        :type image: BaseImage
        :return: True if the image is the same (note, the surface)
        :rtype: bool
        """
        assert isinstance(image, BaseImage)
        im1 = _pygame.image.tostring(self._surface, 'RGBA')
        im2 = _pygame.image.tostring(image._surface, 'RGBA')
        return im1 == im2

    def restore(self):
        """
        Restore image to the original surface.

        :return: None
        """
        self._surface = self._original_surface.copy()

    def checkpoint(self):
        """
        Updates the original surface to the current surface.

        :return: None
        """
        self._original_surface = self._surface.copy()

    def flip(self, x, y):
        """
        This can flip the image either vertically, horizontally, or both.
        Flipping a image is non-destructive and does not change the dimensions.

        :param x: Flip in x axis
        :type x: bool
        :param y: Flip on y axis
        :type y: bool
        :return: None
        """
        assert isinstance(x, bool)
        assert isinstance(y, bool)
        assert not (x and y), 'at least one axis should be True'
        self._surface = _pygame.transform.flip(self._surface, x, y)

    def scale(self, width, height, smooth=False):
        """
        Scale the image to a desired width and height factor.

        :param width: Scale factor of the width
        :type width: int, float
        :param height: Scale factor of the height
        :type height: int, float
        :param smooth: Smooth scalling
        :type smooth: bool
        :return: None
        """
        assert isinstance(width, (int, float))
        assert isinstance(height, (int, float))
        assert isinstance(smooth, bool)
        assert width > 0 and height > 0, 'width and height must be greater than zero'
        w, h = self.get_size()
        if not smooth:
            self._surface = _pygame.transform.scale(self._surface, (int(w * width), int(h * height)))
        else:
            self._surface = _pygame.transform.smoothscale(self._surface, (int(w * width), int(h * height)))

    def scale2x(self):
        """
        This will return a new image that is double the size of the original.
        It uses the AdvanceMAME Scale2X algorithm which does a 'jaggie-less'
        scale of bitmap graphics.

        This really only has an effect on simple images with solid colors.
        On photographic and antialiased images it will look like a regular unfiltered scale.

        :return: None
        """
        self._surface = _pygame.transform.scale2x(self._surface)

    def resize(self, width, height, smooth=False):
        """
        Set the image size to another size.
        This is a fast scale operation.

        :param width: New width of the image
        :type width: int, float
        :param height: New height of the image
        :type height: int, float
        :param smooth: Smooth scalling
        :type smooth: bool
        :return: None
        """
        assert isinstance(width, (int, float))
        assert isinstance(height, (int, float))
        assert width > 0 and height > 0, 'width and height must be greater than zero'
        w, h = self.get_size()
        if w == width and h == height:
            return
        self.scale(width=float(width) / w, height=float(height) / h, smooth=smooth)

    def get_rect(self):
        """
        Return the rect of the image.

        :return: Pygame rect object
        :rtype: pygame.rect.RectType
        """
        return self._surface.get_rect()

    def rotate(self, angle):
        """
        Unfiltered counterclockwise rotation. The angle argument represents degrees
        and can be any floating point value. Negative angle amounts will rotate clockwise.

        Unless rotating by 90 degree increments, the image will be padded larger to hold
        the new size. If the image has pixel alphas, the padded area will be transparent.
        Otherwise pygame will pick a color that matches the image colorkey or the topleft
        pixel value.

        :param angle: Rotation angle
        :type angle: int, float
        :return: None
        """
        assert isinstance(angle, (int, float))
        self._surface = _pygame.transform.rotate(self._surface, angle)
