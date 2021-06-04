"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - IMAGE
Test Image widget.

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

__all__ = ['ImageWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, BaseTest
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
