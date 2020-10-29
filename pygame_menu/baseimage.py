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
# File constants no. 100

import os.path as path
import math

import pygame
from pygame_menu.utils import assert_vector2

# Example images
__fontdir = path.join(path.dirname(path.abspath(__file__)), 'resources', 'images', '{0}')

IMAGE_EXAMPLE_CARBON_FIBER = __fontdir.format('carbon_fiber.png')
IMAGE_EXAMPLE_GRAY_LINES = __fontdir.format('gray_lines.png')
IMAGE_EXAMPLE_METAL = __fontdir.format('metal.png')
IMAGE_EXAMPLE_PYGAME_MENU = __fontdir.format('pygame_menu.png')
IMAGE_EXAMPLE_WALLPAPER = __fontdir.format('wallpaper.jpg')

# Drawing modes
IMAGE_MODE_CENTER = 100
IMAGE_MODE_FILL = 101
IMAGE_MODE_REPEAT_X = 102
IMAGE_MODE_REPEAT_XY = 103
IMAGE_MODE_REPEAT_Y = 104
IMAGE_MODE_SIMPLE = 105  # Just draw the image without any effect


class BaseImage(object):
    """
    Object that loads an image, stores as a surface, transform it and
    let write the image to an surface.

    :param image_path: Path of the image to be loaded
    :type image_path: str
    :param drawing_mode: Drawing mode of the image
    :type drawing_mode: int
    :param drawing_offset: Offset of the image in drawing method
    :type drawing_offset: tuple, list
    """

    def __init__(self,
                 image_path,
                 drawing_mode=IMAGE_MODE_FILL,
                 drawing_offset=(0, 0)
                 ):
        assert isinstance(image_path, str)
        assert isinstance(drawing_mode, int)
        assert_vector2(drawing_offset)

        _, file_extension = path.splitext(image_path)
        file_extension = file_extension.lower()

        valid_formats = ['.jpg', '.png', '.gif', '.bmp', '.pcx', '.tga', '.tif', '.lbm',
                         '.pbm', '.pgm', '.ppm', '.xpm']
        assert file_extension in valid_formats, \
            'file extension {0} not valid, please use: {1}'.format(file_extension, ','.join(valid_formats))
        assert path.isfile(image_path), 'file {0} does not exist or could not be found, please ' \
                                        'check if the path of the image is valid'.format(image_path)

        self._filepath = image_path
        self._filename = path.splitext(path.basename(image_path))[0]
        self._extension = file_extension

        # Drawing mode
        self._drawing_mode = drawing_mode
        self._drawing_offset = (drawing_offset[0], drawing_offset[1])

        # Load the image and store as a surface
        self._surface = pygame.image.load(image_path)  # type: pygame.Surface
        self._original_surface = self._surface.copy()

    def __str__(self):
        """
        :return: String definition of the object
        :rtype: str
        """
        msg = 'BaseImage Object {3}\n\tPath: {0}\n\tDrawing mode: {1}\n\tDrawing offset: {2}'
        return msg.format(self._filepath, self._drawing_mode, self._drawing_offset, hex(id(self)))

    def __repr__(self):
        """
        Prints the object.

        :return: None
        """
        print(self.__str__())

    def get_size(self):
        """
        Return the size in pixels of the image.

        :return: (width,height)
        :rtype: tuple
        """
        return self._surface.get_width(), self._surface.get_height()

    def get_surface(self):
        """
        Return the surface object of the image.

        :return: Image surface
        :rtype: :py:class:`pygame.Surface`
        """
        return self._surface

    def get_namefile(self):
        """
        Return the name of the image file.

        :return: Filename
        :rtype: str
        """
        return self._filename

    def get_extension(self):
        """
        Return the extension of the image file.

        :return: File extension
        :rtype: str
        """
        return self._extension

    def equals(self, image):
        """
        Return true if the image is the same as the object.

        :param image: Image object
        :type image: :py:class:`pygame_menu.baseimage.BaseImage`
        :return: True if the image is the same (note, the surface)
        :rtype: bool
        """
        assert isinstance(image, BaseImage)
        im1 = pygame.image.tostring(self._surface, 'RGBA')
        im2 = pygame.image.tostring(image._surface, 'RGBA')
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
        self._surface = pygame.transform.flip(self._surface, x, y)

    def scale(self, width, height, smooth=False):
        """
        Scale the image to a desired width and height factor.

        :param width: Scale factor of the width
        :type width: int, float
        :param height: Scale factor of the height
        :type height: int, float
        :param smooth: Smooth scaling
        :type smooth: bool
        :return: None
        """
        assert isinstance(width, (int, float))
        assert isinstance(height, (int, float))
        assert isinstance(smooth, bool)
        assert width > 0 and height > 0, 'width and height must be greater than zero'
        w, h = self.get_size()
        if not smooth:
            self._surface = pygame.transform.scale(self._surface, (int(w * width), int(h * height)))
        else:
            self._surface = pygame.transform.smoothscale(self._surface, (int(w * width), int(h * height)))

    def scale2x(self):
        """
        This will return a new image that is double the size of the original.
        It uses the AdvanceMAME Scale2X algorithm which does a 'jaggy-less'
        scale of bitmap graphics.

        This really only has an effect on simple images with solid colors.
        On photographic and antialiased images it will look like a regular unfiltered scale.

        :return: None
        """
        self._surface = pygame.transform.scale2x(self._surface)

    def resize(self, width, height, smooth=False):
        """
        Set the image size to another size.
        This is a fast scale operation.

        :param width: New width of the image
        :type width: int, float
        :param height: New height of the image
        :type height: int, float
        :param smooth: Smooth scaling
        :type smooth: bool
        :return: None
        """
        assert isinstance(width, (int, float))
        assert isinstance(height, (int, float))
        assert isinstance(smooth, bool)
        assert width > 0 and height > 0, 'width and height must be greater than zero'
        w, h = self.get_size()
        if w == width and h == height:
            return
        self.scale(width=float(width) / w, height=float(height) / h, smooth=smooth)

    def get_rect(self):
        """
        Return the rect of the image.

        :return: Pygame rect object
        :rtype: :py:class:`pygame.Rect`
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
        self._surface = pygame.transform.rotate(self._surface, angle)

    def get_drawing_mode(self):
        """
        Return the image drawing mode.

        :return: Image drawing mode
        :rtype: int
        """
        return self._drawing_mode

    def draw(self, surface, area=None, position=(0, 0)):
        """
        Draw the image in a given surface.

        :param surface: Pygame surface object
        :type surface: :py:class:`pygame.Surface`
        :param area: Area to draw, if None, Image will be drawn on entire surface
        :type area: :py:class:`pygame.Rect`, None
        :param position: Position to draw
        :type position: tuple
        :return: None
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(area, (pygame.Rect, type(None)))
        assert isinstance(position, tuple)

        if area is None:
            area = surface.get_rect()

        if self._drawing_mode == IMAGE_MODE_FILL:

            surface.blit(pygame.transform.scale(self._surface, (area.width, area.height)),
                         (
                             self._drawing_offset[0] + position[0],
                             self._drawing_offset[1] + position[1]
                         ))

        elif self._drawing_mode == IMAGE_MODE_REPEAT_X:

            w = self._surface.get_width()
            times = int(math.ceil(float(area.width) / w))
            assert times > 0, \
                'invalid size, width must be greater than zero'
            for x in range(times):
                surface.blit(self._surface,
                             (x * w + self._drawing_offset[0] + position[0],
                              self._drawing_offset[1] + position[1]),
                             area
                             )

        elif self._drawing_mode == IMAGE_MODE_REPEAT_Y:

            h = self._surface.get_height()
            times = int(math.ceil(float(area.height) / h))
            assert times > 0, \
                'invalid size, height must be greater than zero'
            for y in range(times):
                surface.blit(self._surface,
                             (
                                 0 + self._drawing_offset[0] + position[0],
                                 y * h + self._drawing_offset[1] + position[1]),
                             area)

        elif self._drawing_mode == IMAGE_MODE_REPEAT_XY:

            w, h = self._surface.get_size()
            timesx = int(math.ceil(float(area.width) / w))
            timesy = int(math.ceil(float(area.height) / h))
            assert timesx > 0 and timesy > 0, \
                'invalid size, width and height must be greater than zero'
            for x in range(timesx):
                for y in range(timesy):
                    surface.blit(self._surface,
                                 (
                                     x * w + self._drawing_offset[0] + position[0],
                                     y * h + self._drawing_offset[1] + position[1],
                                 ),
                                 area)

        elif self._drawing_mode == IMAGE_MODE_CENTER:

            sw, hw = area.width, area.height  # Window
            w, h = self._surface.get_size()  # Image
            surface.blit(self._surface,
                         (
                             float(sw - w) / 2 + self._drawing_offset[0] + position[0],
                             float(hw - h) / 2 + self._drawing_offset[1] + position[1],
                         ),
                         area)

        elif self._drawing_mode == IMAGE_MODE_SIMPLE:

            surface.blit(
                self._surface,
                (
                    self._drawing_offset[0] + position[0],
                    self._drawing_offset[1] + position[1]
                ),
                area)

        else:
            raise ValueError('invalid image mode')
