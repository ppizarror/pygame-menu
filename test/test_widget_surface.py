"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - SURFACE
Test Surface widget.
"""

__all__ = ['SurfaceWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, BaseTest
import pygame

from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented


class SurfaceWidgetTest(BaseTest):

    def test_surface_widget(self) -> None:
        """
        Test surface widget.
        """
        menu = MenuUtils.generic_menu()
        surf = pygame.Surface((150, 150))
        surf.fill((255, 192, 203))
        surf_widget = menu.add.surface(surf, font_color='red')

        self.assertEqual(surf_widget.get_size(), (166, 158))
        self.assertEqual(surf_widget.get_size(apply_padding=False), (150, 150))
        self.assertEqual(surf_widget.get_surface(), surf)
        self.assertEqual(surf_widget._font_color, (70, 70, 70, 255))  # not red

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.rotate(10))
        self.assertEqual(surf_widget._angle, 0)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.resize(10, 10))
        self.assertFalse(surf_widget._scale[0])
        self.assertEqual(surf_widget._scale[1], 1)
        self.assertEqual(surf_widget._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.scale(100, 100))
        self.assertFalse(surf_widget._scale[0])
        self.assertEqual(surf_widget._scale[1], 1)
        self.assertEqual(surf_widget._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.flip(True, True))
        self.assertFalse(surf_widget._flip[0])
        self.assertFalse(surf_widget._flip[1])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.set_max_width(100))
        self.assertIsNone(surf_widget._max_width[0])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: surf_widget.set_max_height(100))
        self.assertIsNone(surf_widget._max_height[0])

        surf_widget.set_title('epic')
        self.assertEqual(surf_widget.get_title(), '')

        new_surface = pygame.Surface((160, 160))
        new_surface.fill((255, 192, 203))
        inner_surface = pygame.Surface((80, 80))
        inner_surface.fill((75, 0, 130))
        new_surface.blit(inner_surface, (40, 40))
        surf_widget.set_surface(new_surface)
        self.assertEqual(surf_widget.get_size(apply_padding=False), (160, 160))
        menu.draw(surface)
        surf_widget.update(PygameEventUtils.mouse_motion(surf_widget))
        surf_widget.draw(surface)

    def test_value(self) -> None:
        """
        Test surface value.
        """
        menu = MenuUtils.generic_menu()
        surf = menu.add.surface(pygame.Surface((150, 150)))
        self.assertRaises(ValueError, lambda: surf.get_value())
        self.assertRaises(ValueError, lambda: surf.set_value('value'))
        self.assertFalse(surf.value_changed())
        surf.reset_value()
