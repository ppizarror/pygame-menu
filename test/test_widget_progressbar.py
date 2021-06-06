"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - PROGRESSBAR
Test ProgressBar widget.

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

__all__ = ['ProgressBarWidgetTest']

from test._utils import MenuUtils, surface, BaseTest, PYGAME_V2

import pygame_menu

from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented


class ProgressBarWidgetTest(BaseTest):

    def test_progressbar(self) -> None:
        """
        Test progressbar slider.
        """
        menu = MenuUtils.generic_menu()
        pb = pygame_menu.widgets.ProgressBar('progress',
                                             progress_text_font=pygame_menu.font.FONT_BEBAS)
        menu.add.generic_widget(pb, configure_defaults=True)
        menu.draw(surface)

        self.assertRaises(AssertionError, lambda: pygame_menu.widgets.ProgressBar(
            'progress', default=-1))

        self.assertEqual(pb.get_size(), (312, 49))
        self.assertEqual(pb._width, 150)

        # Test invalid transforms
        self.assertRaises(WidgetTransformationNotImplemented, lambda: pb.rotate())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: pb.flip())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: pb.scale())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: pb.resize())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: pb.set_max_width())
        self.assertRaises(WidgetTransformationNotImplemented, lambda: pb.set_max_height())

        self.assertFalse(pb.update([]))

    # noinspection PyTypeChecker
    def test_value(self) -> None:
        """
        Test progressbar value.
        """
        menu = MenuUtils.generic_menu()
        pb = menu.add.progress_bar('progress', default=50,
                                   progress_text_align=pygame_menu.locals.ALIGN_LEFT)
        self.assertRaises(AssertionError, lambda: pb.set_value(-1))
        self.assertRaises(AssertionError, lambda: pb.set_value('a'))
        self.assertEqual(pb.get_value(), 50)
        self.assertFalse(pb.value_changed())
        pb.set_value(75)
        self.assertEqual(pb.get_value(), 75)
        self.assertTrue(pb.value_changed())
        pb.reset_value()
        self.assertEqual(pb.get_value(), 50)
        self.assertFalse(pb.value_changed())

    def test_empty_title(self) -> None:
        """
        Test empty title.
        """
        menu = MenuUtils.generic_menu()
        pb = menu.add.progress_bar('', box_margin=(0, 0), padding=0,
                                   progress_text_align=pygame_menu.locals.ALIGN_RIGHT)
        self.assertEqual(pb.get_size(), (150, 41 if PYGAME_V2 else 42))
        self.assertFalse(pb.is_selected())
