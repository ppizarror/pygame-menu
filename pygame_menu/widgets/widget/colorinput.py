"""
pygame-menu
https://github.com/ppizarror/pygame-menu

COLOR INPUT
Color input class, Widget created in top of TextInput that provides a textbox
for entering and previewing colors in RGB and HEX format.
"""

from __future__ import annotations

__all__ = [
    # Main class
    "ColorInput",
    # Constants
    "COLORINPUT_TYPE_HEX",
    "COLORINPUT_TYPE_RGB",
    "COLORINPUT_HEX_FORMAT_LOWER",
    "COLORINPUT_HEX_FORMAT_NONE",
    "COLORINPUT_HEX_FORMAT_UPPER",
    # Type
    "ColorInputColorType",
    "ColorInputHexFormatType",
]

import math
from typing import Any

import pygame

from pygame_menu._types import (
    CallbackType,
    EventVectorType,
    NumberInstance,
    NumberType,
    Tuple3IntType,
)
from pygame_menu.locals import INPUT_TEXT
from pygame_menu.utils import check_key_pressed_valid, make_surface
from pygame_menu.widgets.widget.textinput import TextInput

# Input modes
COLORINPUT_TYPE_HEX = "hex"
COLORINPUT_TYPE_RGB = "rgb"

# Apply format to hex color string
COLORINPUT_HEX_FORMAT_LOWER = "lower"
COLORINPUT_HEX_FORMAT_NONE = "none"
COLORINPUT_HEX_FORMAT_UPPER = "upper"

# Custom typing
ColorInputColorType = str
ColorInputHexFormatType = str


