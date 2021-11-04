"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TYPES
Defines common pygame-menu types.
"""

from pygame.color import Color as __Color
from pygame.event import Event as EventType

from typing import Union, List, Tuple, Any, Callable, Sequence, Mapping, Optional

# noinspection PyUnresolvedReferences
from typing import Dict, Type  # lgtm [py/unused-import]

# noinspection PyUnresolvedReferences
from typing_extensions import Literal  # lgtm [py/unused-import]

# Common types
ArgsType = Optional[Sequence[Any]]
CallableNoArgsType = Callable[[], Any]
CallbackType = Optional[Callable]
EventListType = List[EventType]
EventVectorType = Union[EventListType, Tuple[EventType]]
KwargsType = Optional[Mapping[Any, Any]]
NumberType = Union[int, float]

# Colors
ColorType = Union[Tuple[int, int, int], Tuple[int, int, int, int]]
ColorInputType = Union[ColorType, str, int, __Color]

# Color input gradient; from, to, vertical, forward
ColorInputGradientType = Tuple[ColorInputType, ColorInputType, bool, bool]

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
Tuple2BoolType = Tuple[bool, bool]
Tuple2IntType = Tuple[int, int]
Tuple2NumberType = Tuple[NumberType, NumberType]
Tuple3IntType = Tuple[int, int, int]
Tuple4IntType = Tuple[int, int, int, int]
Tuple4Tuple2IntType = Tuple[Tuple2IntType, Tuple2IntType, Tuple2IntType, Tuple2IntType]
TupleIntType = Tuple[int, ...]

# Menu constructor types
MenuColumnMaxWidthType = Optional[Union[int, float, VectorType]]
MenuColumnMinWidthType = Union[int, float, VectorType]
MenuRowsType = Optional[Union[int, VectorIntType]]

# Other
PaddingType = Optional[Union[NumberType, List[NumberType], Tuple[NumberType],
                             Tuple[NumberType, NumberType],
                             Tuple[NumberType, NumberType, NumberType, NumberType],
                             Tuple[NumberType, NumberType, NumberType, NumberType]]]
StringVector = Union[str, Tuple[str, ...], List[str]]

# Instances
ColorInputInstance = (int, str, tuple, list, __Color)
NumberInstance = (int, float)
PaddingInstance = (int, float, tuple, list, type(None))
VectorInstance = (tuple, list)

# Cursor
try:
    # noinspection PyUnresolvedReferences
    from pygame.cursors import Cursor as __Cursor

    CursorInputType = Optional[Union[int, __Cursor]]
    CursorInputInstance = (int, __Cursor, type(None))

except (AttributeError, ImportError):
    CursorInputType, CursorInputInstance = Optional[int], (int, type(None))
CursorType = CursorInputType
