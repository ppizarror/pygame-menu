"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BASE
Base object. Provides common methods used by all library objects.
"""

__all__ = ['Base']

from pygame_menu.utils import uuid4

from pygame_menu._types import NumberInstance, NumberType
from typing import Any, Optional


class Base:
    """
    Base object.
    """
    _attributes: Optional[dict[str, Any]]
    _class_id__repr__: bool
    _id: str
    _id__repr__: bool
    _verbose: bool

    def __init__(self, object_id: str, verbose: bool = True) -> None:
        """
        Base constructor.

        :param object_id: Object ID
        :param verbose: Enable verbose mode (errors/warnings)
        """
        if not isinstance(object_id, str):
            raise TypeError("object_id must be a string")
        if not isinstance(verbose, bool):
            raise TypeError("verbose must be a bool")

        self._id = object_id if len(object_id) > 0 else uuid4()
        self._attributes = None
        self._class_id__repr__ = False  # If True, repr/str of the object is class id
        self._id__repr__ = False  # If True, repr/str of the object adds object id
        self._verbose = verbose

    def __repr__(self) -> str:
        """
        Repr print of object.

        :return: Object str status
        """
        sup_repr = super().__repr__()

        assert not (self._class_id__repr__ and self._id__repr__), \
            'class id and id __repr__ cannot be True at the same time'

        if self._class_id__repr__:
            return self.get_class_id()

        if self._id__repr__:
            return sup_repr.replace(' object at ', f'["{self.get_id()}"] object at ')

        return sup_repr

    def _update__repr___(self, obj: 'Base') -> None:
        """
        Update __repr__ from other Base object.

        :param obj: External base object to copy from
        """
        self._class_id__repr__ = obj._class_id__repr__
        self._id__repr__ = obj._id__repr__

    def set_attribute(self, key: str, value: Any = None) -> 'Base':
        """
        Set an attribute.

        :param key: Key of the attribute
        :param value: Value of the attribute
        :return: Self reference
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")

        if self._attributes is None:
            self._attributes = {}

        self._attributes[key] = value
        return self

    def get_counter_attribute(self, key: str, incr: Any = 0, default: Any = 0) -> NumberType:
        """
        Get counter attribute.

        :param key: Key of the attribute
        :param incr: Increase value
        :param default: Default value to start with, by default it's zero
        :return: New increased value
        """
        if not isinstance(incr, NumberInstance):
            incr = float(incr)

        if not isinstance(default, NumberInstance):
            if isinstance(incr, float):
                default = float(default)
            else:
                try:
                    default = int(default)
                except ValueError:
                    default = float(default)

        if not self.has_attribute(key):
            value = default + incr
            self.set_attribute(key, value)
            return value

        new_value = self.get_attribute(key) + incr
        self.set_attribute(key, new_value)
        return new_value

    def get_attribute(self, key: str, default: Any = None) -> Any:
        """
        Get an attribute value.

        :param key: Key of the attribute
        :param default: Value if it does not exist
        :return: Attribute data
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")

        if not self.has_attribute(key):
            return default

        return self._attributes[key]

    def has_attribute(self, key: str) -> bool:
        """
        Return ``True`` if the object has the given attribute.

        :param key: Key of the attribute
        :return: ``True`` if exists
        """
        if not isinstance(key, str):
            raise TypeError("key must be a string")

        return self._attributes is not None and key in self._attributes

    def remove_attribute(self, key: str) -> 'Base':
        """
        Removes the given attribute from the object. Throws ``IndexError`` if
        the given key does not exist.

        :param key: Key of the attribute
        :return: Self reference
        """
        if not self.has_attribute(key):
            raise IndexError(f'attribute "{key}" does not exists on object')

        del self._attributes[key]
        return self

    def get_class_id(self) -> str:
        """
        Return the Class+ID as a string.

        :return: Class+ID format
        """
        return f'{self.__class__.__name__}<"{self._id}">'

    def get_id(self) -> str:
        """
        Return the object ID.

        :return: Object ID
        """
        return self._id
