"""
pygame-menu
https://github.com/ppizarror/pygame-menu

UTILS
Utility functions.
"""

__all__ = [

    # Methods
    'assert_alignment',
    'assert_color',
    'assert_cursor',
    'assert_list_vector',
    'assert_orientation',
    'assert_position',
    'assert_position_vector',
    'assert_vector',
    'check_key_pressed_valid',
    'fill_gradient',
    'format_color',
    'get_cursor',
    'get_finger_pos',
    'is_callable',
    'load_pygame_image_file',
    'make_surface',
    'mouse_motion_current_mouse_position',
    'parse_padding',
    'print_menu_widget_structure',
    'set_pygame_cursor',
    'uuid4',
    'warn',
    'widget_terminal_title',

    # Constants
    'PYGAME_V2',

    # Classes
    'ShadowGenerator',
    'TerminalColors'

]

import functools
import sys
import traceback
import types
import uuid
import warnings

import pygame
import pygame_menu

from pygame_menu.locals import ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT, POSITION_CENTER, \
    POSITION_NORTH, POSITION_SOUTH, POSITION_SOUTHEAST, POSITION_NORTHWEST, \
    POSITION_WEST, POSITION_EAST, POSITION_NORTHEAST, POSITION_SOUTHWEST, \
    ORIENTATION_HORIZONTAL, ORIENTATION_VERTICAL, FINGERDOWN, FINGERUP, FINGERMOTION

from pygame_menu._types import ColorType, ColorInputType, Union, List, Vector2NumberType, \
    NumberType, Any, Optional, Tuple, NumberInstance, VectorInstance, PaddingInstance, \
    PaddingType, Tuple4IntType, ColorInputInstance, VectorType, EventType, \
    CursorInputInstance, CursorInputType, Tuple2IntType, Dict, Tuple3IntType

PYGAME_V2 = pygame.version.vernum[0] >= 2
WARNINGS_LAST_MESSAGES: Dict[int, bool] = {}


def assert_alignment(align: str) -> None:
    """
    Assert that a certain alignment is valid.

    :param align: Align value
    :return: None
    """
    assert isinstance(align, str), f'alignment "{align}" must be a string'
    assert align in (ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT), \
        f'incorrect alignment value "{align}"'


def assert_color(
        color: Union[ColorInputType, List[int]],
        warn_if_invalid: bool = True
) -> ColorType:
    """
    Assert that a certain color is valid.

    :param color: Object color
    :param warn_if_invalid: If ``True`` warns if the color is invalid
    :return: Formatted color if valid, else, throws an ``AssertionError`` exception
    """
    color = format_color(color, warn_if_invalid=warn_if_invalid)
    assert isinstance(color, VectorInstance), \
        f'color must be a tuple or list, not type "{type(color)}"'
    assert 4 >= len(color) >= 3, \
        'color must be a tuple or list of 3 or 4 numbers'
    for i in range(3):
        assert isinstance(color[i], int), \
            f'"{color[i]}" in element color {color} must be an integer, not type "{type(color)}"'
        assert 0 <= color[i] <= 255, \
            f'"{color[i]}" in element color {color} must be an integer between 0 and 255'
    if len(color) == 4:
        assert isinstance(color[3], int), \
            f'alpha channel must be an integer between 0 and 255, not type "{type(color)}"'
        assert 0 <= color[3] <= 255, \
            f'opacity of color {color} must be an integer between 0 and 255; ' \
            f'where 0 is fully-transparent and 255 is fully-opaque'
    return color


def assert_cursor(cursor: CursorInputType) -> None:
    """
    Assert a given cursor is valid.

    :param cursor: Cursor object
    :return: None
    """
    assert isinstance(cursor, CursorInputInstance), \
        'cursor instance invalid, it can be None, an integer, ' \
        'or pygame.cursors.Cursor'


def assert_list_vector(list_vector: Union[List[Vector2NumberType], Tuple[Vector2NumberType, ...]],
                       length: int) -> None:
    """
    Assert that a list fixed length vector is numeric.

    :param list_vector: Numeric list vector
    :param length: Length of the required vector. If ``0`` don't check the length
    :return: None
    """
    assert isinstance(list_vector, VectorInstance), \
        f'list_vector "{list_vector}" must be a tuple or list'
    for v in list_vector:
        assert_vector(v, length)


