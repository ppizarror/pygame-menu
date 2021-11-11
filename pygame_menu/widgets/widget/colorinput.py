"""
pygame-menu
https://github.com/ppizarror/pygame-menu

COLOR INPUT
Color input class, Widget created in top of TextInput that provides a textbox
for entering and previewing colors in RGB and HEX format.
"""

__all__ = [

    # Main class
    'ColorInput',
    'ColorInputManager',

    # Constants
    'COLORINPUT_TYPE_HEX',
    'COLORINPUT_TYPE_RGB',
    'COLORINPUT_HEX_FORMAT_LOWER',
    'COLORINPUT_HEX_FORMAT_NONE',
    'COLORINPUT_HEX_FORMAT_UPPER',

    # Type
    'ColorInputColorType',
    'ColorInputHexFormatType'

]

import math
import pygame
import pygame_menu

from abc import ABC
from pygame_menu.locals import INPUT_TEXT
from pygame_menu.utils import check_key_pressed_valid, make_surface
from pygame_menu.widgets.core.widget import AbstractWidgetManager, Widget
from pygame_menu.widgets.widget.textinput import TextInput

from pygame_menu._types import Union, List, NumberType, Any, Optional, CallbackType, \
    Literal, Tuple3IntType, NumberInstance, EventVectorType, Callable

# Input modes
COLORINPUT_TYPE_HEX = 'hex'
COLORINPUT_TYPE_RGB = 'rgb'

# Apply format to hex color string
COLORINPUT_HEX_FORMAT_LOWER = 'lower'
COLORINPUT_HEX_FORMAT_NONE = 'none'
COLORINPUT_HEX_FORMAT_UPPER = 'upper'

# Custom typing
ColorInputColorType = Literal[COLORINPUT_TYPE_RGB, COLORINPUT_TYPE_HEX]
ColorInputHexFormatType = Literal[COLORINPUT_HEX_FORMAT_LOWER,
                                  COLORINPUT_HEX_FORMAT_UPPER,
                                  COLORINPUT_HEX_FORMAT_NONE]


