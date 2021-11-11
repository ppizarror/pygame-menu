"""
pygame-menu
https://github.com/ppizarror/pygame-menu

FRAME
Widget container.
"""

__all__ = [

    # Main class
    'Frame',
    'FrameManager',

    # Types
    'FrameTitleBackgroundColorType',
    'FrameTitleButtonType',

    # Constants
    'FRAME_DEFAULT_TITLE_BACKGROUND_COLOR',
    'FRAME_TITLE_BUTTON_CLOSE',
    'FRAME_TITLE_BUTTON_MAXIMIZE',
    'FRAME_TITLE_BUTTON_MINIMIZE'

]

import pygame
import pygame_menu

from abc import ABC
from pygame_menu._decorator import Decorator
from pygame_menu.baseimage import BaseImage
from pygame_menu.locals import CURSOR_HAND, ORIENTATION_VERTICAL, \
    ORIENTATION_HORIZONTAL, ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT, POSITION_CENTER, \
    POSITION_NORTH, POSITION_SOUTH, FINGERUP, FINGERDOWN, FINGERMOTION
from pygame_menu.font import FontType, assert_font
from pygame_menu.utils import assert_alignment, make_surface, assert_vector, \
    assert_orientation, assert_color, fill_gradient, parse_padding, uuid4, warn, \
    get_finger_pos
from pygame_menu.widgets.core.widget import Widget, check_widget_mouseleave, \
    WidgetTransformationNotImplemented, AbstractWidgetManager
from pygame_menu.widgets.widget.button import Button
from pygame_menu.widgets.widget.label import Label

from pygame_menu._types import Optional, NumberType, Dict, Tuple, Union, List, \
    Vector2NumberType, Literal, Tuple2IntType, NumberInstance, Any, ColorInputType, \
    EventVectorType, PaddingType, CallbackType, ColorInputGradientType, \
    CursorInputType, VectorInstance

# Constants
FRAME_DEFAULT_TITLE_BACKGROUND_COLOR = ((10, 36, 106), (166, 202, 240), False, True)
FRAME_TITLE_BUTTON_CLOSE = 'close'
FRAME_TITLE_BUTTON_MAXIMIZE = 'maximize'
FRAME_TITLE_BUTTON_MINIMIZE = 'minimize'
S_FINGER_FACTOR = 0.25, 0.25

# Types
FrameTitleBackgroundColorType = Optional[Union[ColorInputType, ColorInputGradientType, BaseImage]]
FrameTitleButtonType = Literal[FRAME_TITLE_BUTTON_CLOSE, FRAME_TITLE_BUTTON_MAXIMIZE,
                               FRAME_TITLE_BUTTON_MINIMIZE]