def assert_orientation(orientation: str) -> None:
    """
    Assert that a certain widget orientation is valid.

    :param orientation: Object orientation
    :return: None
    """
    assert isinstance(orientation, str), \
        f'orientation "{orientation}" must be a string'
    assert orientation in (ORIENTATION_HORIZONTAL, ORIENTATION_VERTICAL), \
        f'invalid orientation value "{orientation}"'


def assert_position(position: str) -> None:
    """
    Assert that a certain position is valid.

    :param position: Object position
    :return: None
    """
    assert isinstance(position, str), \
        f'position "{position}" must be a string'
    assert position in (POSITION_WEST, POSITION_SOUTHWEST, POSITION_SOUTH,
                        POSITION_SOUTHEAST, POSITION_EAST, POSITION_NORTH,
                        POSITION_NORTHWEST, POSITION_NORTHEAST, POSITION_CENTER), \
        f'invalid position value "{position}"'


def assert_position_vector(position: Union[str, List[str], Tuple[str, ...]]) -> None:
    """
    Assert that a position vector is valid.

    :param position: Object position
    :return: None
    """
    if isinstance(position, str):
        assert_position(position)
    else:
        assert isinstance(position, VectorInstance)
        unique = []
        for pos in position:
            assert_position(pos)
            if pos not in unique:
                unique.append(pos)
        assert len(unique) == len(position), 'there cannot be repeated positions'


def assert_vector(
        num_vector: VectorType,
        length: int,
        instance: type = NumberInstance
) -> None:
    """
    Assert that a fixed length vector is numeric.

    :param num_vector: Numeric vector
    :param length: Length of the required vector. If ``0`` don't check the length
    :param instance: Instance of each item of the vector
    :return: None
    """
    assert isinstance(num_vector, VectorInstance), \
        f'vector "{num_vector}" must be a list or tuple of {length} items if type {instance}'
    if length != 0:
        assert len(num_vector) == length, \
            f'vector "{num_vector}" must contain {length} numbers only, ' \
            f'but {num_vector} were given'
    for i in range(len(num_vector)):
        num = num_vector[i]
        if instance == int and isinstance(num, float) and int(num) == num:
            num = int(num)
        assert isinstance(num, instance), \
            f'item {num} of vector must be {instance}, not type "{type(num)}"'


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


def fill_gradient(
        surface: 'pygame.Surface',
        color: ColorInputType,
        gradient: ColorInputType,
        rect: Optional['pygame.Rect'] = None,
        vertical: bool = True,
        forward: bool = True
) -> None:
    """
    Fill a surface with a gradient pattern.

    :param surface: Surface to fill
    :param color: Starting color
    :param gradient: Final color
    :param rect: Area to fill; default is surface's rect
    :param vertical: True=vertical; False=horizontal
    :param forward: True=forward; False=reverse
    :return: None
    """
    if rect is None:
        rect = surface.get_rect()
    x1, x2 = rect.left, rect.right
    y1, y2 = rect.top, rect.bottom
    color = assert_color(color)
    gradient = assert_color(gradient)
    if vertical:
        h = y2 - y1
    else:
        h = x2 - x1
    if forward:
        a, b = color, gradient
    else:
        b, a = color, gradient
    rate = (
        float(b[0] - a[0]) / h,
        float(b[1] - a[1]) / h,
        float(b[2] - a[2]) / h
    )
    fn_line = pygame.draw.line
    if vertical:
        for line in range(y1, y2):
            color = (
                min(max(a[0] + (rate[0] * (line - y1)), 0), 255),
                min(max(a[1] + (rate[1] * (line - y1)), 0), 255),
                min(max(a[2] + (rate[2] * (line - y1)), 0), 255)
            )
            fn_line(surface, color, (x1, line), (x2, line))
    else:
        for col in range(x1, x2):
            color = (
                min(max(a[0] + (rate[0] * (col - x1)), 0), 255),
                min(max(a[1] + (rate[1] * (col - x1)), 0), 255),
                min(max(a[2] + (rate[2] * (col - x1)), 0), 255)
            )
            fn_line(surface, color, (col, y1), (col, y2))