# noinspection PyMissingOrEmptyDocstring
class ColorInput(TextInput):  # lgtm [py/missing-call-to-init]
    """
    Color input widget.

    The callbacks receive the current value and all unknown keyword arguments,
    where ``current_color=widget.get_value()``:

    .. code-block:: python

        onchange(current_color, **kwargs)
        onreturn(current_color, **kwargs)

    .. note::

        This widget cannot select text as :py:class:`pygame_menu.widgets.TextInput`
        does. Also, copy and paste is disabled.

    .. note::

        ColorInput accepts the same transformations as :py:class:`pygame_menu.widgets.TextInput`.

    :param title: Color input title
    :param colorinput_id: ID of the text input
    :param color_type: Type of color input
    :param cursor_switch_ms: Interval of cursor switch between off and on status. First status is ``off``
    :param dynamic_width: If ``True`` the widget width changes if the previsualization color box is active or not
    :param hex_format: Hex format string mode
    :param input_separator: Divisor between RGB channels
    :param input_underline: Character drawn under each number input
    :param input_underline_vmargin: Vertical margin of underline in px
    :param cursor_color: Color of cursor
    :param onchange: Function when changing the values of the color text
    :param onreturn: Function when pressing return on the color text input
    :param onselect: Function when selecting the widget
    :param prev_margin: Horizontal margin between the previsualization and the input text in px
    :param prev_width_factor: Width of the previsualization box in terms of the height of the widget
    :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
    :param repeat_keys_interval_ms: Interval between key press repetition when held
    :param repeat_mouse_interval_ms: Interval between mouse events when held
    :param kwargs: Optional keyword arguments
    """
    _auto_separator_pos: List[int]
    _color_type: str
    _dynamic_width: bool
    _hex_format: str
    _last_g: int
    _last_r: int
    _prev_margin: int
    _previsualization_surface: Optional['pygame.Surface']
    _separator: str

    def __init__(
            self,
            title: Any,
            colorinput_id: str = '',
            color_type: ColorInputColorType = COLORINPUT_TYPE_RGB,
            cursor_color: Tuple3IntType = (0, 0, 0),
            cursor_switch_ms: NumberType = 500,
            dynamic_width: bool = True,
            hex_format: ColorInputHexFormatType = COLORINPUT_HEX_FORMAT_NONE,
            input_separator: str = ',',
            input_underline: str = '_',
            input_underline_vmargin: int = 0,
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: CallbackType = None,
            prev_margin: int = 10,
            prev_width_factor: NumberType = 3,
            repeat_keys_initial_ms: NumberType = 450,
            repeat_keys_interval_ms: NumberType = 80,
            repeat_mouse_interval_ms: NumberType = 100,
            *args,
            **kwargs
    ) -> None:
        assert isinstance(color_type, str)
        assert isinstance(colorinput_id, str)
        assert isinstance(dynamic_width, bool)
        assert isinstance(hex_format, str)
        assert isinstance(input_separator, str)
        assert isinstance(input_underline, str)
        assert isinstance(prev_margin, int)
        assert isinstance(prev_width_factor, NumberInstance)

        assert len(input_separator) == 1, 'input_separator must be a single char'
        assert len(input_separator) != 0, 'input_separator cannot be empty'
        assert prev_width_factor > 0, \
            'previsualization width factor must be greater than zero'
        assert input_separator not in ('0', '1', '2', '3', '4', '5', '6', '7', '8',
                                       '9'), 'input_separator cannot be a number'
        assert color_type in (COLORINPUT_TYPE_HEX, COLORINPUT_TYPE_RGB), \
            f'color type must be "{COLORINPUT_TYPE_HEX}" or "{COLORINPUT_TYPE_RGB}"'
        assert hex_format in (COLORINPUT_HEX_FORMAT_NONE, COLORINPUT_HEX_FORMAT_LOWER,
                              COLORINPUT_HEX_FORMAT_UPPER), \
            'invalid hex format mode, it must be "none", "lower" or "upper"'

        _maxchar = 0
        self._color_type = color_type.lower()
        if self._color_type == COLORINPUT_TYPE_RGB:
            _maxchar = 11  # RRR,GGG,BBB
            self._valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                                 input_separator]
        elif self._color_type == COLORINPUT_TYPE_HEX:
            _maxchar = 7  # #XXYYZZ
            self._valid_chars = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E',
                                 'f', 'F', '#', '0', '1', '2', '3', '4', '5', '6',
                                 '7', '8', '9']

        # noinspection PyArgumentEqualDefault
        super(ColorInput, self).__init__(
            copy_paste_enable=False,
            cursor_color=cursor_color,
            cursor_switch_ms=cursor_switch_ms,
            cursor_selection_enable=False,
            history=0,
            input_type=INPUT_TEXT,
            input_underline=input_underline,
            input_underline_vmargin=input_underline_vmargin,
            maxchar=_maxchar,
            maxwidth=0,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            password=False,
            repeat_keys_initial_ms=repeat_keys_initial_ms,
            repeat_keys_interval_ms=repeat_keys_interval_ms,
            repeat_mouse_interval_ms=repeat_mouse_interval_ms,
            text_ellipsis='',
            textinput_id=colorinput_id,
            title=title,
            valid_chars=self._valid_chars,
            *args,
            **kwargs
        )

        # Store inner variables
        self._auto_separator_pos = []  # This stores indexes of auto separator added
        self._dynamic_width = dynamic_width
        self._hex_format = hex_format
        self._separator = input_separator

        # Previsualization surface, if -1 does not show
        self._last_b = -1
        self._last_g = -1
        self._last_r = -1
        self._prev_margin = prev_margin
        self._prev_width_factor = prev_width_factor
        self._previsualization_surface = None

        # Disable parent callbacks
        self._apply_widget_update_callback = False

        # Disable alt+x
        self._alt_x_enabled = False

    def _apply_font(self) -> None:
        super(ColorInput, self)._apply_font()

        # Compute the size of the underline
        if self._input_underline != '':
            max_width = 0  # Max expected width
            if self._color_type == COLORINPUT_TYPE_RGB:
                max_width = self._font_render_string(
                    f'255{self._separator}255{self._separator}255'
                ).get_width()
            else:
                for i in ('a', 'b', 'c', 'd', 'e', 'f'):
                    max_width = max(
                        max_width,
                        self._font_render_string(f'#{i * 6}').get_width()
                    )

            char = math.ceil(max_width / self._input_underline_size)
            for i in range(10):  # Find the best guess for
                fw = self._font_render_string(self._input_underline * int(char)).get_width()
                char += 1
                if fw >= max_width:
                    break

            self._input_underline_len = char

    def clear(self) -> None:
        super(ColorInput, self).clear()
        self._previsualization_surface = None
        self._auto_separator_pos = []
        if self._color_type == COLORINPUT_TYPE_HEX:
            super(ColorInput, self).set_value('#')
        self.change()

    def set_value(self, color: Optional[Union[str, Tuple3IntType]]) -> None:
        """
        Set the color value.

        :param color: A string if the type is HEX, or a (r, g, b) tuple if RGB
        :return: None
        """
        if color is None:
            color = ''
        format_color = ''
        if self._color_type == COLORINPUT_TYPE_RGB:
            if color == '':
                super(ColorInput, self).set_value('')
                return
            assert isinstance(color, tuple), \
                'color in rgb format must be a tuple in (r,g,b) format'
            assert len(color) == 3, 'tuple must contain only 3 colors, R,G,B'
            r, g, b = color
            assert isinstance(r, int), 'red color must be an integer'
            assert isinstance(g, int), 'blue color must be an integer'
            assert isinstance(b, int), 'green color must be an integer'
            assert 0 <= r <= 255, 'red color must be between 0 and 255'
            assert 0 <= g <= 255, 'blue color must be between 0 and 255'
            assert 0 <= b <= 255, 'green color must be between 0 and 255'
            format_color = f'{r}{self._separator}{g}{self._separator}{b}'
            self._auto_separator_pos = [0, 1]

        elif self._color_type == COLORINPUT_TYPE_HEX:
            text = str(color).strip()
            if text == '' or text == '#':
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
                assert len(text) == 7, \
                    'invalid color, only formats "#RRGGBB" or "RRGGBB" are allowed'
                format_color = text

        super(ColorInput, self).set_value(format_color)
        self._format_hex()

    def value_changed(self) -> bool:
        default = self._default_value
        if self._color_type == COLORINPUT_TYPE_HEX and '#' not in default:
            default = '#' + default
        return self.get_value(as_string=True) != default

    def get_value(self, as_string: bool = False) -> Union[str, Tuple3IntType]:
        """
        Return the color value as a tuple or red blue and green channels.

        .. note::

            If the data is invalid the widget returns ``(-1, -1, -1)``.

        :param as_string: If ``True`` returns the widget value as plain text
        :return: Color tuple as (R, G, B) or color string
        """
        assert isinstance(as_string, bool)
        if as_string:
            return self._input_string

        if self._color_type == COLORINPUT_TYPE_RGB:
            color = self._input_string.split(self._separator)
            if len(color) == 3 and color[0] != '' and color[1] != '' and color[2] != '':
                r, g, b = int(color[0]), int(color[1]), int(color[2])
                if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= g <= 255:
                    return r, g, b

        elif self._color_type == COLORINPUT_TYPE_HEX:
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

    def _draw(self, surface: 'pygame.Surface') -> None:
        super(ColorInput, self)._draw(surface)  # This calls _render()

        # Draw previsualization box
        if self._previsualization_surface is not None:
            posx = self._rect.x + self._rect.width \
                   - self._prev_width_factor * self._rect.height \
                   + self._rect.height / 10
            posy = self._rect.y
            surface.blit(self._previsualization_surface, (int(posx), int(posy)))

    def _render(self) -> Optional[bool]:
        render_text = super(ColorInput, self)._render()

        # Maybe TextInput did not rendered, so this has to be changed
        self._rect.width, self._rect.height = self._surface.get_size()
        if not self._dynamic_width or \
                (self._dynamic_width and self._previsualization_surface is not None):
            self._rect.width += self._prev_width_factor * self._rect.height \
                                + self._prev_margin

        # Render the previsualization box
        r, g, b = self.get_value()
        if not self.is_valid():  # Remove previsualization if invalid color
            self._previsualization_surface = None
            return render_text

        # If previsualization surface is None or the color changed
        if self._last_r != r or self._last_b != b or self._last_g != g or \
                self._previsualization_surface is None:
            width = self._prev_width_factor * self._rect.height
            if width == 0 or self._rect.height == 0:
                self._previsualization_surface = None
            else:
                self._previsualization_surface = make_surface(width, self._rect.height)
                self._previsualization_surface.fill((r, g, b))
                self._last_r = r
                self._last_g = g
                self._last_b = b
                if self._dynamic_width:
                    self._rect.width += self._prev_width_factor * self._rect.height \
                                        + self._prev_margin

        return render_text

    def _format_hex(self) -> None:
        """
        Apply hex format.

        :return: None
        """
        if self._color_type != COLORINPUT_TYPE_HEX or \
                self._hex_format == COLORINPUT_HEX_FORMAT_NONE:
            return
        elif self._hex_format == COLORINPUT_HEX_FORMAT_LOWER:
            self._input_string = self._input_string.lower()
        elif self._hex_format == COLORINPUT_HEX_FORMAT_UPPER:
            self._input_string = self._input_string.upper()

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)

        if self.readonly or not self.is_visible():
            self._readonly_check_mouseover(events)
            return False

        input_str = self._input_string
        cursor_pos = self._cursor_position
        disable_remove_separator = True

        key = ''  # Pressed key

        if self._color_type == COLORINPUT_TYPE_RGB:
            for event in events:

                # User writes
                if event.type == pygame.KEYDOWN and self._keyboard_enabled:
                    # Check if any key is pressed
                    if self._ignores_keyboard_nonphysical() and not check_key_pressed_valid(event):
                        continue

                    if disable_remove_separator and len(input_str) > 0 and \
                            len(input_str) > cursor_pos and (
                            f'{self._separator}{self._separator}' not in input_str or
                            input_str[cursor_pos] == self._separator and
                            len(input_str) == cursor_pos + 1
                    ):
                        # Backspace button, delete text from right
                        if event.key == pygame.K_BACKSPACE:
                            if len(input_str) >= 1 and \
                                    input_str[cursor_pos - 1] == self._separator:
                                return True

                        # Delete button, delete text from left
                        elif event.key == pygame.K_DELETE:
                            if input_str[cursor_pos] == self._separator:
                                return True

                    # Verify only on user key input, the rest of events are checked
                    # by TextInput on super call
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

                            # Check the number between the current separators,
                            # this number must be between 0-255
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
                                # User adds 0 at left, example: 12 -> 012
                                if num != str(int(num)) and key == '0':
                                    return False
                                if len(num) > 3:  # Number like 0XXX
                                    return False

        elif self._color_type == COLORINPUT_TYPE_HEX:
            self._format_hex()

            for event in events:

                # User writes
                if event.type == pygame.KEYDOWN and self._keyboard_enabled:
                    # Check if any key is pressed
                    if self._ignores_keyboard_nonphysical() and not check_key_pressed_valid(event):
                        continue

                    # Backspace button, delete text from right
                    if event.key == pygame.K_BACKSPACE:
                        if cursor_pos == 1:
                            return True

                    # Delete button, delete text from left
                    elif event.key == pygame.K_DELETE:
                        if cursor_pos == 0:
                            return True

                    # Verify only on user key input, the rest of events are checked
                    # by TextInput on super call
                    key = str(event.unicode)
                    if key in self._valid_chars:
                        if key == '#':
                            return True
                        if cursor_pos == 0:
                            return True

        # Update
        updated = super(ColorInput, self).update(events)

        # After
        if self._color_type == COLORINPUT_TYPE_RGB:
            total_separator = 0
            for ch in input_str:
                if ch == self._separator:
                    total_separator += 1

            # Adds auto separator
            if key == '0' and len(self._input_string) == self._cursor_position and \
                    total_separator < 2 and \
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
                auto_pos = len(colors) - 1
                last_num = colors[auto_pos]
                if (len(last_num) == 2 and int(last_num) > 25 or len(last_num) == 3 and
                    int(last_num) <= 255) and \
                        auto_pos not in self._auto_separator_pos:
                    self._push_key_input(self._separator, sounds=False)  # This calls .onchange()
                    self._auto_separator_pos.append(auto_pos)

            # If the user cleared all the string, reset auto separator
            if total_separator == 0 and \
                    (len(self._input_string) < 2 or len(self._input_string) == 2 and
                     int(colors[0]) <= 25):
                self._auto_separator_pos = []

        return updated


