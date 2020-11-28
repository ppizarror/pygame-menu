# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEXT INPUT
Text input class, this widget lets user to write text.

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

import math

import pygame
import pygame_menu.controls as _controls
import pygame_menu.locals as _locals
from pygame_menu.utils import check_key_pressed_valid, make_surface, assert_color, to_string
from pygame_menu.widgets.core import Widget

try:
    # noinspection PyProtectedMember
    from pyperclip import copy, paste, PyperclipException
except ImportError:

    # noinspection PyUnusedLocal
    def copy(text):
        """
        Copy method.

        :return: None
        """
        pass


    def paste():
        """
        Paste method.

        :return: Empty string
        :rtype: str
        """
        return ''


    class PyperclipException(RuntimeError):
        """
        Pyperclip exception thrown by pyperclip.
        """
        pass


class TextInput(Widget):
    """
    Text input widget.

    :param title: Text input title
    :type title: str
    :param textinput_id: ID of the text input
    :type textinput_id: str
    :param input_type: Type of data
    :type input_type: str
    :param input_underline: Character drawn under the input
    :type input_underline: str
    :param cursor_color: Color of cursor
    :type cursor_color: tuple
    :param cursor_selection_color: Selection box color
    :type cursor_selection_color: tuple
    :param cursor_selection_enable: Enables selection of text
    :type cursor_selection_enable: bool
    :param copy_paste_enable: Enables copy, paste and cut
    :type copy_paste_enable: bool
    :param history: Maximum number of editions stored
    :type history: int
    :param maxchar: Maximum length of input
    :type maxchar: int
    :param maxwidth: Maximum size of the text to be displayed (overflow), if 0 this feature is disabled
    :type maxwidth: int
    :param maxwidth_dynamically_update: Dynamically update maxwidth depending on char size
    :type maxwidth_dynamically_update: bool
    :param onchange: Callback when changing the selector
    :type onchange: callable, None
    :param onreturn: Callback when pressing return button
    :type onreturn: callable, None
    :param password: Input string is displayed as a password
    :type password: bool
    :param password_char: Character used by password type
    :type password_char: str
    :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
    :type repeat_keys_initial_ms: int, float
    :param repeat_keys_interval_ms: Interval between key press repetition when held
    :type repeat_keys_interval_ms: int, float
    :param repeat_mouse_interval_ms: Interval between mouse events when held
    :type repeat_mouse_interval_ms: int, float
    :param repeat_touch_interval_ms: Interval between mouse events when held
    :type repeat_touch_interval_ms: int, float
    :param tab_size: Tab whitespace characters
    :type tab_size: int
    :param text_ellipsis: Ellipsis text when overflow occurs (input length exceeds maxwidth)
    :type text_ellipsis: str
    :param valid_chars: List of chars that are valid, None if all chars are valid
    :type valid_chars: list
    :param kwargs: Optional keyword arguments
    :type kwargs: dict
    """

    def __init__(self,
                 title='',
                 textinput_id='',
                 input_type=_locals.INPUT_TEXT,
                 input_underline='',
                 copy_paste_enable=True,
                 cursor_color=(0, 0, 0),
                 cursor_selection_color=(30, 30, 30, 100),
                 cursor_selection_enable=True,
                 history=50,
                 maxchar=0,
                 maxwidth=0,
                 maxwidth_dynamically_update=True,
                 onchange=None,
                 onreturn=None,
                 password=False,
                 password_char='*',
                 repeat_keys_initial_ms=450,
                 repeat_keys_interval_ms=80,
                 repeat_mouse_interval_ms=100,
                 repeat_touch_interval_ms=100,
                 tab_size=4,
                 text_ellipsis='...',
                 valid_chars=None,
                 *args,
                 **kwargs):
        assert isinstance(textinput_id, str)
        assert isinstance(input_type, str)
        assert isinstance(input_underline, str)
        assert isinstance(cursor_color, tuple)
        assert isinstance(copy_paste_enable, bool)
        assert isinstance(cursor_selection_enable, bool)
        assert isinstance(history, int)
        assert isinstance(valid_chars, (type(None), list))
        assert isinstance(maxchar, int)
        assert isinstance(maxwidth, int)
        assert isinstance(password, bool)
        assert isinstance(password_char, str)
        assert isinstance(repeat_keys_initial_ms, (int, float))
        assert isinstance(repeat_keys_interval_ms, (int, float))
        assert isinstance(repeat_mouse_interval_ms, (int, float))
        assert isinstance(repeat_touch_interval_ms, (int, float))
        assert isinstance(tab_size, int)
        assert isinstance(text_ellipsis, str)

        assert history >= 0, 'history must be equal or greater than zero'
        assert maxchar >= 0, 'maxchar must be equal or greater than zero'
        assert maxwidth >= 0, 'maxwidth must be equal or greater than zero'
        assert tab_size >= 0, 'tab size must be equal or greater than zero'
        assert len(password_char) == 1, 'password char must be a character'

        assert_color(cursor_color)
        assert_color(cursor_selection_color)
        if pygame.vernum.major == 2:
            assert len(cursor_selection_color) == 4, 'cursor selection color alpha must be defined'
            assert cursor_selection_color[3] != 255, 'cursor selection color alpha cannot be opaque'

        super(TextInput, self).__init__(
            title=title,
            widget_id=textinput_id,
            onchange=onchange,
            onreturn=onreturn,
            args=args,
            kwargs=kwargs
        )

        self._input_string = ''  # Inputted text
        self._ignore_keys = (  # Ignore keys on keyrepeat event
            _controls.KEY_MOVE_DOWN,
            _controls.KEY_MOVE_UP,
            pygame.K_CAPSLOCK,
            pygame.K_END,
            pygame.K_ESCAPE,
            pygame.K_HOME,
            pygame.K_LCTRL,
            pygame.K_LSHIFT,
            pygame.K_NUMLOCK,
            pygame.K_RCTRL,
            pygame.K_RETURN,
            pygame.K_RSHIFT,
            pygame.K_TAB,
        )

        # Vars to make keydowns repeat after user pressed a key for some time:
        self._absolute_origin = (0, 0)  # To calculate mouse collide point
        self._block_copy_paste = False  # Blocks event
        self._key_is_pressed = False
        self._keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self._keyrepeat_initial_interval_ms = repeat_keys_initial_ms
        self._keyrepeat_interval_ms = repeat_keys_interval_ms
        self._last_key = 0  # type: int

        # Mouse handling
        self._keyrepeat_mouse_ms = 0.0  # type: float
        self._keyrepeat_mouse_interval_ms = repeat_mouse_interval_ms
        self._mouse_is_pressed = False  # type: bool

        # Touchscreen handling
        self._keyrepeat_touch_interval_ms = repeat_touch_interval_ms

        # Render box (overflow)
        self._ellipsis = text_ellipsis
        self._ellipsis_size = 0.0  # type: float
        self._renderbox = [0, 0, 0]  # Left/Right/Inner, int

        # Things cursor:
        self._clock = pygame.time.Clock()  # type: pygame.time.Clock
        self._cursor_color = cursor_color
        self._cursor_ms_counter = 0.0  # type: float
        self._cursor_offset = -1.0  # type: float
        self._cursor_position = 0  # Inside text
        self._cursor_render = True  # If true cursor must be rendered
        self._cursor_surface = None  # type: (pygame.Surface,None)
        self._cursor_surface_pos = [0.0, 0.0]  # Position (x,y) of surface
        self._cursor_switch_ms = 500.0  # type: float
        self._cursor_visible = False  # Switches every self._cursor_switch_ms ms

        # History of editions
        self._history = []  # type: list
        self._history_cursor = []  # type: list
        self._history_renderbox = []  # type: list
        self._history_index = 0  # Index at which the new editions are added
        self._max_history = history

        # Text selection
        self._last_selection_render = [0, 0]  # Position (int)
        self._selection_active = False
        self._selection_box = [0, 0]  # [from, to], (int)
        self._selection_color = cursor_selection_color
        self._selection_enabled = cursor_selection_enable
        self._selection_mouse_first_position = -1  # type: int
        self._selection_position = [0.0, 0.0]  # x,y (float)
        self._selection_render = False
        self._selection_surface = None  # type: (pygame.Surface,None)
        self._selection_touch_first_position = -1  # type: int

        # List of valid chars
        if valid_chars is not None:
            for ch in range(len(valid_chars)):
                _char = to_string(valid_chars[ch])
                valid_chars[ch] = _char
                assert isinstance(_char, str), 'element "{0}" of valid_chars must be a string'.format(_char)
                assert len(_char) == 1, 'element "{0}" of valid_chars must be character'.format(_char)
            assert len(valid_chars) > 0, 'valid_chars list must contain at least 1 element'
        self._valid_chars = valid_chars

        # Other
        self._copy_paste_enabled = copy_paste_enable
        self._input_type = input_type
        self._input_underline = input_underline
        self._input_underline_size = 0.0  # type: float
        self._keychar_size = {'': 0}  # type: dict
        self._last_char = ''  # type: str
        self._last_rendered_string = '__pygame_menu__last_render_string__'  # type: str
        self._last_rendered_surface = None  # type: (pygame.Surface,None)
        self._last_rendered_surface_underline_width = 0  # type: int
        self._maxchar = maxchar
        self._maxwidth = maxwidth  # This value will be changed depending on how many chars are printed
        self._maxwidth_base = maxwidth
        self._maxwidth_update = maxwidth_dynamically_update
        self._maxwidthsize = 0.0  # Updated in _apply_font()
        self._password = password
        self._password_char = password_char
        self._tab_size = tab_size
        self._title_size = 0.0  # type: float

    def _apply_font(self):
        self._ellipsis_size = self._font.size(self._ellipsis)[0]
        self._title_size = self._font.size(self._title)[0]

        # Generate the underline surface
        self._input_underline_size = self._font.size(self._input_underline)[0]

        # Size of maxwidth if not zero
        max_char = 'O'
        if self._password:
            max_char = self._password_char
        self._maxwidthsize = self._font_render_string(max_char * self._maxwidth_base).get_size()[0]

        # Update password char size
        if self._password:
            password_size = self._font_render_string(self._password_char).get_size()[0]
            if password_size == 0:
                raise ValueError(
                    'password character is not valid, the size of the font is zero, '
                    'use another character or change the font')
            self._keychar_size[self._password_char] = password_size

    def clear(self):
        """
        Clear the current text.

        :return: None
        """
        self._input_string = ''
        self._cursor_position = 0
        self._renderbox = [0, 0, 0]
        self._delete()
        self.change()

    def get_value(self):
        """
        Return the value of the text.

        :return: Text inside the widget
        :rtype: str
        """
        value = ''
        if self._input_type == _locals.INPUT_TEXT:
            value = self._input_string  # Without filters
        elif self._input_type == _locals.INPUT_FLOAT:
            try:
                value = float(self._input_string)
            except ValueError:
                value = 0
        elif self._input_type == _locals.INPUT_INT:
            try:
                value = int(float(self._input_string))
            except ValueError:
                value = 0
        return value

    # noinspection PyMissingOrEmptyDocstring
    def draw(self, surface):
        self._render()
        self._clock.tick()

        # Draw background color
        self._fill_background_color(surface)

        if pygame.vernum.major == 2:
            surface.blit(self._surface, (self._rect.x, self._rect.y))  # Draw string
            if self._selection_surface is not None:  # Draw selection
                surface.blit(self._selection_surface, (self._selection_position[0], self._selection_position[1]))
        else:
            if self._selection_surface is not None:  # Draw selection
                surface.blit(self._selection_surface, (self._selection_position[0], self._selection_position[1]))
            surface.blit(self._surface, (self._rect.x, self._rect.y))  # Draw string

        # Draw cursor
        if self.selected and self._cursor_surface and \
                (self._cursor_visible or (self._mouse_is_pressed or self._key_is_pressed)):
            surface.blit(self._cursor_surface, (self._rect.x + self._cursor_surface_pos[0],
                                                self._rect.y + self._cursor_surface_pos[1]))

    def _render(self):
        string = self._title + self._get_input_string()  # Render string

        if not self._render_hash_changed(self._menu.get_id(), string, self.selected, self._cursor_render,
                                         self._selection_enabled, self.active):
            return

        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        updated_surface = self._render_string_surface(string, color)

        # Apply underline if exists
        self._surface = self._render_underline(string, color, updated_surface)

        # Render the cursor
        self._render_cursor()

        # Render the selection box if text is selected
        self._render_selection_box()

        # Update last rendered
        self._last_rendered_string = string

        # Update the size of the render
        self._rect.width, self._rect.height = self._surface.get_size()

        # Check if the size changed
        self._check_render_size_changed()

    def _render_selection_box(self, force=False):
        """
        Render selected text.

        :param force: Force update
        :type force: bool
        :return: None
        """
        if not self._selection_enabled:
            return

        if self._selection_active and \
                (self._last_selection_render[0] != self._selection_box[0] or self._last_selection_render[1] !=
                 self._selection_box[1]) or force:

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

            # Create surface and fill
            self._selection_surface = make_surface(x, y, fill_color=self._selection_color)
            self._selection_position[0] = x1 + self._rect.x
            self._selection_position[1] = self._rect.y

            # Fill cursor
            if self._cursor_surface:
                self._cursor_surface.fill(self._cursor_color)

    def _render_string_surface(self, string, color):
        """
        Renders string surface.

        :param string: String to render
        :type string: str
        :param color: Color of the string to render
        :type color: tuple
        :return: True if surface is updated
        :rtype: bool
        """
        new_surface = self._render_string(string, color)
        updated_surface = self._last_rendered_surface != new_surface
        if updated_surface:
            self._surface = new_surface
            self._last_rendered_surface = self._surface
        return updated_surface

    def _render_underline(self, string, color, updated):
        """
        Render underline surface.

        :param string: String to render
        :type string: str
        :param color: Color of the string to render
        :type color: tuple
        :param updated: Render string has been updated or not
        :type updated: bool
        :return: New rendered surface
        :rtype: :py:class:`pygame.Surface`
        """
        # If underline is not enabled
        if self._input_underline_size == 0:
            return self._surface

        # Render input underline
        if string != self._last_rendered_string or updated:
            menu = self.get_menu()

            # Calculate total available space
            current_rect = self._surface.get_rect()  # type: pygame.Rect
            menu_rect = menu.get_rect()
            posx2 = menu_rect.x + menu_rect.width
            space_between_title = posx2 - self._title_size - self._rect.x
            char = math.ceil(space_between_title * 1.0 / self._input_underline_size)  # floor does not work

            # If char limit
            max_width_current = 0
            if self._maxchar != 0 or self._maxwidth != 0:
                max_chars = max(self._maxchar, self._maxwidth_base)
                basechar = 'O'
                multif = 4  # Factor of ellipsis
                if self._password:
                    basechar = self._password_char
                    multif = 2
                max_size = self._font_render_string(basechar * max_chars)
                max_size = max_size.get_size()[0]
                maxchar_char = math.ceil((max_size + multif * self._ellipsis_size) / self._input_underline_size)
                char = min(char, maxchar_char)
                max_width_current = current_rect.width

            underline_string = self._input_underline * int(char)

            # Render char
            underline = self._font_render_string(underline_string, color, use_background_color=False)

            # Create a new surface
            new_width = max(self._title_size + underline.get_size()[0],
                            max_width_current,
                            self._last_rendered_surface_underline_width)
            new_surface = make_surface(new_width + 1, current_rect.height + 3, alpha=True)

            # Blit current surface
            new_surface.blit(self._surface, (0, 0))
            new_surface.blit(underline, (self._title_size - 1, 6))  # Position (x, y)
            self._last_rendered_surface_with_underline = new_surface
            self._last_rendered_surface_underline_width = new_width
        else:
            new_surface = self._last_rendered_surface_with_underline  # Reuse the rendered surface

        return new_surface

    def _render_cursor(self):
        """
        Cursor is rendered and stored.

        :return: None
        """
        # Cursor should not be rendered
        if not self._cursor_render:
            return

        # Cursor surface does not exist
        if self._cursor_surface is None:
            if self._rect.height == 0:  # If menu has not been initialized this error can occur
                return
            self._cursor_surface = make_surface(self._font_size / 20 + 1, self._rect.height - 2)
            self._cursor_surface.fill(self._cursor_color)

        # Get string
        string = self._get_input_string_filtered()

        # Calculate x position
        if self._maxwidth == 0:  # If no limit is provided
            cursor_x_pos = self._cursor_offset + \
                           self._font.size(self._title + string[:self._cursor_position])[0]
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
        cursor_x_pos += 3

        # Store position
        self._cursor_surface_pos[0] = cursor_x_pos
        self._cursor_surface_pos[1] = cursor_y_pos
        self._cursor_render = False

    def _ellipsis_left(self):
        """
        Return true if left ellipsis is active.

        :return: Boolean
        :rtype: bool
        """
        return self._renderbox[0] != 0 and self._maxwidth != 0

    def _ellipsis_right(self):
        """
        Return true if right ellipsis is active.

        :return: Boolean
        :rtype: bool
        """
        return self._renderbox[1] != len(self._input_string) and self._maxwidth != 0

    def _ellipsis_left_and_right(self):
        """
        Return true if left and right ellipsis are active.

        :return: Boolean
        :rtype: bool
        """
        return self._ellipsis_left() and self._ellipsis_right()

    def _get_input_string_filtered(self):
        """
        Return the input string where all filters have been applied.

        :return: Filtered string
        :rtype: str
        """
        string = self._input_string

        # Apply password
        if self._password:
            string = self._password_char * len(string)

        return string

    def _get_input_string(self, add_ellipsis=True):
        """
        Return the input string, apply overflow if enabled.

        :param add_ellipsis: Adds ellipsis text
        :type add_ellipsis: bool
        :return: String
        :rtype: str
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

    def _update_renderbox(self, left=0, right=0, addition=False, end=False, start=False, update_maxwidth=True):
        """
        Update renderbox position.

        :param left: Left update
        :type left: int
        :param right: Right update
        :type right: int
        :param addition: Update if text addition/deletion
        :type addition: bool
        :param end: Move cursor to end
        :type end: bool
        :param start: Move cursor to start
        :type start: bool
        :param update_maxwidth: Update maxwidth limit depending on the chars written
        :type update_maxwidth: bool
        :return: None
        """
        self._cursor_render = True
        if self._maxwidth == 0:
            return
        len_string = len(self._input_string)

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
            self._renderbox[2] += left
            self._renderbox[2] += right
        else:
            if addition:  # If text is added
                if right < 0 and self._renderbox[2] == self._maxwidth:  # If press del at the end of string
                    return
                if left < 0 and self._renderbox[2] == 0:  # If backspace at beginning of string
                    return

                # If user deletes something and it is in the end
                if right < 0:  # del
                    if self._ellipsis_left():
                        if (self._renderbox[1] - 1) == len_string:  # At the end
                            self._renderbox[2] -= right

                # If the user writes, move renderbox
                if right > 0:
                    if self._renderbox[2] == self._maxwidth:  # If cursor is at the end push box
                        self._renderbox[0] += right
                        self._renderbox[1] += right
                    self._renderbox[2] += right

                if left < 0:
                    if self._renderbox[0] == 0:  # If cursor is at the beginning
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

    def _update_maxlimit_renderbox(self):
        """
        Update renderbox based on how many characters have been written on input.

        :return: None
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
                    _char_size = self._get_char_size(char)
                    accum_size += _char_size
                    biggest = max(biggest, _char_size)

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

    def _update_cursor_mouse(self, mousex):
        """
        Updates cursor position after mouse click or touch action in text.

        :param mousex: Mouse distance relative to surface
        :type mousex: int
        :return: None
        """
        string = self._get_input_string()
        if string == '':  # If string is empty cursor is not updated
            return

        # Calculate size of each character
        string_size = []
        string_total_size = 0
        for i in range(len(string)):
            cs = self._font.size(string[i])[0]  # Char size
            string_size.append(cs)
            string_total_size += cs

        # Find the accumulated char size that gives the position of cursor
        size_sum = 0
        cursor_pos = len(string)
        for i in range(len(string)):
            size_sum += string_size[i] / 2
            if self._title_size + size_sum >= mousex:
                cursor_pos = i
                break
            size_sum += string_size[i] / 2

        # If text have ellipsis
        if self._maxwidth != 0 and len(self._input_string) > self._maxwidth:
            if self._ellipsis_left():
                cursor_pos -= 3

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

    def _check_mouse_collide_input(self, pos):
        """
        Check mouse collision, if true update cursor.

        :param pos: Position
        :type pos: tuple
        :return: None
        """
        if self._rect.collidepoint(*pos):
            # Check if mouse collides left or right as percentage, use only X coordinate
            mousex, _ = pos
            topleft, _ = self._rect.topleft
            self._update_cursor_mouse(mousex - topleft)
            return True  # Prevents double click

    def _check_touch_collide_input(self, pos):
        """
        Check touchscreen collision, if true update cursor.

        :param pos: Position
        :type pos: tuple
        :return: None
        """
        if self._rect.collidepoint(*pos):
            # Check if touchscreen collides left or right as percentage, use only X coordinate
            touchx, _ = pos
            topleft, _ = self._rect.topleft
            self._update_cursor_mouse(touchx - topleft)
            return True  # Prevents double click

    def set_value(self, text):
        """
        Set the value of the text.

        :param text: New text of the widget
        :type text: str, int, float
        :return: None
        """
        if self._password and text != '':
            raise ValueError('value cannot be set in password type')
        assert isinstance(text, (str, int, float))
        if self._check_input_type(text):
            _default = to_string(text)

            # Filter valid chars
            if self._valid_chars is not None:
                _default_valid = ''
                for ch in _default:
                    if ch in self._valid_chars:
                        _default_valid += ch
                _default = _default_valid

            # Apply maxchar
            _ls = len(_default)
            if 0 < self._maxchar < _ls:
                _default = _default[_ls - self._maxchar:_ls]

            self._input_string = _default
            for i in range(len(_default) + 1):
                self._move_cursor_right()
                self._update_renderbox(right=1, addition=True)
            self._update_input_string(_default)
        else:
            raise ValueError('value "{0}" type is not correct according to input_type'.format(text))
        self._update_renderbox()  # Updates cursor
        self._render()  # Renders the selection box

    def _check_input_size(self):
        """
        Check input size.

        :return: True if the input must be limited
        :rtype: bool
        """
        if self._maxchar == 0:
            return False
        return self._maxchar <= len(self._input_string)

    def _check_input_type(self, string):
        """
        Check if input type is valid.

        :param string: String to validate
        :type string: str
        :return: True if the input type is valid
        :rtype: bool
        """
        if string == '':  # Empty is valid
            return True

        if self._input_type == _locals.INPUT_TEXT:
            return True

        conv = None
        if self._input_type == _locals.INPUT_FLOAT:
            conv = float
        elif self._input_type == _locals.INPUT_INT:
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

    def _move_cursor_left(self):
        """
        Move cursor to left position.

        :return: None
        """
        # Subtract one from cursor_pos, but do not go below zero:
        self._cursor_position = max(self._cursor_position - 1, 0)
        self._update_renderbox(left=-1)

    def _move_cursor_right(self):
        """
        Move cursor to right position.

        :return: None
        """
        # Add one to cursor_pos, but do not exceed len(input_string)
        self._cursor_position = min(self._cursor_position + 1, len(self._input_string))
        self._update_renderbox(right=1)

    def _blur(self):
        # self._key_is_pressed = False
        self._mouse_is_pressed = False
        self._keyrepeat_mouse_ms = 0
        self._cursor_visible = False
        self._unselect_text()
        # self._history_index = len(self._history) - 1

    def _focus(self):
        self._cursor_ms_counter = 0
        self._cursor_visible = True
        self._cursor_render = True

    def _unselect_text(self):
        """
        Unselect text.

        :return: True if the selected text was removed in the method call
        :rtype: bool
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
        return removed

    def _get_selected_text(self):
        """
        Return the selected text.

        :return: Text
        :rtype: str
        """
        return self._input_string[self._selection_box[0]:self._selection_box[1]]

    def _update_input_string(self, new_string, update_history=True):
        """
        Update input string with a new string, store changes into history.

        :param new_string: New string of text input
        :type new_string: str
        :param update_history: Updates history
        :type update_history: bool
        :return: None
        """
        assert isinstance(new_string, str)
        assert isinstance(update_history, bool)

        l_history = len(self._history)

        # If last edition is different than the new one -> updates the history
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
            self._history_renderbox.insert(self._history_index,
                                           [self._renderbox[0], self._renderbox[1], self._renderbox[2]])

            if len(self._history) > self._max_history:
                self._history.pop(0)
                self._history_cursor.pop(0)
                self._history_renderbox.pop(0)
            self._history_index = len(self._history)  # This can be changed with undo/redo

        # Updates string
        self._input_string = new_string

    def _copy(self):
        """
        Copy text from clipboard.

        :return: None
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

    def _cut(self):
        """
        Cut operation.

        :return: None
        """
        self._copy()  # This is a safe operation, all checks have been passed

        # If text is selected
        if self._selection_surface:
            self._remove_selection()
        else:
            self._cursor_position = 0
            self._renderbox[0] = 0
            self._renderbox[1] = 0
            self._renderbox[2] = 0
            self._update_input_string('')
            self._cursor_render = True  # Due to manually updating renderbox

    def _get_char_size(self, char):
        """
        Return the widget char size in pixels.

        :param char: Char
        :type char: str
        :return: Char size in px
        :rtype: int
        """
        if char in self._keychar_size.keys():
            return self._keychar_size[char]
        self._keychar_size[char] = self._font_render_string(char).get_size()[0]
        return self._keychar_size[char]

    def _paste(self):
        """
        Paste text from clipboard.

        :return: None
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

        # Cut string (if limit does exists)
        text_end = len(text)
        if self._maxchar != 0:
            char_limit = self._maxchar - len(self._input_string)
            text_end = min(char_limit, text_end)
            if text_end <= 0:  # If there's not more space, returns
                self.sound.play_event_error()
                return False

        new_string = self._input_string[0:self._cursor_position] + \
                     text[0:text_end] + \
                     self._input_string[self._cursor_position:len(self._input_string)]

        # If string is valid
        if self._check_input_type(new_string):

            # Update char size
            for char in new_string:
                if char not in self._keychar_size:
                    self._get_char_size(char)  # This updates the self._keychar_size variable

            self.sound.play_key_add()
            self._input_string = new_string  # For a purpose of computing render_box
            for i in range(len(text)):  # Move cursor
                self._move_cursor_right()
            self._update_input_string(new_string)
            self.change()
            self._update_maxlimit_renderbox()
            self._block_copy_paste = True
        else:
            self.sound.play_event_error()
            return False

        return True

    def _update_from_history(self):
        """
        Update all from history.

        :return: None
        """
        self._input_string = self._history[self._history_index]
        self._renderbox[0] = self._history_renderbox[self._history_index][0]
        self._renderbox[1] = self._history_renderbox[self._history_index][1]
        self._renderbox[2] = self._history_renderbox[self._history_index][2]
        self._cursor_position = self._history_cursor[self._history_index]
        self._cursor_render = True

    def _undo(self):
        """
        Undo operation.

        :return: None
        """
        if self._history_index == 0:  # There's no back history
            return False
        if self._history_index == len(self._history):  # If the actual is the last
            self._history_index -= 1
        self._history_index = max(0, self._history_index - 1)
        self._update_from_history()
        return True

    def _redo(self):
        """
        Redo operation.

        :return: None
        """
        if self._history_index == len(self._history) - 1:  # There's no forward history
            return False
        self._history_index = min(len(self._history) - 1, self._history_index + 1)
        self._update_from_history()
        return True

    def _remove_selection(self):
        """
        Remove text from selection.

        :return: None
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

    def _backspace(self, update_history=True):
        """
        Backspace event.

        :param update_history: Updates history on deletion
        :type update_history: bool
        :return: None
        """
        new_string = (
                self._input_string[:max(self._cursor_position - 1, 0)]
                + self._input_string[self._cursor_position:]
        )
        self._update_input_string(new_string, update_history=update_history)
        self._update_renderbox(left=-1, addition=True)

        # Subtract one from cursor_pos, but do not go below zero:
        self._cursor_position = max(self._cursor_position - 1, 0)

    def _delete(self, update_history=True):
        """
        Delete event.

        :param update_history: Updates history on deletion
        :type update_history: bool
        :return: None
        """
        new_string = (
                self._input_string[:self._cursor_position]
                + self._input_string[self._cursor_position + 1:]
        )
        self._update_input_string(new_string, update_history=update_history)
        self._update_renderbox(right=-1, addition=True)

    def _select_all(self):
        """
        Select all text.

        :return: None
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

    def _push_key_input(self, keychar, sounds=True):
        """
        Insert a key in the cursor position.

        :param keychar: Char to be inserted
        :type keychar: str
        :param sounds: Use widget sounds
        :type sounds: bool
        :return: If False the event loop breaks
        :rtype: bool
        """
        # If selected text
        if self._selection_surface:
            self._remove_selection()

        # Check input exceeded the limit returns
        if self._check_input_size():
            if sounds:
                self.sound.play_event_error()
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
                self.sound.play_event_error()
            return False

        # If data is valid
        if self._check_input_type(new_string):
            lkey = len(keychar)
            if lkey > 0:

                # Update char size
                if keychar not in self._keychar_size.keys():
                    self._get_char_size(keychar)  # This updates keychar size data
                self._last_char = keychar

                # Update string
                if sounds:
                    self.sound.play_key_add()
                self._cursor_position += 1  # Some are empty, e.g. K_UP
                self._input_string = new_string  # Only here this is changed (due to renderbox update)
                self._update_input_string(new_string)  # Update the string and the history
                self._update_renderbox(right=1, addition=True)
                self.change()
                return True
        else:
            if sounds:
                self.sound.play_event_error()
        return False

    # noinspection PyMissingOrEmptyDocstring
    def update(self, events):
        updated = False
        events = self._merge_events(events)  # Extend events with custom events

        for event in events:  # type: pygame.event.Event

            if event.type == pygame.KEYDOWN:

                # Check if any key is pressed, if True the event is invalid
                if not check_key_pressed_valid(event):
                    continue

                self._cursor_visible = True  # So the user sees where he writes
                self._key_is_pressed = True
                self._last_key = event.key

                # If none exist, create counter for that key:
                if event.key not in self._keyrepeat_counters and event.key not in self._ignore_keys and \
                        'unicode' in event.dict:
                    self._keyrepeat_counters[event.key] = [0, event.unicode]

                # User press ctrl+something
                if pygame.key.get_mods() & pygame.KMOD_CTRL:

                    # If test, disable CTRL
                    if 'test' in event.dict and event.dict['test']:
                        # noinspection PyArgumentList
                        pygame.key.set_mods(pygame.KMOD_NONE)

                    # Ctrl+C copy
                    if event.key == pygame.K_c:
                        if not self._copy_paste_enabled:
                            self.sound.play_event_error()
                            return
                        self.active = True
                        copy_status = self._copy()
                        if not copy_status:
                            self.sound.play_event_error()
                        return copy_status

                    # Ctrl+V paste
                    elif event.key == pygame.K_v:
                        if not self._copy_paste_enabled:
                            self.sound.play_event_error()
                            return
                        self.active = True
                        return self._paste()

                    # Ctrl+Z undo
                    elif event.key == pygame.K_z:
                        if self._max_history == 0:
                            self.sound.play_event_error()
                            return
                        self.active = True
                        self.sound.play_key_del()
                        return self._undo()

                    # Ctrl+Y redo
                    elif event.key == pygame.K_y:
                        if self._max_history == 0:
                            self.sound.play_event_error()
                            return
                        self.active = True
                        self.sound.play_key_add()
                        return self._redo()

                    # Ctrl+X cut
                    elif event.key == pygame.K_x:
                        if not self._copy_paste_enabled:
                            self.sound.play_event_error()
                            return
                        self.active = True
                        self.sound.play_key_del()
                        return self._cut()

                    # Ctrl+A select all
                    elif event.key == pygame.K_a:
                        if not self._selection_enabled:
                            self.sound.play_event_error()
                            return
                        self.active = True
                        self._select_all()
                        return False

                    # Command not found, returns
                    else:
                        return False

                # Backspace button, delete text from right
                if event.key == pygame.K_BACKSPACE:

                    # Play sound
                    if self._cursor_position == 0:
                        self.sound.play_event_error()
                    else:
                        self.sound.play_key_del()

                    # If text is selected
                    if self._selection_surface:
                        self._remove_selection()
                        return True

                    self._backspace()
                    self.change()
                    self.active = True
                    updated = True

                # Delete button, delete text from left
                elif event.key == pygame.K_DELETE:

                    # Play sound
                    if self._cursor_position == len(self._input_string):
                        self.sound.play_event_error()
                    else:
                        self.sound.play_key_del()

                    # If text is selected
                    if self._selection_surface:
                        self._remove_selection()
                        return True

                    self._delete()
                    self.change()
                    self.active = True
                    updated = True

                # Right arrow
                elif event.key == pygame.K_RIGHT:

                    # Play sound
                    if self._cursor_position == len(self._input_string):
                        self.sound.play_event_error()
                    else:
                        self.sound.play_key_add()

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
                            return

                    # Move cursor
                    self._move_cursor_right()
                    self.active = True
                    updated = True

                # Left arrow
                elif event.key == pygame.K_LEFT:

                    # Play sound
                    if self._cursor_position == 0:
                        self.sound.play_event_error()
                    else:
                        self.sound.play_key_add()

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
                            return

                    # Move cursor
                    self._move_cursor_left()
                    self.active = True
                    updated = True

                # Up arrow
                elif event.key == _controls.KEY_MOVE_UP:
                    self.active = False

                # Down arrow
                elif event.key == _controls.KEY_MOVE_DOWN:
                    self.active = False

                # End
                elif event.key == pygame.K_END:
                    self.sound.play_key_add()
                    self._cursor_position = len(self._input_string)
                    self._update_renderbox(end=True)
                    self._unselect_text()
                    self.active = True
                    updated = True

                # Home
                elif event.key == pygame.K_HOME:
                    self.sound.play_key_add()
                    self._cursor_position = 0
                    self._update_renderbox(start=True)
                    self._unselect_text()
                    self.active = True
                    updated = True

                # Tab
                elif event.key == pygame.K_TAB:
                    for _ in range(self._tab_size):
                        self._push_key_input(' ')
                        updated = True
                    self.active = True

                # Enter
                elif event.key == _controls.KEY_APPLY:
                    self.sound.play_open_menu()
                    self.apply()
                    self._unselect_text()
                    updated = True
                    self.active = not self.active

                # Escape
                elif event.key == pygame.K_ESCAPE:
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
                    return False

                # Any other key, add as input
                elif event.key not in self._ignore_keys:
                    if not self._push_key_input(event.unicode):  # Error in char, not valid or string limit exceeds
                        break
                    self.active = True
                    updated = True

            elif event.type == pygame.KEYUP:
                # Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self._keyrepeat_counters:
                    del self._keyrepeat_counters[event.key]

                # If selection keys are released, stop selection
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    self._selection_active = False

                # Release inputs
                self._block_copy_paste = False
                self._key_is_pressed = False

            elif self.mouse_enabled and event.type == pygame.MOUSEBUTTONUP:
                if self._rect.collidepoint(*event.pos) and \
                        self.get_selected_time() > 1.5 * self._keyrepeat_mouse_interval_ms:
                    self._absolute_origin = getattr(event, 'origin', self._absolute_origin)
                    self._selection_active = False
                    self._check_mouse_collide_input(event.pos)
                    self._cursor_ms_counter = 0

            elif self.mouse_enabled and event.type == pygame.MOUSEBUTTONDOWN:
                if self.get_selected_time() > self._keyrepeat_mouse_interval_ms:
                    self._absolute_origin = getattr(event, 'origin', self._absolute_origin)
                    if self._selection_active:
                        self._unselect_text()
                    self._cursor_ms_counter = 0
                    self._selection_active = True
                    self._selection_mouse_first_position = -1
                    self.active = True

            elif self.touchscreen_enabled and event.type == pygame.FINGERUP:
                window_size = self.get_menu().get_window_size()
                finger_pos = (event.x * window_size[0], event.y * window_size[1])
                if self._rect.collidepoint(finger_pos) and \
                        self.get_selected_time() > 1.5 * self._keyrepeat_touch_interval_ms:
                    self._absolute_origin = getattr(event, 'origin', self._absolute_origin)
                    self._selection_active = False
                    self._check_touch_collide_input(finger_pos)
                    self._cursor_ms_counter = 0

            elif self.touchscreen_enabled and event.type == pygame.FINGERDOWN:
                if self.get_selected_time() > self._keyrepeat_touch_interval_ms:
                    self._absolute_origin = getattr(event, 'origin', self._absolute_origin)
                    if self._selection_active:
                        self._unselect_text()
                    self._cursor_ms_counter = 0
                    self._selection_active = True
                    self._selection_touch_first_position = -1
                    self.active = True

        # Get time clock
        time_clock = self._clock.get_time()
        self._keyrepeat_mouse_ms += time_clock

        # Check mouse pressed
        # noinspection PyArgumentList
        mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()
        self._mouse_is_pressed = mouse_left or mouse_right or mouse_middle

        if self._keyrepeat_mouse_ms > self._keyrepeat_mouse_interval_ms:
            self._keyrepeat_mouse_ms = 0
            if mouse_left:
                pos = pygame.mouse.get_pos()
                self._check_mouse_collide_input((pos[0] - self._absolute_origin[0],
                                                 pos[1] - self._absolute_origin[1]))

        # Update key counters:
        for key in self._keyrepeat_counters:
            self._keyrepeat_counters[key][0] += time_clock  # Update clock

            # Generate new key events if enough time has passed:
            if self._keyrepeat_counters[key][0] >= self._keyrepeat_initial_interval_ms:
                self._keyrepeat_counters[key][0] = self._keyrepeat_initial_interval_ms - self._keyrepeat_interval_ms

                event_key, event_unicode = key, self._keyrepeat_counters[key][1]
                try:
                    # noinspection PyArgumentList
                    self._add_event(
                        pygame.event.Event(pygame.KEYDOWN,
                                           key=event_key,
                                           unicode=event_unicode)
                    )
                except pygame.error:  # If the keys are too fast pygame can raise a Sound Exception
                    pass

        self._cursor_ms_counter += time_clock
        if self._cursor_ms_counter >= self._cursor_switch_ms:
            self._cursor_ms_counter %= self._cursor_switch_ms
            self._cursor_visible = not self._cursor_visible

        return updated
