# coding=utf-8
"""
SELECTOR
Selector class, manage elements and adds entries to menu.

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

import os.path
import pygame


class TextInput(object):

    """
    Text input object
    """

    def __init__(self,
                 font,
                 label="",
                 default="",
                 font_size=35,
                 antialias=True,
                 text_color=(0, 0, 0),
                 cursor_color=(0, 0, 1),
                 repeat_keys_initial_ms=400,
                 repeat_keys_interval_ms=35,
                 onchange=None, onreturn=None, **kwargs):
        """
        :param font: Name or list of names for font (see pygame.font.match_font for precise format)
        :param default: Initial text to be displayed
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param text_color: Color of text (duh)
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :param onchange: Event when changing the selector
        :param onreturn: Event when pressing return button
        :param kwargs: Optional arguments

        :type onchange: function, NoneType
        :type onreturn: function, NoneType
        """
        self._input_string = default  # Inputted text
        self._kwargs = kwargs
        self._on_change = onchange
        self._on_return = onreturn

        self.label = label
        self.antialias = antialias
        self.text_color = text_color
        self.text_size = font_size

        if isinstance(font, pygame.font.Font):
            self.font_object = font
        else:
            if not os.path.isfile(font):
                font = pygame.font.match_font(font)
            self.font_object = pygame.font.Font(font, font_size)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.text_size / 20 + 1), self.text_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(default)  # Inside text
        self.cursor_visible = True  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pygame.K_BACKSPACE:
                    self._input_string = (
                        self._input_string[:max(self.cursor_position - 1, 0)]
                        + self._input_string[self.cursor_position:]
                    )

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pygame.K_DELETE:
                    self._input_string = (
                        self._input_string[:self.cursor_position]
                        + self._input_string[self.cursor_position + 1:]
                    )

                elif event.key == pygame.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self._input_string))

                elif event.key == pygame.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pygame.K_END:
                    self.cursor_position = len(self._input_string)

                elif event.key == pygame.K_HOME:
                    self.cursor_position = 0

                else:
                    # If no special key is pressed, add unicode of key to input_string
                    self._input_string = (
                        self._input_string[:self.cursor_position]
                        + event.unicode
                        + self._input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pygame.KEYUP:
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
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=event_key, unicode=event_unicode))

        # Update self.cursor_visible
        self.cursor_ms_counter += self.clock.get_time()
        if self.cursor_ms_counter >= self.cursor_switch_ms:
            self.cursor_ms_counter %= self.cursor_switch_ms
            self.cursor_visible = not self.cursor_visible

    def apply(self):
        """
        Apply the selected item when return event.

        :return: None
        """
        if self._on_return is not None:
            if len(self._kwargs) > 0:
                self._on_return(self.get_value(), **self._kwargs)
            else:
                self._on_return(self.get_value())

    def change(self):
        """
        Apply the selected item after change event is triggered.

        :return: None
        """
        if self._on_change is not None:
            if len(self._kwargs) > 0:
                self._on_change(self.get_value(), **self._kwargs)
            else:
                self._on_change(self.get_value())

    def clear(self):
        """
        Clear the current text.

        :return: None
        """
        self._input_string = ""
        self.cursor_position = 0

    def draw(self, surface, pos):
        """
        Return surface.

        :return: Surface
        :rtype: str
        """
        #
        self.clock.tick()

        # Re-render text surface:
        text = self.font_object.render(self.label + self._input_string, self.antialias, self.text_color)
        surface.blit(text, pos)

        if self.cursor_visible:
            cursor_x_pos = self.font_object.size(self.label + self._input_string[:self.cursor_position])[0]
            # Without this, the cursor is invisible when self.cursor_position > 0:
            if self.cursor_position > 0 or (self.label and self.cursor_position == 0):
                cursor_x_pos -= self.cursor_surface.get_width()

            cursor_y_pos = (text.get_height() - self.text_size) / 2
            surface.blit(self.cursor_surface, (pos[0] + cursor_x_pos, pos[1] + cursor_y_pos))

    def get_value(self):
        """
        Return the value of the text input.

        :return: text
        :rtype: str
        """
        return self._input_string

    def set_value(self, text):
        """
        Set the value of the text input.

        :return: None
        """
        self._input_string = text

    def set_text_color(self, color):
        """
        Set the font color.

        :return: None
        """
        self.text_color = color
