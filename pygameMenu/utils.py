# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

UTILS
Utilitary functions.

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

import pygame as _pygame
import pygameMenu.locals as _locals


def assert_alignment(align):
    """
    Assert alignment local.

    :param align: Align value
    :type align: basestring
    """
    assert isinstance(align, str), 'alignment "{0}" must be a string'.format(align)
    assert align in [_locals.ALIGN_LEFT,
                     _locals.ALIGN_CENTER,
                     _locals.ALIGN_RIGHT,
                     _locals.ALIGN_TOP,
                     _locals.ALIGN_BOTTOM], \
        'incorrect alignment value "{0}"'.format(align)


def assert_color(color):
    """
    Assert that a certain color is valid.

    :param color: Object color
    """
    assert isinstance(color, (list, tuple))
    assert len(color) == 3, 'color must be a tuple or list of 3 numbers'
    for i in color:
        assert isinstance(i, int), '"{0}" in element color {1} must be an integer'.format(i, color)


def assert_position(position):
    """
    Assert that a certain widget position is valid.

    :param position: Object position
    :type position: basestring
    """
    assert isinstance(position, str)
    assert position in [_locals.POSITION_WEST, _locals.POSITION_SOUTHWEST,
                        _locals.POSITION_SOUTH, _locals.POSITION_SOUTHEAST,
                        _locals.POSITION_EAST, _locals.POSITION_NORTH,
                        _locals.POSITION_NORTHWEST, _locals.POSITION_NORTHEAST], \
        'invalid position value "{0}"'.format(position)


def check_key_pressed_valid(event):
    """
    Checks if the pressed key is valid.
    :param event: Key press event
    :type event: pygame.event.EventType
    :return: True if a key is pressed
    :rtype: bool
    """
    # If the system detects that any key event has been pressed but
    # there's not any key pressed then this method raises a KEYUP
    # flag
    bad_event = not (True in _pygame.key.get_pressed())
    if bad_event:
        if 'test' in event.dict and event.dict['test']:
            return True
        ev = _pygame.event.Event(_pygame.KEYUP, {'key': event.key})
        _pygame.event.post(ev)
    return not bad_event


def dummy_function():
    """
    Dummy function, this can be archieved with lambda but it's against
    PEP-8.

    :return: None
    """
    return


def make_surface(width, height, alpha=False):
    """
    Creates a pygame surface object.

    :param width: Surface width
    :type width: int, float
    :param height: Surface height
    :type height: int, float
    :param alpha: Enable alpha channel on surface
    :type alpha: bool
    :return: Pygame surface
    :rtype: _pygame.Surface
    """
    assert width > 0 and height > 0, 'surface width and height must be greater than zero'
    assert isinstance(alpha, bool)
    surface = _pygame.Surface((width, height), _pygame.SRCALPHA, 32)  # lgtm [py/call/wrong-arguments]
    if alpha:
        surface = _pygame.Surface.convert_alpha(surface)
    return surface
