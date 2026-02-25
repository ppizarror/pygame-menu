"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERSION
Library version.
"""

from __future__ import annotations

__all__ = ['Version', 'vernum', 'ver', 'rev']


class Version(tuple):
    """
    Version class.
    """

    __slots__ = ()
    fields = 'major', 'minor', 'patch'

    def __new__(cls, major, minor, patch) -> 'Version':
        return tuple.__new__(cls, (major, minor, patch))  # type: ignore

    def __repr__(self) -> str:
        fields = (f'{fld}={val}' for fld, val in zip(self.fields, self))
        return f'{self.__class__.__name__}({", ".join(fields)})'

    def __str__(self) -> str:
        return ".".join(str(x) for x in self)

    major = property(lambda self: self[0])
    minor = property(lambda self: self[1])
    patch = property(lambda self: self[2])


vernum = Version(4, 5, 5)
ver = str(vernum)
rev = ''
