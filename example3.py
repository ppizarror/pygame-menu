# coding=utf-8
"""
EXAMPLE 3
Game menu with a input text

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

# Import pygame and libraries
import os
import pygame

# Import pygameMenu
import pygameMenu
from pygameMenu import locals as pgm_loc

ABOUT = ['PygameMenu {0}'.format(pygameMenu.__version__),
         'Author: {0}'.format(pygameMenu.__author__),
         pgm_loc.PYGAMEMENU_TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 100, 36)
WINDOW_SIZE = (640, 480)

# -----------------------------------------------------------------------------
# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Create pygame screen and objects
surface = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('PygameMenu example 2')
clock = pygame.time.Clock()
dt = 1 / FPS


def main_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    surface.fill((40, 40, 40))


# -----------------------------------------------------------------------------
# PLAY MENU
settings_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.fonts.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.6),
                                menu_width=int(WINDOW_SIZE[0] * 0.6),
                                onclose=pgm_loc.PYGAME_MENU_DISABLE_CLOSE,
                                option_shadow=False,
                                title='Play menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

settings_menu.add_selector('Select difficulty', [('Easy', 'EASY'),
                                                 ('Medium', 'MEDIUM'),
                                                 ('Hard', 'HARD')])
settings_menu.add_textinput("Firstname: ")
settings_menu.add_textinput("Lastname: ")
settings_menu.add_option('Return to main menu', pgm_loc.PYGAME_MENU_BACK)

# MAIN MENU
main_menu = pygameMenu.Menu(surface,
                            bgfun=main_background,
                            color_selected=COLOR_WHITE,
                            font=pygameMenu.fonts.FONT_BEBAS,
                            font_color=COLOR_BLACK,
                            font_size=30,
                            menu_alpha=100,
                            menu_color=MENU_BACKGROUND_COLOR,
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            onclose=pgm_loc.PYGAME_MENU_DISABLE_CLOSE,
                            option_shadow=False,
                            title='Main menu',
                            window_height=WINDOW_SIZE[1],
                            window_width=WINDOW_SIZE[0]
                            )

main_menu.add_option('Settings', settings_menu)
main_menu.add_option('Quit', pgm_loc.PYGAME_MENU_EXIT)

# -----------------------------------------------------------------------------
# Main loop
while True:

    # Tick
    clock.tick(60)

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    # Main menu
    main_menu.mainloop(events)

    # Flip surface
    pygame.display.flip()
