# -*- coding: utf-8 -*-
"""
TEXT INPUT
Text input class, this widget lets user to write text.

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
"""

import pygame as _pygame
from pygameMenu import config_controls as _ctrl
from pygameMenu.widgets.abstract import Widget


class TextInput(Widget):
    """
    Text input widget.
    """

    def __init__(self,
                 label='',
                 default='',
                 textinput_id='',
                 antialias=True,
                 cursor_color=(0, 0, 1),
                 maxlength=0,
                 maxsize=0,
                 onchange=None,
                 onreturn=None,
                 repeat_keys_initial_ms=400,
                 repeat_keys_interval_ms=35,
                 text_ellipsis='...',
                 **kwargs
                 ):
        """
        Description of the specific paramaters (see Widget class for generic ones):

        :param label: Input label text
        :param default: Initial text to be displayed
        :param textinput_id: Id of the text input
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param cursor_color: Color of cursor
        :param maxlength: Maximum length of input
        :param maxsize: Maximum size of the text to be displayed (overflow)
        :param onchange: callback when changing the selector
        :param onreturn: callback when pressing return button
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :param text_ellipsis: Ellipsis text when overflow occurs
        :param kwargs: Optional keyword-arguments for callbacks
        :type label: basestring
        :type default: basestring
        :type textinput_id: basestring
        :type antialias: bool
        :type cursor_color: tuple
        :type maxlength: int
        :type maxsize: int
        :type onchange: function, NoneType
        :type onreturn: function, NoneType
        :type repeat_keys_initial_ms: float, int
        :type repeat_keys_interval_ms: float, int
        :type text_ellipsis: basestring
        """
        super(TextInput, self).__init__(widget_id=textinput_id, onchange=onchange,
                                        onreturn=onreturn, kwargs=kwargs)
        if maxlength < 0:
            raise Exception('maxlength must be equal or greater than zero')
        if maxsize < 0:
            raise Exception('maxsize must be equal or greater than zero')

        self._antialias = antialias
        self._input_string = default  # Inputted text
        self._ignore_keys = (_ctrl.MENU_CTRL_UP, _ctrl.MENU_CTRL_DOWN, _pygame.K_ESCAPE,
                             _pygame.K_NUMLOCK, _pygame.K_TAB, _pygame.K_CAPSLOCK)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self._keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self._keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self._keyrepeat_interval_ms = repeat_keys_interval_ms

        # Render box (overflow)
        self._renderbox = [0, 0, 0]  # Left/Right/Inner
        self._ellipsis = text_ellipsis

        # Things cursor:
        self._cursor_color = cursor_color
        self._cursor_surface = None
        self._cursor_position = len(default)  # Inside text
        self._cursor_visible = False  # Switches every self._cursor_switch_ms ms
        self._cursor_switch_ms = 500  # /|\
        self._cursor_ms_counter = 0
        self._clock = _pygame.time.Clock()

        # Public attributs
        self.label = label
        self.maxsize = maxsize
        self.maxlength = maxlength

    def clear(self):
        """
        Clear the current text.

        :return: None
        """
        self._input_string = ''
        self._cursor_position = 0

    def draw(self, surface):
        """
        See upper class doc.
        """
        self._clock.tick()
        self._render()

        if not self._cursor_surface:
            self._cursor_surface=_pygame.Surface((int(self._font_size / 20 + 1), self._rect.height - 2))
            self._cursor_surface.fill(self._cursor_color)

        if self._shadow:
            string = self.label + self._input_string
            text_bg = self._font.render(string, self._antialias, self._shadow_color)
            surface.blit(text_bg, self._rect.move(-3, -3).topleft)

        surface.blit(self._surface, (self._rect.x, self._rect.y))

        if self._cursor_visible and self.selected:
            if self.maxsize == 0 or len(self._input_string) <= self.maxsize:  # If no limit is provided
                cursor_x_pos = 2 + self._font.size(self.label + self._input_string[:self._cursor_position])[0]
            else:  # Calculate position depending on renderbox
                sstring = self._input_string
                sstring = sstring[self._renderbox[0]:(self._renderbox[0] + self._renderbox[2])]
                cursor_x_pos = 2 + self._font.size(self.label + sstring)[0]

                # Add ellipsis
                delta = self._font.size(self._ellipsis)[0]
                if self._renderbox[0] != 0 and \
                        self._renderbox[1] != len(self._input_string):  # If Left+Right ellipsis
                    delta *= 1
                elif self._renderbox[1] != len(self._input_string):  # Right ellipsis
                    delta *= 0
                elif self._renderbox[0] != 0:  # Left ellipsis
                    delta *= 1
                else:
                    delta *= 0
                cursor_x_pos += delta

            # Without this, the cursor is invisible when self._cursor_position > 0:
            if self._cursor_position > 0 or (self.label and self._cursor_position == 0):
                cursor_x_pos -= self._cursor_surface.get_width()

            cursor_y_pos = 1
            surface.blit(self._cursor_surface, (self._rect.x + cursor_x_pos, self._rect.y + cursor_y_pos))

    def get_value(self):
        """
        See upper class doc.
        """
        return self._input_string

    def _render(self):
        """
        See upper class doc.
        """
        string = self.label + self._get_input_string()
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        self._surface = self._font.render(string, self._antialias, color)

    def _get_input_string(self):
        """
        Return input string, apply overflow if enabled.

        :return: String
        """
        if self.maxsize != 0 and len(self._input_string) > self.maxsize:
            text = self._input_string[self._renderbox[0]:self._renderbox[1]]
            if self._renderbox[1] != len(self._input_string):  # Right ellipsis
                text += self._ellipsis
            if self._renderbox[0] != 0:  # Left ellipsis
                text = self._ellipsis + text
            return text
        else:
            return self._input_string

    def _update_renderbox(self, left=0, right=0, addition=False, end=False, start=False):
        """
        Update renderbox position.

        :param left: Left update
        :param right: Right update
        :param addition: Update is text addition/deletion
        :param end: Move cursor to end
        :param start: Move cursor to start
        :type left: int
        :type right: int
        :type addition: bool
        :return:
        """
        if self.maxsize == 0:
            return
        ls = len(self._input_string)

        # Move cursor to end
        if end:
            self._renderbox[0] = max(0, ls - self.maxsize)
            self._renderbox[1] = ls
            self._renderbox[2] = min(ls, self.maxsize)
            return

        # Move cursor to start
        if start:
            self._renderbox[0] = 0
            self._renderbox[1] = min(ls, self.maxsize)
            self._renderbox[2] = 0
            return

        # Check limits
        if left < 0 and ls == 0:
            return

        # If no overflow
        if ls <= self.maxsize:
            if right < 0 and self._renderbox[2] == ls:  # If del at the end of string
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
                if right < 0 and self._renderbox[2] == self.maxsize:  # If del at the end of string
                    return
                if left < 0 and self._renderbox[2] == 0:  # If backspace at begining of string
                    return

                # If user deletes something and it is in the end
                if right < 0:  # del
                    if self._renderbox[0] != 0:
                        if (self._renderbox[1] - 1) == ls:  # At the end
                            self._renderbox[2] -= right

                # If the user writes, move renderbox
                if right > 0:
                    if self._renderbox[2] == self.maxsize:  # If cursor is at the end push box
                        self._renderbox[0] += right
                        self._renderbox[1] += right
                    self._renderbox[2] += right

                if left < 0:
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
                if self._renderbox[2] > self.maxsize:
                    self._renderbox[0] += right
                    self._renderbox[1] += right

            # Apply string limits
            self._renderbox[1] = max(self.maxsize, min(self._renderbox[1], ls))
            self._renderbox[0] = self._renderbox[1] - self.maxsize

        # Apply limits
        self._renderbox[0] = max(0, self._renderbox[0])
        self._renderbox[1] = max(0, self._renderbox[1])
        self._renderbox[2] = max(0, min(self._renderbox[2], min(self.maxsize, ls)))

    def set_value(self, text):
        """
        See upper class doc.
        """
        self._input_string = text

    def _check_input_size(self):
        """
        Check input size.

        :return: bool, if True the input must be limited
        """
        if self.maxlength == 0:
            return False
        return self.maxlength < len(self._input_string)

    def update(self, events):
        """
        See upper class doc.
        """
        updated = False
        for event in events:
            if event.type == _pygame.KEYDOWN:
                self._cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self._keyrepeat_counters and event.key not in self._ignore_keys:
                    self._keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == _pygame.K_BACKSPACE:
                    self._input_string = (
                            self._input_string[:max(self._cursor_position - 1, 0)]
                            + self._input_string[self._cursor_position:]
                    )
                    self._update_renderbox(left=-1, addition=True)
                    updated = True

                    # Subtract one from cursor_pos, but do not go below zero:
                    self._cursor_position = max(self._cursor_position - 1, 0)

                elif event.key == _pygame.K_DELETE:
                    self._input_string = (
                            self._input_string[:self._cursor_position]
                            + self._input_string[self._cursor_position + 1:]
                    )
                    self._update_renderbox(right=-1, addition=True)
                    updated = True

                elif event.key == _pygame.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self._cursor_position = min(self._cursor_position + 1, len(self._input_string))
                    self._update_renderbox(right=1)
                    updated = True

                elif event.key == _pygame.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self._cursor_position = max(self._cursor_position - 1, 0)
                    self._update_renderbox(left=-1)
                    updated = True

                elif event.key == _pygame.K_END:
                    self._cursor_position = len(self._input_string)
                    self._update_renderbox(end=True)
                    updated = True

                elif event.key == _pygame.K_HOME:
                    self._cursor_position = 0
                    self._update_renderbox(start=True)
                    updated = True

                elif event.key == _ctrl.MENU_CTRL_ENTER:
                    self.apply()
                    updated = True

                elif event.key not in self._ignore_keys:
                    # Check input has not exceeded the limit
                    if self._check_input_size():
                        break
                    # If no special key is pressed, add unicode of key to input_string
                    self._input_string = (
                            self._input_string[:self._cursor_position]
                            + event.unicode
                            + self._input_string[self._cursor_position:]
                    )
                    lkey = len(event.unicode)
                    if lkey > 0:
                        self._cursor_position += lkey  # Some are empty, e.g. K_UP
                        self._update_renderbox(right=1, addition=True)
                    updated = True

            elif event.type == _pygame.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self._keyrepeat_counters:
                    del self._keyrepeat_counters[event.key]

        # Update key counters:
        for key in self._keyrepeat_counters:
            self._keyrepeat_counters[key][0] += self._clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self._keyrepeat_counters[key][0] >= self._keyrepeat_intial_interval_ms:
                self._keyrepeat_counters[key][0] = self._keyrepeat_intial_interval_ms - self._keyrepeat_interval_ms

                event_key, event_unicode = key, self._keyrepeat_counters[key][1]
                # noinspection PyArgumentList
                _pygame.event.post(_pygame.event.Event(_pygame.KEYDOWN,
                                                       key=event_key,
                                                       unicode=event_unicode)
                                   )

        # Update self._cursor_visible
        self._cursor_ms_counter += self._clock.get_time()
        if self._cursor_ms_counter >= self._cursor_switch_ms:
            self._cursor_ms_counter %= self._cursor_switch_ms
            self._cursor_visible = not self._cursor_visible

        return updated
