"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TYPES
Defines common pygame-menu types.

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

# noinspection PyUnresolvedReferences
from typing import Union, Dict, List, Tuple, Any, Callable, Sequence, Mapping, \
    TYPE_CHECKING

# Common types
ArgsType = Union[Sequence[Any], None]
ColorType = Union[Tuple[int, int, int], Tuple[int, int, int, int]]
KwargsType = Union[Mapping[Any, Any], None]
NumberType = Union[int, float]

# Vectors
Vector2BoolType = Union[Tuple[bool, bool], List[bool]]
Vector2IntType = Union[Tuple[int, int], List[int]]
Vector2FloatType = Union[Tuple[float, float], List[float]]
Vector2NumberType = Union[Tuple[NumberType, NumberType], List[NumberType]]

# Generic length
VectorTupleType = Tuple[NumberType, ...]
VectorListType = List[NumberType]
VectorType = Union[VectorTupleType, VectorListType]
VectorIntType = Union[Tuple[int, ...], List[int]]

# Tuples
Tuple2NumberType = Tuple[NumberType, NumberType]
Tuple2IntType = Tuple[int, int]
Tuple4Tuple2IntType = Tuple[Tuple2IntType, Tuple2IntType, Tuple2IntType, Tuple2IntType]

# Menu constructor types
MenuColumnMaxWidthType = Union[int, float, VectorType, None]
MenuColumnMinWidthType = Union[int, float, VectorType]
MenuRowsType = Union[int, VectorIntType, None]

# Other
PaddingType = Union[NumberType, List[NumberType],
                    Tuple[NumberType, NumberType],
                    Tuple[NumberType, NumberType, NumberType, NumberType],
                    Tuple[NumberType, NumberType, NumberType, NumberType]]