# noinspection PyMissingOrEmptyDocstring,PyProtectedMember
class Frame(Widget):
    """
    Frame is a widget container, it can pack many widgets.

    All widgets inside have a floating position. Widgets inside are placed using
    its margin + width/height. ``(0, 0)`` coordinate is the top-left position in
    frame.

    Frame modifies ``translation`` of widgets. Thus, if widget has a translation
    before it will be removed.

    Widget packing currently only supports LEFT, CENTER and RIGHT alignment in
    the same line, widgets cannot be packed in two different lines. For such
    purpose use several frames. If widget width or height exceeds Frame size
    ``_FrameSizeException`` will be raised.

    .. note::

        Frame cannot be selected. Thus, it does not receive any selection effect.

    .. note::

        Frames should be appended to Menu scrollable frames if it's scrollable,
        be careful when removing. Check :py:class:`pygame_menu.widgets.DropSelect`
        as a complete example of Frame implementation within another Widgets.

    .. note::

        Frame only accepts translation and resize transformations.

    :param width: Frame width in px
    :param height: Frame height in px
    :param orientation: Frame orientation (horizontal or vertical). See :py:mod:`pygame_menu.locals`
    :param frame_id: ID of the frame
    """
    _accepts_scrollarea: bool
    _accepts_title: bool
    _control_widget: Optional['Widget']
    _control_widget_last_pos: Optional[Vector2NumberType]
    _draggable: bool
    _frame_scrollarea: Optional['pygame_menu._scrollarea.ScrollArea']
    _frame_size: Tuple2IntType
    _frame_title: Optional['Frame']
    _has_frames: bool  # True if frame has packed other frames
    _has_title: bool
    _height: int
    _menu_can_be_none_pack: bool
    _orientation: str
    _pack_margin_warning: bool
    _pos: Dict[str, Tuple[int, int]]  # Widget positioning
    _real_rect: 'pygame.Rect'
    _recursive_render: int
    _widgets: Dict[str, 'Widget']  # widget
    _widgets_props: Dict[str, Tuple[str, str]]  # alignment, vertical position
    _width: int
    first_index: int  # First selectable widget index
    horizontal: bool
    last_index: int  # Last selectable widget index
    selected_widget_draw: Tuple[Optional['Widget'], Optional['pygame.Surface']]  # Stores selected widget

    def __init__(
            self,
            width: NumberType,
            height: NumberType,
            orientation: str,
            frame_id: str = ''
    ) -> None:
        super(Frame, self).__init__(widget_id=frame_id)
        assert isinstance(width, NumberInstance)
        assert isinstance(height, NumberInstance)
        assert width > 0, \
            f'width must be greater than zero ({width} received)'
        assert height > 0, \
            f'height must be greater than zero ({height} received)'
        assert_orientation(orientation)

        # Internals
        self._accepts_scrollarea = True
        self._accepts_title = True
        self._control_widget = None
        self._control_widget_last_pos = None  # This checks if menu has updated widget position
        self._draggable = False
        self._frame_scrollarea = None
        self._frame_size = (width, height)  # Size of the frame, set in make_scrollarea
        self._has_frames = False
        self._height = int(height)
        self._menu_can_be_none_pack = False
        self._orientation = orientation
        self._pack_margin_warning = True  # Set to False for hiding the pack margin warning
        self._pos = {}
        self._real_rect = pygame.Rect(0, 0, width, height)
        self._recursive_render = 0
        self._relax = False  # If True ignore sizing
        self._widgets = {}
        self._widgets_props = {}
        self._width = int(width)

        # Title
        self._frame_title = None
        self._has_title = False

        # Configure widget public's
        self.first_index = -1
        self.horizontal = orientation == ORIENTATION_HORIZONTAL
        self.is_scrollable = False
        self.is_selectable = False
        self.last_index = -1
        self.selected_widget_draw = (None, None)

    def set_title(
            self,
            title: str,
            cursor: CursorInputType = None,
            background_color: FrameTitleBackgroundColorType = FRAME_DEFAULT_TITLE_BACKGROUND_COLOR,
            draggable: bool = False,
            padding_inner: PaddingType = 0,
            padding_outer: PaddingType = 0,
            title_alignment: str = ALIGN_LEFT,
            title_buttons_alignment: str = ALIGN_RIGHT,
            title_font: Optional[FontType] = None,
            title_font_color: Optional[ColorInputType] = None,
            title_font_size: Optional[int] = None
    ) -> 'Frame':
        """
        Add a title to the frame.

        :param title: New title
        :param cursor: Title cursor
        :param background_color: Title background color. It can be a Color, a gradient, or an image
        :param draggable: If ``True`` the title accepts user drag using the mouse
        :param padding_inner: Padding inside the title
        :param padding_outer: Padding outside the title (respect to the Frame)
        :param title_alignment: Alignment of the title
        :param title_buttons_alignment: Alignment of the title buttons (if appended later)
        :param title_font: Title font. If ``None`` uses the same as the Frame
        :param title_font_color: Title font color. If ``None`` uses the same as the Frame
        :param title_font_size: Title font size in px. If ``None`` uses the same as the Frame
        :return: Title frame object
        """
        assert self.configured, \
            f'{self.get_class_id()} must be configured before setting a title'
        if not self._accepts_title:
            raise _FrameDoNotAcceptTitle(f'{self.get_class_id()} does not accept a title')
        self._title = title

        # If has previous title
        self.remove_title()

        assert isinstance(draggable, bool)
        self._draggable = draggable

        # Format title font properties
        if title_font is None:
            title_font = self._font_name
        assert_font(title_font)
        if title_font_color is None:
            title_font_color = self._font_color
        title_font_color = assert_color(title_font_color)
        if title_font_size is None:
            title_font_size = self._font_size
        assert isinstance(title_font_size, int) and title_font_size > 0
        assert_alignment(title_alignment)
        assert_alignment(title_buttons_alignment)

        # Check alignment are different
        assert title_alignment != title_buttons_alignment, \
            'title alignment and buttons alignment must be different'

        # Create title widget
        title_label = Label(
            title=title,
            label_id=self._id + '+title+label-' + uuid4(short=True)
        )
        title_label.set_font(
            antialias=self._font_antialias,
            background_color=None,
            color=title_font_color,
            font=title_font,
            font_size=title_font_size,
            readonly_color=self._font_readonly_color,
            readonly_selected_color=self._font_readonly_selected_color,
            selected_color=self._font_selected_color
        )
        title_label.set_tab_size(self._tab_size)
        title_label.configured = True
        title_label.set_menu(self._menu)
        title_label._update__repr___(self)

        # Create frame title
        pad_outer = parse_padding(padding_outer)  # top, right, bottom, left
        pad_inner = parse_padding(padding_inner)
        self._frame_title = Frame(
            width=self.get_width() - (pad_outer[1] + pad_outer[3] + pad_inner[1] + pad_inner[3]),
            height=title_label.get_height(),
            orientation=ORIENTATION_HORIZONTAL,
            frame_id=self._id + '+title-' + uuid4(short=True)
        )
        self._frame_title._accepts_scrollarea = False
        self._frame_title._accepts_title = False
        self._frame_title._menu_can_be_none_pack = True
        self._frame_title._menu = self._menu
        self._frame_title.set_attribute('buttons_alignment', title_buttons_alignment)
        self._frame_title.set_attribute('pbottom', pad_outer[2] - pad_inner[2])
        self._frame_title.set_cursor(cursor if cursor is not None else self._cursor)
        self._frame_title.set_padding(padding_inner)
        self._frame_title.set_scrollarea(self._scrollarea)
        self._frame_title.translate(pad_outer[3] + pad_inner[3], pad_outer[0] + pad_inner[0])
        self._frame_title.set_controls(
            joystick=self._joystick_enabled,
            mouse=self._mouse_enabled,
            touchscreen=self._touchscreen_enabled,
            keyboard=self._keyboard_enabled
        )
        if self._frame is not None:
            self._frame_title.set_frame(self._frame)
        self._frame_title._update__repr___(self)

        # Store constructor
        self._frame_title.set_attribute(
            'constructor', {
                'title': title,
                'cursor': cursor,
                'background_color': background_color,
                'draggable': draggable,
                'padding_inner': padding_inner,
                'padding_outer': padding_outer,
                'title_alignment': title_alignment,
                'title_buttons_alignment': title_buttons_alignment,
                'title_font': title_font,
                'title_font_color': title_font_color,
                'title_font_size': title_font_size
            }
        )

        # Create frame title background rect
        title_bg = make_surface(
            self.get_width(),
            title_label.get_height() + pad_outer[0] + pad_outer[2] + pad_inner[0] + pad_inner[2]
        )

        # Blit frame bgrect if scrollable
        if self._frame_scrollarea is not None and self.is_scrollable:
            area_color = self._background_color
            if isinstance(area_color, BaseImage):
                area_color.draw(title_bg, area=title_bg.get_rect())
            elif area_color is not None:
                title_bg.fill(area_color, rect=title_bg.get_rect())
        self._frame_title.get_decorator().add_surface(-title_bg.get_width() / 2,
                                                      -title_bg.get_height() / 2 + 1,
                                                      title_bg)

        # Set background
        is_color = True
        try:
            assert_color(background_color, warn_if_invalid=False)
        except (ValueError, AssertionError):
            is_color = False
        if isinstance(background_color, pygame_menu.BaseImage) or is_color:
            self._frame_title.set_background_color(background_color)
        else:  # Is gradient
            assert isinstance(background_color, tuple)
            assert len(background_color) == 4, \
                'gradient color type must has 4 components (from color, to color, ' \
                'vertical, forward)'
            w, h = self._frame_title.get_size()
            new_surface = make_surface(w, h)
            fill_gradient(
                surface=new_surface,
                color=background_color[0],
                gradient=background_color[1],
                vertical=background_color[2],
                forward=background_color[3]
            )
            self._frame_title.get_decorator().add_surface(-w / 2, -h / 2 + 1, new_surface)

        # Pack title
        self._frame_title.pack(title_label, align=title_alignment)

        self._has_title = True
        self._render()
        self.set_position(self._position[0], self._position[1])
        self.force_menu_surface_update()

        # Title adds frame to scrollable frames even if not scrollable
        self._append_menu_update_frame(self)

        return self._frame_title

    def remove_title(self) -> 'Frame':
        """
        Remove title from current Frame.

        :return: Self reference
        """
        if not self._accepts_title:
            raise _FrameDoNotAcceptTitle(f'{self.get_class_id()} does not accept a title')
        if self._has_title:
            self._frame_title = None
            self._has_title = False
        if not self.is_scrollable:
            self._remove_menu_update_frame(self)
        self._draggable = False
        self._render()
        self.force_menu_surface_update()
        return self

    def add_title_generic_button(
            self,
            button: 'Button',
            margin: Vector2NumberType = (0, 0)
    ) -> 'Frame':
        """
        Add button to title. Button kwargs receive the ``button`` reference and
        the Frame reference in ``frame`` argument, such as:

        .. code-block:: python

            onreturn_button_callback(*args, frame=Frame, button=Button, **kwargs)

        :param button: Button object
        :param margin: Pack margin on x-axis and y-axis (x, y) in px
        :return: Self reference
        """
        if not self._accepts_title:
            raise _FrameDoNotAcceptTitle(f'{self.get_class_id()} does not accept a title')
        assert self._has_title, \
            f'{self.get_class_id()} does not have any title, call set_title(...) beforehand'
        assert isinstance(button, Button)
        assert button.get_menu() is None, \
            f'{button.get_class_id()} menu reference must be None'
        assert button.configured, \
            f'{button.get_class_id()} must be configured before addition to title'
        assert button.get_frame() is None, \
            f'{button.get_class_id()} frame must be None'

        # Check sizing
        total_title_height = self._frame_title.get_height(apply_padding=False)
        assert button.get_height() <= total_title_height, \
            f'{button.get_class_id()} height ({button.get_height()}) must be lower' \
            f' than frame title height ({total_title_height})'

        # Add frame to button kwargs
        if 'frame' in button._kwargs.keys():
            raise ValueError(f'{button.get_class_id()} already has "frame" kwargs option')
        button._kwargs['frame'] = self
        if 'button' in button._kwargs.keys():
            raise ValueError(f'{button.get_class_id()} already has "button" kwargs option')
        button._kwargs['button'] = button

        # Pack
        align = self._frame_title.get_attribute('buttons_alignment')
        button.set_attribute('align', align)
        button.set_attribute('margin', margin)
        self._frame_title.pack(button, align=align, margin=margin)
        self._frame_title.update_position()

        return self

    def add_title_button(
            self,
            style: FrameTitleButtonType,
            callback: CallbackType,
            background_color: ColorInputType = (150, 150, 150),
            cursor: CursorInputType = CURSOR_HAND,
            margin: Vector2NumberType = (4, 0),
            symbol_color: ColorInputType = (0, 0, 0),
            symbol_height: NumberType = 0.75,
            symbol_margin: int = 4
    ) -> 'Button':
        """
        Add predefined button to title. The button kwargs receive the ``button``
        reference and the Frame reference in ``frame`` argument, such as:

        .. code-block:: python

            onreturn_button_callback(*args, frame=Frame, button=Button, **kwargs)

        :param style: Style of the button (changes the symbol)
        :param callback: Callback of the button if pressed
        :param cursor: Button cursor
        :param background_color: Button background color
        :param margin: Pack margin on x-axis and y-axis (x, y) in px
        :param symbol_color: Color of the symbol
        :param symbol_height: Symbol height factor, if ``1.0`` uses 100% of the button height
        :param symbol_margin: Symbol margin in px
        :return: Added button
        """
        if not self._accepts_title:
            raise _FrameDoNotAcceptTitle(f'{self.get_class_id()} does not accept a title')
        assert self._has_title, \
            f'{self.get_class_id()} does not have any title, call set_title(...) beforehand'
        assert isinstance(symbol_height, NumberInstance) and 0 <= symbol_height <= 1
        assert isinstance(symbol_margin, int) and 0 <= symbol_margin
        h = self._frame_title.get_height(apply_padding=False) * symbol_height
        dh = self._frame_title.get_height(apply_padding=False) * (1 - symbol_height)
        assert symbol_margin < h / 2
        if dh > 0:
            dh += 1

        # Create button
        btn = Button('', onreturn=callback,
                     button_id=self._frame_title._id + '+button-' + uuid4(short=True))
        btn.set_padding(h / 2)
        btn.translate(0, dh / 2)
        btn.set_cursor(cursor)
        btn.set_background_color(background_color)
        btn.configured = True
        btn._update__repr___(self)

        # Create style decoration
        btn_rect = btn.get_rect()
        btn_rect.x = 0
        btn_rect.y = 0
        t = symbol_margin
        border = 1

        if style == FRAME_TITLE_BUTTON_CLOSE:
            style_pos = (
                (btn_rect.left + t, btn_rect.top + t),
                (btn_rect.centerx, btn_rect.centery),
                (btn_rect.right - t, btn_rect.top + t),
                (btn_rect.centerx, btn_rect.centery),
                (btn_rect.right - t, btn_rect.bottom - t),
                (btn_rect.centerx, btn_rect.centery),
                (btn_rect.left + t, btn_rect.bottom - t),
                (btn_rect.centerx, btn_rect.centery),
                (btn_rect.left + t, btn_rect.top + t)
            )
            border = 0

        elif style == FRAME_TITLE_BUTTON_MAXIMIZE:
            style_pos = (
                (btn_rect.left + t, btn_rect.bottom - t),
                (btn_rect.right - t, btn_rect.bottom - t),
                (btn_rect.right - t, btn_rect.top + t),
                (btn_rect.left + t, btn_rect.top + t)
            )

        elif style == FRAME_TITLE_BUTTON_MINIMIZE:
            style_pos = (
                (btn_rect.left + t, btn_rect.centery + border),
                (btn_rect.right - t, btn_rect.centery + border)
            )

        else:
            raise ValueError(f'unknown button style "{style}"')

        # Draw style
        style_surface = make_surface(h, h, alpha=True)
        # noinspection PyArgumentList
        pygame.draw.polygon(style_surface, symbol_color, style_pos, border)
        btn.get_decorator().add_surface(0, 0, surface=style_surface, centered=True)

        self.add_title_generic_button(btn, margin)
        return btn

    def get_title(self) -> str:
        if not self._has_title:
            # raise ValueError(f'{self.get_class_id()} does not have any title')
            return ''
        return self._title

    def get_inner_size(self) -> Tuple2IntType:
        """
        Return Frame inner size (width, height).

        :return: Size tuple in px
        """
        return self._width, self._height

    def _get_menu_update_frames(self) -> List['pygame_menu.widgets.Frame']:
        """
        Return the menu update frames list.

        .. warning::

            Use with caution.

        :return: Frame update list if the menu reference is not ``None``, else, return an empty list
        """
        if self._menu is not None:
            return self._menu._update_frames
        return []

    def _sort_menu_update_frames(self) -> None:
        """
        Sort the menu update frames (frames which receive updates).

        :return: None
        """
        if self._menu is not None:
            self._menu._sort_update_frames()

    def _append_menu_update_frame(self, frame: 'Frame') -> None:
        """
        Append update frame to menu and sort.

        :param frame: Frame to append
        :return: None
        """
        assert isinstance(frame, Frame)
        update_frames = self._get_menu_update_frames()
        if frame not in update_frames:
            update_frames.append(frame)
            self._sort_menu_update_frames()

    def _remove_menu_update_frame(self, frame: 'Frame') -> None:
        """
        Remove update frame to menu and sort.

        :param frame: Frame to append
        :return: None
        """
        assert isinstance(frame, Frame)
        update_frames = self._get_menu_update_frames()
        if frame in update_frames:
            update_frames.remove(frame)

    def on_remove_from_menu(self) -> 'Frame':
        for w in self.get_widgets(unpack_subframes=False):
            self.unpack(w)
        self.update_indices()
        return self

    def set_menu(self, menu: Optional['pygame_menu.Menu']) -> 'Frame':
        # If menu is set, remove from previous scrollable if enabled
        self._remove_menu_update_frame(self)

        # Update menu
        super(Frame, self).set_menu(menu)

        # Add self to scrollable
        if self.is_scrollable:
            self._append_menu_update_frame(self)

        return self

    def relax(self, relax: bool = True) -> 'Frame':
        """
        Set relax status. If ``True`` Frame ignores sizing checks.

        :param relax: Relax status
        :return: Self reference
        """
        assert isinstance(relax, bool)
        self._relax = relax
        return self

    def get_max_size(self) -> Tuple2IntType:
        """
        Return the max size of the frame.

        :return: Max (width, height) in px
        """
        if self._frame_scrollarea is not None:
            return self._frame_scrollarea.get_size(inner=True)
        return self.get_size()

    def make_scrollarea(
            self,
            max_width: Optional[NumberType],
            max_height: Optional[NumberType],
            scrollarea_color: Optional[Union[ColorInputType, 'pygame_menu.BaseImage']],
            scrollbar_color: ColorInputType,
            scrollbar_cursor: CursorInputType,
            scrollbar_shadow: bool,
            scrollbar_shadow_color: ColorInputType,
            scrollbar_shadow_offset: int,
            scrollbar_shadow_position: str,
            scrollbar_slider_color: ColorInputType,
            scrollbar_slider_hover_color: ColorInputType,
            scrollbar_slider_pad: NumberType,
            scrollbar_thick: NumberType,
            scrollbars: Union[str, Tuple[str, ...]]
    ) -> 'Frame':
        """
        Make the scrollarea of the frame.

        :param max_width: Maximum width of the scrollarea in px
        :param max_height: Maximum height of the scrollarea in px
        :param scrollarea_color: Scroll area color or image. If ``None`` area is transparent
        :param scrollbar_color: Scrollbar color
        :param scrollbar_cursor: Scrollbar cursor
        :param scrollbar_shadow: Indicate if a shadow is drawn on each scrollbar
        :param scrollbar_shadow_color: Color of the shadow of each scrollbar
        :param scrollbar_shadow_offset: Offset of the scrollbar shadow in px
        :param scrollbar_shadow_position: Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
        :param scrollbar_slider_color: Color of the sliders
        :param scrollbar_slider_hover_color: Color of the slider if hovered or clicked
        :param scrollbar_slider_pad: Space between slider and scrollbars borders in px
        :param scrollbar_thick: Scrollbar thickness in px
        :param scrollbars: Positions of the scrollbars. See :py:mod:`pygame_menu.locals`
        :return: Self reference
        """
        if not self._accepts_scrollarea:
            raise _FrameDoNotAcceptScrollarea(f'{self.get_class_id()} does not accept a scrollarea')
        assert len(self._widgets.keys()) == 0, 'frame widgets must be empty if creating the scrollarea'
        assert self.configured, 'frame must be configured before adding the scrollarea'
        if max_width is None:
            max_width = self._width
        if max_height is None:
            max_height = self._height
        assert isinstance(max_width, NumberInstance)
        assert isinstance(max_height, NumberInstance)
        assert 0 < max_width <= self._width, \
            f'scroll area width ({max_width}) cannot exceed frame width ({self._width})'
        assert 0 < max_height <= self._height, \
            f'scroll area height ({max_height}) cannot exceed frame height ({self._height})'
        # if not self._relax:
        #     pass
        # else:
        #     max_height = min(max_height, self._height)
        #     max_width = min(max_width, self._width)

        sx = 0 if self._width == max_width else scrollbar_thick
        sy = 0 if self._height == max_height else scrollbar_thick

        if self._width > max_width or self._height > max_height:
            self.is_scrollable = True
            self.set_padding(0)
        else:
            # Configure size
            self._frame_size = (self._width, self._height)
            self._frame_scrollarea = None

            # If in previous scrollable frames
            if self.is_scrollable:
                self._remove_menu_update_frame(self)

            self.is_scrollable = False
            return self

        # Create area object
        self._frame_scrollarea = pygame_menu._scrollarea.ScrollArea(
            area_color=scrollarea_color,
            area_height=max_height + sx,
            area_width=max_width + sy,
            controls_joystick=self._joystick_enabled,
            controls_keyboard=self._keyboard_enabled,
            controls_mouse=self._mouse_enabled,
            controls_touchscreen=self._touchscreen_enabled,
            parent_scrollarea=self._scrollarea,
            scrollbar_color=scrollbar_color,
            scrollbar_cursor=scrollbar_cursor,
            scrollbar_slider_color=scrollbar_slider_color,
            scrollbar_slider_hover_color=scrollbar_slider_hover_color,
            scrollbar_slider_pad=scrollbar_slider_pad,
            scrollbar_thick=scrollbar_thick,
            scrollbars=scrollbars,
            shadow=scrollbar_shadow,
            shadow_color=scrollbar_shadow_color,
            shadow_offset=scrollbar_shadow_offset,
            shadow_position=scrollbar_shadow_position
        )

        # Store constructor data
        self._frame_scrollarea.set_attribute(
            'constructor',
            {
                'scrollarea_color': scrollarea_color,
                'scrollbar_color': scrollbar_color,
                'scrollbar_cursor': scrollbar_cursor,
                'scrollbar_shadow': scrollbar_shadow,
                'scrollbar_shadow_color': scrollbar_shadow_color,
                'scrollbar_shadow_offset': scrollbar_shadow_offset,
                'scrollbar_shadow_position': scrollbar_shadow_position,
                'scrollbar_slider_color': scrollbar_slider_color,
                'scrollbar_slider_hover_color': scrollbar_slider_hover_color,
                'scrollbar_slider_pad': scrollbar_slider_pad,
                'scrollbar_thick': scrollbar_thick,
                'scrollbars': scrollbars
            }
        )

        if self._width == max_width:
            self._frame_scrollarea.hide_scrollbars(ORIENTATION_HORIZONTAL)
        if self._height == max_height:
            self._frame_scrollarea.hide_scrollbars(ORIENTATION_VERTICAL)

        # Create surface
        self._surface = make_surface(self._width, self._height, alpha=True)

        # Configure area
        self._frame_scrollarea.set_world(self._surface)

        # Configure size
        self._frame_size = (max_width + sy, max_height + sx)

        # Set menu
        self._frame_scrollarea.set_menu(self._menu)

        # If has title
        if self._has_title:
            warn(f'previous {self.get_class_id()} title has been removed')
            self.remove_title()

        return self

    def get_indices(self) -> Tuple[int, int]:
        """
        Return first and last selectable indices tuple.

        :return: First, Last widget selectable indices
        """
        return self.first_index, self.last_index

    def get_total_packed(self) -> int:
        """
        Return the total number of packed widgets.

        :return: Number of packed widgets
        """
        return len(self._widgets.values())

    def select(self, *args, **kwargs) -> 'Frame':
        return self

    def set_selection_effect(self, *args, **kwargs) -> 'Frame':
        pass

    def _apply_font(self) -> None:
        pass

    def _title_height(self) -> int:
        """
        Return the title height.

        :return: Title height in px
        """
        if not self._has_title or self._frame_title is None:
            return 0
        h = self._frame_title.get_height()
        h += self._frame_title.get_translate()[1]
        h += self._frame_title.get_attribute('pbottom')  # Bottom padding
        return h

    def _render(self) -> None:
        self._rect.height = self._frame_size[1] + self._title_height()
        self._rect.width = self._frame_size[0]

    def _draw(self, *args, **kwargs) -> None:
        pass

    def scale(self, *args, **kwargs) -> 'Frame':
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args, **kwargs) -> 'Frame':
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args, **kwargs) -> 'Frame':
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args, **kwargs) -> 'Frame':
        raise WidgetTransformationNotImplemented()

    def flip(self, *args, **kwargs) -> 'Frame':
        raise WidgetTransformationNotImplemented()

    def get_decorator(self) -> 'Decorator':
        """
        Frame decorator belongs to the scrollarea decorator if enabled.

        :return: ScrollArea decorator
        """
        if self.is_scrollable:
            return self._frame_scrollarea.get_decorator()
        return self._decorator

    def get_index(self, widget: 'Widget') -> int:
        """
        Get index of the given widget within the widget list. Throws
        ``IndexError`` if widget does not exist.

        :param widget: Widget
        :return: Index
        """
        w = self.get_widgets(unpack_subframes=False)
        try:
            return w.index(widget)
        except ValueError:
            raise IndexError(f'{widget.get_class_id()} widget does not exist on {self.get_class_id()}')

    def set_position(self, x: NumberType, y: NumberType) -> 'Frame':
        if self._has_title:
            pad = self.get_padding()  # top, right, bottom, left
            tx, ty = self.get_translate()
            self._frame_title.set_position(x - pad[3] + tx, y - pad[0] + ty)
            for w in self._frame_title.get_widgets():
                w._set_position_relative_to_frame()
        super(Frame, self).set_position(x, y)
        if self.is_scrollable:
            self._frame_scrollarea.set_position(self._rect.x,
                                                self._rect.y + self._title_height())
        return self

    def draw(self, surface: 'pygame.Surface') -> 'Frame':
        if not self.is_visible():
            return self

        selected_widget: Optional['Widget'] = None

        # Simple case, no scrollarea
        if not self.is_scrollable:
            self.last_surface = surface
            self._draw_shadow(surface)
            self._draw_background_color(surface)
            self._decorator.draw_prev(surface)
            for widget in self._widgets.values():
                if widget.is_selected():
                    selected_widget = widget
                widget.draw(surface)
            self._draw_border(surface)
            self._decorator.draw_post(surface)

        # Scrollarea
        else:
            self.last_surface = self._surface
            self._surface.fill((255, 255, 255, 0))
            self._draw_shadow(self._surface, rect=self._real_rect)
            self._draw_background_color(self._surface, rect=self._real_rect)
            scrollarea_decorator = self.get_decorator()
            scrollarea_decorator.force_cache_update()
            scrollarea_decorator.draw_prev(self._surface)
            for widget in self._widgets.values():
                if widget.is_selected():
                    selected_widget = widget
                widget.draw(self._surface)
            self._frame_scrollarea.draw(surface)
            self._draw_border(surface)

        # If title
        if self._has_title:
            self._frame_title.draw(surface)

        self.apply_draw_callbacks()

        # Stores selected widget
        self.selected_widget_draw = selected_widget, self.last_surface

        return self

    def _get_ht(self, widget: 'Widget', a: str) -> int:
        """
        Return the horizontal translation for widget.

        :param widget: Widget
        :param a: Horizontal alignment
        :return: Px
        """
        w = widget.get_width()
        # Some systems introduce 1px margin
        if w > (self._width + 1) and not self._relax:
            raise _FrameSizeException(
                f'{widget.get_class_id()} width ({w}) is greater than {self.get_class_id()}'
                f' width ({self._width}), try using widget.set_max_width(...) for '
                f'avoiding this issue, or set the widget as floating'
            )
        if a == ALIGN_CENTER:
            return int((self._width - w) / 2)
        elif a == ALIGN_RIGHT:
            return self._width - w
        else:  # Alignment left
            return 0

    def _get_vt(self, widget: 'Widget', v: str) -> int:
        """
        Return vertical translation for widget.

        :param widget: Widget
        :param v: Vertical position
        :return: Px
        """
        h = widget.get_height()
        if h > (self._height + 1) and not self._relax:
            raise _FrameSizeException(
                f'{widget.get_class_id()} height ({h}) is greater than {self.get_class_id()}'
                f' height ({self._height}), try using widget.set_max_height(...) '
                f'for avoiding this issue, or set the widget as floating'
            )
        if v == POSITION_CENTER:
            return int((self._height - h) / 2)
        elif v == POSITION_SOUTH:
            return self._height - h
        else:  # Position north
            return 0

    def _update_position_horizontal(self) -> None:
        """
        Compute widget position for horizontal orientation.

        :return: None
        """
        x_left = 0  # Total added to left
        x_right = 0  # Total added to right
        w_center = 0

        for w in self._widgets.values():
            align, v_pos = self._widgets_props[w.get_id()]
            if not w.is_visible(check_frame=False) or w.is_floating():
                continue
            if align == ALIGN_CENTER:
                w_center += w.get_width() + w.get_margin()[0]
                continue
            elif align == ALIGN_LEFT:
                x_left += w.get_margin()[0]
                self._pos[w.get_id()] = (x_left,
                                         self._get_vt(w, v_pos) + w.get_margin()[1])
                x_left += w.get_width()
            elif align == ALIGN_RIGHT:
                x_right -= (w.get_width() + w.get_margin()[0])
                self._pos[w.get_id()] = (self._width + x_right,
                                         self._get_vt(w, v_pos) + w.get_margin()[1])
            dw = x_left - x_right
            if dw > self._width and not self._relax:
                raise _FrameSizeException(
                    f'{w.get_class_id()} width ({dw}) exceeds {self.get_class_id()}'
                    f' width ({self._width}). Set frame._relax=True to ignore this Exception'
                )

        # Now center widgets
        available = self._width - (x_left - x_right)
        if w_center > available and not self._relax:
            raise _FrameSizeException(
                f'cannot place center widgets as required width ({w_center}) is '
                f'greater than available ({available}) in {self.get_class_id()}.'
                f' Set frame._relax=True to ignore this Exception'
            )
        x_center = int(self._width / 2 - w_center / 2)
        for w in self._widgets.values():
            align, v_pos = self._widgets_props[w.get_id()]
            if not w.is_visible(check_frame=False) or w.is_floating():
                continue
            if align == ALIGN_CENTER:
                x_center += w.get_margin()[0]
                self._pos[w.get_id()] = (x_center,
                                         self._get_vt(w, v_pos) + w.get_margin()[1])
                x_center += w.get_width()

    def _update_position_vertical(self) -> None:
        """
        Compute widget position for vertical orientation.

        :return: None
        """
        y_top = 0  # Total added to top
        y_bottom = 0  # Total added to bottom
        w_center = 0
        for w in self._widgets.values():
            align, v_pos = self._widgets_props[w.get_id()]
            if not w.is_visible(check_frame=False) or w.is_floating():
                continue
            if v_pos == POSITION_CENTER:
                w_center += w.get_height() + w.get_margin()[1]
                continue
            elif v_pos == POSITION_NORTH:
                y_top += w.get_margin()[1]
                self._pos[w.get_id()] = (self._get_ht(w, align) + w.get_margin()[0], y_top)
                y_top += w.get_height()
            elif v_pos == POSITION_SOUTH:
                y_bottom -= (w.get_height() + w.get_margin()[1])
                self._pos[w.get_id()] = (self._get_ht(w, align) + w.get_margin()[0],
                                         self._height + y_bottom)
            dh = y_top - y_bottom
            if dh > self._height and not self._relax:
                raise _FrameSizeException(
                    f'{w.get_class_id()} height ({dh}) exceeds {self.get_class_id()}'
                    f' height ({self._height}). Set frame._relax=True to ignore '
                    f'this Exception'
                )

        # Now center widgets
        available = self._height - (y_top - y_bottom)
        if w_center > available and not self._relax:
            raise _FrameSizeException(
                f'cannot place center widgets as required height ({w_center}) is'
                f' greater than available ({available}) in {self.get_class_id()}.'
                f' Set frame._relax=True to ignore this Exception'
            )
        y_center = int(self._height / 2 - w_center / 2)
        for w in self._widgets.values():
            align, v_pos = self._widgets_props[w.get_id()]
            if not w.is_visible(check_frame=False) or w.is_floating():
                continue
            if v_pos == POSITION_CENTER:
                y_center += w.get_margin()[1]
                self._pos[w.get_id()] = (self._get_ht(w, align) + w.get_margin()[0],
                                         y_center)
                y_center += w.get_height()

    def update_position(self) -> 'Frame':
        """
        Update the position of each widget.

        :return: Self reference
        """
        if len(self._widgets) == 0:
            return self

        # Update position based on orientation
        if self._orientation == ORIENTATION_HORIZONTAL:
            self._update_position_horizontal()
        elif self._orientation == ORIENTATION_VERTICAL:
            self._update_position_vertical()

        # Apply position to each widget
        for w in self._widgets.keys():
            widget = self._widgets[w]
            if not widget.is_visible(check_frame=False):
                widget.set_position(0, 0)
                continue
            if widget.is_floating():
                tx = 0
                ty = 0
            else:
                tx, ty = self._pos[w]
            ty += self._title_height()
            if widget.get_menu() is None:  # Widget is only appended to Frame
                fx, fy = self.get_position()
                margin = widget.get_margin()
                padding = widget.get_padding()
                widget.set_position(fx + margin[0] + padding[3], fy + padding[0])
            if self.is_scrollable and isinstance(widget, Frame) and widget.is_scrollable:
                widget.get_scrollarea(inner=True).set_position(tx, ty)
            # If scrollarea, subtract this position to each widget
            if self._frame_scrollarea is not None:
                sx, sy = self._frame_scrollarea.get_position()
                tx -= sx
                ty -= sy
            widget._translate_virtual = (tx, ty)  # Translate to scrollarea

        # Check if control widget has changed positioning. This fixes centering issues
        if self._control_widget is not None:
            c_pos = self._control_widget.get_position()
            if self._control_widget_last_pos != c_pos:
                self._control_widget_last_pos = c_pos
                if self._recursive_render <= 100 and self._menu is not None:
                    self._menu.render()
                self._recursive_render += 1
            else:
                self._recursive_render = 0

        # If frame has title
        if self._has_title:
            self._frame_title.update_position()

        return self

    def get_widgets(
            self,
            unpack_subframes: bool = True,
            unpack_subframes_include_frame: bool = False,
            reverse: bool = False
    ) -> Tuple['Widget', ...]:
        """
        Get widgets as a tuple.

        :param unpack_subframes: If ``True`` add frame widgets instead of frame
        :param unpack_subframes_include_frame: If ``True`` the unpacked frame is also added to the widget list
        :param reverse: Reverse the returned tuple
        :return: Widget tuple
        """
        wtp = []
        for widget in self._widgets.values():
            if isinstance(widget, Frame) and unpack_subframes:
                if unpack_subframes_include_frame:
                    wtp.append(widget)
                ww = widget.get_widgets(
                    unpack_subframes=unpack_subframes,
                    unpack_subframes_include_frame=unpack_subframes_include_frame
                )
                for i in ww:
                    wtp.append(i)
                continue
            wtp.append(widget)
        if reverse:
            wtp.reverse()
        return tuple(wtp)

    def clear(self) -> Union['Widget', Tuple['Widget', ...]]:
        """
        Unpack all widgets within frame.

        :return: Removed widgets
        """
        unpacked = []
        for w in self.get_widgets(unpack_subframes=False):
            self.unpack(w)
            unpacked.append(w)
        return tuple(unpacked)

    def resize(
            self,
            width: NumberType,
            height: NumberType,
            max_width: Optional[NumberType] = None,
            max_height: Optional[NumberType] = None
    ) -> 'Frame':
        """
        Resize the Frame.

        :param width: New width in px. Horizontal padding will be subtracted
        :param height: New height in px. Vertical padding will be subtracted
        :param max_width: Max frame width if the Frame is scrollable. If ``None`` the same width will be used
        :param max_height: Max frame height if the Frame is scrollable. If ``None`` the same height will be used
        :return: Self reference
        """
        assert isinstance(width, NumberInstance)
        assert isinstance(height, NumberInstance)

        pad_h = self._padding[1] + self._padding[3]
        pad_v = self._padding[0] + self._padding[2]

        # Subtract padding
        width -= pad_h
        height -= pad_v

        # Check size
        assert width > 0 and height > 0, 'new width and height must be greater than zero'

        # Update width/height
        if width < self._width or height < self._height:
            self.relax()
        self._frame_size = (width, height)  # Size of the frame, set in make_scrollarea
        self._height = int(height)
        self._real_rect = pygame.Rect(0, 0, width, height)
        self._width = int(width)

        # Get previous buttons if has title
        prev_has_title = self._has_title
        prev_title_frame = self._frame_title
        prev_title_buttons = list(self._frame_title.get_widgets()) if self._has_title else []
        if len(prev_title_buttons) >= 1:  # Pop label
            prev_title_buttons.pop(0)

        # Make scrollable if scrollable
        if self.is_scrollable:
            assert self._frame_scrollarea.has_attribute('constructor'), \
                'frame scrollarea does not have the "constructor" attribute. Make ' \
                'sure the scrollarea has been created using make_scrollarea() method'
            kwargs: Dict[str, Any] = self._frame_scrollarea.get_attribute('constructor')
            if max_width is None:
                max_width = width
            if max_height is None:
                max_height = height
            self.make_scrollarea(
                max_height=max_height,
                max_width=max_width,
                scrollarea_color=kwargs['scrollarea_color'],
                scrollbar_color=kwargs['scrollbar_color'],
                scrollbar_cursor=kwargs['scrollbar_cursor'],
                scrollbar_shadow=kwargs['scrollbar_shadow'],
                scrollbar_shadow_color=kwargs['scrollbar_shadow_color'],
                scrollbar_shadow_offset=kwargs['scrollbar_shadow_offset'],
                scrollbar_shadow_position=kwargs['scrollbar_shadow_position'],
                scrollbar_slider_color=kwargs['scrollbar_slider_color'],
                scrollbar_slider_hover_color=kwargs['scrollbar_slider_hover_color'],
                scrollbar_slider_pad=kwargs['scrollbar_slider_pad'],
                scrollbar_thick=kwargs['scrollbar_thick'],
                scrollbars=kwargs['scrollbars']
            )
        else:
            assert max_width is None and max_height is None, \
                'if previous Frame is not scrollable (make_scrollarea has been ' \
                'called) max_width and max_height must be None'

        # If had title, remove and create a new one
        if self._has_title:
            self.remove_title()
        if prev_has_title:
            for btn in prev_title_buttons:
                prev_title_frame.unpack(btn)
                btn.set_margin(0, 0)
                btn.set_float(False)
            assert prev_title_frame.has_attribute('constructor'), \
                'frame title does not have the attribute "constructor". Make sure ' \
                'the frame title has been created through set_title() method.'
            kwargs = prev_title_frame.get_attribute('constructor')
            new_title_frame = self.set_title(
                title=kwargs['title'],
                cursor=kwargs['cursor'],
                background_color=kwargs['background_color'],
                draggable=kwargs['draggable'],
                padding_inner=kwargs['padding_inner'],
                padding_outer=kwargs['padding_outer'],
                title_alignment=kwargs['title_alignment'],
                title_buttons_alignment=kwargs['title_buttons_alignment'],
                title_font=kwargs['title_font'],
                title_font_color=kwargs['title_font_color'],
                title_font_size=kwargs['title_font_size']
            )

            # Pack previous buttons
            # prev_title_buttons.reverse()
            for btn in prev_title_buttons:
                align = btn.get_attribute('align', kwargs['title_buttons_alignment'])
                margin = btn.get_attribute('margin', (0, 0))
                new_title_frame.pack(btn, align=align, margin=margin)

        # Force render
        self._render()
        self.force_menu_surface_update()

        return self

    def unfloat(self) -> 'Frame':
        """
        Disable float status for each subwidget.

        :return: Self reference
        """
        for w in self.get_widgets(unpack_subframes_include_frame=True):
            w.set_float(False)
        if self._menu is not None:
            self._menu.render()
            self._menu.scroll_to_widget(None)
        return self

    def get_scrollarea(self, inner: bool = False) -> Optional['pygame_menu._scrollarea.ScrollArea']:
        """
        Return the scrollarea object.

        :param inner: If ``True`` return the inner scrollarea
        :return: ScrollArea object
        """
        if inner:
            return self._frame_scrollarea
        return self._scrollarea

    def set_frame(self, frame: 'pygame_menu.widgets.Frame') -> 'Frame':
        assert self != frame, \
            f'{frame.get_class_id()} cannot set itself as a frame'
        super(Frame, self).set_frame(frame)
        if self._frame_title is not None:
            self._frame_title.set_frame(frame)
        return self

    def set_scrollarea(self, scrollarea: Optional['pygame_menu._scrollarea.ScrollArea']) -> None:
        if scrollarea is not None:
            assert scrollarea != self._frame_scrollarea, \
                f'scrollarea cannot be {self.get_class_id()}._frame_scrollarea {scrollarea.get_class_id()}'
        self._scrollarea = scrollarea
        if self._frame_scrollarea is not None:
            self._frame_scrollarea.set_parent_scrollarea(scrollarea)
        else:
            for w in self.get_widgets(unpack_subframes=False):
                w.set_scrollarea(scrollarea)
        if self._frame_title is not None:
            self._frame_title.set_scrollarea(scrollarea)

    def scrollh(self, value: NumberType) -> 'Frame':
        """
        Scroll to horizontal value if frame is scrollable.

        :param value: Horizontal scroll value, if ``0`` scroll to left; ``1`` scroll to right
        :return: Self reference
        """
        if self._frame_scrollarea is not None:
            self._frame_scrollarea.scroll_to(ORIENTATION_HORIZONTAL, value)
        return self

    def scrollv(self, value: NumberType) -> 'Frame':
        """
        Scroll to vertical value if frame is scrollable.

        :param value: Vertical scroll value, if ``0`` scroll to top; ``1`` scroll to bottom
        :return: Self reference
        """
        if self._frame_scrollarea is not None:
            self._frame_scrollarea.scroll_to(ORIENTATION_VERTICAL, value)
        return self

    def get_scroll_value_percentage(self, orientation: str) -> float:
        """
        Get the scroll value in percentage, if ``0`` the scroll is at top/left,
        ``1`` bottom/right.

        .. note::

            If ScrollArea does not contain such orientation scroll, or frame is not scrollable,
            ``-1`` is returned.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :return: Value from ``0`` to ``1``
        """
        if self._frame_scrollarea is not None:
            return self._frame_scrollarea.get_scroll_value_percentage(orientation)
        return -1

    def unpack(self, widget: 'Widget') -> 'Frame':
        """
        Unpack widget from Frame. If widget does not exist, raises ``ValueError``.
        Unpacked widgets adopt a floating position and are moved to the last position
        of the widget list of Menu

        :param widget: Widget to unpack
        :return: Unpacked widget
        """
        assert widget != self, 'frame cannot unpack itself'
        assert len(self._widgets) > 0, 'frame is empty'
        wid = widget.get_id()
        if wid not in self._widgets.keys():
            raise ValueError(f'{widget.get_class_id()} does not exist in {self.get_class_id()}')
        assert widget._frame == self, 'widget frame differs from current'
        widget.set_float()
        if self._menu is not None:
            widget.set_scrollarea(self._menu.get_scrollarea())
        widget._frame = None
        widget._translate_virtual = (0, 0)
        del self._widgets[wid]
        try:
            del self._pos[wid]
        except KeyError:
            pass

        # Move widget to the last position of widget list
        menu_widgets = self._get_menu_widgets()
        if widget.get_menu() == self._menu and widget in menu_widgets:
            self._menu._validate_frame_widgetmove = False
            try:
                self._menu.move_widget_index(widget, render=False)
            # Assertion error if moving widget (last) to same position (last)
            except (ValueError, AssertionError):
                pass
            if isinstance(widget, Frame):
                widgets = widget.get_widgets(unpack_subframes_include_frame=True)
                for w in widgets:
                    if w.get_menu() is None or w not in menu_widgets:
                        continue
                    self._menu.move_widget_index(w, render=False)
            self._menu._validate_frame_widgetmove = True

        # Check if frame contains more frames
        self._has_frames = False
        for k in self.get_widgets(unpack_subframes=False):
            if isinstance(k, Frame):
                self._has_frames = True
                break

        # Update selected
        if self._menu is not None:
            self._menu.move_widget_index(None, update_selected_index=True)

        # Update indices
        self.update_indices()

        # Render menu
        self._menu_render()

        if self._control_widget == widget:
            self._control_widget = None
            self._control_widget_last_pos = None
            for w in self.get_widgets():
                if w.get_menu() is not None:
                    self._control_widget = w
                    self._control_widget_last_pos = self._control_widget.get_position()
                    break

        if widget.is_selected():
            widget.scroll_to_widget()

        if len(self._widgets) == 0:  # Scroll to top
            self.scrollv(0)
            self.scrollh(0)

        if isinstance(widget, Frame):
            self._sort_menu_update_frames()

        # Update widget leave
        check_widget_mouseleave()

        return widget

    def pack(
            self,
            widget: Union['Widget', List['Widget'], Tuple['Widget', ...]],
            align: str = ALIGN_LEFT,
            vertical_position: str = POSITION_NORTH,
            margin: Vector2NumberType = (0, 0)
    ) -> Union['Widget', List['Widget'], Tuple['Widget', ...], Any]:
        """
        Packs widget in the frame line. To pack a widget it has to be already
        appended to Menu, and the Menu must be the same as the frame.

        Packing is added to the same line, for example if three LEFT widgets are
        added:

            .. code-block:: python

                <frame horizontal>
                frame.pack(W1, alignment=ALIGN_LEFT, vertical_position=POSITION_NORTH)
                frame.pack(W2, alignment=ALIGN_LEFT, vertical_position=POSITION_CENTER)
                frame.pack(W3, alignment=ALIGN_LEFT, vertical_position=POSITION_SOUTH)

                ----------------
                |W1            |
                |   W2         |
                |      W3      |
                ----------------

        Another example:

            .. code-block:: python

                <frame horizontal>
                frame.pack(W1, alignment=ALIGN_LEFT)
                frame.pack(W2, alignment=ALIGN_CENTER)
                frame.pack(W3, alignment=ALIGN_RIGHT)

                ----------------
                |W1    W2    W3|
                ----------------

            .. code-block:: python

                <frame vertical>
                frame.pack(W1, alignment=ALIGN_LEFT)
                frame.pack(W2, alignment=ALIGN_CENTER)
                frame.pack(W3, alignment=ALIGN_RIGHT)

                --------
                |W1    |
                |  W2  |
                |    W3|
                --------

        .. note::

            Frame does not consider previous widget margin. For such purpose, use
            ``margin`` pack parameter.

        .. note::

            It is recommended to force menu rendering after packing all widgets.

        .. note::

            Packing applies a virtual translation to the widget, previous translation
            is not modified.

        .. note::

            Widget floating is also considered within frames. If a widget is floating,
            it does not add any size to the respective positioning.

        :param widget: Widget to be packed
        :param align: Widget alignment. See :py:mod:`pygame_menu.locals`
        :param vertical_position: Vertical position of the widget within frame. Only valid: north, center, and south. See :py:mod:`pygame_menu.locals`
        :param margin: (left, top) margin of added widget in px. It overrides the previous widget margin
        :return: Added widget references
        """
        assert self._menu is not None or self._menu_can_be_none_pack, \
            f'{self.get_class_id()} menu must be set before packing widgets'
        if isinstance(widget, VectorInstance):
            for w in widget:
                self.pack(widget=w, align=align, vertical_position=vertical_position)
            return widget
        assert isinstance(widget, Widget)
        if isinstance(widget, Frame):
            assert widget.get_menu() is not None or self._menu_can_be_none_pack, \
                f'{widget.get_class_id()} menu cannot be None'
        assert widget.get_id() not in self._widgets.keys(), \
            f'{widget.get_class_id()} already exists in {self.get_class_id()}'
        assert widget.get_menu() == self._menu or widget.get_menu() is None, \
            'widget menu to be added to frame must be in same menu as frame, or ' \
            'it can have any Menu instance'
        assert widget.get_frame() is None, \
            f'{widget.get_class_id()} is already packed in {widget.get_frame().get_class_id()}'
        assert_alignment(align)
        assert vertical_position in (POSITION_NORTH, POSITION_CENTER, POSITION_SOUTH), \
            'vertical position must be NORTH, CENTER, or SOUTH'
        assert_vector(margin, 2)
        assert widget.configured, \
            f'{widget.get_class_id()} must be configured before packing'

        if widget.get_margin() != (0, 0) and self._pack_margin_warning:
            warn(
                f'{widget.get_class_id()} margin should be (0, 0) if packed, but'
                f' received {widget.get_margin()}; {self.get_class_id()}.pack() '
                f'does not consider previous widget margin. Set '
                f'frame._pack_margin_warning=False to hide this warning'
            )

        if isinstance(widget, Frame):
            widget.update_indices()

        widget.set_frame(self)
        widget.set_margin(*margin)
        if self._frame_scrollarea is not None:
            widget.set_scrollarea(self._frame_scrollarea)
        else:
            widget.set_scrollarea(self._scrollarea)
        if self.is_scrollable or self._has_title or isinstance(widget, Frame):
            self._sort_menu_update_frames()
        self._widgets[widget.get_id()] = widget
        self._widgets_props[widget.get_id()] = (align, vertical_position)

        # Sort widgets to keep selection order
        menu_widgets = self._get_menu_widgets()
        if widget.get_menu() is not None and widget in menu_widgets:
            self._menu._validate_frame_widgetmove = False
            widgets_list = list(self._widgets.values())

            # Move frame to last
            if len(self._widgets) > 1:
                w_last = widgets_list[-2]  # -1 is the last added
                for i in range(2, len(self._widgets)):
                    if w_last.get_menu() is None and len(self._widgets) > 2:
                        w_last = widgets_list[-(i + 1)]
                    else:
                        break

                # Check for last if w_last is frame
                while True:
                    if not (isinstance(w_last, Frame) and
                            w_last.get_indices() != (-1, -1)) or \
                            w_last.get_menu() is None:
                        break
                    w_last = menu_widgets[w_last.last_index]

                if w_last.get_menu() == self._menu:
                    self._menu.move_widget_index(self, w_last, render=False)

            # Swap
            self._menu.move_widget_index(widget, self, render=False)
            if isinstance(widget, Frame):
                reverse = menu_widgets.index(widget) == len(menu_widgets) - 1
                widgs = widget.get_widgets(unpack_subframes_include_frame=True,
                                           reverse=reverse)

                first_moved_widget = None
                last_moved_widget = None
                for w in widgs:
                    if w.get_menu() is None or w not in menu_widgets:
                        continue
                    self._menu.move_widget_index(w, self, render=False)
                    if first_moved_widget is None:
                        first_moved_widget = w
                    last_moved_widget = w

                swap_target = last_moved_widget if reverse else first_moved_widget
                if swap_target is not None:
                    menu_widgets.remove(widget)
                    menu_widgets.insert(menu_widgets.index(swap_target), widget)

            # Move widget to first
            menu_widgets.remove(self)
            for k in range(len(widgets_list)):
                if widgets_list[k].get_menu() == self._menu:
                    menu_widgets.insert(menu_widgets.index(widgets_list[k]), self)
                    break
            self._menu._validate_frame_widgetmove = True

            # Update control widget
            if self._control_widget is None:
                self._control_widget = widget
                self._control_widget_last_pos = self._control_widget.get_position()

        if isinstance(widget, Frame):
            self._has_frames = True

        # Update menu selected widget
        if self._menu is not None:
            self._menu.move_widget_index(None, update_selected_index=True)

        # Render is mandatory as it modifies row/column layout
        try:
            self.update_position()
            self._menu_render()
        except _FrameSizeException:
            self.unpack(widget)
            raise

        # Request scroll if widget is selected
        if widget.is_selected():
            widget.scroll_to_widget()
            widget.scroll_to_widget()

        # Update widget leave
        check_widget_mouseleave()

        return widget

    def contains_widget(self, widget: 'Widget') -> bool:
        """
        Return true if the frame contains the given widget.

        :param widget: Widget to check
        :return: ``True`` if widget within frame
        """
        return widget.get_frame() == self and widget.get_id() in self._widgets.keys()

    def hide(self) -> 'Frame':
        super(Frame, self).hide()
        if self._has_title:
            self._frame_title.hide()
        # sub-widgets cannot be hidden because some widgets compute sizing even
        # if the frame itself is hidden
        # for w in self.get_widgets(unpack_subframes=False):
        #     w.hide()
        return self

    def show(self) -> 'Frame':
        super(Frame, self).show()
        # same as hiding, sub-widgets should not be modified
        # for w in self.get_widgets(unpack_subframes=False):
        #     w.show()
        if self._has_title:
            self._frame_title.show()
        return self

    def update_indices(self) -> 'Frame':
        """
        Update first and last selectable widget index.

        :return: Self reference
        """
        # Public index update only triggered if frame does not contain subframes
        if not self._has_frames:
            self._update_indices()
        return self

    def _update_indices(self) -> None:
        """
        Private update indices method.

        :return: None
        """
        self.first_index = -1
        self.last_index = -1
        for widget in self.get_widgets(unpack_subframes=False):
            if (widget.is_selectable or isinstance(widget, Frame)) and \
                    widget.get_menu() is not None:
                if isinstance(widget, Frame) and widget.get_indices() == (-1, -1):
                    continue  # Frames with not selectable indices are not counted
                windex = widget.get_col_row_index()[2]
                if self.first_index == -1:
                    self.first_index = windex
                    self.last_index = windex
                else:
                    self.first_index = min(self.first_index, windex)
                    self.last_index = max(self.last_index, windex)
        if self.get_frame() is not None:
            self.get_frame()._update_indices()

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)

        updated = False
        if self.readonly or not self.is_visible():
            self._readonly_check_mouseover(events)
            return updated

        # Check title events
        if self._has_title:
            # Check for buttons
            for w in self._frame_title.get_widgets():
                updated = updated or w.update(events)

            # Check if clicked the title for drag
            for event in events:

                # Check mouseover
                self._frame_title._check_mouseover(event)

                # If clicked in title
                if (event.type == pygame.MOUSEBUTTONDOWN and self._mouse_enabled and event.button in
                    (1, 2, 3) or event.type == FINGERDOWN and self._touchscreen_enabled and self._menu is not None) and \
                        self._draggable:
                    event_pos = get_finger_pos(self._menu, event)

                    if self._frame_title.get_rect(to_real_position=True).collidepoint(*event_pos):
                        if not self._frame_title.get_attribute('drag', False):
                            self._frame_title.set_attribute('drag', True)
                            updated = True

                # User releases the button
                elif event.type == pygame.MOUSEBUTTONUP and self._mouse_enabled and \
                        event.button in (1, 2, 3) or \
                        event.type == FINGERUP and self._touchscreen_enabled:
                    self._frame_title.set_attribute('drag', False)

                # Mouse out from window
                # elif event.type == pygame.ACTIVEEVENT:
                #     if event.gain != 1:
                #         self._frame_title.set_attribute('drag', False)
                #         break

                # User moves the mouse while drag
                elif event.type == pygame.MOUSEMOTION and hasattr(event, 'rel') or \
                        event.type == FINGERMOTION and self._touchscreen_enabled and self._menu is not None:

                    if self._frame_title.get_attribute('drag', False) and self._draggable:
                        # Get relative movement
                        rx = event.rel[0] if event.type == pygame.MOUSEMOTION else \
                            event.dx * self._menu.get_window_size()[0] * S_FINGER_FACTOR[0]
                        ry = event.rel[1] if event.type == pygame.MOUSEMOTION else \
                            event.dy * self._menu.get_window_size()[1] * S_FINGER_FACTOR[1]

                        event_pos = get_finger_pos(self._menu, event)
                        tx, ty = self.get_translate()
                        title_rect = self._frame_title.get_rect(to_real_position=True)

                        if self._rect.y <= 0:
                            if not title_rect.collidepoint(*event_pos):
                                if ry > 0:
                                    self.translate(tx, ty - self._rect.y)
                                    self.force_menu_surface_update()
                                    updated = True
                                continue

                        elif self.get_scrollarea() is not None:
                            max_v = self.get_scrollarea().get_world_size()[1] - self._title_height()
                            if self._rect.y >= max_v:
                                if not title_rect.collidepoint(*event_pos):
                                    if ry < 0:
                                        continue
                                if ry > 0:
                                    continue
                            if ry > 0 and self._rect.y + ry >= max_v:
                                continue

                        # Get the max/min distance which can translate in vertical
                        if ry < 0:
                            ry = -min(-ry, self._rect.y)

                        self.translate(tx + rx, ty + ry)
                        self.force_menu_surface_update()
                        updated = True

        # Check mouseover
        for event in events:
            if self._check_mouseover(event):
                break

        # If not scrollable, return
        if not self.is_scrollable:
            return updated

        return updated or self._frame_scrollarea.update(events)