class ColorInput(TextInput):
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
    :param onreturn: Function when pressing return (apply) on the color text input
    :param onselect: Function when selecting the widget
    :param prev_margin: Horizontal margin between the previsualization and the input text in px
    :param prev_width_factor: Width of the previsualization box in terms of the height of the widget
    :param repeat_keys_initial_ms: Time in milliseconds before keys are repeated when held
    :param repeat_keys_interval_ms: Interval between key press repetition when held
    :param repeat_mouse_interval_ms: Interval between mouse events when held
    :param kwargs: Optional keyword arguments
    """

    _auto_separator_pos: list[int]
    _color_type: str
    _dynamic_width: bool
    _hex_format: str
    _last_color: tuple[int, int, int] | None
    _prev_margin: int
    _previsualization_surface: pygame.Surface | None
    _separator: str

    def __init__(
        self,
        title: Any,
        colorinput_id: str = "",
        color_type: ColorInputColorType = COLORINPUT_TYPE_RGB,
        cursor_color: Tuple3IntType = (0, 0, 0),
        cursor_switch_ms: NumberType = 500,
        dynamic_width: bool = True,
        hex_format: ColorInputHexFormatType = COLORINPUT_HEX_FORMAT_NONE,
        input_separator: str = ",",
        input_underline: str = "_",
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
        **kwargs,
    ) -> None:
        assert isinstance(color_type, str)
        assert isinstance(colorinput_id, str)
        assert isinstance(dynamic_width, bool)
        assert isinstance(hex_format, str)
        assert isinstance(input_separator, str)
        assert isinstance(input_underline, str)
        assert isinstance(prev_margin, int)
        assert isinstance(prev_width_factor, NumberInstance)

        assert len(input_separator) == 1, "input_separator must be a single char"
        assert len(input_separator) != 0, "input_separator cannot be empty"
        assert prev_width_factor > 0, (
            "previsualization width factor must be greater than zero"
        )
        assert input_separator not in (
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        ), "input_separator cannot be a number"
        assert color_type in (COLORINPUT_TYPE_HEX, COLORINPUT_TYPE_RGB), (
            f'color type must be "{COLORINPUT_TYPE_HEX}" or "{COLORINPUT_TYPE_RGB}"'
        )
        assert hex_format in (
            COLORINPUT_HEX_FORMAT_NONE,
            COLORINPUT_HEX_FORMAT_LOWER,
            COLORINPUT_HEX_FORMAT_UPPER,
        ), 'invalid hex format mode, it must be "none", "lower" or "upper"'

        maxchar: int = 0
        valid_chars: list[str] | None = None
        self._color_type = color_type.lower()
        if self._color_type == COLORINPUT_TYPE_RGB:
            maxchar = 11  # RRR,GGG,BBB
            valid_chars = [
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                input_separator,
            ]
        elif self._color_type == COLORINPUT_TYPE_HEX:
            maxchar = 7  # #XXYYZZ
            valid_chars = [
                "a",
                "A",
                "b",
                "B",
                "c",
                "C",
                "d",
                "D",
                "e",
                "E",
                "f",
                "F",
                "#",
                "0",
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
            ]

        # noinspection PyArgumentEqualDefault
        super().__init__(
            alt_x_enabled=False,
            apply_widget_update_callback=False,
            copy_paste_enable=False,
            cursor_color=cursor_color,
            cursor_switch_ms=cursor_switch_ms,
            cursor_selection_enable=False,
            history=0,
            input_type=INPUT_TEXT,
            input_underline=input_underline,
            input_underline_vmargin=input_underline_vmargin,
            maxchar=maxchar,
            maxwidth=0,
            onchange=onchange,
            onreturn=onreturn,
            onselect=onselect,
            password=False,
            repeat_keys_initial_ms=repeat_keys_initial_ms,
            repeat_keys_interval_ms=repeat_keys_interval_ms,
            repeat_mouse_interval_ms=repeat_mouse_interval_ms,
            text_ellipsis="",
            textinput_id=colorinput_id,
            title=title,
            valid_chars=valid_chars,
            *args,
            **kwargs,
        )

        # Store inner variables
        self._auto_separator_pos = []  # This stores indexes of auto separator added
        self._dynamic_width = dynamic_width
        self._hex_format = hex_format
        self._separator = input_separator

        # Previsualization surface and cache
        self._last_color = None
        self._prev_margin = prev_margin
        self._prev_width_factor = prev_width_factor
        self._previsualization_surface = None

    def _apply_font(self) -> None:
        super()._apply_font()

        # Compute the size of the underline
        if self._input_underline != "":
            max_width: int = 0  # Max expected width
            if self._color_type == COLORINPUT_TYPE_RGB:
                max_width = self._font_render_string(
                    f"255{self._separator}255{self._separator}255"
                ).get_width()
            else:
                for i in ("a", "b", "c", "d", "e", "f"):
                    max_width = max(
                        max_width, self._font_render_string(f"#{i * 6}").get_width()
                    )

            char = math.ceil(max_width / self._input_underline_size)
            for i in range(10):  # Find the best guess for
                fw = self._font_render_string(
                    self._input_underline * int(char)
                ).get_width()
                char += 1
                if fw >= max_width:
                    break

            self._input_underline_len = char

    def clear(self) -> None:
        super().clear()
        self._invalidate_preview()
        self._auto_separator_pos.clear()
        if self._color_type == COLORINPUT_TYPE_HEX:
            super().set_value("#")
        self.change()

    def set_value(self, color: str | Tuple3IntType | None) -> None:
        """
        Set the color value.

        :param color: A string if the type is HEX, or a (r, g, b) tuple if RGB
        """
        if self._color_type == COLORINPUT_TYPE_RGB:
            self._set_rgb_value(color)
        else:
            self._set_hex_value(color)
        self._format_hex()

    def _set_rgb_value(self, color: str | Tuple3IntType | None) -> None:
        if color is None or color == "":
            super().set_value("")
            return

        assert isinstance(color, tuple), (
            "color in rgb format must be a tuple in (r,g,b) format"
        )
        assert len(color) == 3, "tuple must contain only 3 colors, R,G,B"
        r, g, b = color
        assert isinstance(r, int) and isinstance(g, int) and isinstance(b, int), (
            "color channels must be integers"
        )
        assert 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255, (
            "color channels must be between 0 and 255"
        )

        format_color = self._format_rgb((r, g, b))
        self._auto_separator_pos = [0, 1]
        super().set_value(format_color)

    def _set_hex_value(self, color: str | Tuple3IntType | None) -> None:
        if color is None:
            super().set_value("#")
            return

        text = str(color).strip()

        if text == "" or text == "#":
            super().set_value("#")
            return

        valid_text = "".join(ch for ch in text if ch in self._valid_chars)

        count_hash = valid_text.count("#")

        if count_hash == 1:
            assert valid_text[0] == "#", 'color format must be "#RRGGBB"'
        elif count_hash == 0:
            valid_text = "#" + valid_text
        else:
            raise AssertionError('color format must be "#RRGGBB"')

        assert len(valid_text) == 7, 'color format must be "#RRGGBB"'

        super().set_value(valid_text)

    def value_changed(self) -> bool:
        default = self._default_value
        if self._color_type == COLORINPUT_TYPE_HEX and "#" not in default:
            default = "#" + default
        return self.get_value(as_string=True) != default

    def get_value(self, as_string: bool = False) -> str | Tuple3IntType:
        """
        Return the color value as a tuple or red blue and green channels.

        .. note::

            If the data is invalid the widget returns ``(-1, -1, -1)``.

        :param as_string: If ``True`` returns the widget value as plain text
        :return: Color tuple as (R, G, B) or color string
        """
        if as_string:
            return self._input_string
        color = self._parse_current_color()
        if color is None:
            return -1, -1, -1
        return color

    def is_valid(self) -> bool:
        """
        Return ``True`` if the current value of the input is a valid color or not.

        :return: ``True`` if valid
        """
        return self._parse_current_color() is not None

    def _parse_rgb(self, text: str) -> Tuple3IntType | None:
        parts = text.split(self._separator)
        if len(parts) != 3:
            return None
        try:
            r, g, b = map(int, parts)
        except ValueError:
            return None
        if not all(0 <= c <= 255 for c in (r, g, b)):
            return None
        return (r, g, b)

    def _parse_hex(self, text: str) -> Tuple3IntType | None:
        if len(text) != 7 or not text.startswith("#"):
            return None
        try:
            return (
                int(text[1:3], 16),
                int(text[3:5], 16),
                int(text[5:7], 16),
            )
        except ValueError:
            return None

    def _parse_current_color(self) -> Tuple3IntType | None:
        if self._color_type == COLORINPUT_TYPE_RGB:
            return self._parse_rgb(self._input_string)
        return self._parse_hex(self._input_string)

    def _format_rgb(self, color: tuple[int, int, int]) -> str:
        r, g, b = color
        return f"{r}{self._separator}{g}{self._separator}{b}"

    def _preview_extra_width(self) -> int:
        return int(self._prev_width_factor * self._rect.height + self._prev_margin)

    def _invalidate_preview(self) -> None:
        self._previsualization_surface = None
        self._last_color = None

    def _create_preview_surface(self, color: tuple[int, int, int]) -> None:
        width = int(self._prev_width_factor * self._rect.height)
        if width <= 0:
            self._previsualization_surface = None
            return
        surface = make_surface(width, self._rect.height)
        surface.fill(color)
        self._previsualization_surface = surface
        self._last_color = color

    def _update_preview_surface(self) -> None:
        color = self._parse_current_color()
        if color is None:
            self._invalidate_preview()
            return
        if self._previsualization_surface is not None and color == self._last_color:
            return
        self._create_preview_surface(color)

    def _draw(self, surface: pygame.Surface) -> None:
        super()._draw(surface)  # This calls _render()

        # Draw previsualization box
        if self._previsualization_surface is not None:
            posx: float = (
                self._rect.x
                + self._rect.width
                - self._prev_width_factor * self._rect.height
                + self._rect.height / 10
            )
            posy: int = self._rect.y
            surface.blit(self._previsualization_surface, (int(posx), int(posy)))

    def _render(self) -> bool | None:
        render_text = super()._render()

        # Maybe TextInput did not render, so this has to be changed
        self._rect.width, self._rect.height = self._surface.get_size()
        self._update_preview_surface()
        if not self._dynamic_width or self._previsualization_surface is not None:
            self._rect.width += self._preview_extra_width()

        return render_text

    def _format_hex(self) -> None:
        """
        Apply hex format.
        """
        if (
            self._color_type != COLORINPUT_TYPE_HEX
            or self._hex_format == COLORINPUT_HEX_FORMAT_NONE
        ):
            return

        if self._hex_format == COLORINPUT_HEX_FORMAT_LOWER:
            self._input_string = self._input_string.lower()
        elif self._hex_format == COLORINPUT_HEX_FORMAT_UPPER:
            self._input_string = self._input_string.upper()

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)

        if self.readonly or not self.is_visible():
            self._readonly_check_mouseover(events)
            return False

        if self._color_type == COLORINPUT_TYPE_RGB:
            return self._update_rgb(events)
        return self._update_hex(events)

    def _update_rgb(self, events: EventVectorType) -> bool:
        original_text = self._input_string
        original_cursor = self._cursor_position
        typed_key = ""

        for event in events:
            if event.type != pygame.KEYDOWN or not self._keyboard_enabled:
                continue
            if self._ignores_keyboard_nonphysical() and not check_key_pressed_valid(
                event
            ):
                continue

            if self._handle_rgb_backspace_delete(event, original_text, original_cursor):
                return True

            key = str(event.unicode)
            if not original_text and key == self._separator:
                return False

            if key in self._valid_chars and not self._is_rgb_key_valid(
                key, original_cursor, original_text
            ):
                return False
            typed_key = key

        updated = super().update(events)
        self._post_process_rgb(original_text, original_cursor, typed_key)
        return updated

    def _update_hex(self, events: EventVectorType) -> bool:
        self._format_hex()

        for event in events:
            # User writes
            if event.type == pygame.KEYDOWN and self._keyboard_enabled:
                # Check if any key is pressed
                if self._ignores_keyboard_nonphysical() and not check_key_pressed_valid(
                    event
                ):
                    continue

                # Backspace button, delete text from right
                elif self._ctrl.back(event, self) and self._cursor_position == 1:
                    return True

                # Delete button, delete text from left
                elif self._ctrl.delete(event, self) and self._cursor_position == 0:
                    return True

                # Verify only on user key input, the rest of events are checked
                # by TextInput on super call
                key = str(event.unicode)
                if key in self._valid_chars:
                    if key == "#":
                        return True
                    elif self._cursor_position == 0:
                        return True

        return super().update(events)

    def _handle_rgb_backspace_delete(
        self, event: pygame.Event, input_str: str, cursor_pos: int
    ) -> bool:
        if (
            len(input_str) > 0
            and len(input_str) > cursor_pos
            and (
                f"{self._separator}{self._separator}" not in input_str
                or input_str[cursor_pos] == self._separator
                and len(input_str) == cursor_pos + 1
            )
        ):
            # Backspace button, delete text from right
            if self._ctrl.back(event, self):
                if cursor_pos > 0 and input_str[cursor_pos - 1] == self._separator:
                    return True

            # Delete button, delete text from left
            elif self._ctrl.delete(event, self):
                if input_str[cursor_pos] == self._separator:
                    return True
        return False

    def _separator_count(self, text: str) -> int:
        return text.count(self._separator)

    def _channel_valid(self, value: str) -> bool:
        if value == "":
            return True

        if len(value) > 3:
            return False

        number = int(value)

        if number > 255:
            return False

        if value != str(number):
            return False

        return True

    def _channel_after_insert(self, key: str, text: str, cursor: int) -> str:
        new_text = text[:cursor] + key + text[cursor:]
        left = new_text.rfind(self._separator, 0, cursor + 1)
        right = new_text.find(self._separator, cursor)
        if left == -1:
            left = 0
        else:
            left += 1
        if right == -1:
            right = len(new_text)
        return new_text[left:right]

    def _is_rgb_key_valid(self, key: str, cursor: int, text: str) -> bool:
        if key == self._separator:
            return self._separator_count(text) < 2
        channel = self._channel_after_insert(key, text, cursor)
        return self._channel_valid(channel.replace(self._separator, ""))

    def _validate_rgb_channels(self, original_input: str, original_cursor: int) -> bool:
        colors = self._input_string.split(self._separator)
        for c in colors:
            if len(c) > 0 and (int(c) > 255 or int(c) < 0):
                self._input_string = original_input
                self._cursor_position = original_cursor
                return False
        return True

    def _auto_insert_zero_separator(self, key: str, total_separator: int) -> None:
        if (
            key == "0"
            and len(self._input_string) == self._cursor_position
            and total_separator < 2
            and (
                len(self._input_string) == 1
                or len(self._input_string) > 2
                and self._input_string[self._cursor_position - 2] == self._separator
            )
        ):
            self._push_key_input(
                self._separator, sounds=False
            )  # This calls .onchange()

    def _auto_insert_separator(self, colors: list[str], total_separator: int) -> None:
        if total_separator < 2 and len(self._input_string) == self._cursor_position:
            auto_pos = len(colors) - 1
            last_num = colors[auto_pos]
            if (
                (len(last_num) == 2 and int(last_num) > 25)
                or (len(last_num) == 3 and int(last_num) <= 255)
            ) and auto_pos not in self._auto_separator_pos:
                self._push_key_input(
                    self._separator, sounds=False
                )  # This calls .onchange()
                self._auto_separator_pos.append(auto_pos)

    def _reset_auto_separator_state(
        self, colors: list[str], total_separator: int
    ) -> None:
        if total_separator == 0 and (
            len(self._input_string) < 2
            or len(self._input_string) == 2
            and int(colors[0]) <= 25
        ):
            self._auto_separator_pos.clear()

    def _post_process_rgb(
        self, original_input: str, original_cursor: int, key: str
    ) -> None:
        total_separator = self._separator_count(self._input_string)

        self._auto_insert_zero_separator(key, total_separator)

        if not self._validate_rgb_channels(original_input, original_cursor):
            return

        colors = self._input_string.split(self._separator)
        if len(colors) == 3:
            self._auto_separator_pos = [0, 1]

        self._auto_insert_separator(colors, total_separator)
        self._reset_auto_separator_state(colors, total_separator)
