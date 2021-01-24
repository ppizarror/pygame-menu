"""
pygame-menu
https://github.com/ppizarror/pygame-menu

UTILS
Utility functions.

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

__all__ = [

    'assert_alignment',
    'assert_color',
    'assert_list_vector',
    'assert_orientation',
    'assert_position',
    'assert_vector',
    'check_key_pressed_valid',
    'is_callable',
    'make_surface'

]

import types
import functools

import pygame
import pygame_menu.locals as _locals
from pygame_menu._custom_types import ColorType, Union, List, Vector2NumberType, NumberType, Any, \
    Optional, Tuple


def assert_alignment(align: str) -> None:
    """
    Assert that a certain alignment is valid.

    :param align: Align value
    :return: None
    """
    assert isinstance(align, str), 'alignment "{0}" must be a string'.format(align)
    assert align in (_locals.ALIGN_LEFT, _locals.ALIGN_CENTER, _locals.ALIGN_RIGHT), \
        'incorrect alignment value "{0}"'.format(align)


def assert_color(color: Union[ColorType, List[int]]) -> None:
    """
    Assert that a certain color is valid.

    :param color: Object color
    :return: None
    """
    assert isinstance(color, (tuple, list)), \
        'color must be a tuple or list, not type "{0}"'.format(type(color))
    assert 4 >= len(color) >= 3, \
        'color must be a tuple or list of 3 or 4 numbers'
    for i in range(3):
        assert isinstance(color[i], int), \
            '"{0}" in element color {1} must be an integer, not type "{2}"'.format(color[i], color, type(color))
        assert 0 <= color[i] <= 255, \
            '"{0}" in element color {1} must be an integer between 0 and 255'.format(color[i], color)
    if len(color) == 4:
        assert isinstance(color[3], int), \
            'alpha channel must be an integer between 0 and 255, not type "{0}"'.format(type(color))
        assert 0 <= color[3] <= 255, \
            'opacity of color {0} must be an integer between 0 and 255; where ' \
            '0 is fully-transparent and 255 is fully-opaque'.format(color)


def assert_orientation(orientation: str) -> None:
    """
    Assert that a certain widget orientation is valid.

    :param orientation: Object orientation
    :return: None
    """
    assert isinstance(orientation, str), 'orientation must be a string'
    assert orientation in [_locals.ORIENTATION_HORIZONTAL, _locals.ORIENTATION_VERTICAL], \
        'invalid orientation value "{0}"'.format(orientation)


def assert_position(position: str) -> None:
    """
    Assert that a certain position is valid.

    :param position: Object position
    :return: None
    """
    assert isinstance(position, str), 'position must be a string'
    assert position in [_locals.POSITION_WEST, _locals.POSITION_SOUTHWEST,
                        _locals.POSITION_SOUTH, _locals.POSITION_SOUTHEAST,
                        _locals.POSITION_EAST, _locals.POSITION_NORTH,
                        _locals.POSITION_NORTHWEST, _locals.POSITION_NORTHEAST,
                        _locals.POSITION_CENTER], \
        'invalid position value "{0}"'.format(position)


def assert_list_vector(list_vector: Union[List[Vector2NumberType], Tuple[Vector2NumberType, ...]],
                       length: int) -> None:
    """
    Assert that a list fixed length vector is numeric.

    :param list_vector: Numeric list vector
    :param length: Length of the required vector. If ``0`` don't check the length
    :return: None
    """
    assert isinstance(list_vector, (list, tuple))
    for v in list_vector:
        assert_vector(v, length=length)


def assert_vector(num_vector: Vector2NumberType, length: int) -> None:
    """
    Assert that a fixed length vector is numeric.

    :param num_vector: Numeric vector
    :param length: Length of the required vector. If ``0`` don't check the length
    :return: None
    """
    assert isinstance(num_vector, (tuple, list)), \
        'vector "{0}" must be a list or tuple of {1} items'.format(num_vector, length)
    if length != 0:
        msg = 'vector "{0}" must contain {1} numbers only, ' \
              'but {2} were given'.format(num_vector, length, len(num_vector))
        assert len(num_vector) == length, msg
    for i in range(len(num_vector)):
        assert isinstance(num_vector[i], (int, float)), \
            'item {0} of vector must be integer or float, not type "{1}"'.format(num_vector[i], type(num_vector[i]))


def check_key_pressed_valid(event: 'pygame.event.Event') -> bool:
    """
    Checks if the pressed key is valid.

    :param event: Key press event
    :return: ``True`` if a key is pressed
    """
    # If the system detects that any key event has been pressed but
    # there's not any key pressed then this method raises a KEYUP
    # flag
    bad_event = not (True in pygame.key.get_pressed())
    if bad_event:
        if 'test' in event.dict and event.dict['test']:
            return True
        ev = pygame.event.Event(pygame.KEYUP, {'key': event.key})
        pygame.event.post(ev)
    return not bad_event


def is_callable(func: Any) -> bool:
    """
    Return ``True`` if ``func`` is callable.

    :param func: Function object
    :return: ``True`` if function
    """
    # noinspection PyTypeChecker
    return isinstance(func, (types.FunctionType, types.BuiltinFunctionType,
                             types.MethodType, functools.partial))


def make_surface(width: NumberType, height: NumberType,
                 alpha: bool = False, fill_color: Optional[ColorType] = None) -> 'pygame.Surface':
    """
    Creates a pygame surface object.

    :param width: Surface width
    :param height: Surface height
    :param alpha: Enable alpha channel on surface
    :param fill_color: Fill surface with a certain color
    :return: Pygame surface
    """
    assert isinstance(width, (int, float))
    assert isinstance(height, (int, float))
    assert isinstance(alpha, bool)
    assert isinstance(fill_color, (type(None), tuple))
    assert width >= 0 and height >= 0, \
        'surface width and height must be equal or greater than zero'
    surface = pygame.Surface((int(width), int(height)), pygame.SRCALPHA, 32)  # lgtm [py/call/wrong-arguments]
    if alpha:
        # noinspection PyArgumentList
        surface = pygame.Surface.convert_alpha(surface)
    if fill_color is not None:
        assert_color(fill_color)
        surface.fill(fill_color)
    return surface
