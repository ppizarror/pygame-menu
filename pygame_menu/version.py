"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERSION
Library version.
"""

__all__ = ['Version', 'vernum', 'ver', 'rev']

from typing import Tuple


class Version(tuple):
    """
    Version class.
    """

    __slots__ = ()
    fields = 'major', 'minor', 'patch'

    def __new__(cls, major, minor, patch) -> Tuple:
        return tuple.__new__(cls, (major, minor, patch))

    def __repr__(self) -> str:
        fields = (f'{fld}={val}' for fld, val in zip(self.fields, self))
        return f'{str(self.__class__.__name__)}({", ".join(fields)})'

    def __str__(self) -> str:
        return '{}.{}.{}'.format(*self)

    major = property(lambda self: self[0])
    minor = property(lambda self: self[1])
    patch = property(lambda self: self[2])


vernum = Version(4, 3, 6)
ver = str(vernum)
rev = ''
