# coding=utf-8
"""
EXAMPLE 1
Example file, timer clock with in-menu options.

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
from random import randrange
import datetime
import os
import pygame
from pygame.locals import *

# Import pygameMenu
import pygameMenu
from pygameMenu.locals import *

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['pygameMenu {0}'.format(pygameMenu.__version__),
         'Author: {0}'.format(pygameMenu.__author__),
         PYGAMEMENU_TEXT_NEWLINE,
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

# -----------------------------------------------------------------------------
# Init pygame
# -----------------------------------------------------------------------------
pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Write help message on console
for m in HELP:
    print(m)

# Create window
surface = pygame.display.set_mode((W_SIZE, H_SIZE))
pygame.display.set_caption('pygameMenu example')

# Main timer and game clock
clock = pygame.time.Clock()
timer = [0.0]
dt = 1.0 / FPS
timer_font = pygame.font.Font(pygameMenu.fonts.FONT_NEVIS, 100)


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def mainmenu_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    surface.fill((40, 0, 40))


def reset_timer():
    """
    Reset timer.
    """
    timer[0] = 0


class TestCallClassMethod(object):
    """
    Class call method.
    """

    @staticmethod
    def update_game_settings():
        """
        Class method.
        """
        print('Update game with new settings')


def change_color_bg(text, c=None, **kwargs):
    """
    Change background color.

    :param text: Name of the color in the selector
    :param c: Color tuple
    """
    if c == (-1, -1, -1):  # If random color
        c = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    if kwargs['write_on_console']:
        print('New background color: {0} ({1},{2},{3})'.format(text, *c))
    COLOR_BACKGROUND[0] = c[0]
    COLOR_BACKGROUND[1] = c[1]
    COLOR_BACKGROUND[2] = c[2]


# -----------------------------------------------------------------------------
# Create menus
# -----------------------------------------------------------------------------

# Timer
timer_menu = pygameMenu.Menu(surface,
                             dopause=False,
                             font=pygameMenu.fonts.FONT_NEVIS,
                             menu_alpha=85,
                             menu_color=(0, 0, 0),  # Background color
                             menu_color_title=(0, 0, 0),
                             menu_height=int(H_SIZE * 0.65),
                             menu_width=600,
                             onclose=PYGAME_MENU_RESET,  # If this menu closes (press ESC) back to main
                             rect_width=4,
                             title='Timer Menu',
                             title_offsety=5,  # Adds 5px to title vertical position
                             window_height=H_SIZE,
                             window_width=W_SIZE
                             )
timer_menu.add_option('Reset timer', reset_timer)

# Adds a selector (element that can handle functions)
timer_menu.add_selector('Change bgcolor',
                        # Values of selector, call to change_color_bg
                        [('Random', (-1, -1, -1)),
                         ('Default', (128, 0, 128)),
                         ('Black', (0, 0, 0)),
                         ('Blue', COLOR_BLUE)],
                        default=1,  # Optional parameter that sets default item of selector
                        onchange=change_color_bg,  # Action when changing element with left/right
                        onreturn=change_color_bg,  # Action when pressing return on a element
                        write_on_console=True  # Optional parameters to change_color_bg function
                        )
timer_menu.add_option('Update game object', TestCallClassMethod().update_game_settings)
timer_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
timer_menu.add_option('Close Menu', PYGAME_MENU_CLOSE)

# Help menu
help_menu = pygameMenu.TextMenu(surface,
                                dopause=False,
                                font=pygameMenu.fonts.FONT_FRANCHISE,
                                menu_color=(30, 50, 107),  # Background color
                                menu_color_title=(120, 45, 30),
                                onclose=PYGAME_MENU_DISABLE_CLOSE,  # Pressing ESC button does nothing
                                title='Help',
                                window_height=H_SIZE,
                                window_width=W_SIZE
                                )
help_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
for m in HELP:
    help_menu.add_line(m)

# About menu
about_menu = pygameMenu.TextMenu(surface,
                                 dopause=False,
                                 draw_text_region_x=50,
                                 font=pygameMenu.fonts.FONT_NEVIS,
                                 font_size_title=30,
                                 font_title=pygameMenu.fonts.FONT_8BIT,
                                 menu_color_title=COLOR_BLUE,
                                 onclose=PYGAME_MENU_DISABLE_CLOSE,  # Disable menu close (ESC button)
                                 text_centered=True,
                                 text_fontsize=20,
                                 title='About',
                                 window_height=H_SIZE,
                                 window_width=W_SIZE
                                 )
about_menu.add_option('Return to Menu', PYGAME_MENU_BACK)
for m in ABOUT:
    about_menu.add_line(m)
about_menu.add_line(PYGAMEMENU_TEXT_NEWLINE)

# Main menu, pauses execution of the application
menu = pygameMenu.Menu(surface,
                       bgfun=mainmenu_background,
                       enabled=False,
                       font=pygameMenu.fonts.FONT_NEVIS,
                       menu_alpha=90,
                       menu_centered=True,
                       onclose=PYGAME_MENU_CLOSE,
                       title='Main Menu',
                       title_offsety=5,
                       window_height=H_SIZE,
                       window_width=W_SIZE
                       )
menu.add_option(timer_menu.get_title(), timer_menu)  # Add timer submenu
menu.add_option(help_menu.get_title(), help_menu)  # Add help submenu
menu.add_option(about_menu.get_title(), about_menu)  # Add about submenu
menu.add_option('Exit', PYGAME_MENU_EXIT)  # Add exit function

# -----------------------------------------------------------------------------
# Main loop
# -----------------------------------------------------------------------------
while True:

    # Tick clock
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