def format_color(
        color: Union[ColorInputType, Any],
        warn_if_invalid: bool = True
) -> Union[ColorType, Any]:
    """
    Format color from string, int, or tuple to tuple type.

    Available formats:
    - Color name str: name of the color to use, e.g. ``"red"`` (all the supported name strings can be found in the colordict module, see https://github.com/pygame/pygame/blob/main/src_py/colordict.py)
    - HTML color format str: ``"#rrggbbaa"`` or ``"#rrggbb"``, where rr, gg, bb, and aa are 2-digit hex numbers in the range of ``0`` to ``0xFF`` inclusive, the aa (alpha) value defaults to ``0xFF`` if not provided
    - Hex number str: ``"0xrrggbbaa"`` or ``"0xrrggbb"``, where rr, gg, bb, and aa are 2-digit hex numbers in the range of ``0x00`` to ``0xFF`` inclusive, the aa (alpha) value defaults to ``0xFF`` if not provided
    - int: int value of the color to use, using hex numbers can make this parameter more readable, e.g. ``0xrrggbbaa``, where rr, gg, bb, and aa are 2-digit hex numbers in the range of ``0x00`` to ``0xFF`` inclusive, note that the aa (alpha) value is not optional for the int format and must be provided
    - tuple/list of int color values: ``(R, G, B, A)`` or ``(R, G, B)``, where R, G, B, and A are int values in the range of ``0`` to ``255`` inclusive, the A (alpha) value defaults to ``255`` (opaque) if not provided

    :param color: Color to format. If format is valid returns the same input value
    :param warn_if_invalid: If ``True`` warns if the color is invalid
    :return: Color in (r, g, b, a) format
    """
    if not isinstance(color, ColorInputInstance):
        return color
    if not isinstance(color, pygame.Color):
        if isinstance(color, str):
            if len(color) == 4 and color[0] == '#':
                r, g, b = color[1], color[2], color[3]
                color = f'#{r * 2}{g * 2}{b * 2}'
        try:
            if isinstance(color, VectorInstance) and 3 <= len(color) <= 4:
                if PYGAME_V2:
                    for j in color:
                        if not isinstance(j, int):
                            raise ValueError('color cannot contain floating point values')
                c = pygame.Color(*color)
            else:
                c = pygame.Color(color)
        except ValueError:
            if warn_if_invalid:
                warn(f'invalid color value "{color}"')
            else:
                raise
            return color
    else:
        c = color
    return c.r, c.g, c.b, c.a


def get_cursor() -> CursorInputType:
    """
    Return the pygame cursor object.

    :return: Cursor object
    """
    try:
        return pygame.mouse.get_cursor()
    except TypeError as e:
        warn(str(e))
    return None


def get_finger_pos(menu: 'pygame_menu.Menu', event: EventType) -> Tuple2IntType:
    """
    Return the position from finger (or mouse) event on x-axis and y-axis (x, y).

    :param menu: Menu object for relative positioning in finger events
    :param event: Pygame event object
    :return: Position on x-axis and y-axis (x, y) in px
    """
    if event.type in (FINGERDOWN, FINGERMOTION, FINGERUP):
        assert menu is not None, \
            'menu reference cannot be none while using finger position'
        display_size = menu.get_window_size()
        finger_pos = (int(event.x * display_size[0]), int(event.y * display_size[1]))
        return finger_pos
    return event.pos


def is_callable(func: Any) -> bool:
    """
    Return ``True`` if ``func`` is callable.

    :param func: Function object
    :return: ``True`` if function
    """
    # noinspection PyTypeChecker
    return isinstance(func, (types.FunctionType, types.BuiltinFunctionType,
                             types.MethodType, functools.partial))


def load_pygame_image_file(image_path: str, **kwargs) -> 'pygame.Surface':
    """
    Loads an image and returns a surface.

    :param image_path: Image file
    :param kwargs: Optional keyword arguments
    :return: Surface
    """
    # Try to load the image
    try:
        if 'test' in kwargs.keys():
            raise pygame.error('File is not a Windows BMP file')

        surface = pygame.image.load(image_path)

    except pygame.error as exc:
        # Check if file is not a windows file
        if str(exc) == 'File is not a Windows BMP file':
            pil_invalid_exception = Exception

            # Check if Pillow exists
            try:
                # noinspection PyPackageRequirements
                from PIL import Image, UnidentifiedImageError

                pil_invalid_exception = UnidentifiedImageError
                img_pil = Image.open(image_path)
                surface = pygame.image.fromstring(
                    img_pil.tobytes(), img_pil.size, img_pil.mode).convert()

            except (ModuleNotFoundError, ImportError):
                warn(f'Image file "{image_path}" could not be loaded, as pygame.error '
                     f'is raised. To avoid this issue install the Pillow library')
                raise

            except pil_invalid_exception:
                warn(f'The image "{image_path}" could not be loaded using Pillow')
                raise

        else:
            raise

    return surface


