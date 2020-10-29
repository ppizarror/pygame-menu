# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - DYNAMIC BUTTON
Menu with dynamic buttons.

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
import sys

sys.path.insert(0, '../../')
import pygame_menu
from random import randrange
import pygame
import os

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
surface = pygame.display.set_mode((600, 400))

menu = pygame_menu.Menu(height=300,
                        width=400,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Welcome')


def add_dynamic_button():
    """
    Append a button to the menu on demand.

    :return: None
    """
    print('Adding a button dynamically')
    btn = menu.add_button(randrange(0, 10), None)

    def _update_button():
        count = btn.get_attribute('count', int(btn.get_title())) + 1
        btn.set_title(count)
        btn.set_attribute('count', count)

    btn.update_callback(_update_button)


menu.add_text_input('Name: ', default='John Doe')
menu.add_button('Play', add_dynamic_button)
menu.add_button('Quit', pygame_menu.events.EXIT)


def main(test=False):
    """
    Main function.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """
    menu.mainloop(surface, disable_loop=test)


if __name__ == '__main__':
    main()
