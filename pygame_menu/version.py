"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERSION
Library version.
"""

from __future__ import annotations

__all__ = ["Version", "vernum", "ver", "rev"]


class Version(tuple):
    """
    Version class.
    """

    __slots__ = ()
    fields: tuple[str, str, str] = ("major", "minor", "patch")

    def __new__(cls, major: int, minor: int, patch: int) -> Version:
        if not all(isinstance(x, int) for x in (major, minor, patch)):
            raise TypeError("Version components must be integers")
        return tuple.__new__(cls, (major, minor, patch))  # type: ignore

    def __repr__(self) -> str:
        fields = (f"{fld}={val}" for fld, val in zip(self.fields, self))
        return f"{self.__class__.__name__}({', '.join(fields)})"

    def __str__(self) -> str:
        return ".".join(str(x) for x in self)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return tuple(self) < tuple(other)

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return tuple(self) <= tuple(other)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return tuple(self) > tuple(other)

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return tuple(self) >= tuple(other)

    @property
    def major(self) -> int:
        return self[0]

    @property
    def minor(self) -> int:
        return self[1]

    @property
    def patch(self) -> int:
        return self[2]

    # Parser
    @classmethod
    def parse(cls, s: str) -> Version:
        parts = s.split(".")
        if len(parts) != 3:
            raise ValueError("Version string must be 'major.minor.patch'")
        return cls(*(int(x) for x in parts))


vernum = Version(4, 5, 5)
ver = str(vernum)
rev = ""
