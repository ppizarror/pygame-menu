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

    # Methods
    'assert_alignment',
    'assert_color',
    'assert_cursor',
    'assert_list_vector',
    'assert_orientation',
    'assert_position',
    'assert_vector',
    'check_key_pressed_valid',
    'format_color',
    'is_callable',
    'make_surface',
    'parse_padding',
    'uuid4',
    'widget_terminal_title',

    # Classes
    'TerminalColors',

]

import functools
import types
import uuid
import warnings

import pygame
import pygame_menu
import pygame_menu.locals as _locals

from pygame_menu._types import ColorType, ColorInputType, Union, List, Vector2NumberType, NumberType, Any, \
    Optional, Tuple, NumberInstance, VectorInstance, PaddingInstance, PaddingType, Tuple4IntType, \
    ColorInputInstance, VectorType, EventType

PYGAME_V2 = pygame.version.vernum[0] >= 2


def assert_alignment(align: str) -> None:
    """
    Assert that a certain alignment is valid.

    :param align: Align value
    :return: None
    """
    assert isinstance(align, str), 'alignment "{0}" must be a string'.format(align)
    assert align in (_locals.ALIGN_LEFT, _locals.ALIGN_CENTER, _locals.ALIGN_RIGHT), \
        'incorrect alignment value "{0}"'.format(align)


def assert_color(color: Union[ColorInputType, List[int]]) -> ColorType:
    """
    Assert that a certain color is valid.

    :param color: Object color
    :return: Formatted color if valid, else, throws an ``AssertionError`` exception
    """
    color = format_color(color)
    assert isinstance(color, VectorInstance), \
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
    return color


def assert_cursor(cursor: Optional[Union[int, 'pygame.cursors.Cursor']]) -> None:
    """
    Assert a given cursor is valid.

    :param cursor: Cursor object
    :return: None
    """
    if hasattr(pygame.cursors, 'Cursor'):
        assert isinstance(cursor, (int, type(pygame.cursors.Cursor), type(None)))
    else:
        assert isinstance(cursor, (int, type(None)))


def assert_list_vector(list_vector: Union[List[Vector2NumberType], Tuple[Vector2NumberType, ...]],
                       length: int) -> None:
    """
    Assert that a list fixed length vector is numeric.

    :param list_vector: Numeric list vector
    :param length: Length of the required vector. If ``0`` don't check the length
    :return: None
    """
    assert isinstance(list_vector, (tuple, list))
    for v in list_vector:
        assert_vector(v, length)


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


def assert_vector(num_vector: VectorType, length: int, instance: type = NumberInstance) -> None:
    """
    Assert that a fixed length vector is numeric.

    :param num_vector: Numeric vector
    :param length: Length of the required vector. If ``0`` don't check the length
    :param instance: Instance of each item of the vector
    :return: None
    """
    assert isinstance(num_vector, VectorInstance), \
        'vector "{0}" must be a list or tuple of {1} items if type {2}'.format(num_vector, length, instance)
    if length != 0:
        msg = 'vector "{0}" must contain {1} numbers only, ' \
              'but {2} were given'.format(num_vector, length, len(num_vector))
        assert len(num_vector) == length, msg
    for i in range(len(num_vector)):
        num = num_vector[i]
        if instance == int and isinstance(num, float) and int(num) == num:
            num = int(num)
        assert isinstance(num, instance), \
            'item {0} of vector must be {1}, not type "{2}"'.format(num, instance, type(num))


def check_key_pressed_valid(event: EventType) -> bool:
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


def format_color(color: Union[ColorInputType, Any]) -> Union[ColorType, Any]:
    """
    Format color from string, int, or tuple to tuple type.

    Available formats:
    - Color name str: name of the color to use, e.g. ``"red"`` (all the supported name strings can be found in the colordict module, see https://github.com/pygame/pygame/blob/main/src_py/colordict.py)
    - HTML color format str: ``"#rrggbbaa"`` or ``"#rrggbb"``, where rr, gg, bb, and aa are 2-digit hex numbers in the range of ``0`` to ``0xFF`` inclusive, the aa (alpha) value defaults to ``0xFF`` if not provided
    - Hex number str: ``"0xrrggbbaa"`` or ``"0xrrggbb"``, where rr, gg, bb, and aa are 2-digit hex numbers in the range of ``0x00`` to ``0xFF`` inclusive, the aa (alpha) value defaults to ``0xFF`` if not provided
    - int: int value of the color to use, using hex numbers can make this parameter more readable, e.g. ``0xrrggbbaa``, where rr, gg, bb, and aa are 2-digit hex numbers in the range of ``0x00`` to ``0xFF`` inclusive, note that the aa (alpha) value is not optional for the int format and must be provided
    - tuple/list of int color values: ``(R, G, B, A)`` or ``(R, G, B)``, where R, G, B, and A are int values in the range of ``0`` to ``255`` inclusive, the A (alpha) value defaults to ``255`` (opaque) if not provided

    :param color: Color to format. If format is valid returns the same input value
    :return: Color in (r, g, b, a) format
    """
    if not isinstance(color, ColorInputInstance):
        return color
    if not isinstance(color, pygame.Color):
        try:
            if isinstance(color, (tuple, list)) and 3 <= len(color) <= 4:
                if PYGAME_V2:
                    for j in color:
                        if not isinstance(j, int):
                            raise ValueError('color cannot contain floating point values')
                c = pygame.Color(*color)
            else:
                c = pygame.Color(color)
        except ValueError:
            warnings.warn('invalid color value "{0}"'.format(color))
            return color
    else:
        c = color
    return c.r, c.g, c.b, c.a


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
                 alpha: bool = False, fill_color: Optional[ColorInputType] = None) -> 'pygame.Surface':
    """
    Creates a pygame surface object.

    :param width: Surface width
    :param height: Surface height
    :param alpha: Enable alpha channel on surface
    :param fill_color: Fill surface with a certain color
    :return: Pygame surface
    """
    assert isinstance(width, NumberInstance)
    assert isinstance(height, NumberInstance)
    assert isinstance(alpha, bool)
    assert width >= 0 and height >= 0, \
        'surface width and height must be equal or greater than zero'
    surface = pygame.Surface((int(width), int(height)), pygame.SRCALPHA, 32)  # lgtm [py/call/wrong-arguments]
    if alpha:
        # noinspection PyArgumentList
        surface = pygame.Surface.convert_alpha(surface)
    if fill_color is not None:
        fill_color = assert_color(fill_color)
        surface.fill(fill_color)
    return surface


