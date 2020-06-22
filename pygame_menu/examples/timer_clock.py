# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - TIMER CLOCK
Example file, timer clock with in-menu options.

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

# Import libraries
import sys

sys.path.insert(0, '../../')

import datetime
import os
import pygame
from random import randrange

import pygame_menu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['pygame-menu {0}'.format(pygame_menu.__version__),
         'Author: @{0}'.format(pygame_menu.__author__),
         '',
         'Email: {0}'.format(pygame_menu.__email__)]
COLOR_BACKGROUND = [128, 0, 128]
FPS = 60
H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
W_SIZE = 800  # Width of window size

surface = None  # type: pygame.Surface
timer = None  # type: list


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def mainmenu_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.

    :return: None
    """
    surface.fill((40, 0, 40))


def reset_timer():
    """
    Reset timer.

    :return: None
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

        :return: None
        """
        print('Update game with new settings')


def change_color_bg(value, c=None, **kwargs):
    """
    Change background color.

    :param value: Selected option (data, index)
    :type value: tuple
    :param c: Color tuple
    :type c: tuple
    :return: None
    """
    color, _ = value
    if c == (-1, -1, -1):  # If random color
        c = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    if kwargs['write_on_console']:
        print('New background color: {0} ({1},{2},{3})'.format(color, *c))
    COLOR_BACKGROUND[0] = c[0]
    COLOR_BACKGROUND[1] = c[1]
    COLOR_BACKGROUND[2] = c[2]


def main(test=False):
    """
    Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Write help message on console
    for m in HELP:
        print(m)

    # Create window
    global surface
    surface = pygame.display.set_mode((W_SIZE, H_SIZE))
    pygame.display.set_caption('Example - Timer Clock')

    # Main timer and game clock
    clock = pygame.time.Clock()
    global timer
    timer = [0.0]
    dt = 1.0 / FPS
    timer_font = pygame_menu.font.get_font(pygame_menu.font.FONT_NEVIS, 100)

    # -------------------------------------------------------------------------
    # Create menus: Timer
    # -------------------------------------------------------------------------

    timer_theme = pygame_menu.themes.THEME_DARK.copy()  # Create a new copy
    timer_theme.background_color = (0, 0, 0, 180)  # Enable transparency

    # Timer
    timer_menu = pygame_menu.Menu(
        theme=timer_theme,
        height=400,
        width=600,
        onclose=pygame_menu.events.RESET,
        title='Timer Menu',
    )

    # Add widgets
    timer_menu.add_button('Reset timer', reset_timer)

    # Adds a selector (element that can handle functions)
    timer_menu.add_selector(title='Change color ',
                            items=[('Random', (-1, -1, -1)),  # Values of selector, call to change_color_bg
                                   ('Default', (128, 0, 128)),
                                   ('Black', (0, 0, 0)),
                                   ('Blue', (12, 12, 200))],
                            default=1,  # Optional parameter that sets default item of selector
                            onchange=change_color_bg,  # Action when changing element with left/right
                            onreturn=change_color_bg,  # Action when pressing return on an element
                            # Optional parameters to change_color_bg function
                            write_on_console=True,
                            )
    timer_menu.add_button('Update game object', TestCallClassMethod().update_game_settings)
    timer_menu.add_button('Return to Menu', pygame_menu.events.BACK)
    timer_menu.add_button('Close Menu', pygame_menu.events.CLOSE)

    # -------------------------------------------------------------------------
    # Create menus: Help
    # -------------------------------------------------------------------------
    help_theme = pygame_menu.themes.Theme(
        background_color=(30, 50, 107, 190),  # 75% opacity
        title_background_color=(120, 45, 30, 190),
        title_font=pygame_menu.font.FONT_FRANCHISE,
        title_font_size=60,
        widget_font=pygame_menu.font.FONT_FRANCHISE,
        widget_font_color=(170, 170, 170),
        widget_font_size=45,
        widget_shadow=False,
        widget_shadow_position=pygame_menu.locals.POSITION_SOUTHEAST,
    )

    help_menu = pygame_menu.Menu(
        height=600,  # Fullscreen
        onclose=pygame_menu.events.DISABLE_CLOSE,  # Pressing ESC button does nothing
        theme=help_theme,
        title='Help',
        width=800,
    )
    for m in HELP:
        help_menu.add_label(m, align=pygame_menu.locals.ALIGN_CENTER)
    help_menu.add_vertical_margin(25)
    help_menu.add_button('Return to Menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_DARK.copy()
    about_theme.widget_font = pygame_menu.font.FONT_NEVIS
    about_theme.title_font = pygame_menu.font.FONT_8BIT
    about_theme.title_offset = (5, -2)
    about_theme.widget_offset = (0, 0.14)

    about_menu = pygame_menu.Menu(
        height=400,
        mouse_visible=False,
        onclose=pygame_menu.events.DISABLE_CLOSE,  # Disable menu close (ESC button)
        theme=about_theme,
        title='About',
        width=600,
    )
    for m in ABOUT:
        about_menu.add_label(m, margin=(0, 0))
    about_menu.add_label('')
    about_menu.add_button('Return to Menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu = pygame_menu.Menu(
        enabled=False,
        height=400,
        theme=pygame_menu.themes.THEME_DARK,
        title='Main Menu',
        width=600,
    )

    main_menu.add_button(timer_menu.get_title(), timer_menu)  # Add timer submenu
    main_menu.add_button(help_menu.get_title(), help_menu)  # Add help submenu
    main_menu.add_button(about_menu.get_title(), about_menu)  # Add about submenu
    main_menu.add_button('Exit', pygame_menu.events.EXIT)  # Add exit function

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick clock
        clock.tick(FPS)
        timer[0] += dt

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu.toggle()

        # Title is evaluated at current level as the title of the base pointer object (main_menu)
        # can change if user opens submenus
        if main_menu.get_current().get_title() != 'Main Menu' or not main_menu.is_enabled():
            # Draw timer
            surface.fill(COLOR_BACKGROUND)
            time_string = str(datetime.timedelta(seconds=int(timer[0])))
            time_blit = timer_font.render(time_string, 1, (255, 255, 255))
            time_blit_size = time_blit.get_size()
            surface.blit(time_blit, (int(W_SIZE / 2 - time_blit_size[0] / 2),
                                     int(H_SIZE / 2 - time_blit_size[1] / 2)))
        else:
            # Background color if the menu is enabled and timer is hidden
            surface.fill((40, 0, 40))

        if main_menu.is_enabled():
            main_menu.draw(surface)

        main_menu.update(events)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
