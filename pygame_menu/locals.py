"""
pygame-menu
https://github.com/ppizarror/pygame-menu

LOCALS
Local constants.
"""

from __future__ import annotations

__all__ = [
    # Alignment
    "ALIGN_CENTER",
    "ALIGN_LEFT",
    "ALIGN_RIGHT",
    # Data types
    "INPUT_FLOAT",
    "INPUT_INT",
    "INPUT_TEXT",
    # Positioning
    "POSITION_CENTER",
    "POSITION_EAST",
    "POSITION_NORTH",
    "POSITION_NORTHEAST",
    "POSITION_SOUTHWEST",
    "POSITION_SOUTH",
    "POSITION_SOUTHEAST",
    "POSITION_NORTHWEST",
    "POSITION_WEST",
    # Orientation
    "ORIENTATION_HORIZONTAL",
    "ORIENTATION_VERTICAL",
    # Scrollarea
    "SCROLLAREA_POSITION_BOTH_HORIZONTAL",
    "SCROLLAREA_POSITION_BOTH_VERTICAL",
    "SCROLLAREA_POSITION_FULL",
    "SCROLLAREA_POSITION_NONE",
    # Cursors
    "CURSOR_ARROW",
    "CURSOR_CROSSHAIR",
    "CURSOR_HAND",
    "CURSOR_IBEAM",
    "CURSOR_NO",
    "CURSOR_SIZEALL",
    "CURSOR_SIZENESW",
    "CURSOR_SIZENS",
    "CURSOR_SIZENWSE",
    "CURSOR_SIZEWE",
    "CURSOR_WAIT",
    "CURSOR_WAITARROW",
    # Event compatibility
    "FINGERDOWN",
    "FINGERMOTION",
    "FINGERUP",
]

import pygame as __pygame

# Alignment
ALIGN_CENTER = "align-center"
ALIGN_LEFT = "align-left"
ALIGN_RIGHT = "align-right"

# Input data type
INPUT_FLOAT = "input-float"
INPUT_INT = "input-int"
INPUT_TEXT = "input-text"

# Position
POSITION_CENTER = "position-center"
POSITION_EAST = "position-east"
POSITION_NORTH = "position-north"
POSITION_NORTHEAST = "position-northeast"
POSITION_NORTHWEST = "position-northwest"
POSITION_SOUTH = "position-south"
POSITION_SOUTHEAST = "position-southeast"
POSITION_SOUTHWEST = "position-southwest"
POSITION_WEST = "position-west"

# Menu ScrollArea position
SCROLLAREA_POSITION_BOTH_HORIZONTAL = "scrollarea-position-both-horizontal"
SCROLLAREA_POSITION_BOTH_VERTICAL = "scrollarea-position-both-vertical"
SCROLLAREA_POSITION_FULL = "scrollarea-position-full"
SCROLLAREA_POSITION_NONE = "scrollarea-position-none"

# Orientation
ORIENTATION_HORIZONTAL = "orientation-horizontal"
ORIENTATION_VERTICAL = "orientation-vertical"

# Cursors
CURSOR_ARROW = getattr(__pygame, "SYSTEM_CURSOR_ARROW", None)
CURSOR_CROSSHAIR = getattr(__pygame, "SYSTEM_CURSOR_CROSSHAIR", None)
CURSOR_HAND = getattr(__pygame, "SYSTEM_CURSOR_HAND", None)
CURSOR_IBEAM = getattr(__pygame, "SYSTEM_CURSOR_IBEAM", None)
CURSOR_NO = getattr(__pygame, "SYSTEM_CURSOR_NO", None)
CURSOR_SIZEALL = getattr(__pygame, "SYSTEM_CURSOR_SIZEALL", None)
CURSOR_SIZENESW = getattr(__pygame, "SYSTEM_CURSOR_SIZENESW", None)
CURSOR_SIZENS = getattr(__pygame, "SYSTEM_CURSOR_SIZENS", None)
CURSOR_SIZENWSE = getattr(__pygame, "SYSTEM_CURSOR_SIZENWSE", None)
CURSOR_SIZEWE = getattr(__pygame, "SYSTEM_CURSOR_SIZEWE", None)
CURSOR_WAIT = getattr(__pygame, "SYSTEM_CURSOR_WAIT", None)
CURSOR_WAITARROW = getattr(__pygame, "SYSTEM_CURSOR_WAITARROW", None)

# Events compatibility with lower pygame versions
FINGERDOWN = getattr(__pygame, "FINGERDOWN", -1)
FINGERMOTION = getattr(__pygame, "FINGERMOTION", -1)
FINGERUP = getattr(__pygame, "FINGERUP", -1)
