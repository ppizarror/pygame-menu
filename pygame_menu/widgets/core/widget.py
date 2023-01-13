"""
pygame-menu
https://github.com/ppizarror/pygame-menu

WIDGET
Base class for widgets.
"""

__all__ = [

    # Main class
    'AbstractWidgetManager',
    'Widget',

    # Utils
    'check_widget_mouseleave',

    # Types
    'WidgetBorderPositionType',

    # Global widget mouseover list
    'WIDGET_MOUSEOVER',

    # Others
    'WIDGET_BORDER_POSITION_FULL',
    'WIDGET_BORDER_POSITION_NONE',
    'WIDGET_FULL_BORDER',
    'WIDGET_SHADOW_TYPE_ELLIPSE',
    'WIDGET_SHADOW_TYPE_RECTANGULAR',
    'WidgetTransformationNotImplemented'

]

import random
import time

import pygame
import pygame_menu

from pygame_menu._base import Base
from pygame_menu._decorator import Decorator
from pygame_menu.controls import Controller
from pygame_menu.font import FontType
from pygame_menu.locals import POSITION_NORTHWEST, POSITION_SOUTHWEST, POSITION_WEST, \
    POSITION_EAST, POSITION_NORTHEAST, POSITION_CENTER, POSITION_NORTH, POSITION_SOUTH, \
    POSITION_SOUTHEAST, ALIGN_CENTER
from pygame_menu.sound import Sound
from pygame_menu.utils import make_surface, assert_alignment, assert_color, \
    assert_position, assert_vector, parse_padding, uuid4, \
    mouse_motion_current_mouse_position, PYGAME_V2, set_pygame_cursor, warn, \
    get_cursor, ShadowGenerator
from pygame_menu.widgets.core.selection import Selection

from pygame_menu._types import Optional, ColorType, Tuple2IntType, NumberType, \
    PaddingType, Union, List, Tuple, Any, CallbackType, Dict, Callable, Tuple4IntType, \
    Tuple2BoolType, Tuple3IntType, NumberInstance, ColorInputType, EventType, \
    EventVectorType, EventListType, CursorInputType, CursorType, VectorInstance, \
    Tuple2NumberType, CallableNoArgsType

# This list stores the current widget which requested the mouseover status, and
# the previous widget list which requested the mouseover. Each time the widget
# changes the over status, if leaves all previous widgets that are not hovered
# trigger mouseleave. The format of each item of the list is
# [..., [widget, previous_cursor, [previous_widget, previous_cursor2, [....]
WIDGET_MOUSEOVER: List[Any] = [None, []]

# Stores the top cursor for validation
WIDGET_TOP_CURSOR: List[Any] = [None]
WIDGET_TOP_CURSOR_WARNING = False

WIDGET_BORDER_POSITION_NONE = 'border-none'
WIDGET_BORDER_POSITION_FULL = 'border-position-border-full'
WIDGET_FULL_BORDER = (POSITION_NORTH, POSITION_SOUTH, POSITION_EAST, POSITION_WEST)

# Creates the shadow generator
WIDGET_SHADOW_GENERATOR = ShadowGenerator()
WIDGET_SHADOW_TYPE_ELLIPSE = 'ellipse'
WIDGET_SHADOW_TYPE_RECTANGULAR = 'rectangular'


def check_widget_mouseleave(event: Optional[EventType] = None, force: bool = False) -> None:
    """
    Check if the active widget (WIDGET_MOUSEOVER[0]) is still over, else, execute
    previous list (WIDGET_MOUSEOVER[1]).

    :param event: Mouse motion event. If ``None`` this method creates the event
    :param force: If ``True`` calls all mouse leave without checking if the mouse is still over
    """
    return _check_widget_mouseleave(event, force)


# noinspection PyProtectedMember
def _check_widget_mouseleave(
        event: Optional[EventType] = None,
        force: bool = False,
        recursive: bool = False
) -> None:
    """
    Check if the active widget (WIDGET_MOUSEOVER[0]) is still over, else, execute
    previous list (WIDGET_MOUSEOVER[1]).

    :param event: Mouse motion event. If ``None`` this method creates the event
    :param force: If ``True`` calls all mouse leave without checking if the mouse is still over
    :param recursive: If ``True`` the call is recursive
    """
    # If no widget is over, return
    if WIDGET_MOUSEOVER[0] is None:
        assert len(WIDGET_MOUSEOVER[1]) == 0, 'widget leave sublist must be empty'
        assert WIDGET_TOP_CURSOR[0] is None, 'widget top cursor must be None'
        return

    if event is None:
        event = mouse_motion_current_mouse_position()

    # Check widget is still over
    current: 'Widget' = WIDGET_MOUSEOVER[0]
    current._check_mouseover(event, check_all_widget_mouseleave=False)  # This may change WIDGET_MOUSEOVER

    # If mouse is not visible, forces
    if PYGAME_V2:
        force = force or not pygame.mouse.get_visible()

    # The active widget is not over
    if (not current._mouseover or force) and WIDGET_MOUSEOVER[0] is not None:
        assert len(WIDGET_MOUSEOVER[1]) == 3, 'invalid widget leave sublist length'

        # Unpack list
        prev_widget: 'Widget' = WIDGET_MOUSEOVER[1][0]
        prev_cursor = WIDGET_MOUSEOVER[1][1]
        prev_list: List[Any] = WIDGET_MOUSEOVER[1][2]

        assert WIDGET_MOUSEOVER[0] == prev_widget, \
            'inconsistent widget leave sublist'

        # Set previous cursor
        set_pygame_cursor(prev_cursor)

        # Unpack list
        if len(prev_list) == 0:
            WIDGET_MOUSEOVER[0] = None
            WIDGET_MOUSEOVER[1] = []
            if prev_cursor != WIDGET_TOP_CURSOR[0]:
                if WIDGET_TOP_CURSOR_WARNING and current._verbose:
                    warn(
                        f'expected {WIDGET_TOP_CURSOR[0]} to be the top cursor '
                        f'(WIDGET_TOP_CURSOR), but {prev_cursor} is the current '
                        f'previous cursor from WIDGET_MOUSEOVER recursive list. '
                        f'The top cursor {WIDGET_TOP_CURSOR[0]} will be established '
                        f'as the pygame default mouse cursor'
                    )
                set_pygame_cursor(WIDGET_TOP_CURSOR[0])
            WIDGET_TOP_CURSOR[0] = None
        else:
            assert len(prev_list) == 3, 'invalid widget leave sublist length'
            WIDGET_MOUSEOVER[0] = prev_list[0]
            WIDGET_MOUSEOVER[1] = prev_list

        # Call leave
        prev_widget.mouseleave(event, check_all_widget_mouseleave=False)

        # Recursive call
        _check_widget_mouseleave(event, force, recursive=True)

    # Check sublist
    if len(WIDGET_MOUSEOVER[1]) == 3 and len(WIDGET_MOUSEOVER[1][2]) > 0 and \
            not recursive and not force:
        prev: List[Any] = WIDGET_MOUSEOVER[1][2]  # [widget, cursor, [widget, cursor, [...]]]
        while True:
            if len(prev) == 0:
                break
            widget: 'Widget' = prev[0]
            cursor = prev[1]

            # Check widget is still over
            widget._check_mouseover(event, check_all_widget_mouseleave=False)

            # If not active
            if not widget._mouseover:
                # Update the array
                if len(prev[2]) == 3:
                    prev[0] = prev[2][0]
                    prev[1] = prev[2][1]
                    prev[2] = prev[2][2]

                    # Set previous cursor
                    set_pygame_cursor(cursor)
                else:
                    for _ in range(len(prev)):
                        prev.pop()
                    break
            else:
                prev = prev[2]  # Recursive call


# Types
BackgroundSurfaceType = Optional[List[Union['pygame.Rect', 'pygame.Surface', Optional[Union[ColorType, 'pygame_menu.BaseImage']]]]]
CallbackMouseType = Optional[Union[Callable[['Widget', EventType], Any], CallableNoArgsType]]
CallbackSelectType = Optional[Union[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any], CallableNoArgsType]]
WidgetBorderPositionType = Union[str, List[str], Tuple[str, ...]]
WidgetBorderType = Tuple[ColorType, int, WidgetBorderPositionType, Tuple2IntType]
WidgetShadowType = Dict[str, Union[Optional['pygame.Surface'], Optional['pygame.Rect'], bool, Tuple[str, int, int, int, Tuple3IntType]]]