def parse_padding(padding: PaddingType) -> Tuple4IntType:
    """
    Get the padding value from tuple.

    - If an integer or float is provided: top, right, bottom and left values will be the same
    - If 2-item tuple is provided: top and bottom takes the first value, left and right the second
    - If 3-item tuple is provided: top will take the first value, left and right the second, and bottom the third
    - If 4-item tuple is provided: padding will be (top, right, bottom, left)

    .. note::

        See `CSS W3Schools <https://www.w3schools.com/css/css_padding.asp>`_ for more info about padding.

    :param padding: Can be a single number, or a tuple of 2, 3 or 4 elements following CSS style
    :return: Padding value, (top, right, bottom, left), in px
    """
    assert isinstance(padding, PaddingInstance)

    if isinstance(padding, NumberInstance):
        assert padding >= 0, 'padding cannot be a negative number'
        return padding, padding, padding, padding
    else:
        assert 1 <= len(padding) <= 4, 'padding must be a tuple of 2, 3 or 4 elements'
        for i in range(len(padding)):
            assert isinstance(padding[i], NumberInstance), 'all padding elements must be integers or floats'
            assert padding[i] >= 0, 'all padding elements must be equal or greater than zero'
        if len(padding) == 1:
            return padding[0], padding[0], padding[0], padding[0]
        elif len(padding) == 2:
            return padding[0], padding[1], padding[0], padding[1]
        elif len(padding) == 3:
            return padding[0], padding[1], padding[2], padding[1]
        else:
            return padding[0], padding[1], padding[2], padding[3]


def uuid4() -> str:
    """
    Create custom version of uuid4.

    :return: UUID of 18 chars
    """
    return str(uuid.uuid4())[:18]


def widget_terminal_title(
        widget: 'pygame_menu.widgets.Widget',
        widget_indx: int = -1,
        current_index: int = -1
) -> str:
    """
    Return widget title to be printed on terminals.

    :param widget: Widget to get title from
    :param widget_indx: Widget index
    :param current_index: Menu index
    :return: Widget title
    """
    wclassid = TerminalColors.BOLD + widget.get_class_id() + TerminalColors.ENDC
    if isinstance(widget, pygame_menu.widgets.Frame):
        wtitle = TerminalColors.BRIGHT_WHITE + '┌━' + TerminalColors.ENDC
        wtitle += '{0} - {3}[{1},{2},'.format(wclassid, *widget.get_indices(), TerminalColors.LGREEN)
        if widget.horizontal:
            wtitle += 'H] '
        else:
            wtitle += 'V] '
        if widget.is_scrollable:
            wsz = widget.get_inner_size()
            wsm = widget.get_max_size()
            wsh = wsm[0] if wsm[0] == wsz[0] else '{0}→{1}'.format(wsm[0], wsz[0])
            wsv = wsm[1] if wsm[1] == wsz[1] else '{0}→{1}'.format(wsm[1], wsz[1])
            wtitle += '∑ [{0},{1}] '.format(wsh, wsv)
        wtitle += TerminalColors.ENDC
    else:
        if widget.get_title() != '':
            wtitle = '{0} - {1} - '.format(wclassid,
                                           TerminalColors.UNDERLINE + widget.get_title() + TerminalColors.ENDC)
        else:
            wtitle = wclassid

    # Column/Row position
    wtitle += TerminalColors.INDIGO
    cr = widget.get_col_row_index()
    wtitle += '{' + str(cr[0]) + ',' + str(cr[1]) + '}'
    wtitle += TerminalColors.ENDC

    # Add position
    wtitle += TerminalColors.MAGENTA
    wtitle += ' ({0},{1})'.format(*widget.get_position())
    wtitle += TerminalColors.ENDC

    # Add mods
    wtitle += TerminalColors.CYAN
    if widget.is_floating():
        wtitle += ' Φ'
    if not widget.is_visible():
        wtitle += ' ╳'
    if not widget.is_selectable:
        wtitle += ' β'
    if widget.is_selected():
        wtitle += TerminalColors.BOLD + ' ⟵'
        if current_index != -1 and current_index != widget_indx:
            wtitle += '! [{0}->{1}]'.format(widget_indx, current_index)
    if widget.get_menu() is None:
        wtitle += ' !▲'
    wtitle += TerminalColors.ENDC

    return wtitle


class TerminalColors(object):
    """
    Terminal colors.

    See https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html.
    """
    BOLD = '\033[1m'
    BRIGHT_MAGENTA = '\u001b[35;1m'
    BRIGHT_WHITE = '\u001b[37;1m'
    CYAN = '\u001b[36m'
    ENDC = '\u001b[0m'
    GRAY = '\u001b[30;1m'
    INDIGO = '\u001b[38;5;129m'
    LGREEN = '\u001b[38;5;150m'
    MAGENTA = '\u001b[35m'
    RED = '\u001b[31m'
    UNDERLINE = '\033[4m'
