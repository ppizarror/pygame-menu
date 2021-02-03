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

    # Menubar styles
    'MENUBAR_STYLE_ADAPTIVE',
    'MENUBAR_STYLE_SIMPLE',
    'MENUBAR_STYLE_TITLE_ONLY',
    'MENUBAR_STYLE_TITLE_ONLY_DIAGONAL',
    'MENUBAR_STYLE_NONE',
    'MENUBAR_STYLE_UNDERLINE',
    'MENUBAR_STYLE_UNDERLINE_TITLE',

    # Custom types
    'MenuBarStyleModeType',

    # Main class
    'MenuBar'

]

import pygame
import pygame_menu
import pygame.gfxdraw as gfxdraw
import pygame_menu.controls as _controls
import pygame_menu.locals as _locals
from pygame_menu.widgets.core import Widget
from pygame_menu.utils import assert_color
from pygame_menu._types import Union, List, Tuple, CallbackType, Tuple2IntType, Literal, \
    NumberType, ColorType, Any, Optional, PaddingType
import warnings

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
MenuBarStyleModeType = Literal[MENUBAR_STYLE_ADAPTIVE, MENUBAR_STYLE_SIMPLE, MENUBAR_STYLE_TITLE_ONLY,
                               MENUBAR_STYLE_TITLE_ONLY_DIAGONAL, MENUBAR_STYLE_NONE, MENUBAR_STYLE_UNDERLINE,
                               MENUBAR_STYLE_UNDERLINE_TITLE]


