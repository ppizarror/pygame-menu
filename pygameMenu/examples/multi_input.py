# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).

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
import pygame
import pygameMenu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['pygameMenu {0}'.format(pygameMenu.__version__),
         'Author: @{0}'.format(pygameMenu.__author__),
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
FPS = 60.0
MENU_BACKGROUND_COLOR = (228, 100, 36)
WINDOW_SIZE = (640, 480)

sound = None
surface = None
main_menu = None


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def main_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.

    :return: None
    """
    global surface
    surface.fill((40, 40, 40))


def check_name_test(value):
    """
    This function tests the text input widget.

    :param value: The widget value
    :type value: basestring
    :return: None
    """
    print('User name: {0}'.format(value))


# noinspection PyUnusedLocal
def update_menu_sound(value, enabled):
    """
    Update menu sound.

    :param value: Value of the selector (Label and index)
    :type value: tuple
    :param enabled: Parameter of the selector, (True/False)
    :type enabled: bool
    :return: None
    """
    global main_menu
    global sound
    if enabled:
        main_menu.set_sound(sound, recursive=True)
        print('Menu sound were enabled')
    else:
        main_menu.set_sound(None, recursive=True)
        print('Menu sound were disabled')


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
    global main_menu
    global sound
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Example - Multi Input')
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Set sounds
    # -------------------------------------------------------------------------
    sound = pygameMenu.sound.Sound()

    # Load example sounds
    sound.load_example_sounds()

    # Disable a sound
    sound.set_sound(pygameMenu.sound.SOUND_TYPE_ERROR, None)

    # -------------------------------------------------------------------------
    # Create menus
    # -------------------------------------------------------------------------

    # Settings menu
    settings_menu = pygameMenu.Menu(surface,
                                    bgfun=main_background,
                                    color_selected=COLOR_WHITE,
                                    font=pygameMenu.font.FONT_HELVETICA,
                                    font_color=COLOR_BLACK,
                                    font_size=25,
                                    font_size_title=50,
                                    menu_alpha=100,
                                    menu_color=MENU_BACKGROUND_COLOR,
                                    menu_height=int(WINDOW_SIZE[1] * 0.85),
                                    menu_width=int(WINDOW_SIZE[0] * 0.9),
                                    onclose=pygameMenu.events.DISABLE_CLOSE,
                                    title='Settings',
                                    widget_alignment=pygameMenu.locals.ALIGN_LEFT,
                                    window_height=WINDOW_SIZE[1],
                                    window_width=WINDOW_SIZE[0]
                                    )

    # Add text inputs with different configurations
    wid1 = settings_menu.add_text_input('First name: ',
                                        default='John',
                                        onreturn=check_name_test,
                                        textinput_id='first_name')
    wid2 = settings_menu.add_text_input('Last name: ',
                                        default='Rambo',
                                        maxchar=10,
                                        textinput_id='last_name',
                                        input_underline='.')
    settings_menu.add_text_input('Your age: ',
                                 default=25,
                                 maxchar=3,
                                 textinput_id='age',
                                 input_type=pygameMenu.locals.INPUT_INT,
                                 enable_selection=False)
    settings_menu.add_text_input('Some long text: ',
                                 maxwidth=19,
                                 textinput_id='long_text',
                                 input_underline='_')
    settings_menu.add_text_input('Password: ',
                                 maxchar=6,
                                 password=True,
                                 textinput_id='pass',
                                 input_underline='_')

    # Create selector with 3 difficulty options
    settings_menu.add_selector('Select difficulty',
                               [('Easy', 'EASY'),
                                ('Medium', 'MEDIUM'),
                                ('Hard', 'HARD')],
                               selector_id='difficulty',
                               default=1)

    def data_fun():
        """
        Print data of the menu.

        :return: None
        """
        print('Settings data:')
        data = settings_menu.get_input_data()
        for k in data.keys():
            print(u'\t{0}\t=>\t{1}'.format(k, data[k]))

    settings_menu.add_option('Store data', data_fun)  # Call function
    settings_menu.add_option('Return to main menu', pygameMenu.events.BACK,
                             align=pygameMenu.locals.ALIGN_CENTER)

    # Main menu
    main_menu = pygameMenu.Menu(surface,
                                bgfun=main_background,
                                color_selected=COLOR_WHITE,
                                font=pygameMenu.font.FONT_COMIC_NEUE,
                                font_color=COLOR_BLACK,
                                font_size=30,
                                font_size_title=40,
                                menu_alpha=100,
                                menu_color=MENU_BACKGROUND_COLOR,
                                menu_height=int(WINDOW_SIZE[1] * 0.7),
                                menu_width=int(WINDOW_SIZE[0] * 0.8),
                                # User press ESC button
                                onclose=pygameMenu.events.EXIT,
                                option_shadow=False,
                                title='Main menu',
                                window_height=WINDOW_SIZE[1],
                                window_width=WINDOW_SIZE[0]
                                )
    main_menu.set_fps(FPS)

    main_menu.add_option('Settings', settings_menu)
    main_menu.add_selector('Menu sounds',
                           [('Off', False), ('On', True)],
                           onchange=update_menu_sound)
    main_menu.add_option('Quit', pygameMenu.events.EXIT)

    assert main_menu.get_widget('first_name', recursive=True) is wid1
    assert main_menu.get_widget('last_name', recursive=True) is wid2
    assert main_menu.get_widget('last_name') is None

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        main_background()

        # Main menu
        main_menu.mainloop(disable_loop=test)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
