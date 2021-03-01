# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BASEIMAGE
Provides a class to perform basic image loading and manipulation with pygame.

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
# File constants no. 100

import os.path as path
import math

try:
    # noinspection PyCompatibility
    from pathlib import Path as _Path
except ImportError:
    _Path = None

import pygame
from pygame_menu.utils import assert_vector2, isinstance_str

# Example image paths
__images_path__ = path.join(path.dirname(path.abspath(__file__)), 'resources', 'images', '{0}')

IMAGE_EXAMPLE_CARBON_FIBER = __images_path__.format('carbon_fiber.png')
IMAGE_EXAMPLE_GRAY_LINES = __images_path__.format('gray_lines.png')
IMAGE_EXAMPLE_METAL = __images_path__.format('metal.png')
IMAGE_EXAMPLE_PYGAME_MENU = __images_path__.format('pygame_menu.png')
IMAGE_EXAMPLE_WALLPAPER = __images_path__.format('wallpaper.jpg')

IMAGE_EXAMPLES = (IMAGE_EXAMPLE_CARBON_FIBER, IMAGE_EXAMPLE_GRAY_LINES, IMAGE_EXAMPLE_METAL,
                  IMAGE_EXAMPLE_PYGAME_MENU, IMAGE_EXAMPLE_WALLPAPER)

# Drawing modes
IMAGE_MODE_CENTER = 100
IMAGE_MODE_FILL = 101
IMAGE_MODE_REPEAT_X = 102
IMAGE_MODE_REPEAT_XY = 103
IMAGE_MODE_REPEAT_Y = 104
IMAGE_MODE_SIMPLE = 105  # Just draw the image without any effect

# Other constants
_VALID_IMAGE_FORMATS = ['.jpg', '.png', '.gif', '.bmp', '.pcx', '.tga', '.tif', '.lbm',
                        '.pbm', '.pgm', '.ppm', '.xpm']


