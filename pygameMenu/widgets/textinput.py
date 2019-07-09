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
                 label="",
                 default="",
                 antialias=True,
                 cursor_color=(0, 0, 1),
                 repeat_keys_initial_ms=400,
                 repeat_keys_interval_ms=35,
                 maxlength=0,
                 onchange=None,
                 onreturn=None,
                 **kwargs
                 ):
        """
        Description of the specific paramaters (see Widget class for generic ones):

        :param label: Input label text
        :param default: Initial text to be displayed
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :param maxlength: Maximum length of input
        """
        super(TextInput, self).__init__(onchange, onreturn, kwargs=kwargs)
        if maxlength < 0:
            raise Exception('maxlength must be equal or greater than zero')

        self._input_string = default  # Inputted text
        self._ignore_keys = (_ctrl.MENU_CTRL_UP, _ctrl.MENU_CTRL_DOWN)

        self.label = label
        self.antialias = antialias
        self.maxlength = maxlength

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = _pygame.Surface((int(self._font_size / 20 + 1), self._font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(default)  # Inside text
        self.cursor_visible = False  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = _pygame.time.Clock()

    def clear(self):
        """
        Clear the current text.

        :return: None
        """
        self._input_string = ""
        self.cursor_position = 0

    def draw(self, surface):
        """
        See upper class doc.
        """
        self.clock.tick()
        self._render()

        if self._shadow:
            string = self.label + self._input_string
            text_bg = self._font.render(string, self.antialias, self._shadow_color)
            surface.blit(text_bg, self._rect.move(-3, -3).topleft)

        surface.blit(self._surface, (self._rect.x, self._rect.y))

        if self.cursor_visible and self.selected:
            cursor_x_pos = self._font.size(self.label + self._input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0 or (self.label and self.cursor_position == 0):
                cursor_x_pos -= self.cursor_surface.get_width()

            cursor_y_pos = (self._surface.get_height() - self._font_size) / 2
            surface.blit(self.cursor_surface, (self._rect.x + cursor_x_pos, self._rect.y + cursor_y_pos))

    def get_value(self):
        """
        See upper class doc.
        """
        return self._input_string

    def _render(self):
        """
        See upper class doc.
        """
        string = self.label + self._input_string
        if self.selected:
            color = self._font_selected_color
        else:
            color = self._font_color
        self._surface = self._font.render(string, self.antialias, color)

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
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters and event.key not in self._ignore_keys:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == _pygame.K_BACKSPACE:
                    self._input_string = (
                            self._input_string[:max(self.cursor_position - 1, 0)]
                            + self._input_string[self.cursor_position:]
                    )
                    updated = True

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == _pygame.K_DELETE:
                    self._input_string = (
                            self._input_string[:self.cursor_position]
                            + self._input_string[self.cursor_position + 1:]
                    )
                    updated = True

                elif event.key == _pygame.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self._input_string))
                    updated = True

                elif event.key == _pygame.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                    updated = True

                elif event.key == _pygame.K_END:
                    self.cursor_position = len(self._input_string)
                    updated = True

                elif event.key == _pygame.K_HOME:
                    self.cursor_position = 0
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
                            self._input_string[:self.cursor_position]
                            + event.unicode
                            + self._input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP
                    updated = True

            elif event.type == _pygame.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = self.keyrepeat_intial_interval_ms - self.keyrepeat_interval_ms

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                # noinspection PyArgumentList
                _pygame.event.post(_pygame.event.Event(_pygame.KEYDOWN,
                                                       key=event_key,
                                                       unicode=event_unicode))

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

        return updated
