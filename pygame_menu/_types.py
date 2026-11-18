"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TYPES
Defines common pygame-menu types.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any, Optional, Union

from pygame.color import Color as __Color
from pygame.event import Event as EventType

# Common types
ArgsType = Sequence[Any] | None
CallableNoArgsType = Callable[[], Any]
CallbackType = Callable | None
EventListType = list[EventType]
EventVectorType = EventListType | tuple[EventType]
KwargsType = Mapping[Any, Any] | None
NumberType = int | float

# Colors
ColorType = tuple[int, int, int] | tuple[int, int, int, int]
ColorInputType = ColorType | str | int | __Color

# Color input gradient; from, to, vertical, forward
ColorInputGradientType = tuple[ColorInputType, ColorInputType, bool, bool]

# Vectors
Vector2BoolType = tuple[bool, bool] | list[bool]
Vector2IntType = tuple[int, int] | list[int]
Vector2FloatType = tuple[float, float] | list[float]
Vector2NumberType = tuple[NumberType, NumberType] | list[NumberType]

# Generic length
VectorTupleType = tuple[NumberType, ...]
VectorListType = list[NumberType]
VectorType = VectorTupleType | VectorListType
VectorIntType = tuple[int, ...] | list[int]

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
MenuColumnMaxWidthType = int | float | VectorType | None
MenuColumnMinWidthType = int | float | VectorType | None
MenuRowsType = int | VectorIntType | None

# Other
PaddingType = (
    NumberType
    | list[NumberType]
    | tuple[NumberType]
    | Tuple2NumberType
    | Tuple4NumberType
    | None
)
StringVector = str | tuple[str, ...] | list[str]

# Instances
ColorInputInstance = (int, str, tuple, list, __Color)
NumberInstance = (int, float)
PaddingInstance = (int, float, tuple, list, type(None))
VectorInstance = (tuple, list)

# Cursor
try:
    from pygame.cursors import Cursor as __Cursor  # type: ignore

    CursorInputType = int | __Cursor | None
    CursorInputInstance = (int, __Cursor, type(None))

except (AttributeError, ImportError):
    CursorInputType, CursorInputInstance = int | None, (int, type(None))
CursorType = CursorInputType
