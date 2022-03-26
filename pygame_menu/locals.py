"""
pygame-menu
https://github.com/ppizarror/pygame-menu

LOCALS
Local constants.
"""

__all__ = [

    # Alignment
    'ALIGN_CENTER',
    'ALIGN_LEFT',
    'ALIGN_RIGHT',

    # Data types
    'INPUT_FLOAT',
    'INPUT_INT',
    'INPUT_TEXT',

    # Positioning
    'POSITION_CENTER',
    'POSITION_EAST',
    'POSITION_NORTH',
    'POSITION_NORTHEAST',
    'POSITION_SOUTHWEST',
    'POSITION_SOUTH',
    'POSITION_SOUTHEAST',
    'POSITION_NORTHWEST',
    'POSITION_WEST',

    # Orientation
    'ORIENTATION_HORIZONTAL',
    'ORIENTATION_VERTICAL',

    # Scrollarea
    'SCROLLAREA_POSITION_BOTH_HORIZONTAL',
    'SCROLLAREA_POSITION_BOTH_VERTICAL',
    'SCROLLAREA_POSITION_FULL',
    'SCROLLAREA_POSITION_NONE',

    # Cursors
    'CURSOR_ARROW',
    'CURSOR_CROSSHAIR',
    'CURSOR_HAND',
    'CURSOR_IBEAM',
    'CURSOR_NO',
    'CURSOR_SIZEALL',
    'CURSOR_SIZENESW',
    'CURSOR_SIZENS',
    'CURSOR_SIZENWSE',
    'CURSOR_SIZEWE',
    'CURSOR_WAIT',
    'CURSOR_WAITARROW',

    # Event compatibility
    'FINGERDOWN',
    'FINGERMOTION',
    'FINGERUP'

]

import pygame as __pygame

# Alignment
ALIGN_CENTER = 'align-center'
ALIGN_LEFT = 'align-left'
ALIGN_RIGHT = 'align-right'

# Input data type
INPUT_FLOAT = 'input-float'
INPUT_INT = 'input-int'
INPUT_TEXT = 'input-text'

# Position
POSITION_CENTER = 'position-center'
POSITION_EAST = 'position-east'
POSITION_NORTH = 'position-north'
POSITION_NORTHEAST = 'position-northeast'
POSITION_NORTHWEST = 'position-northwest'
POSITION_SOUTH = 'position-south'
POSITION_SOUTHEAST = 'position-southeast'
POSITION_SOUTHWEST = 'position-southwest'
POSITION_WEST = 'position-west'

# Menu ScrollArea position
SCROLLAREA_POSITION_BOTH_HORIZONTAL = 'scrollarea-position-both-horizontal'
SCROLLAREA_POSITION_BOTH_VERTICAL = 'scrollarea_position-both-vertical'
SCROLLAREA_POSITION_FULL = 'scrollarea-position-full'
SCROLLAREA_POSITION_NONE = 'scrollarea-position-none'

# Orientation
ORIENTATION_HORIZONTAL = 'orientation-horizontal'
ORIENTATION_VERTICAL = 'orientation-vertical'

# Cursors
CURSOR_ARROW = None if not hasattr(__pygame, 'SYSTEM_CURSOR_ARROW') else __pygame.SYSTEM_CURSOR_ARROW
CURSOR_CROSSHAIR = None if not hasattr(__pygame, 'SYSTEM_CURSOR_CROSSHAIR') else __pygame.SYSTEM_CURSOR_CROSSHAIR
CURSOR_HAND = None if not hasattr(__pygame, 'SYSTEM_CURSOR_HAND') else __pygame.SYSTEM_CURSOR_HAND
CURSOR_IBEAM = None if not hasattr(__pygame, 'SYSTEM_CURSOR_IBEAM') else __pygame.SYSTEM_CURSOR_IBEAM
CURSOR_NO = None if not hasattr(__pygame, 'SYSTEM_CURSOR_NO') else __pygame.SYSTEM_CURSOR_NO
CURSOR_SIZEALL = None if not hasattr(__pygame, 'SYSTEM_CURSOR_SIZEALL') else __pygame.SYSTEM_CURSOR_SIZEALL
CURSOR_SIZENESW = None if not hasattr(__pygame, 'SYSTEM_CURSOR_SIZENESW') else __pygame.SYSTEM_CURSOR_SIZENESW
CURSOR_SIZENS = None if not hasattr(__pygame, 'SYSTEM_CURSOR_SIZENS') else __pygame.SYSTEM_CURSOR_SIZENS
CURSOR_SIZENWSE = None if not hasattr(__pygame, 'SYSTEM_CURSOR_SIZENWSE') else __pygame.SYSTEM_CURSOR_SIZENWSE
CURSOR_SIZEWE = None if not hasattr(__pygame, 'SYSTEM_CURSOR_SIZEWE') else __pygame.SYSTEM_CURSOR_SIZEWE
CURSOR_WAIT = None if not hasattr(__pygame, 'SYSTEM_CURSOR_WAIT') else __pygame.SYSTEM_CURSOR_WAIT
CURSOR_WAITARROW = None if not hasattr(__pygame, 'SYSTEM_CURSOR_WAITARROW') else __pygame.SYSTEM_CURSOR_WAITARROW

# Events compatibility with lower pygame versions
FINGERDOWN = -1 if not hasattr(__pygame, 'FINGERDOWN') else __pygame.FINGERDOWN
FINGERMOTION = -1 if not hasattr(__pygame, 'FINGERMOTION') else __pygame.FINGERMOTION
FINGERUP = -1 if not hasattr(__pygame, 'FINGERUP') else __pygame.FINGERUP
