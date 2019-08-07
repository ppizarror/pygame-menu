# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEXT INPUT
Text input class, this widget lets user to write text.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

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

import math as _math
import pygame as _pygame
from pygameMenu.widgets.widget import Widget
import pygameMenu.controls as _ctrl
import pygameMenu.locals as _locals

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
        :rtype: basestring
        """
        return ''


    class PyperclipException(RuntimeError):
        """
        Pyperclip exception trown by pyperclip.
        """
        pass


# noinspection PyTypeChecker
class TextInput(Widget):
    """
    Text input widget.
    """

    def __init__(self,
                 label='',
                 default='',
                 textinput_id='',
                 input_type=_locals.INPUT_TEXT,
                 input_underline='',
                 cursor_color=(0, 0, 0),
                 enable_selection=True,
                 history=50,
                 maxchar=0,
                 maxwidth=0,
                 maxwidth_dynamically_update=True,
                 onchange=None,
                 onreturn=None,
                 password=False,
                 password_char='*',
                 repeat_keys_initial_ms=400,
                 repeat_keys_interval_ms=40,
                 repeat_mouse_interval_ms=100,
                 selection_color=(30, 30, 30),
                 text_ellipsis='...',
                 **kwargs
                 ):
        """
        Description of the specific paramaters (see Widget class for generic ones):

        :param label: Input label text
        :type label: basestring
        :param default: Initial value to be displayed
        :type default: basestring, int, float
        :param textinput_id: ID of the text input
        :type textinput_id: basestring
        :param input_type: Type of data
        :type input_type: basestring
        :param input_underline: Character drawn under the input
        :type input_underline: basestring
        :param cursor_color: Color of cursor
        :type cursor_color: tuple
        :param enable_selection: Enables selection of text
        :type enable_selection: tuple
        :param history: Maximum number of editions stored
        :type history: int
        :param maxchar: Maximum length of input
        :type maxchar: int
        :param maxwidth: Maximum size of the text to be displayed (overflow)
        :type maxwidth: int
        :param maxwidth_dynamically_update: Dynamically update maxwidth depending on char size
        :type maxwidth_dynamically_update: bool
        :param onchange: Callback when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Callback when pressing return button
        :type onreturn: function, NoneType
        :param password: Input string is displayed as a pasword
        :type password: bool
        :param password_char: Character used by password type
        :type password_char: basestring
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :type repeat_keys_initial_ms: float, int
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :type repeat_keys_interval_ms: float, int
        :param repeat_mouse_interval_ms: Interval between mouse events when held
        :type repeat_mouse_interval_ms: float, int
        :param selection_color: Selection box color
        :type selection_color: tuple
        :param text_ellipsis: Ellipsis text when overflow occurs
        :type text_ellipsis: basestring
        :param kwargs: Optional keyword-arguments for callbacks
        """
        assert isinstance(label, str)
        assert isinstance(default, (str, int, float))
        assert isinstance(textinput_id, str)
        assert isinstance(input_type, str)
        assert isinstance(input_underline, str)
        assert isinstance(cursor_color, tuple)
        assert isinstance(history, int)
        assert isinstance(maxchar, int)
        assert isinstance(maxwidth, int)
        assert isinstance(password, bool)
        assert isinstance(password_char, str)
        assert isinstance(repeat_keys_initial_ms, int)
        assert isinstance(repeat_keys_interval_ms, int)
        assert isinstance(repeat_mouse_interval_ms, int)
        assert isinstance(text_ellipsis, str)

        if history < 0:
            raise ValueError('history must be equal or greater than zero')
        if maxchar < 0:
            raise ValueError('maxchar must be equal or greater than zero')
        if maxwidth < 0:
            raise ValueError('maxwidth must be equal or greater than zero')
        if len(password_char) != 1:
            raise ValueError('password_char must be a character')

        super(TextInput, self).__init__(widget_id=textinput_id,
                                        onchange=onchange,
                                        onreturn=onreturn,
                                        kwargs=kwargs)

        self._input_string = ''  # Inputted text
        self._ignore_keys = (  # Ignore keys on input-gathering events
            _ctrl.KEY_MOVE_DOWN,
            _ctrl.KEY_MOVE_UP,
            _pygame.K_CAPSLOCK,
            _pygame.K_LCTRL,
            _pygame.K_LSHIFT,
            _pygame.K_NUMLOCK,
            _pygame.K_RCTRL,
            _pygame.K_RETURN,
            _pygame.K_RSHIFT,
            _pygame.K_TAB
        )

        # Vars to make keydowns repeat after user pressed a key for some time:
        self._block_copy_paste = False  # Blocks event
        self._key_is_pressed = False
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
        self._renderbox = [0, 0, 0]  # Left/Right/Inner

        # Things cursor:
        self._clock = _pygame.time.Clock()
        self._cursor_color = cursor_color
        self._cursor_ms_counter = 0
        self._cursor_offset = -1
        self._cursor_position = 0  # Inside text
        self._cursor_render = True  # If true cursor must be rendered
        self._cursor_surface = None
        self._cursor_surface_pos = [0, 0]  # Position (x,y) of surface
        self._cursor_switch_ms = 500  # /|\
        self._cursor_visible = False  # Switches every self._cursor_switch_ms ms

        # History of editions
        self._history = []
        self._history_cursor = []
        self._history_renderbox = []
        self._history_index = 0  # Index at which the new editions are added
        self._max_history = history

        # Text selection
        self._last_selection_render = [0, 0]
        self._selection_active = False
        self._selection_enabled = enable_selection
        self._selection_box = [0, 0]  # [from, to]
        self._selection_color = selection_color
        self._selection_mouse_first_position = -1
        self._selection_position = [0, 0]  # (x,y)
        self._selection_render = False
        self._selection_surface = None  # type: _pygame.SurfaceType

        # Other
        self._first_render = True
        self._input_type = input_type
        self._input_underline = input_underline
        self._input_underline_size = 0
        self._keychar_size = {'': 0}
        self._label = label
        self._label_size = 0
        self._last_char = ''
        self._last_rendered_string = '__pygameMenu__last_render_string__'
        self._last_rendered_surface = None
        self._last_rendered_surface_underline_width = 0
        self._maxchar = maxchar
        self._maxwidth = maxwidth  # This value will be changed depending on how many chars are printed
        self._maxwidth_base = maxwidth
        self._maxwidth_update = maxwidth_dynamically_update
        self._maxwidthsize = 0  # Updated in font
        self._password = password
        self._password_char = password_char

        # If password is active no default value should exist
        if self._password and default != '':
            raise ValueError('default value must be empty if the input is a password')

        # Set default value
        self.set_value(default)

    def _apply_font(self):
        """
        See upper class doc.
        """
        self._ellipsis_size = self._font.size(self._ellipsis)[0]
        self._label_size = self._font.size(self._label)[0]

        # Generate the underline surface
        self._input_underline_size = self._font.size(self._input_underline)[0]

        # Size of maxwidth if not zero
        self._maxwidthsize = self.font_render_string('O' * self._maxwidth_base).get_size()[0]

        # Update password char size
        if self._password:
            password_size = self.font_render_string(self._password_char).get_size()[0]
            if password_size == 0:
                raise ValueError(
                    'Password character is not valid, the size of the font is zero, use another character or change the font')
            self._keychar_size[self._password_char] = password_size

    def clear(self):
        """
        Clear the current text.

        :return: None
        """
        self._input_string = ''
        self._cursor_position = 0

    def get_value(self):
        """
        See upper class doc.
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

    def draw(self, surface):
        """
        See upper class doc.
        """
        self._clock.tick()
        self._render()

        # Draw selection first
        if self._selection_surface is not None:
            surface.blit(self._selection_surface, (self._selection_position[0], self._selection_position[1]))

        # Draw string
        surface.blit(self._surface, (self._rect.x, self._rect.y))

        # Draw cursor
        if self.selected and self._cursor_surface and (
                self._cursor_visible or (self._mouse_is_pressed or self._key_is_pressed)):
            surface.blit(self._cursor_surface, (self._rect.x + self._cursor_surface_pos[0],
                                                self._rect.y + self._cursor_surface_pos[1]))

    def _render(self):
        """
        See upper class doc.
        """
        string = self._label + self._get_input_string()  # Render string
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        updated_surface = self._render_string_surface(string, color)

        # Apply render methods after first rendering call
        if self._first_render:
            self._first_render = False
            return

        # Apply underline if exists
        self._surface = self._render_underline(string, color, updated_surface)

        # Render the cursor
        self._render_cursor()

        # Render the selection box if text is selected
        self._render_selection_box()

        # Update last rendered
        self._last_rendered_string = string

    def _render_selection_box(self, force=False):
        """
        Render selected text.

        :param force: Force update
        :type force: bool
        :return: None
        """
        if not self._selection_enabled:
            return

        if self._selection_active and (
                self._last_selection_render[0] != self._selection_box[0] or self._last_selection_render[1] !=
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

            x1 = self._cursor_offset + self._font.size(self._label + string_init)[0]
            x2 = self._cursor_offset + self._font.size(self._label + string_final)[0] - 1

            self._last_selection_render[0] = self._selection_box[0]
            self._last_selection_render[1] = self._selection_box[1]

            x = x2 - x1
            if x <= 0:
                self._selection_surface = None
                return
            y = self._font.size(self._label)[1]

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
            new_surface = _pygame.Surface((x, y), _pygame.SRCALPHA, 32)  # lgtm [py/call/wrong-arguments]
            self._selection_surface = _pygame.Surface.convert_alpha(new_surface)  # type: _pygame.SurfaceType
            self._selection_surface.fill(self._selection_color)
            self._selection_position[0] = x1 + self._rect.x
            self._selection_position[1] = self._rect.y

            # Fill cursor
            if self._cursor_surface:
                self._cursor_surface.fill(self._font_selected_color)

    def _render_string_surface(self, string, color):
        """
        Renders string surface.

        :param string: String to render
        :type string: basestring
        :param color: Color of the string to render
        :type color: tuple
        :return: True if surface is updated
        :rtype: bool
        """
        new_surface = self.render_string(string, color)
        updated_surface = self._last_rendered_surface != new_surface
        if updated_surface:
            self._surface = new_surface
            self._last_rendered_surface = self._surface
        return updated_surface

    def _render_underline(self, string, color, updated):
        """
        Render underline surface.

        :param string: String to render
        :type string: basestring
        :param color: Color of the string to render
        :type color: tuple
        :param updated: Render string has been updated or not
        :type updated: bool
        :return: New rendered surface
        :rtype: pygame.surface.SurfaceType
        """
        # If underline is not enabled
        if self._input_underline_size == 0:
            return self._surface

        # Render input underline
        if string != self._last_rendered_string or updated:
            menu = self.get_menu()

            # Calculate total avaiable space
            current_rect = self._surface.get_rect()  # type: _pygame.rect.RectType
            _, _, menu_width, _ = menu.get_position()
            space_between_label = menu_width - self._label_size - self._rect.x
            char = _math.ceil(space_between_label * 1.0 / self._input_underline_size)  # floor does not work

            # If char limit
            max_width_current = 0
            if self._maxchar != 0 or self._maxwidth != 0:
                max_chars = max(self._maxchar, self._maxwidth_base)
                basechar = 'O'
                if self._password:
                    basechar = self._password_char
                max_size = self.font_render_string(basechar * max_chars)
                max_size = max_size.get_size()[0]
                maxchar_char = _math.ceil(max_size * 1.0 / self._input_underline_size)
                char = min(char, maxchar_char)
                max_width_current = current_rect.width

            underline_string = self._input_underline * int(char)

            # Render char
            underline = self.font_render_string(underline_string, color)

            # Create a new surface
            new_width = max(self._label_size + underline.get_size()[0],
                            max_width_current,
                            self._last_rendered_surface_underline_width)
            new_size = (new_width + 1, current_rect.height + 3)

            new_surface = _pygame.Surface(new_size, _pygame.SRCALPHA, 32)  # lgtm [py/call/wrong-arguments]
            new_surface = _pygame.Surface.convert_alpha(new_surface)  # type: _pygame.SurfaceType

            # Blit current surface
            new_surface.blit(self._surface, (0, 0))
            new_surface.blit(underline, (self._label_size - 1, 6))  # Position (x, y)
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
            self._cursor_surface = _pygame.Surface((int(self._font_size / 20 + 1), self._rect.height - 2))
            self._cursor_surface.fill(self._cursor_color)

        # Get string
        string = self._get_input_string_filtered()

        # Calculate x position
        if self._maxwidth == 0:  # If no limit is provided
            cursor_x_pos = self._cursor_offset + \
                           self._font.size(self._label + string[:self._cursor_position])[0]
        else:  # Calculate position depending on renderbox
            string = string[self._renderbox[0]:(self._renderbox[0] + self._renderbox[2])]
            cursor_x_pos = self._cursor_offset + self._font.size(self._label + string)[0]

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
        if self._cursor_position > 0 or (self._label and self._cursor_position == 0):
            # Without this, the cursor is invisible when self._cursor_position > 0:
            cursor_x_pos -= self._cursor_surface.get_width()

        # Calculate y position
        cursor_y_pos = 0

        # Move x position
        cursor_x_pos += 2

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
        Returns input string where all filters have been applied.

        :return: Filtered string
        :rtype: basestring
        """
        string = self._input_string

        # Apply password
        if self._password:
            string = self._password_char * len(string)

        return string

    def _get_input_string(self, add_ellipsis=True):
        """
        Return input string, apply overflow if enabled.

        :param add_ellipsis: Adds ellipsis text
        :type add_ellipsis: bool
        :return: String
        :rtype: basestring
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
        ls = len(self._input_string)

        # Move cursor to end
        if end:
            self._renderbox[0] = max(0, ls - self._maxwidth)
            self._renderbox[1] = ls
            self._renderbox[2] = min(ls, self._maxwidth)
            return

        # Move cursor to start
        if start:
            self._renderbox[0] = 0
            self._renderbox[1] = min(ls, self._maxwidth)
            self._renderbox[2] = 0
            return

        # Check limits
        if left < 0 and ls == 0:
            return

        # If no overflow
        if ls <= self._maxwidth:
            if right < 0 and self._renderbox[2] == ls:  # If del at the end of string
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
                if left < 0 and self._renderbox[2] == 0:  # If backspace at begining of string
                    return

                # If user deletes something and it is in the end
                if right < 0:  # del
                    if self._ellipsis_left():
                        if (self._renderbox[1] - 1) == ls:  # At the end
                            self._renderbox[2] -= right

                # If the user writes, move renderbox
                if right > 0:
                    if self._renderbox[2] == self._maxwidth:  # If cursor is at the end push box
                        self._renderbox[0] += right
                        self._renderbox[1] += right
                    self._renderbox[2] += right

                if left < 0:
                    if self._renderbox[0] == 0:  # If cursor is at the begining
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
                if self._renderbox[1] > ls or self._renderbox[0] < 0:
                    if self._renderbox[2] != self._maxwidth - 1:
                        update_maxwidth = False

            # Apply string limits
            self._renderbox[1] = max(self._maxwidth, min(self._renderbox[1], ls))
            self._renderbox[0] = self._renderbox[1] - self._maxwidth

        # Apply limits
        self._renderbox[0] = max(0, self._renderbox[0])
        self._renderbox[1] = max(0, self._renderbox[1])
        self._renderbox[2] = max(0, min(self._renderbox[2], min(self._maxwidth, ls)))

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
                    accum_size += self._keychar_size[char]
                    biggest = max(biggest, self._keychar_size[char])

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
        Updates cursor position after mouse click in text.

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
            if self._label_size + size_sum >= mousex:
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

        # Text does not have ellipsis, infered position is correct
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

    def set_value(self, text):
        """
        See upper class doc.
        """
        if self._check_input_type(text):
            default = str(text)
            self._input_string = default
            for i in range(len(default) + 1):
                self._move_cursor_right()
            self._update_input_string(default)
        else:
            raise ValueError('value "{0}" type is not correct according to input_type'.format(text))

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
        :type string: basestring
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
        """
        See upper class doc.
        """
        # self._key_is_pressed = False
        self._mouse_is_pressed = False
        self._keyrepeat_mouse_ms = 0
        self._cursor_visible = False
        self._unselect_text()
        # self._history_index = len(self._history) - 1

    def _focus(self):
        """
        See upper class doc.
        """
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
        Return text selected.

        :return: Text
        :rtype: basestring
        """
        return self._input_string[self._selection_box[0]:self._selection_box[1]]

    def _update_input_string(self, new_string):
        """
        Update input string with a new string, store changes into history.

        :param new_string: New string of text input
        :type new_string: basestring
        :return: None
        """
        l_history = len(self._history)

        # If last edition is different than the new one -> updates the history
        if ((l_history > 0 and self._history[l_history - 1] != new_string) or l_history == 0) and self._max_history > 0:

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

        :return:
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
                    self._keychar_size[char] = self.font_render_string(char).get_size()[0]

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
                self._delete()
            else:
                self._backspace()

        # Destroy selection
        self._unselect_text()

    def _backspace(self):
        """
        Backspace event.

        :return: None
        """
        new_string = (
                self._input_string[:max(self._cursor_position - 1, 0)]
                + self._input_string[self._cursor_position:]
        )
        self._update_input_string(new_string)
        self._update_renderbox(left=-1, addition=True)

        # Subtract one from cursor_pos, but do not go below zero:
        self._cursor_position = max(self._cursor_position - 1, 0)

    def _delete(self):
        """
        Delete event.

        :return: None
        """
        new_string = (
                self._input_string[:self._cursor_position]
                + self._input_string[self._cursor_position + 1:]
        )
        self._update_input_string(new_string)
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

    def update(self, events):
        """
        See upper class doc.
        """
        updated = False

        for event in events:  # type: _pygame.event.EventType

            if event.type == _pygame.KEYDOWN:

                # Check if any key is pressed, if True the event is invalid
                if not self.check_key_pressed_valid(event):
                    continue

                self._cursor_visible = True  # So the user sees where he writes
                self._key_is_pressed = True
                self._last_key = event.key

                # If none exist, create counter for that key:
                if event.key not in self._keyrepeat_counters and event.key not in self._ignore_keys:
                    self._keyrepeat_counters[event.key] = [0, event.unicode]

                # User press ctrl+something
                if _pygame.key.get_mods() & _pygame.KMOD_CTRL:

                    # Ctrl+C copy
                    if event.key == _pygame.K_c:
                        copy_status = self._copy()
                        if not copy_status:
                            self.sound.play_event_error()
                        return copy_status

                    # Ctrl+V paste
                    elif event.key == _pygame.K_v:
                        return self._paste()

                    # Ctrl+Z undo
                    elif event.key == _pygame.K_z:
                        self.sound.play_key_del()
                        return self._undo()

                    # Ctrl+Y redo
                    elif event.key == _pygame.K_y:
                        self.sound.play_key_add()
                        return self._redo()

                    # Ctrl+X cut
                    elif event.key == _pygame.K_x:
                        self.sound.play_key_del()
                        return self._cut()

                    # Ctrl+A select all
                    elif event.key == _pygame.K_a:
                        self._select_all()
                        return False

                    # Command not found, returns
                    else:
                        return False

                # Backspace button, delete text from right
                if event.key == _pygame.K_BACKSPACE:

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
                    updated = True

                # Delete button, delete text from left
                elif event.key == _pygame.K_DELETE:

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
                    updated = True

                # Right arrow
                elif event.key == _pygame.K_RIGHT:

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
                    updated = True

                # Left arrow
                elif event.key == _pygame.K_LEFT:

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
                    updated = True

                # End
                elif event.key == _pygame.K_END:
                    self.sound.play_key_add()
                    self._cursor_position = len(self._input_string)
                    self._update_renderbox(end=True)
                    self._unselect_text()
                    updated = True

                # Home
                elif event.key == _pygame.K_HOME:
                    self.sound.play_key_add()
                    self._cursor_position = 0
                    self._update_renderbox(start=True)
                    self._unselect_text()
                    updated = True

                # Enter
                elif event.key == _ctrl.KEY_APPLY:
                    self.sound.play_open_menu()
                    self.apply()
                    self._unselect_text()
                    updated = True

                # Escape
                elif event.key == _pygame.K_ESCAPE:
                    self._unselect_text()
                    updated = True

                # Press lshift, rshift -> selection
                elif event.key == _pygame.K_LSHIFT or event.key == _pygame.K_RSHIFT:
                    if not self._selection_active:
                        self._selection_active = True
                        self._selection_box[0] = self._cursor_position
                        self._selection_box[1] = self._cursor_position
                    return False

                # Any other key, add as input
                elif event.key not in self._ignore_keys:

                    # If selected text
                    if self._selection_surface:
                        self._remove_selection()

                    # Check input exceeded the limit returns
                    if self._check_input_size():
                        self.sound.play_event_error()
                        break

                    # If no special key is pressed, add unicode of key to input_string
                    new_string = (
                            self._input_string[:self._cursor_position]
                            + event.unicode
                            + self._input_string[self._cursor_position:]
                    )

                    # If unwanted escape sequences
                    event_escaped = repr(event.unicode)
                    if '\\r' in event_escaped:
                        return False

                    # If data is valid
                    if self._check_input_type(new_string):
                        lkey = len(event.unicode)
                        if lkey > 0:

                            # Update char size
                            if event.unicode not in self._keychar_size:
                                self._keychar_size[event.unicode] = self.font_render_string(event.unicode).get_size()[0]
                            self._last_char = event.unicode

                            # Update string
                            self.sound.play_key_add()
                            self._cursor_position += 1  # Some are empty, e.g. K_UP
                            self._input_string = new_string  # Only here this is changed (due to renderbox update)
                            self._update_renderbox(right=1, addition=True)
                            self._update_input_string(new_string)
                            self.change()
                            updated = True

                    else:
                        self.sound.play_event_error()

            elif event.type == _pygame.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self._keyrepeat_counters:
                    del self._keyrepeat_counters[event.key]

                # If selection keys are released, stop selection
                elif event.key == _pygame.K_LSHIFT or event.key == _pygame.K_RSHIFT:
                    self._selection_active = False

                # Release inputs
                self._block_copy_paste = False
                self._key_is_pressed = False

            elif self.mouse_enabled and event.type == _pygame.MOUSEBUTTONUP:
                self._selection_active = False
                self._check_mouse_collide_input(event.pos)

            elif self.mouse_enabled and event.type == _pygame.MOUSEBUTTONDOWN:
                if self._selection_active:
                    self._unselect_text()
                self._selection_active = True
                self._selection_mouse_first_position = -1

        # Get time clock
        time_clock = self._clock.get_time()
        self._keyrepeat_mouse_ms += time_clock

        # Check mouse pressed
        mouse_left, mouse_middle, mouse_right = _pygame.mouse.get_pressed()
        self._mouse_is_pressed = mouse_left or mouse_right or mouse_middle

        if self._keyrepeat_mouse_ms > self._keyrepeat_mouse_interval_ms:
            self._keyrepeat_mouse_ms = 0
            if mouse_left:
                self._check_mouse_collide_input(_pygame.mouse.get_pos())

        # Update key counters:
        for key in self._keyrepeat_counters:
            self._keyrepeat_counters[key][0] += time_clock  # Update clock

            # Generate new key events if enough time has passed:
            if self._keyrepeat_counters[key][0] >= self._keyrepeat_initial_interval_ms:
                self._keyrepeat_counters[key][0] = self._keyrepeat_initial_interval_ms - self._keyrepeat_interval_ms

                event_key, event_unicode = key, self._keyrepeat_counters[key][1]
                # noinspection PyArgumentList
                _pygame.event.post(_pygame.event.Event(_pygame.KEYDOWN,
                                                       key=event_key,
                                                       unicode=event_unicode)
                                   )

        # Update self._cursor_visible
        self._cursor_ms_counter += time_clock
        if self._cursor_ms_counter >= self._cursor_switch_ms:
            self._cursor_ms_counter %= self._cursor_switch_ms
            self._cursor_visible = not self._cursor_visible

        return updated
