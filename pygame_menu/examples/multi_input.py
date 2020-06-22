# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).

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

import os
import pygame
import pygame_menu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60.0
WINDOW_SIZE = (640, 480)

sound = None  # type: pygame_menu.sound.Sound
surface = None  # type: pygame.Surface
main_menu = None  # type: pygame_menu.Menu


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def main_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.

    :return: None
    """
    surface.fill((40, 40, 40))


def check_name_test(value):
    """
    This function tests the text input widget.

    :param value: The widget value
    :type value: str
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
    if enabled:
        main_menu.set_sound(sound, recursive=True)
        print('Menu sounds were enabled')
    else:
        main_menu.set_sound(None, recursive=True)
        print('Menu sounds were disabled')


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
    sound = pygame_menu.sound.Sound()

    # Load example sounds
    sound.load_example_sounds()

    # Disable a sound
    sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, None)

    # -------------------------------------------------------------------------
    # Create menus: Settings
    # -------------------------------------------------------------------------
    settings_menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
    settings_menu_theme.title_offset = (5, -2)
    settings_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
    settings_menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
    settings_menu_theme.widget_font_size = 20

    settings_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.85,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        theme=settings_menu_theme,
        title='Settings',
        width=WINDOW_SIZE[0] * 0.9,
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
                                 maxwidth=3,
                                 textinput_id='age',
                                 input_type=pygame_menu.locals.INPUT_INT,
                                 cursor_selection_enable=False)
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
    settings_menu.add_selector('Select difficulty ',
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

    settings_menu.add_button('Store data', data_fun)  # Call function
    settings_menu.add_button('Return to main menu', pygame_menu.events.BACK,
                             align=pygame_menu.locals.ALIGN_CENTER)

    # -------------------------------------------------------------------------
    # Create menus: More settings
    # -------------------------------------------------------------------------
    more_settings_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.85,
        width=WINDOW_SIZE[0] * 0.9,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        title='More Settings',
        theme=settings_menu_theme,
    )

    more_settings_menu.add_image(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU,
                                 scale=(0.25, 0.25),
                                 align=pygame_menu.locals.ALIGN_CENTER)
    more_settings_menu.add_color_input('Color 1 RGB: ', color_type='rgb')
    more_settings_menu.add_color_input('Color 2 RGB: ', color_type='rgb', default=(255, 0, 0), input_separator='-')

    def print_color(color):
        """
        Test onchange/onreturn.

        :param color: Color tuple
        :type color: tuple
        :return: None
        """
        print('Returned color: ', color)

    more_settings_menu.add_color_input('Color in Hex: ', color_type='hex', onreturn=print_color)

    more_settings_menu.add_vertical_margin(25)
    more_settings_menu.add_button('Return to main menu', pygame_menu.events.BACK,
                                  align=pygame_menu.locals.ALIGN_CENTER)

    # -------------------------------------------------------------------------
    # Create menus: Column buttons
    # -------------------------------------------------------------------------
    button_column_menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
    button_column_menu_theme.background_color = pygame_menu.baseimage.BaseImage(
        image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    button_column_menu_theme.widget_font_size = 25

    button_column_menu = pygame_menu.Menu(
        columns=2,
        height=WINDOW_SIZE[1] * 0.45,
        onclose=pygame_menu.events.DISABLE_CLOSE,
        rows=3,
        theme=button_column_menu_theme,
        title='Textures+Columns',
        width=WINDOW_SIZE[0] * 0.9,
    )
    for i in range(4):
        button_column_menu.add_button('Button {0}'.format(i), pygame_menu.events.BACK)
    button_column_menu.add_button(
        'Return to main menu', pygame_menu.events.BACK,
        background_color=pygame_menu.baseimage.BaseImage(
            image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_METAL
        )
    )

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
    main_menu_theme.widget_offset = (0, 0.09)
    main_menu_theme.title_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font_size = 30

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        width=WINDOW_SIZE[0] * 0.8,
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        title='Main menu',
        theme=main_menu_theme,
    )

    main_menu.add_button('Settings', settings_menu)
    main_menu.add_button('More Settings', more_settings_menu)
    main_menu.add_button('Menu in textures and columns', button_column_menu)
    main_menu.add_selector('Menu sounds ',
                           [('Off', False), ('On', True)],
                           onchange=update_menu_sound)
    main_menu.add_button('Quit', pygame_menu.events.EXIT)

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
        main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
