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


def make_surface(width, height, alpha=False):
    """
    Creates a pygame surface object.

    :param width: Surface width
    :type width: int
    :param height: Surface height
    :type height: int
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
