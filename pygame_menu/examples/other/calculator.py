"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - CALCULATOR
Simple calculator app.

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

__all__ = ['main']

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Union, List


class CalculatorApp(object):
    """
    Simple calculator app.
    """
    op: str  # Operation
    prev: str  # Prev value
    curr: str  # Current value
    menu: 'pygame_menu.Menu'
    screen: 'pygame_menu.widgets.Label'
    surface: 'pygame.Surface'

    # noinspection PyArgumentEqualDefault
    def __init__(self) -> None:
        """
        Constructor.
        """
        self.surface = create_example_window('Example - Calculator', (320, 480))

        # Configure theme
        theme = pygame_menu.Theme()

        theme.background_color = (43, 43, 43)
        theme.title_background_color = (43, 43, 43)
        theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
        theme.title_close_button_cursor = pygame_menu.locals.CURSOR_HAND
        theme.title_font_size = 35
        theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        theme.widget_background_color = None
        theme.widget_font = pygame_menu.font.FONT_DIGITAL
        theme.widget_font_color = (255, 255, 255)
        theme.widget_font_size = 40
        theme.widget_padding = 0
        theme.widget_selection_effect = \
            pygame_menu.widgets.HighlightSelection(1, 0, 0).set_color((120, 120, 120))

        self.menu = pygame_menu.Menu('', 320, 480,
                                     center_content=False,
                                     mouse_motion_selection=True,
                                     onclose=pygame_menu.events.EXIT,
                                     overflow=False,
                                     theme=theme,
                                     )
        menu_deco = self.menu.get_scrollarea().get_decorator()

        # Add the layout
        self.menu.add.vertical_margin(40)
        menu_deco.add_rectangle(10, 88, 300, 55, (60, 63, 65), use_center_positioning=False)
        self.screen = self.menu.add.label('0', background_color=None, margin=(10, 0),
                                          selectable=True, selection_effect=None)
        self.menu.add.vertical_margin(20)

        cursor = pygame_menu.locals.CURSOR_HAND

        # Add horizontal frames
        f1 = self.menu.add.frame_h(299, 54, margin=(10, 0))
        b1 = f1.pack(self.menu.add.button('1', lambda: self._press(1), cursor=cursor))
        b2 = f1.pack(self.menu.add.button('2', lambda: self._press(2), cursor=cursor),
                     align=pygame_menu.locals.ALIGN_CENTER)
        b3 = f1.pack(self.menu.add.button('3', lambda: self._press(3), cursor=cursor),
                     align=pygame_menu.locals.ALIGN_RIGHT)
        self.menu.add.vertical_margin(10)

        f2 = self.menu.add.frame_h(299, 54, margin=(10, 0))
        b4 = f2.pack(self.menu.add.button('4', lambda: self._press(4), cursor=cursor))
        b5 = f2.pack(self.menu.add.button('5', lambda: self._press(5), cursor=cursor),
                     align=pygame_menu.locals.ALIGN_CENTER)
        b6 = f2.pack(self.menu.add.button('6', lambda: self._press(6), cursor=cursor),
                     align=pygame_menu.locals.ALIGN_RIGHT)
        self.menu.add.vertical_margin(10)

        f3 = self.menu.add.frame_h(299, 54, margin=(10, 0))
        b7 = f3.pack(self.menu.add.button('7', lambda: self._press(7), cursor=cursor))
        b8 = f3.pack(self.menu.add.button('8', lambda: self._press(8), cursor=cursor),
                     align=pygame_menu.locals.ALIGN_CENTER)
        b9 = f3.pack(self.menu.add.button('9', lambda: self._press(9), cursor=cursor),
                     align=pygame_menu.locals.ALIGN_RIGHT)
        self.menu.add.vertical_margin(10)

        f4 = self.menu.add.frame_h(299, 54, margin=(10, 0))
        b0 = f4.pack(self.menu.add.button('0', lambda: self._press(0), cursor=cursor))
        b_plus = f4.pack(self.menu.add.button('+', lambda: self._press('+'), cursor=cursor),
                         align=pygame_menu.locals.ALIGN_CENTER)
        b_minus = f4.pack(self.menu.add.button('-', lambda: self._press('-'), cursor=cursor),
                          align=pygame_menu.locals.ALIGN_RIGHT)
        self.menu.add.vertical_margin(10)

        f5 = self.menu.add.frame_h(299, 54, margin=(10, 0))
        b_times = f5.pack(self.menu.add.button('x', lambda: self._press('x'), cursor=cursor))
        b_div = f5.pack(self.menu.add.button('/', lambda: self._press('/'), cursor=cursor),
                        align=pygame_menu.locals.ALIGN_CENTER)
        beq = f5.pack(self.menu.add.button('=', lambda: self._press('='), cursor=cursor),
                      align=pygame_menu.locals.ALIGN_RIGHT)

        # Add decorator for each object
        for widget in (b1, b2, b3, b4, b5, b6, b7, b8, b9, b0, beq, b_plus,
                       b_minus, b_times, b_div):
            w_deco = widget.get_decorator()
            if widget != beq:
                w_deco.add_rectangle(-37, -27, 74, 54, (15, 15, 15))
                on_layer = w_deco.add_rectangle(-37, -27, 74, 54, (84, 84, 84))
            else:
                w_deco.add_rectangle(-37, -27, 74, 54, (38, 96, 103))
                on_layer = w_deco.add_rectangle(-37, -27, 74, 54, (40, 171, 187))
            w_deco.disable(on_layer)
            widget.set_attribute('on_layer', on_layer)

            def widget_select(sel: bool, wid: 'pygame_menu.widgets.Widget', _):
                """
                Function triggered if widget is selected
                """
                lay = wid.get_attribute('on_layer')
                if sel:
                    wid.get_decorator().enable(lay)
                else:
                    wid.get_decorator().disable(lay)

            widget.set_onselect(widget_select)
            widget.set_padding((2, 19, 0, 23))
            widget._keyboard_enabled = False

        self.prev = ''
        self.curr = ''
        self.op = ''

        self.menu.set_onupdate(self.process_events)
        self.menu.set_onwindowmouseleave(lambda m: self.screen.select(update_menu=True))

    def process_events(self, events: List['pygame.event.Event'], _=None) -> None:
        """
        Process events from user.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # noinspection PyUnresolvedReferences
                if event.key == pygame.K_0:
                    self._press(0)
                elif event.key == pygame.K_1:
                    self._press(1)
                elif event.key == pygame.K_2:
                    self._press(2)
                elif event.key == pygame.K_3:
                    self._press(3)
                elif event.key == pygame.K_4:
                    self._press(4)
                elif event.key == pygame.K_5:
                    self._press(5)
                elif event.key == pygame.K_6:
                    self._press(6)
                elif event.key == pygame.K_7:
                    self._press(7)
                elif event.key == pygame.K_8:
                    self._press(8)
                elif event.key == pygame.K_9:
                    self._press(9)
                elif event.key == pygame.K_PLUS:
                    self._press('+')
                elif event.key == pygame.K_MINUS:
                    self._press('-')
                elif event.key == pygame.K_SLASH or \
                        (hasattr(pygame, 'K_PERCENT') and event.key == pygame.K_PERCENT):
                    self._press('/')
                elif event.key == pygame.K_ASTERISK or event.key == pygame.K_x:
                    self._press('x')
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_RETURN:
                    self._press('=')
                elif event.key == pygame.K_BACKSPACE:
                    self._press('=')
                    self._press('=')

    def _operate(self) -> Union[int, float]:
        """
        Operate current and previous values.

        :return: Operation result
        """
        a = 0 if self.curr == '' else float(self.curr)
        b = 0 if self.prev == '' else float(self.prev)
        c = 0
        if self.op == '+':
            c = a + b
        elif self.op == '-':
            c = b - a
        elif self.op == 'x':
            c = a * b
        elif self.op == '/':
            if a != 0:
                c = b / a
            else:
                self.screen.set_title('Error')
        return int(c)

    def _press(self, digit: Union[int, str]) -> None:
        """
        Press calculator digit.

        :param digit: Number or symbol
        :return: None
        """
        if digit in ('+', '-', 'x', '/'):
            if self.curr != '':
                if self.op != '':
                    self.prev = str(self._operate())
                else:
                    self.prev = self.curr
                self.curr = ''
            self.op = digit
            if len(self.prev) <= 8:
                self.screen.set_title(self.prev + self.op)
            else:
                self.screen.set_title('Ans' + self.op)
        elif digit == '=':
            if self.prev == '':
                self.curr = ''
                self.screen.set_title('0')
                return
            c = self._operate()
            self.screen.set_title(str(c))
            if len(str(c)) > 8:
                c = 0
                self.screen.set_title('Overflow')
            self.prev = ''
            self.curr = str(c)
            self.op = ''
        else:
            if self.op == '':
                if len(self.prev) <= 7:
                    self.prev += str(digit)
                    self.prev = self._format(self.prev)
                self.screen.set_title(self.prev)
            else:
                if len(self.curr) <= 7:
                    self.curr += str(digit)
                    self.curr = self._format(self.curr)
                self.screen.set_title(self.curr)

    @staticmethod
    def _format(x: str) -> str:
        """
        Format number.

        :param x: Number
        :return: Str
        """
        try:
            if int(x) == float(x):
                return str(int(x))
        except ValueError:
            pass
        return str(round(int(x), 0))

    def mainloop(self, test: bool) -> None:
        """
        App mainloop.

        :param test: Test status
        """
        self.menu.mainloop(self.surface, disable_loop=test)


def main(test: bool = False) -> 'CalculatorApp':
    """
    Main function.

    :param test: Indicate function is being tested
    :return: App object
    """
    app = CalculatorApp()
    app.mainloop(test)
    return app


if __name__ == '__main__':
    main()
