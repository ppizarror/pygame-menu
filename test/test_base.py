"""
pygame-obj
https://github.com/ppizarror/pygame-obj

TEST FONT
Test font management.

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

__all__ = ['BaseTest']

import unittest

# noinspection PyProtectedMember
from pygame_menu._base import Base


class BaseTest(unittest.TestCase):

    def test_counter(self) -> None:
        """
        Test counter.
        """
        obj = Base('')
        self.assertEqual(obj.get_counter_attribute('count', 1), 1)
        self.assertEqual(obj.get_counter_attribute('count', 1), 2)
        self.assertEqual(obj.get_counter_attribute('count', 1), 3)
        self.assertEqual(obj.get_counter_attribute('count', 1), 4)
        self.assertEqual(obj.get_counter_attribute('count', 1), 5)
        self.assertEqual(obj.get_counter_attribute('count', 1), 6)

        self.assertAlmostEqual(obj.get_counter_attribute('count_epic', 1, '3.14'), 4.14)
        self.assertAlmostEqual(obj.get_counter_attribute('count_epic', 1, '3.14'), 5.14)
        self.assertAlmostEqual(obj.get_counter_attribute('count_epic', 1, '3.14'), 6.14)

        # Test check instance
        self.assertEqual(obj.get_counter_attribute('count1', 1, '1'), 2)
        self.assertEqual(obj.get_counter_attribute('count1', 1, '1'), 3)

        # Test check instance
        self.assertEqual(obj.get_counter_attribute('count2', 1.0, '1'), 2.0)
        self.assertEqual(obj.get_counter_attribute('count2', 1.0, '1'), 3.0)

    def test_classid(self) -> None:
        """
        Test class id.
        """
        obj = Base('id')
        self.assertEqual(obj.get_class_id(), 'Base<"id">')

    def test_attributes(self) -> None:
        """
        Test attributes.
        """
        obj = Base('')
        self.assertFalse(obj.has_attribute('epic'))
        self.assertRaises(IndexError, lambda: obj.remove_attribute('epic'))
        obj.set_attribute('epic', True)
        self.assertTrue(obj.has_attribute('epic'))
        self.assertTrue(obj.get_attribute('epic'))
        obj.set_attribute('epic', False)
        self.assertFalse(obj.get_attribute('epic'))
        obj.remove_attribute('epic')
        self.assertFalse(obj.has_attribute('epic'))
        self.assertEqual(obj.get_attribute('epic', 420), 420)

    def test_repr(self) -> None:
        """
        Test base repr.
        """
        obj = Base('id')
        self.assertNotIn('["id"]', str(obj))
        obj._id__repr__ = True
        self.assertIn('["id"]', str(obj))
        obj = Base('id2')
        obj._class_id__repr__ = True
        self.assertEqual(str(obj), 'Base<"id2">')
