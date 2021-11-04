"""
pygame-menu
https://github.com/ppizarror/pygame-menu

BASE
Base object. Provides common methods used by all library objects.
"""

__all__ = ['Base']

from pygame_menu.utils import uuid4

from pygame_menu._types import Dict, Any, NumberInstance, NumberType, Optional


class Base(object):
    """
    Base object.
    """
    _attributes: Optional[Dict[str, Any]]
    _class_id__repr__: bool
    _id: str
    _id__repr__: bool

    def __init__(self, object_id: str) -> None:
        """
        Base constructor.

        :param object_id: Object ID
        """
        assert isinstance(object_id, str)
        if len(object_id) == 0:
            object_id = uuid4()
        self._attributes = None
        self._class_id__repr__ = False  # If True, repr/str of the object is class id
        self._id = object_id
        self._id__repr__ = False  # If True, repr/str of the object adds object id

    def __repr__(self) -> str:
        """
        Repr print of object.

        :return: Object str status
        """
        sup_repr = super(Base, self).__repr__()
        assert not (self._class_id__repr__ and self._id__repr__), \
            'class id and id __repr__ cannot be True at the same time'
        if self._class_id__repr__:
            return self.get_class_id()
        if self._id__repr__:
            return sup_repr.replace(' object at ',
                                    f'["{self.get_id()}"] object at ')
        return sup_repr

    def _update__repr___(self, obj: 'Base') -> None:
        """
        Update __repr__ from other Base object.

        :param obj: External base object to copy from
        :return: None
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
        assert isinstance(key, str)
        if self._attributes is None:
            self._attributes = {}
        self._attributes[key] = value
        return self

    def get_counter_attribute(self, key: str, incr: Any = 0, default: Any = 0) -> NumberType:
        """
        Get counter attribute.

        :param key: Key of the attribute
        :param incr: Increase value
        :param default: Default vale to start with, by default it's zero
        :return: New increase value
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
            self.set_attribute(key, default + incr)
            return default + incr
        new = self.get_attribute(key) + incr
        self.set_attribute(key, new)
        return new

    def get_attribute(self, key: str, default: Any = None) -> Any:
        """
        Get an attribute value.

        :param key: Key of the attribute
        :param default: Value if does not exists
        :return: Attribute data
        """
        assert isinstance(key, str)
        if not self.has_attribute(key):
            return default
        return self._attributes[key]

    def has_attribute(self, key: str) -> bool:
        """
        Return ``True`` if the object has the given attribute.

        :param key: Key of the attribute
        :return: ``True`` if exists
        """
        assert isinstance(key, str)
        if self._attributes is None:
            return False
        return key in self._attributes.keys()

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
