"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BASEIMAGE
Provides a class to perform basic image loading an manipulation with pygame.

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

__all__ = [

    # Image paths
    'IMAGE_EXAMPLE_CARBON_FIBER',
    'IMAGE_EXAMPLE_GRAY_LINES',
    'IMAGE_EXAMPLE_METAL',
    'IMAGE_EXAMPLE_PYGAME_MENU',
    'IMAGE_EXAMPLE_WALLPAPER',
    'IMAGE_EXAMPLES',

    # Drawing modes
    'IMAGE_MODE_CENTER',
    'IMAGE_MODE_FILL',
    'IMAGE_MODE_REPEAT_X',
    'IMAGE_MODE_REPEAT_XY',
    'IMAGE_MODE_REPEAT_Y',
    'IMAGE_MODE_SIMPLE',

    # Base class
    'BaseImage'

]

import os.path as path
import math
from pathlib import Path

import pygame
from pygame_menu.utils import assert_vector2
from pygame_menu.custom_types import Tuple2IntType, Union, Vector2NumberType, Callable, Tuple, List, \
    NumberType, Optional, Dict

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
    let write the image to an surface.

    :param image_path: Path of the image to be loaded. It can be a string or :py:class:`pathlib.Path` on ``Python 3+``
    :param drawing_mode: Drawing mode of the image
    :param drawing_offset: Offset of the image in drawing method
    :param load_from_file: Loads the image from the given path
    """
    _drawing_mode: int
    _drawing_offset: Tuple2IntType
    _extension: str
    _filename: str
    _filepath: str
    _original_surface: 'pygame.Surface'
    _surface: 'pygame.Surface'

    def __init__(self,
                 image_path: Union[str, Path],
                 drawing_mode: int = IMAGE_MODE_FILL,
                 drawing_offset: Vector2NumberType = (0, 0),
                 load_from_file: bool = True
                 ) -> None:
        assert isinstance(image_path, (str, Path))
        if isinstance(image_path, Path):
            image_path = str(image_path)
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
            self._surface = pygame.image.load(image_path)
            self._original_surface = self._surface.copy()

    def __copy__(self) -> 'BaseImage':
        """
        Copy method.

        :return: New instance of the object
        """
        return self.copy()

    def __deepcopy__(self, memodict: Dict) -> 'BaseImage':
        """
        Deepcopy method.

        :param memodict: Memo dict
        :return: New instance of the object
        """
        return self.copy()

    def copy(self) -> 'BaseImage':
        """
        Return a copy of the image.

        :return: Image
        """
        image = BaseImage(
            image_path=self._filepath,
            drawing_mode=self._drawing_mode,
            drawing_offset=self._drawing_offset,
            load_from_file=False
        )
        image._surface = self._surface.copy()
        image._original_surface = self._surface.copy()
        return image

    def get_path(self) -> str:
        """
        Return the image path.

        :return: Image path
        """
        return self._filepath

    def get_drawing_mode(self) -> int:
        """
        Return the image drawing mode.

        :return: Image drawing mode
        """
        return self._drawing_mode

    def set_drawing_mode(self, drawing_mode: int) -> None:
        """
        Set the image drawing mode.

        :param drawing_mode: Drawing mode
        :return: None
        """
        assert isinstance(drawing_mode, int)
        assert drawing_mode in [IMAGE_MODE_CENTER, IMAGE_MODE_FILL, IMAGE_MODE_REPEAT_X,
                                IMAGE_MODE_REPEAT_Y, IMAGE_MODE_REPEAT_XY, IMAGE_MODE_SIMPLE], \
            'unknown image drawing mode'
        self._drawing_mode = drawing_mode

    def get_drawing_offset(self) -> Tuple2IntType:
        """
        Return the image drawing offset.

        :return: Image drawing offset
        """
        return self._drawing_offset

    def set_drawing_offset(self, drawing_offset: Vector2NumberType) -> None:
        """
        Set the image drawing offset.

        :param drawing_offset: Drawing offset tuple *(x, y)*
        :return: None
        """
        assert_vector2(drawing_offset)
        self._drawing_offset = (int(drawing_offset[0]), int(drawing_offset[1]))

    def get_size(self) -> Tuple2IntType:
        """
        Return the size in pixels of the image.

        :return: Image size tuple *(width, height)*
        """
        return int(self._surface.get_width()), int(self._surface.get_height())

    def get_surface(self) -> 'pygame.Surface':
        """
        Return the surface object of the image.

        :return: Image surface
        """
        return self._surface

    def get_namefile(self) -> str:
        """
        Return the name of the image file.

        :return: Filename
        """
        return self._filename

    def get_extension(self) -> str:
        """
        Return the extension of the image file.

        :return: File extension
        """
        return self._extension

    def equals(self, image: 'BaseImage') -> bool:
        """
        Return ``True`` if the image is the same as the object.

        :param image: Image object
        :return: ``True`` if the image is the same (note, the surface)
        """
        assert isinstance(image, BaseImage)
        im1 = pygame.image.tostring(self._surface, 'RGBA')
        im2 = pygame.image.tostring(image._surface, 'RGBA')
        return im1 == im2

    def restore(self) -> None:
        """
        Restore image to the original surface.

        :return: None
        """
        self._surface = self._original_surface.copy()

    def checkpoint(self) -> None:
        """
        Updates the original surface to the current surface.

        :return: None
        """
        self._original_surface = self._surface.copy()

    def apply_image_function(self, image_function: Callable[[int, int, int, int], Tuple[int, int, int, int]]
                             ) -> 'BaseImage':
        """
        Apply a function to each pixel of the image. The function will receive the red, green, blue and alpha
        colors and must return the same values. The color pixel will be overriden by the function output.

        .. note::

            See :py:meth:`pygame_menu.BaseImage.to_bw` method as an example.

        :param image_function: Color function, takes colors as ``image_function=myfunc(r,g,b,a)``. Returns the same tuple *(r, g, b, a)*
        :return: Self reference
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

    def to_bw(self) -> 'BaseImage':
        """
        Converts the image to black and white.

        :return: Self reference
        """

        def bw(r: int, g: int, b: int, a: int) -> Tuple[int, int, int, int]:
            """
            To black-white function.
            """
            c = int((r + g + b) / 3)
            return c, c, c, a

        return self.apply_image_function(image_function=bw)

    def pick_channels(self, channels: Union[str, Tuple[str, ...], List[str]]) -> 'BaseImage':
        """
        Pick certain channels of the image, channels are ``"r"`` (red), ``"g"`` (green) and ``"b"`` (blue),
        ``channels param`` is a list/tuple of channels (non empty).

        For example, ``pick_channels(['r', 'g'])``: All channels not included on the list will be discarded.

        :param channels: Channels, list or tuple containing ``"r"``, ``"g"`` or ``"b"`` (all combinations are possible)
        :return: Self reference
        """
        if isinstance(channels, str):
            channels = [channels]
        assert isinstance(channels, (tuple, list))
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

    def flip(self, x: bool, y: bool) -> 'BaseImage':
        """
        This method can flip the image either vertically, horizontally, or both.
        Flipping a image is non-destructive and does not change the dimensions.

        :param x: Flip in x axis
        :param y: Flip on y axis
        :return: Self reference
        """
        assert isinstance(x, bool)
        assert isinstance(y, bool)
        assert (x or y), 'at least one axis should be True'
        self._surface = pygame.transform.flip(self._surface, x, y)
        return self

    def scale(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'BaseImage':
        """
        Scale the image to a desired width and height factor.

        :param width: Scale factor of the width
        :param height: Scale factor of the height
        :param smooth: Smooth scaling
        :return: Self reference
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
        return self

    def scale2x(self) -> 'BaseImage':
        """
        This will return a new image that is double the size of the original.
        It uses the AdvanceMAME Scale2X algorithm which does a "jaggy-less"
        scale of bitmap graphics.

        This really only has an effect on simple images with solid colors.
        On photographic and antialiased images it will look like a regular
        unfiltered scale.

        :return: Self reference
        """
        self._surface = pygame.transform.scale2x(self._surface)
        return self

    def resize(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'BaseImage':
        """
        Set the image size to another size.

        :param width: New width of the image in px
        :param height: New height of the image in px
        :param smooth: Smooth scaling
        :return: Self reference
        """
        assert isinstance(width, (int, float))
        assert isinstance(height, (int, float))
        assert isinstance(smooth, bool)
        assert width > 0 and height > 0, 'width and height must be greater than zero'
        w, h = self.get_size()
        if w == width and h == height:
            return self
        return self.scale(width=float(width) / w, height=float(height) / h, smooth=smooth)

    def get_rect(self) -> 'pygame.Rect':
        """
        Return the rect of the image.

        :return: Pygame rect object
        """
        return self._surface.get_rect()

    def rotate(self, angle: NumberType) -> 'BaseImage':
        """
        Unfiltered counterclockwise rotation. The angle argument represents degrees
        and can be any floating point value. Negative angle amounts will rotate clockwise.

        .. note::

            Unless rotating by 90 degree increments, the image will be padded larger to hold
            the new size. If the image has pixel alphas, the padded area will be transparent.
            Otherwise pygame will pick a color that matches the image colorkey or the topleft
            pixel value.

        :param angle: Rotation angle (degrees ``0-360``)
        :return: Self reference
        """
        assert isinstance(angle, (int, float))
        self._surface = pygame.transform.rotate(self._surface, angle)
        return self

    def draw(self, surface: 'pygame.Surface', area: Optional['pygame.Rect'] = None,
             position: Tuple2IntType = (0, 0)) -> None:
        """
        Draw the image in a given surface.

        :param surface: Pygame surface object
        :param area: Area to draw; if ``None`` the image will be drawn on entire surface
        :param position: Position to draw in *(x, y)*
        :return: None
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(area, (pygame.Rect, type(None)))
        assert isinstance(position, tuple)

        if area is None:
            area = surface.get_rect()

        if self._drawing_mode == IMAGE_MODE_FILL:

            surface.blit(
                pygame.transform.scale(self._surface, (area.width, area.height)),
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
