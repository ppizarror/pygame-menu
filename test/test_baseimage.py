"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST BASE IMAGE
Test base image management.
"""

__all__ = ['BaseImageTest']

from pathlib import Path
from test._utils import surface, PYGAME_V2, BaseTest
import base64
import copy
import io

import pygame
import pygame_menu

from pygame_menu.baseimage import IMAGE_MODE_CENTER, IMAGE_MODE_FILL, IMAGE_MODE_REPEAT_X, \
    IMAGE_MODE_REPEAT_XY, IMAGE_MODE_REPEAT_Y, IMAGE_MODE_SIMPLE
from pygame_menu.utils import load_pygame_image_file


class BaseImageTest(BaseTest):

    def test_pathlib(self) -> None:
        """
        Test image load with pathlib.
        """
        path_img = Path(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        image = pygame_menu.BaseImage(path_img)
        image.draw(surface)
        self.assertEqual(image.get_path(), str(path_img))

    # noinspection SpellCheckingInspection
    def test_from_bytesio(self) -> None:
        """
        Test image load from base64.
        """
        photo = 'R0lGODlhRgBGAPZUAAAAAAAAMwAAzAArAAArMwArzAAr/wBVmQBVzABV/zMAADMAMzMrADMrMzMrmTMrzDMr/zNVADNVMzNVZjNVmTN' \
                'VzDNV/zOAADOAMzOAZjOA/zOqM2YAM2YrAGYrM2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaAM2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmW' \
                'aqzJkrAJkrM5lVAJlVM5lVZplVmZmAAJmAM5mAZpmAmZmAzJmqZpmqmZmqzJmq/5nVmZnVzMxVAMxVM8xVZsyAAMyAM8yAZsyqZsyqm' \
                'cyqzMyq/8zVmczVzMzV/8z/zMz////VzP/V////zP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' \
                'AAAAAAAAAAAAAACH5BAUAAFQALAAAAABGAEYAAAf/gFOCg4SFhoeIiYZMOScoKI45SUxJk4qXmJmJSSghKCI4OSInOT1JTT05TJqsrY' \
                'hMPCETnpCQIjyVSbiuvK1NjJ2jIiE5KI0ouJQ8PVC9zohPusWOndU4o5+4SaWrz96CULAhnsU4n9Tlnqc9SElP389NPKK1J8KkKOa0y' \
                'JU9u/CumDByhI+GsWq0zOUgZ6oSDx5RAGriYcyTvVrHruUTkQ/SsUlJTEnMxClEpI7HikGq4fFRDXsn+jFpNjIRk1SOsJGz1wgURkfm' \
                'UOrg0Y2VwElFX1WClRFlx6cKN1bsaBJFklYCmSB5mCypIIFcH467uLCjTxQGbXXEx/GRKk1O/2CZwGCChYm5JnIQHST3LgsMszgGTRm' \
                'pcDm3J0idQOJVEZMTd+ni3XD3gokTqx5PvivrxM6pPY+9fGTwotUmRlvgtUvZbt2/JnDtkOx6Q4hhEzyOmsa7JTpcUlo9QWLigl3XsG' \
                'HX3bEDMga7z03I6gSzNzHSj6713MsKCg/VdylHr+uXrnnk4U3Muk2QXtCgJ1hCmjHjSMTUEUxQJk/+eXTod/XnmgkSoLCeR4V9EpQxM' \
                '8ggwwxIvKMJE8WRt99+A7Y2V3LhwcYeR6HxBBQkITT4YDs0XSIFD7DRVl5d4w0II392zXLgMVRVRIMHHjjoIITBXdKEX5ERSJcEdyG5' \
                '4f9mx9HVpCchZLDbU3oJlEMHMfQoAxE2FNGYIVC0uFp5rh3JAoDKHZekBMNYxBExlkzBxAw89kgEETIwdgmF/ZHpVwZzgUDXCei12KI' \
                'EnlXTSClByolDnVviicMS9yHCA1376RcghwNicB5eSa42gQizJMqEhIMkAUKPJsogxBFIQOHEIY8ViuhDzkUQ3X4SSABCr0ZuSh6iEk' \
                'yAJBKHJDFDBzJ40CAROBwBRJyE8LDaeTtMwgMO4C1plwQYCIokpjOy4CuSEUiwA2qFzAkCDDzeWQQOPOzAAyFMNPciBotJ2IQTUcByg' \
                'nk08lcwwf6Z0OggUOCQpQcfBDEDCEUW9dj/BQRj9iU4SziHV8LJIWzXCTg0x267PPQIAwgy2CDDXyzs8JW1xvG3Mb7fjUskedAJOqlA' \
                'TjSRoiFR8LBsvEQE+9UOGG7Yw8JTBHyTQOFY+zGMLQrKQjL4JrIECB8gHSgGX73oWgsQ8RWLBA00EEJXPAy8qcf8ItGDZ/d+ZZNqLD9' \
                'I8XNlO7kkXd0wEULbIACgeNuYyYkEueDOhURcITAQgARXybkxFC1gLEMMIFBsl+Y7Q1dCbF9JAEADJ0yggOKrZ14rXpa1sEoSqq9eeC' \
                'JOQGbCDBxAfCbZsIjHoXhLTJFEA6s/lLviIXTD1V0n7BWFZ4oTgKyciXBuHAgdePC3/wlTxF26i5jxwDwAC6wPwACrzzoFFE9AAQQTj' \
                'aq/OgMNuAPFyYZ4gr5MAIIY0CIE3lFTjJyEgR20wH2wawDbGtANAAoiIupjAJQccrPy4YAyiRoG+VrgnNrw7DkkXIDiJBCAxY2DggGD' \
                '2hScsI0BBIAUIMCVDBmWr7kkxjOEcgIOYrQzYUlgAA2gQe4k8EKuMCFghCia61bHtglcpoNO6IGaqEO2IrWGXGqaS6/ctwAkDmCISGr' \
                'B9lL3OtgxgC4yU0QUliC4xJiECZ0zmGpM+JxvMWAAZRzAHxtAF10l5gdMEBoTJqC4ARCAARIwDg8sWIhoaOoyb5LCCSQAHeWMJ/9A/e' \
                'kVkpAEIFCi7SEgaMAAfPWtxiUiCisyIUzwWIL/8Cw9nvLWmWAkqCVl6i4kVCAIbJeIaPhjSZdJjCYlMzgWEAqURwqUzkB1yw2EEQO9c' \
                'iAPhlYIVECAAsLijBRacDoN9QlmZSIQXpQkOONFBja9wgAPlqAVVHUzBQ8ogBU7aQIUPCE9WCsdMq8Jqk+GK0DRjI1WaLAxJlTAAAmo' \
                'gOBGxjnJZGpXyNyAp5qkJvEgCQQzwEFIZ0CDGdwApDjAwRBukDlDNOGhCTCAFVcwIyFaBjnP3BldKJYeuYEqdCAIAQ2GSlKSErWk9MF' \
                'fshAQUwQgQEAmqOi1Ogko2NAAB1f/DSoBt1qiktIApCCdWElFaoSRljQJlSKEEmBqAAREzjUCLKKaSjlWs2J1CDS4wVe7OtarFvWr9A' \
                'EBDr4kBSD0AKKIrQAFMFACtEVhBzNyJ23ocgO8FoGogf1rWcv61dDdBaih8wBDD9GEFFQgpglIbVutKDMnmO+WJyRPibBKnxLZdqS07' \
                'aySOBM6oe4grYN4aQEQi9oCUMAF20vCbNIEskuWiKQi9WtJgcokQ1lzB0yQXyGcoAMLEBe1BqhAD/jyAyJtwHcDCiMot+otInEKL9xZ' \
                'hAUKgFoEQDSmFngaXwDaH9Xsxz9/MY+nPvVFnZInjoaQgg8egNoGQxQCPrAY/3hgRiRbFuyW12wSf+jCA3t+xQdsBW8C7JuAFLS0tJH' \
                'DJXIYGDKo2tJF4nHlIJ7QhBGEeMT3fbAOgPCVHlQgBLUEVRiHXGH0aKqj5OGBdvkyAhITN8dNVQJfdACBCVjxoIMiF6D4palP8jNAv5' \
                'TAE7vpY+Iy9b70hWgFKmjaBBRAohsmWEGpmbC6DOwvdMMABVLQg5MloQIh/i5iC5BfQlRguDGtwEzVi9BGA8qHnuolqGgqAftaYM1SK' \
                'K2b6wtlNFfgxIdWLQIOoKS5HmeujU71eltnAAO82QcheeiTU0tf1Yb3BVGsgACIS+gCHMDKOtPQeDTEXLxM4AAIqHWrE/tw6bY2WLXg' \
                'RYAFqDWFlwpa1CN+8wEcgAAKdLvbB6AABcId7nFz+wCHJrGD171pKMfUACnwShTm22kRfzfN9M23fYfrZBH729nuRuyZE/CA8XZT1s+' \
                '+9rvX/V12uzvN9m6wst1sgWR5t60QhXi/ax3xWWdcxBB3MIn7jdgH5JebU+jBxd+N2GUPt+VpbjnLF+7yZbe65iyX+c1H0APgCkLlBr' \
                'AAs5ktbWYHXdpBN7oFin5aoTcdARAYutCnHtEERJ3qQo960xPA81MdwgcqsEDYVaABEpD97CnQgArITgK1l33sYy+72+NudrGfXe1in' \
                'zveVVABFSQBYIgIBAA7'
        output = io.BytesIO(base64.b64decode(photo))
        image = pygame_menu.BaseImage(output)
        self.assertEqual(image.get_width(), 70)
        self.assertEqual(image.get_height(), 70)
        self.assertEqual(image.get_bitsize(), 8)
        self.assertEqual(image.get_size(), (70, 70))
        self.assertEqual(image.get_path(), output)
        self.assertEqual(image.get_extension(), 'BytesIO')

        # Assemble new from base64 bs
        image2 = pygame_menu.BaseImage(photo, frombase64=True)
        self.assertTrue(image.equals(image2))
        self.assertEqual(image2.get_extension(), 'base64')

        # Clone base64
        image3 = image2.copy()
        if PYGAME_V2:
            self.assertTrue(image2.equals(image3))

    def test_rotation(self) -> None:
        """
        Test rotation.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        image.rotate(360)
        prev_size = image.get_size()
        self.assertEqual(prev_size, (256, 256))
        i_sum = 0
        for i in range(91):
            image.rotate(i_sum)
            i_sum += 1  # Rotate the image many angles
        self.assertEqual(image.get_size(), prev_size)

        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU)
        self.assertEqual(image.get_size(), (640, 505))
        image.rotate(90)
        self.assertEqual(image.get_size(), (505, 640))
        image.rotate(180)
        self.assertEqual(image.get_size(), (640, 505))
        image.rotate(270)
        self.assertEqual(image.get_size(), (505, 640))
        image.rotate(360)
        self.assertEqual(image.get_size(), (640, 505))

        self.assertEqual(image.get_angle(), 0)
        image.rotate(60)
        self.assertEqual(image.get_size(), (757, 806))
        self.assertEqual(image.get_angle(), 60)
        image.rotate(160)
        self.assertEqual(image.get_size(), (774, 693))
        self.assertEqual(image.get_angle(), 160)
        image.rotate(180)
        self.assertEqual(image.get_angle(), 180)
        self.assertEqual(image.get_size(), (640, 505))

    def test_crop(self) -> None:
        """
        Test baseimage crop.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        image_c = image.get_crop(0, 0, 10, 10)
        image_cr = image.get_crop_rect(pygame.Rect(0, 0, 10, 10))
        im1 = pygame.image.tostring(image_c, 'RGBA')
        im2 = pygame.image.tostring(image_cr, 'RGBA')
        self.assertEqual(im1, im2)

        # Save the whole image crop
        w, h = image.get_size()
        image2 = image.copy()
        image2.crop(0, 0, w, h)
        self.assertTrue(image2.equals(image))

        # Crop from rect
        image.crop_rect(pygame.Rect(0, 0, 8, 8))
        self.assertEqual(image.get_size(), (8, 8))

    # noinspection PyTypeChecker
    def test_alpha(self) -> None:
        """
        Test alpha modes.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        self.assertRaises(AssertionError, lambda: image.set_alpha(0.5))
        self.assertRaises(AssertionError, lambda: image.set_alpha(-1))
        self.assertRaises(AssertionError, lambda: image.set_alpha(267))
        image.set_alpha(None)

    def test_modes(self) -> None:
        """
        Test drawing modes.
        """
        for mode in [IMAGE_MODE_CENTER, IMAGE_MODE_FILL, IMAGE_MODE_REPEAT_X, IMAGE_MODE_REPEAT_XY,
                     IMAGE_MODE_REPEAT_Y, IMAGE_MODE_SIMPLE]:
            image = pygame_menu.BaseImage(
                pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
                drawing_mode=mode
            )
            image.draw(surface)

        # Attempt to create an invalid drawing mode
        self.assertRaises(AssertionError, lambda: pygame_menu.BaseImage(
            pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
            drawing_mode=-1
        ))

        # Get drawing mode
        image = pygame_menu.BaseImage(
            pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
            drawing_mode=IMAGE_MODE_CENTER
        )
        self.assertEqual(image.get_drawing_mode(), IMAGE_MODE_CENTER)

    def test_drawing_offset(self) -> None:
        """
        Test drawing offset.
        """
        image = pygame_menu.BaseImage(
            pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
            drawing_mode=IMAGE_MODE_CENTER
        )
        image.set_drawing_offset((50, 150))
        self.assertEqual(image.get_drawing_offset(), (50, 150))

    def test_image_path(self) -> None:
        """
        Test path.
        """
        image = pygame_menu.BaseImage(
            pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES,
            drawing_mode=IMAGE_MODE_CENTER
        )
        self.assertEqual(image.get_path(), pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    # noinspection SpellCheckingInspection
    def test_extension_validation(self) -> None:
        """
        Validate a image extension.
        """
        self.assertRaises(AssertionError, lambda: pygame_menu.BaseImage('invalid.pnng'))
        self.assertRaises(AssertionError, lambda: pygame_menu.BaseImage('invalid'))
        self.assertRaises(AssertionError, lambda: pygame_menu.BaseImage('file_invalid.png'))
        pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

    def test_image_properties(self) -> None:
        """
        Test the getters of the image object.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        w, h = image.get_size()
        self.assertEqual(w, 256)
        self.assertEqual(h, 256)
        self.assertEqual(image.get_filename(), 'gray_lines')
        self.assertEqual(image.get_extension(), '.png')

    def test_scale(self) -> None:
        """
        Test scale.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        w, h = image.get_size()
        self.assertEqual(w, 256)
        self.assertEqual(h, 256)

        image4 = image.copy().scale(4, 4)
        self.assertEqual(image4.get_size(), (1024, 1024))

        # Apply scale 2x algorithm
        image4a = image.copy().scale2x().scale2x()
        self.assertEqual(image4a.get_size(), (1024, 1024))

        image4b = image.copy().scale4x()

        image.scale(2, 2).scale(2, 2)
        self.assertEqual(image.get_size(), (1024, 1024))

        # Check if equal
        self.assertTrue(image.equals(image4))
        self.assertFalse(image.equals(image4a))
        self.assertTrue(image4a.equals(image4b))

    def test_operations(self) -> None:
        """
        Test the file operations.
        """
        image_original = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
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

    def test_invalid_image(self) -> None:
        """
        Test invalid image opening.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYTHON)
        self.assertEqual(image.get_size(), (110, 109))

        image._drawing_position = 'invalid'
        self.assertRaises(ValueError, lambda: image._get_position_delta())

        # Test invalid image
        self.assertRaises(Exception, lambda: load_pygame_image_file(pygame_menu.baseimage.IMAGE_EXAMPLE_PYTHON, test=True))

    def test_copy(self) -> None:
        """
        Test copy image.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        image_copied = image.copy()
        self.assertTrue(image.equals(image_copied))
        image_copy = copy.copy(image)
        image_copy2 = copy.deepcopy(image)
        self.assertTrue(image.equals(image_copy))
        self.assertTrue(image.equals(image_copy2))

    def test_transform(self) -> None:
        """
        Test the image transformation.
        """
        image_original = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)

        # Scale
        image.scale(0.5, 0.5)
        self.assertEqual(image.get_size(), (128, 128))
        self.assertRaises(AssertionError, lambda: image.scale(0, 1))
        image.scale(2, 1)
        self.assertEqual(image.get_size(), (256, 128))
        self.assertFalse(image.equals(image_original))

        # Set size
        image.restore()
        image.resize(100, 50)
        image.resize(100, 50)  # This should do nothing
        self.assertEqual(image.get_size(), (100, 50))
        image.restore()
        self.assertTrue(image.equals(image_original))

        # As the example is not 24/32 bits smooth scale fails, but baseimage should notice that
        imag_c = image.copy()
        imag_c.resize(100, 100)

        # Get rect
        rect = image.get_rect()
        self.assertEqual(rect.width, 256)

        # Rotate
        image.rotate(45)
        self.assertEqual(image.get_size(), (362, 362))
        image.restore()

        # Scale 2x
        image.scale2x()
        self.assertEqual(image.get_size(), (512, 512))
        image.restore()

        # Scale should not change
        image.scale(1, 1)

        # Image bw
        image.to_bw()

        # Image channels
        # noinspection PyTypeChecker
        image.pick_channels(('r', 'g', 'b'))

        self.assertEqual(image.get_at((10, 10)), (56, 56, 56, 255))

        image.set_at((10, 10), (0, 0, 0))
        # self.assertEqual(image.get_at((10, 10)), (0, 0, 0, 255))

    def test_drawing_position(self) -> None:
        """
        Test drawing position.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, drawing_offset=(100, 100))
        w, h = image.get_size()
        image.set_drawing_position(pygame_menu.locals.POSITION_NORTHWEST)
        self.assertEqual(image._get_position_delta(), (0, 0))
        image.set_drawing_position(pygame_menu.locals.POSITION_NORTH)
        self.assertEqual(image._get_position_delta(), (w / 2, 0))
        image.set_drawing_position(pygame_menu.locals.POSITION_NORTHEAST)
        self.assertEqual(image._get_position_delta(), (w, 0))
        image.set_drawing_position(pygame_menu.locals.POSITION_WEST)
        self.assertEqual(image._get_position_delta(), (0, h / 2))
        image.set_drawing_position(pygame_menu.locals.POSITION_CENTER)
        self.assertEqual(image._get_position_delta(), (w / 2, h / 2))
        image.set_drawing_position(pygame_menu.locals.POSITION_EAST)
        self.assertEqual(image._get_position_delta(), (w, h / 2))
        image.set_drawing_position(pygame_menu.locals.POSITION_SOUTHWEST)
        self.assertEqual(image._get_position_delta(), (0, h))
        image.set_drawing_position(pygame_menu.locals.POSITION_SOUTH)
        self.assertEqual(image._get_position_delta(), (w / 2, h))
        image.set_drawing_position(pygame_menu.locals.POSITION_SOUTHEAST)
        self.assertEqual(image._get_position_delta(), (w, h))
        self.assertRaises(AssertionError, lambda: image.set_drawing_position(pygame_menu.locals.ALIGN_LEFT))

    def test_attributes_copy(self) -> None:
        """
        Test image attributes on object copy.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, drawing_offset=(100, 100))
        image.set_attribute('angle', 0)
        image2 = image.copy()
        self.assertTrue(image2.has_attribute('angle'))
        self.assertEqual(image2.get_attribute('angle'), 0)
        self.assertEqual(image.get_attribute('angle'), 0)
        image2.set_attribute('angle', 1)
        self.assertEqual(image2.get_attribute('angle'), 1)
        self.assertEqual(image.get_attribute('angle'), 0)

    def test_cache(self) -> None:
        """
        Cache draw test.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES)
        self.assertIsNone(image._last_transform[2])

        image.set_drawing_mode(pygame_menu.baseimage.IMAGE_MODE_FILL)

        # Draw, this should force cache
        image.draw(surface)
        self.assertIsNotNone(image._last_transform[2])
        s = image._last_transform[2]
        image.draw(surface)  # Draw again, then the image should be the same
        self.assertEqual(image._last_transform[2], s)
        self.assertEqual(image._last_transform[0], 600)

        # Changes the area, then image should change
        r = image.get_rect()
        r.width = 300
        image.draw(surface, r)
        self.assertNotEqual(image._last_transform[2], s)
        self.assertEqual(image._last_transform[0], 300)

    def test_subsurface(self) -> None:
        """
        Test subsurface.
        """
        image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_TILED_BORDER)
        self.assertEqual(image.get_size(), (18, 18))
        self.assertEqual(image.subsurface((0, 0, 3, 3)).get_size(), (3, 3))