def make_surface(
        width: NumberType,
        height: NumberType,
        alpha: bool = False,
        fill_color: Optional[ColorInputType] = None
) -> 'pygame.Surface':
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


def mouse_motion_current_mouse_position() -> EventType:
    """
    Return a pygame event type MOUSEMOTION in the current mouse position.

    :return: Event
    """
    x, y = pygame.mouse.get_pos()
    return pygame.event.Event(pygame.MOUSEMOTION, {'pos': (int(x), int(y))})


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
    if padding is False or None:
        padding = 0
    assert isinstance(padding, PaddingInstance)

    if isinstance(padding, NumberInstance):
        assert padding >= 0, 'padding cannot be a negative number'
        return int(padding), int(padding), int(padding), int(padding)
    else:
        assert 1 <= len(padding) <= 4, 'padding must be a tuple of 2, 3 or 4 elements'
        for i in range(len(padding)):
            assert isinstance(padding[i], NumberInstance), \
                'all padding elements must be integers or floats'
            assert padding[i] >= 0, \
                'all padding elements must be equal or greater than zero'
        if len(padding) == 1:
            return int(padding[0]), int(padding[0]), int(padding[0]), int(padding[0])
        elif len(padding) == 2:
            return int(padding[0]), int(padding[1]), int(padding[0]), int(padding[1])
        elif len(padding) == 3:
            return int(padding[0]), int(padding[1]), int(padding[2]), int(padding[1])
        else:
            return int(padding[0]), int(padding[1]), int(padding[2]), int(padding[3])


def print_menu_widget_structure(
        widgets: List['pygame_menu.widgets.Widget'],
        index: int
) -> None:
    """
    Test printing widgets order.

    .. note::

        - Φ       Floating status
        - ⇇      Selected
        - !▲      Widget is not appended to current menu
        - ╳      Widget is hidden
        - ∑       Scrollable frame sizing
        - β       Widget is not selectable
        - {x,y}   Widget *column, row* position
        - <x,y>   Frame indices (min, max)

    :param widgets: Menu widgets list
    :param index: Menu index
    :return: None
    """
    indx = 0
    current_depth = 0
    depth_widths = {}
    c = TerminalColors

    def close_frames(depth: int) -> None:
        """
        Close frames up to current depth.

        :param depth: Depth to close
        :return: None
        """
        d = current_depth - depth
        for i in range(d):
            j = depth + d - (i + 1)  # Current depth
            line = f'·   {"│   " * j}└{"┄" * 3}'  # * depth_widths[j]
            print(c.BRIGHT_WHITE + line.ljust(0, '━') + c.ENDC)  # 80 also work

    non_menu_frame_widgets: Dict[int, List['pygame_menu.widgets.Widget']] = {}

    def process_non_menu_frame(w_indx: int) -> None:
        """
        Print non-menu frames list.

        :param w_indx: Current iteration index to print widgets
        :return: None
        """
        for nmi in list(non_menu_frame_widgets.keys()):
            if nmi == w_indx:
                v = non_menu_frame_widgets[nmi]
                for v_wid in v:
                    print(c.BRIGHT_WHITE + '·   ' + '│   ' * v_wid.get_frame_depth()
                          + c.ENDC + widget_terminal_title(v_wid))
                del non_menu_frame_widgets[nmi]

    for w in widgets:
        w_depth = w.get_frame_depth()
        close_frames(w.get_frame_depth())
        title = widget_terminal_title(w, indx, index)
        print('{0}{1}{2}'.format(
            str(indx).ljust(3),
            ' ' + c.BRIGHT_WHITE + '│   ' * w_depth + c.ENDC,
            title
        ))
        if w_depth not in depth_widths.keys():
            depth_widths[w_depth] = 0
        # depth_widths[w_depth] = max(int(len(title) * 1.2) + 3, depth_widths[w_depth])
        depth_widths[w_depth] = len(title) - 2
        current_depth = w.get_frame_depth()
        process_non_menu_frame(indx)
        jw = widgets[0]
        try:
            if isinstance(w, pygame_menu.widgets.Frame):  # Print ordered non-menu widgets
                current_depth += 1
                prev_indx = indx
                for jw in w.get_widgets(unpack_subframes=False):
                    if jw.get_menu() is None or jw not in widgets:
                        if prev_indx not in non_menu_frame_widgets.keys():
                            non_menu_frame_widgets[prev_indx] = []
                        non_menu_frame_widgets[prev_indx].append(jw)
                    else:
                        prev_indx = widgets.index(jw)
        except ValueError as e:
            print(f'[ERROR] while requesting widget {jw.get_class_id()}')
            warn(str(e))
        indx += 1
    process_non_menu_frame(indx)
    close_frames(0)


