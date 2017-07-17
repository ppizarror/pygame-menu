# coding=utf-8
"""
EXAMPLE
Example file, timer clock with in-menu options.

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
from random import randrange
import datetime
import os
import pygame
from pygame.locals import *

# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *

# Constants and global variables
ABOUT = ['PygameMenu {0}'.format(pygameMenu.__version__),
         'Author: {0}'.format(pygameMenu.__author__),
         TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
FPS = 60
H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
W_SIZE = 800  # Width of window size

# Init pygame
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Write help message on console
for m in HELP:
    print(m)

# Create window
surface = pygame.display.set_mode((W_SIZE, H_SIZE))
pygame.display.set_caption('PygameMenu example')

# Main timer and game clock
clock = pygame.time.Clock()
timer = [0.0]
dt = 1.0 / FPS
timer_font = pygame.font.Font(pygameMenu.fonts.FONT_NEVIS, 100)


# Functions
def mainmenu_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    surface.fill((40, 0, 40))


def reset_timer():
    """
    Reset timer
    """
    timer[0] = 0


def change_color_bg(c, **kwargs):
    """
    Change background color
    
    :param c: Color tuple
    """
    if c == (-1, -1, -1):  # If random color
        c = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    if kwargs['write_on_console']:
        print('New background color: ({0},{1},{2})'.format(*c))
    COLOR_BACKGROUND[0] = c[0]
    COLOR_BACKGROUND[1] = c[1]
    COLOR_BACKGROUND[2] = c[2]


# Timer menu
timer_menu = pygameMenu.Menu(surface,
                             window_width=W_SIZE,
                             window_height=H_SIZE,
                             font=pygameMenu.fonts.FONT_NEVIS,
                             title='Timer Menu',
                             # Adds 5px to title vertical position
                             title_offsety=5,
                             menu_alpha=85,
                             menu_width=600,
                             menu_height=int(H_SIZE / 2),
                             # If this menu closes (press ESC) back to main
                             onclose=PYGAME_MENU_RESET,
                             dopause=False)
timer_menu.add_option('Reset timer', reset_timer)

# Adds a selector (element that can handle functions)
timer_menu.add_selector('Change bgcolor',
                        # Values of selector, call to change_color_bg
                        [('Random', (-1, -1, -1)),  # Random color
                         ('Default', (128, 0, 128)),
                         ('Black', (0, 0, 0)),
                         ('Blue', COLOR_BLUE)],
                        # Action when changing element with left/right
                        onchange=None,
                        # Action when pressing return on a element
                        onreturn=change_color_bg,
                        # Kwargs, optional parametrs to change_color_bg function
                        write_on_console=True)
timer_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
timer_menu.add_option('Close Menu', PYGAME_MENU_CLOSE)

# Help menu
help_menu = pygameMenu.TextMenu(surface,
                                window_width=W_SIZE,
                                window_height=H_SIZE,
                                font=pygameMenu.fonts.FONT_FRANCHISE,
                                title='Help',
                                # Pressing ESC button does nothing on this menu
                                onclose=PYGAME_MENU_DISABLE_CLOSE,
                                menu_color_title=(120, 45, 30),
                                # Background color
                                menu_color=(30, 50, 107),
                                dopause=False)
help_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
for m in HELP:
    help_menu.add_line(m)

# About menu
about_menu = pygameMenu.TextMenu(surface,
                                 window_width=W_SIZE,
                                 window_height=H_SIZE,
                                 font=pygameMenu.fonts.FONT_NEVIS,
                                 font_title=pygameMenu.fonts.FONT_8BIT,
                                 title='About',
                                 # Disable menu close (ESC button)
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,
                                 text_fontsize=20,
                                 font_size_title=30,
                                 menu_color_title=COLOR_BLUE,
                                 dopause=False)
about_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(TEXT_NEWLINE)

# Main menu, pauses execution of the application
menu = pygameMenu.Menu(surface,
                       window_width=W_SIZE,
                       window_height=H_SIZE,
                       font=pygameMenu.fonts.FONT_NEVIS,
                       title='Main Menu',
                       title_offsety=5,
                       menu_alpha=90,
                       enabled=False,
                       bgfun=mainmenu_background,
                       onclose=PYGAME_MENU_CLOSE)
menu.add_option(timer_menu.get_title(), timer_menu)  # Add timer submenu
menu.add_option(help_menu.get_title(), help_menu)  # Add help submenu
menu.add_option(about_menu.get_title(), about_menu)  # Add about submenu
menu.add_option('Exit', PYGAME_MENU_EXIT)  # Add exit function

# Main loop
while True:

    # Tick
    clock.tick(60)
    timer[0] += dt

    # Paint background
    surface.fill(COLOR_BACKGROUND)

    # Application events
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if menu.is_disabled():
                    menu.enable()

    # Draw timer
    time_string = str(datetime.timedelta(seconds=int(timer[0])))
    time_blit = timer_font.render(time_string, 1, COLOR_WHITE)
    time_blit_size = time_blit.get_size()
    surface.blit(time_blit, (
        W_SIZE / 2 - time_blit_size[0] / 2, H_SIZE / 2 - time_blit_size[1] / 2))

    # Execute main from principal menu if is enabled
    menu.mainloop(events)

    # Flip surface
    pygame.display.flip()
