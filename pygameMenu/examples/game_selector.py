# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - GAME SELECTOR
Game with 3 difficulty options.

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

# Import libraries
import sys

sys.path.insert(0, '../../')

import os
from random import randrange
import pygame
import pygameMenu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['pygameMenu {0}'.format(pygameMenu.__version__),
         'Author: @{0}'.format(pygameMenu.__author__),
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BACKGROUND = (128, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
DIFFICULTY = ['EASY']
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
WINDOW_SIZE = (640, 480)

clock = None
main_menu = None
surface = None


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def change_difficulty(value, difficulty):
    """
    Change difficulty of the game.

    :param value: Tuple containing the data of the selected object
    :type value: tuple
    :param difficulty: Optional parameter passed as argument to add_selector
    :type difficulty: basestring
    :return: None
    """
    selected, index = value
    print('Selected difficulty: "{0}" ({1}) at index {2}'.format(selected, difficulty, index))
    DIFFICULTY[0] = difficulty


def random_color():
    """
    Return random color.

    :return: Color tuple
    :rtype: tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def play_function(difficulty, font, test=False):
    """
    Main game function.

    :param difficulty: Difficulty of the game
    :type difficulty: basestring
    :param font: Pygame font
    :type font: pygame.font.FontType
    :param test: Test method, if true only one loop is allowed
    :type test: bool
    :return: None
    """
    assert isinstance(difficulty, (tuple, list))
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)

    # Define globals
    global main_menu
    global clock

    if difficulty == 'EASY':
        f = font.render('Playing as a baby (easy)', 1, COLOR_WHITE)
    elif difficulty == 'MEDIUM':
        f = font.render('Playing as a kid (medium)', 1, COLOR_WHITE)
    elif difficulty == 'HARD':
        f = font.render('Playing as a champion (hard)', 1, COLOR_WHITE)
    else:
        raise Exception('Unknown difficulty {0}'.format(difficulty))

    # Draw random color and text
    bg_color = random_color()
    f_width = f.get_size()[0]

    # Reset main menu and disable
    # You also can set another menu, like a 'pause menu', or just use the same
    # main_menu as the menu that will check all your input.
    main_menu.disable()
    main_menu.reset(1)

    while True:

        # Clock tick
        clock.tick(60)

        # Application events
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE and main_menu.is_disabled():
                    main_menu.enable()

                    # Quit this function, then skip to loop of main-menu on line 317
                    return

        # Pass events to main_menu
        main_menu.mainloop(events)

        # Continue playing
        surface.fill(bg_color)
        surface.blit(f, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 2))
        pygame.display.flip()

        # If test returns
        if test:
            break


def main_background():
    """
    Function used by menus, draw on background while menu is active.

    :return: None
    """
    global surface
    surface.fill(COLOR_BACKGROUND)


def main(test=False):
    """
    Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global clock
    global main_menu
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Example - Game Selector')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus
    # -------------------------------------------------------------------------

    # Play menu
    play_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.7),
                                menu_width=int(WINDOW_SIZE[0] * 0.7),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Play menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

    play_submenu = pygameMenu.Menu(surface,
                                   bgfun=main_background,
                                   color_selected=COLOR_WHITE,
                                   font=pygameMenu.font.FONT_BEBAS,
                                   font_color=COLOR_BLACK,
                                   font_size=30,
                                   menu_alpha=100,
                                   menu_color=MENU_BACKGROUND_COLOR,
                                   menu_height=int(WINDOW_SIZE[1] * 0.5),
                                   menu_width=int(WINDOW_SIZE[0] * 0.7),
                                   option_shadow=False,
                                   title='Submenu',
                                   window_height=WINDOW_SIZE[1],
                                   window_width=WINDOW_SIZE[0]
                                   )
    play_submenu.add_option('Back', pygameMenu.events.BACK)

    play_menu.add_option('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                         play_function,
                         DIFFICULTY,
                         pygame.font.Font(pygameMenu.font.FONT_FRANCHISE, 30))
    play_menu.add_selector('Select difficulty',
                           [('1 - Easy', 'EASY'),
                            ('2 - Medium', 'MEDIUM'),
                            ('3 - Hard', 'HARD')],
                           onchange=change_difficulty,
                           selector_id='select_difficulty')
    play_menu.add_option('Another menu', play_submenu)
    play_menu.add_option('Return to main menu', pygameMenu.events.BACK)

    # About menu
    about_menu = pygameMenu.TextMenu(surface,
                                     bgfun=main_background,
                                     color_selected=COLOR_WHITE,
                                     font=pygameMenu.font.FONT_BEBAS,
                                     font_color=COLOR_BLACK,
                                     font_size_title=30,
                                     font_title=pygameMenu.font.FONT_8BIT,
                                     menu_color=MENU_BACKGROUND_COLOR,
                                     menu_color_title=COLOR_WHITE,
                                     menu_height=int(WINDOW_SIZE[1] * 0.6),
                                     menu_width=int(WINDOW_SIZE[0] * 0.6),
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=False,
                                     text_color=COLOR_BLACK,
                                     text_fontsize=20,
                                     title='About',
                                     window_height=WINDOW_SIZE[1],
                                     window_width=WINDOW_SIZE[0]
                                     )
    for m in ABOUT:
        about_menu.add_line(m)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)
    about_menu.add_option('Return to menu', pygameMenu.events.BACK)

    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_BEBAS,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.6),
                                menu_width=int(WINDOW_SIZE[0] * 0.6),
                                onclose=pygameMenu.events.DISABLE_CLOSE,
                                option_shadow=False,
                                title='Main menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )

    main_menu.add_option('Play', play_menu)
    main_menu.add_option('About', about_menu)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    # Configure main menu
    main_menu.set_fps(FPS)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Main menu
        main_menu.mainloop(events, disable_loop=test)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