def set_pygame_cursor(cursor: CursorInputType) -> None:
    """
    Set pygame cursor.

    :param cursor: Cursor object
    :return: None
    """
    try:
        if cursor is not None:
            # noinspection PyArgumentList
            pygame.mouse.set_cursor(cursor)
    except (pygame.error, TypeError):
        if PYGAME_V2:
            warn(f'could not establish widget cursor, invalid value {cursor}')


def uuid4(short: bool = False) -> str:
    """
    Create custom version of uuid4.

    :param short: If ``True`` only returns the first 8 chars of the uuid, else, 18
    :return: UUID of 18 chars
    """
    return str(uuid.uuid4())[:18 if not short else 8]


def warn(message: str, print_stack: bool = True) -> None:
    """
    Warnings warn method.

    :param message: Message to warn about
    :param print_stack: Print stack trace of the call
    :return: None
    """
    assert isinstance(message, str)

    # noinspection PyUnresolvedReferences,PyProtectedMember
    frame = sys._getframe().f_back
    # frame_info = inspect.getframeinfo(frame)  # Traceback(filename, lineno, function, code_context, index)

    # Check if message in dict
    msg_hash = hash(message)
    msg_in_hash = False
    try:
        msg_in_hash = WARNINGS_LAST_MESSAGES[msg_hash]
    except KeyError:
        pass

    if not msg_in_hash and print_stack:
        traceback.print_stack(frame, limit=5)
        WARNINGS_LAST_MESSAGES[msg_hash] = True

    # warnings.showwarning(message, UserWarning, frame_info[0], frame_info[1])
    warnings.warn(message, stacklevel=2)


def widget_terminal_title(
        widget: 'pygame_menu.widgets.Widget',
        widget_index: int = -1,
        current_index: int = -1
) -> str:
    """
    Return widget title to be printed on terminals.

    :param widget: Widget to get title from
    :param widget_index: Widget index
    :param current_index: Menu index
    :return: Widget title
    """
    w_class_id = TerminalColors.BOLD + widget.get_class_id() + TerminalColors.ENDC
    if isinstance(widget, pygame_menu.widgets.Frame):
        w_title = TerminalColors.BRIGHT_WHITE + '┌━' + TerminalColors.ENDC
        w_title += f'{0} - {3}[{1},{2},'.format(w_class_id, *widget.get_indices(), TerminalColors.LGREEN)
        if widget.horizontal:
            w_title += 'H] '
        else:
            w_title += 'V] '
        if widget.is_scrollable:
            wsz = widget.get_inner_size()
            wsm = widget.get_max_size()
            wsh = wsm[0] if wsm[0] == wsz[0] else f'{wsm[0]}→{wsz[0]}'
            wsv = wsm[1] if wsm[1] == wsz[1] else f'{wsm[1]}→{wsz[1]}'
            w_title += f'∑ [{wsh},{wsv}] '
        w_title += TerminalColors.ENDC
    else:
        if widget.get_title() != '':
            title_f = TerminalColors.UNDERLINE + widget.get_title() + TerminalColors.ENDC
            w_title = f'{w_class_id} - {title_f} - '
        else:
            w_title = w_class_id + ' - '

    # Column/Row position
    w_title += TerminalColors.INDIGO
    cr = widget.get_col_row_index()
    w_title += '{' + str(cr[0]) + ',' + str(cr[1]) + '}'
    w_title += TerminalColors.ENDC

    # Add position
    w_title += TerminalColors.MAGENTA
    w_title += ' ({0},{1})'.format(*widget.get_position())
    w_title += TerminalColors.ENDC

    # Add size
    w_title += TerminalColors.BLUE
    w_title += ' ({0},{1})'.format(*widget.get_size())
    w_title += TerminalColors.ENDC

    # Add mods
    w_title += TerminalColors.CYAN
    if widget.is_floating():
        w_title += ' Φ'
    if not widget.is_visible():
        w_title += ' ╳'
    if not widget.is_selectable:
        w_title += ' β'
    if widget.is_selected():
        w_title += TerminalColors.BOLD + ' ⟵'
        if current_index != -1 and current_index != widget_index:
            w_title += f'! [{widget_index}->{current_index}]'
    if widget.get_menu() is None:
        w_title += ' !▲'
    w_title += TerminalColors.ENDC

    return w_title


