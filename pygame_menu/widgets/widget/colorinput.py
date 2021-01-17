"""
pygame-menu
https://github.com/ppizarror/pygame-menu

COLOR INPUT
Color input class, Widget created in top of TextInput that provides a textbox
for entering and previewing colors in RGB and HEX format.

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

    # Constants
    'TYPE_HEX',
    'TYPE_RGB',
    'HEX_FORMAT_LOWER',
    'HEX_FORMAT_NONE',
    'HEX_FORMAT_UPPER',

    # Main class
    'ColorInput'

]

import pygame
import pygame_menu.locals as _locals
from pygame_menu.utils import check_key_pressed_valid, make_surface
from pygame_menu.widgets.widget.textinput import TextInput
from pygame_menu.custom_types import Union, Tuple, List, NumberType, Any, Optional, \
    CallbackType, Tuple2IntType

ColorType = Tuple[int, int, int]

# Input modes
TYPE_HEX = 'hex'
TYPE_RGB = 'rgb'

# Apply format to hex color string
HEX_FORMAT_LOWER = 'lower'
HEX_FORMAT_NONE = 'none'
HEX_FORMAT_UPPER = 'upper'


# noinspection PyMissingOrEmptyDocstring
class ColorInput(TextInput):  # lgtm [py/missing-call-to-init]
    """
    Color input widget.

    The callbacks receive the current value and all unknown keyword
    arguments, where ``current_color=widget.get_value()``:

    .. code-block:: python

        onchange(current_color, **kwargs)
        onreturn(current_color, **kwargs)

    .. note::

        This widget implements the same transformations as :py:class:`pygame_menu.widgets.widget.TextInput`.

    :param title: Color input title
    :param colorinput_id: ID of the text input
    :param color_type: Type of color input ``(rgb, hex)``
    :param hex_format: Hex format string mode ``(none, lower, upper)``
    :param input_separator: Divisor between RGB channels
    :param input_underline: Character drawn under each number input
    :param cursor_color: Color of cursor
    :param onchange: Function when changing the values of the color text
    :param onreturn: Function when pressing return on the color text input
    :param onselect: Function when selecting the widget
    :param prev_margin: Horizontal margin between the previsualization and the input text (px)
    :param prev_width_factor: Width of the previsualization box in terms of the height of the widget
    :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
    :param repeat_keys_interval_ms: Interval between key press repetition when held
    :param repeat_mouse_interval_ms: Interval between mouse events when held
    :param kwargs: Optional keyword arguments
    """
    _auto_separator_pos: List[int]
    _color_type: str
    _hex_format: str
    _last_g: int
    _last_r: int
    _prev_margin: int
    _previsualization_position: Tuple2IntType
    _previsualization_surface: Optional['pygame.Surface']
    _rect_width: int
    _separator: str
    _valid_chars: List[str]

    def __init__(self,
                 title: Any = '',
                 colorinput_id: str = '',
                 color_type: str = TYPE_RGB,
                 hex_format: str = HEX_FORMAT_NONE,
                 input_separator: str = ',',
                 input_underline: str = '_',
                 cursor_color: ColorType = (0, 0, 0),
                 onchange: CallbackType = None,
                 onreturn: CallbackType = None,
                 onselect: CallbackType = None,
                 prev_margin: int = 0,
                 prev_width_factor: NumberType = 3,
                 repeat_keys_initial_ms: NumberType = 450,
                 repeat_keys_interval_ms: NumberType = 80,
                 repeat_mouse_interval_ms: NumberType = 100,
                 *args,
                 **kwargs
                 ) -> None:
        assert isinstance(color_type, str)
        assert isinstance(colorinput_id, str)
        assert isinstance(cursor_color, tuple)
        assert isinstance(hex_format, str)
        assert isinstance(input_separator, str)
        assert isinstance(input_underline, str)
        assert isinstance(prev_margin, int)
        assert isinstance(prev_width_factor, (int, float))
        assert isinstance(repeat_keys_initial_ms, (int, float))
        assert isinstance(repeat_keys_interval_ms, (int, float))
        assert isinstance(repeat_mouse_interval_ms, (int, float))

        assert len(input_separator) == 1, 'input_separator must be a single char'
        assert len(input_separator) != 0, 'input_separator cannot be empty'
        assert prev_width_factor > 0, 'previsualization width factor must be greater than zero'
        assert input_separator not in ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                       '9'], 'input_separator cannot be a number'
        assert color_type in [TYPE_HEX, TYPE_RGB], \
            'color type must be "{0}" or "{1}"'.format(TYPE_HEX, TYPE_RGB)
        assert hex_format in [HEX_FORMAT_NONE, HEX_FORMAT_LOWER, HEX_FORMAT_UPPER], \
            'invalid hex format mode, it must be "none", "lower" or "upper"'

        _maxchar = 0
        self._color_type = color_type.lower()
        if self._color_type == TYPE_RGB:
            _maxchar = 11  # RRR,GGG,BBB
            self._valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', input_separator]
        elif self._color_type == TYPE_HEX:
            _maxchar = 7  # #XXYYZZ
            self._valid_chars = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', '0', '1', '2', '3', '#',
                                 '4', '5', '6', '7', '8', '9']

        _input_type = _locals.INPUT_TEXT
        _maxwidth = 0
        _password = False

        super(ColorInput, self).__init__(
            title=title,
            textinput_id=colorinput_id,
            input_type=_input_type,
            input_underline=input_underline,
            cursor_color=cursor_color,
            copy_paste_enable=False,
            cursor_selection_enable=False,
            history=0,
            maxchar=_maxchar,
            maxwidth=_maxwidth,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            password=_password,
            repeat_keys_initial_ms=repeat_keys_initial_ms,
            repeat_keys_interval_ms=repeat_keys_interval_ms,
            repeat_mouse_interval_ms=repeat_mouse_interval_ms,
            tab_size=0,
            text_ellipsis='',
            valid_chars=self._valid_chars,
            *args,
            **kwargs
        )

        # Store inner variables
        self._auto_separator_pos = []  # This stores indexes of auto separator added
        self._hex_format = hex_format
        self._separator = input_separator

        # Previsualization surface, if -1 previsualization does not show
        self._last_b = -1
        self._last_g = -1
        self._last_r = -1
        self._prev_margin = prev_margin
        self._prev_width_factor = prev_width_factor
        self._previsualization_position = (0, 0)
        self._previsualization_surface = None

        # Disable parent callbacks
        self._apply_widget_update_callback = False
        self._apply_widget_draw_callback = False

    def clear(self) -> None:
        super(ColorInput, self).clear()
        self._previsualization_surface = None
        self._auto_separator_pos = []
        if self._color_type == TYPE_HEX:
            super(ColorInput, self).set_value('#')
        self.change()

    def set_value(self, color: Union[str, ColorType]) -> None:
        format_color = ''
        if self._color_type == TYPE_RGB:
            if color == '':
                super(ColorInput, self).set_value('')
                return
            assert isinstance(color, tuple), 'color in rgb format must be a tuple in (r,g,b) format'
            assert len(color) == 3, 'tuple must contain only 3 colors, R,G,B'
            r, g, b = color
            assert isinstance(r, int), 'red color must be an integer'
            assert isinstance(g, int), 'blue color must be an integer'
            assert isinstance(b, int), 'green color must be an integer'
            assert 0 <= r <= 255, 'red color must be between 0 and 255'
            assert 0 <= g <= 255, 'blue color must be between 0 and 255'
            assert 0 <= b <= 255, 'green color must be between 0 and 255'
            format_color = '{0}{3}{1}{3}{2}'.format(r, g, b, self._separator)
            self._auto_separator_pos = [0, 1]
        elif self._color_type == TYPE_HEX:
            text = str(color).strip()
            if text == '':
                format_color = '#'
            else:
                # Remove all invalid chars
                valid_text = ''
                for ch in text:
                    if ch in self._valid_chars:
                        valid_text += ch
                text = valid_text

                # Check if the color is valid
                count_hash = 0
                for ch in text:
                    if ch == '#':
                        count_hash += 1
                if count_hash == 1:
                    assert text[0] == '#', 'color format must be "#RRGGBB"'
                if count_hash == 0:
                    text = '#' + text
                assert len(text) == 7, 'invalid color, only formats "#RRGGBB" and "RRGGBB" are allowed'
                format_color = text

        super(ColorInput, self).set_value(format_color)
        self._format_hex()

    def get_value(self, as_string: bool = False) -> Union[str, ColorType]:
        """
        Return the color value as a tuple or red blue and green channels.

        .. note::

            If the data is invalid the widget returns ``(-1,-1,-1)``.

        :param as_string: If ``True`` returns the widget value as plain text
        :return: Color tuple as (R,G,B) or color string
        """
        assert isinstance(as_string, bool)
        if as_string:
            return self._input_string
        if self._color_type == TYPE_RGB:
            color = self._input_string.split(self._separator)
            if len(color) == 3 and color[0] != '' and color[1] != '' and color[2] != '':
                r, g, b = int(color[0]), int(color[1]), int(color[2])
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= g <= 255:
                    return r, g, b
        elif self._color_type == TYPE_HEX:
            if len(self._input_string) == 7:
                color = self._input_string[1:]
                color = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
                return color[0], color[1], color[2]
        return -1, -1, -1

    def is_valid(self) -> bool:
        """
        Return ``True`` if the current value of the input is a valid color or not.

        :return: ``True`` if valid
        """
        r, g, b = self.get_value()
        if r == -1 or g == -1 or b == -1:
            return False
        return True

    def _draw_previsualize_color(self, surface: Optional['pygame.Surface']) -> None:
        """
        Changes the color of the previsualization box.

        :param surface: Surface to draw
        :return: None
        """
        r, g, b = self.get_value()
        if not self.is_valid():  # Remove previsualization if invalid color
            self._previsualization_surface = None
            return

        # If previsualization surface is None or the color changed
        if self._last_r != r or self._last_b != b or self._last_g != g or self._previsualization_surface is None:
            _width = self._prev_width_factor * self._rect.height
            if _width == 0 or self._rect.height == 0:
                self._previsualization_surface = None
                return
            self._previsualization_surface = make_surface(_width, self._rect.height)
            self._previsualization_surface.fill((r, g, b))
            self._last_r = r
            self._last_g = g
            self._last_b = b
            _posx = self._rect.x + self._rect.width - self._prev_width_factor * self._rect.height + self._rect.height / 10
            _posy = self._rect.y
            self._previsualization_position = (int(_posx), int(_posy))
            self._force_render()

        # Draw the surface
        if surface is not None:
            surface.blit(self._previsualization_surface, self._previsualization_position)

    def draw(self, surface: 'pygame.Surface') -> None:
        super(ColorInput, self).draw(surface)  # This calls _render()
        self._draw_previsualize_color(surface)
        self.apply_draw_callbacks()

    def _render(self) -> Optional[bool]:
        r = super(ColorInput, self)._render()

        # Maybe TextInput did not rendered, so this has to be changed
        self._rect.width, self._rect.height = self._surface.get_size()
        self._rect.width += self._prev_width_factor * self._rect.height + self._prev_margin

        # Force previsualization rendering
        if not r:
            self._previsualization_surface = None

        return r

    def _format_hex(self) -> None:
        """
        Apply hex format.

        :return: None
        """
        if self._color_type != TYPE_HEX or self._hex_format == HEX_FORMAT_NONE:
            return
        elif self._hex_format == HEX_FORMAT_LOWER:
            self._input_string = self._input_string.lower()
        elif self._hex_format == HEX_FORMAT_UPPER:
            self._input_string = self._input_string.upper()

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        if self.readonly:
            return False
        input_str = self._input_string
        cursor_pos = self._cursor_position
        disable_remove_separator = True

        key = ''  # Pressed key
        if self._color_type == TYPE_RGB:
            for event in events:
                if event.type == pygame.KEYDOWN:

                    # Check if any key is pressed, if True the event is invalid
                    if not check_key_pressed_valid(event):
                        return True

                    if disable_remove_separator and len(input_str) > 0 and len(input_str) > cursor_pos and (
                            '{0}{0}'.format(self._separator) not in input_str or
                            input_str[cursor_pos] == self._separator and len(input_str) == cursor_pos + 1
                    ):

                        # Backspace button, delete text from right
                        if event.key == pygame.K_BACKSPACE:
                            if len(input_str) >= 1 and input_str[cursor_pos - 1] == self._separator:
                                return True

                        # Delete button, delete text from left
                        elif event.key == pygame.K_DELETE:
                            if input_str[cursor_pos] == self._separator:
                                return True

                    # Verify only on user key input, the rest of events are checked by TextInput on super call
                    key = str(event.unicode)
                    if key in self._valid_chars:

                        new_string = (
                                self._input_string[:self._cursor_position]
                                + key
                                + self._input_string[self._cursor_position:]
                        )

                        # Cannot be separator at first
                        if len(input_str) == 0 and key == self._separator:
                            return False

                        if len(input_str) > 1:

                            # Check separators
                            if key == self._separator:

                                # If more than 2 separators
                                total_separator = 0
                                for ch in input_str:
                                    if ch == self._separator:
                                        total_separator += 1
                                if total_separator >= 2:
                                    return False

                            # Check the number between the current separators, this number must be between 0-255
                            if key != self._separator:
                                pos_before = 0
                                pos_after = 0
                                for i in range(cursor_pos):
                                    if new_string[cursor_pos - i - 1] == self._separator:
                                        pos_before = cursor_pos - i
                                        break
                                for i in range(len(new_string) - cursor_pos):
                                    if new_string[cursor_pos + i] == self._separator:
                                        pos_after = cursor_pos + i
                                        break
                                if pos_after == 0:
                                    pos_after = len(new_string)
                                num = new_string[pos_before:pos_after].replace(',', '')
                                if num == '':
                                    num = '0'

                                if int(num) > 255:  # Number exceeds 25X
                                    return False
                                if num != str(int(num)) and key == '0':  # User adds 0 at left, example: 12 -> 012
                                    return False
                                if len(num) > 3:  # Number like 0XXX
                                    return False

        elif self._color_type == TYPE_HEX:
            self._format_hex()

            for event in events:
                if event.type == pygame.KEYDOWN:

                    # Check if any key is pressed, if True the event is invalid
                    if not check_key_pressed_valid(event):
                        return True

                    # Backspace button, delete text from right
                    if event.key == pygame.K_BACKSPACE:
                        if cursor_pos == 1:
                            return True

                    # Delete button, delete text from left
                    elif event.key == pygame.K_DELETE:
                        if cursor_pos == 0:
                            return True

                    # Verify only on user key input, the rest of events are checked by TextInput on super call
                    key = str(event.unicode)
                    if key in self._valid_chars:
                        if key == '#':
                            return True
                        if cursor_pos == 0:
                            return True

        # Update
        updated = super(ColorInput, self).update(events)

        # After
        if self._color_type == TYPE_RGB:

            total_separator = 0
            for ch in input_str:
                if ch == self._separator:
                    total_separator += 1

            # Adds auto separator
            if key == '0' and len(self._input_string) == self._cursor_position and total_separator < 2 and \
                    (len(self._input_string) == 1 or
                     (len(self._input_string) > 2 and self._input_string[
                         self._cursor_position - 2] == self._separator)):
                self._push_key_input(self._separator, sounds=False)  # This calls .onchange()

            # Check number is valid (fix) because sometimes the user can type
            # too fast and avoid analysis of the text
            colors = self._input_string.split(self._separator)
            for c in colors:
                if len(c) > 0 and (int(c) > 255 or int(c) < 0):
                    self._input_string = input_str
                    self._cursor_position = cursor_pos
                    break

            if len(colors) == 3:
                self._auto_separator_pos = [0, 1]

            # Add an auto separator if the number can't continue growing and the cursor
            # is at the end of the line
            if total_separator < 2 and len(self._input_string) == self._cursor_position:
                autopos = len(colors) - 1
                last_num = colors[autopos]
                if (len(last_num) == 2 and int(last_num) > 25 or len(last_num) == 3 and int(last_num) <= 255) and \
                        autopos not in self._auto_separator_pos:
                    self._push_key_input(self._separator, sounds=False)  # This calls .onchange()
                    self._auto_separator_pos.append(autopos)

            # If the user cleared all the string, reset auto separator
            if total_separator == 0 and \
                    (len(self._input_string) < 2 or len(self._input_string) == 2 and int(colors[0]) <= 25):
                self._auto_separator_pos = []

        if updated:
            self.apply_update_callbacks()

        return updated