# noinspection PyProtectedMember
class Widget(Base):
    """
    Widget abstract class.

    .. note::

        Widget cannot be copied or deep-copied.

    :param title: Widget title
    :param widget_id: Widget identifier
    :param onchange: Callback when updating the status of the widget, executed in :py:meth:`pygame_menu.widgets.core.widget.Widget.change`
    :param onreturn: Callback when applying on the widget (return), executed in :py:meth:`pygame_menu.widgets.core.widget.Widget.apply`
    :param onselect: Callback when selecting the widget, executed in :py:meth:`pygame_menu.widgets.core.widget.Widget.set_selected`
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments
    """
    _accept_events: bool
    _alignment: str
    _angle: NumberType
    _args: List[Any]
    _background_color: Optional[Union[ColorType, 'pygame_menu.BaseImage']]
    _background_inflate: Tuple2IntType
    _background_surface: BackgroundSurfaceType
    _border_color: ColorType
    _border_inflate: Tuple2IntType
    _border_position: WidgetBorderPositionType
    _border_width: int
    _check_mouseleave_call_render: bool
    _col_row_index: Tuple3IntType
    _ctrl: 'Controller'
    _cursor: CursorType
    _decorator: 'Decorator'
    _default_value: Any
    _draw_callbacks: Dict[str, Callable[['Widget', 'pygame_menu.Menu'], Any]]
    _events: EventListType
    _flip: Tuple2BoolType
    _floating: bool
    _floating_origin_position: bool
    _font: Optional['pygame.font.Font']
    _font_antialias: bool
    _font_background_color: Optional[ColorType]
    _font_color: ColorType
    _font_name: FontType
    _font_readonly_color: ColorType
    _font_readonly_selected_color: ColorType
    _font_selected_color: ColorType
    _font_shadow: bool
    _font_shadow_color: ColorType
    _font_shadow_offset: NumberType
    _font_shadow_position: str
    _font_shadow_tuple: Tuple2IntType
    _font_size: int
    _frame: Optional['pygame_menu.widgets.Frame']
    _joystick_enabled: bool
    _keyboard_enabled: bool
    _keyboard_ignore_nonphysical: bool
    _kwargs: Dict[Any, Any]
    _last_render_hash: int
    _margin: Tuple2IntType
    _max_height: List[Optional[bool]]
    _max_width: List[Optional[bool]]
    _menu: Optional['pygame_menu.Menu']  # Menu which contains the Widget
    _menu_hook: Optional['pygame_menu.Menu']  # Menu the Widget points to (submenu)
    _mouse_enabled: bool
    _mouseleave_called: bool
    _mouseover: bool  # Check if mouse is over
    _mouseover_called: Optional[bool]  # Check if the mouseover/mouseleave callbacks were called
    _mouseover_check_rect: Callable[[], 'pygame.Rect']
    _onchange: CallbackType
    _onmouseleave: CallbackMouseType
    _onmouseover: CallbackMouseType
    _onreturn: CallbackType
    _onselect: CallbackSelectType
    _padding: Tuple4IntType
    _padding_transform: Tuple4IntType
    _position: Tuple2IntType
    _rect: 'pygame.Rect'
    _rect_size_delta: Tuple2IntType
    _scale: List[Union[bool, NumberType]]
    _scrollarea: Optional['pygame_menu._scrollarea.ScrollArea']  # Parent scrollarea
    _selected: bool
    _selection_effect: 'Selection'
    _selection_effect_draw_post: bool
    _selection_time: NumberType
    _shadow: WidgetShadowType
    _sound: 'Sound'
    _surface: Optional['pygame.Surface']
    _tab_size: int
    _title: str
    _touchscreen_enabled: bool
    _translate: Tuple2IntType  # Translation made by user
    _translate_virtual: Tuple2IntType  # Virtual translation applied by api
    _update_callbacks: Dict[str, Callable[[EventListType, 'Widget', 'pygame_menu.Menu'], Any]]
    _visible: bool
    active: bool
    configured: bool
    force_menu_draw_focus: bool
    is_scrollable: bool
    is_selectable: bool
    last_surface: Optional['pygame.Surface']
    lock_position: bool
    readonly: bool
    selection_expand_background: bool

    def __init__(
            self,
            title: Any = '',
            widget_id: str = '',
            onchange: CallbackType = None,
            onmouseleave: Optional[Callable[['Widget', EventType], Any]] = None,
            onmouseover: Optional[Callable[['Widget', EventType], Any]] = None,
            onreturn: CallbackType = None,
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            args=None,
            kwargs=None
    ) -> None:
        super(Widget, self).__init__(object_id=widget_id)

        self._accept_events = False  # Indicate the widget receives events (info)
        self._alignment = ALIGN_CENTER  # Widget alignment
        self._background_color = None
        self._background_inflate = (0, 0)
        self._background_surface = None
        self._check_mouseleave_call_render = False
        self._col_row_index = (-1, -1, -1)
        self._cursor = None
        self._decorator = Decorator(self)
        self._default_value = _WidgetNoValue()
        self._events = []
        self._frame = None
        self._margin = (0, 0)
        self._max_height = [None, False, True]  # size, width_scale, smooth
        self._max_width = [None, False, True]  # size, height_scale, smooth
        self._mouseleave_called = False
        self._mouseover = False
        self._mouseover_called = None
        self._padding = (0, 0, 0, 0)  # top, right, bottom, left
        self._padding_transform = (0, 0, 0, 0)
        self._position = (0, 0)
        self._scrollarea = None  # Widget scrollarea container
        self._selected = False  # Use select() to modify this status
        self._selection_time = 0
        self._sound = Sound()
        self._tab_size = 0  # Tab spaces
        self._title = str(title)
        self._visible = True  # Use show() or hide() to modify this status

        # If True, the widget don't contribute width/height to the Menu widget
        # positioning computation. Use .set_float() to modify this status
        self._floating = False
        self._floating_origin_position = False

        # Which function is used to get the rect which checks if the widget is
        # active or not
        self._mouseover_check_rect = lambda: self.get_rect(to_real_position=True)

        # Widget transforms
        self._angle = 0  # Rotation angle (degrees)
        self._flip = (False, False)  # x, y
        self._scale = [False, 1, 1, False]  # do_scale, x, y, smooth
        self._scale_factor = (1, 1)  # Transformed/Original in x, y
        self._translate = (0, 0)
        self._translate_virtual = (0, 0)  # Translation virtual used by scrollarea's

        # Widget rect. This object does not contain padding. For getting the
        # widget+padding use .get_rect() widget method instead. Widget subclass
        # should ONLY modify width/height, in rendering and READ position (rect.x,
        # rect.y) in drawing. Position during rendering is not the same as it will
        # have in menu (menu rendering changes widget position). Some widgets like
        # MenuBar are the exception, as its position never changes during menu
        # execution (unless user triggers a change), then widgets like these may
        # access without problems
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._rect_size_delta = (0, 0)  # Size added to rect width/height

        # Callbacks
        self._draw_callbacks = {}
        self._update_callbacks = {}

        self.set_onchange(onchange)
        self.set_onmouseleave(onmouseleave)
        self.set_onmouseover(onmouseover)
        self.set_onreturn(onreturn)
        self.set_onselect(onselect)

        self._args = args or []
        self._kwargs = kwargs or {}

        # Surface of the widget
        self._surface = None

        # Menu reference
        self._menu = None  # Menu which contains the widget
        self._menu_hook = None  # Menu the widget points to. Modified by WidgetManager._add_submenu

        # Modified in set_font() method
        self._font = None
        self._font_antialias = True
        self._font_background_color = None
        self._font_color = (0, 0, 0)
        self._font_name = ''
        self._font_readonly_color = (0, 0, 0)
        self._font_readonly_selected_color = (255, 255, 255)
        self._font_selected_color = (255, 255, 255)
        self._font_size = 0

        # Font shadow
        self._font_shadow = False
        self._font_shadow_color = (0, 0, 0)
        self._font_shadow_offset = 2.0
        self._font_shadow_position = POSITION_NORTHWEST
        self._font_shadow_tuple = (0, 0)  # (x px offset, y px offset)

        # Widget shadow
        self._shadow = {
            'enabled': False,
            'properties': (),
            'rect': None,
            'surface': None
        }

        # Border
        self._border_color = (0, 0, 0)
        self._border_inflate = (0, 0)
        self._border_position = 'none'
        self._border_width = 0

        # Rendering, this variable may be used by render() method. If the hash
        # of the variables change respect to the last render hash (hash computed
        # using self._hash_variables() method) then the widget should render and
        # update the hash
        self._last_render_hash = 0

        # Selection effect, for avoiding exception while getting object rect,
        # NullSelection was created. Initially it was None
        self._selection_effect = pygame_menu.widgets.NoneSelection()
        # If False, the selection effect is drawn previous the widget surface
        self._selection_effect_draw_post = True

        # Inputs
        self._ctrl = Controller()
        self._keyboard_enabled = True
        self._keyboard_ignore_nonphysical = True  # Ignores non-physical keyboard buttons pressed
        self._joystick_enabled = True
        self._mouse_enabled = True  # Accept mouse interaction
        self._touchscreen_enabled = True

        # Public statutes. These values can be changed without calling for
        # methods (safe to update)
        self.active = False  # Widget requests focus if selected
        self.configured = False  # Widget has been configured
        self.force_menu_draw_focus = False  # If True Menu draw focus if widget is selected, don't consider the previous requisites
        self.is_scrollable = False  # Some widgets can be scrolled, such as the Frame
        self.is_selectable = True  # Some widgets cannot be selected like labels
        self.last_surface = None  # Stores the last surface the widget has been drawn
        self.lock_position = False  # If True, the widget don't update the position if .set_position() is executed
        self.readonly = False  # If True, widget ignores all input
        self.receive_menu_update_events = True  # If False, the widget does not receive events from Menu.update(events)
        self.selection_expand_background = False  # If True, the widget background will inflate to match selection margin if selected

    def _ignores_keyboard_nonphysical(self) -> bool:
        """
        Ignores the keyboard non-physical button events.

        :return: True if ignored
        """
        if self._menu is None:
            return self._keyboard_ignore_nonphysical
        return self._keyboard_ignore_nonphysical and self._menu._keyboard_ignore_nonphysical

    def set_onchange(self, onchange: CallbackType) -> 'Widget':
        """
        Set ``onchange`` callback. This method is executed in
        :py:meth:`pygame_menu.widgets.core.widget.Widget.change` method. The
        callback function receives the following arguments:

        .. code-block:: python

            onchange(value, *args, *widget._args, **widget._kwargs)

        :param onchange: Callback executed if the Widget changes its value; it can be a function or None
        :return: Self reference
        """
        if onchange:
            assert callable(onchange), \
                'onchange must be callable (function-type) or None'
        self._onchange = onchange
        return self

    def set_onreturn(self, onreturn: CallbackType) -> 'Widget':
        """
        Set ``onreturn`` callback. This method is executed in
        :py:meth:`pygame_menu.widgets.core.widget.Widget.apply` method. The
        callback function receives the following arguments:

        .. code-block:: python

            onreturn(value, *args, *widget._args, **widget._kwargs)

        :param onreturn: Callback executed if user applies on Widget; it can be a function or None
        :return: Self reference
        """
        if onreturn:
            assert callable(onreturn), \
                'onreturn must be callable (function-type) or None'
        self._onreturn = onreturn
        return self

    def set_onselect(self, onselect: CallbackSelectType) -> 'Widget':
        """
        Set ``onselect`` callback. This method is executed in
        :py:meth:`pygame_menu.widgets.core.widget.Widget.select` method. The
        callback function receives the following arguments:

        .. code-block:: python

            onselect(selected, widget, menu) <or> onselect()

        :param onselect: Callback executed if user selects the Widget; it can be a function or None
        :return: Self reference
        """
        if onselect:
            assert callable(onselect), \
                'onselect must be callable (function-type) or None'
        self._onselect = onselect
        return self

    def set_onmouseover(self, onmouseover: CallbackMouseType) -> 'Widget':
        """
        Set ``onmouseover`` callback. This method is executed in
        :py:meth:`pygame_menu.widgets.core.widget.Widget.mouseover` method. The
        callback function receives the following arguments:

        .. code-block:: python

            onmouseover(widget, event) <or> onmouseover()

        :param onmouseover: Callback executed if user enters the Widget with the mouse; it can be a function or None
        :return: Self reference
        """
        if onmouseover:
            assert callable(onmouseover), \
                'onmouseover must be callable (function-type) or None'
        self._onmouseover = onmouseover
        return self

    def set_onmouseleave(self, onmouseleave: CallbackMouseType) -> 'Widget':
        """
        Set ``onmouseleave`` callback. This method is executed in
        :py:meth:`pygame_menu.widgets.core.widget.Widget.mouseleave` method. The
        callback function receives the following arguments:

        .. code-block:: python

            onmouseleave(widget, event) <or> onmouseleave()

        :param onmouseleave: Callback executed if user leaves the Widget with the mouse; it can be a function or None
        :return: Self reference
        """
        if onmouseleave:
            assert callable(onmouseleave), \
                'onmouseleave must be callable (function-type) or None'
        self._onmouseleave = onmouseleave
        return self

    def mouseover(
            self,
            event: EventType,
            check_all_widget_mouseleave: bool = True
    ) -> 'Widget':
        """
        Run the ``onmouseover`` if the mouse is placed over the Widget. The
        callback receive the Widget object reference and the mouse event:

        .. code-block:: python

            onmouseover(widget, event) <or> onmouseover()

        .. warning::

            This method does not evaluate if the mouse is placed over the Widget.
            Only executes the callback and updates the cursor if enabled.

        :param event: ``MOUSEMOVE`` pygame event
        :param check_all_widget_mouseleave: Check widget leave statutes
        :return: Self reference
        """
        # Check if within frame, and the previous frame has not been called, call it
        if check_all_widget_mouseleave:
            if self._frame is not None and WIDGET_MOUSEOVER[0] != self._frame:
                in_prev = False

                # Check frame not in previous
                prev = WIDGET_MOUSEOVER[1]
                if len(prev) != 0:
                    while True:
                        if len(prev) == 0:
                            break
                        if prev[0] == self._frame:
                            in_prev = True
                            break
                        prev = prev[2]

                if not in_prev:
                    self._frame.mouseover(event, check_all_widget_mouseleave)

        if self._onmouseover is not None:
            if self._mouseover_called is None or not self._mouseover_called:
                try:
                    self._onmouseover(self, event)
                except TypeError:
                    self._onmouseover()
                self._mouseover_called = True
        self._mouseleave_called = False

        # Check previous state
        if check_all_widget_mouseleave:
            check_widget_mouseleave(event)

        # Change cursor
        previous_cursor = get_cursor()  # Previous cursor
        set_pygame_cursor(self._cursor)

        # Update previous state
        if check_all_widget_mouseleave:
            if WIDGET_MOUSEOVER[0] is None:
                WIDGET_TOP_CURSOR[0] = previous_cursor
            WIDGET_MOUSEOVER[0] = self
            WIDGET_MOUSEOVER[1] = [self, previous_cursor, WIDGET_MOUSEOVER[1]]

        return self

    def mouseleave(
            self,
            event: EventType,
            check_all_widget_mouseleave: bool = True
    ) -> 'Widget':
        """
        Run the ``onmouseleave`` callback if the mouse is placed outside the Widget.
        The callback receive the Widget object reference and the mouse event:

        .. code-block:: python

            onmouseleave(widget, event) <or> onmouseleave()

        .. warning::

            This method does not evaluate if the mouse is placed over the Widget.
            Only executes the callback and updates the cursor if enabled.

        :param event: ``MOUSEMOVE`` pygame event
        :param check_all_widget_mouseleave: Check widget leave statutes
        :return: Self reference
        """
        # Check for consistency
        if WIDGET_MOUSEOVER[0] != self or not check_all_widget_mouseleave:
            if self._onmouseleave is not None and self._mouseover_called or self._onmouseover is None:
                if self._onmouseleave and not self._mouseleave_called:
                    try:
                        self._onmouseleave(self, event)
                    except TypeError:
                        self._onmouseleave()
                self._mouseover_called = False
                self._mouseleave_called = True
        if check_all_widget_mouseleave:
            check_widget_mouseleave(event)
        return self

    def _check_mouseover(
            self,
            event: EventType,
            rect: Optional['pygame.Rect'] = None,
            check_all_widget_mouseleave: bool = True
    ) -> bool:
        """
        Check the mouse is over the widget. If so, execute the methods.

        :param event: Mouse event (``MOUSEMOTION`` or ``ACTIVEEVENT``)
        :param rect: Rect object. If ``None`` uses the widget rect in real position
        :param check_all_widget_mouseleave: Check widget leave statutes
        :return: ``True`` if the mouseover status changed
        """
        if not hasattr(event, 'type') or event.type not in (pygame.MOUSEMOTION, pygame.ACTIVEEVENT):
            return False

        # If mouse out from window
        if event.type == pygame.ACTIVEEVENT and hasattr(event, 'gain'):
            if event.gain == 1:
                return False
            else:  # Mouse out from window
                check_widget_mouseleave(force=True)
                return True

        if rect is None:
            rect = self._mouseover_check_rect()
        updated = False

        # Check if menu is active
        menu_enabled = True if self._menu is None else self._menu.is_enabled()

        # Check if mouse is over the widget, the widget must be visible
        if self.is_visible() and \
                self._mouse_enabled and \
                hasattr(event, 'pos') and rect.collidepoint(*event.pos) and \
                menu_enabled:
            if not self._mouseover:
                self._mouseover = True
                self.mouseover(event, check_all_widget_mouseleave)
                updated = True

        else:
            if self._mouseover:
                self._mouseover = False
                self.mouseleave(event, check_all_widget_mouseleave)
                updated = True

        if updated and self._check_mouseleave_call_render:
            self._render()

        return updated

    def set_cursor(self, cursor: CursorInputType) -> 'Widget':
        """
        Set the Widget cursor if user places the mouse over the Widget.

        :param cursor: Pygame cursor
        :return: Self reference
        """
        self._cursor = cursor
        return self

    def get_sound(self) -> 'Sound':
        """
        Return the Widget sound engine.

        :return: Sound API
        """
        return self._sound

    def is_selected(self) -> bool:
        """
        Return ``True`` if the Widget is selected.

        :return: Selected status
        """
        return self._selected

    def on_remove_from_menu(self) -> 'Widget':
        """
        Function executed if the Widget is removed from the Menu.

        :return: Self reference
        """
        return self

    def is_visible(self, check_frame: bool = True) -> bool:
        """
        Return ``True`` if the Widget is visible.

        :param check_frame: If ``True`` check frame and sub-frames if they're opened as well
        :return: Visible status
        """
        if not check_frame:
            return self._visible
        if not self._visible:
            return False
        frame = self._frame
        if frame is not None:
            while True:
                if frame is None:
                    break
                if not frame._visible:
                    return False
                frame = frame._frame
        return True

    def is_floating(self) -> bool:
        """
        Return ``True`` if the Widget is floating.

        :return: Float status
        """
        return self._floating

    def __copy__(self) -> 'pygame_menu.Menu':
        """
        Copy method.

        :return: Raises copy exception
        """
        raise _WidgetCopyException('Widget class cannot be copied')

    def __deepcopy__(self, memodict: Dict) -> 'pygame_menu.Menu':
        """
        Deep-copy method.

        :param memodict: Memo dict
        :return: Raises copy exception
        """
        raise _WidgetCopyException('Widget class cannot be deep-copied')

    def _force_render(self) -> Optional[bool]:
        """
        Forces Widget render.

        .. note::

            If this method is used it's not necessary to call Widget methods
            :py:meth:`pygame_menu.widgets.core.widget.Widget.force_menu_surface_update` and
            :py:meth:`pygame_menu.widgets.core.widget.Widget.force_menu_surface_cache_update`.
            As `render` should force Menu render, updating both surface and cache.

        :return: Render return value
        """
        self._last_render_hash = 0
        return self._render()

    def force_menu_surface_update(self) -> 'Widget':
        """
        Forces menu surface update after next rendering call.
        This method automatically updates widget decoration cache as Menu render
        forces it to re-render.

        This method also should be aclled by each widget after render.

        .. note::

            This method is expensive, as menu surface update forces re-rendering
            of all widgets (because them can change in size, position, etc...).

        :return: Self reference
        """
        if self._menu is not None:
            # Don't set _menu._widgets_surface to None because if so
            # in the drawing process it may destroy the surface and raising
            # an Error. The usage of _widgets_surface_need_update is only on
            # Menu _render()
            self._menu._widgets_surface_need_update = True
        self._shadow['surface'] = None
        return self

    def force_menu_surface_cache_update(self) -> 'Widget':
        """
        Forces menu surface cache to update after next drawing call. This also
        updates widget decoration.

        .. note::

            This method only updates the surface cache, without forcing re-rendering
            of all Menu widgets as
            :py:meth:`pygame_menu.widgets.core.widget.Widget.force_menu_surface_update`
            does.

        :return: Self reference
        """
        if self._menu is not None:
            # Menu _widget_surface_cache_need_update property is only accessed on
            # draw method. This does not set _menu._widgets_surface to None
            self._menu._widget_surface_cache_need_update = True
            self._decorator.force_cache_update()
        return self

    def render(self) -> Optional[bool]:
        """
        Public rendering method.

        .. note::

            Unlike private ``_render`` method, public method forces widget rendering
            (calling :py:meth:`pygame_menu.widgets.core.widget.Widget._force_render`).
            Use this method only if the widget has changed the state. Running this
            function many times may affect the performance.

        .. note::

            Before rendering, check out if the widget font/title/values are
            set. If not, it is probable that a zero-size surface is set.

        :return: ``True`` if widget has rendered a new state, ``None`` if the widget has not changed, so render used a cache
        """
        return self._force_render()

    def _render(self) -> Optional[bool]:
        """
        Render the Widget surface.

        This method shall update the attribute ``_surface`` with a :py:class:`pygame.Surface`
        object representing the outer borders of the widget.

        .. note::

            Before rendering, check out if the widget font/title/values are
            set. If not, it is probable that a zero-size surface is set.

        .. note::

            Render methods should call
            :py:meth:`pygame_menu.widgets.core.widget.Widget.force_menu_surface_update`
            to force Menu to update the drawing surface.

        :return: ``True`` if widget has rendered a new state, ``None`` if the widget has not changed, so render used a cache
        """
        raise NotImplementedError('override is mandatory')

    @staticmethod
    def _hash_variables(*args) -> int:
        """
        Compute hash from a series of variables.

        :param args: Variables to compute hash
        :return: Hash data
        """
        h = hash(args)
        if h == 0:  # Menu considers 0 as un-rendered status
            h = random.randrange(-100000, 100000)
        return h

    def _render_hash_changed(self, *args) -> bool:
        """
        This method checks if the widget must render because the inner variables
        changed. This method should include all the variables used by the render
        method, for example, visibility, selected, etc.

        :param args: Variables to check the hash
        :return: ``True`` if render has changed the widget
        """
        _hash = self._hash_variables(*args)
        if _hash != self._last_render_hash or self._last_render_hash == 0:
            self._last_render_hash = _hash
            return True
        return False

    def set_title(self, title: str) -> 'Widget':
        """
        Update the Widget title.

        .. note::

            Not all widgets implements this method, for example, images don't
            accept a title.

        :param title: New title
        :return: Self reference
        """
        self._title = str(title)
        self._apply_font()
        self._force_render()
        return self

    def get_title(self) -> str:
        """
        Return the Widget title.

        .. note::

            Not all widgets implements this method, for example, images don't
            accept a title, and such widget would return an empty string if this
            method is called.

        :return: Widget title
        """
        return self._title

    def set_background_color(
            self,
            color: Optional[Union[ColorInputType, 'pygame_menu.BaseImage']],
            inflate: Optional[Tuple2IntType] = (0, 0)
    ) -> 'Widget':
        """
        Set the Widget background color.

        :param color: Widget background color
        :param inflate: Inflate background on x-axis and y-axis (x, y). If ``None``, the widget value is not updated
        :return: Self reference
        """
        if color is not None:
            if isinstance(color, pygame_menu.BaseImage):
                assert color.get_drawing_mode() == pygame_menu.baseimage.IMAGE_MODE_FILL, \
                    'currently widget only supports IMAGE_MODE_FILL drawing mode'
            else:
                color = assert_color(color)
        if inflate is None:
            inflate = self._background_inflate
        assert_vector(inflate, 2, int)
        assert inflate[0] >= 0 and inflate[1] >= 0, \
            'widget background inflate must be equal or greater than zero in both axis'

        self._background_color = color
        self._background_inflate = tuple(inflate)
        self._background_surface = None
        self._force_render()
        return self

    def background_inflate_to_selection_effect(self) -> 'Widget':
        """
        Expand the Widget background inflate to match the selection effect
        (the Widget don't require to be selected).

        This is a permanent change; for dynamic purposes, depending on if the widget
        is selected or not, setting ``widget.selection_expand_background`` to
        ``True`` may help.

        .. note::

            This method may have unexpected results with certain selection effects.

        :return: Self reference
        """
        self._background_inflate = self._selection_effect.get_xy_margin()
        self._background_surface = None
        return self

    def _get_background_inflate(self) -> Tuple[int, int]:
        """
        Returns the background inflate.

        :return: Background inflte
        """
        if not (self.selection_expand_background and self._selected):
            inflate = self._background_inflate
        else:
            inflate = self._selection_effect.get_xy_margin()
        return inflate

    def _draw_background_color(
            self,
            surface: 'pygame.Surface',
            rect: Optional['pygame.Rect'] = None
    ) -> None:
        """
        Fill a surface with the widget background color.

        :param surface: Surface to fill
        :param rect: If given, use that rect instead of widget rect
        """
        bg = self._background_color
        if self.is_selected() and self._selection_effect.get_background_color():
            bg = self._selection_effect.get_background_color()

        if bg is None:
            return
        if rect is None:
            rect = self.get_rect(inflate=self._get_background_inflate())

        # Create the background surface if none, if the rect changed, or if the background color changed
        if self._background_surface is None or self._background_surface[0] != rect or \
                self._background_surface[2] != bg:
            background_surface = make_surface(rect.width, rect.height, alpha=True)
            if isinstance(bg, pygame_menu.BaseImage):
                bg.draw(
                    surface=background_surface,
                    area=background_surface.get_rect(),
                    position=(0, 0)
                )
            else:
                background_surface.fill(bg, background_surface.get_rect())
            if self._background_surface is None:
                self._background_surface = [rect, background_surface, bg]
            else:
                self._background_surface[0] = rect
                self._background_surface[1] = background_surface
                self._background_surface[2] = bg

        # Draw the background surface
        surface.blit(self._background_surface[1], rect)

    def _readonly_check_mouseover(self, events: EventListType, rect: Optional['pygame.Rect'] = None) -> None:
        """
        Check mouseover if readonly.

        :param events: Event list
        :param rect: Rect object
        """
        if self.readonly:
            for event in events:
                if self._check_mouseover(event, rect):
                    return

    def get_border(self) -> WidgetBorderType:
        """
        Return the widget border properties.

        :return: Color, width, position, and inflate
        """
        return self._border_color, self._border_width, \
            self._border_position, self._border_inflate

    def _draw_border(self, surface: 'pygame.Surface') -> None:
        """
        Draw Widget border in the surface.

        :param surface: Surface to draw the border
        """
        if self._border_width == 0 or self._border_color is None:
            return
        rect = self.get_rect(
            inflate=(self._border_inflate[0] + self._background_inflate[0],
                     self._border_inflate[1] + self._background_inflate[1]))

        if self._border_position == WIDGET_BORDER_POSITION_NONE:
            return

        elif self._border_position == WIDGET_BORDER_POSITION_FULL:
            pygame.draw.rect(
                surface,
                self._border_color,
                rect,
                self._border_width
            )

        else:
            for pos in self._border_position:
                if pos == POSITION_NORTH:
                    start, end = rect.topleft, rect.topright
                elif pos == POSITION_SOUTH:
                    start, end = rect.bottomleft, rect.bottomright
                elif pos == POSITION_EAST:
                    start, end = rect.topright, rect.bottomright
                elif pos == POSITION_WEST:
                    start, end = rect.topleft, rect.bottomleft
                else:
                    raise RuntimeError('invalid border position')
                pygame.draw.line(
                    surface,
                    self._border_color,
                    start,
                    end,
                    self._border_width
                )

    def set_border(
            self,
            width: int,
            color: Optional[ColorInputType],
            inflate: Tuple2IntType = (0, 0),
            position: WidgetBorderPositionType = WIDGET_FULL_BORDER
    ) -> 'Widget':
        """
        Set the Widget border.

        .. note::

            Inflate is added to the background inflate in drawing time.

        :param width: Border width in px
        :param color: Border color
        :param inflate: Inflate on x-axis and y-axis (x, y) in px
        :param position: Border position. Valid only: north, south, east, and west. See :py:mod:`pygame_menu.locals`
        :return: Self reference
        """
        assert isinstance(width, int) and width >= 0
        if color is not None:
            color = assert_color(color)
        assert_vector(inflate, 2, int)
        assert inflate[0] >= 0 and inflate[1] >= 0

        # Check position
        assert isinstance(position, (str, VectorInstance))
        if isinstance(position, str):
            position = [position]

        # Check positioning
        if POSITION_WEST in position and POSITION_SOUTH in position and \
                POSITION_NORTH in position and POSITION_EAST in position:
            position = WIDGET_BORDER_POSITION_FULL

        else:
            for pos in position:
                assert pos in (POSITION_NORTH, POSITION_SOUTH, POSITION_EAST, POSITION_WEST), \
                    f'only north, south, east, and west positions are valid, ' \
                    f'but received "{pos}"'

        if width == 0:
            position = WIDGET_BORDER_POSITION_NONE

        self._border_width = width
        self._border_color = color
        self._border_inflate = inflate
        self._border_position = position

        return self

    def get_selection_effect(self) -> 'Selection':
        """
        Return the selection effect.

        .. note::

            If no selection has been provided, ``_WidgetNullSelection`` class
            will be returned.

        .. note::

            For drawing, use
            :py:meth:`pygame_menu.widgets.core.widget.Widget.draw_selection_effect`.

        .. warning::

            Use with caution.

        :return: Selection effect
        """
        return self._selection_effect

    def set_selection_effect(self, selection: Optional['Selection'] = None) -> 'Widget':
        """
        Set the selection effect handler.

        .. note::

            If ``selection=None`` the selection effect will be established to
            ``_WidgetNullSelection`` class.

        :param selection: Selection effect class
        :return: Self reference
        """
        assert isinstance(selection, (Selection, type(None)))
        if selection is None:
            selection = pygame_menu.widgets.NoneSelection()
        self._selection_effect = selection
        self._force_render()
        return self

    def apply(self, *args) -> Any:
        """
        Run ``onreturn`` callback when return event. The callback function receives
        the following arguments:

        .. code-block:: python

            onreturn(value, *args, *widget._args, **widget._kwargs)

        Where
            - ``value`` if something is returned by :py:meth:`pygame_menu.widgets.core.widget.Widget.get_value`
            - ``args`` given to this method
            - ``args`` of the widget
            - ``kwargs`` of the widget

        .. note::

            Not all widgets have an ``onreturn`` method.

        :param args: Extra arguments passed to the callback
        :return: Callback return value
        """
        self.scroll_to_widget(scroll_parent=False)
        if self.readonly:
            return
        if self._onreturn:
            args = list(args) + list(self._args)
            try:
                args.insert(0, self.get_value())
            except ValueError:
                pass
            return self._onreturn(*args, **self._kwargs)

    def change(self, *args) -> Any:
        """
        Run ``onchange`` callback after change event is triggered. The callback
        function receives the following arguments:

        .. code-block:: python

            onchange(value, *args, *widget._args, **widget._kwargs)

        Where
            - ``value`` if something is returned by :py:meth:`pygame_menu.widgets.core.widget.Widget.get_value`
            - ``args`` given to this method
            - ``args`` of the widget
            - ``kwargs`` of the widget

        .. note::

            Not all widgets have an ``onchange`` method.

        :param args: Extra arguments passed to the callback
        :return: Callback return value
        """
        val = None
        self.scroll_to_widget(scroll_parent=False)
        if self.readonly:
            return val
        if self._onchange:
            args = list(args) + list(self._args)
            try:
                args.insert(0, self.get_value())
            except ValueError:
                pass
            val = self._onchange(*args, **self._kwargs)
        if self._menu is not None and self._menu._onwidgetchange is not None:
            self._menu._onwidgetchange(self._menu, self)
        return val

    def value_changed(self) -> bool:
        """
        Return ``True`` if the Widget's value changed from the default value.

        :return: ``True`` if changed
        """
        try:
            return self.get_value() != self._default_value
        except ValueError:
            return False

    def _draw_shadow(
            self,
            surface: 'pygame.Surface', rect: Optional['pygame.Rect'] = None
    ) -> None:
        """
        Draw the widget shadow.

        :param surface: Surface to draw the shadow
        :param rect: Which rect use to compute surfaces
        """
        if self._shadow['enabled']:
            if not rect:
                rect = self.get_rect(inflate=self._get_background_inflate())
            if not self._shadow['surface'] or self._shadow['rect'] != rect:
                shadow_type, shadow_width, corner_radius, aa_amount, color = self._shadow['properties']
                s: 'pygame.Surface'
                w, h = rect.width + 2 * shadow_width, rect.height + 2 * shadow_width
                if shadow_type == WIDGET_SHADOW_TYPE_RECTANGULAR:
                    s = WIDGET_SHADOW_GENERATOR.create_new_rectangle_shadow(
                        width=w,
                        height=h,
                        shadow_width_param=shadow_width,
                        corner_radius_param=corner_radius,
                        aa_amount=aa_amount,
                        color=color
                    )
                else:
                    s = WIDGET_SHADOW_GENERATOR.create_new_ellipse_shadow(
                        width=w,
                        height=h,
                        shadow_width_param=shadow_width,
                        aa_amount=aa_amount,
                        color=color
                    )
                WIDGET_SHADOW_GENERATOR.clear_short_term_caches()
                self._shadow['surface'] = s
            if not self._shadow['surface']:
                if self._verbose:
                    warn(f'{self.get_class_id()} shadow computation failed, check if'
                         f' the radius is smaller than the width and height of the menu')
                self._shadow['enabled'] = False
                return
            w = self._shadow['properties'][1]
            surface.blit(self._shadow['surface'], (rect.x - w, rect.y - w))

    def draw(self, surface: 'pygame.Surface') -> 'Widget':
        """
        Draw the Widget on a given surface.

        .. note:: Widget drawing order:

            1. Background color
            2. ``prev`` decorator
            3. Widget selection effect (if prev)
            4. Widget surface
            5. Widget selection effect (if post)
            6. Widget border
            7. ``post`` decorator

        :param surface: Surface to draw
        :return: Self reference
        """
        if not self.is_visible():
            return self

        # Check for consistency
        if self.active and not self._selected:
            self.active = False

        # Force rendering
        self._render()

        if self.is_selected() and not self._selection_effect_draw_post:
            self._selection_effect.draw(surface, self)

        self._draw_shadow(surface)
        self._draw_background_color(surface)
        self._decorator.draw_prev(surface)
        self._draw(surface)
        self._draw_border(surface)
        self._decorator.draw_post(surface)

        # Apply callbacks
        self.apply_draw_callbacks()

        # Store last surface
        self.last_surface = surface

        return self

    def draw_after_if_selected(self, surface: Optional['pygame.Surface']) -> 'Widget':
        """
        Draw Widget if selected after all widgets have been drawn. This method
        should also update ``last_surface``; see
        :py:class:`pygame_menu.widgets.DropSelect` widget example or
        :py:class:`pygame_menu.widgets.RangeSlider`.

        :param surface: Surface to draw. ``None`` if frame is requesting the draw, as some widgets are drawn outside the frame surface
        :return: Self reference
        """
        if self.is_selected() and self._selection_effect_draw_post:
            self._selection_effect.draw(surface, self)
        return self

    def _draw(self, surface: 'pygame.Surface') -> None:
        """
        Draw the Widget on a given surface. This method must be overridden by all
        classes.

        :param surface: Surface to draw
        """
        raise NotImplementedError('override is mandatory')

    def get_margin(self) -> Tuple2IntType:
        """
        Return the Widget margin.

        :return: Widget margin (left, bottom)
        """
        return self._margin

    def set_margin(self, x: NumberType, y: NumberType) -> 'Widget':
        """
        Set the Widget margin (left, bottom).

        :param x: Margin on x-axis (left)
        :param y: Margin on y-axis (bottom)
        :return: Self reference
        """
        assert isinstance(x, NumberInstance)
        assert isinstance(y, NumberInstance)
        self._margin = (int(x), int(y))
        self._force_render()
        return self

    def get_padding(self, transformed: bool = True) -> Tuple:
        """
        Return the Widget padding.

        :param transformed: If ``True``, returns the scaled padding if widget is transformed (flip, scale)
        :return: Widget padding (top, right, bottom, left)
        """
        if transformed:
            return self._padding_transform
        return self._padding

    def set_padding(self, padding: PaddingType) -> 'Widget':
        """
        Set the Widget padding according to CSS rules:

        - If an integer or float is provided: top, right, bottom and left values will be the same
        - If 2-item tuple is provided: top and bottom takes the first value, left and right the second
        - If 3-item tuple is provided: top will take the first value, left and right the second, and bottom the third
        - If 4-item tuple is provided: padding will be (top, right, bottom, left)

        .. note::

            See `CSS W3Schools <https://www.w3schools.com/css/css_padding.asp>`_ for more info about padding.

        :param padding: Can be a single number, or a tuple of 2, 3 or 4 elements following CSS style
        :return: Self reference
        """
        self._padding = parse_padding(padding)
        self._padding_transform = self._padding
        self._force_render()
        return self

    def set_scrollarea(self, scrollarea: Optional['pygame_menu._scrollarea.ScrollArea']) -> None:
        """
        Set scrollarea reference. Mostly used for events.

        :param scrollarea: Scrollarea object
        """
        assert isinstance(scrollarea, (type(None), pygame_menu._scrollarea.ScrollArea))
        self._scrollarea = scrollarea

    def get_scrollarea(self) -> 'pygame_menu._scrollarea.ScrollArea':
        """
        Return the scrollarea object.

        :return: ScrollArea object
        """
        return self._scrollarea

    def scroll_to_widget(self, margin: Tuple2NumberType = (0, 0), scroll_parent: bool = True) -> 'Widget':
        """
        The container ScrollArea scrolls to the Widget.

        :param margin: Extra margin around the rect in px on x-axis and y-axis
        :param scroll_parent: If ``True`` parent scroll also scrolls to widget
        :return: Self reference
        """
        if self.has_attribute('ignore_scroll_to_widget'):
            return self
        if self._frame is not None and self._frame.is_scrollable and \
                self._frame.get_scrollarea() is not None:
            self._frame.get_scrollarea().scroll_to_rect(self.get_frame().get_rect(), margin, scroll_parent)
        if self._scrollarea is not None:
            rect = self.get_rect()
            # rect.y += self._border_width
            self._scrollarea.scroll_to_rect(rect, margin, scroll_parent)
        return self

    def get_focus_rect(self) -> 'pygame.Rect':
        """
        Return rect to be used in Widget focus.

        :return: Focus rect
        """
        return self.get_rect(to_real_position=True)

    def get_rect(
            self,
            inflate: Optional[Tuple2IntType] = None,
            apply_padding: bool = True,
            use_transformed_padding: bool = True,
            to_real_position: bool = False,
            to_absolute_position: bool = False,
            render: bool = False,
            real_position_visible: bool = True
    ) -> 'pygame.Rect':
        """
        Return the :py:class:`pygame.Rect` object of the Widget. This method
        forces rendering.

        :param inflate: Inflate rect on x-axis and y-axis (x, y) in px
        :param apply_padding: Apply widget padding
        :param use_transformed_padding: Use scaled padding if the widget is scaled
        :param to_real_position: Transform the widget rect to real coordinates (if the Widget change the position if scrollbars move offsets). Used by events
        :param to_absolute_position: Transform the widget rect to absolute coordinates (if the Widget does not change the position if scrollbars move offsets). Used by events
        :param render: Force widget rendering
        :param real_position_visible: Return only the visible width/height if ``to_real_position=True``
        :return: Widget rect object
        """
        if render:
            self._render()

        # Padding + inflate
        if inflate is None:
            inflate = (0, 0)

        padding = self.get_padding(transformed=use_transformed_padding)  # top,right,bottom,left
        pad_top = padding[0] * apply_padding + inflate[1] / 2
        pad_right = padding[1] * apply_padding + inflate[0] / 2
        pad_bottom = padding[2] * apply_padding + inflate[1] / 2
        pad_left = padding[3] * apply_padding + inflate[0] / 2

        rect = pygame.Rect(int(self._rect.x - pad_left),
                           int(self._rect.y - pad_top),
                           int(self._rect.width + pad_left + pad_right + self._rect_size_delta[0]),
                           int(self._rect.height + pad_bottom + pad_top + self._rect_size_delta[1]))

        if self._scrollarea is not None:
            assert not (to_real_position and to_absolute_position), \
                'real and absolute positions cannot be True at the same time'
            if to_real_position:
                rect = self._scrollarea.to_real_position(rect, visible=real_position_visible)
            elif to_absolute_position:
                rect = self._scrollarea.to_absolute_position(rect)

        return rect

    def get_value(self) -> Any:
        """
        Return the Widget value. If exception ``ValueError`` is raised, no value
        will be passed to the callbacks.

        .. warning::

            Not all widgets return a value.

        :return: Widget data value
        """
        raise ValueError(f'{self.get_class_id()} does not accept value')

    def add_self_to_kwargs(self, key: str = 'widget') -> 'Widget':
        """
        Adds the Widget object to kwargs, it helps to get the Widget reference for
        callbacks. It raises ``KeyError`` if key is duplicated.

        :param key: Name of the parameter
        :return: Self reference
        """
        assert isinstance(key, str)
        if key in self._kwargs.keys():
            raise KeyError('duplicated key')
        self._kwargs[key] = self
        return self

    def _apply_transforms(self) -> None:
        """
        Apply surface transforms: angle, flip and scaling. Translation is applied
        on Widget positioning.
        """
        if self._angle != 0:
            self._surface = pygame.transform.rotate(self._surface, self._angle)

        if self._flip[0] or self._flip[1]:
            self._surface = pygame.transform.flip(self._surface, self._flip[0], self._flip[1])

        self._padding_transform = self._padding  # Reset pad scaling

        # Get width/height
        width, height = self._surface.get_size()
        width_pad, height_pad = width + self._padding[1] + self._padding[3], \
                                height + self._padding[0] + self._padding[2]

        new_size, smooth = None, None

        # Compute scale factor
        if self._max_width[0] is None and self._max_height[0] is None:
            if self._scale[0] and (self._scale[1] != 1 or self._scale[2] != 1):
                w = self._scale[1]
                h = self._scale[2]
                new_size = int(w * width), int(h * height)
                smooth = self._scale[3]

        elif self._max_width[0] is not None:
            if width_pad > self._max_width[0]:
                w = width * self._max_width[0] / width_pad
                if self._max_width[1]:  # If scale height
                    height *= self._max_width[0] / width_pad
                new_size = int(w), int(height)
                smooth = self._max_width[2]

        elif self._max_height[0] is not None:
            if height_pad > self._max_height[0]:
                h = height * self._max_height[0] / height_pad
                if self._max_height[1]:  # If scale width
                    width *= self._max_height[0] / height_pad
                new_size = int(width), int(h)
                smooth = self._max_height[2]

        else:
            raise RuntimeError('max_width and max_height cannot be non-None at '
                               'the same time')

        # Apply scaling
        self._scale_factor = (1, 1)
        if new_size is not None and smooth is not None and width > 0 and height > 0:
            # Apply surface transformation
            if smooth and self._surface.get_bitsize() >= 24:
                self._surface = pygame.transform.smoothscale(self._surface, new_size)
            else:
                self._surface = pygame.transform.scale(self._surface, new_size)

            self._scale_factor = new_size[0] / width, new_size[1] / height

            # Scale pad
            w, h = new_size
            pad_width = w / width
            pad_height = h / height

            # (top,right,bottom,left)
            self._padding_transform = (int(self._padding[0] * pad_height),
                                       int(self._padding[1] * pad_width),
                                       int(self._padding[2] * pad_height),
                                       int(self._padding[3] * pad_width))

    def _font_render_string(
            self,
            text: str,
            color: ColorInputType = (0, 0, 0),
            use_background_color: bool = True
    ) -> 'pygame.Surface':
        """
        Render text. If the font is not defined returns a zero-width surface.

        :param text: Text to render
        :param color: Text color
        :param use_background_color: Use default background color
        :return: Text surface
        """
        assert isinstance(text, str)
        assert isinstance(use_background_color, bool), \
            'use_background_color must be boolean'
        color = assert_color(color)
        bgcolor = self._font_background_color

        # Disable
        if not use_background_color:
            bgcolor = None

        if self._font is None:
            return make_surface(0, 0)

        # Replace tabs
        text = text.replace('\t', ' ' * self._tab_size)

        surface = self._font.render(text, self._font_antialias, color, bgcolor)
        return surface

    def _render_string(self, string: str, color: ColorInputType) -> 'pygame.Surface':
        """
        Render text and turn it into a surface.

        :param string: Text to render
        :param color: Text color
        :return: Text surface
        """
        text = self._font_render_string(string, color)

        # Create surface
        surface = make_surface(
            width=text.get_width(),
            height=text.get_height(),
            alpha=True
        )

        # Draw shadow first
        if self._font_shadow:
            text_bg = self._font_render_string(string, self._font_shadow_color)
            surface.blit(text_bg, self._font_shadow_tuple)

        surface.blit(text, (0, 0))
        return surface

    def shadow(
            self,
            shadow_type: str = WIDGET_SHADOW_TYPE_RECTANGULAR,
            shadow_width: int = 10,
            corner_radius: int = 0,
            color: ColorInputType = (0, 0, 0),
            aa_amount: int = 4
    ) -> 'Widget':
        """
        Configure the widget shadow.

        :param shadow_type: Shadow type, it can be rectangular or ellipse
        :param shadow_width: Shadow width in px. If ``0`` the shadow is disabled
        :param corner_radius: Shadow corner radius if rectangular in px
        :param color: Shadow color
        :param aa_amount: Antialiasing amout
        :return: Self reference
        """
        assert shadow_type in (WIDGET_SHADOW_TYPE_ELLIPSE, WIDGET_SHADOW_TYPE_RECTANGULAR)
        assert isinstance(shadow_width, int) and shadow_width >= 0
        assert isinstance(corner_radius, int) and corner_radius >= 0
        assert isinstance(aa_amount, int) and aa_amount > 0
        color = assert_color(color)
        self._shadow['enabled'] = shadow_width > 0
        self._shadow['properties'] = (shadow_type, shadow_width, shadow_width + corner_radius, aa_amount, color[0:3])
        self._shadow['surface'] = None
        return self

    def get_font_color_status(self, check_selection: bool = True) -> ColorType:
        """
        Return the Widget font color based on the widget status.

        :param check_selection: If ``True`` font is also checked if selected
        :return: Color by widget status
        """
        if self.readonly:
            if self._selected:
                return self._font_readonly_selected_color
            return self._font_readonly_color
        if self._selected and check_selection and self._selection_effect.widget_apply_font_color:
            return self._font_selected_color
        return self._font_color

    def set_font(
            self,
            font: FontType,
            font_size: int,
            color: ColorInputType,
            selected_color: ColorInputType,
            readonly_color: ColorInputType,
            readonly_selected_color: ColorInputType,
            background_color: Optional[ColorInputType],
            antialias: bool = True
    ) -> 'Widget':
        """
        Set the Widget font.

        :param font: Font name (see :py:meth:`pygame.font.match_font` for precise format)
        :param font_size: Size of font in pixels
        :param color: Normal font color
        :param selected_color: Font color if widget is selected
        :param readonly_color: Font color if widget is in readonly mode
        :param readonly_selected_color: Font color if widget is selected and in readonly mode
        :param background_color: Font background color. If ``None`` no background color is used
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :return: Self reference
        """
        assert isinstance(font_size, int) and font_size > 0
        assert isinstance(antialias, bool)
        color = assert_color(color)
        selected_color = assert_color(selected_color)
        readonly_color = assert_color(readonly_color)
        readonly_selected_color = assert_color(readonly_selected_color)

        if background_color is not None:
            background_color = assert_color(background_color)

            # If background is a color, and it's transparent raise a warning
            # Font background color must be opaque, otherwise the results are quite bad
            if len(background_color) == 4 and background_color[3] != 255:
                background_color = None
                if self._verbose:
                    warn('font background color must be opaque, alpha channel must be 255')

        font_size = int(font_size)

        self._font = pygame_menu.font.get_font(font, font_size)
        self._font_antialias = antialias
        self._font_background_color = background_color
        self._font_color = color
        self._font_name = font
        self._font_readonly_color = readonly_color
        self._font_readonly_selected_color = readonly_selected_color
        self._font_selected_color = selected_color
        self._font_size = font_size

        self._apply_font()
        self._force_render()
        return self

    def set_font_shadow(
            self,
            enabled: bool = True,
            color: Optional[ColorInputType] = None,
            position: Optional[str] = None,
            offset: int = 2
    ) -> 'Widget':
        """
        Set the Widget font shadow.

        .. note::

            See :py:mod:`pygame_menu.locals` for valid ``position`` values.

        :param enabled: Shadow is enabled or not
        :param color: Shadow color
        :param position: Shadow position
        :param offset: Shadow offset
        :return: Self reference
        """
        self._font_shadow = enabled
        if color is not None:
            color = assert_color(color)
            self._font_shadow_color = color
        if position is not None:
            assert_position(position)
            self._font_shadow_position = position
        assert isinstance(offset, int)
        assert offset > 0, 'shadow offset must be greater than zero if enabled'
        self._font_shadow_offset = offset

        # Set position
        x = 0
        y = 0
        if self._font_shadow_position == POSITION_NORTHWEST:
            x = -1
            y = -1
        elif self._font_shadow_position == POSITION_NORTH:
            y = -1
        elif self._font_shadow_position == POSITION_NORTHEAST:
            x = 1
            y = -1
        elif self._font_shadow_position == POSITION_EAST:
            x = 1
        elif self._font_shadow_position == POSITION_SOUTHEAST:
            x = 1
            y = 1
        elif self._font_shadow_position == POSITION_SOUTH:
            y = 1
        elif self._font_shadow_position == POSITION_SOUTHWEST:
            x = -1
            y = 1
        elif self._font_shadow_position == POSITION_WEST:
            x = -1
        elif self._font_shadow_position == POSITION_CENTER:
            pass  # (0, 0)

        self._font_shadow_tuple = (x * self._font_shadow_offset,
                                   y * self._font_shadow_offset)
        self._force_render()
        return self

    def update_font(self, style: Dict[str, Any]) -> 'Widget':
        """
        Updates the Widget font. This method receives a style dict (non-empty).

        Optional style keys
            - ``antialias``                 (bool) – Font antialias
            - ``background_color``          (tuple) – Background color
            - ``color``                     (tuple) – Font color
            - ``name``                      (str) – Name of the font
            - ``readonly_color``            (tuple) – Readonly color
            - ``readonly_selected_color``   (tuple) – Readonly selected color
            - ``selected_color``            (tuple) – Selected color
            - ``size``                      (int) – Size of the font

        .. note::

            If a key is not defined it will be rewritten using current font style
            from :py:meth:`pygame_menu.widgets.core.widget.Widget.get_font_info`
            method.

        :param style: Font style dict
        :return: Self reference
        """
        assert isinstance(style, dict)
        assert 1 <= len(style.keys()) <= 6
        current_font = self.get_font_info()
        for k in current_font.keys():
            if k not in style.keys():
                style[k] = current_font[k]
        return self.set_font(
            antialias=style['antialias'],
            background_color=style['background_color'],
            color=style['color'],
            font=style['name'],
            font_size=style['size'],
            readonly_color=style['readonly_color'],
            readonly_selected_color=style['readonly_selected_color'],
            selected_color=style['selected_color']
        )

    def get_font_info(self) -> Dict[str, Any]:
        """
        Return a dict with the information of the Widget font.

        :return: Font information dict
        """
        return {
            'antialias': self._font_antialias,
            'background_color': self._font_background_color,
            'color': self._font_color,
            'name': self._font_name,
            'readonly_color': self._font_readonly_color,
            'readonly_selected_color': self._font_readonly_selected_color,
            'selected_color': self._font_selected_color,
            'size': self._font_size
        }

    def set_menu(self, menu: Optional['pygame_menu.Menu']) -> 'Widget':
        """
        Set the Widget menu reference.

        :param menu: Menu object
        :return: Self reference
        """
        self._menu = menu
        if menu is None:
            self._col_row_index = (-1, -1, -1)
            self._selected = False
            self.active = False
        self._force_render()
        return self

    def get_menu(self) -> Optional['pygame_menu.Menu']:
        """
        Return the Menu reference, ``None`` if it has not been set.

        :return: Menu reference
        """
        return self._menu

    def _get_menu_widgets(self) -> List['Widget']:
        """
        Return the menu API widgets list.

        .. warning::

            Use with caution.

        :return: Widget list if the menu reference is not ``None``, else, return an empty list
        """
        if self._menu is not None:
            return self._menu._widgets
        return []

    def _get_menu_update_widgets(self) -> List['Widget']:
        """
        Return the menu update widgets.

        .. warning::

            Use with caution.

        :return: Widget update list if the menu reference is not ``None``, else, return an empty list
        """
        if self._menu is not None:
            return self._menu._update_widgets
        return []

    def _menu_render(self) -> None:
        """
        Call menu _render if reference is not ``None``.
        """
        if self._menu is not None:
            self._menu._render()

    def _apply_font(self) -> None:
        """
        Function triggered after a font is applied to the widget.
        """
        raise NotImplementedError('override is mandatory')

    def _set_position_relative_to_frame(self, index: int = -1) -> 'Widget':
        """
        Set the Widget position relative to its frame.

        :param index: Widget index
        :return: Self reference
        """
        if self._frame is not None:
            fx, fy = self._frame.get_position()
            self.set_position(fx + self._padding[3], fy + self._padding[0])
            c, r, _ = self._frame.get_col_row_index()
            self.set_col_row_index(c, r, index)
            self._frame.update_indices()
        else:
            # raise ValueError(f'{self.get_class_id()} is not within a frame')
            pass
        return self

    def set_position(self, x: NumberType, y: NumberType) -> 'Widget':
        """
        Set the Widget position relative to the Menu/Frame.

        This method is executed by the Menu when updating the widget positioning.
        For moving the widget use ``translate`` method instead, as this position
        will be rewritten on next menu rendering phase.

        .. note::

            Use :py:meth:`pygame_menu.widgets.core.widget.Widget.render` method
            to force Widget rendering after calling this method.

        :param x: X position in px
        :param y: Y position in px
        :return: Self reference
        """
        assert isinstance(x, NumberInstance)
        assert isinstance(y, NumberInstance)
        if self.lock_position:
            return self
        self._position = (int(x), int(y))
        self._rect.x = self._position[0] + self._translate[0] + self._translate_virtual[0]
        self._rect.y = self._position[1] + self._translate[1] + self._translate_virtual[1]
        return self

    def get_position(
            self,
            apply_padding: bool = False,
            use_transformed_padding: bool = True,
            to_real_position: bool = False,
            to_absolute_position: bool = False,
            real_position_visible: bool = True
    ) -> Tuple2IntType:
        """
        Return the widget position tuple on x-axis and y-axis (x, y) in px.

        :param apply_padding: Apply widget padding to position
        :param use_transformed_padding: Use scaled padding if the widget is scaled
        :param to_real_position: Get the real position within window (not the surface container)
        :param to_absolute_position: Get the absolute position within surface container, considering also the parent scrollarea positioning
        :param real_position_visible: Return only the visible width/height if ``to_real_position=True``
        :return: Widget position
        """
        if not (apply_padding or to_real_position or to_absolute_position):
            return self._rect.x, self._rect.y
        rect = self.get_rect(
            apply_padding=apply_padding,
            use_transformed_padding=use_transformed_padding,
            to_real_position=to_real_position,
            to_absolute_position=to_absolute_position,
            real_position_visible=real_position_visible
        )
        return rect.x, rect.y

    def flip(self, x: bool, y: bool) -> 'Widget':
        """
        Transformation: This method can flip the Widget either vertically,
        horizontally, or both. Flipping a Widget is non-destructive and does not
        change the dimensions.

        .. note::

            Flip is only applied after Widget rendering. Thus, the changes are
            not immediate.

        .. note::

            Use :py:meth:`pygame_menu.widgets.core.widget.Widget.render` method to force
            Widget rendering after calling this method.

        :param x: Flip on x-axis
        :param y: Flip on y-axis
        :return: Self reference
        """
        assert isinstance(x, bool)
        assert isinstance(y, bool)
        self._flip = (x, y)
        self._force_render()
        return self

    def _disable_scale(self) -> None:
        """
        Disables Widget scale.
        """
        self._scale[0] = False
        self._scale[1] = 1
        self._scale[2] = 1
        self._max_width[0] = None
        self._max_height[0] = None
        self.render()

    def _scale_warn(
            self,
            scale: bool = True,
            maxwidth: bool = True,
            maxheight: bool = True
    ) -> None:
        """
        Warns user about overriding properties of scale/maxwidth/maxheight.

        :param scale: Warn about scale
        :param maxwidth: Warn bout maxwidth
        :param maxheight: Warn about maxheight
        """
        if not self._verbose:
            return
        if self._scale[0] and scale:
            warn('widget already has a scaling factor applied. Scaling has '
                 'been disabled')
        if self._max_width[0] is not None and maxwidth:
            warn(
                'widget max width is not None. Set widget.set_max_width(None) '
                'for disabling such feature. This scaling will be ignored'
            )
        if self._max_height[0] is not None and maxheight:
            warn(
                'widget max height is not None. Set widget.set_max_height(None) '
                'for disabling such feature. This scaling will be ignored'
            )

    def set_max_width(
            self,
            width: Optional[NumberType],
            scale_height: NumberType = False,
            smooth: bool = True
    ) -> 'Widget':
        """
        Transformation: Set the Widget max width, it applies a scaling factor if
        the widget width is greater than the limit.

        .. note::

            If ``width=0`` the widget will use the max column width of the Menu
            (using the column the widget belongs to).

        .. note::

            Max width considers padding.

        .. note::

            Max width is only applied after widget rendering. Thus, the changes
            are not immediate.

        .. note::

            Use :py:meth:`pygame_menu.widgets.core.widget.Widget.render` method
            to force widget rendering after calling this method.

        .. warning::

            Final Widget size may not be exactly the same as the desired (width,
            height) tuple due to rounding errors, expect ±2 px average.

        .. warning::

            Widget will scale only if :py:meth:`pygame_menu.widgets.core.widget.Widget.scale`
            and :py:meth:`pygame_menu.widgets.core.widget.Widget.set_max_height`
            are set to ``None``. Thus, calling this method disables both scale and max height.

        :param width: Width in px, ``None`` if max width is disabled
        :param scale_height: If ``True`` the height is also scaled if the width exceeds the limit
        :param smooth: Smooth scaling
        :return: Self reference
        """
        assert isinstance(scale_height, bool)
        assert isinstance(smooth, bool)

        self._scale_warn(maxwidth=False)
        self._disable_scale()

        if width is None:
            self._max_width[0] = None
        else:
            assert isinstance(width, NumberInstance), 'width must be numeric'
            assert width >= 0, 'width must be equal or greater than zero'
            self._max_width = [width, scale_height, smooth]

        self._force_render()
        return self

    def set_max_height(
            self,
            height: Optional[NumberType],
            scale_width: NumberType = False,
            smooth: bool = True
    ) -> 'Widget':
        """
        Transformation: Set the Widget max height, it applies a scaling factor
        if the widget height is greater than the limit.

        .. note::

            Max height considers padding.

        .. note::

            Max height is only applied after Widget rendering. Thus, the changes
            are not immediate.

        .. note::

            Use :py:meth:`pygame_menu.widgets.core.widget.Widget.render` method
            to force widget rendering after calling this method.

        .. warning::

            Final Widget size may not be exactly the same as the desired (width,
            height) tuple due to rounding errors, expect ±2 px average.

        .. warning::

            Widget will scale only if :py:meth:`pygame_menu.widgets.core.widget.Widget.scale`
            and :py:meth:`pygame_menu.widgets.core.widget.Widget.set_max_width`
            are set to ``None``. Thus, calling this method disables both scale and max width.

        :param height: Height in px, ``None`` if max height is disabled
        :param scale_width: If ``True`` the width is also scaled if the height exceeds the limit
        :param smooth: Smooth scaling
        :return: Self reference
        """
        assert isinstance(scale_width, bool)
        assert isinstance(smooth, bool)

        self._scale_warn(maxheight=False)
        self._disable_scale()

        if height is None:
            self._max_height[0] = None
        else:
            assert isinstance(height, NumberInstance), 'height must be numeric'
            assert height > 0, 'height must be greater than zero'
            self._max_height = [height, scale_width, smooth]

        self._force_render()
        return self

    def scale(
            self,
            width: NumberType,
            height: NumberType,
            smooth: bool = True
    ) -> 'Widget':
        """
        Transformation: Scale the Widget to a desired width and height factor.

        .. note::

            Not all widgets are affected by scale.

        .. note::

            Scale considers widget padding.

        .. note::

            Scale is only applied after widget rendering. Thus, the changes are
            not immediate.

        .. note::

            Use :py:meth:`pygame_menu.widgets.core.widget.Widget.render` method
            to force widget rendering after calling this method.

        .. warning::

            Widget will scale only if :py:meth:`pygame_menu.widgets.core.widget.Widget.set_max_width`
            and :py:meth:`pygame_menu.widgets.core.widget.Widget.set_max_height`
            are set to ``None``. Thus, calling this method disables both max width and height.

        :param width: Scale factor of the width
        :param height: Scale factor of the height
        :param smooth: Smooth scaling
        :return: Self reference
        """
        assert isinstance(width, NumberInstance)
        assert isinstance(height, NumberInstance)
        assert isinstance(smooth, bool)
        assert width > 0 and height > 0, \
            'width and height must be greater than zero'

        self._scale_warn(scale=False)
        self._disable_scale()

        self._scale = [True, width, height, smooth]
        if width == 1 and height == 1:  # Disables scaling
            self._scale[0] = False

        self._force_render()
        return self

    def resize(
            self,
            width: NumberType,
            height: NumberType,
            smooth: bool = True
    ) -> 'Widget':
        """
        Transformation: Set the Widget size to another size.

        .. note::

            This method calls :py:meth:`pygame_menu.widgets.core.widget.Widget.scale`
            method; thus, some widgets may not support this transformation.

        .. note::

            The resize method uses the base Widget size, without any transformation,
            if a scaling factor is applied it unscales and then scales back to get
            the desired width/height.

        .. note::

            Resize is only applied after Widget rendering. Thus, the changes are
            not immediate.

        .. note::

            Use :py:meth:`pygame_menu.widgets.core.widget.Widget.render` method
            to force widget rendering after calling this method.

        .. warning::

            Final Widget size may not be exactly the same as the desired (width,
            height) tuple due to rounding errors, expect ±2 px average.

        :param width: New width of the widget in px
        :param height: New height of the widget in px
        :param smooth: Smooth scaling
        :return: Self reference
        """
        self._disable_scale()
        if width == 1 and height == 1:
            if self._verbose:
                warn('did you mean widget.scale(1,1) instead of widget.resize(1,1)?')
        self.scale(float(width) / self.get_width(),
                   float(height) / self.get_height(), smooth)
        return self

    def translate(self, x: NumberType, y: NumberType) -> 'Widget':
        """
        Transformation: Translate to (+x, +y) according to the default position.

        .. note::

            Translate is only applied when updating the widget position (calling
            :py:meth:`pygame_menu.widgets.core.widget.Widget.set_position`). This
            is done by Menu when rendering the surface. Thus, the position change
            is not immediate. To force translation update you may call Menu render
            method.

        .. note::

            To revert changes, only set to ``(0, 0)``.

        .. note::

            Use :py:meth:`pygame_menu.widgets.core.widget.Widget.render` method
            to force widget rendering after calling this method.

        :param x: +X in px
        :param y: +Y in px
        """
        assert isinstance(x, NumberInstance)
        assert isinstance(y, NumberInstance)
        self._translate = (int(x), int(y))
        self._force_render()
        return self

    def get_translate(self, virtual: bool = False) -> Tuple2IntType:
        """
        Get Widget translation on x-axis and y-axis (x, y) in px.

        :param virtual: If ``True`` get virtual translation, usually applied within frame scrollarea
        :return: Translation on both axis
        """
        if virtual:
            return self._translate_virtual
        return self._translate

    def rotate(self, angle: NumberType) -> 'Widget':
        """
        Transformation: Unfiltered counterclockwise rotation. The angle argument
        represents degrees and can be any floating point value. Negative angle
        amounts will rotate clockwise.

        .. note::

            Not all widgets accepts rotation. Also, this rotation only affects the
            text or images, the selection or background is not rotated.

        .. note::

            Rotation is only applied after widget rendering. Thus, the changes are
            not immediate.

        .. note::

            Use :py:meth:`pygame_menu.widgets.core.widget.Widget.render` method
            to force widget rendering after calling this method.

        :param angle: Rotation angle (degrees ``0-360``)
        :return: Self reference
        """
        assert isinstance(angle, NumberInstance)
        self._angle = angle
        self._force_render()
        return self

    def set_alignment(self, align: str) -> 'Widget':
        """
        Set the alignment of the Widget.

        .. note::

            Alignment is only applied when updating the widget position, done by
            Menu when rendering the surface. Thus, the alignment change is not
            immediate.

        .. note::

            Use :py:meth:`pygame_menu.widgets.core.widget.Widget.render` method
            to force widget rendering after calling this method.

        .. note::

            See :py:mod:`pygame_menu.locals` for valid ``align`` values.

        :param align: Widget align
        :return: Self reference
        """
        assert_alignment(align)
        self._alignment = align
        self._force_render()
        return self

    def get_alignment(self) -> str:
        """
        Return the Widget alignment.

        :return: Widget align
        """
        return self._alignment

    def select(self, status: bool = True, update_menu: bool = False) -> 'Widget':
        """
        Mark the Widget as selected and execute the ``onselect`` callback function
        as follows:

        .. code-block:: python

            onselect(selected, widget, menu) <or> onselect()

        If Widget ``is_selectable`` is ``False`` this function is not executed.

        .. note::

            Use :py:meth:`pygame_menu.widgets.core.widget.Widget.render` method
            to force Widget rendering after calling this method.

        .. warning::

            This method should only be used by the menu.

        :param status: Selection status
        :param update_menu: If ``True`` this status is also applied on the menu that contains this widget
        :return: Self reference
        """
        assert isinstance(status, bool)
        if not self.is_selectable:
            return self

        # Update status
        self._selected = status
        self.active = False

        # Toggle between focus and blur events
        if self._selected:
            self._focus()
            self._selection_time = time.time()
        else:
            self._blur()
            self._events = []  # Remove events

        self._force_render()

        # Call selection event
        if self._onselect is not None:
            try:
                self._onselect(self._selected, self, self._menu)
            except TypeError:
                self._onselect()

        # Update the menu object
        if update_menu:
            assert self._menu is not None
            self._menu.select_widget(None)  # Unselect previous one
            self._menu.select_widget(self)

        return self

    def get_selected_time(self) -> NumberType:
        """
        Return time the Widget has been selected in milliseconds. If the Widget
        is not currently selected, return ``0``.

        :return: Time in milliseconds
        """
        if not self._selected:
            return 0
        return (time.time() - self._selection_time) * 1000

    def get_surface(self) -> 'pygame.Surface':
        """
        Return the Widget surface.

        .. warning::

            Use with caution.

        :return: Widget surface object
        """
        return self._surface

    def get_width(
            self,
            apply_padding: bool = True,
            apply_selection: bool = False
    ) -> int:
        """
        Return the Widget width.

        .. warning::

            If the Widget is not rendered, this method will return ``0``.

        :param apply_padding: Apply padding
        :param apply_selection: Apply selection
        :return: Widget width in px
        """
        assert isinstance(apply_padding, bool)
        assert isinstance(apply_selection, bool)
        rect = self.get_rect(apply_padding=apply_padding, render=True)
        width = rect.width
        if apply_selection:
            width += self._selection_effect.get_width()
        return int(width)

    def get_height(
            self,
            apply_padding: bool = True,
            apply_selection: bool = False
    ) -> int:
        """
        Return the Widget height.

        .. warning::

            If the widget is not rendered, this method will return ``0``.

        :param apply_padding: Apply padding
        :param apply_selection: Apply selection
        :return: Widget height in px
        """
        assert isinstance(apply_padding, bool)
        assert isinstance(apply_selection, bool)
        rect = self.get_rect(apply_padding=apply_padding, render=True)
        height = rect.height
        if apply_selection:
            height += self._selection_effect.get_height()
        return int(height)

    def get_size(
            self,
            apply_padding: bool = True,
            apply_selection: bool = False
    ) -> Tuple2IntType:
        """
        Return the Widget size.

        .. warning::

            If the widget is not rendered this method might return ``(0, 0)``.

        :param apply_padding: Apply padding
        :param apply_selection: Apply selection
        :return: Widget width and height in px
        """
        return self.get_width(apply_padding=apply_padding, apply_selection=apply_selection), \
            self.get_height(apply_padding=apply_padding, apply_selection=apply_selection)

    def _focus(self) -> None:
        """
        Function that is executed when the Widget receives the user focus (is
        selected).
        """
        pass

    def _blur(self) -> None:
        """
        Function that is executed when the Widget loses the focus.
        """
        pass

    def _configure(self) -> None:
        """
        Function that is executed after the Widget is configured.
        """
        pass

    def _append_to_menu(self) -> None:
        """
        Function that is executed after the Widget is appended to the Menu.
        """
        pass

    def set_sound(self, sound: 'Sound') -> 'Widget':
        """
        Set sound engine to the Widget.

        :param sound: Sound object
        :return: Self reference
        """
        self._sound = sound
        return self

    def set_controls(
            self,
            joystick: bool = True,
            mouse: bool = True,
            touchscreen: bool = True,
            keyboard: bool = True
    ) -> 'Widget':
        """
        Enable interfaces to control the Widget.

        :param joystick: Use joystick events
        :param mouse: Use mouse events
        :param touchscreen: Use touchscreen events
        :param keyboard: Use keyboard events
        :return: Self reference
        """
        assert isinstance(joystick, bool)
        assert isinstance(mouse, bool)
        assert isinstance(touchscreen, bool)
        assert isinstance(keyboard, bool)
        self._joystick_enabled = joystick
        self._mouse_enabled = mouse
        self._touchscreen_enabled = touchscreen
        self._keyboard_enabled = keyboard
        return self

    def set_value(self, value: Any) -> None:
        """
        Set the Widget value.

        .. note::

            Not all widgets accepts a value, for example the image widget.

        .. warning::

            This method does not fire the callbacks as it is called programmatically.
            This behavior is deliberately chosen to avoid infinite loops.

        :param value: Value to be set on the widget
        """
        raise ValueError(f'{self.get_class_id()} does not accept value')

    def set_default_value(self, value: Any) -> 'Widget':
        """
        Set the Widget value, and then make it as default.

        .. note::

            This method is intended to be used along
            :py:meth:`pygame_menu.widgets.core.widget.Widget.reset_value`
            method that sets the Widget value back to the default set with this
            method.

        .. note::

            Not all widgets accepts a value, for example the image widget.

        :param value: Default widget value
        :return: Self reference
        """
        self.set_value(value)
        self._default_value = value
        return self

    def reset_value(self) -> 'Widget':
        """
        Reset the Widget value to the default one.

        :return: Self reference
        """
        if not isinstance(self._default_value, _WidgetNoValue):
            self.set_value(self._default_value)
        return self

    def update(self, events: EventVectorType) -> bool:
        """
        Update according to the given events list and fire the callbacks. This
        method must return ``True`` if it updated (the internal variables
        changed during user input).

        .. note::

            Update is not performed if the Widget is in ``readonly`` state, or
            it's hidden. However, ``apply_update_callbacks`` method is called
            in most widgets, except :py:class:`pygame_menu.widgets.NoneWidget`.

        :param events: List/Tuple of pygame events
        :return: ``True`` if updated
        """
        raise NotImplementedError('override is mandatory')

    def update_menu(self, events: EventVectorType) -> bool:
        """
        Update the widget from Menu. This method is the same as update(), however,
        it takes into account the value of ``widget.receive_menu_update_events``.

        :param events: List/Tuple of pygame events
        :return: ``True`` if updated
        """
        if not self.receive_menu_update_events:
            return False
        return self.update(events)

    def add_draw_callback(
            self,
            draw_callback: Callable[['Widget', 'pygame_menu.Menu'], Any]
    ) -> str:
        """
        Adds a function to the Widget to be executed each time the widget is drawn.

        The function that this method receives two objects: the Widget itself and
        the Menu reference.

        .. code-block:: python

            import math

            def draw_update_function(widget, menu):
                t = widget.get_attribute('t', 0)
                t += menu.get_clock().get_time()
                widget.set_padding(10*(1 + math.sin(t))) # Oscillating padding

            button = menu.add.button('This button updates its padding', None)
            button.set_draw_callback(draw_update_function)

        After creating a new callback, this functions returns the ID of the call.
        It can be removed anytime using
        :py:meth:`pygame_menu.widgets.core.widget.Widget.remove_draw_callback`.

        .. note::

            If Menu surface cache is enabled this method may run only once. To
            force running the added method each time call
            ``widget.force_menu_surface_update()`` to force Menu update the cache
            status if the drawing callback does not make the Widget to render.
            Remember that rendering the Widget forces the Menu to update its
            surface, thus updating the cache too.

        :param draw_callback: Function
        :return: Callback ID
        """
        assert callable(draw_callback), \
            'draw callback must be callable (function-type)'
        callback_id = uuid4()
        self._draw_callbacks[callback_id] = draw_callback
        return callback_id

    def remove_draw_callback(self, callback_id: str) -> 'Widget':
        """
        Removes draw callback from ID.

        :param callback_id: Callback ID
        :return: Self reference
        """
        assert isinstance(callback_id, str)
        if callback_id not in self._draw_callbacks.keys():
            raise IndexError(f'callback ID "{callback_id}" does not exist')
        del self._draw_callbacks[callback_id]
        return self

    def apply_draw_callbacks(self) -> 'Widget':
        """
        Apply callbacks on Widget draw.

        :return: Self reference
        """
        if len(self._draw_callbacks) == 0:
            return self
        for callback in self._draw_callbacks.values():
            callback(self, self._menu)
        return self

    def add_update_callback(
            self,
            update_callback: Callable[[EventListType, 'Widget', 'pygame_menu.Menu'], Any]
    ) -> str:
        """
        Adds a function to the Widget to be executed each time the Widget is
        updated.

        The function that this method receives three objects: the events
        list, the Widget itself and the Menu reference. It is similar to
        :py:meth:`pygame_menu.widgets.core.widget.Widget.add_draw_callback`.

        After creating a new callback, this functions returns the ID of the call.
        It can be removed anytime using
        :py:meth:`pygame_menu.widgets.core.widget.Widget.remove_update_callback`.

        .. note::

            Not all widgets are updated, so the provided function may never be
            executed in some widgets (for example, label or images).

        :param update_callback: Function
        :return: Callback ID
        """
        assert callable(update_callback), \
            'update callback must be callable (function-type)'
        callback_id = uuid4()
        self._update_callbacks[callback_id] = update_callback
        return callback_id

    def remove_update_callback(self, callback_id: str) -> 'Widget':
        """
        Removes update callback from ID.

        :param callback_id: Callback ID
        :return: Self reference
        """
        assert isinstance(callback_id, str)
        if callback_id not in self._update_callbacks.keys():
            raise IndexError(f'callback<"{callback_id}"> does not exist')
        del self._update_callbacks[callback_id]
        return self

    def apply_update_callbacks(self, events: EventListType) -> 'Widget':
        """
        Apply callbacks on Widget update.

        .. note::

            Readonly widgets or hidden widgets do not apply update callbacks.

        :param events: Events list
        :return: Self reference
        """
        if len(self._update_callbacks) == 0 or self.readonly:
            return self
        for callback in self._update_callbacks.values():
            callback(events, self, self._menu)
        return self

    def _add_event(self, event: EventType) -> None:
        """
        Add a custom event to the Widget for the next update.

        :param event: Custom event
        """
        self._events.append(event)

    def _merge_events(self, events: EventListType) -> EventListType:
        """
        Append the Widget events to events list.

        :param events: Event list
        :return: Augmented event list
        """
        if len(self._events) == 0:
            return events
        copy_events = []
        for e in events:
            copy_events.append(e)
        for e in self._events:
            copy_events.append(e)
        self._events = []
        return copy_events

    def set_float(
            self,
            float_status: bool = True,
            menu_render: bool = False,
            origin_position: bool = False
    ) -> 'Widget':
        """
        Set the floating status. If ``True`` the Widget don't contribute its
        width/height to the Menu widget positioning computation (for example,
        the surface area or the column/row layout), and don't add one unit to
        the rows (use the same vertical place as the previous widget).

        For example, before floating:

            .. code-block:: python

                ----------------------------
                |    wid1    |    wid3     |
                |    wid2    |    wid4     |
                ----------------------------

        After ``wid3.set_float(True)``:

            .. code-block:: python

                ----------------------------
                |    wid1    |    wid4     |
                | wid2,wid3  |             |
                ----------------------------

        If the Widget is within a Frame, it does not contribute to the
        width/height of the layout. Also, it is being set to the *(0, 0)* position,
        thus, the only way to move the Widget to a desired position is by
        translating it.

        :param float_status: Float status
        :param menu_render: If ``True`` forces the Menu to render instantly; else, rendering is controlled by menu
        :param origin_position: If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating (updated by the Menu render phase)
        """
        assert isinstance(float_status, bool)
        assert isinstance(menu_render, bool)
        assert isinstance(origin_position, bool)
        self._floating = float_status
        self._floating_origin_position = origin_position
        self.force_menu_surface_update()
        if menu_render and self._menu is not None:
            self._menu.render()
        return self

    def __update_menu_after_toggle(self, prev_visible: bool) -> 'Widget':
        """
        Updates menu position after widget toggle (show/hide).

        :param prev_visible: Previous visible status
        :return: Self reference
        """
        self._render()
        if self._menu is not None:
            self._menu._update_selection_if_hidden()
            if prev_visible != self._visible:
                try:
                    self._menu._update_widget_position()
                except AttributeError:
                    pass
        return self

    def show(self) -> 'Widget':
        """
        Set the Widget visible.

        :return: Self reference
        """
        prev_visible = self._visible
        self._visible = True
        return self.__update_menu_after_toggle(prev_visible)

    def hide(self) -> 'Widget':
        """
        Hides the Widget.

        :return: Self reference
        """
        prev_visible = self._visible
        if self._mouseover:
            self._mouseover = False
            self.mouseleave(mouse_motion_current_mouse_position())
        self._visible = False
        self.active = False
        return self.__update_menu_after_toggle(prev_visible)

    def set_col_row_index(self, col: int, row: int, index: int) -> 'Widget':
        """
        Set the (column, row, index) position. If the column or row is ``-1`` then
        the widget is not assigned to a certain column/row (for example, if it's
        hidden).

        :param col: Column
        :param row: Row
        :param index: Index in Menu widget list
        :return: Self reference
        """
        assert isinstance(col, int) and col >= -1
        assert isinstance(row, int) and row >= -1
        assert isinstance(index, int) and index >= -1
        self._col_row_index = (col, row, index)
        return self

    def get_col_row_index(self) -> Tuple3IntType:
        """
        Get the Widget column/row position.

        :return: (column, row, index) tuple
        """
        return self._col_row_index

    def get_decorator(self) -> 'Decorator':
        """
        Return the Widget decorator API.

        :return: Decorator API
        """
        return self._decorator

    def get_frame(self) -> Optional['pygame_menu.widgets.Frame']:
        """
        Get container frame of Widget. If Widget is not within a Frame, the method
        returns ``None``.

        :return: Frame object
        :rtype: :py:class:`pygame_menu.widgets.Frame`
        """
        return self._frame

    def set_frame(self, frame: 'pygame_menu.widgets.Frame') -> 'Widget':
        """
        Set Widget frame.

        :param frame: Frame object
        :return: Self reference
        """
        assert self._frame is None, 'widget is already in another frame'
        assert isinstance(frame, pygame_menu.widgets.Frame)
        self._frame = frame
        return self

    def get_frame_depth(self) -> int:
        """
        Get frame depth (If frame is packed within another frame).

        :return: Frame depth
        """
        frame = self._frame
        depth = 0
        if frame is not None:
            while True:
                if frame is None:
                    break
                depth += 1
                frame = frame._frame
        return depth

    def _get_status(self) -> Tuple[Any, ...]:
        """
        Get the status of the Widget as a tuple (position, indices, values, etc.).

        :return: Data
        """
        # Assemble class name
        cls_name = self.__class__.__name__
        if self.get_title() != '':
            cls_name += '-' + self.get_title()

        # Assemble geometric data
        rect = self.get_rect(render=True)
        rect_real = self.get_rect(to_real_position=True)
        rect_abs = self.get_rect(to_absolute_position=True)
        cri = self.get_col_row_index()
        geom = (
            cri[0], cri[1], cri[2],  # Column/row layout
            rect.x, rect.y, rect.width, rect.height,  # Drawing rect
            rect_real.x, rect_real.y,  # Real rect positioning
            rect_abs.x, rect_abs.y  # Absolute rect positioning
        )

        # Bool info
        bool_status = (
            int(self.is_selectable),
            int(self.is_floating()),
            int(self.is_selected()),
            int(self.is_visible()),
            int(self.is_scrollable),
            int(self.get_frame() is not None),
            self.get_frame_depth()
        )

        # Starting data
        data = [cls_name, geom, bool_status]

        # Append inner widgets if frame and not menu
        if isinstance(self, pygame_menu.widgets.Frame):
            data.append(self.get_indices())
            for ww in self.get_widgets():
                if ww.get_menu() != self.get_menu():
                    data.append(ww._get_status())

        # Append inner widgets if drop select
        if isinstance(self, pygame_menu.widgets.DropSelect) and self._drop_frame is not None:
            data.append(self._drop_frame._get_status())
            for btn in self._option_buttons:
                data.append(btn._get_status())

        try:
            data.append(self.get_value())
        except ValueError:
            pass

        return tuple(data)

    def set_tab_size(self, tab_size: int) -> 'Widget':
        """
        Set widget tab size.

        :param tab_size: Width of a tab character
        :return: Self reference
        """
        assert isinstance(tab_size, int) and tab_size >= 0
        self._tab_size = tab_size
        return self

    def set_controller(self, controller: 'Controller') -> 'Widget':
        """
        Set a new controller object.

        :param controller: Controller
        :return: Self reference
        """
        self._ctrl = controller
        return self

    def get_controller(self) -> 'Controller':
        """
        Return the widget controller. Each widget has their own controller object.

        :return: Controller object
        """
        return self._ctrl