# noinspection PyMissingOrEmptyDocstring
class MenuBar(Widget):
    """
    MenuBar widget.

    .. note::

        This widget does not accept scale/resize transformation.

    :param title: Title of the menubar
    :param width: Width of the widget, generally width of the Menu
    :param background_color: Background color
    :param back_box: Draw a back-box button on header
    :param mode: Mode of drawing the bar
    :param modify_scrollarea: If ``True`` it modifies the scrollbars of the scrollarea depending on the bar mode
    :param offsetx: Offset x-position of title (px)
    :param offsety: Offset y-position of title (px)
    :param onreturn: Callback when pressing the back-box button
    :param args: Optional arguments for callbacks
    :param kwargs: Optional keyword arguments for callbacks
    """
    _backbox: bool
    _backbox_border_width: int
    _backbox_pos: Any
    _backbox_rect: Optional['pygame.Rect']
    _background_color: ColorType
    _box_mode: int
    _modify_scrollarea: bool
    _mouseoverback: bool
    _offsetx: NumberType
    _offsety: NumberType
    _polygon_pos: Any
    _style: int
    _width: int

    def __init__(self,
                 title: Any,
                 width: NumberType,
                 background_color: ColorType,
                 back_box: bool = False,
                 mode: MenuBarStyleModeType = MENUBAR_STYLE_ADAPTIVE,
                 modify_scrollarea: bool = True,
                 offsetx: NumberType = 0,
                 offsety: NumberType = 0,
                 onreturn: CallbackType = None,
                 *args,
                 **kwargs
                 ) -> None:
        assert isinstance(width, (int, float))
        assert isinstance(back_box, bool)

        assert_color(background_color)

        # MenuBar has no ID
        super(MenuBar, self).__init__(
            title=title,
            onreturn=onreturn,
            args=args,
            kwargs=kwargs
        )

        self._backbox = back_box
        self._backbox_border_width = 1  # px
        self._backbox_pos = None
        self._backbox_rect = None
        self._background_color = background_color
        self._box_mode = 0
        self._modify_scrollarea = modify_scrollarea
        self._mouseoverback = False
        self._offsetx = 0
        self._offsety = 0
        self._polygon_pos = None
        self._style = mode
        self._title = ''
        self._width = int(width)

        self.set_title(title, offsetx, offsety)
        self.is_selectable = False

    def _apply_font(self) -> None:
        pass

    def set_padding(self, padding: PaddingType) -> 'Widget':
        return self

    def scale(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'Widget':
        return self

    def resize(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'Widget':
        return self

    def set_max_height(self, height: NumberType, scale_width: NumberType = False, smooth: bool = True) -> 'Widget':
        return self

    def set_max_width(self, width: NumberType, scale_height: NumberType = False, smooth: bool = True) -> 'Widget':
        return self

    def set_selection_effect(self, selection: 'pygame_menu.widgets.core.Selection') -> 'Widget':
        return self

    def set_border(self, width: int, color: ColorType, inflate: Tuple2IntType) -> 'Widget':
        return self

    def _check_title_color(self, background_menu: bool) -> None:
        """
        Performs title color and prints a warning if the color is similar to the background.

        :return: None
        """
        if background_menu:
            cback = self.get_menu().get_theme().background_color
        else:
            cback = self._background_color
        if not isinstance(cback, (tuple, list)):  # If is color
            return
        tol = 5
        cdif1 = abs(cback[0] - self._font_color[0])
        cdif2 = abs(cback[1] - self._font_color[1])
        cdif3 = abs(cback[2] - self._font_color[2])
        if cdif1 < tol and cdif2 < tol and cdif3 < tol:
            msg = 'title font color {0} is {3} to the {1} background color {2}, consider ' \
                  'editing your Theme'.format(self._font_color,
                                              'menu' if background_menu else 'title',
                                              cback,
                                              'equal' if cdif1 == cdif2 == cdif3 == 0 else 'similar')
            warnings.warn(msg)

    def get_title_offset(self) -> Tuple2IntType:
        """
        Return the title offset in *(x, y)*.

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

    def _draw_background_color(self, surface: 'pygame.Surface') -> None:
        pass

    def _draw_border(self, surface: 'pygame.Surface') -> None:
        pass

    def _backbox_visible(self) -> bool:
        """
        Returns ``True`` if backbox is visible.

        :return: Bool
        """
        # The following check belongs to the case if the Menu displays a "x" button to close
        # the Menu, but onclose Menu method is None (Nothing is executed), then the button will
        # not be displayed
        # noinspection PyProtectedMember
        return self._mouse_enabled and self._backbox and \
               not (self._box_mode == _MODE_CLOSE and self.get_menu()._onclose is None)

    def _draw(self, surface: 'pygame.Surface') -> None:
        if len(self._polygon_pos) > 2:
            gfxdraw.filled_polygon(surface, self._polygon_pos, self._background_color)

        # Draw backbox if enabled
        if self._backbox_visible():
            # noinspection PyArgumentList
            pygame.draw.rect(surface, self._font_selected_color, self._backbox_rect, self._backbox_border_width)
            pygame.draw.polygon(surface, self._font_selected_color, self._backbox_pos)

        surface.blit(self._surface,
                     (self._rect.topleft[0] + self._offsetx,
                      self._rect.topleft[1] + self._offsety))

    def get_scrollbar_style_change(self, position: str) -> Tuple[int, Tuple2IntType]:
        """
        Return scrollbar change (width, position) depending on the style of the menubar.

        :param position: Position of the scrollbar
        :return: Change in length and position (px)
        """
        self._render()
        if not self._modify_scrollarea:
            return 0, (0, 0)
        if self._style == MENUBAR_STYLE_ADAPTIVE:
            if position == _locals.POSITION_EAST:
                t = self._polygon_pos[4][1] - self._polygon_pos[2][1]
                return t, (0, -t)
        return 0, (0, 0)

    def _render(self) -> Optional[bool]:
        # noinspection PyProtectedMember
        menu_prev_condition = not self._menu or not self._menu._top or not self._menu._top._prev

        if not self._render_hash_changed(self._menu.get_id(), self._rect.x, self._rect.y, self._title,
                                         self._font_selected_color, menu_prev_condition, self._visible):
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
            d = self._rect.x + self._rect.width + 25 + self._offsetx, self._rect.y + self._rect.height * 0.6
            e = self._rect.x + self._rect.width + 5 + self._offsetx, \
                self._rect.y + self._rect.height
            f = self._rect.x, self._rect.y + self._rect.height
            self._polygon_pos = a, b, c, d, e, f
            cross_size = self._rect.height * 0.6
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
            cross_size = self._rect.height
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
            cross_size = self._rect.height * 0.6
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
            cross_size = self._rect.height * 0.6
            self._check_title_color(background_menu=False)

        elif self._style == MENUBAR_STYLE_NONE:
            """
            A------------------B
             ****             x        *0,6 height
            """

            a = self._rect.x, self._rect.y
            b = self._rect.x + self._width - 1, self._rect.y
            self._polygon_pos = a, b
            cross_size = self._rect.height * 0.6
            self._check_title_color(background_menu=True)

        elif self._style == MENUBAR_STYLE_UNDERLINE:
            """
             ****             x
            A-------------------B      *0,09 height
            D-------------------C
            """

            dy = 4
            a = self._rect.x, self._rect.y + 0.91 * self._rect.height + dy
            b = self._rect.x + self._width - 1, self._rect.y + 0.91 * self._rect.height + dy
            c = self._rect.x + self._width - 1, self._rect.y + self._rect.height + dy
            d = self._rect.x, self._rect.y + self._rect.height + dy
            self._polygon_pos = a, b, c, d
            cross_size = 0.6 * self._rect.height
            self._check_title_color(background_menu=True)

        elif self._style == MENUBAR_STYLE_UNDERLINE_TITLE:
            """
             ****               x
            A----B                     *0,09 height
            D----C
            """

            dy = 3
            a = self._rect.x, self._rect.y + 0.91 * self._rect.height + dy
            b = self._rect.x + self._rect.width + 5 + self._offsetx, self._rect.y + 0.91 * self._rect.height + dy
            c = self._rect.x + self._rect.width + 5 + self._offsetx, self._rect.y + self._rect.height + dy
            d = self._rect.x, self._rect.y + self._rect.height + dy
            self._polygon_pos = a, b, c, d
            cross_size = 0.6 * self._rect.height
            self._check_title_color(background_menu=True)

        else:
            raise ValueError('invalid menubar mode {0}'.format(self._style))
        self._rect.height += dy

        # Create the back box
        if self._backbox:
            backbox_margin = 4

            # Subtract the scrollarea thickness if float and enabled
            scroll_delta = 0
            if self._floating:
                scroll_delta = self.get_menu().get_width() - self.get_menu().get_width(inner=True)

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
                    (self._backbox_rect.left + 4, self._backbox_rect.top + 4),
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

    def set_title(self, title: Any, offsetx: NumberType = 0, offsety: NumberType = 0) -> 'Widget':
        """
        Set the menubar title.

        :param title: Menu title
        :param offsetx: Offset x-position of title (px)
        :param offsety: Offset y-position of title (px)
        :return: Self reference
        """
        assert isinstance(offsetx, (int, float))
        assert isinstance(offsety, (int, float))
        self._title = str(title)
        self._offsety = offsety
        self._offsetx = offsetx
        if self._menu is not None:
            self._render()
        return self

    def get_height(self, apply_padding: bool = True, apply_selection: bool = False) -> int:
        if self._floating:
            return 0
        return super(MenuBar, self).get_height(apply_padding, apply_selection)

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        updated = False

        for event in events:

            if self._mouse_enabled and event.type == pygame.MOUSEBUTTONUP and \
                    event.button in (1, 2, 3):  # Don't consider the mouse wheel (button 4 & 5)
                if self._backbox_rect and self._backbox_rect.collidepoint(*event.pos):
                    self._sound.play_click_mouse()
                    self.apply()
                    updated = True
                    if self._backbox_visible() and self._mouseoverback:
                        self._mouseoverback = False
                        self.mouseleave(event)

            elif self._joystick_enabled and event.type == pygame.JOYBUTTONDOWN:
                if event.button == _controls.JOY_BUTTON_BACK:
                    self._sound.play_key_del()
                    self.apply()
                    updated = True

            # Check mouse over backrect and visible
            elif self._backbox_visible() and \
                    (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION):
                if self._backbox_rect.collidepoint(*event.pos):
                    if not self._mouseoverback:
                        self._mouseoverback = True
                        self.mouseover(event)
                else:
                    if self._mouseoverback:
                        self._mouseoverback = False
                        self.mouseleave(event)

            elif self._touchscreen_enabled and event.type == pygame.FINGERUP:
                window_size = self.get_menu().get_window_size()
                finger_pos = (event.x * window_size[0], event.y * window_size[1])
                if self._backbox_rect and self._backbox_rect.collidepoint(*finger_pos):
                    self._sound.play_click_mouse()
                    self.apply()
                    updated = True

        if updated:
            self.apply_update_callbacks()

        return updated
