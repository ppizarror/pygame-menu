# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - LONG SCROLLING MENU
Shows scrolling in menu.

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

import os
import pygame
import pygameMenu
from functools import partial

H_SIZE = 600  # Height of window size
W_SIZE = 800  # Width of window size
COLOR_BACKGROUND = (128, 0, 128)


def on_button_click(button_id):
    print("Hello from button {}".format(button_id))


def paint_background(surface):
    surface.fill(COLOR_BACKGROUND)


def make_long_menu(surface):
    # Main menu, pauses execution of the application
    menu = pygameMenu.Menu(surface,
                           bgfun=partial(paint_background, surface),
                           enabled=False,
                           font=pygameMenu.font.FONT_NEVIS,
                           menu_alpha=90,
                           onclose=pygameMenu.events.CLOSE,
                           title='Main Menu',
                           window_height=H_SIZE,
                           window_width=W_SIZE
                           )
    label = "Button n°{}"
    for i in range(1, 10):
        txt = label.format(i)
        menu.add_button(txt, on_button_click, i)
    menu.add_button('Exit', pygameMenu.events.EXIT)
    return menu


def main(test=False):
    """
    Main function
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    # Create window
    screen = pygame.display.set_mode((W_SIZE, H_SIZE))
    pygame.display.set_caption('Example - Scrolling Menu')

    # Create menu
    menu = make_long_menu(screen)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:
        # Paint background
        paint_background(screen)

        # Execute main from principal menu if is enabled
        menu.mainloop(disable_loop=test)

        # Flip surface
        pygame.display.update()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
