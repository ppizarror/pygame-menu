# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - TIMER CLOCK
Example file, timer clock with in-menu options.

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

from random import randrange
import datetime
import os
import pygame
import pygameMenu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['pygameMenu {0}'.format(pygameMenu.__version__),
         'Author: @{0}'.format(pygameMenu.__author__),
         pygameMenu.locals.TEXT_NEWLINE,
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

surface = None
timer = None


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def mainmenu_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    global surface
    surface.fill((40, 0, 40))


def reset_timer():
    """
    Reset timer.
    """
    global timer
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


def change_color_bg(value, c=None, **kwargs):
    """
    Change background color.

    :param value: Selected option (data, index)
    :type value: tuple
    :param c: Color tuple
    :type c: tuple
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
    timer_font = pygameMenu.font.get_font(pygameMenu.font.FONT_NEVIS, 100)

    # -------------------------------------------------------------------------
    # Create menus
    # -------------------------------------------------------------------------

    # Timer
    timer_menu = pygameMenu.Menu(surface,
                                 dopause=False,
                                 font=pygameMenu.font.FONT_NEVIS,
                                 menu_alpha=85,
                                 menu_color=(0, 0, 0),  # Background color
                                 menu_color_title=(0, 0, 0),
                                 menu_height=int(H_SIZE * 0.65),
                                 menu_width=600,
                                 onclose=pygameMenu.events.RESET,  # If this menu closes (ESC) back to main
                                 option_shadow=True,
                                 rect_width=4,
                                 title='Timer Menu',
                                 title_offsety=5,  # Adds 5px to title vertical position
                                 window_height=H_SIZE,
                                 window_width=W_SIZE
                                 )

    # Add options
    timer_menu.add_option('Reset timer', reset_timer)

    # Adds a selector (element that can handle functions)
    timer_menu.add_selector('Change bgcolor',
                            # Values of selector, call to change_color_bg
                            [('Random', (-1, -1, -1)),
                             ('Default', (128, 0, 128)),
                             ('Black', (0, 0, 0)),
                             ('Blue', COLOR_BLUE)],
                            # Optional parameter that sets default item of selector
                            default=1,
                            # Action when changing element with left/right
                            onchange=change_color_bg,
                            # Action when pressing return on an element
                            onreturn=change_color_bg,
                            # Optional parameters to change_color_bg function
                            write_on_console=True
                            )
    timer_menu.add_option('Update game object', TestCallClassMethod().update_game_settings)
    timer_menu.add_option('Return to Menu', pygameMenu.events.BACK)
    timer_menu.add_option('Close Menu', pygameMenu.events.CLOSE)

    # Help menu
    help_menu = pygameMenu.TextMenu(surface,
                                    dopause=False,
                                    font=pygameMenu.font.FONT_FRANCHISE,
                                    menu_color=(30, 50, 107),  # Background color
                                    menu_color_title=(120, 45, 30),
                                    # Pressing ESC button does nothing
                                    onclose=pygameMenu.events.DISABLE_CLOSE,
                                    option_shadow=True,
                                    option_shadow_position=pygameMenu.locals.POSITION_SOUTHEAST,
                                    text_align=pygameMenu.locals.ALIGN_CENTER,
                                    title='Help',
                                    window_height=H_SIZE,
                                    window_width=W_SIZE
                                    )
    help_menu.add_option('Return to Menu', pygameMenu.events.BACK)
    for m in HELP:
        help_menu.add_line(m)

    # About menu
    about_menu = pygameMenu.TextMenu(surface,
                                     dopause=False,
                                     draw_text_region_x=5,  # 5% margin
                                     font=pygameMenu.font.FONT_NEVIS,
                                     font_size_title=30,
                                     font_title=pygameMenu.font.FONT_8BIT,
                                     menu_color_title=COLOR_BLUE,
                                     mouse_visible=False,
                                     # Disable menu close (ESC button)
                                     onclose=pygameMenu.events.DISABLE_CLOSE,
                                     option_shadow=True,
                                     text_fontsize=20,
                                     title='About',
                                     window_height=H_SIZE,
                                     window_width=W_SIZE
                                     )
    about_menu.add_option('Return to Menu', pygameMenu.events.BACK)
    for m in ABOUT:
        about_menu.add_line(m)
    about_menu.add_line(pygameMenu.locals.TEXT_NEWLINE)

    # Main menu, pauses execution of the application
    main_menu = pygameMenu.Menu(surface,
                                bgfun=mainmenu_background,
                                enabled=False,
                                font=pygameMenu.font.FONT_NEVIS,
                                menu_alpha=90,
                                fps=FPS,
                                onclose=pygameMenu.events.CLOSE,
                                title='Main Menu',
                                title_offsety=5,
                                window_height=H_SIZE,
                                window_width=W_SIZE
                                )

    main_menu.add_option(timer_menu.get_title(), timer_menu)  # Add timer submenu
    main_menu.add_option(help_menu.get_title(), help_menu)  # Add help submenu
    main_menu.add_option(about_menu.get_title(), about_menu)  # Add about submenu
    main_menu.add_option('Exit', pygameMenu.events.EXIT)  # Add exit function

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick clock
        clock.tick(FPS)
        timer[0] += dt

        # Paint background
        surface.fill(COLOR_BACKGROUND)

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main_menu.enable()

        # Draw timer
        time_string = str(datetime.timedelta(seconds=int(timer[0])))
        time_blit = timer_font.render(time_string, 1, COLOR_WHITE)
        time_blit_size = time_blit.get_size()
        surface.blit(time_blit, (
            W_SIZE / 2 - time_blit_size[0] / 2, H_SIZE / 2 - time_blit_size[1] / 2))

        # Execute main from principal menu if is enabled
        main_menu.mainloop(events, disable_loop=test)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