class TerminalColors(object):
    """
    Terminal colors.

    See https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html.
    """
    BLUE = '\u001b[38;5;27m'
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


class ShadowGenerator(object):
    """
    A class to generate surfaces that work as a 'shadow' for rectangular UI elements. Base shadow
    surface are generated with an algorithm, then when one is requested at a specific size the
    closest pre-generated shadow surface is picked and then scaled to the exact size requested.

    By default it creates a four base shadows in a small range of sizes. If you find the shadow
    appearance unsatisfactory then it is possible to create more closer to the size of the
    elements you are having trouble with.

    Source: https://github.com/MyreMylar/pygame_gui with many edits.
    """

    _created_ellipse_shadows: Dict[str, 'pygame.Surface']
    _preloaded_shadow_corners: Dict[str, Dict[str, 'pygame.Surface']]
    _short_term_rect_cache: Dict[str, 'pygame.Surface']

    def __init__(self) -> None:
        self._created_ellipse_shadows = {}
        self._preloaded_shadow_corners = {}
        self._short_term_rect_cache = {}

    def clear_short_term_caches(self, force: bool = False) -> None:
        """
        Empties short term caches so we aren't hanging on to so many surfaces.

        :param force: Force clear
        """
        t = len(self._created_ellipse_shadows) + len(self._preloaded_shadow_corners) + \
            len(self._short_term_rect_cache)
        if t >= 100 or force:
            self._created_ellipse_shadows.clear()
            self._preloaded_shadow_corners.clear()
            self._short_term_rect_cache.clear()

    def _create_shadow_corners(
            self,
            shadow_width_param: int,
            corner_radius_param: int,
            color: Tuple3IntType,
            aa_amount: int = 4
    ) -> Dict[str, 'pygame.Surface']:
        """
        Create corners for our rectangular shadows. These can be used across many
        sizes of shadow with the same shadow width and corner radius.

        :param shadow_width_param: Width of the shadow
        :param corner_radius_param: Corner radius of the shadow
        :param color: Shadow color
        :param aa_amount: Anti-aliasing amount. Defaults to 4x
        :return: Dict that contain the shadows of each border
        """
        shadow_width_param = max(1, shadow_width_param)

        corner_rect = pygame.Rect(
            0, 0,
            corner_radius_param * aa_amount,
            corner_radius_param * aa_amount
        )

        corner_surface, edge_surface = self._create_single_corner_and_edge(
            aa_amount=aa_amount,
            corner_radius_param=corner_radius_param,
            corner_rect=corner_rect,
            shadow_width_param=shadow_width_param,
            color=color
        )

        sub_radius = ((corner_radius_param - shadow_width_param) * aa_amount)
        top_edge = pygame.transform.smoothscale(edge_surface,
                                                (shadow_width_param, shadow_width_param))
        left_edge = pygame.transform.rotate(top_edge, 90)

        tl_corner = pygame.transform.smoothscale(corner_surface,
                                                 (corner_radius_param,
                                                  corner_radius_param))

        if sub_radius > 0:
            corner_sub_surface = pygame.surface.Surface(corner_rect.size,
                                                        flags=pygame.SRCALPHA,
                                                        depth=32)
            corner_sub_surface.fill(pygame.Color('#00000000'))

            pygame.draw.circle(corner_sub_surface,
                               pygame.Color('#FFFFFFFF'),
                               corner_rect.size,
                               sub_radius)

            corner_small_sub_surface = pygame.transform.smoothscale(corner_sub_surface,
                                                                    (corner_radius_param,
                                                                     corner_radius_param))

            tl_corner.blit(corner_small_sub_surface,
                           (0, 0),
                           special_flags=pygame.BLEND_RGBA_SUB)

        corners_and_edges = {
            'bottom': pygame.transform.flip(top_edge, False, True),
            'bottom_left': pygame.transform.flip(tl_corner, False, True),
            'bottom_right': pygame.transform.flip(tl_corner, True, True),
            'left': left_edge,
            'right': pygame.transform.flip(left_edge, True, False),
            'top': top_edge,
            'top_left': tl_corner,
            'top_right': pygame.transform.flip(tl_corner, True, False)
        }
        self._preloaded_shadow_corners[(str(shadow_width_param) +
                                        'x' +
                                        str(corner_radius_param))] = corners_and_edges

        return corners_and_edges

    @staticmethod
    def _create_single_corner_and_edge(
            aa_amount: int,
            corner_radius_param: int,
            corner_rect: 'pygame.Rect',
            shadow_width_param: int,
            color: Tuple3IntType
    ) -> Tuple['pygame.Surface', 'pygame.Surface']:
        """
        Creates a single corner surface and a single edge surface for a shadow.

        :param aa_amount: Amount of anti-aliasing
        :param corner_radius_param: Radius of a corner this shadow will go around
        :param corner_rect: Rectangular size of corner
        :param shadow_width_param: Width of shadow
        :param color: Shadow color
        :return: A tuple of the corner surface and the edge surface
        """
        aa_amount = max(1, aa_amount)
        final_corner_surface = pygame.surface.Surface((corner_radius_param * aa_amount,
                                                       corner_radius_param * aa_amount),
                                                      flags=pygame.SRCALPHA, depth=32)
        final_corner_surface.fill(pygame.Color('#00000000'))
        final_edge_surface = pygame.surface.Surface((shadow_width_param * aa_amount,
                                                     shadow_width_param * aa_amount),
                                                    flags=pygame.SRCALPHA, depth=32)
        final_edge_surface.fill(pygame.Color('#00000000'))
        corner_radius = corner_radius_param * aa_amount
        corner_centre = (corner_radius, corner_radius)
        edge_rect = pygame.Rect(0, 0,
                                shadow_width_param * aa_amount,
                                shadow_width_param * aa_amount)
        edge_shadow_fade_height = edge_rect.width

        alpha_increment = 20.0 / (shadow_width_param ** 1.5)
        shadow_alpha = alpha_increment
        r, g, b = color
        for _ in range(shadow_width_param):
            if corner_rect.width > 0 and corner_rect.height > 0 and corner_radius > 0:
                # Edge
                edge_shadow_surface = pygame.surface.Surface(
                    edge_rect.size,
                    flags=pygame.SRCALPHA,
                    depth=32)
                edge_shadow_surface.fill(pygame.Color('#00000000'))
                edge_shadow_surface.fill(pygame.Color(r, g, b, int(shadow_alpha)),
                                         pygame.Rect(0,
                                                     edge_rect.height - edge_shadow_fade_height,
                                                     edge_rect.width,
                                                     edge_shadow_fade_height))

                final_edge_surface.blit(edge_shadow_surface,
                                        (0, 0),
                                        special_flags=pygame.BLEND_RGBA_ADD)

                # Corner
                corner_shadow_surface = pygame.surface.Surface(corner_rect.size,
                                                               flags=pygame.SRCALPHA,
                                                               depth=32)
                corner_shadow_surface.fill(pygame.Color('#00000000'))
                pygame.draw.circle(corner_shadow_surface,
                                   pygame.Color(r, g, b, int(shadow_alpha)),
                                   corner_centre,
                                   corner_radius)

                final_corner_surface.blit(corner_shadow_surface,
                                          (0, 0),
                                          special_flags=pygame.BLEND_RGBA_ADD)

                # increments/decrements
                shadow_alpha += alpha_increment
                corner_radius -= aa_amount
                edge_shadow_fade_height -= aa_amount
        return final_corner_surface, final_edge_surface

    def create_new_rectangle_shadow(
            self,
            width: int,
            height: int,
            shadow_width_param: int,
            corner_radius_param: int,
            aa_amount: int = 4,
            color: Tuple3IntType = (0, 0, 0)
    ) -> Optional['pygame.Surface']:
        """
        Creates a rectangular shadow surface at the specified size and stores it for later use.

        :param width: The width of the base shadow to create
        :param height: The height of the base shadow to create
        :param shadow_width_param: The width of the shadowed edge
        :param corner_radius_param: The radius of the rectangular shadow's corners
        :param aa_amount: Antialiasing
        :param color: Shadow color (r, g, b)
        return: Shadow
        """
        assert isinstance(width, int)
        assert isinstance(height, int)
        assert_vector(color, 3, int)
        shadow_width_param, corner_radius_param, aa_amount = int(shadow_width_param), \
                                                             int(corner_radius_param), int(aa_amount)
        if width < corner_radius_param or height < corner_radius_param or shadow_width_param == 0:
            return None
        r, g, b = color
        params = [width, height, shadow_width_param, corner_radius_param, aa_amount, r, g, b]
        shadow_id = '_'.join(str(param) for param in params)
        if shadow_id in self._short_term_rect_cache:
            return self._short_term_rect_cache[shadow_id]
        final_surface = pygame.surface.Surface((width, height), flags=pygame.SRCALPHA, depth=32)
        final_surface.fill(pygame.Color('#00000000'))

        corner_index_id = str(shadow_width_param) + 'x' + str(corner_radius_param)
        if corner_index_id in self._preloaded_shadow_corners:
            edges_and_corners = self._preloaded_shadow_corners[corner_index_id]
        else:
            edges_and_corners = self._create_shadow_corners(
                shadow_width_param=shadow_width_param,
                corner_radius_param=corner_radius_param,
                color=color,
                aa_amount=aa_amount
            )

        final_surface.blit(edges_and_corners['top_left'], (0, 0))
        final_surface.blit(edges_and_corners['top_right'], (width - corner_radius_param, 0))

        final_surface.blit(edges_and_corners['bottom_left'],
                           (0, height - corner_radius_param))
        final_surface.blit(edges_and_corners['bottom_right'],
                           (width - corner_radius_param, height - corner_radius_param))

        if width - (2 * corner_radius_param) > 0:
            top_edge = pygame.transform.scale(edges_and_corners['top'],
                                              (width - (2 * corner_radius_param),
                                               shadow_width_param))
            bottom_edge = pygame.transform.scale(edges_and_corners['bottom'],
                                                 (width - (2 * corner_radius_param),
                                                  shadow_width_param))
            final_surface.blit(top_edge, (corner_radius_param, 0))
            final_surface.blit(bottom_edge, (corner_radius_param, height - shadow_width_param))

        if height - (2 * corner_radius_param) > 0:
            left_edge = pygame.transform.scale(edges_and_corners['left'],
                                               (shadow_width_param,
                                                height - (2 * corner_radius_param)))
            right_edge = pygame.transform.scale(edges_and_corners['right'],
                                                (shadow_width_param,
                                                 height - (2 * corner_radius_param)))

            final_surface.blit(left_edge, (0, corner_radius_param))
            final_surface.blit(right_edge, (width - shadow_width_param,
                                            corner_radius_param))

        self._short_term_rect_cache[shadow_id] = final_surface
        return final_surface

    def create_new_ellipse_shadow(
            self,
            width: int,
            height: int,
            shadow_width_param: int,
            aa_amount: int = 4,
            color: Tuple3IntType = (0, 0, 0)
    ) -> Optional['pygame.Surface']:
        """
        Creates a ellipse shaped shadow surface at the specified size and stores it for later use.

        :param width: The width of the shadow to create
        :param height: The height of the shadow to create
        :param shadow_width_param: The width of the shadowed edge
        :param aa_amount: The amount of anti-aliasing to use, defaults to 4
        :param color: Shadow color (r, g, b)
        :return: Surface with shadow
        """
        assert isinstance(width, int)
        assert isinstance(height, int)
        assert_vector(color, 3, int)
        shadow_width_param, aa_amount = int(shadow_width_param), int(aa_amount)
        if shadow_width_param == 0:
            return None
        shadow_surface = pygame.surface.Surface((width * aa_amount, height * aa_amount),
                                                flags=pygame.SRCALPHA, depth=32)
        shadow_surface.fill(pygame.Color('#00000000'))
        r, g, b = color
        ellipse_id = str(width) + 'x' + str(height) + 'x' + str(shadow_width_param)
        if ellipse_id in self._created_ellipse_shadows:
            return self._created_ellipse_shadows[ellipse_id]

        alpha_increment = max(1, int(20 / shadow_width_param))
        shadow_alpha = alpha_increment
        shadow_width = width * aa_amount
        shadow_height = height * aa_amount
        for i in range(shadow_width_param):
            if shadow_width > 0 and shadow_height > 0:
                shadow_rect = pygame.Rect(i * aa_amount,
                                          i * aa_amount,
                                          shadow_width,
                                          shadow_height)
                pygame.draw.ellipse(shadow_surface,
                                    pygame.Color(r, g, b, shadow_alpha), shadow_rect)
                shadow_width -= (2 * aa_amount)
                shadow_height -= (2 * aa_amount)
                shadow_alpha += alpha_increment

        final_surface = pygame.transform.smoothscale(shadow_surface, (width, height))
        self._created_ellipse_shadows[ellipse_id] = final_surface
        return final_surface