class _WidgetCopyException(Exception):
    """
    If user tries to copy a Widget.
    """
    pass


class _WidgetNoValue(object):
    """
    No value class.
    """
    pass


class WidgetTransformationNotImplemented(Exception):
    """
    Exception raised if widget does not implement a transformation.
    """
    pass


class AbstractWidgetManager(object):
    """
    Add/Remove widgets to the Menu.
    """
    _menu: 'pygame_menu.Menu'

    def __init__(self) -> None:
        pass

    @property
    def _theme(self) -> 'pygame_menu.Theme':
        """
        Return menu theme.

        :return: Menu theme reference
        """
        raise NotImplementedError('override is mandatory')

    def _add_submenu(self, menu: 'pygame_menu.Menu', hook: 'Widget') -> None:
        """
        Adds a submenu. Requires the menu instance and the widget that adds the
        sub-menu.

        :param menu: Menu reference
        :param hook: Widget hook
        """
        raise NotImplementedError('override is mandatory')

    def _filter_widget_attributes(self, kwargs: Dict) -> Dict[str, Any]:
        """
        Return the valid widgets attributes from a dictionary.

        The valid (key, value) are removed from the initial dictionary.

        :param kwargs: Optional keyword arguments (input attributes)
        :return: Dictionary of valid attributes
        """
        raise NotImplementedError('override is mandatory')

    def _configure_widget(self, widget: 'Widget', **kwargs) -> None:
        """
        Update the given widget with the parameters defined at the Menu level.
        This method does not add widget to Menu.

        :param widget: Widget object
        :param kwargs: Optional keywords arguments
        """
        raise NotImplementedError('override is mandatory')

    @staticmethod
    def _check_kwargs(kwargs: Dict) -> None:
        """
        Check kwargs after widget addition. It should be empty. Raises ``ValueError``.

        :param kwargs: Kwargs dict
        """
        raise NotImplementedError('override is mandatory')

    def _append_widget(self, widget: 'Widget') -> None:
        """
        Add a widget to the list of widgets.

        :param widget: Widget object
        """
        raise NotImplementedError('override is mandatory')

    def configure_defaults_widget(self, widget: 'Widget') -> None:
        """
        Apply default menu settings to widget. This method does not add widget to
        the Menu.

        :param widget: Widget to be configured
        """
        raise NotImplementedError('override is mandatory')
