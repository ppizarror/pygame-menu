"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEXT INPUT
Text input class, this widget lets user write text.
"""

__all__ = [
    'TextInput',
    'TextInputManager'
]

import math
import pygame
import pygame_menu
import pygame_menu.controls as ctrl

from abc import ABC
from pygame_menu.locals import FINGERDOWN, FINGERUP, INPUT_INT, INPUT_FLOAT, INPUT_TEXT
from pygame_menu.utils import check_key_pressed_valid, make_surface, assert_color, \
    get_finger_pos, warn, assert_vector
from pygame_menu.widgets.core.widget import Widget, WidgetTransformationNotImplemented, \
    AbstractWidgetManager

from pygame_menu._types import Optional, Any, CallbackType, Tuple, List, ColorType, \
    NumberType, Tuple2IntType, Dict, Tuple2NumberType, NumberInstance, ColorInputType, \
    EventVectorType, Union, Callable

try:
    # noinspection PyProtectedMember
    from pyperclip import copy, paste, PyperclipException

except (ModuleNotFoundError, ImportError):
    copy, paste = lambda text: None, lambda: ''


    class PyperclipException(RuntimeError):
        """
        Pyperclip exception thrown by pyperclip.
        """

CTRL_KMOD = (
    pygame.KMOD_CTRL, pygame.KMOD_CTRL | pygame.KMOD_CAPS,
    pygame.KMOD_LCTRL, pygame.KMOD_LCTRL | pygame.KMOD_CAPS,
    pygame.KMOD_RCTRL, pygame.KMOD_RCTRL | pygame.KMOD_CAPS
)


# noinspection PyMissingOrEmptyDocstring
class TextInput(Widget):
    """
    Text input widget.

    The callbacks receive the current value and all unknown keyword arguments,
    where ``current_text=widget.get_value``:

    .. code-block:: python

        onchange(current_text, **kwargs)
        onreturn(current_text, **kwargs)

    .. note::

        TextInput text input is sensitive to the widget font, some fonts do not
        support some characters or languages (for example Chinese). Be careful
        about which font use.

    .. note::

        TextInput only accepts vertical flip and translation transformations.

    :param title: Text input title
    :param textinput_id: ID of the text input
    :param copy_paste_enable: Enables copy, paste, and cut
    :param cursor_color: Color of cursor
    :param cursor_selection_color: Color of the text selection if the cursor is enabled on certain widgets
    :param cursor_selection_enable: Enables selection of text
    :param cursor_size: Set surface x,y of the cursor which determines cursor size
    :param cursor_switch_ms: Interval of cursor switch between off and on status. First status is ``off``
    :param history: Maximum number of editions stored
    :param input_type: Type of the input data. See :py:mod:`pygame_menu.locals`
    :param input_underline: Character string drawn under the input
    :param input_underline_len: Total of characters to be drawn under the input. If ``0`` this number is computed automatically to fit the font
    :param input_underline_vmargin: Vertical margin of underline in px
    :param maxchar: Maximum length of input
    :param maxwidth: Maximum size of the text to be displayed (overflow). If ``0`` this feature is disabled
    :param maxwidth_dynamically_update: Dynamically update maxwidth depending on char size
    :param onchange: Callback when changing the text input
    :param onreturn: Callback when pressing return (apply) on the text input
    :param onselect: Function when selecting the widget
    :param password: Input string is displayed as a password
    :param password_char: Character used by password type
    :param repeat_keys: Enable key repeat
    :param repeat_keys_initial_ms: Time in milliseconds before keys are repeated when held in milliseconds
    :param repeat_keys_interval_ms: Interval between key press repetition when held in milliseconds
    :param repeat_mouse_interval_ms: Interval between mouse events when held in milliseconds
    :param text_ellipsis: Ellipsis text when overflow occurs (input length exceeds maxwidth)
    :param valid_chars: List of chars that are valid, ``None`` if all chars are valid
    :param kwargs: Optional keyword arguments
    """
    _absolute_origin: Tuple2IntType
    _alt_x_enabled: bool
    _apply_widget_update_callback: bool  # Used in ColorInput
    _block_copy_paste: bool
    _clock: 'pygame.time.Clock'
    _copy_paste_enabled: bool
    _current_underline_string: str  # Testing
    _cursor_color: ColorType
    _cursor_ms_counter: NumberType  # Stores the ms between cursor switch
    _cursor_offset: NumberType
    _cursor_position: int
    _cursor_render: bool
    _cursor_size: Optional[Tuple2IntType]  # Size defined by user
    _cursor_surface: Optional['pygame.Surface']
    _cursor_surface_pos: List[int]
    _cursor_switch_ms: NumberType
    _cursor_visible: bool
    _ellipsis: str
    _ellipsis_size: NumberType
    _history: List[str]
    _history_cursor: List[int]
    _history_index: int
    _history_renderbox: List[List[int]]
    _ignore_keys: Tuple[int, ...]
    _input_string: str
    _input_type: str
    _input_underline: str
    _input_underline_len: int
    _input_underline_size: NumberType
    _input_underline_vmargin: int
    _key_is_pressed: bool
    _keychar_size: Dict[str, NumberType]
    _keyrepeat: bool
    _keyrepeat_counters: Dict[int, List[int]]
    _keyrepeat_initial_interval_ms: NumberType
    _keyrepeat_interval_ms: NumberType
    _keyrepeat_mouse_interval_ms: NumberType
    _keyrepeat_mouse_ms: NumberType
    _last_char: str
    _last_container_width: int
    _last_key: int
    _last_selection_render: List[int]
    _maxchar: int
    _maxwidth: int
    _maxwidth_base: int
    _maxwidth_update: bool
    _maxwidthsize: NumberType
    _mouse_is_pressed: bool
    _password: bool
    _password_char: str
    _renderbox: List[int]
    _selection_active: bool
    _selection_box: List[int]
    _selection_color: ColorType
    _selection_enabled: bool
    _selection_mouse_first_position: int
    _selection_position: List[int]
    _selection_surface: Optional['pygame.Surface']
    _title_size: NumberType
    _valid_chars: Optional[List[str]]

    def __init__(
            self,
            title: Any,
            textinput_id: str = '',
            copy_paste_enable: bool = True,
            cursor_color: ColorInputType = (0, 0, 0),
            cursor_selection_color: ColorInputType = (30, 30, 30, 100),
            cursor_selection_enable: bool = True,
            cursor_size: Optional[Tuple2IntType] = None,
            cursor_switch_ms: NumberType = 500,
            history: int = 50,
            input_type: str = INPUT_TEXT,
            input_underline: str = '',
            input_underline_len: int = 0,
            input_underline_vmargin: int = 0,
            maxchar: int = 0,
            maxwidth: int = 0,
            maxwidth_dynamically_update: bool = True,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: CallbackType = None,
            password: bool = False,
            password_char: str = '*',
            repeat_keys: bool = True,
            repeat_keys_initial_ms: NumberType = 400,
            repeat_keys_interval_ms: NumberType = 50,
            repeat_mouse_interval_ms: NumberType = 400,
            text_ellipsis: str = '...',
            valid_chars: Optional[List[str]] = None,
            *args,
            **kwargs
    ) -> None:
        assert isinstance(copy_paste_enable, bool)
        assert isinstance(cursor_selection_enable, bool)
        assert isinstance(cursor_size, (type(None), tuple))
        assert isinstance(cursor_switch_ms, NumberInstance)
        assert isinstance(history, int)
        assert isinstance(input_type, str)
        assert isinstance(input_underline, str)
        assert isinstance(input_underline_len, int)
        assert isinstance(input_underline_vmargin, int)
        assert isinstance(maxchar, int)
        assert isinstance(maxwidth, int)
        assert isinstance(password, bool)
        assert isinstance(password_char, str)
        assert isinstance(repeat_keys, bool)
        assert isinstance(repeat_keys_initial_ms, NumberInstance)
        assert isinstance(repeat_keys_interval_ms, NumberInstance)
        assert isinstance(repeat_mouse_interval_ms, NumberInstance)
        assert isinstance(text_ellipsis, str)
        assert isinstance(textinput_id, str)
        assert isinstance(valid_chars, (type(None), list))

        assert history >= 0, \
            'history must be equal or greater than zero'
        assert maxchar >= 0, \
            'maxchar must be equal or greater than zero'
        assert maxwidth >= 0, \
            'maxwidth must be equal or greater than zero'
        assert len(password_char) == 1, \
            'password char must be a character'
        assert input_underline_len >= 0, \
            'input underline length must be equal or greater than zero'
        assert cursor_switch_ms > 0, \
            'cursor switch in milliseconds must be greater than zero'
        assert repeat_keys_initial_ms > 0, \
            'repeat keys initial ms cannot be lower or equal than zero'
        assert repeat_keys_interval_ms > 0, \
            'repeat keys interval ms cannot be lower or equal than zero'
        assert repeat_mouse_interval_ms > 0, \
            'repeat mouse interval ms cannot be lower or equal than zero'

        cursor_color = assert_color(cursor_color)
        cursor_selection_color = assert_color(cursor_selection_color)
        if pygame.vernum[0] >= 2:  # pygame 1.9.3 don't have vernum.major
            assert len(cursor_selection_color) == 4, \
                'cursor selection color alpha must be defined'
            assert cursor_selection_color[3] != 255, \
                'cursor selection color alpha cannot be opaque'

        if cursor_size is not None:
            assert_vector(cursor_size, 2, int)
            assert cursor_size[0] > 0, \
                'cursor size width must be greater than zero'
            assert cursor_size[1] > 0, \
                'cursor size height must be greater than zero'

        super(TextInput, self).__init__(
            args=args,
            kwargs=kwargs,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            title=title,
            widget_id=textinput_id
        )

        self._input_string = ''
        self._ignore_keys = (  # Ignore keys on keyrepeat event
            ctrl.KEY_MOVE_DOWN,
            ctrl.KEY_MOVE_UP,
            ctrl.KEY_TAB,
            pygame.K_CAPSLOCK,
            pygame.K_END,
            pygame.K_ESCAPE,
            pygame.K_HOME,
            pygame.K_LCTRL,
            pygame.K_LSHIFT,
            pygame.K_NUMLOCK,
            pygame.K_RCTRL,
            pygame.K_RETURN,
            pygame.K_RSHIFT
        )

        # Vars to make keydown repeat after user pressed a key for some time:
        self._block_copy_paste = False  # Blocks event
        self._key_is_pressed = False
        self._keyrepeat = repeat_keys
        self._keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self._keyrepeat_initial_interval_ms = repeat_keys_initial_ms
        self._keyrepeat_interval_ms = repeat_keys_interval_ms
        self._last_key = 0

        # Mouse handling
        self._keyrepeat_mouse_ms = 0
        self._keyrepeat_mouse_interval_ms = repeat_mouse_interval_ms
        self._mouse_is_pressed = False

        # Render box (overflow)
        self._ellipsis = text_ellipsis
        self._ellipsis_size = 0
        self._renderbox = [0, 0, 0]  # Left/Right/Inner, int

        # Things cursor:
        self._clock = pygame.time.Clock()
        self._cursor_color = cursor_color
        self._cursor_ms_counter = 0
        self._cursor_offset = -1.0
        self._cursor_position = 0  # Inside text
        self._cursor_render = True  # If True cursor must be rendered
        self._cursor_surface = None
        self._cursor_surface_pos = [0, 0]  # Position (x,y) of surface
        self._cursor_size = cursor_size
        self._cursor_switch_ms = cursor_switch_ms
        self._cursor_visible = False  # Switches every self._cursor_switch_ms ms

        # History of editions
        self._history = []
        self._history_cursor = []
        self._history_renderbox = []
        self._history_index = 0  # Index at which the new editions are added
        self._max_history = history

        # Text selection
        self._last_selection_render = [0, 0]  # Position, int
        self._selection_active = False
        self._selection_box = [0, 0]  # [from, to], int
        self._selection_color = cursor_selection_color
        self._selection_enabled = cursor_selection_enable
        # Touch emulates a mouse, so this is used by both touch and mouse
        self._selection_mouse_first_position = -1
        self._selection_position = [0, 0]  # x,y (float)
        self._selection_surface = None

        # List of valid chars
        if valid_chars is not None:
            for ch in range(len(valid_chars)):
                _char = str(valid_chars[ch])
                valid_chars[ch] = _char
                assert isinstance(_char, str), \
                    f'element "{_char}" of valid_chars must be a string'
                assert len(_char) == 1, \
                    f'element "{_char}" of valid_chars must be character'
            assert len(valid_chars) > 0, \
                'valid_chars list must contain at least 1 element'
        self._valid_chars = valid_chars

        # Callbacks
        self._apply_widget_update_callback = True

        # Other
        self._accept_events = True
        self._alt_x_enabled = True
        self._copy_paste_enabled = copy_paste_enable
        self._current_underline_string = ''
        self._input_type = input_type
        self._input_underline = input_underline
        self._input_underline_len = input_underline_len
        self._input_underline_size = 0
        self._input_underline_vmargin = input_underline_vmargin
        self._keychar_size = {'': 0}
        self._last_char = ''
        self._last_container_width = 0
        self._maxchar = maxchar
        self._maxwidth = maxwidth  # This value will be changed depending on how many chars are printed
        self._maxwidth_base = maxwidth
        self._maxwidth_update = maxwidth_dynamically_update
        self._maxwidthsize = 0  # Updated in _apply_font()
        self._password = password
        self._password_char = password_char
        self._title_size = 0

    def _apply_font(self) -> None:
        self._ellipsis_size = self._font.size(self._ellipsis)[0]
        self._title_size = self._font.size(self._title)[0]

        # Generate the underline surface
        self._input_underline_size = self._font.size(self._input_underline * 3)[0] / 3

        # Size of maxwidth if not zero
        max_char = 'O'
        if self._password:
            max_char = self._password_char
        max_char_size = self._font_render_string(max_char * self._maxwidth_base).get_size()
        self._maxwidthsize = max_char_size[0]

        # Update password char size
        if self._password:
            password_size = self._font_render_string(self._password_char).get_size()[0]
            if password_size == 0:
                raise ValueError(
                    'password character is not valid, the size of the font is zero, '
                    'use another character or change the font')
            self._keychar_size[self._password_char] = password_size

    def clear(self) -> None:
        """
        Clear the current text.
        """
        self._input_string = ''
        self._cursor_position = 0
        self._renderbox = [0, 0, 0]
        self._delete()
        self.change()

    def get_value(self) -> str:
        """
        Return the value of the text.

        :return: Text inside the widget
        """
        value = ''
        if self._input_type == INPUT_TEXT:
            value = self._input_string  # Without filters
        elif self._input_type == INPUT_FLOAT:
            try:
                value = float(self._input_string)
            except ValueError:
                value = 0
        elif self._input_type == INPUT_INT:
            try:
                value = int(float(self._input_string))
            except ValueError:
                value = 0
        return value

    def scale(self, *args, **kwargs) -> 'TextInput':
        raise WidgetTransformationNotImplemented()

    def resize(self, *args, **kwargs) -> 'TextInput':
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args, **kwargs) -> 'TextInput':
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args, **kwargs) -> 'TextInput':
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args, **kwargs) -> 'TextInput':
        raise WidgetTransformationNotImplemented()

    def flip(self, x: bool, y: bool) -> 'TextInput':  # Actually flip on x-axis is disabled
        super(TextInput, self).flip(False, y)
        return self

    def _draw(self, surface: 'pygame.Surface') -> None:
        # Draw selection surface
        if pygame.vernum[0] >= 2:  # pygame 1.9.3 don't have vernum.major
            surface.blit(self._surface, (self._rect.x, self._rect.y))  # Draw string
            if self._selection_surface is not None:  # Draw selection
                surface.blit(self._selection_surface, (self._selection_position[0], self._selection_position[1]))
        else:
            if self._selection_surface is not None:  # Draw selection
                surface.blit(self._selection_surface, (self._selection_position[0], self._selection_position[1]))
            surface.blit(self._surface, (self._rect.x, self._rect.y))  # Draw string

        # Draw cursor
        if self._selected and self._cursor_surface and \
                (self._cursor_visible or self._key_is_pressed) and \
                not self.readonly:
            x = self._rect.x + self._cursor_surface_pos[0]
            if self._flip[0]:  # Flip on x-axis (bug)
                x = self._surface.get_width() - x
            y = self._rect.y + self._cursor_surface_pos[1]
            surface.blit(self._cursor_surface, (x, y))

    def _render(self) -> Optional[bool]:
        string = self._title + self._get_input_string()  # Render string

        max_cont_width = self._get_max_container_width()
        if max_cont_width != 0:
            self._last_container_width = max_cont_width

        if not self._render_hash_changed(
                string, self._selected, self._cursor_render, self._cursor_position,
                self._selection_enabled, self.active, self._visible, self.readonly,
                self._last_container_width, self._selection_box[0], self._menu,
                self._selection_box[1], self._last_selection_render[0], self._padding,
                self._last_selection_render[1], self._renderbox[0], self._renderbox[1],
                self._renderbox[2], self._cursor_visible, self._title_size,
                self._selection_effect.get_width()):
            return True

        # Apply underline if exists
        self._surface = self._render_string_underline(string, self.get_font_color_status())
        self._apply_transforms()

        # Render the cursor
        self._render_cursor()

        # Render the selection box if text is selected
        self._render_selection_box()

        # Update last rendered
        self._last_rendered_string = string

        # Update the size of the render
        self._rect.width, self._rect.height = self._surface.get_size()

        # Force Menu update
        self.force_menu_surface_update()

    def _render_selection_box(self, force: bool = False) -> None:
        """
        Render selected text.

        :param force: Force update
        """
        if not self._selection_enabled:
            return

        if self._selection_active and \
                (self._last_selection_render[0] != self._selection_box[0] or
                 self._last_selection_render[1] != self._selection_box[1]) or force:

            # If there's no limit
            pos = [0, 0]
            if self._maxwidth == 0:
                pos[0] = self._selection_box[0]
                pos[1] = self._selection_box[1]
            else:
                pos[0] = max(self._selection_box[0], self._renderbox[0])
                pos[1] = min(self._selection_box[1], self._renderbox[1])

            # Find coordinates of each position
            string = self._get_input_string_filtered()
            string_init = string[self._renderbox[0]:pos[0]]
            string_final = string[self._renderbox[0]:pos[1]]

            x1 = self._cursor_offset + self._font.size(self._title + string_init)[0]
            x2 = self._cursor_offset + self._font.size(self._title + string_final)[0] + 1

            self._last_selection_render[0] = self._selection_box[0]
            self._last_selection_render[1] = self._selection_box[1]

            x = x2 - x1
            if x <= 1:
                self._selection_surface = None
                return
            y = self._font.size(self._title)[1]

            # Add ellipsis
            delta = self._ellipsis_size
            if self._ellipsis_left_and_right():  # If Left+Right ellipsis
                delta *= 1
            elif self._ellipsis_right():  # Right ellipsis
                delta *= 0
            elif self._ellipsis_left():  # Left ellipsis
                delta *= 1
            else:
                delta *= 0
            x1 += delta
            x2 += delta

            # Apply scale factor (experimental)
            x *= self._scale_factor[0]
            y *= self._scale_factor[1]
            x1 *= self._scale_factor[0]

            # Create surface and fill
            self._selection_surface = make_surface(x, y, fill_color=self._selection_color)
            self._selection_position[0] = x1 + self._rect.x
            self._selection_position[1] = self._rect.y

            # Fill cursor
            if self._cursor_surface:
                self._cursor_surface.fill(self._cursor_color)

    def _get_max_container_width(self) -> int:
        """
        Return the maximum textarea container width. It can be the column width,
        menu width or frame width if horizontal.

        :return: Container width
        """
        menu = self._menu
        frame = self.get_frame()
        if menu is None:
            return 0
        try:
            # noinspection PyProtectedMember
            max_width = menu._column_widths[self.get_col_row_index()[0]]
        except IndexError:
            max_width = menu.get_width(inner=True)

        # Textarea within frame
        if frame is not None:
            if frame.horizontal:
                raise RuntimeError(
                    'horizontal frame cannot contain variable width sizing textinput '
                    '(requested by input underline). Set input_underline_len variable '
                    'to avoid this Exception'
                )
            max_width = frame.get_width()
        return max_width - self._padding[1] - self._padding[3]

    def _render_string_underline(self, string: str, color: ColorInputType) -> 'pygame.Surface':
        """
        Render underline string surface.

        :param string: String to render
        :param color: Color of the string to render
        :return: New surface
        """
        color = assert_color(color)

        # Create surface with no underline (just text)
        surface = self._render_string(string, color)

        # If underline is not enabled
        if self._input_underline_size == 0:
            return surface

        current_rect = surface.get_rect()

        # Compute initial char guess
        if self._input_underline_len != 0:  # User defined the amount of underline chars to use
            char = self._input_underline_len

        else:  # Compute available width and propose the maximum chars needed (fill all width)

            # Calculate total available space
            #  |---------------------------------------------------|
            #  |MENU                                               |
            #  |                <---- space-between-title --->     |
            #  |   .===TITLE====|=THE INPUT OF USER===========.    |
            #  | self._rect.x   title                       posx2  |
            #  |                                                   |
            #  |---------------------------------------------------|

            posx2 = max(self._get_max_container_width() - self._input_underline_size * 1.75, current_rect.width)
            delta_ch = posx2 - self._title_size - self._selection_effect.get_width()
            char = math.ceil(delta_ch / self._input_underline_size)
            for i in range(10):  # Find the best guess for
                fw = self._font_render_string(self._input_underline * int(char), color).get_width()
                char += 1
                if fw >= delta_ch:
                    break

        # If char limit
        if self._maxchar != 0 or self._maxwidth_base != 0:
            max_chars = max(self._maxchar, self._maxwidth_base)
            base_char = 'O'
            if self._password:
                base_char = self._password_char
            max_size = self._font_render_string(base_char * max_chars)
            max_size = max_size.get_size()[0]
            maxchar_char = math.ceil((max_size + self._ellipsis_size) / self._input_underline_size)
            char = min(char, maxchar_char)

        underline_string = self._input_underline * max(int(char), 0)

        # Render char
        self._current_underline_string = underline_string
        underline = self._font_render_string(underline_string, color, use_background_color=False)

        # Create a new surface
        new_width = max(self._title_size + underline.get_size()[0], current_rect.width)
        new_surface = make_surface(
            new_width, current_rect.height + 3 + self._input_underline_vmargin,
            alpha=True
        )

        # Compute underline vmargin by its height
        uvm = 5  # underline vertical margin
        if underline.get_height() <= 15:
            uvm = 4
        if underline.get_height() <= 7:
            uvm = 3

        # Blit current surface
        new_surface.blit(surface, (0, 0))
        new_surface.blit(underline, (self._title_size, uvm + self._input_underline_vmargin))

        # Return new surface
        return new_surface

    def _render_cursor(self) -> None:
        """
        Cursor is rendered and stored.
        """
        # Cursor should not be rendered
        if not self._cursor_render:
            return

        # Cursor surface does not exist
        if self._cursor_surface is None:
            if self._rect.height == 0:  # If Menu has not been initialized this error can occur
                return
            if self._cursor_size is not None:
                self._cursor_surface = make_surface(*self._cursor_size)
            else:
                self._cursor_surface = make_surface(self._font_size / 20 + 1, self._rect.height - 2)
            self._cursor_surface.fill(self._cursor_color)

        # Get string
        string = self._get_input_string_filtered()

        # Calculate x position
        if self._maxwidth == 0:  # If no limit is provided
            cursor_x_pos = self._cursor_offset + self._font.size(self._title + string[:self._cursor_position])[0]
        else:  # Calculate position depending on renderbox
            string = string[self._renderbox[0]:(self._renderbox[0] + self._renderbox[2])]
            cursor_x_pos = self._cursor_offset + self._font.size(self._title + string)[0]

            # Add ellipsis
            delta = self._ellipsis_size
            if self._ellipsis_left_and_right():  # If Left+Right ellipsis
                delta *= 1
            elif self._ellipsis_right():  # Right ellipsis
                delta *= 0
            elif self._ellipsis_left():  # Left ellipsis
                delta *= 1
            else:
                delta *= 0
            cursor_x_pos += delta
        if self._cursor_position > 0 or (self._title and self._cursor_position == 0):
            # Without this, the cursor is invisible when self._cursor_position > 0:
            cursor_x_pos -= self._cursor_surface.get_width()

        # Calculate y position
        cursor_y_pos = 0

        # Move x position
        cursor_x_pos += 2

        # Store position, apply scale factor (experimental)
        self._cursor_surface_pos[0] = int(cursor_x_pos) * self._scale_factor[0]
        self._cursor_surface_pos[1] = int(cursor_y_pos) * self._scale_factor[1]
        self._cursor_render = False

    def _ellipsis_left(self) -> bool:
        """
        Return ``True`` if left ellipsis is active.

        :return: Boolean
        """
        return self._renderbox[0] != 0 and self._maxwidth != 0

    def _ellipsis_right(self) -> bool:
        """
        Return ``True`` if right ellipsis is active.

        :return: Boolean
        """
        return self._renderbox[1] != len(self._input_string) and self._maxwidth != 0

    def _ellipsis_left_and_right(self) -> bool:
        """
        Return ``True`` if left and right ellipsis are active.

        :return: Boolean
        """
        return self._ellipsis_left() and self._ellipsis_right()

    def _get_input_string_filtered(self) -> str:
        """
        Return the input string where all filters have been applied.

        :return: Filtered string
        """
        string = self._input_string

        # Apply password
        if self._password:
            string = self._password_char * len(string)

        return string

    def _get_input_string(self, add_ellipsis: bool = True) -> str:
        """
        Return the input string, apply overflow if enabled.

        :param add_ellipsis: Adds ellipsis text
        :return: String
        """
        string = self._get_input_string_filtered()

        if self._maxwidth != 0 and len(string) > self._maxwidth:
            text = string[self._renderbox[0]:self._renderbox[1]]
            if add_ellipsis:
                if self._ellipsis_right():
                    text += self._ellipsis
                if self._ellipsis_left():
                    text = self._ellipsis + text
            return text
        else:
            return string

    def _update_renderbox(
            self,
            left: int = 0,
            right: int = 0,
            addition: bool = False,
            end: bool = False,
            start: bool = False,
            update_maxwidth: bool = True
    ) -> None:
        """
        Update renderbox position.

        :param left: Left update
        :param right: Right update
        :param addition: Update if text addition/deletion
        :param end: Move cursor to end
        :param start: Move cursor to start
        :param update_maxwidth: Update maxwidth limit depending on the chars written
        """
        self._cursor_render = True
        if self._maxwidth == 0:
            return
        len_string = len(self._input_string)
        prev_renderbox = self._renderbox.copy()

        # Move cursor to end
        if end:
            self._renderbox[0] = max(0, len_string - self._maxwidth)
            self._renderbox[1] = len_string
            self._renderbox[2] = min(len_string, self._maxwidth)
            return

        # Move cursor to start
        if start:
            self._renderbox[0] = 0
            self._renderbox[1] = min(len_string, self._maxwidth)
            self._renderbox[2] = 0
            return

        # Check limits
        if left < 0 and len_string == 0:
            return

        # If no overflow
        if len_string <= self._maxwidth:
            if right < 0 and self._renderbox[2] == len_string:  # If del at the end of string
                return
            if left < 0 and self._renderbox[2] == 0:  # If cursor is at beginning
                return
            self._renderbox[0] = 0  # To catch unexpected errors
            if addition:  # left/right are ignored
                if left < 0:
                    self._renderbox[1] += left
                self._renderbox[1] += right
                if right < 0:
                    self._renderbox[2] -= right

            # If text is typed increase inner position
            if self._renderbox[0] == prev_renderbox[0]:
                self._renderbox[2] += left
                self._renderbox[2] += right

        else:
            if addition:  # If text is added
                # If press del at the end of string
                if right < 0 and self._renderbox[2] == self._maxwidth:
                    return
                # If backspace at beginning of string
                if left < 0 and self._renderbox[2] == 0:
                    return

                # If user deletes something and it is in the end
                if right < 0:  # del
                    if self._ellipsis_left():
                        if (self._renderbox[1] - 1) == len_string:  # At the end
                            self._renderbox[2] -= right

                # If the user writes, move renderbox
                if right > 0:
                    # If cursor is at the end push box
                    if self._renderbox[2] == self._maxwidth:
                        self._renderbox[0] += right
                        self._renderbox[1] += right
                    self._renderbox[2] += right

                if left < 0:
                    # If cursor is at the beginning
                    if self._renderbox[0] == 0:
                        self._renderbox[2] += left
                    self._renderbox[0] += left
                    self._renderbox[1] += left

            if not addition:  # Move inner (left/right)
                self._renderbox[2] += right
                self._renderbox[2] += left

                # If user pushes after limit the renderbox moves
                if self._renderbox[2] < 0:
                    self._renderbox[0] += left
                    self._renderbox[1] += left
                elif self._renderbox[2] > self._maxwidth:
                    self._renderbox[0] += right
                    self._renderbox[1] += right
                else:
                    update_maxwidth = False

                # If cursor is at limit
                if self._renderbox[1] > len_string or self._renderbox[0] < 0:
                    if self._renderbox[2] != self._maxwidth - 1:
                        update_maxwidth = False

            # Apply string limits
            self._renderbox[1] = max(self._maxwidth, min(self._renderbox[1], len_string))
            self._renderbox[0] = self._renderbox[1] - self._maxwidth

        # Apply limits
        self._renderbox[0] = max(0, self._renderbox[0])
        self._renderbox[1] = min(max(0, self._renderbox[1]), len_string)
        self._renderbox[2] = max(0, min(self._renderbox[2], min(self._maxwidth, len_string)))

        if update_maxwidth:
            self._update_maxlimit_renderbox()

    def _update_maxlimit_renderbox(self) -> None:
        """
        Update renderbox based on how many characters have been written on input.
        """
        if not self._maxwidth_update:
            return

        sign = 0  # Sign of search
        while True:
            curr_string = self._get_input_string(False)  # Already filtered
            lcs = len(curr_string)
            if lcs > 0:
                accum_size = 0
                if self._ellipsis_left():
                    accum_size += self._ellipsis_size + 5

                biggest = 0
                for char in curr_string:
                    char_size = self._get_char_size(char)
                    accum_size += char_size
                    biggest = max(biggest, char_size)

                if self._ellipsis_right():
                    accum_size += self._ellipsis_size

                if accum_size < self._maxwidthsize - biggest:  # Increase
                    if sign < 0:
                        break
                    sign = 1
                    if self._renderbox[0] != 0:
                        self._renderbox[0] -= 1
                    else:
                        break
                    self._maxwidth += 1
                    self._renderbox[2] += 1
                elif accum_size > self._maxwidthsize:
                    if sign > 0:
                        break
                    sign = -1
                    if self._renderbox[2] == 0:
                        self._renderbox[1] -= 1
                    else:
                        self._renderbox[0] += 1
                        # self._renderbox[1] += 1
                        self._renderbox[2] -= 1
                    self._maxwidth -= 1
                else:
                    break
            else:
                self._maxwidth = self._maxwidth_base  # Return to normal
                break

    def _update_cursor_mouse(self, mouse_x: int) -> None:
        """
        Updates cursor position after mouse click or touch action in text.

        :param mouse_x: Mouse distance relative to surface
        """
        string = self._get_input_string()
        if string == '':  # If string is empty cursor is not updated
            return
        self.force_menu_surface_cache_update()

        # Find the accumulated char size that gives the position of cursor
        cursor_pos = 0
        for i in range(len(string)):
            curr_char = string[i] if i < len(string) - 1 else 0
            curr_char_size = 0 if curr_char == 0 else self._font.size(curr_char)[0]
            if self._font.size(self._title + string[0:i])[0] + curr_char_size / 2 < mouse_x:
                cursor_pos += 1
            else:
                break

        # If text have ellipsis
        if self._maxwidth != 0 and len(self._input_string) > self._maxwidth:
            if self._ellipsis_left():
                cursor_pos -= len(self._ellipsis)

            # Check if user clicked on ellipsis
            if cursor_pos < 0 or cursor_pos > self._maxwidth:
                if cursor_pos < 0:
                    self._renderbox[2] = 0
                    self._move_cursor_left()
                if cursor_pos > self._maxwidth:
                    self._renderbox[2] = self._maxwidth
                    self._move_cursor_right()
                return

            # User clicked on text, update cursor
            cursor_pos = max(0, min(self._maxwidth, cursor_pos))
            self._cursor_position = self._renderbox[0] + cursor_pos
            self._renderbox[2] = cursor_pos
            self._update_maxlimit_renderbox()

        # Text does not have ellipsis, inferred position is correct
        else:
            self._cursor_position = cursor_pos
            if self._maxwidth != 0:  # Update renderbox
                self._cursor_position += self._renderbox[0]
                self._renderbox[2] = cursor_pos
                self._update_maxlimit_renderbox()

        if self._selection_mouse_first_position == -1:
            if self._selection_active:  # Unselect and select again
                self._unselect_text()
                self._selection_mouse_first_position = self._cursor_position
        else:
            a = self._selection_mouse_first_position
            b = self._cursor_position
            self._selection_box[0] = min(a, b)
            self._selection_box[1] = max(a, b)
            self._render_selection_box(True)
        self._cursor_render = True

    def _check_mouse_collide_input(self, pos: Tuple2NumberType) -> bool:
        """
        Check mouse collision.

        .. note::

            If this method returns ``True`` the cursor must be updated.

        :param pos: Position
        :return: Cursor update status
        """
        rect = self.get_rect(to_real_position=True, apply_padding=False)
        if rect.collidepoint(*pos):
            # Check if mouse collides left or right as percentage, use only X coordinate
            mouse_x, _ = pos
            topleft, _ = rect.topleft
            self._update_cursor_mouse(mouse_x - topleft)
            return True  # Prevents double click

    def _check_touch_collide_input(self, pos: Tuple2NumberType) -> bool:
        """
        Check touchscreen collision.

        .. note::

            If this method returns ``True`` the cursor must be updated.

        :param pos: Position
        :return: Cursor update status
        """
        rect = self.get_rect(to_real_position=True, apply_padding=False)
        if rect.collidepoint(*pos):
            # Check if touchscreen collides left or right as percentage, use only X coordinate
            touch_x, _ = pos
            topleft, _ = rect.topleft
            self._update_cursor_mouse(touch_x - topleft)
            return True  # Prevents double click

    def set_value(self, text: Any) -> None:
        """
        Set the value of the text.

        :param text: New text of the widget
        """
        if self._password and text != '':
            raise ValueError('value cannot be set in password type')
        if self._check_input_type(text):
            default_text = str(text)

            # Filter valid chars
            if self._valid_chars is not None:
                default_valid = ''
                for ch in default_text:
                    if ch in self._valid_chars:
                        default_valid += ch
                default_text = default_valid

            # Apply maxchar
            len_text = len(default_text)
            if 0 < self._maxchar < len_text:
                default_text = default_text[len_text - self._maxchar:len_text]

            self._input_string = default_text
            for i in range(len(default_text) + 1):
                self._move_cursor_right()
                self._update_renderbox(right=1, addition=True)
            self._update_input_string(default_text)
        else:
            raise ValueError(f'value "{text}" type is not correct according to input_type')
        self._update_renderbox()  # Updates cursor
        self._render()  # Renders the selection box

    def _check_input_size(self) -> bool:
        """
        Check input size.

        :return: ``True`` if the input must be limited
        """
        if self._maxchar == 0:
            return False
        return self._maxchar <= len(self._input_string)

    def _check_input_type(self, string: Any) -> bool:
        """
        Check if input type is valid.

        :param string: String to validate
        :return: ``True`` if the input type is valid
        """
        if string == '':  # Empty is valid
            return True
        if self._input_type == INPUT_TEXT:
            return True

        conv = None
        if self._input_type == INPUT_FLOAT:
            conv = float
        elif self._input_type == INPUT_INT:
            conv = int

        if string == '-':
            return True
        if conv is None:
            return False

        try:
            conv(string)
            return True
        except ValueError:
            return False

    def _move_cursor_left(self) -> None:
        """
        Move cursor to left position.
        """
        # Subtract one from cursor_pos, but do not go below zero:
        self._cursor_position = max(self._cursor_position - 1, 0)
        self._update_renderbox(left=-1)

    def _move_cursor_right(self) -> None:
        """
        Move cursor to right position.
        """
        # Add one to cursor_pos, but do not exceed len(input_string)
        self._cursor_position = min(self._cursor_position + 1, len(self._input_string))
        self._update_renderbox(right=1)

    def _blur(self) -> None:
        # self._key_is_pressed = False
        self._mouse_is_pressed = False
        self._keyrepeat_mouse_ms = 0
        self._cursor_ms_counter = 0
        self._cursor_visible = False
        self._unselect_text()
        # self._history_index = len(self._history) - 1

    def _focus(self) -> None:
        self._cursor_ms_counter = 0
        self._cursor_visible = True
        self._cursor_render = True

    def _unselect_text(self) -> bool:
        """
        Unselect text.

        :return: ``True`` if the selected text was removed in the method call
        """
        removed = self._selection_surface is not None
        if not removed:
            return False
        self._selection_box[0] = 0
        self._selection_box[1] = 0
        self._selection_surface = None
        if self._cursor_surface is not None:
            self._cursor_surface.fill(self._cursor_color)
        self._selection_active = False
        self.force_menu_surface_cache_update()
        return True

    def _get_selected_text(self) -> str:
        """
        Return the selected text.

        :return: Text
        """
        return self._input_string[self._selection_box[0]:self._selection_box[1]]

    def _update_input_string(self, new_string: str, update_history: bool = True) -> None:
        """
        Update input string with a new string, store changes into history.

        :param new_string: New string of text input
        :param update_history: Updates history
        """
        assert isinstance(new_string, str)
        assert isinstance(update_history, bool)

        l_history = len(self._history)

        # If last edition is different from the new one -> updates the history
        if update_history and \
                ((l_history > 0 and self._history[
                    l_history - 1] != new_string) or l_history == 0) and self._max_history > 0:

            # If index is not at last add the current status as new
            if self._history_index != l_history:
                last_string = self._history[self._history_index]
                self._history_index = len(self._history)
                self._update_input_string(last_string)

            # Add new status to history
            self._history.insert(self._history_index, new_string)
            self._history_cursor.insert(self._history_index, self._cursor_position)
            self._history_renderbox.insert(self._history_index, [self._renderbox[0], self._renderbox[1], self._renderbox[2]])

            if len(self._history) > self._max_history:
                self._history.pop(0)
                self._history_cursor.pop(0)
                self._history_renderbox.pop(0)
            self._history_index = len(self._history)  # This can be changed with undo/redo

        # Updates string
        self._input_string = new_string

    def _copy(self) -> bool:
        """
        Copy text from clipboard.

        :return: ``True`` if copied
        """
        if self._block_copy_paste:  # Prevents multiple executions of event
            return False
        if self._password:  # Password cannot be copied
            return False

        try:
            if self._selection_surface:  # If text is selected
                copy(self._get_selected_text())
            else:  # Copy all text
                copy(self._input_string)
        except PyperclipException:
            pass

        self._block_copy_paste = True
        return True

    def _cut(self) -> bool:
        """
        Cut operation.

        :return: ``True`` if cut
        """
        if not self._copy_paste_enabled:  # Ignore cut
            return False

        self._copy()  # This is a safe operation, all checks have been passed

        # If text is selected
        if self._selection_surface:
            self._remove_selection()
            return True
        return False

    def _get_char_size(self, char) -> int:
        """
        Return the widget char size in pixels.

        :param char: Char
        :return: Char size in px
        """
        if char in self._keychar_size.keys():
            return self._keychar_size[char]
        self._keychar_size[char] = self._font_render_string(char).get_size()[0]
        return self._keychar_size[char]

    def _paste(self) -> bool:
        """
        Paste text from clipboard.

        :return: ``True`` if pasted
        """
        if self._block_copy_paste:  # Prevents multiple executions of event
            return False

        # If text is selected
        if self._selection_surface:
            self._remove_selection()

        # Paste text in cursor
        try:
            text = paste()
        except PyperclipException:
            return False

        text = text.strip()
        for i in ['\n', '\r']:
            text = text.replace(i, '')

        # Delete escape chars
        escapes = ''.join([chr(char) for char in range(1, 32)])
        text = text.translate(escapes)
        if text == '':
            return False

        # Remove invalid chars
        if self._valid_chars is not None:
            valid_text = ''
            for ch in text:
                if ch in self._valid_chars:
                    valid_text += ch
            text = valid_text
            if text == '':
                return False

        # Cut string (if limit does exist)
        text_end = len(text)
        if self._maxchar != 0:
            char_limit = self._maxchar - len(self._input_string)
            text_end = min(char_limit, text_end)
            if text_end <= 0:  # If there's no more space, returns
                self._sound.play_event_error()
                return False

        new_string = self._input_string[0:self._cursor_position] \
                     + text[0:text_end] \
                     + self._input_string[self._cursor_position:len(self._input_string)]

        # If string is valid
        if self._check_input_type(new_string):
            # Update char size
            for char in new_string:
                if char not in self._keychar_size:
                    # This updates the self._keychar_size variable
                    self._get_char_size(char)

            self._sound.play_key_add()
            self._input_string = new_string  # For a purpose of computing render_box
            for i in range(len(text)):  # Move cursor
                self._move_cursor_right()
            self._update_input_string(new_string)
            self.change()
            self._update_maxlimit_renderbox()
            self._block_copy_paste = True

        else:
            self._sound.play_event_error()
            return False

        return True

    def _update_from_history(self) -> None:
        """
        Update all from history.
        """
        self._input_string = self._history[self._history_index]
        self._renderbox[0] = self._history_renderbox[self._history_index][0]
        self._renderbox[1] = self._history_renderbox[self._history_index][1]
        self._renderbox[2] = self._history_renderbox[self._history_index][2]
        self._cursor_position = self._history_cursor[self._history_index]
        self._cursor_render = True

    def _undo(self) -> bool:
        """
        Undo operation.

        :return: ``True`` if undo
        """
        if self._history_index == 0:  # There's no back history
            return False
        if self._history_index == len(self._history):  # If the actual is the last
            self._history_index -= 1
        self._history_index = max(0, self._history_index - 1)
        self._update_from_history()
        return True

    def _redo(self) -> bool:
        """
        Redo operation.

        :return: ``True`` if redo
        """
        if self._history_index == len(self._history) - 1:  # There's no forward history
            return False
        self._history_index = min(len(self._history) - 1, self._history_index + 1)
        self._update_from_history()
        return True

    def _remove_selection(self) -> None:
        """
        Remove text from selection.
        """
        removed = self._selection_box[1] - self._selection_box[0]
        left = False
        if self._selection_box[0] == self._cursor_position:
            left = True

        for i in range(removed):
            if left:
                self._delete(update_history=i == removed - 1)
            else:
                self._backspace(update_history=i == removed - 1)

        # Destroy selection
        self._unselect_text()

    def _backspace(self, update_history=True) -> None:
        """
        Backspace event.

        :param update_history: Updates history on deletion
        """
        new_string = (
                self._input_string[:max(self._cursor_position - 1, 0)]
                + self._input_string[self._cursor_position:]
        )
        self._update_input_string(new_string, update_history=update_history)
        self._update_renderbox(left=-1, addition=True)

        # Subtract one from cursor_pos, but do not go below zero:
        self._cursor_position = max(self._cursor_position - 1, 0)

    def _delete(self, update_history: bool = True) -> None:
        """
        Delete event.

        :param update_history: Updates history on deletion
        """
        new_string = (
                self._input_string[:self._cursor_position]
                + self._input_string[self._cursor_position + 1:]
        )
        self._update_input_string(new_string, update_history=update_history)
        self._update_renderbox(right=-1, addition=True)

    def _select_all(self) -> None:
        """
        Select all text.
        """
        if not self._selection_enabled:
            return
        self._selection_box[0] = 0
        self._selection_box[1] = len(self._input_string)
        self._cursor_position = self._selection_box[1]
        for i in range(len(self._input_string)):
            self._move_cursor_right()
        self._render_selection_box(True)
        self._selection_active = False

    def _push_key_input(self, keychar: str, sounds: bool = True) -> bool:
        """
        Insert a key in the cursor position.

        :param keychar: Char to be inserted
        :param sounds: Use widget sounds
        :return: If ``False`` the event loop breaks
        """
        # If selected text
        if self._selection_surface:
            self._remove_selection()

        # Check input exceeded the limit returns
        if self._check_input_size():
            if sounds:
                self._sound.play_event_error()
            return False

        # If no special key is pressed, add unicode of key to input_string
        new_string = (
                self._input_string[:self._cursor_position]
                + keychar
                + self._input_string[self._cursor_position:]
        )

        # If unwanted escape sequences
        event_escaped = repr(keychar)
        if '\\r' in event_escaped:
            return False

        # Check if char is valid
        if self._valid_chars is not None and keychar not in self._valid_chars:
            if sounds:
                self._sound.play_event_error()
            return False

        # If data is valid
        if self._check_input_type(new_string):
            l_key = len(keychar)
            if l_key > 0:

                # Update char size
                if keychar not in self._keychar_size.keys():
                    self._get_char_size(keychar)  # This updates keychar size data
                self._last_char = keychar

                # Update string
                if sounds:
                    self._sound.play_key_add()
                self._cursor_position += 1  # Some are empty, e.g. K_UP
                self._input_string = new_string  # Only here this is changed (due to renderbox update)
                self._update_input_string(new_string)  # Update the string and the history
                self._update_renderbox(right=1, addition=True)
                self.change()
                return True
        else:
            if sounds:
                self._sound.play_event_error()
        return False

    def update(self, events: EventVectorType) -> bool:
        if self._apply_widget_update_callback:
            self.apply_update_callbacks(events)

        self._clock.tick(60)

        # Check mouse pressed
        # noinspection PyArgumentList
        mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()
        self._mouse_is_pressed = (mouse_left or mouse_right or mouse_middle) and self._mouse_enabled

        rect = self.get_rect(to_real_position=True)

        if self.readonly or not self.is_visible():
            self._readonly_check_mouseover(events, rect)
            return False

        # Get time clock
        time_clock = self._clock.get_time()

        # Update cursor switch
        self._cursor_ms_counter += time_clock
        if self._cursor_ms_counter >= self._cursor_switch_ms:
            self._cursor_ms_counter %= self._cursor_switch_ms
            self._cursor_visible = not self._cursor_visible
            self.force_menu_surface_cache_update()

        updated = False
        events = self._merge_events(events)  # Extend events with custom events

        for event in events:

            # Check mouse over
            self._check_mouseover(event, rect)

            # User press a key
            if event.type == pygame.KEYDOWN and self._keyboard_enabled:
                # Check if any key is pressed, if True the event is invalid
                if self._ignores_keyboard_nonphysical() and not check_key_pressed_valid(event):
                    continue

                self._cursor_visible = True  # So the user sees where he writes
                self._key_is_pressed = True
                self._last_key = event.key

                # If None exist, create counter for that key:
                if event.key not in self._keyrepeat_counters and \
                        event.key not in self._ignore_keys and \
                        'unicode' in event.dict:
                    self._keyrepeat_counters[event.key] = [0, event.unicode]

                # User press ctrl+something
                if pygame.key.get_mods() in CTRL_KMOD:
                    # If test, disable CTRL
                    if 'test' in event.dict and event.dict['test']:
                        # noinspection PyArgumentList
                        pygame.key.set_mods(pygame.KMOD_NONE)

                    # Ctrl+C copy
                    if event.key == pygame.K_c:
                        if not self._copy_paste_enabled:
                            self._sound.play_event_error()
                            break
                        self.active = True
                        copy_status = self._copy()
                        if not copy_status:
                            self._sound.play_event_error()
                        updated = updated or copy_status
                        break

                    # Ctrl+V paste
                    elif event.key == pygame.K_v:
                        if not self._copy_paste_enabled:
                            self._sound.play_event_error()
                            break
                        self.active = True
                        updated = updated or self._paste()
                        break

                    # Ctrl+Z undo
                    elif event.key == pygame.K_z:
                        if self._max_history == 0:
                            self._sound.play_event_error()
                            break
                        self.active = True
                        self._sound.play_key_del()
                        updated = updated or self._undo()
                        break

                    # Ctrl+Y redo
                    elif event.key == pygame.K_y:
                        if self._max_history == 0:
                            self._sound.play_event_error()
                            break
                        self.active = True
                        self._sound.play_key_add()
                        updated = updated or self._redo()
                        break

                    # Ctrl+X cut
                    elif event.key == pygame.K_x:
                        if not self._copy_paste_enabled:
                            self._sound.play_event_error()
                            break
                        self.active = True
                        self._sound.play_key_del()
                        updated = updated or self._cut()
                        break

                    # Ctrl+A select all
                    elif event.key == pygame.K_a:
                        if not self._selection_enabled:
                            self._sound.play_event_error()
                            break
                        self.active = True
                        self._select_all()
                        updated = True
                        break

                    # Command not found, returns
                    else:
                        break

                # User press alt+x get the unicode char from string
                if pygame.key.get_mods() in (pygame.KMOD_ALT, pygame.KMOD_LALT) and \
                        event.key == pygame.K_x and self._alt_x_enabled:
                    # Get the last hex value
                    last_space = self._input_string.rfind(' ')
                    if last_space == -1:  # space not found, try 0x
                        last_space = self._input_string.rfind('0x')
                    if last_space == -1:  # 0x not found, try 0X
                        last_space = self._input_string.rfind('0x')
                    if last_space == -1:  # Finally, find the subsequence of valid hex chars
                        last_space = 0
                        for j in range(len(self._input_string)):
                            if self._input_string[j].lower() not in \
                                    ('0', '1', '2', '3', '4', '5', '6', '7',
                                     '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'):
                                last_space = j + 1
                        if last_space >= len(self._input_string):
                            last_space = -1
                    if last_space >= 0:
                        try:
                            unicode_hex = self._input_string[last_space:]
                            if unicode_hex.lower() == '0x':
                                continue
                            unicode_int = int(unicode_hex, 16)

                            # Remove the code
                            for _ in range(len(unicode_hex)):
                                self._backspace()

                            if not self._push_key_input(chr(unicode_int)):
                                break
                            self.active = True
                            updated = True
                            continue
                        except (ValueError, OverflowError):
                            pass

                # Backspace button, delete text from right
                if self._ctrl.back(event, self):
                    # Play sound
                    if self._cursor_position == 0:
                        self._sound.play_event_error()
                    else:
                        self._sound.play_key_del()

                    # If text is selected
                    if self._selection_surface:
                        self._remove_selection()
                        updated = True
                        break

                    self._backspace()
                    self.change()
                    self.active = True
                    updated = True

                # Delete button, delete text from left
                elif self._ctrl.delete(event, self):
                    # Play sound
                    if self._cursor_position == len(self._input_string):
                        self._sound.play_event_error()
                    else:
                        self._sound.play_key_del()

                    updated = True

                    # If text is selected
                    if self._selection_surface:
                        self._remove_selection()
                        break

                    self._delete()
                    self.change()
                    self.active = True

                # Right arrow
                elif self._ctrl.right(event, self):
                    # Play sound
                    if self._cursor_position == len(self._input_string):
                        self._sound.play_event_error()
                    else:
                        self._sound.play_key_add()

                    # Update selection box
                    if self._selection_active:
                        if self._cursor_position == self._selection_box[1]:
                            if self._selection_box[0] == self._selection_box[1]:
                                self._selection_box[1] = self._selection_box[0] + 1
                            else:
                                self._selection_box[1] = min(len(self._input_string), self._selection_box[1] + 1)
                        else:
                            self._selection_box[0] = min(self._selection_box[1], self._selection_box[0] + 1)
                    else:
                        if self._unselect_text():
                            break

                    # Move cursor
                    self._move_cursor_right()
                    self.active = True
                    updated = True

                # Left arrow
                elif self._ctrl.left(event, self):
                    # Play sound
                    if self._cursor_position == 0:
                        self._sound.play_event_error()
                    else:
                        self._sound.play_key_add()

                    # Update selection box
                    if self._selection_active:
                        if self._cursor_position == self._selection_box[0]:
                            self._selection_box[0] = max(0, self._selection_box[0] - 1)
                        else:
                            if self._selection_box[1] - self._selection_box[0] == 1:
                                self._selection_box[1] = self._selection_box[0]
                            else:
                                self._selection_box[1] = max(self._selection_box[0], self._selection_box[1] - 1)
                    else:
                        if self._unselect_text():
                            break

                    # Move cursor
                    self._move_cursor_left()
                    self.active = True
                    updated = True

                # Up arrow
                elif self._ctrl.move_up(event, self):
                    self.active = False

                # Down arrow
                elif self._ctrl.move_down(event, self):
                    self.active = False

                # End
                elif self._ctrl.end(event, self):
                    self._sound.play_key_add()
                    self._cursor_position = len(self._input_string)
                    self._update_renderbox(end=True)
                    self._unselect_text()
                    self.active = True
                    updated = True

                # Home
                elif self._ctrl.home(event, self):
                    self._sound.play_key_add()
                    self._cursor_position = 0
                    self._update_renderbox(start=True)
                    self._unselect_text()
                    self.active = True
                    updated = True

                # Tab
                elif self._ctrl.tab(event, self):
                    for _ in range(self._tab_size):
                        self._push_key_input(' ')
                        updated = True
                    self.active = True

                # Enter
                elif self._ctrl.apply(event, self):
                    self._sound.play_open_menu()
                    self.apply()
                    self._unselect_text()
                    updated = True
                    self.active = not self.active

                # Escape
                elif self._ctrl.escape(event, self):
                    if self._get_selected_text():
                        self._unselect_text()
                        updated = True
                    elif self.active:
                        # Disable active status on the widget
                        self.active = False
                        updated = True

                # Press lshift, rshift -> selection
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    if not self._selection_active:
                        self._selection_active = True
                        self._selection_box[0] = self._cursor_position
                        self._selection_box[1] = self._cursor_position
                    self.active = True
                    break

                # Any other key, add as input
                elif event.key not in self._ignore_keys and hasattr(event, 'unicode'):
                    if event.unicode == ' ' and event.key != 32:
                        if self._verbose:
                            warn(
                                f'{self.get_class_id()} received "{event.unicode}" '
                                f'unicode but key is different than 32 ({event.key}), '
                                f'check if event has defined the proper unicode char'
                            )
                        break

                    # Error in char, not valid or string limit exceeds
                    if not self._push_key_input(event.unicode):
                        break
                    self.active = True
                    updated = True

            # User releases a key
            elif event.type == pygame.KEYUP and self._keyboard_enabled:
                # Because KEYUP doesn't include event.unicode, this dict is stored
                # in such a weird way
                if event.key in self._keyrepeat_counters:
                    del self._keyrepeat_counters[event.key]

                # If selection keys are released, stop selection
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self._selection_active = False

                # Release inputs
                self._block_copy_paste = False
                self._key_is_pressed = False

            # User releases the mouse button or finger; don't consider the mouse
            # wheel (button 4 & 5)
            elif event.type == pygame.MOUSEBUTTONUP and self._mouse_enabled and \
                    event.button in (1, 2, 3) or \
                    event.type == FINGERUP and self._touchscreen_enabled and self._menu is not None:
                event_pos = get_finger_pos(self._menu, event)
                if rect.collidepoint(*event_pos) and \
                        self.get_selected_time() > 1.5 * self._keyrepeat_mouse_interval_ms:
                    self._selection_active = False
                    self._check_mouse_collide_input(event_pos)
                    self._cursor_ms_counter = 0
                    self._cursor_visible = True

            # User press the mouse button or finger; don't consider the mouse
            # wheel (button 4 & 5)
            elif event.type == pygame.MOUSEBUTTONDOWN and self._mouse_enabled and \
                    event.button in (1, 2, 3) or \
                    event.type == FINGERDOWN and self._touchscreen_enabled:
                if self.get_selected_time() > self._keyrepeat_mouse_interval_ms or hasattr(event, 'test'):
                    if self._selection_active:
                        self._unselect_text()
                    self._cursor_ms_counter = 0
                    self._cursor_visible = True
                    self._selection_active = True
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self._selection_mouse_first_position = -1
                    self.active = True

        # Update mouse
        self._keyrepeat_mouse_ms += time_clock
        if self._keyrepeat_mouse_ms > self._keyrepeat_mouse_interval_ms:
            # self._keyrepeat_mouse_ms = 0
            if mouse_left:
                pos = pygame.mouse.get_pos()
                self._check_mouse_collide_input((pos[0], pos[1]))

        # Update key counters
        if self._keyrepeat:
            for key in self._keyrepeat_counters:
                self._keyrepeat_counters[key][0] += time_clock  # Update clock

                # Generate new key events if enough time has passed:
                if self._keyrepeat_counters[key][0] >= self._keyrepeat_initial_interval_ms:
                    self._keyrepeat_counters[key][0] = \
                        self._keyrepeat_initial_interval_ms - self._keyrepeat_interval_ms

                    event_key, event_unicode = key, self._keyrepeat_counters[key][1]
                    self._add_event(
                        pygame.event.Event(
                            pygame.KEYDOWN,
                            key=event_key,
                            unicode=event_unicode)
                    )

        return updated


class TextInputManager(AbstractWidgetManager, ABC):
    """
    TextInput manager.
    """

    def text_input(
            self,
            title: Any,
            default: Union[str, int, float] = '',
            copy_paste_enable: bool = True,
            cursor_selection_enable: bool = True,
            cursor_size: Optional[Tuple2IntType] = None,
            input_type: str = INPUT_TEXT,
            input_underline: str = '',
            input_underline_len: int = 0,
            maxchar: int = 0,
            maxwidth: int = 0,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            password: bool = False,
            textinput_id: str = '',
            valid_chars: Optional[List[str]] = None,
            **kwargs
    ) -> 'pygame_menu.widgets.TextInput':
        """
        Add a text input to the Menu: free text area and two functions that
        execute when changing the text and pressing return (apply) on the element.

        The callbacks receive the current value and all unknown keyword arguments,
        where ``current_text=widget.get_value``:

        .. code-block:: python

            onchange(current_text, **kwargs)
            onreturn(current_text, **kwargs)

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``history``                       (int) - Maximum number of editions stored. If ``0`` the feature is disabled. ``50`` by default
            - ``input_underline_vmargin``       (int) – Vertical margin of underline in px
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``maxwidth_dynamically_update``   (bool) - Dynamically update maxwidth depending on char size. ``True`` by default
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``password_char``                 (str) - Character used by password type. ``"*"`` by default
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``repeat_keys``                   (bool) - Enable key repeat. ``True`` by default
            - ``repeat_keys_initial_ms``        (int, float) - Time in milliseconds before keys are repeated when held in milliseconds. ``400`` by default
            - ``repeat_keys_interval_ms``       (int, float) - Interval between key press repetition when held in milliseconds. ``50`` by default
            - ``repeat_mouse_interval_ms``      (int, float) - Interval between mouse events when held in milliseconds. ``400`` by default
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``tab_size``                      (int) – Width of a tab character
            - ``text_ellipsis``                 (str) - Ellipsis text when overflow occurs (input length exceeds maxwidth). ``"..."`` by default

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the text input
        :param default: Default value to display
        :param copy_paste_enable: Enable text copy, paste and cut
        :param cursor_selection_enable: Enable text selection on input
        :param cursor_size: Size of the cursor (width, height) in px. If ``None`` uses the default sizing
        :param input_type: Data type of the input. See :py:mod:`pygame_menu.locals`
        :param input_underline: Underline character
        :param input_underline_len: Total of characters to be drawn under the input. If ``0`` this number is computed automatically to fit the font
        :param maxchar: Maximum length of string, if 0 there's no limit
        :param maxwidth: Maximum size of the text widget (in number of chars), if ``0`` there's no limit
        :param onchange: Callback executed when changing the text input
        :param onreturn: Callback executed when pressing return (apply) on the text input
        :param onselect: Callback executed when selecting the widget
        :param password: Text input is a password
        :param textinput_id: ID of the text input
        :param valid_chars: List of authorized chars. ``None`` if all chars are valid
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.TextInput`
        """
        assert isinstance(default, (str, NumberInstance))

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)
        input_underline_vmargin = kwargs.pop('input_underline_vmargin', 0)

        # If password is active no default value should exist
        if password and default != '':
            raise ValueError('default value must be empty if the input is a password')

        widget = pygame_menu.widgets.TextInput(
            copy_paste_enable=copy_paste_enable,
            cursor_color=self._theme.cursor_color,
            cursor_selection_color=self._theme.cursor_selection_color,
            cursor_selection_enable=cursor_selection_enable,
            cursor_size=cursor_size,
            cursor_switch_ms=self._theme.cursor_switch_ms,
            input_type=input_type,
            input_underline=input_underline,
            input_underline_len=input_underline_len,
            input_underline_vmargin=input_underline_vmargin,
            maxchar=maxchar,
            maxwidth=maxwidth,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            password=password,
            textinput_id=textinput_id,
            title=title,
            valid_chars=valid_chars,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        widget.set_default_value(default)

        return widget
