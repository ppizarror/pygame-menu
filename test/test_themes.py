"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST THEME
Test theme.
"""

__all__ = ['ThemeTest']

from test._utils import MenuUtils, BaseTest
from pathlib import Path

import pygame_menu


class ThemeTest(BaseTest):

    def test_validation(self) -> None:
        """
        Validate theme.
        """
        theme = pygame_menu.themes.THEME_ORANGE.copy()
        self.assertEqual(theme.validate(), theme)

        # Modify property to invalid and assert error
        theme.widget_padding = 'Epic'
        self.assertRaises(AssertionError, lambda: theme.validate())
        theme.widget_padding = -1
        self.assertRaises(AssertionError, lambda: theme.validate())
        theme.widget_padding = (-1, -1)
        self.assertRaises(AssertionError, lambda: theme.validate())
        theme.widget_padding = (1, 1)
        self.assertEqual(theme.validate(), theme)

        # Disable validation
        theme._disable_validation = True
        theme.widget_padding = 'Epic'
        self.assertEqual(theme.validate(), theme)

    def test_copy(self) -> None:
        """
        Test theme copy.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

        # Create theme
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.background_color = image

        # Copy the theme
        theme_copy = theme.__copy__()
        self.assertNotEqual(theme.background_color, theme_copy.background_color)
        self.assertNotEqual(theme.background_color, pygame_menu.themes.THEME_DEFAULT.background_color)

        # Test attribute copy
        color_main = (29, 120, 107, 255)
        color_copy = (241, 125, 1)
        theme_white = pygame_menu.themes.Theme(
            scrollbar_thick=50,
            selection_color=color_main
        )

        sub_theme_white = theme_white.copy()
        sub_theme_white.selection_color = color_copy

        self.assertEqual(theme_white.selection_color, color_main)
        self.assertEqual(sub_theme_white.selection_color, color_copy)

        self.assertNotEqual(theme_white.selection_color, sub_theme_white.selection_color)
        self.assertNotEqual(theme_white.widget_selection_effect, sub_theme_white.widget_selection_effect)

        # Test the widget effect color is different in both objects
        m1 = MenuUtils.generic_menu(theme=theme_white)
        m2 = MenuUtils.generic_menu(theme=sub_theme_white)
        b1 = m1.add.button('1')
        b2 = m2.add.button('2')

        self.assertEqual(b1._selection_effect.color, b1.get_menu().get_theme().selection_color)
        self.assertEqual(b2._selection_effect.color, b2.get_menu().get_theme().selection_color)
        self.assertNotEqual(b1._selection_effect.color, b2._selection_effect.color)

        # Main Theme selection effect class should not be modified
        self.assertEqual(b1.get_menu().get_theme(), theme_white)
        self.assertEqual(theme_white.widget_selection_effect.color, (0, 0, 0))

    def test_methods(self) -> None:
        """
        Test theme method.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

        # Create theme
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.background_color = image

        self.assertRaises(AssertionError, lambda: theme.set_background_color_opacity(0.5))

        # Test color
        self.assertEqual(theme._format_color_opacity([1, 1, 1, 1]), (1, 1, 1, 1))
        self.assertEqual(theme._format_color_opacity([1, 1, 1]), (1, 1, 1, 255))

    def test_invalid_kwargs(self) -> None:
        """
        Test invalid theme kwargs.
        """
        self.assertRaises(ValueError, lambda: pygame_menu.themes.Theme(this_is_an_invalid_kwarg=True))

    def test_to_tuple(self) -> None:
        """
        Test to_tuple theme method.
        """
        t = pygame_menu.themes.THEME_DEFAULT
        self.assertEqual(t._vec_to_tuple((1, 2, 3)), (1, 2, 3))
        self.assertEqual(t._vec_to_tuple([1, 2, 3]), (1, 2, 3))
        self.assertRaises(ValueError, lambda: t._vec_to_tuple(1))
        self.assertRaises(ValueError, lambda: t._vec_to_tuple((1, 2, 3), check_length=4))

    def test_format_opacity(self) -> None:
        """
        Test format opacity color.
        """
        t = pygame_menu.themes.THEME_DEFAULT
        self.assertEqual(t._format_color_opacity((1, 2, 3)), (1, 2, 3, 255))
        self.assertEqual(t._format_color_opacity([1, 2, 3]), (1, 2, 3, 255))
        self.assertEqual(t._format_color_opacity([1, 2, 3, 25]), (1, 2, 3, 25))
        self.assertRaises(AssertionError, lambda: t._format_color_opacity([1, 2]))
        img = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        self.assertEqual(img, t._format_color_opacity(img))
        self.assertIsNone(t._format_color_opacity(None, none=True))
        self.assertRaises(ValueError, lambda: self.assertIsNone(t._format_color_opacity(None)))
        self.assertRaises(ValueError, lambda: t._format_color_opacity('1,2,3'))
        self.assertRaises(AssertionError, lambda: t._format_color_opacity((1, 1, -1)))
        self.assertRaises(AssertionError, lambda: self.assertEqual(t._format_color_opacity((1, 1, 1.1)), (1, 1, 1, 255)))

    def test_str_int_color(self) -> None:
        """
        Test string colors.
        """
        t = pygame_menu.themes.THEME_DEFAULT.copy()
        t.cursor_color = '#ffffff'
        t.validate()
        self.assertEqual(t.cursor_color, (255, 255, 255, 255))

        t2 = pygame_menu.themes.Theme(
            cursor_color='#ffffff',
            selection_color='0xFFFFFF',
            surface_clear_color=0X00,
            title_font_color='chocolate3')
        self.assertEqual(t2.cursor_color, (255, 255, 255, 255))
        self.assertEqual(t2.selection_color, (255, 255, 255, 255))
        self.assertEqual(t2.surface_clear_color, (0, 0, 0, 0))
        self.assertEqual(t2.title_font_color, (205, 102, 29, 255))

    def test_get(self) -> None:
        """
        Test custom types get.
        """
        t = pygame_menu.themes.THEME_DEFAULT
        img = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

        class Test(object):
            """
            Class to test.
            """
            pass

        def dummy() -> bool:
            """
            Callable.
            """
            return True

        # Test correct
        t._get({}, '', 'alignment', pygame_menu.locals.ALIGN_LEFT)
        t._get({}, '', 'callable', dummy)
        t._get({}, '', 'callable', dummy)
        t._get({}, '', 'color', (1, 1, 1))
        t._get({}, '', 'color', [11, 1, 0, 55])
        t._get({}, '', 'color', [11, 1, 0])
        t._get({}, '', 'color_image', (1, 1, 1))
        t._get({}, '', 'color_image', [11, 1, 0, 55])
        t._get({}, '', 'color_image', [11, 1, 0])
        t._get({}, '', 'color_image', img)
        t._get({}, '', 'color_image_none', [11, 1, 0, 55])
        t._get({}, '', 'color_image_none', img)
        t._get({}, '', 'color_image_none', None)
        t._get({}, '', 'color_none', (1, 1, 1))
        t._get({}, '', 'color_none', [11, 1, 0, 55])
        t._get({}, '', 'color_none', [11, 1, 0])
        t._get({}, '', 'color_none', None)
        t._get({}, '', 'cursor', 1)
        t._get({}, '', 'cursor', None)
        t._get({}, '', 'font', 'font')
        t._get({}, '', 'font', Path('.'))
        t._get({}, '', 'image', img)
        t._get({}, '', 'none', None)
        t._get({}, '', 'position', pygame_menu.locals.POSITION_SOUTHWEST)
        t._get({}, '', 'position_vector', [pygame_menu.locals.POSITION_WEST, pygame_menu.locals.POSITION_NORTH])
        t._get({}, '', 'tuple2', (1, -1))
        t._get({}, '', 'tuple2', (1, 1))
        t._get({}, '', 'tuple2', [1, -1])
        t._get({}, '', 'tuple2int', (0.000000000, 0.0))
        t._get({}, '', 'tuple2int', (1.0, -1))
        t._get({}, '', 'tuple2int', [1, -1])
        t._get({}, '', 'tuple3', [1, -1, 1])
        t._get({}, '', 'tuple3int', [1, -1.0, 1])
        t._get({}, '', 'type', bool)
        t._get({}, '', bool, True)
        t._get({}, '', callable, dummy)
        t._get({}, '', int, 4)
        t._get({}, '', str, 'hi')
        t._get({}, '', Test, Test())

        self.assertTrue(t._get({}, '', 'callable', dummy)())

        # Test raises
        invalid_pos_vector = [
            [pygame_menu.locals.POSITION_WEST, pygame_menu.locals.POSITION_WEST],
            [pygame_menu.locals.POSITION_WEST, 2],
            [pygame_menu.locals.POSITION_WEST, bool]
        ]

        self.assertRaises(AssertionError, lambda: t._get({}, '', 'color', [1, 1, 1, 256]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'color', [11, 1, -1]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'color', [11, 1, -1]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'color', [11, 1]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'color', None))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'cursor', 'hi'))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'font', 1))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'image', bool))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'none', 1))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'none', bool))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'position', 'position-invalid'))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'position_vector', invalid_pos_vector))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'position_vector', invalid_pos_vector[0]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'position_vector', invalid_pos_vector[1]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'position_vector', invalid_pos_vector[2]))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'tuple2', (1, 1, 1)))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'tuple2.1', (1, 1)))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'tuple2int', (1.5, 1)))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'tuple3', (1, 1, 1, 1)))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'tuple3int', (1, 1, 1.000001)))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'type', 'bool'))
        self.assertRaises(AssertionError, lambda: t._get({}, '', 'unknown', Test()))
        self.assertRaises(AssertionError, lambda: t._get({}, '', bool, 4.4))
        self.assertRaises(AssertionError, lambda: t._get({}, '', callable, Test()))
        self.assertRaises(AssertionError, lambda: t._get({}, '', int, 4.4))
