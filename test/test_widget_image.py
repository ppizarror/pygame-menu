"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - IMAGE
Test Image widget.
"""

__all__ = ['ImageWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, BaseTest

import pygame
import pygame_menu


class ImageWidgetTest(BaseTest):

    def test_image_widget(self) -> None:
        """
        Test image widget.
        """
        menu = MenuUtils.generic_menu()
        image = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, font_color=(2, 9))

        image.set_title('epic')
        self.assertEqual(image.get_title(), '')
        self.assertEqual(image.get_image(), image._image)
        image.update(PygameEventUtils.mouse_motion(image))

        self.assertEqual(image.get_height(apply_selection=True), 264)
        self.assertFalse(image._selected)
        self.assertEqual(image.get_selected_time(), 0)

        # Test transformations
        self.assertEqual(image.get_size(), (272, 264))
        image.scale(2, 2)
        self.assertEqual(image.get_size(), (528, 520))
        image.resize(500, 500)

        # Remove padding
        image.set_padding(0)
        self.assertEqual(image.get_size(), (500, 500))

        # Set max width
        image.set_max_width(400)
        self.assertEqual(image.get_size(), (400, 500))
        image.set_max_width(800)
        self.assertEqual(image.get_size(), (400, 500))
        image.set_max_width(300, scale_height=True)
        self.assertEqual(image.get_size(), (300, 375))

        # Set max height
        image.set_max_height(400)
        self.assertEqual(image.get_size(), (300, 375))
        image.set_max_height(300)
        self.assertEqual(image.get_size(), (300, 300))
        image.set_max_height(200, scale_width=True)
        self.assertEqual(image.get_size(), (200, 200))

        self.assertEqual(image.get_angle(), 0)
        image.rotate(90)
        self.assertEqual(image.get_angle(), 90)
        image.rotate(60)
        self.assertEqual(image.get_angle(), 60)

        # Flip
        image.flip(True, True)
        self.assertEqual(image._flip, (True, True))
        image.flip(False, False)
        self.assertEqual(image._flip, (False, False))
        image.draw(surface)

    def test_value(self) -> None:
        """
        Test image value.
        """
        menu = MenuUtils.generic_menu()
        image = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        self.assertRaises(ValueError, lambda: image.get_value())
        self.assertRaises(ValueError, lambda: image.set_value('value'))
        self.assertFalse(image.value_changed())
        image.reset_value()

    def test_image_from_surface(self) -> None:
        """
        Test that Image accepts a pygame.Surface and wraps it correctly.
        """
        menu = MenuUtils.generic_menu()
        surf = pygame.Surface((120, 80))
        img = menu.add.image(surf)
        img.set_padding(0)
        self.assertIsInstance(img.get_image(), pygame_menu.baseimage.BaseImage)
        self.assertEqual(img.get_size(), (120, 80))

    def test_image_surface_transformations(self) -> None:
        """
        Test transformations on an Image created from a pygame.Surface.
        """
        menu = MenuUtils.generic_menu()
        surf = pygame.Surface((100, 50))
        img = menu.add.image(surf)
        img.set_padding(0)
        img.scale(2, 2)
        self.assertEqual(img.get_size(), (200, 100))
        img.resize(300, 150)
        self.assertEqual(img.get_size(), (300, 150))
        img.rotate(45)
        self.assertEqual(img.get_angle(), 45)

    def test_image_surface_widget_behavior(self) -> None:
        """
        Ensure Surface-based Image behaves like a normal widget.
        """
        menu = MenuUtils.generic_menu()
        surf = pygame.Surface((60, 60))
        img = menu.add.image(surf)
        img.set_padding(10)
        self.assertEqual(img.get_size(), (80, 80))
        img.update(PygameEventUtils.mouse_motion(img))
        self.assertTrue(img._mouseover)
