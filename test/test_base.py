"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST BASE
Test base class.
"""

__all__ = ['BaseTest']

from test._utils import BaseTest as _BaseTest

# noinspection PyProtectedMember
from pygame_menu._base import Base


class BaseTest(_BaseTest):

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

    def test_object_id_zero_string(self):
        obj = Base("0")
        self.assertEqual(obj.get_id(), "0")

    def test_object_id_whitespace(self) -> None:
        obj = Base("   ")
        self.assertEqual(obj.get_id(), "   ")

    def test_object_id_type_error(self) -> None:
        with self.assertRaises(TypeError):
            Base(123)

    def test_verbose_type_error(self) -> None:
        with self.assertRaises(TypeError):
            Base("id", verbose="yes")

    def test_repr_conflict(self) -> None:
        obj = Base("id")
        obj._class_id__repr__ = True
        obj._id__repr__ = True
        with self.assertRaises(AssertionError):
            repr(obj)

    def test_repr_default(self) -> None:
        obj = Base("id")
        r = repr(obj)
        self.assertIn("object at", r)
        self.assertNotIn("id", r)

    def test_attribute_overwrite(self) -> None:
        obj = Base("")
        obj.set_attribute("x", 1)
        obj.set_attribute("x", "hello")
        self.assertEqual(obj.get_attribute("x"), "hello")

    def test_get_attribute_no_attributes(self) -> None:
        obj = Base("")
        self.assertEqual(obj.get_attribute("missing", 99), 99)

    def test_attribute_key_type_error(self) -> None:
        obj = Base("")
        with self.assertRaises(TypeError):
            obj.set_attribute(123, "value")

    def test_counter_non_numeric_default(self) -> None:
        obj = Base("")
        with self.assertRaises(ValueError):
            obj.get_counter_attribute("c", 1, "not_a_number")

    def test_counter_non_numeric_incr(self) -> None:
        obj = Base("")
        self.assertEqual(obj.get_counter_attribute("c", "5"), 5.0)

    def test_update_repr_flags(self) -> None:
        a = Base("a")
        b = Base("b")
        b._class_id__repr__ = True
        b._id__repr__ = True
        a._update__repr___(b)
        self.assertTrue(a._class_id__repr__)
        self.assertTrue(a._id__repr__)
