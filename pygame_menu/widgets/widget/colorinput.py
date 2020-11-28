# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

COLOR INPUT
Color input class, Widget created in top of TextInput that provides a textbox
for entering and previewing colors in RGB and HEX format.

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

import pygame
import pygame_menu.locals as _locals
from pygame_menu.utils import check_key_pressed_valid, make_surface, to_string
from pygame_menu.widgets.widget.textinput import TextInput

TYPE_HEX = 'hex'
TYPE_RGB = 'rgb'


class ColorInput(TextInput):  # lgtm [py/missing-call-to-init]
    """
    Color input widget.

    :param title: Color input title
    :type title: str
    :param colorinput_id: ID of the text input
    :type colorinput_id: str
    :param color_type: Type of color input (rgb, hex)
    :type color_type: str
    :param input_separator: Divisor between RGB channels
    :type input_separator: str
    :param input_underline: Character drawn under each number input
    :type input_underline: str
    :param cursor_color: Color of cursor
    :type cursor_color: tuple
    :param onchange: Callback when changing the selector
    :type onchange: callable, None
    :param onreturn: Callback when pressing return button
    :type onreturn: callable, None
    :param prev_size: Width of the previsualization box in terms of the height of the widget
    :type prev_size: int, float
    :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
    :type repeat_keys_initial_ms: int, float
    :param repeat_keys_interval_ms: Interval between key press repetition when held
    :type repeat_keys_interval_ms: int, float
    :param repeat_mouse_interval_ms: Interval between mouse events when held
    :type repeat_mouse_interval_ms: int, float
    :param kwargs: Optional keyword arguments
    :type kwargs: dict
    """

    def __init__(self,
                 title='',
                 colorinput_id='',
                 color_type=TYPE_RGB,
                 input_separator=',',
                 input_underline='_',
                 cursor_color=(0, 0, 0),
                 onchange=None,
                 onreturn=None,
                 prev_size=3,
                 repeat_keys_initial_ms=450,
                 repeat_keys_interval_ms=80,
                 repeat_mouse_interval_ms=100,
                 *args,
                 **kwargs):
        assert isinstance(colorinput_id, str)
        assert isinstance(color_type, str)
        assert isinstance(input_separator, str)
        assert isinstance(input_underline, str)
        assert isinstance(cursor_color, tuple)
        assert isinstance(repeat_keys_initial_ms, (int, float))
        assert isinstance(repeat_keys_interval_ms, (int, float))
        assert isinstance(repeat_mouse_interval_ms, (int, float))
        assert isinstance(prev_size, (int, float))

        assert len(input_separator) == 1, 'input_separator must be a single char'
        assert len(input_separator) != 0, 'input_separator cannot be empty'
        assert prev_size > 0, 'previsualization width must be greater than zero'
        assert input_separator not in ['0', '1', '2', '3', '4', '5', '6', '7', '8',
                                       '9'], 'input_separator cannot be a number'
        assert color_type in [TYPE_HEX, TYPE_RGB], 'color type must be "{0}" or "{1}"'.format(TYPE_HEX, TYPE_RGB)

        _maxchar = 0
        self._color_type = color_type.lower()  # type: str
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
            maxwidth=_maxwidth,  # Disabled
            onchange=onchange,
            onreturn=onreturn,
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
        self._separator = input_separator

        # Previsualization surface, if -1 previsualization does not show
        self._last_r = -1  # type: int
        self._last_g = -1  # type: int
        self._last_b = -1  # type: int
        self._previsualization_position = (0.0, 0.0)
        self._previsualization_surface = None  # type: (pygame.Surface,None)
        self._prev_size = prev_size  # type: int

    # noinspection PyMissingOrEmptyDocstring
    def clear(self):
        super(ColorInput, self).clear()
        self._previsualization_surface = None
        self._auto_separator_pos = []
        if self._color_type == TYPE_HEX:
            super(ColorInput, self).set_value('#')
        self.change()

    # noinspection PyMissingOrEmptyDocstring
    def set_value(self, color):
        _color = ''
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
            _color = '{0}{3}{1}{3}{2}'.format(r, g, b, self._separator)
            self._auto_separator_pos = [0, 1]
        elif self._color_type == TYPE_HEX:
            text = to_string(color).strip()
            if text == '':
                _color = '#'
            else:
                # Remove all invalid chars
                _valid_text = ''
                for ch in text:
                    if ch in self._valid_chars:
                        _valid_text += ch
                text = _valid_text

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
                _color = text

        super(ColorInput, self).set_value(_color)

    def get_value(self):
        """
        Return the color value as a tuple or red blue and green channels.
        If the data is invalid the widget returns (-1,-1,-1).

        :return: Color tuple as (R,G,B)
        :rtype: tuple
        """
        if self._color_type == TYPE_RGB:
            _color = self._input_string.split(self._separator)
            if len(_color) == 3 and _color[0] != '' and _color[1] != '' and _color[2] != '':
                r, g, b = int(_color[0]), int(_color[1]), int(_color[2])
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= g <= 255:
                    return r, g, b
        elif self._color_type == TYPE_HEX:
            if len(self._input_string) == 7:
                _color = self._input_string[1:]
                return tuple(int(_color[i:i + 2], 16) for i in (0, 2, 4))
        return -1, -1, -1

    def is_valid(self):
        """
        Return true if the current value of the input is a valid color or not.

        :return: True if valid
        :rtype: bool
        """
        r, g, b = self.get_value()
        if r == -1 or g == -1 or b == -1:
            return False
        return True

    def _previsualize_color(self, surface):
        """
        Changes the color of the previsualization box.

        :param surface: Surface to draw
        :type surface: :py:class:`pygame.surface.Surface`, None
        :return: None
        """
        r, g, b = self.get_value()
        if not self.is_valid():  # Remove previsualization if invalid color
            self._previsualization_surface = None
            return

        # If previsualization surface is None or the color changed
        if self._last_r != r or self._last_b != b or self._last_g != g or self._previsualization_surface is None:
            _width = self._prev_size * self._rect.height
            if _width == 0 or self._rect.height == 0:
                self._previsualization_surface = None
                return
            self._previsualization_surface = make_surface(_width, self._rect.height)
            self._previsualization_surface.fill((r, g, b))
            self._last_r = r
            self._last_g = g
            self._last_b = b
            _posx = self._rect.x + self._rect.width - self._prev_size * self._rect.height + self._rect.height / 10
            _posy = self._rect.y
            self._previsualization_position = (_posx, _posy)

        # Draw the surface
        if surface is not None:
            surface.blit(self._previsualization_surface, self._previsualization_position)

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface):
        super(ColorInput, self).draw(surface)  # This calls _render()
        self._previsualize_color(surface)

    def _render(self):
        super(ColorInput, self)._render()

        # Maybe TextInput did not rendered, so this has to be changed
        self._rect.width, self._rect.height = self._surface.get_size()
        self._rect.width += self._prev_size * self._rect.height  # Adds the previsualization size to the box

    # noinspection PyMissingOrEmptyDocstring
    def update(self, events):
        _input = self._input_string
        _curpos = self._cursor_position
        _disable_remove_separator = True

        key = ''  # Pressed key
        if self._color_type == TYPE_RGB:
            for event in events:  # type: pygame.event.Event
                if event.type == pygame.KEYDOWN:

                    # Check if any key is pressed, if True the event is invalid
                    if not check_key_pressed_valid(event):
                        return True

                    if _disable_remove_separator and len(_input) > 0 and len(_input) > _curpos and (
                            '{0}{0}'.format(self._separator) not in _input or
                            _input[_curpos] == self._separator and len(_input) == _curpos + 1
                    ):

                        # Backspace button, delete text from right
                        if event.key == pygame.K_BACKSPACE:
                            if len(_input) >= 1 and _input[_curpos - 1] == self._separator:
                                return True

                        # Delete button, delete text from left
                        elif event.key == pygame.K_DELETE:
                            if _input[_curpos] == self._separator:
                                return True

                    # Verify only on user key input, the rest of events are checked by TextInput on super call
                    key = str(event.unicode)
                    if key in self._valid_chars:

                        _new_string = (
                                self._input_string[:self._cursor_position]
                                + key
                                + self._input_string[self._cursor_position:]
                        )

                        # Cannot be separator at first
                        if len(_input) == 0 and key == self._separator:
                            return False

                        if len(_input) > 1:

                            # Check separators
                            if key == self._separator:

                                # If more than 2 separators
                                _total_separator = 0
                                for _ch in _input:
                                    if _ch == self._separator:
                                        _total_separator += 1
                                if _total_separator >= 2:
                                    return False

                            # Check the number between the current separators, this number must be between 0-255
                            if key != self._separator:
                                _pos_before = 0
                                _pos_after = 0
                                for _i in range(_curpos):
                                    if _new_string[_curpos - _i - 1] == self._separator:
                                        _pos_before = _curpos - _i
                                        break
                                for _i in range(len(_new_string) - _curpos):
                                    if _new_string[_curpos + _i] == self._separator:
                                        _pos_after = _curpos + _i
                                        break
                                if _pos_after == 0:
                                    _pos_after = len(_new_string)
                                _num = _new_string[_pos_before:_pos_after].replace(',', '')
                                if _num == '':
                                    _num = '0'

                                if int(_num) > 255:  # Number exceeds 25X
                                    return False
                                if _num != str(int(_num)) and key == '0':  # User adds 0 at left, example: 12 -> 012
                                    return False
                                if len(_num) > 3:  # Number like 0XXX
                                    return False

        elif self._color_type == TYPE_HEX:
            for event in events:  # type: pygame.event.Event
                if event.type == pygame.KEYDOWN:

                    # Check if any key is pressed, if True the event is invalid
                    if not check_key_pressed_valid(event):
                        return True

                    # Backspace button, delete text from right
                    if event.key == pygame.K_BACKSPACE:
                        if _curpos == 1:
                            return True

                    # Delete button, delete text from left
                    elif event.key == pygame.K_DELETE:
                        if _curpos == 0:
                            return True

                    # Verify only on user key input, the rest of events are checked by TextInput on super call
                    key = str(event.unicode)
                    if key in self._valid_chars:
                        if key == '#':
                            return True
                        if _curpos == 0:
                            return True

        # Update
        updated = super(ColorInput, self).update(events)

        # After
        if self._color_type == TYPE_RGB:

            _total_separator = 0
            for _ch in _input:
                if _ch == self._separator:
                    _total_separator += 1

            # Adds auto separator
            if key == '0' and len(self._input_string) == self._cursor_position and _total_separator < 2 and \
                    (len(self._input_string) == 1 or
                     (len(self._input_string) > 2 and self._input_string[
                         self._cursor_position - 2] == self._separator)):
                self._push_key_input(self._separator, sounds=False)  # This calls .onchange()

            # Check number is valid (fix) because sometimes the user can type
            # too fast and avoid analysis of the text
            colors = self._input_string.split(self._separator)
            for c in colors:
                if len(c) > 0 and (int(c) > 255 or int(c) < 0):
                    self._input_string = _input
                    self._cursor_position = _curpos
                    break

            if len(colors) == 3:
                self._auto_separator_pos = [0, 1]

            # Add an auto separator if the number can't continue growing and the cursor
            # is at the end of the line
            if _total_separator < 2 and len(self._input_string) == self._cursor_position:
                autopos = len(colors) - 1
                last_num = colors[autopos]
                if (len(last_num) == 2 and int(last_num) > 25 or len(last_num) == 3 and int(last_num) <= 255) and \
                        autopos not in self._auto_separator_pos:
                    self._push_key_input(self._separator, sounds=False)  # This calls .onchange()
                    self._auto_separator_pos.append(autopos)

            # If the user cleared all the string, reset auto separator
            if _total_separator == 0 and \
                    (len(self._input_string) < 2 or len(self._input_string) == 2 and int(colors[0]) <= 25):
                self._auto_separator_pos = []

        return updated
