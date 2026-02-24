"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TYPES
Defines common pygame-menu types.
"""

from pygame.color import Color as __Color
from pygame.event import Event as EventType

from typing import Union, Any, Optional
from collections.abc import Sequence, Mapping, Callable


# Common types
ArgsType = Optional[Sequence[Any]]
CallableNoArgsType = Callable[[], Any]
CallbackType = Optional[Callable]
EventListType = list[EventType]
EventVectorType = Union[EventListType, tuple[EventType]]
KwargsType = Optional[Mapping[Any, Any]]
NumberType = Union[int, float]

# Colors
ColorType = Union[tuple[int, int, int], tuple[int, int, int, int]]
ColorInputType = Union[ColorType, str, int, __Color]

# Color input gradient; from, to, vertical, forward
ColorInputGradientType = tuple[ColorInputType, ColorInputType, bool, bool]

# Vectors
Vector2BoolType = Union[tuple[bool, bool], list[bool]]
Vector2IntType = Union[tuple[int, int], list[int]]
Vector2FloatType = Union[tuple[float, float], list[float]]
Vector2NumberType = Union[tuple[NumberType, NumberType], list[NumberType]]

# Generic length
VectorTupleType = tuple[NumberType, ...]
VectorListType = list[NumberType]
VectorType = Union[VectorTupleType, VectorListType]
VectorIntType = Union[tuple[int, ...], list[int]]

# Tuples
Tuple2BoolType = tuple[bool, bool]
Tuple2IntType = tuple[int, int]
Tuple2NumberType = tuple[NumberType, NumberType]
Tuple3IntType = tuple[int, int, int]
Tuple4IntType = tuple[int, int, int, int]
Tuple4NumberType = tuple[NumberType, NumberType, NumberType, NumberType]
Tuple4Tuple2IntType = tuple[Tuple2IntType, Tuple2IntType, Tuple2IntType, Tuple2IntType]
TupleIntType = tuple[int, ...]

# Menu constructor types
MenuColumnMaxWidthType = Optional[Union[int, float, VectorType]]
MenuColumnMinWidthType = Union[int, float, VectorType]
MenuRowsType = Optional[Union[int, VectorIntType]]

# Other
PaddingType = Optional[Union[NumberType, list[NumberType], tuple[NumberType], Tuple2NumberType, Tuple4NumberType]]
StringVector = Union[str, tuple[str, ...], list[str]]

# Instances
ColorInputInstance = (int, str, tuple, list, __Color)
NumberInstance = (int, float)
PaddingInstance = (int, float, tuple, list, type(None))
VectorInstance = (tuple, list)

# Cursor
try:
    from pygame.cursors import Cursor as __Cursor  # type: ignore

    CursorInputType = Optional[Union[int, __Cursor]]
    CursorInputInstance = (int, __Cursor, type(None))

except (AttributeError, ImportError):
    CursorInputType, CursorInputInstance = Optional[int], (int, type(None))
CursorType = CursorInputType
