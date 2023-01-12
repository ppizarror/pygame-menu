"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BASEIMAGE
Provides a class to perform basic image loading and manipulation with pygame.
"""
# File constants no. 100

__all__ = [

    # Base class
    'BaseImage',

    # Image paths
    'IMAGE_EXAMPLE_CARBON_FIBER',
    'IMAGE_EXAMPLE_GRAY_LINES',
    'IMAGE_EXAMPLE_METAL',
    'IMAGE_EXAMPLE_PYGAME_MENU',
    'IMAGE_EXAMPLE_PYTHON',
    'IMAGE_EXAMPLE_TILED_BORDER',
    'IMAGE_EXAMPLE_WALLPAPER',
    'IMAGE_EXAMPLES',

    # Drawing modes
    'IMAGE_MODE_CENTER',
    'IMAGE_MODE_FILL',
    'IMAGE_MODE_REPEAT_X',
    'IMAGE_MODE_REPEAT_XY',
    'IMAGE_MODE_REPEAT_Y',
    'IMAGE_MODE_SIMPLE'

]

from io import BytesIO
from pathlib import Path
import base64
import math
import os.path as path

import pygame

from pygame_menu._base import Base
from pygame_menu.locals import POSITION_NORTHWEST, POSITION_NORTHEAST, POSITION_CENTER, \
    POSITION_WEST, POSITION_SOUTHWEST, POSITION_EAST, POSITION_SOUTHEAST, \
    POSITION_SOUTH, POSITION_NORTH
from pygame_menu.utils import assert_vector, assert_position, assert_color, \
    load_pygame_image_file

from pygame_menu._types import Tuple2IntType, Union, Vector2NumberType, Callable, \
    Tuple, List, NumberType, Optional, Dict, Tuple4IntType, Literal, Tuple2NumberType, \
    ColorInputType, Tuple3IntType, NumberInstance, VectorInstance

# Example image paths
__images_path__ = path.join(path.dirname(path.abspath(__file__)), 'resources', 'images', '{0}')

IMAGE_EXAMPLE_CARBON_FIBER = __images_path__.format('carbon_fiber.png')
IMAGE_EXAMPLE_GRAY_LINES = __images_path__.format('gray_lines.png')
IMAGE_EXAMPLE_METAL = __images_path__.format('metal.png')
IMAGE_EXAMPLE_PYGAME_MENU = __images_path__.format('pygame_menu.png')
IMAGE_EXAMPLE_PYTHON = __images_path__.format('python.svg')
IMAGE_EXAMPLE_TILED_BORDER = __images_path__.format('tiled_border.png')
IMAGE_EXAMPLE_WALLPAPER = __images_path__.format('wallpaper.jpg')

IMAGE_EXAMPLES = (IMAGE_EXAMPLE_CARBON_FIBER, IMAGE_EXAMPLE_GRAY_LINES,
                  IMAGE_EXAMPLE_METAL, IMAGE_EXAMPLE_PYGAME_MENU, IMAGE_EXAMPLE_PYTHON,
                  IMAGE_EXAMPLE_TILED_BORDER, IMAGE_EXAMPLE_WALLPAPER)

# Drawing modes
IMAGE_MODE_CENTER = 100
IMAGE_MODE_FILL = 101
IMAGE_MODE_REPEAT_X = 102
IMAGE_MODE_REPEAT_XY = 103
IMAGE_MODE_REPEAT_Y = 104
IMAGE_MODE_SIMPLE = 105  # Just draw the image without any effect

_VALID_IMAGE_MODES = (IMAGE_MODE_CENTER, IMAGE_MODE_FILL, IMAGE_MODE_REPEAT_X,
                      IMAGE_MODE_REPEAT_XY, IMAGE_MODE_REPEAT_Y, IMAGE_MODE_SIMPLE)

# Other constants
_VALID_IMAGE_FORMATS = ['.jpg', '.png', '.gif', '.bmp', '.pcx', '.tga', '.tif',
                        '.lbm', '.pbm', '.pgm', '.ppm', '.xpm', '.svg', 'BytesIO',
                        'base64']

# Custom types
ColorChannelType = Literal['r', 'g', 'b']
ChannelType = Union[ColorChannelType, Tuple[ColorChannelType, ColorChannelType], Tuple[ColorChannelType, ColorChannelType, ColorChannelType], List[ColorChannelType]]


class BaseImage(Base):
    """
    Object that loads an image, stores as a surface, transform it and
    let write the image to a surface.

    :param image_path: Path of the image to be loaded. It can be a string (path, base64), :py:class:`pathlib.Path`, or :py:class:`io.BytesIO`
    :param drawing_mode: Drawing mode of the image
    :param drawing_offset: Offset of the image in drawing method
    :param drawing_position: Drawing position if mode is ``IMAGE_MODE_SIMPLE``. See :py:mod:`pygame_menu.locals` for valid ``position`` values
    :param load_from_file: Loads the image from the given path
    :param frombase64: If ``True`` consider ``image_path`` as base64 string
    :param image_id: str
    """
    _angle: NumberType
    _drawing_mode: int
    _drawing_offset: Tuple2IntType
    _drawing_position: str
    _extension: str
    _filename: str
    _filepath: Union[str, 'BytesIO']
    _frombase64: bool
    _last_transform: Tuple[int, int, Optional['pygame.Surface']]
    _original_surface: 'pygame.Surface'
    _rotated: bool
    _surface: 'pygame.Surface'
    smooth_scaling: bool

    def __init__(
            self,
            image_path: Union[str, 'Path', 'BytesIO'],
            drawing_mode: int = IMAGE_MODE_FILL,
            drawing_offset: Vector2NumberType = (0, 0),
            drawing_position: str = POSITION_NORTHWEST,
            load_from_file: bool = True,
            frombase64: bool = False,
            image_id: str = ''
    ) -> None:
        super(BaseImage, self).__init__(object_id=image_id)

        assert isinstance(image_path, (str, Path, BytesIO)), \
            'path must be string, Path, or BytesIO object type'
        assert isinstance(load_from_file, bool)
        assert isinstance(frombase64, bool)

        if isinstance(image_path, (str, Path)):
            image_path = str(image_path)
            if not frombase64:
                _, file_extension = path.splitext(image_path)
                file_extension = file_extension.lower()
                assert path.isfile(image_path), \
                    f'file {image_path} does not exist or could not be found, please ' \
                    f'check if the path of the image is valid'
            else:
                file_extension = 'base64'
        else:
            file_extension = 'BytesIO'

        assert file_extension in _VALID_IMAGE_FORMATS, \
            f'file extension {file_extension} not valid, please use: {", ".join(_VALID_IMAGE_FORMATS)}'

        self._filepath = image_path
        if isinstance(self._filepath, str) and not frombase64:
            self._filename = path.splitext(path.basename(image_path))[0]
        else:
            self._filename = ''
        self._extension = file_extension
        self._frombase64 = frombase64

        # Drawing mode
        self._drawing_mode = 0
        self._drawing_offset = (0, 0)
        self._drawing_position = ''

        self.set_drawing_mode(drawing_mode)
        self.set_drawing_offset(drawing_offset)
        self.set_drawing_position(drawing_position)

        # Convert from bas64 to bytesio
        if frombase64:
            if 'base64,' in image_path:  # Remove header of file
                for i in range(len(image_path)):
                    if image_path[i] == ',':
                        image_path = image_path[(i + 1):]
                        break
            image_path = BytesIO(base64.b64decode(image_path))

        # Load the image and store as a surface
        if load_from_file:
            self._surface = load_pygame_image_file(image_path)
            self._original_surface = self._surface.copy()

        # Other internals
        self._angle = 0
        self._last_transform = (0, 0, None)  # Improves drawing
        self._rotated = False
        self.smooth_scaling = True  # Uses smooth scaling by default in draw() method

    def __copy__(self) -> 'BaseImage':
        """
        Copy method.

        :return: New instance of the object
        """
        return self.copy()

    def __deepcopy__(self, memodict: Dict) -> 'BaseImage':
        """
        Deep-copy method.

        :param memodict: Memo dict
        :return: New instance of the object
        """
        return self.copy()

    def crop_rect(self, rect: 'pygame.Rect') -> 'BaseImage':
        """
        Crop image from rect.

        :param rect: Crop rect geometry
        :return: Self reference
        """
        self._surface = self.get_crop_rect(rect)
        return self

    def set_alpha(self, value: Optional[int], flags: int = 0) -> 'BaseImage':
        """
        Set the current alpha value for the Surface. When blitting this Surface
        onto a destination, the pixels will be drawn slightly transparent. The alpha
        value is an integer from ``0`` to ``255``, ``0`` is fully transparent and
        ``255`` is fully opaque. If None is passed for the alpha value, then alpha
        blending will be disabled, including per-pixel alpha.

        This value is different from the per pixel Surface alpha. For a surface with
        per pixel alpha, blanket alpha is ignored and None is returned.

        For pygame 2.0: per-surface alpha can be combined with per-pixel alpha.

        The optional flags argument can be set to pygame.RLEACCEL to provide better
        performance on non accelerated displays. A RLEACCEL Surface will be slower
        to modify, but quicker to blit as a source.

        :param value: Transparency value from ``0`` to ``255``
        :param flags: Optional flags
        :return: Self reference
        """
        if value is None:
            self._surface.set_alpha(None)
            return self
        assert isinstance(value, int)
        assert 0 <= value <= 255, 'alpha value must be an integer between 0 and 255'
        self._surface.set_alpha(value, flags)
        return self

    def crop(
            self,
            x: NumberType,
            y: NumberType,
            width: NumberType,
            height: NumberType
    ) -> 'BaseImage':
        """
        Crops the image from coordinate on x-axis and y-axis (x, y).

        :param x: X position within the image in px
        :param y: Y position in px
        :param width: Crop width in px
        :param height: Crop height in px
        :return: Self reference
        """
        self._surface = self.get_crop(x, y, width, height)
        return self

    def get_crop_rect(self, rect: 'pygame.Rect') -> 'pygame.Surface':
        """
        Get a crop surface of the image from rect.

        :param rect: Crop rect geometry
        :return: Cropped surface
        """
        return self._surface.subsurface(rect)

    def get_crop(
            self,
            x: NumberType,
            y: NumberType,
            width: NumberType,
            height: NumberType
    ) -> 'pygame.Surface':
        """
        Get a crop of the image from coordinate on x-axis and y-axis (x, y).

        :param x: X position within the image in px
        :param y: Y position in px
        :param width: Crop width in px
        :param height: Crop height in px
        :return: Cropped surface
        """
        assert 0 <= x < self.get_width(), \
            'X position must be between 0 and the image width'
        assert 0 <= y < self.get_height(), \
            'Y position must be between 0 and the image width'
        assert 0 < width <= self.get_width(), \
            'Width must be greater than zero and less than the image width'
        assert 0 < height <= self.get_height(), \
            'Height must be greater than zero and less than the image height'
        assert (x + width) <= self.get_width(), \
            'Crop box cannot exceed image width'
        assert (y + height) <= self.get_height(), \
            'Crop box cannot exceed image height'
        rect = pygame.Rect(0, 0, 0, 0)
        rect.x = x
        rect.y = y
        rect.width = width
        rect.height = height
        return self.get_crop_rect(rect)

    def copy(self) -> 'BaseImage':
        """
        Return a copy of the image.

        :return: Image
        """
        image = BaseImage(
            image_path=self._filepath,
            drawing_mode=self._drawing_mode,
            drawing_offset=self._drawing_offset,
            load_from_file=False,
            frombase64=self._frombase64
        )
        image._angle = self._angle
        image._surface = self._surface.copy()
        image._original_surface = self._surface.copy()
        image.smooth_scaling = self.smooth_scaling
        if self._attributes is not None:
            for k in self._attributes.keys():
                image.set_attribute(k, self._attributes[k])
        return image

    def get_path(self) -> Union[str, 'BytesIO']:
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

    def set_drawing_mode(self, drawing_mode: int) -> 'BaseImage':
        """
        Set the image drawing mode.

        :param drawing_mode: Drawing mode
        :return: Self reference
        """
        assert isinstance(drawing_mode, int)
        assert drawing_mode in _VALID_IMAGE_MODES, 'unknown image drawing mode'
        self._drawing_mode = drawing_mode
        return self

    def get_drawing_offset(self) -> Tuple2IntType:
        """
        Return the image drawing offset.

        :return: Image drawing offset
        """
        return self._drawing_offset

    def set_drawing_offset(self, offset: Vector2NumberType) -> 'BaseImage':
        """
        Set the image drawing offset.

        :param offset: Drawing offset tuple on x-axis and y-axis (x, y) in px
        :return: Self reference
        """
        assert_vector(offset, 2)
        self._drawing_offset = (int(offset[0]), int(offset[1]))
        return self

    def set_drawing_position(self, position: str) -> 'BaseImage':
        """
        Set the image position.

        .. note::

            See :py:mod:`pygame_menu.locals` for valid ``position`` values.

        :param position: Image position
        :return: Self reference
        """
        assert_position(position)
        self._drawing_position = position
        return self

    def get_width(self) -> int:
        """
        Return image width in px.

        :return: Image width
        """
        return int(self._surface.get_width())

    def get_height(self) -> int:
        """
        Return image height in px.

        :return: Image height
        """
        return int(self._surface.get_height())

    def subsurface(self, rect: Union[Tuple4IntType, 'pygame.Rect']) -> 'pygame.Surface':
        """
        Return a subsurface from a rect.

        :param rect: Rect
        :return: Subsurface
        """
        return self._surface.subsurface(rect)

    def get_size(self) -> Tuple2IntType:
        """
        Return the size in pixels of the image.

        :return: Image size tuple (width, height)
        """
        return self.get_width(), self.get_height()

    def get_at(
            self,
            pos: Tuple2NumberType,
            ignore_alpha: bool = False
    ) -> Union[Tuple3IntType, Tuple4IntType]:
        """
        Get the color from a certain position in image on x-axis and y-axis (x, y).

        ``get_at`` return a copy of the RGBA Color value at the given pixel. If the
        Surface has no per pixel alpha, then the alpha value will always be ``255``
        (opaque). If the pixel position is outside the area of the Surface an
        ``IndexError`` exception will be raised.

        Getting and setting pixels one at a time is generally too slow to be used
        in a game or realtime situation. It is better to use methods which operate
        on many pixels at a time like with the blit, fill and draw methods - or by
        using pygame.surfarraypygame module for accessing surface pixel data using
        array interfaces/pygame.PixelArraypygame object for direct pixel access of
        surfaces.

        :param pos: Position on x-axis and y-axis (x, y) in px
        :param ignore_alpha: If ``True`` returns only the three main channels
        :return: Color
        """
        assert_vector(pos, 2)
        color = self._surface.get_at(pos)
        if ignore_alpha:
            return color[0], color[1], color[2]
        return color

    def set_at(self, pos: Tuple2NumberType, color: ColorInputType) -> 'BaseImage':
        """
        Set the color of pixel on x-axis and y-axis (x, y).

        :param pos: Position on x-axis and y-axis (x, y) in px
        :param color: Color
        :return: Self reference
        """
        assert_vector(pos, 2)
        self._surface.set_at(pos, assert_color(color))
        return self

    def get_bitsize(self) -> int:
        """
        Return the image bit size.

        :return: Image size
        """
        return self._surface.get_bitsize()

    def get_surface(self, new: bool = True) -> 'pygame.Surface':
        """
        Return the surface object of the image.

        :param new: Return a new surface; if ``False`` return the same object
        :return: Image surface
        """
        if new:
            return self.get_crop_rect(self.get_rect())
        return self._surface

    def get_filename(self) -> str:
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

    def restore(self) -> 'BaseImage':
        """
        Restore image to the original surface.

        :return: Self reference
        """
        self._surface = self._original_surface.copy()
        return self

    def checkpoint(self) -> 'BaseImage':
        """
        Updates the original surface to the current surface.

        :return: Self reference
        """
        self._original_surface = self._surface.copy()
        return self

    def apply_image_function(
            self,
            image_function: Callable[[int, int, int, int], Tuple4IntType]
    ) -> 'BaseImage':
        """
        Apply a function to each pixel of the image. The function will receive the
        red, green, blue and alpha colors and must return the same values. The
        color pixel will be overridden by the function output.

        .. note::

            See :py:meth:`pygame_menu.baseimage.BaseImage.to_bw` method as an
            example.

        :param image_function: Color function, takes colors as ``image_function=myfunc(r,g,b,a)``. Returns the same tuple (r, g, b, a)
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
                self.set_at((x, y), pygame.Color(r, g, b, a))
        return self

    def to_bw(self) -> 'BaseImage':
        """
        Converts the image to black and white.

        .. note::

            This function is slow for large images.

        :return: Self reference
        """

        def bw(r: int, g: int, b: int, a: int) -> Tuple4IntType:
            """
            To black-white function.
            """
            c = int((r + g + b) / 3)
            return c, c, c, a

        return self.apply_image_function(image_function=bw)

    def pick_channels(self, channels: ChannelType) -> 'BaseImage':
        """
        Pick certain channels of the image, channels are ``"r"`` (red), ``"g"``
        (green) and ``"b"`` (blue); ``channels param`` is a list/tuple of channels
        (non-empty).

        For example, ``pick_channels(['r', 'g'])``: All channels not included on
        the list will be discarded.

        :param channels: Channels, list or tuple containing ``"r"``, ``"g"`` or ``"b"`` (all combinations are possible)
        :return: Self reference
        """
        if isinstance(channels, str):
            channels = [channels]
        assert isinstance(channels, VectorInstance)
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
        Flipping an image is non-destructive and does not change the dimensions.

        :param x: Flip on x-axis
        :param y: Flip on y-axis
        :return: Self reference
        """
        assert isinstance(x, bool)
        assert isinstance(y, bool)
        assert (x or y), 'at least one axis should be True'
        self._surface = pygame.transform.flip(self._surface, x, y)
        return self

    def scale(
            self,
            width: NumberType,
            height: NumberType,
            smooth: bool = True
    ) -> 'BaseImage':
        """
        Scale the image to a desired width and height factor.

        .. note::

            The scale transformation is permanent, and is applied over the same
            object. Thus, if ``image.scale(2, 2).scale(2, 2)`` the final scale of
            the initial image is equal to ``image.scale(4, 4)``.

        :param width: Width scale factor
        :param height: Height scale factor
        :param smooth: Smooth scaling
        :return: Self reference
        """
        assert isinstance(width, NumberInstance)
        assert isinstance(height, NumberInstance)
        assert isinstance(smooth, bool)
        assert width > 0 and height > 0, \
            'width and height must be greater than zero'
        w, h = self.get_size()
        if width == 1 and height == 1:
            return self
        if not smooth or self._surface.get_bitsize() < 24:
            self._surface = pygame.transform.scale(self._surface, (int(w * width), int(h * height)))
        else:  # image bitsize less than 24 bits raises ValueError
            self._surface = pygame.transform.smoothscale(self._surface, (int(w * width), int(h * height)))
        return self

    def scale2x(self) -> 'BaseImage':
        """
        This will return a new image that is double the size of the original. It
        uses the AdvanceMAME Scale2X algorithm which does a "jaggy-less" scale of
        bitmap graphics.

        This really only has an effect on simple images with solid colors. On
        photographic and anti-aliased images it will look like a regular unfiltered
        scale.

        :return: Self reference
        """
        self._surface = pygame.transform.scale2x(self._surface)
        return self

    def scale4x(self) -> 'BaseImage':
        """
        Applies a x4 scale factor using scale 2x algorithm.

        :return: Self reference
        """
        return self.scale2x().scale2x()

    def resize(
            self,
            width: NumberType,
            height: NumberType,
            smooth: bool = True
    ) -> 'BaseImage':
        """
        Resize the image to a desired (width, height) size in pixels.

        :param width: New width of the image in px
        :param height: New height of the image in px
        :param smooth: Smooth scaling
        :return: Self reference
        """
        assert isinstance(width, NumberInstance)
        assert isinstance(height, NumberInstance)
        assert isinstance(smooth, bool)
        assert width > 0 and height > 0, \
            'width and height must be greater than zero'
        w, h = self.get_size()
        if w == width and h == height:
            return self
        return self.scale(width=float(width) / w, height=float(height) / h, smooth=smooth)

    def get_rect(self) -> 'pygame.Rect':
        """
        Return the :py:class:`pygame.Rect` object of the BaseImage.

        This method returns a new rectangle covering the entire surface. The
        rectangle will always start at *(0, 0)* with a same width and height size
        as the image.

        :return: Pygame rect object
        """
        return self._surface.get_rect()

    def rotate(self, angle: NumberType, auto_checkpoint: bool = True) -> 'BaseImage':
        """
        Unfiltered counterclockwise rotation. The angle argument represents degrees
        and can be any floating point value. Negative angle amounts will rotate
        clockwise.

        .. note::

            Unless rotating by 90 degree increments, the image will be padded
            larger to hold the new size. If the image has pixel alphas, the padded
            area will be transparent. Otherwise, pygame will pick a color that matches
            the image color-key or the topleft pixel value.

        .. warning::

            Image should be rotated once. If this method is called once the Class
            rotates the previously check-pointed state. If you wish to rotate the
            current image use ``checkpoint`` to update the surface. This may
            increase the image size, because the bounding rectangle of a rotated
            image is always greater than the bounding rectangle of the original
            image (except some rotations by multiples of 90 degrees). The image
            gets distort because of the multiply copies. Each rotation generates
            a small error (inaccuracy). The sum of the errors is growing and the
            images decays.

        :param angle: Rotation angle (degrees ``0-360``)
        :param auto_checkpoint: Checkpoint after first rotation to avoid rotating the same image. If multiple rotations are applied to the same surface it will increase its size very fast because of inaccuracies
        :return: Self reference
        """
        assert isinstance(angle, NumberInstance)
        if angle == self._angle:
            return self
        if not self._rotated and auto_checkpoint:
            self.checkpoint()
        if self._rotated:
            self.restore()
        self._rotated = True
        self._surface = pygame.transform.rotate(self._surface, angle)
        self._angle = angle % 360
        return self

    def get_angle(self) -> NumberType:
        """
        Return the image angle.

        :return: Angle in degrees
        """
        return self._angle

    def _get_position_delta(self) -> Tuple2IntType:
        """
        Return the delta from drawing position.

        :return: Delta positions on x-axis and y-axis (x, y) in px
        """
        rect = self.get_rect()
        if self._drawing_position == POSITION_NORTHWEST:
            return rect.topleft
        elif self._drawing_position == POSITION_NORTH:
            return rect.midtop
        elif self._drawing_position == POSITION_NORTHEAST:
            return rect.topright
        elif self._drawing_position == POSITION_WEST:
            return rect.midleft
        elif self._drawing_position == POSITION_CENTER:
            return rect.center
        elif self._drawing_position == POSITION_EAST:
            return rect.midright
        elif self._drawing_position == POSITION_SOUTHWEST:
            return rect.bottomleft
        elif self._drawing_position == POSITION_SOUTH:
            return rect.midbottom
        elif self._drawing_position == POSITION_SOUTHEAST:
            return rect.bottomright
        else:
            raise ValueError('unknown drawing position')

    def draw(
            self,
            surface: 'pygame.Surface',
            area: Optional['pygame.Rect'] = None,
            position: Tuple2IntType = (0, 0)
    ) -> 'BaseImage':
        """
        Draw the image in a given surface.

        :param surface: Pygame surface object
        :param area: Area to draw; if ``None`` the image will be drawn on entire surface
        :param position: Position to draw on x-axis and y-axis (x, y) in px
        :return: Self reference
        """
        assert isinstance(surface, pygame.Surface)
        assert isinstance(area, (pygame.Rect, type(None)))
        assert_vector(position, 2, int)

        if area is None:
            area = surface.get_rect()

        # Compute offset based on drawing offset + drawing position
        px, py = self._get_position_delta()
        if self._drawing_mode != IMAGE_MODE_SIMPLE:
            px = 0
            py = 0

        offx = self._drawing_offset[0] - px
        offy = self._drawing_offset[1] - py

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
                    offx + position[0],
                    offy + position[1]
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
                        x * w + offx + position[0],
                        offy + position[1]
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
                        0 + offx + position[0],
                        y * h + offy + position[1]
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
                            x * w + offx + position[0],
                            y * h + offy + position[1]
                        ),
                        area
                    )

        elif self._drawing_mode == IMAGE_MODE_CENTER:
            sw, hw = area.width, area.height  # Window
            w, h = self._surface.get_size()  # Image
            surface.blit(
                self._surface,
                (
                    int(float(sw - w) / 2 + offx + position[0]),
                    int(float(hw - h) / 2 + offy + position[1])
                ),
                area
            )

        elif self._drawing_mode == IMAGE_MODE_SIMPLE:
            surface.blit(
                self._surface,
                (
                    offx + position[0],
                    offy + position[1]
                ),
                area
            )

        return self
