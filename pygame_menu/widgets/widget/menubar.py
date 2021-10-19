"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENUBAR
MenuBar class to display the Menu title.

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
# File constants no. 1000

__all__ = [

    # Main class
    'MenuBar',

    # Menubar styles
    'MENUBAR_STYLE_ADAPTIVE',
    'MENUBAR_STYLE_SIMPLE',
    'MENUBAR_STYLE_TITLE_ONLY',
    'MENUBAR_STYLE_TITLE_ONLY_DIAGONAL',
    'MENUBAR_STYLE_NONE',
    'MENUBAR_STYLE_UNDERLINE',
    'MENUBAR_STYLE_UNDERLINE_TITLE',

    # Custom types
    'MenuBarStyleModeType'

]

import pygame
import pygame.gfxdraw as gfxdraw
import pygame_menu.controls as ctrl

from pygame_menu.locals import FINGERUP, POSITION_EAST, POSITION_WEST, POSITION_NORTH, \
    POSITION_SOUTH
from pygame_menu.utils import assert_color, get_finger_pos, warn
from pygame_menu.widgets.core.widget import Widget, WidgetTransformationNotImplemented

from pygame_menu._types import Tuple, CallbackType, Tuple2IntType, Literal, Any, \
    Optional, NumberInstance, ColorInputType, EventVectorType, VectorInstance, \
    List, ColorType, NumberType

# Menubar styles
MENUBAR_STYLE_ADAPTIVE = 1000
MENUBAR_STYLE_SIMPLE = 1001
MENUBAR_STYLE_TITLE_ONLY = 1002
MENUBAR_STYLE_TITLE_ONLY_DIAGONAL = 1003
MENUBAR_STYLE_NONE = 1004
MENUBAR_STYLE_UNDERLINE = 1005
MENUBAR_STYLE_UNDERLINE_TITLE = 1006

# Menubar operation modes
_MODE_CLOSE = 1020
_MODE_BACK = 1021

# Custom types
MenuBarStyleModeType = Literal[MENUBAR_STYLE_ADAPTIVE, MENUBAR_STYLE_SIMPLE,
                               MENUBAR_STYLE_TITLE_ONLY,
                               MENUBAR_STYLE_TITLE_ONLY_DIAGONAL,
                               MENUBAR_STYLE_NONE, MENUBAR_STYLE_UNDERLINE,
                               MENUBAR_STYLE_UNDERLINE_TITLE]