class ColorInputManager(AbstractWidgetManager, ABC):
    """
    ColorInput manager.
    """

    def color_input(
            self,
            title: Union[str, Any],
            color_type: ColorInputColorType,
            color_id: str = '',
            default: Union[str, Tuple3IntType] = '',
            hex_format: ColorInputHexFormatType = COLORINPUT_HEX_FORMAT_NONE,
            input_separator: str = ',',
            input_underline: str = '_',
            onchange: CallbackType = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            **kwargs
    ) -> 'pygame_menu.widgets.ColorInput':
        """
        Add a color widget with RGB or HEX format to the Menu.
        Includes a preview box that renders the given color.

        The callbacks (if defined) receive the current value and all unknown
        keyword arguments, where ``current_color=widget.get_value()``:

        .. code-block:: python

            onchange(current_color, **kwargs)
            onreturn(current_color, **kwargs)

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
            - ``dynamic_width``                 (bool) – If ``True`` the widget width changes if the pre-visualization color box is active or not
            - ``float``                         (bool) - If ``True`` the widget don't contributes width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``input_underline_vmargin``       (int) – Vertical margin of underline in px
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``maxwidth_dynamically_update``   (bool) - Dynamically update maxwidth depending on char size. ``True`` by default
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``previsualization_margin``       (int) – Pre-visualization left margin from text input in px. Default is ``0``
            - ``previsualization_width``        (int, float) – Pre-visualization width as a factor of the height. Default is ``3``
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``repeat_keys_initial_ms``        (int, float) - Time in ms before keys are repeated when held in ms. ``400`` by default
            - ``repeat_keys_interval_ms``       (int, float) - Interval between key press repetition when held in ms. ``50`` by default
            - ``repeat_mouse_interval_ms``      (int, float) - Interval between mouse events when held in ms. ``400`` by default
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``tab_size``                      (int) – Width of a tab character

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

        :param title: Title of the color input
        :param color_type: Type of the color input
        :param color_id: ID of the color input
        :param default: Default value to display, if RGB type it must be a tuple ``(r, g, b)``, if HEX must be a string ``"#XXXXXX"``
        :param hex_format: Hex format string mode
        :param input_separator: Divisor between RGB channels, not valid in HEX format
        :param input_underline: Underline character
        :param onchange: Callback executed when changing the values of the color text
        :param onreturn: Callback executed when pressing return on the color input
        :param onselect: Callback executed when selecting the widget
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.ColorInput`
        """
        assert isinstance(default, (str, tuple))

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        dynamic_width = kwargs.pop('dynamic_width', True)
        input_underline_vmargin = kwargs.pop('input_underline_vmargin', 0)
        prev_margin = kwargs.pop('previsualization_margin', 10)
        prev_width = kwargs.pop('previsualization_width', 3)

        widget = ColorInput(
            color_type=color_type,
            colorinput_id=color_id,
            cursor_color=self._theme.cursor_color,
            cursor_switch_ms=self._theme.cursor_switch_ms,
            dynamic_width=dynamic_width,
            hex_format=hex_format,
            input_separator=input_separator,
            input_underline=input_underline,
            input_underline_vmargin=input_underline_vmargin,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            prev_margin=prev_margin,
            prev_width_factor=prev_width,
            title=title,
            **kwargs
        )

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)
        widget.set_default_value(default)

        return widget
