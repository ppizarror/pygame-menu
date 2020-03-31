# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

COLOR RGB
Color input class, provides 3 number inputs for defining RGB from 0-255.

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

import math as _math
import pygame as _pygame
from pygameMenu.widgets.widget import Widget
import pygameMenu.controls as _ctrl


# noinspection PyTypeChecker
class ColorRGB(Widget):
    """
    Text input widget.
    """

    def __init__(self,
                 label='',
                 colorrgb_id='',
                 input_underline='_',
                 cursor_color=(0, 0, 0),
                 onchange=None,
                 onreturn=None,
                 repeat_keys_initial_ms=450,
                 repeat_keys_interval_ms=80,
                 repeat_mouse_interval_ms=100,
                 **kwargs
                 ):
        """
        Description of the specific paramaters (see Widget class for generic ones):

        :param label: Input label text
        :type label: basestring
        :param colorrgb_id: ID of the text input
        :type colorrgb_id: basestring
        :param input_underline: Character drawn under each number input (rgb channels)
        :type input_underline: basestring
        :param cursor_color: Color of cursor
        :type cursor_color: tuple
        :param onchange: Callback when changing the selector
        :type onchange: function, NoneType
        :param onreturn: Callback when pressing return button
        :type onreturn: function, NoneType
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :type repeat_keys_initial_ms: float, int
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :type repeat_keys_interval_ms: float, int
        :param repeat_mouse_interval_ms: Interval between mouse events when held
        :type repeat_mouse_interval_ms: float, int
        :param kwargs: Optional keyword-arguments for callbacks
        """
        assert isinstance(label, str)
        assert isinstance(colorrgb_id, str)
        assert isinstance(input_underline, str)
        assert isinstance(cursor_color, tuple)
        assert isinstance(repeat_keys_initial_ms, int)
        assert isinstance(repeat_keys_interval_ms, int)
        assert isinstance(repeat_mouse_interval_ms, int)

        super(ColorRGB, self).__init__(widget_id=colorrgb_id,
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

        # Things cursor:
        self._clock = _pygame.time.Clock()
        self._cursor_color = cursor_color
        self._cursor_ms_counter = 0
        self._cursor_offset = -1
        self._cursor_position = 0  # Inside text
        self._cursor_render = True  # If true cursor must be rendered
        self._cursor_surface = None
        self._cursor_surface_pos = [0, 0]  # Position (x,y) of surface
        self._cursor_switch_ms = 500
        self._cursor_visible = False  # Switches every self._cursor_switch_ms ms

        # Other
        self._first_render = True
        self._input_underline = input_underline
        self._input_underline_size = 0
        self._keychar_size = {'': 0}
        self._label = label
        self._label_size = 0
        self._last_char = ''
        self._last_rendered_string = '__pygameMenu__last_render_string__'
        self._last_rendered_surface = None
        self._last_rendered_surface_underline_width = 0

    def _apply_font(self):
        """
        See upper class doc.
        """
        self._label_size = self._font.size(self._label)[0]

        # Generate the underline surface
        self._input_underline_size = self._font.size(self._input_underline)[0]

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
        return value

    def draw(self, surface):
        """
        See upper class doc.
        """
        self._clock.tick()
        self._render()

        # Draw string
        surface.blit(self._surface, (self._rect.x, self._rect.y))

        # Draw cursor
        if self.selected and self._cursor_surface and \
                (self._cursor_visible or (self._mouse_is_pressed or self._key_is_pressed)):
            surface.blit(self._cursor_surface, (self._rect.x + self._cursor_surface_pos[0],
                                                self._rect.y + self._cursor_surface_pos[1]))

    def _render(self):
        """
        See upper class doc.
        """
        string = self._label + self._input_string  # Render string
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

        # Update last rendered
        self._last_rendered_string = string

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

            underline_string = self._input_underline * int(char)

            # Render char
            underline = self.font_render_string(underline_string, color)

            # Create a new surface
            new_width = max(self._label_size + underline.get_size()[0],
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
        string = self._input_string
        cursor_x_pos = self._cursor_offset + \
                       self._font.size(self._label + string[:self._cursor_position])[0]
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

    def _update_cursor_mouse(self, mousex):
        """
        Updates cursor position after mouse click in text.

        :param mousex: Mouse distance relative to surface
        :type mousex: int
        :return: None
        """
        string = self._input_string
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

        self._cursor_position = cursor_pos
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
        assert isinstance(text, (str, int, float))
        print(text)

    def _move_cursor_left(self):
        """
        Move cursor to left position.

        :return: None
        """
        # Subtract one from cursor_pos, but do not go below zero:
        self._cursor_position = max(self._cursor_position - 1, 0)

    def _move_cursor_right(self):
        """
        Move cursor to right position.

        :return: None
        """
        # Add one to cursor_pos, but do not exceed len(input_string)
        self._cursor_position = min(self._cursor_position + 1, len(self._input_string))

    def _blur(self):
        """
        See upper class doc.
        """
        # self._key_is_pressed = False
        self._mouse_is_pressed = False
        self._keyrepeat_mouse_ms = 0
        self._cursor_visible = False

    def _focus(self):
        """
        See upper class doc.
        """
        self._cursor_ms_counter = 0
        self._cursor_visible = True
        self._cursor_render = True

    def _get_char_size(self, char):
        """
        Return char size in pixels.

        :param char: Char
        """
        if char in self._keychar_size.keys():
            return self._keychar_size[char]
        self._keychar_size[char] = self.font_render_string(char).get_size()[0]
        return self._keychar_size[char]

    def _backspace(self):
        """
        Backspace event.

        :return: None
        """
        new_string = (
                self._input_string[:max(self._cursor_position - 1, 0)]
                + self._input_string[self._cursor_position:]
        )
        self._input_string = new_string

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
        self._input_string = new_string

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
                self._cursor_render = True
                self._key_is_pressed = True
                self._last_key = event.key

                # If none exist, create counter for that key:
                if event.key not in self._keyrepeat_counters and event.key not in self._ignore_keys:
                    self._keyrepeat_counters[event.key] = [0, event.unicode]

                # Backspace button, delete text from right
                if event.key == _pygame.K_BACKSPACE:

                    # Play sound
                    if self._cursor_position == 0:
                        self.sound.play_event_error()
                    else:
                        self.sound.play_key_del()

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

                    # Move cursor
                    self._move_cursor_left()
                    updated = True

                # End
                elif event.key == _pygame.K_END:
                    self.sound.play_key_add()
                    self._cursor_position = len(self._input_string)
                    updated = True

                # Home
                elif event.key == _pygame.K_HOME:
                    self.sound.play_key_add()
                    self._cursor_position = 0
                    updated = True

                # Enter
                elif event.key == _ctrl.KEY_APPLY:
                    self.sound.play_open_menu()
                    self.apply()
                    updated = True

                # Escape
                elif event.key == _pygame.K_ESCAPE:
                    return False

                # Any other key, add as input
                elif event.key not in self._ignore_keys:

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
                    if event.unicode in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        lkey = len(event.unicode)
                        if lkey > 0:
                            # Update char size
                            if event.unicode not in self._keychar_size.keys():
                                self._get_char_size(event.unicode)  # This updates keychar size data
                            self._last_char = event.unicode

                            # Update string
                            self.sound.play_key_add()
                            self._cursor_position += 1  # Some are empty, e.g. K_UP
                            self._input_string = new_string  # Only here this is changed (due to renderbox update)
                            self.change()
                            updated = True
                    else:
                        self.sound.play_event_error()

            elif event.type == _pygame.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self._keyrepeat_counters:
                    del self._keyrepeat_counters[event.key]

                # Release inputs
                self._block_copy_paste = False
                self._key_is_pressed = False

            elif self.mouse_enabled and event.type == _pygame.MOUSEBUTTONUP:
                self._check_mouse_collide_input(event.pos)

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