# noinspection PyMissingOrEmptyDocstring
class MenuBar(Widget):
    """
    MenuBar widget.

    .. note::

        MenuBar only accepts translation transformation.

    :param title: Title of the menubar
    :param width: Width of the widget, generally the same as the width of the menu
    :param background_color: Background color
    :param menubar_id: ID of the MenuBar
    :param back_box: Draw a back-box button on header
    :param back_box_background_color: Back-box button color
    :param mode: Mode of drawing the bar
    :param modify_scrollarea: If ``True`` it modifies the scrollbars of the scrollarea depending on the bar mode
    :param offsetx: Offset x-position of title in px
    :param offsety: Offset y-position of title in px
    :param onreturn: Callback when pressing the back-box button
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments for callbacks
    """
    _backbox: bool
    _backbox_background_color: ColorType
    _backbox_border_width: int
    _backbox_pos: Any
    _backbox_rect: Optional['pygame.Rect']
    _box_mode: int
    _modify_scrollarea: bool
    _offsetx: NumberType
    _offsety: NumberType
    _polygon_pos: Any
    _scrollbar_deltas: List[Tuple[int, Tuple2IntType]]
    _style: int
    _width: int
    fixed: bool

    def __init__(
            self,
            title: Any,
            width: NumberType,
            background_color: ColorInputType,
            menubar_id: str = '',
            back_box: bool = False,
            back_box_background_color: ColorInputType = (0, 0, 0),
            mode: MenuBarStyleModeType = MENUBAR_STYLE_ADAPTIVE,
            modify_scrollarea: bool = True,
            offsetx: NumberType = 0,
            offsety: NumberType = 0,
            onreturn: CallbackType = None,
            *args,
            **kwargs
    ) -> None:
        assert isinstance(width, NumberInstance)
        assert isinstance(back_box, bool)

        assert width > 0, 'width must be greater or equal than zero'

        background_color = assert_color(background_color)
        back_box_background_color = assert_color(back_box_background_color)

        # MenuBar has no ID
        super(MenuBar, self).__init__(
            args=args,
            kwargs=kwargs,
            onreturn=onreturn,
            title=title,
            widget_id=menubar_id
        )

        self._backbox = back_box
        self._backbox_background_color = back_box_background_color
        self._backbox_border_width = 1  # px
        self._backbox_pos = None
        self._backbox_rect = None
        self._background_color = background_color
        self._box_mode = 0
        self._modify_scrollarea = modify_scrollarea
        self._mouseover_check_rect = lambda: self._backbox_rect
        self._offsetx = 0
        self._offsety = 0
        self._polygon_pos = None
        # north, east, south, west
        self._scrollbar_deltas = [(0, (0, 0)), (0, (0, 0)), (0, (0, 0)), (0, (0, 0))]
        self._style = mode
        self._title = ''
        self._width = int(width)

        self.set_title(title, offsetx, offsety)

        # Public's
        self.is_selectable = False
        self.fixed = True

    def _apply_font(self) -> None:
        pass

    def set_padding(self, *args, **kwargs) -> 'MenuBar':
        return self

    def scale(self, *args, **kwargs) -> 'MenuBar':
        raise WidgetTransformationNotImplemented()

    def resize(self, *args, **kwargs) -> 'MenuBar':
        raise WidgetTransformationNotImplemented()

    def set_max_width(self, *args, **kwargs) -> 'MenuBar':
        raise WidgetTransformationNotImplemented()

    def set_max_height(self, *args, **kwargs) -> 'MenuBar':
        raise WidgetTransformationNotImplemented()

    def rotate(self, *args, **kwargs) -> 'MenuBar':
        raise WidgetTransformationNotImplemented()

    def flip(self, *args, **kwargs) -> 'MenuBar':
        raise WidgetTransformationNotImplemented()

    def set_selection_effect(self, *args, **kwargs) -> 'MenuBar':
        return self

    def set_border(self, *args, **kwargs) -> 'MenuBar':
        return self

    def _check_title_color(self, background_menu: bool) -> None:
        """
        Performs title color and prints a warning if the color is similar to the
        background.

        :return: None
        """
        if background_menu and self._menu is not None:
            c_back = self._menu.get_theme().background_color
        else:
            c_back = self._background_color
        if not isinstance(c_back, VectorInstance):  # If is color
            return
        tol = 5
        c_dif_1 = abs(c_back[0] - self._font_color[0])
        c_dif_2 = abs(c_back[1] - self._font_color[1])
        c_dif_3 = abs(c_back[2] - self._font_color[2])
        if c_dif_1 < tol and c_dif_2 < tol and c_dif_3 < tol:
            warn(
                'title font color {0} is {3} to the {1} background color {2}, '
                'consider editing your Theme'.format(
                    self._font_color,
                    'menu' if background_menu else 'title',
                    c_back,
                    'equal' if c_dif_1 == c_dif_2 == c_dif_3 == 0 else 'similar'
                )
            )

    def get_title_offset(self) -> Tuple2IntType:
        """
        Return the title offset on x-axis and y-axis (x, y) in px.

        :return: Title offset
        """
        return int(self._offsetx), int(self._offsety)

    def set_backbox_border_width(self, width: int) -> None:
        """
        Set backbox border width in px.

        :param width: Width in px
        :return: None
        """
        assert isinstance(width, int)
        assert width > 0
        self._backbox_border_width = width

    def _draw_background_color(self, *args, **kwargs) -> None:
        pass

    def _draw_border(self, *args, **kwargs) -> None:
        pass

    def _backbox_visible(self) -> bool:
        """
        Return ``True`` if backbox is visible.

        :return: Bool
        """
        # The following check belongs to the case if the Menu displays a "x" button
        # to close the Menu, but onclose Menu method is None (Nothing is executed),
        # then the button will not be displayed
        # noinspection PyProtectedMember
        return (self._mouse_enabled or self._touchscreen_enabled) and self._backbox and \
               not (self._box_mode == _MODE_CLOSE and
                    self._menu is not None and
                    self._menu._onclose is None)

    def _draw(self, surface: 'pygame.Surface') -> None:
        if len(self._polygon_pos) > 2:
            gfxdraw.filled_polygon(surface, self._polygon_pos, self._background_color)

        # Draw backbox if enabled
        if self._backbox_visible():
            # noinspection PyArgumentList
            pygame.draw.rect(surface, self._backbox_background_color,
                             self._backbox_rect, self._backbox_border_width)
            pygame.draw.polygon(surface, self._backbox_background_color,
                                self._backbox_pos)

        surface.blit(self._surface,
                     (self._rect.topleft[0] + self._offsetx,
                      self._rect.topleft[1] + self._offsety))

    def get_scrollbar_style_change(self, position: str) -> Tuple[int, Tuple2IntType]:
        """
        Return scrollbar change (width, position) depending on the style of the
        menubar.

        :param position: Position of the scrollbar
        :return: Change in length and position in px
        """
        self._render()
        if not self._modify_scrollarea or not self.is_visible():
            return 0, (0, 0)
        if not self.fixed or self.is_floating():
            if self._style == MENUBAR_STYLE_ADAPTIVE:
                if position == POSITION_EAST:
                    t = self._polygon_pos[4][1] - self._polygon_pos[2][1]
                    return t, (0, -t)
            return 0, (0, 0)
        if position == POSITION_NORTH:
            return self._scrollbar_deltas[0]
        elif position == POSITION_EAST:
            return self._scrollbar_deltas[1]
        elif position == POSITION_SOUTH:
            return self._scrollbar_deltas[2]
        elif position == POSITION_WEST:
            return self._scrollbar_deltas[3]
        return 0, (0, 0)

    def _render(self) -> Optional[bool]:
        if self._menu is None:
            return

        # noinspection PyProtectedMember
        menu_prev_condition = not self._menu or not self._menu._top or not self._menu._top._prev

        if not self._render_hash_changed(
                self._menu.get_id(), self._rect.x, self._rect.y, self._title, self._width,
                self._visible, self._font_selected_color, menu_prev_condition):
            return True

        # Update box mode
        if menu_prev_condition:
            self._box_mode = _MODE_CLOSE
        else:
            self._box_mode = _MODE_BACK

        self._surface = self._render_string(self._title, self._font_selected_color)
        self._rect.width, self._rect.height = self._surface.get_size()
        self._apply_transforms()  # Rotation does not affect rect size

        dy = 0

        if self._style == MENUBAR_STYLE_ADAPTIVE:
            """
            A-------------------B                  D-E: 25 dx
            |****             x | *0,6 height
            |      D------------C
            F----E/
            """
            a = self._rect.x, self._rect.y
            b = self._rect.x + self._width - 1, self._rect.y
            c = self._rect.x + self._width - 1, self._rect.y + self._rect.height * 0.6
            d = self._rect.x + self._rect.width + 25 + self._offsetx, \
                self._rect.y + self._rect.height * 0.6
            e = self._rect.x + self._rect.width + 5 + self._offsetx, \
                self._rect.y + self._rect.height
            f = self._rect.x, self._rect.y + self._rect.height
            self._polygon_pos = a, b, c, d, e, f
            cross_size = int(self._rect.height * 0.6)
            self._scrollbar_deltas = [(0, (0, self._rect.height)),
                                      (-cross_size, (0, cross_size)),
                                      (0, (0, 0)),
                                      (-self._rect.height, (0, self._rect.height))]
            self._check_title_color(background_menu=False)

        elif self._style == MENUBAR_STYLE_SIMPLE:
            """
            A-------------------B
            |****             x | *1,0 height
            D-------------------C
            """
            a = self._rect.x, self._rect.y
            b = self._rect.x + self._width - 1, self._rect.y
            c = self._rect.x + self._width - 1, self._rect.y + self._rect.height
            d = self._rect.x, self._rect.y + self._rect.height
            self._polygon_pos = a, b, c, d
            cross_size = int(self._rect.height * self._backbox_visible())
            self._scrollbar_deltas = [(0, (0, self._rect.height)),
                                      (-self._rect.height, (0, self._rect.height)),
                                      (0, (0, 0)),
                                      (-self._rect.height, (0, self._rect.height))]
            self._check_title_color(background_menu=False)

        elif self._style == MENUBAR_STYLE_TITLE_ONLY:
            """
            A-----B
            | *** |           x        *0,6 height
            D-----C
            """
            a = self._rect.x, self._rect.y
            b = self._rect.x + self._rect.width + 5 + self._offsetx, self._rect.y
            c = self._rect.x + self._rect.width + 5 + self._offsetx, \
                self._rect.y + self._rect.height
            d = self._rect.x, self._rect.y + self._rect.height
            self._polygon_pos = a, b, c, d
            cross_size = int(self._rect.height * 0.6 * self._backbox_visible())
            self._scrollbar_deltas = [(0, (0, self._rect.height)),
                                      (-cross_size, (0, cross_size)),
                                      (0, (0, 0)),
                                      (-self._rect.height, (0, self._rect.height))]
            self._check_title_color(background_menu=False)

        elif self._style == MENUBAR_STYLE_TITLE_ONLY_DIAGONAL:
            """
            A--------B
            | **** /          x        *0,6 height
            D-----C
            """
            a = self._rect.x, self._rect.y
            b = self._rect.x + self._rect.width + 25 + self._offsetx, self._rect.y
            c = self._rect.x + self._rect.width + 5 + self._offsetx, \
                self._rect.y + self._rect.height
            d = self._rect.x, self._rect.y + self._rect.height
            self._polygon_pos = a, b, c, d
            cross_size = int(self._rect.height * 0.6 * self._backbox_visible())
            self._scrollbar_deltas = [(0, (0, self._rect.height)),
                                      (-cross_size, (0, cross_size)),
                                      (0, (0, 0)),
                                      (-self._rect.height, (0, self._rect.height))]
            self._check_title_color(background_menu=False)

        elif self._style == MENUBAR_STYLE_NONE:
            """
            A------------------B
             ****             x        *0,6 height
            """
            a = self._rect.x, self._rect.y
            b = self._rect.x + self._width - 1, self._rect.y
            self._polygon_pos = a, b
            cross_size = int(self._rect.height * 0.6 * self._backbox_visible())
            self._scrollbar_deltas = [(0, (0, self._rect.height)),
                                      (-cross_size, (0, cross_size)),
                                      (0, (0, 0)),
                                      (-self._rect.height, (0, self._rect.height))]
            self._check_title_color(background_menu=True)

        elif self._style == MENUBAR_STYLE_UNDERLINE:
            """
             ****             x
            A-------------------B      *0,09 height
            D-------------------C
            """
            # dy = 0
            a = self._rect.x, self._rect.y + 0.91 * self._rect.height + dy
            b = self._rect.x + self._width - 1, self._rect.y + 0.91 * self._rect.height + dy
            c = self._rect.x + self._width - 1, self._rect.y + self._rect.height + dy
            d = self._rect.x, self._rect.y + self._rect.height + dy
            self._polygon_pos = a, b, c, d
            cross_size = int(0.6 * self._rect.height * self._backbox_visible())
            self._scrollbar_deltas = [(0, (0, self._rect.height)),
                                      (-self._rect.height, (0, self._rect.height)),
                                      (0, (0, 0)),
                                      (-self._rect.height, (0, self._rect.height))]
            self._check_title_color(background_menu=True)

        elif self._style == MENUBAR_STYLE_UNDERLINE_TITLE:
            """
             ****               x
            A----B                     *0,09 height
            D----C
            """
            # dy = 3
            a = self._rect.x, self._rect.y + 0.91 * self._rect.height + dy
            b = self._rect.x + self._rect.width + 5 + self._offsetx, \
                self._rect.y + 0.91 * self._rect.height + dy
            c = self._rect.x + self._rect.width + 5 + self._offsetx, \
                self._rect.y + self._rect.height + dy
            d = self._rect.x, self._rect.y + self._rect.height + dy
            self._polygon_pos = a, b, c, d
            cross_size = int(0.6 * self._rect.height * self._backbox_visible())
            self._scrollbar_deltas = [(0, (0, self._rect.height)),
                                      (-cross_size, (0, cross_size)),
                                      (0, (0, 0)),
                                      (-self._rect.height, (0, self._rect.height))]
            self._check_title_color(background_menu=True)

        else:
            raise ValueError(f'invalid menubar mode {self._style}')
        self._rect.height += dy

        # Create the back box
        if self._backbox:
            backbox_margin = 4

            # Subtract the scrollarea thickness if float and enabled
            scroll_delta = 0
            if self._floating and self._menu is not None:
                scroll_delta = self._menu.get_width() - self._menu.get_width(inner=True)

            self._backbox_rect = pygame.Rect(
                int(self._rect.x + self._width - cross_size + backbox_margin - scroll_delta),
                int(self._rect.y + backbox_margin),
                int(cross_size - 2 * backbox_margin),
                int(cross_size - 2 * backbox_margin)
            )

            if self._box_mode == _MODE_CLOSE:
                # Make a cross for top Menu
                self._backbox_pos = (
                    (self._backbox_rect.left + 4, self._backbox_rect.top + 4),
                    (self._backbox_rect.centerx, self._backbox_rect.centery),
                    (self._backbox_rect.right - 4, self._backbox_rect.top + 4),
                    (self._backbox_rect.centerx, self._backbox_rect.centery),
                    (self._backbox_rect.right - 4, self._backbox_rect.bottom - 4),
                    (self._backbox_rect.centerx, self._backbox_rect.centery),
                    (self._backbox_rect.left + 4, self._backbox_rect.bottom - 4),
                    (self._backbox_rect.centerx, self._backbox_rect.centery),
                    (self._backbox_rect.left + 4, self._backbox_rect.top + 4)
                )

            elif self._box_mode == _MODE_BACK:
                # Make a back arrow for sub-menus
                self._backbox_pos = (
                    (self._backbox_rect.left + 5, self._backbox_rect.centery),
                    (self._backbox_rect.centerx, self._backbox_rect.top + 5),
                    (self._backbox_rect.centerx, self._backbox_rect.centery - 2),
                    (self._backbox_rect.right - 5, self._backbox_rect.centery - 2),
                    (self._backbox_rect.right - 5, self._backbox_rect.centery + 2),
                    (self._backbox_rect.centerx, self._backbox_rect.centery + 2),
                    (self._backbox_rect.centerx, self._backbox_rect.bottom - 5),
                    (self._backbox_rect.left + 5, self._backbox_rect.centery)
                )

    def set_title(self, title: Any, offsetx: NumberType = 0, offsety: NumberType = 0) -> 'MenuBar':
        """
        Set the menubar title.

        :param title: Menu title
        :param offsetx: Offset x-position of title in px
        :param offsety: Offset y-position of title in px
        :return: Self reference
        """
        assert isinstance(offsetx, NumberInstance)
        assert isinstance(offsety, NumberInstance)
        self._title = str(title)
        self._offsety = offsety
        self._offsetx = offsetx
        if self._menu is not None:
            self._render()
        return self

    def get_height(self, apply_padding: bool = True, apply_selection: bool = False) -> int:
        if self._floating or not self.is_visible():
            return 0
        return super(MenuBar, self).get_height(apply_padding, apply_selection)

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)

        if self.readonly or not self.is_visible():
            return False

        for event in events:

            # Check mouse over
            if self._backbox_visible():
                self._check_mouseover(event)

            # User clicks/touches the backbox rect; don't consider the mouse wheel (button 4 & 5)
            if event.type == pygame.MOUSEBUTTONUP and self._mouse_enabled and \
                    event.button in (1, 2, 3) or \
                    event.type == FINGERUP and self._touchscreen_enabled and \
                    self._menu is not None:
                event_pos = get_finger_pos(self._menu, event)
                if self._backbox_visible() and self._backbox_rect.collidepoint(*event_pos):
                    if event.type == pygame.MOUSEBUTTONUP:
                        self._sound.play_click_mouse()
                    else:
                        self._sound.play_click_touch()
                    self.apply()
                    return True

            # User applies joy back button
            elif event.type == pygame.JOYBUTTONDOWN and self._joystick_enabled:
                if event.button == ctrl.JOY_BUTTON_BACK:
                    self._sound.play_key_del()
                    self.apply()
                    return True

        return False
