"""
pygame-menu
https://github.com/ppizarror/pygame-menu

VERSION
Library version.

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
        fields = ('{}={}'.format(fld, val) for fld, val in zip(self.fields, self))
        return '{}({})'.format(str(self.__class__.__name__), ', '.join(fields))

    def __str__(self) -> str:
        return '{}.{}.{}'.format(*self)

    major = property(lambda self: self[0])
    minor = property(lambda self: self[1])
    patch = property(lambda self: self[2])


vernum = Version(4, 0, 0)
ver = str(vernum)
rev = ''
