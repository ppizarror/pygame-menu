# coding=utf-8
"""
EXAMPLE
Game menu with 3 difficulty options.

Copyright (C) 2017 Pablo Pizarro @ppizarror

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

# Import pygame and libraries
from pygame.locals import *
from random import randrange
import os
import pygame

# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *

ABOUT = ['PygameMenu {0}'.format(pygameMenu.__version__),
         'Author: {0}'.format(pygameMenu.__author__),
         TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BACKGROUND = (128, 0, 128)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 55, 36)
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

# Global variables
DIFFICULTY = ['EASY']


# -----------------------------------------------------------------------------

def change_difficulty(d):
    """
    Change difficulty of the game.
    
    :return: 
    """
    print ('Selected difficulty: {0}'.format(d))
    DIFFICULTY[0] = d


def random_color():
    """
    Return random color.
    
    :return: Color tuple
    """
    return randrange(0, 255), randrange(0, 255), randrange(0, 255)


def play_function(difficulty, font):
    """
    Main game function
    
    :param difficulty: Difficulty of the game
    :param font: Pygame font
    :return: None
    """
    difficulty = difficulty[0]
    assert isinstance(difficulty, str)

    if difficulty == 'EASY':
        f = font.render('Playing as baby', 1, COLOR_WHITE)
    elif difficulty == 'MEDIUM':
        f = font.render('Playing as normie', 1, COLOR_WHITE)
    elif difficulty == 'HARD':
        f = font.render('Playing as god', 1, COLOR_WHITE)
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
        playevents = pygame.event.get()
        for e in playevents:
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    if main_menu.is_disabled():
                        main_menu.enable()

                        # Quit this function, then skip to loop of main-menu on line 197
                        return

        # Pass events to main_menu
        main_menu.mainloop(playevents)

        # Continue playing
        surface.fill(bg_color)
        surface.blit(f, ((WINDOW_SIZE[0] - f_width) / 2, WINDOW_SIZE[1] / 2))
        pygame.display.flip()


def main_background():
    """
    Function used by menus, draw on background while menu is active.
    
    :return: None
    """
    surface.fill(COLOR_BACKGROUND)


# -----------------------------------------------------------------------------
# PLAY MENU
play_menu = pygameMenu.Menu(surface,
                            window_width=WINDOW_SIZE[0],
                            window_height=WINDOW_SIZE[1],
                            font=pygameMenu.fonts.FONT_BEBAS,
                            title='Play menu',
                            menu_alpha=100,
                            font_size=30,
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            bgfun=main_background,
                            menu_color=MENU_BACKGROUND_COLOR,
                            option_shadow=False,
                            font_color=COLOR_BLACK,
                            color_selected=COLOR_WHITE,
                            onclose=PYGAME_MENU_DISABLE_CLOSE
                            )
# When pressing return -> play(DIFFICULTY[0], font)
play_menu.add_option('Play', play_function, DIFFICULTY,
                     pygame.font.Font(pygameMenu.fonts.FONT_FRANCHISE, 30))
play_menu.add_selector('Select difficulty', [('Easy', 'EASY'),
                                             ('Medium', 'MEDIUM'),
                                             ('Hard', 'HARD')],
                       onreturn=None,
                       onchange=change_difficulty)
play_menu.add_option('Return to main menu', PYGAME_MENU_BACK)

# ABOUT MENU
about_menu = pygameMenu.TextMenu(surface,
                                 window_width=WINDOW_SIZE[0],
                                 window_height=WINDOW_SIZE[1],
                                 font=pygameMenu.fonts.FONT_BEBAS,
                                 font_title=pygameMenu.fonts.FONT_8BIT,
                                 title='About',
                                 # Disable menu close (ESC button)
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,
                                 font_color=COLOR_BLACK,
                                 text_fontsize=20,
                                 font_size_title=30,
                                 menu_color_title=COLOR_WHITE,
                                 menu_color=MENU_BACKGROUND_COLOR,
                                 menu_width=int(WINDOW_SIZE[0] * 0.6),
                                 menu_height=int(WINDOW_SIZE[1] * 0.6),
                                 option_shadow=False,
                                 color_selected=COLOR_WHITE,
                                 text_color=COLOR_BLACK,
                                 bgfun=main_background)
for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(TEXT_NEWLINE)
about_menu.add_option('Return to menu', PYGAME_MENU_BACK)

# MAIN MENU
main_menu = pygameMenu.Menu(surface,
                            window_width=WINDOW_SIZE[0],
                            window_height=WINDOW_SIZE[1],
                            font=pygameMenu.fonts.FONT_BEBAS,
                            title='Main menu',
                            menu_alpha=100,
                            font_size=30,
                            menu_width=int(WINDOW_SIZE[0] * 0.6),
                            menu_height=int(WINDOW_SIZE[1] * 0.6),
                            onclose=PYGAME_MENU_DISABLE_CLOSE,  # ESC disabled
                            bgfun=main_background,
                            menu_color=MENU_BACKGROUND_COLOR,
                            option_shadow=False,
                            font_color=COLOR_BLACK,
                            color_selected=COLOR_WHITE,
                            )
main_menu.add_option('Play', play_menu)
main_menu.add_option('About', about_menu)
main_menu.add_option('Quit', PYGAME_MENU_EXIT)

# -----------------------------------------------------------------------------
# Main loop
while True:

    # Tick
    clock.tick(60)

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            exit()

    # Main menu
    main_menu.mainloop(events)

    # Flip surface
    pygame.display.flip()
