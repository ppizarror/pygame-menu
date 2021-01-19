# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST BASE IMAGE
Test base image management.

NOTE: pygame-menu v3 will not provide new widgets or functionalities, consider
upgrading to the latest version.

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

from test._utils import *
import sys

from pygame_menu.baseimage import *


class BaseImageTest(unittest.TestCase):

    def test_pathlib(self):
        """
        Test image load with pathlib.
        """
        if sys.version_info >= (3, 0):
            # noinspection PyCompatibility
            from pathlib import Path
            pathimg = Path(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
            image = pygame_menu.baseimage.BaseImage(pathimg)
            image.draw(surface)
            self.assertEqual(image.get_path(), str(pathimg))

    def test_modes(self):
        """
        Test drawing modes.
        """
        for mode in [IMAGE_MODE_CENTER, IMAGE_MODE_FILL, IMAGE_MODE_REPEAT_X, IMAGE_MODE_REPEAT_XY,
                     IMAGE_MODE_REPEAT_Y, IMAGE_MODE_SIMPLE]:
            image = pygame_menu.baseimage.BaseImage(
                pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
                drawing_mode=mode
            )
            image.draw(surface)

        # Attempt to create an invalid drawing mode
        self.assertRaises(AssertionError, lambda: pygame_menu.baseimage.BaseImage(
            pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
            drawing_mode=-1
        ))

        # Get drawing mode
        image = pygame_menu.baseimage.BaseImage(
            pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
            drawing_mode=IMAGE_MODE_CENTER
        )
        self.assertEqual(image.get_drawing_mode(), IMAGE_MODE_CENTER)

    def test_drawing_offset(self):
        """
        Test drawing offset.
        """
        image = pygame_menu.baseimage.BaseImage(
            pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
            drawing_mode=IMAGE_MODE_CENTER
        )
        image.set_drawing_offset((50, 150))
        self.assertEqual(image.get_drawing_offset()[0], 50)
        self.assertEqual(image.get_drawing_offset()[1], 150)

    def test_image_path(self):
        """
        Test path.
        """
        image = pygame_menu.baseimage.BaseImage(
            pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
            drawing_mode=IMAGE_MODE_CENTER
        )
        self.assertEqual(image.get_path(), pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

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

    def test_copy(self):
        """
        Test copy image.
        """
        image = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        image_copied = image.copy()
        self.assertTrue(image.equals(image_copied))

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

        # As the example is not 24/32 bits smooth scale fails, but baseimage should notice that
        imagc = image.copy()
        imagc.resize(100, 100, True)

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

        # Image bw
        image.to_bw()

        # Image channels
        image.pick_channels(('r', 'g', 'b'))
