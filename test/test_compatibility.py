"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST COMPATIBILITY
Test compatibility for pygame-menu v3.

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

__all__ = ['CompatibilityTest']

from test._utils import MenuUtils, surface
import unittest

import pygame_menu


class CompatibilityTest(unittest.TestCase):

    def test_themes(self) -> None:
        """
        Test themes deprecation.
        """
        theme = pygame_menu.themes.Theme(menubar_close_button=False)
        self.assertFalse(theme.title_close_button)

    @staticmethod
    def test_general_use() -> None:
        """
        Test multi input example from v3.
        """

        # noinspection PyMissingTypeHints
        def main_background() -> None:
            """
            Background function.
            """
            surface.fill((40, 40, 40))

        def check_name_test(value) -> None:
            """
            Name test.
            """
            print('User name: {0}'.format(value))

        # noinspection PyUnusedLocal
        def update_menu_sound(value, enabled) -> None:
            """
            Update menu sound.
            """
            if enabled:
                main_menu.set_sound(sound, recursive=True)
                print('Menu sounds were enabled')
            else:
                main_menu.set_sound(None, recursive=True)
                print('Menu sounds were disabled')

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
            height=400,
            theme=settings_menu_theme,
            title='Settings',
            width=600
        )

        # Add text inputs with different configurations
        wid1 = settings_menu.add_text_input(
            'First name: ',
            default='John',
            onreturn=check_name_test,
            textinput_id='first_name'
        )
        wid2 = settings_menu.add_text_input(
            'Last name: ',
            default='Rambo',
            maxchar=10,
            textinput_id='last_name',
            input_underline='.'
        )
        settings_menu.add_text_input(
            'Your age: ',
            default=25,
            maxchar=3,
            maxwidth=3,
            textinput_id='age',
            input_type=pygame_menu.locals.INPUT_INT,
            cursor_selection_enable=False
        )
        settings_menu.add_text_input(
            'Some long text: ',
            maxwidth=19,
            textinput_id='long_text',
            input_underline='_'
        )
        settings_menu.add_text_input(
            'Password: ',
            maxchar=6,
            password=True,
            textinput_id='pass',
            input_underline='_'
        )

        # Create selector with 3 difficulty options
        settings_menu.add_selector(
            'Select difficulty ',
            [('Easy', 'EASY'),
             ('Medium', 'MEDIUM'),
             ('Hard', 'HARD')],
            selector_id='difficulty',
            default=1
        )

        def data_fun() -> None:
            """
            Print data of the menu.
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
            height=400,
            theme=settings_menu_theme,
            title='More Settings',
            width=600
        )

        more_settings_menu.add_image(
            pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU,
            scale=(0.25, 0.25),
            align=pygame_menu.locals.ALIGN_CENTER
        )
        more_settings_menu.add_color_input(
            'Color 1 RGB: ',
            color_type='rgb'
        )
        more_settings_menu.add_color_input(
            'Color 2 RGB: ',
            color_type='rgb',
            default=(255, 0, 0),
            input_separator='-'
        )

        def print_color(color) -> None:
            """
            Test onchange/onreturn.
            """
            print('Returned color: ', color)

        more_settings_menu.add_color_input(
            'Color in Hex: ',
            color_type='hex',
            onreturn=print_color
        )

        more_settings_menu.add_vertical_margin(25)
        more_settings_menu.add_button(
            'Return to main menu',
            pygame_menu.events.BACK,
            align=pygame_menu.locals.ALIGN_CENTER
        )

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
            height=400,
            onclose=pygame_menu.events.DISABLE_CLOSE,
            rows=3,
            theme=button_column_menu_theme,
            title='Textures+Columns',
            width=600
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
        main_menu_theme.title_font = pygame_menu.font.FONT_COMIC_NEUE
        main_menu_theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
        main_menu_theme.widget_font_size = 30

        main_menu = pygame_menu.Menu(
            height=400,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=main_menu_theme,
            title='Main menu',
            width=600
        )

        main_menu.add_button('Settings', settings_menu, padding=(0, 0, 0, 0))
        main_menu.add_button('More Settings', more_settings_menu)
        main_menu.add_button('Menu in textures and columns', button_column_menu)
        main_menu.add_selector('Menu sounds ',
                               [('Off', False), ('On', True)],
                               onchange=update_menu_sound)
        main_menu.add_button('Quit', pygame_menu.events.EXIT)

        assert main_menu.get_widget('first_name', recursive=True) is wid1
        assert main_menu.get_widget('last_name', recursive=True) is wid2
        assert main_menu.get_widget('last_name') is None
        main_menu.mainloop(surface, main_background, disable_loop=True)

    def test_menu_compatibility(self) -> None:
        """
        Menu compatibility.
        """
        # Test Menu constructor
        # noinspection PyTypeChecker
        menu = pygame_menu.Menu(400, 300, 'title')
        self.assertEqual(menu._width, 300)
        self.assertEqual(menu._height, 400)
        self.assertEqual(menu.get_title(), 'title')

        # Test widget addition compatibility
        menu = MenuUtils.generic_menu()
        self.assertIsInstance(menu.add_button('title', None), pygame_menu.widgets.Button)
        self.assertIsInstance(menu.add_color_input('title', 'rgb'), pygame_menu.widgets.ColorInput)
        self.assertIsInstance(menu.add_image(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU),
                              pygame_menu.widgets.Image)
        self.assertIsInstance(menu.add_label('title'), pygame_menu.widgets.Label)
        self.assertIsInstance(menu.add_selector(title='epic selector', items=[('1', '3'), ('2', '4')]),
                              pygame_menu.widgets.Selector)
        self.assertIsInstance(menu.add_text_input(title='text', default='the default text'),
                              pygame_menu.widgets.TextInput)
        self.assertIsInstance(menu.add_vertical_margin(10), pygame_menu.widgets.VMargin)
        self.assertIsInstance(menu.add_generic_widget(pygame_menu.widgets.NoneWidget()),
                              pygame_menu.widgets.NoneWidget)
