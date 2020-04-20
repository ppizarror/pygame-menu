# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST BASE IMAGE
Test base image management.

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

from test._utils import *


class BaseImageTest(unittest.TestCase):

    def test_extension_validation(self):
        """
        Validate a image extension.
        """
        self.assertRaises(AssertionError, lambda: pygame_menu.baseimage.BaseImage('invalid.pnng'))
        self.assertRaises(AssertionError, lambda: pygame_menu.baseimage.BaseImage('invalid'))
        self.assertRaises(AssertionError, lambda: pygame_menu.baseimage.BaseImage('file_invalid.png'))
        pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    def test_image_properties(self):
        """
        Test the getters of the image object.
        """
        image = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        w, h = image.get_size()
        self.assertEqual(w, 256)
        self.assertEqual(h, 256)
        self.assertEqual(image.get_namefile(), 'gray_lines')
        self.assertEqual(image.get_extension(), '.png')

    def test_operations(self):
        """
        Test the file operations.
        """
        image_original = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        image = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        self.assertTrue(image.equals(image_original))

        # Flip
        image.flip(True, False)
        self.assertFalse(image.equals(image_original))
        image.restore()
        self.assertTrue(image.equals(image_original))

        # Checkpoint
        image.flip(True, False)
        self.assertFalse(image.equals(image_original))
        image.checkpoint()
        self.assertFalse(image.equals(image_original))
        image.restore()
        self.assertFalse(image.equals(image_original))

    def test_transform(self):
        """
        Test the image transformation.
        """
        image_original = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        image = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

        # Scale
        image.scale(0.5, 0.5)
        w, h = image.get_size()
        self.assertEqual(w, 128)
        self.assertEqual(h, 128)
        self.assertRaises(AssertionError, lambda: image.scale(0, 1))
        image.scale(2, 1)
        w, h = image.get_size()
        self.assertEqual(w, 256)
        self.assertEqual(h, 128)
        self.assertFalse(image.equals(image_original))

        # Set size
        image.restore()
        image.resize(100, 50)
        w, h = image.get_size()
        self.assertEqual(w, 100)
        self.assertEqual(h, 50)
        image.restore()
        self.assertTrue(image.equals(image_original))

        # As the example is not 24/32 bits smooth scale fails
        self.assertRaises(ValueError, lambda: image.resize(100, 100, True))

        # Get rect
        rect = image.get_rect()
        self.assertEqual(rect.width, 256)

        # Rotate
        image.rotate(45)
        w, h = image.get_size()
        self.assertEqual(w, 362)
        self.assertEqual(h, 362)
        image.restore()

        # Scale 2x
        image.scale2x()
        w, h = image.get_size()
        self.assertEqual(w, 512)
        self.assertEqual(h, 512)
        image.restore()

        # Scale should not change
        image.scale(1, 1)