class _FrameSizeException(Exception):
    """
    If widget size is greater than frame raises exception.
    """
    pass


class _FrameDoNotAcceptScrollarea(Exception):
    """
    Raised if the frame does not accept a scrollarea.
    """
    pass


class _FrameDoNotAcceptTitle(Exception):
    """
    Raised if the frame does not accept a title.
    """
    pass


class FrameManager(AbstractWidgetManager, ABC):
    """
    Frame manager.
    """

    def _frame(
            self,
            width: NumberType,
            height: NumberType,
            orientation: str,
            frame_id: str = '',
            **kwargs
    ) -> 'pygame_menu.widgets.Frame':
        """
        Adds a frame to the Menu.

        :param width: Frame width in px
        :param height: Frame height in px
        :param orientation: Frame orientation, horizontal or vertical. See :py:mod:`pygame_menu.locals`
        :param frame_id: ID of the frame
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Frame`
        """
        from pygame_menu._scrollarea import get_scrollbars_from_position

        # Remove invalid keys from kwargs
        for key in list(kwargs.keys()):
            if key not in ('align', 'background_color', 'background_inflate',
                           'border_color', 'border_inflate', 'border_width',
                           'cursor', 'margin', 'padding', 'max_height', 'max_width',
                           'scrollbar_color', 'scrollbar_cursor',
                           'scrollbar_shadow_color', 'scrollbar_shadow_offset',
                           'scrollbar_shadow_position', 'scrollbar_shadow',
                           'scrollbar_slider_color', 'scrollbar_slider_pad',
                           'scrollbar_thick', 'scrollbars', 'scrollarea_color',
                           'border_position', 'scrollbar_slider_hover_color',
                           'tab_size', 'float', 'float_origin_position'):
                kwargs.pop(key, None)

        attributes = self._filter_widget_attributes(kwargs)
        pad = parse_padding(attributes['padding'])  # top, right, bottom, left
        pad_h = pad[1] + pad[3]
        pad_v = pad[0] + pad[2]

        assert width > pad_h, \
            f'frame width ({width}) cannot be lower than horizontal padding size ({pad_h})'
        assert height > pad_v, \
            f'frame height ({height}) cannot be lower than vertical padding size ({pad_v})'

        widget = Frame(
            width=width - pad_h,
            height=height - pad_v,
            orientation=orientation,
            frame_id=frame_id
        )
        self._configure_widget(widget=widget, **attributes)

        widget.make_scrollarea(
            max_height=kwargs.pop('max_height', height) - pad_v,
            max_width=kwargs.pop('max_width', width) - pad_h,
            scrollarea_color=kwargs.pop('scrollarea_color', None),
            scrollbar_color=kwargs.pop('scrollbar_color',
                                       self._theme.scrollbar_color),
            scrollbar_cursor=kwargs.pop('scrollbar_cursor',
                                        self._theme.scrollbar_cursor),
            scrollbar_shadow=kwargs.pop('scrollbar_shadow',
                                        self._theme.scrollbar_shadow),
            scrollbar_shadow_color=kwargs.pop('scrollbar_shadow_color',
                                              self._theme.scrollbar_shadow_color),
            scrollbar_shadow_offset=kwargs.pop('scrollbar_shadow_offset',
                                               self._theme.scrollbar_shadow_offset),
            scrollbar_shadow_position=kwargs.pop('scrollbar_shadow_position',
                                                 self._theme.scrollbar_shadow_position),
            scrollbar_slider_color=kwargs.pop('scrollbar_slider_color',
                                              self._theme.scrollbar_slider_color),
            scrollbar_slider_hover_color=kwargs.pop('scrollbar_slider_hover_color',
                                                    self._theme.scrollbar_slider_hover_color),
            scrollbar_slider_pad=kwargs.pop('scrollbar_slider_pad',
                                            self._theme.scrollbar_slider_pad),
            scrollbar_thick=kwargs.pop('scrollbar_thick', self._theme.scrollbar_thick),
            scrollbars=get_scrollbars_from_position(
                kwargs.pop('scrollbars', self._theme.scrollarea_position))
        )

        self._append_widget(widget)
        self._check_kwargs(kwargs)

        return widget

    def frame_h(
            self,
            width: NumberType,
            height: NumberType,
            frame_id: str = '',
            **kwargs
    ) -> 'pygame_menu.widgets.Frame':
        """
        Adds a horizontal frame to the Menu. Frame is a widget container that
        packs many widgets within. All contained widgets have a floating position,
        and use only 1 position in column/row layout.

        .. code-block:: python

            frame.pack(W1, alignment=ALIGN_LEFT, vertical_position=POSITION_NORTH)
            frame.pack(W2, alignment=ALIGN_LEFT, vertical_position=POSITION_CENTER)
            frame.pack(W3, alignment=ALIGN_LEFT, vertical_position=POSITION_SOUTH)
            ...

            ----------------
            |W1            |
            |   W2     ... |
            |      W3      |
            ----------------

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the frame if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contributes width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``max_height``                    (int) – Max height in px. If this value is lower than the frame ``height`` a scrollbar will appear on vertical axis. ``None`` by default (same height)
            - ``max_width``                     (int) – Max width in px. If this value is lower than the frame ``width`` a scrollbar will appear on horizontal axis. ``None`` by default (same width)
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``scrollarea_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`,None) – Scroll area color. If ``None`` area is transparent
            - ``scrollbar_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Scrollbar color
            - ``scrollbar_cursor``              (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the scrollbars if the mouse is placed over
            - ``scrollbar_shadow_color``        (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the shadow of each scrollbar
            - ``scrollbar_shadow_offset``       (int) – Offset of the scrollbar shadow in px
            - ``scrollbar_shadow_position``     (str) – Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
            - ``scrollbar_shadow``              (bool) – Indicate if a shadow is drawn on each scrollbar
            - ``scrollbar_slider_color``        (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the sliders
            - ``scrollbar_slider_hover_color``  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider if hovered or clicked
            - ``scrollbar_slider_pad``          (int, float) – Space between slider and scrollbars borders in px
            - ``scrollbar_thick``               (int) – Scrollbar thickness in px
            - ``scrollbars``                    (str) – Scrollbar position. See :py:mod:`pygame_menu.locals`
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            If horizontal frame contains a scrollarea (setting ``max_height`` or
            ``max_width`` less than size) padding will be set at zero.

        .. note::

            Packing applies a virtual translation to the widget, previous translation
            is not modified.

        .. note::

            Widget floating is also considered within frames. If a widget is
            floating, it does not add any size to the respective positioning.

        .. note::

            The Frame size created with this method does consider the padding. Thus,
            if Frame is created with ``width=100``, ``height=200`` and ``padding=25``
            the final internal size is ``width=50`` and ``height=150``.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param width: Frame width in px
        :param height: Frame height in px
        :param frame_id: ID of the horizontal frame
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Frame`
        """
        return self._frame(width, height, ORIENTATION_HORIZONTAL, frame_id, **kwargs)

    def frame_v(
            self,
            width: NumberType,
            height: NumberType,
            frame_id: str = '',
            **kwargs
    ) -> 'pygame_menu.widgets.Frame':
        """
        Adds a vertical frame to the Menu. Frame is a widget container that packs
        many widgets within. All contained widgets have a floating position, and
        use only 1 position in column/row layout.

        .. code-block:: python

            frame.pack(W1, alignment=ALIGN_LEFT)
            frame.pack(W2, alignment=ALIGN_CENTER)
            frame.pack(W3, alignment=ALIGN_RIGHT)
            ...

            --------
            |W1    |
            |  W2  |
            |    W3|
            | ...  |
            --------

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the frame if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contributes width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``max_height``                    (int) – Max height in px. If this value is lower than the frame ``height`` a scrollbar will appear on vertical axis. ``None`` by default (same height)
            - ``max_width``                     (int) – Max width in px. If this value is lower than the frame ``width`` a scrollbar will appear on horizontal axis. ``None`` by default (same width)
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``scrollarea_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`,None) – Scroll area color. If ``None`` area is transparent
            - ``scrollbar_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Scrollbar color
            - ``scrollbar_cursor``              (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the scrollbars if the mouse is placed over
            - ``scrollbar_shadow_color``        (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the shadow of each scrollbar
            - ``scrollbar_shadow_offset``       (int) – Offset of the scrollbar shadow in px
            - ``scrollbar_shadow_position``     (str) – Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
            - ``scrollbar_shadow``              (bool) – Indicate if a shadow is drawn on each scrollbar
            - ``scrollbar_slider_color``        (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the sliders
            - ``scrollbar_slider_hover_color``  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the slider if hovered or clicked
            - ``scrollbar_slider_pad``          (int, float) – Space between slider and scrollbars borders in px
            - ``scrollbar_thick``               (int) – Scrollbar thickness in px
            - ``scrollbars``                    (str) – Scrollbar position. See :py:mod:`pygame_menu.locals`
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            If vertical frame contains a scrollarea (setting ``max_height`` or
            ``max_width`` less than size) padding will be set at zero.

        .. note::

            Packing applies a virtual translation to the widget, previous translation
            is not modified.

        .. note::

            Widget floating is also considered within frames. If a widget is
            floating, it does not add any size to the respective positioning.

        .. note::

            The Frame size created with this method does consider the padding. Thus,
            if Frame is created with ``width=100``, ``height=200`` and ``padding=25``
            the final internal size is ``width=50`` and ``height=150``.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param width: Frame width in px
        :param height: Frame height in px
        :param frame_id: ID of the vertical frame
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Frame`
        """
        return self._frame(width, height, ORIENTATION_VERTICAL, frame_id, **kwargs)
