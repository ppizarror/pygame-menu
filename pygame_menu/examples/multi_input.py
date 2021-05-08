"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MULTI-INPUT
Shows different inputs (widgets).

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

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

__all__ = ['main']

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Tuple, Optional

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60
WINDOW_SIZE = (640, 480)

sound: Optional['pygame_menu.sound.Sound'] = None
surface: Optional['pygame.Surface'] = None
main_menu: Optional['pygame_menu.Menu'] = None


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def main_background() -> None:
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.

    :return: None
    """
    surface.fill((40, 40, 40))


def check_name_test(value: str) -> None:
    """
    This function tests the text input widget.

    :param value: The widget value
    :return: None
    """
    print('User name: {0}'.format(value))


def update_menu_sound(value: Tuple, enabled: bool) -> None:
    """
    Update menu sound.

    :param value: Value of the selector (Label and index)
    :param enabled: Parameter of the selector, (True/False)
    :return: None
    """
    assert isinstance(value, tuple)
    if enabled:
        main_menu.set_sound(sound, recursive=True)
        print('Menu sounds were enabled')
    else:
        main_menu.set_sound(None, recursive=True)
        print('Menu sounds were disabled')


def main(test: bool = False) -> None:
    """
    Main program.

    :param test: Indicate function is being tested
    :return: None
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface

    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = create_example_window('Example - Multi Input', WINDOW_SIZE)
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
        theme=settings_menu_theme,
        title='Settings',
        width=WINDOW_SIZE[0] * 0.9
    )

    # Add text inputs with different configurations
    settings_menu.add.text_input(
        'First name: ',
        default='John',
        onreturn=check_name_test,
        textinput_id='first_name'
    )
    settings_menu.add.text_input(
        'Last name: ',
        default='Rambo',
        maxchar=10,
        textinput_id='last_name',
        input_underline='.'
    )
    settings_menu.add.text_input(
        'Your age: ',
        default=25,
        maxchar=3,
        maxwidth=3,
        textinput_id='age',
        input_type=pygame_menu.locals.INPUT_INT,
        cursor_selection_enable=False
    )
    settings_menu.add.text_input(
        'Some long text: ',
        maxwidth=19,
        textinput_id='long_text',
        input_underline='_'
    )
    settings_menu.add.text_input(
        'Password: ',
        maxchar=6,
        password=True,
        textinput_id='pass',
        input_underline='_'
    )

    # Selectable items
    items = [('Easy', 'EASY'),
             ('Medium', 'MEDIUM'),
             ('Hard', 'HARD')]

    # Create selector with 3 difficulty options
    settings_menu.add.selector(
        'Select difficulty:\t',
        items,
        selector_id='difficulty',
        default=1
    )
    settings_menu.add.selector(
        'Select difficulty fancy',
        items,
        selector_id='difficulty_fancy',
        default=1,
        style='fancy'
    )
    settings_menu.add.dropselect(
        'Select difficulty (drop)',
        items,
        default=1,
        dropselect_id='difficulty_drop'
    )
    settings_menu.add.dropselect_multiple(
        title='Pick 3 colors',
        items=[('Black', (0, 0, 0)),
               ('Blue', (0, 0, 255)),
               ('Cyan', (0, 255, 255)),
               ('Fuchsia', (255, 0, 255)),
               ('Green', (0, 255, 0)),
               ('Red', (255, 0, 0)),
               ('White', (255, 255, 255)),
               ('Yellow', (255, 255, 0))],
        dropselect_multiple_id='pickcolors',
        max_selected=3,
        open_middle=True,
        selection_box_height=6  # How many options show if opened
    )

    # Create switch
    settings_menu.add.toggle_switch('First Switch', False,
                                    toggleswitch_id='first_switch')
    settings_menu.add.toggle_switch('Other Switch', True,
                                    toggleswitch_id='second_switch',
                                    state_text=('Apagado', 'Encencido'))

    def data_fun() -> None:
        """
        Print data of the menu.

        :return: None
        """
        print('Settings data:')
        data = settings_menu.get_input_data()
        for k in data.keys():
            print(u'\t{0}\t=>\t{1}'.format(k, data[k]))

    settings_menu.add.clock(clock_format='%Y/%m/%d %H:%M', title_format='Clock: {0}')
    settings_menu.add.button('Store data', data_fun)  # Call function
    settings_menu.add.button('Restore original values', settings_menu.reset_value)
    settings_menu.add.button('Return to main menu', pygame_menu.events.BACK,
                             align=pygame_menu.locals.ALIGN_CENTER)

    # -------------------------------------------------------------------------
    # Create menus: More settings
    # -------------------------------------------------------------------------
    more_settings_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.85,
        theme=settings_menu_theme,
        title='More Settings',
        width=WINDOW_SIZE[0] * 0.9
    )

    more_settings_menu.add.image(
        pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU,
        scale=(0.25, 0.25),
        align=pygame_menu.locals.ALIGN_CENTER
    )
    more_settings_menu.add.color_input(
        'Color 1 RGB: ',
        color_type='rgb'
    )
    more_settings_menu.add.color_input(
        'Color 2 RGB: ',
        color_type='rgb',
        default=(255, 0, 0),
        input_separator='-'
    )

    def print_color(color: Tuple) -> None:
        """
        Test onchange/onreturn.

        :param color: Color tuple
        :return: None
        """
        print('Returned color: ', color)

    more_settings_menu.add.color_input(
        'Color in Hex: ',
        color_type='hex',
        hex_format='lower',
        onreturn=print_color
    )

    more_settings_menu.add.vertical_margin(25)
    more_settings_menu.add.button(
        'Return to main menu',
        pygame_menu.events.BACK,
        align=pygame_menu.locals.ALIGN_CENTER
    )

    # -------------------------------------------------------------------------
    # Create menus: Column buttons
    # -------------------------------------------------------------------------
    button_column_menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
    button_column_menu_theme.background_color = pygame_menu.BaseImage(
        image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
    )
    button_column_menu_theme.widget_font_size = 25

    button_column_menu = pygame_menu.Menu(
        columns=2,
        height=WINDOW_SIZE[1] * 0.45,
        rows=3,
        theme=button_column_menu_theme,
        title='Textures+Columns',
        width=WINDOW_SIZE[0] * 0.9
    )
    for i in range(4):
        button_column_menu.add.button('Button {0}'.format(i), pygame_menu.events.BACK)
    button_column_menu.add.button(
        'Return to main menu', pygame_menu.events.BACK,
        background_color=pygame_menu.BaseImage(
            image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_METAL
        )
    ).background_inflate_to_selection_effect()

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
    main_menu_theme.title_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
    main_menu_theme.widget_font_size = 30

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        theme=main_menu_theme,
        title='Main menu',
        width=WINDOW_SIZE[0] * 0.8
    )

    main_menu.add.button('Settings', settings_menu)
    main_menu.add.button('More Settings', more_settings_menu)
    main_menu.add.button('Menu in textures and columns', button_column_menu)
    main_menu.add.selector('Menu sounds ',
                           [('Off', False), ('On', True)],
                           onchange=update_menu_sound)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

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