class BaseImage(object):
    """
    Object that loads an image, stores as a surface, transform it and
    let write the image to a surface.

    :param image_path: Path of the image to be loaded. It can be a string or :py:class:`pathlib.Path` on ``Python 3+``
    :type image_path: str, :py:class:`pathlib.Path`
    :param drawing_mode: Drawing mode of the image
    :type drawing_mode: int
    :param drawing_offset: Offset of the image in drawing method
    :type drawing_offset: tuple, list
    :param load_from_file: Loads the image from the given path
    :type load_from_file: bool
    """

    def __init__(self,
                 image_path,
                 drawing_mode=IMAGE_MODE_FILL,
                 drawing_offset=(0, 0),
                 load_from_file=True
                 ):
        if _Path is not None:
            if isinstance(image_path, _Path):
                image_path = str(image_path)
        assert isinstance_str(image_path)
        assert isinstance(load_from_file, bool)

        _, file_extension = path.splitext(image_path)
        file_extension = file_extension.lower()

        assert file_extension in _VALID_IMAGE_FORMATS, \
            'file extension {0} not valid, please use: {1}'.format(file_extension, ','.join(_VALID_IMAGE_FORMATS))
        assert path.isfile(image_path), 'file {0} does not exist or could not be found, please ' \
                                        'check if the path of the image is valid'.format(image_path)

        self._filepath = image_path
        self._filename = path.splitext(path.basename(image_path))[0]
        self._extension = file_extension

        # Drawing mode
        self._drawing_mode = 0
        self._drawing_offset = (0, 0)

        self.set_drawing_mode(drawing_mode)
        self.set_drawing_offset(drawing_offset)

        # Load the image and store as a surface
        if load_from_file:
            self._surface = pygame.image.load(image_path)  # type: pygame.Surface
            self._original_surface = self._surface.copy()

        # Other internals
        self._last_transform = (0, 0, None)  # Improves drawing
        self.smooth_scaling = True  # Uses smooth scaling by default in draw() method

    def get_path(self):
        """
        Return the image path.

        :return: Image path
        :rtype: str
        """
        return self._filepath

    def get_drawing_mode(self):
        """
        Return the image drawing mode.

        :return: Image drawing mode
        :rtype: int
        """
        return self._drawing_mode

    def set_drawing_mode(self, drawing_mode):
        """
        Set the image drawing mode.

        :param drawing_mode: Drawing mode
        :type drawing_mode: int
        :return: None
        """
        assert isinstance(drawing_mode, int)
        assert drawing_mode in [IMAGE_MODE_CENTER, IMAGE_MODE_FILL, IMAGE_MODE_REPEAT_X,
                                IMAGE_MODE_REPEAT_Y, IMAGE_MODE_REPEAT_XY, IMAGE_MODE_SIMPLE], \
            'unknown image drawing mode'
        self._drawing_mode = drawing_mode

    def get_drawing_offset(self):
        """
        Return the image drawing offset.

        :return: Image drawing offset
        :rtype: tuple
        """
        return self._drawing_offset

    def set_drawing_offset(self, drawing_offset):
        """
        Set the image drawing offset.

        :param drawing_offset: Drawing offset tuple *(x, y)*
        :type drawing_offset: tuple, list
        :return: None
        """
        assert_vector2(drawing_offset)
        self._drawing_offset = (drawing_offset[0], drawing_offset[1])

    def __copy__(self):
        """
        Copy method.

        :return: New instance of the object
        :rtype: BaseImage
        """
        return self.copy()

    def __deepcopy__(self, memodict):
        """
        Deepcopy method.

        :param memodict: Memo dict
        :type memodict: dict
        :return: New instance of the object
        :rtype: BaseImage
        """
        return self.copy()

    def copy(self):
        """
        Return a copy of the image.

        :return: Image
        :rtype: BaseImage
        """
        image = BaseImage(
            image_path=self._filepath,
            drawing_mode=self._drawing_mode,
            drawing_offset=self._drawing_offset,
            load_from_file=False
        )
        image._surface = self._surface.copy()
        image._original_surface = self._surface.copy()
        image.smooth_scaling = self.smooth_scaling
        return image

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

    def apply_image_function(self, image_function):
        """
        Apply a function to each pixel of the image. The function will receive the red, green, blue and alpha
        colors and must return the same values. The color pixel will be overridden by the function output.

        .. note::

            See ``BaseImage.to_bw()`` method as an example.

        :param image_function: Color function, takes colors as ``image_function=myfunc(r, g, b, a)``. Returns the same tuple *(r,g,b,a)*
        :type image_function: callable
        :return: Self reference
        :rtype: BaseImage
        """
        w, h = self._surface.get_size()
        for x in range(w):
            for y in range(h):
                r, g, b, a = self._surface.get_at((x, y))
                r, g, b, a = image_function(r, g, b, a)
                r = int(max(0, min(r, 255)))
                g = int(max(0, min(g, 255)))
                b = int(max(0, min(b, 255)))
                a = int(max(0, min(a, 255)))
                # noinspection PyArgumentList
                self._surface.set_at((x, y), pygame.Color(r, g, b, a))
        return self

    def to_bw(self):
        """
        Converts the image to black and white.

        :return: Self reference
        :rtype: BaseImage
        """

        def bw(r, g, b, a):
            """
            To black-white function.
            """
            c = (r + g + b) / 3
            return c, c, c, a

        return self.apply_image_function(image_function=bw)

    def pick_channels(self, channels):
        """
        Pick certain channels of the image, channels are 'r' (red), 'g' (green) and 'b' (blue),
        ``channels param`` is a list/tuple of channels (non empty).

        For example, ``pick_channels(['r', 'g'])``: All channels not included on the list will be discarded.

        :param channels: Channels, list or tuple containing 'r', 'g' or 'b' (all combinations are possible)
        :type channels: tuple, list, str
        :return: Self reference
        :rtype: BaseImage
        """
        if isinstance_str(channels):
            channels = [channels]
        assert isinstance(channels, (list, tuple))
        assert 1 <= len(channels) <= 3, 'maximum size of channels can be 3'

        w, h = self._surface.get_size()
        for x in range(w):
            for y in range(h):
                r, g, b, a = self._surface.get_at((x, y))
                if 'r' not in channels:
                    r = 0
                if 'g' not in channels:
                    g = 0
                if 'b' not in channels:
                    b = 0
                # noinspection PyArgumentList
                self._surface.set_at((x, y), pygame.Color(r, g, b, a))
        return self

    def flip(self, x, y):
        """
        This method can flip the image either vertically, horizontally, or both.
        Flipping a image is non-destructive and does not change the dimensions.

        :param x: Flip in x axis
        :type x: bool
        :param y: Flip on y axis
        :type y: bool
        :return: Self reference
        :rtype: BaseImage
        """
        assert isinstance(x, bool)
        assert isinstance(y, bool)
        assert (x or y), 'at least one axis should be True'
        self._surface = pygame.transform.flip(self._surface, x, y)
        return self

    def scale(self, width, height, smooth=False):
        """
        Scale the image to a desired width and height factor.

        :param width: Scale factor of the width
        :type width: int, float
        :param height: Scale factor of the height
        :type height: int, float
        :param smooth: Smooth scaling
        :type smooth: bool
        :return: Self reference
        :rtype: BaseImage
        """
        assert isinstance(width, (int, float))
        assert isinstance(height, (int, float))
        assert isinstance(smooth, bool)
        assert width > 0 and height > 0, 'width and height must be greater than zero'
        w, h = self.get_size()
        if width == 1 and height == 1:
            return self
        if not smooth or self._surface.get_bitsize() < 24:
            self._surface = pygame.transform.scale(self._surface, (int(w * width), int(h * height)))
        else:  # image bitsize less than 24 bits raises ValueError
            self._surface = pygame.transform.smoothscale(self._surface, (int(w * width), int(h * height)))
        return self

    def scale2x(self):
        """
        This will return a new image that is double the size of the original.
        It uses the AdvanceMAME Scale2X algorithm which does a 'jaggy-less'
        scale of bitmap graphics.

        This really only has an effect on simple images with solid colors.
        On photographic and antialiased images it will look like a regular
        unfiltered scale.

        :return: Self reference
        :rtype: BaseImage
        """
        self._surface = pygame.transform.scale2x(self._surface)
        return self

    def resize(self, width, height, smooth=False):
        """
        Set the image size to another size.

        :param width: New width of the image in px
        :type width: int, float
        :param height: New height of the image in px
        :type height: int, float
        :param smooth: Smooth scaling
        :type smooth: bool
        :return: Self reference
        :rtype: BaseImage
        """
        assert isinstance(width, (int, float))
        assert isinstance(height, (int, float))
        assert isinstance(smooth, bool)
        assert width > 0 and height > 0, 'width and height must be greater than zero'
        w, h = self.get_size()
        if w == width and h == height:
            return self
        return self.scale(width=float(width) / w, height=float(height) / h, smooth=smooth)

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

        .. note::

            Unless rotating by 90 degree increments, the image will be padded larger to hold
            the new size. If the image has pixel alphas, the padded area will be transparent.
            Otherwise pygame will pick a color that matches the image colorkey or the topleft
            pixel value.

        :param angle: Rotation angle (degrees 0-360)
        :type angle: int, float
        :return: Self reference
        :rtype: BaseImage
        """
        assert isinstance(angle, (int, float))
        self._surface = pygame.transform.rotate(self._surface, angle)
        return self

    def draw(self, surface, area=None, position=(0, 0)):
        """
        Draw the image in a given surface.

        :param surface: Pygame surface object
        :type surface: :py:class:`pygame.Surface`
        :param area: Area to draw, if None, Image will be drawn on entire surface
        :type area: :py:class:`pygame.Rect`, None
        :param position: Position to draw in *(x, y)*
        :type position: tuple
        :return: None
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(area, (pygame.Rect, type(None)))
        assert isinstance(position, tuple)

        if area is None:
            area = surface.get_rect()

        if self._drawing_mode == IMAGE_MODE_FILL:

            # Check if exists the transformed surface
            if area.width == self._last_transform[0] and area.height == self._last_transform[1] and \
                    self._last_transform[2] is not None:
                surf = self._last_transform[2]
            else:  # Transform scale
                if self.smooth_scaling and self._surface.get_bitsize() > 8:
                    surf = pygame.transform.smoothscale(self._surface, (area.width, area.height))
                else:
                    surf = pygame.transform.scale(self._surface, (area.width, area.height))
                self._last_transform = (area.width, area.height, surf)

            surface.blit(
                surf,
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
                surface.blit(
                    self._surface,
                    (
                        x * w + self._drawing_offset[0] + position[0],
                        self._drawing_offset[1] + position[1]
                    ),
                    area
                )

        elif self._drawing_mode == IMAGE_MODE_REPEAT_Y:

            h = self._surface.get_height()
            times = int(math.ceil(float(area.height) / h))
            assert times > 0, \
                'invalid size, height must be greater than zero'
            for y in range(times):
                surface.blit(
                    self._surface,
                    (
                        0 + self._drawing_offset[0] + position[0],
                        y * h + self._drawing_offset[1] + position[1]
                    ),
                    area
                )

        elif self._drawing_mode == IMAGE_MODE_REPEAT_XY:

            w, h = self._surface.get_size()
            timesx = int(math.ceil(float(area.width) / w))
            timesy = int(math.ceil(float(area.height) / h))
            assert timesx > 0 and timesy > 0, \
                'invalid size, width and height must be greater than zero'
            for x in range(timesx):
                for y in range(timesy):
                    surface.blit(
                        self._surface,
                        (
                            x * w + self._drawing_offset[0] + position[0],
                            y * h + self._drawing_offset[1] + position[1]
                        ),
                        area
                    )

        elif self._drawing_mode == IMAGE_MODE_CENTER:

            sw, hw = area.width, area.height  # Window
            w, h = self._surface.get_size()  # Image
            surface.blit(
                self._surface,
                (
                    float(sw - w) / 2 + self._drawing_offset[0] + position[0],
                    float(hw - h) / 2 + self._drawing_offset[1] + position[1]
                ),
                area
            )

        elif self._drawing_mode == IMAGE_MODE_SIMPLE:

            surface.blit(
                self._surface,
                (
                    self._drawing_offset[0] + position[0],
                    self._drawing_offset[1] + position[1]
                ),
                area
            )
