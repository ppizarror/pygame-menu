"""
pygame-menu
https://github.com/ppizarror/pygame-menu

FRAME
Widget container.

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

__all__ = ['Frame']

import pygame
import pygame_menu
import pygame_menu.locals as _locals
from pygame_menu._decorator import Decorator
from pygame_menu.widgets.core import Widget
from pygame_menu._types import Optional, NumberType, Dict, Tuple, Union, List, Vector2NumberType, \
    ColorType, Tuple2IntType, NumberInstance
from pygame_menu.utils import assert_alignment, make_surface, assert_vector, assert_orientation


# noinspection PyMissingOrEmptyDocstring
class Frame(Widget):
    """
    Frame is a widget container, it can pack many widgets.

    All widgets inside have a floating position. Widgets inside are placed using its
    margin + width/height. ``(0, 0)`` coordinate is the top-left position in frame.

    Frame modifies ``translation`` of widgets. Thus, if widget has a translation before
    it will be removed.

    Widget packing currently only supports LEFT, CENTER and RIGHT alignment in the same line, widgets
    cannot be packed in two different lines. For such purpose use several frames. If widget width or
    height exceeds Frame size ``_FrameSizeException`` will be raised.

    .. note::

        Frame only implements translation.

    .. note::

        Frame cannot be selected. Thus, it does not receive any selection effect.

    :param width: Frame width
    :param height: Frame height
    :param orientation: Frame orientation (horizontal or vertical). See :py:mod:`pygame_menu.locals`
    :param frame_id: ID of the frame
    """
    _control_widget: Optional['Widget']
    _control_widget_last_pos: Optional[Vector2NumberType]
    _frame_scrollarea: Optional['pygame_menu.scrollarea.ScrollArea']
    _height: int
    _orientation: str
    _pos: Dict[str, Tuple[int, int]]  # Widget positioning
    _real_rect: 'pygame.Rect'
    _recursive_render: int
    _widgets: Dict[str, Tuple['Widget', str, str]]  # widget, alignment, vertical position
    _width: int
    first_index: int  # First selectable widget index
    horizontal: bool
    last_index: int  # Last selectable widget index

    def __init__(self,
                 width: NumberType,
                 height: NumberType,
                 orientation: str,
                 frame_id: str = ''
                 ) -> None:
        super(Frame, self).__init__(widget_id=frame_id)
        assert isinstance(width, NumberInstance) and width > 0
        assert isinstance(height, NumberInstance) and height > 0
        assert_orientation(orientation)

        # Internals
        self._control_widget = None
        self._control_widget_last_pos = None  # This checks if menu has updated widget position
        self._frame_scrollarea = None
        self._height = int(height)
        self._orientation = orientation
        self._pos = {}
        self._real_rect = pygame.Rect(0, 0, width, height)
        self._recursive_render = 0
        self._widgets = {}
        self._width = int(width)

        # Configure widget publics
        self.first_index = -1
        self.horizontal = orientation == _locals.ORIENTATION_HORIZONTAL
        self.is_selectable = False
        self.is_scrollable = False
        self.last_index = -1

    def get_max_size(self) -> Tuple2IntType:
        """
        Returns the max size of the frame.

        :return: Max width, height
        """
        if self._frame_scrollarea is not None:
            return self._frame_scrollarea.get_size()
        return self.get_size()

    def make_scrollarea(self,
                        max_width: Optional[NumberType],
                        max_height: Optional[NumberType],
                        scrollbar_color: ColorType,
                        scrollbar_cursor: Optional[Union[int, 'pygame.cursors.Cursor']],
                        scrollbar_shadow: bool,
                        scrollbar_shadow_color: ColorType,
                        scrollbar_shadow_offset: int,
                        scrollbar_shadow_position: str,
                        scrollbar_slider_color: ColorType,
                        scrollbar_slider_pad: NumberType,
                        scrollbar_thick: NumberType,
                        scrollbars: Union[str, Tuple[str, ...]],
                        ) -> 'Frame':
        """
        Make the scrollarea of the frame.

        :param max_width: Maximum width of the scrollarea
        :param max_height: Maximum height of the scrollarea
        :param scrollbar_color: Scrollbar color
        :param scrollbar_cursor: Scrollbar cursor
        :param scrollbar_shadow: Indicate if a shadow is drawn on each scrollbar
        :param scrollbar_shadow_color: Color of the shadow of each scrollbar
        :param scrollbar_shadow_offset: Offset of the scrollbar shadow (px)
        :param scrollbar_shadow_position: Position of the scrollbar shadow. See :py:mod:`pygame_menu.locals`
        :param scrollbar_slider_color: Color of the sliders
        :param scrollbar_slider_pad: Space between slider and scrollbars borders (px)
        :param scrollbar_thick: Scrollbar thickness (px)
        :param scrollbars: Positions of the scrollbars. See :py:mod:`pygame_menu.locals`
        :return: Self reference
        """
        assert self.configured, 'frame must be configured before adding the scrollarea'
        assert self.get_menu() is not None, 'menu must be defined before creating the scrollarea'
        if max_width is None:
            max_width = self._width
        if max_height is None:
            max_height = self._height
        assert isinstance(max_width, NumberInstance)
        assert isinstance(max_height, NumberInstance)
        assert 0 < max_width <= self._width, \
            'scroll area width ({0}) cannot exceed frame width ({1})'.format(max_width, self._width)
        assert 0 < max_height <= self._height, \
            'scroll area height ({0}) cannot exceed frame height ({1})'.format(max_height, self._height)

        # Create area to get scrollbar thickness
        sa = pygame_menu.scrollarea.ScrollArea(
            area_width=max_width,
            area_height=max_height,
            scrollbar_slider_pad=scrollbar_slider_pad,
            scrollbar_thick=scrollbar_thick,
            scrollbars=scrollbars
        )

        sx = sa.get_scrollbar_thickness(_locals.ORIENTATION_HORIZONTAL, real=True)
        sy = sa.get_scrollbar_thickness(_locals.ORIENTATION_VERTICAL, real=True)
        if self._width == max_width:
            sx *= 0
        if self._height == max_height:
            sy *= 0

        if self._width > max_width or self._height > max_height:
            self.is_scrollable = True
            self.set_padding(0)
        else:
            # Configure rect
            self._rect.height = self._height
            self._rect.width = self._width
            self._frame_scrollarea = None
            self.is_scrollable = False
            return self

        # Create area object
        self._frame_scrollarea = pygame_menu.scrollarea.ScrollArea(
            area_width=max_width + sy + sx,
            area_height=max_height + sx + sy,
            scrollbar_cursor=scrollbar_cursor,
            scrollbar_color=scrollbar_color,
            parent_scrollarea=self._scrollarea,
            scrollbar_slider_color=scrollbar_slider_color,
            scrollbar_slider_pad=scrollbar_slider_pad,
            scrollbar_thick=scrollbar_thick,
            scrollbars=scrollbars,
            shadow=scrollbar_shadow,
            shadow_color=scrollbar_shadow_color,
            shadow_offset=scrollbar_shadow_offset,
            shadow_position=scrollbar_shadow_position
        )

        if self._width == max_width:
            self._frame_scrollarea.hide_scrollbars(_locals.ORIENTATION_HORIZONTAL)
        if self._height == max_height:
            self._frame_scrollarea.hide_scrollbars(_locals.ORIENTATION_VERTICAL)

        # Create surface
        self._surface = make_surface(self._width + sy, self._height + sx, alpha=True)

        # Configure area
        self._frame_scrollarea.set_world(self._surface)

        # Configure rect
        self._rect.height = max_height + sx
        self._rect.width = max_width + sy

        return self

    def get_indices(self) -> Tuple[int, int]:
        """
        Return first and last indices tuple.

        :return: First, Last widget selectable indices
        """
        return self.first_index, self.last_index

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        if not self.is_scrollable:
            return False
        return self._frame_scrollarea.update(events)

    def select(self, *args, **kwargs) -> 'Widget':
        return self

    def set_selection_effect(self, *args, **kwargs) -> 'Widget':
        pass

    def _apply_font(self) -> None:
        pass

    def _render(self) -> None:
        pass

    def _draw(self, *args, **kwargs) -> None:
        pass

    def scale(self, *args, **kwargs) -> 'Widget':
        return self

    def resize(self, *args, **kwargs) -> 'Widget':
        return self

    def set_max_width(self, *args, **kwargs) -> 'Widget':
        return self

    def set_max_height(self, *args, **kwargs) -> 'Widget':
        return self

    def rotate(self, *args, **kwargs) -> 'Widget':
        return self

    def flip(self, *args, **kwargs) -> 'Widget':
        return self

    def get_decorator(self) -> 'Decorator':
        """
        Frame decorator belongs to the scrollarea decorator if enabled.

        :return: ScrollArea decorator
        """
        if not self.is_scrollable:
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
            raise IndexError('{0} widget does not exist on {1}'.format(widget.get_class_id(), self.get_class_id()))

    def set_position(self, posx: NumberType, posy: NumberType) -> 'Frame':
        super(Frame, self).set_position(posx, posy)
        if self.is_scrollable:
            self._frame_scrollarea.set_position(posx, posy)
        return self

    def get_scrollarea(self, inner: bool = False) -> Optional['pygame_menu.scrollarea.ScrollArea']:
        """
        Return the scrollarea object.

        :param inner: If ``True`` return the inner scrollarea
        :return: ScrollArea object
        """
        if inner:
            return self._frame_scrollarea
        return self._scrollarea

    def draw(self, surface: 'pygame.Surface') -> 'Widget':
        # Simple case, no scrollarea
        if not self.is_scrollable:
            self.last_surface = surface
            self._draw_background_color(surface)
            self._decorator.draw_prev(surface)
            for w in self._widgets.values():
                widget = w[0]
                if widget.is_visible():
                    widget.draw(surface)
            self._draw_border(surface)
            self._decorator.draw_post(surface)

        # Scrollarea
        else:
            self.last_surface = self._surface
            self._surface.fill((255, 255, 255, 0))
            self._draw_background_color(self._surface, rect=self._real_rect)
            scrollarea_decorator = self.get_decorator()
            scrollarea_decorator.force_cache_update()
            scrollarea_decorator.draw_prev(self._surface)
            selected_widget = None
            for w in self._widgets.values():
                widget = w[0]
                if widget.is_visible():
                    widget.draw(self._surface)
                if widget.is_selected():
                    selected_widget = widget
            if selected_widget is not None:
                selected_widget.draw_selection_effect()
            self._frame_scrollarea.draw(surface)
            self._draw_border(surface)
        self.apply_draw_callbacks()
        return self

    def _get_ht(self, widget: 'Widget', a: str) -> int:
        """
        Return the horizontal translation for widget.

        :param widget: Widget
        :param a: Horizontal alignment
        :return: Px
        """
        w = widget.get_width()
        if w > self._width:
            raise _FrameSizeException('{0} width ({1}) is greater than {3} width ({2})'.format(
                widget.get_class_id(), w, self._width, self.get_class_id()
            ))
        if a == _locals.ALIGN_CENTER:
            return int((self._width - w) / 2)
        elif a == _locals.ALIGN_RIGHT:
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
        if h > self._height:
            raise _FrameSizeException('{0} height ({1}) is greater than {3} height ({2})'.format(
                widget.get_class_id(), h, self._height, self.get_class_id()
            ))
        if v == _locals.POSITION_CENTER:
            return int((self._height - h) / 2)
        elif v == _locals.POSITION_SOUTH:
            return self._height - h
        else:  # Position north
            return 0

    def _update_position_horizontal(self) -> None:
        """
        Compute widget position for horizontal orientation.

        :return: None
        """
        xleft = 0  # Total added to left
        xright = 0  # Total added to right
        wcenter = 0

        for w in self._widgets.values():
            w, align, vpos = w
            if align == _locals.ALIGN_CENTER:
                wcenter += w.get_width() + w.get_margin()[0]
                continue
            elif align == _locals.ALIGN_LEFT:
                xleft += w.get_margin()[0]
                self._pos[w.get_id()] = (xleft, self._get_vt(w, vpos) + w.get_margin()[1])
                xleft += w.get_width()
            elif align == _locals.ALIGN_RIGHT:
                xright -= (w.get_width())
                self._pos[w.get_id()] = (self._width + xright, self._get_vt(w, vpos) + w.get_margin()[1])
                xright += w.get_margin()[0]
            dw = xleft - xright
            if dw > self._width:
                msg = '{3} sizing ({0}) exceeds {2} width ({1})' \
                      ''.format(dw, self._width, self.get_class_id(), w.get_class_id())
                raise _FrameSizeException(msg)

        # Now center widgets
        available = self._width - (xleft - xright)
        if wcenter > available:
            msg = 'cannot place center widgets as required width ({0}) ' \
                  'is greater than available ({1})'.format(wcenter, available)
            raise _FrameSizeException(msg)
        xcenter = int(self._width / 2 - wcenter / 2)
        for w in self._widgets.values():
            w, align, vpos = w
            if align == _locals.ALIGN_CENTER:
                xcenter += w.get_margin()[0]
                self._pos[w.get_id()] = (xcenter, self._get_vt(w, vpos) + w.get_margin()[1])
                xcenter += w.get_width()

    def _update_position_vertical(self) -> None:
        """
        Compute widget position for vertical orientation.

        :return: None
        """
        ytop = 0  # Total added to top
        ybottom = 0  # Total added to bottom
        wcenter = 0
        for w in self._widgets.values():
            w, align, vpos = w
            if vpos == _locals.POSITION_CENTER:
                wcenter += w.get_width() + w.get_margin()[1]
                continue
            elif vpos == _locals.POSITION_NORTH:
                ytop += w.get_margin()[1]
                self._pos[w.get_id()] = (self._get_ht(w, align) + w.get_margin()[0], ytop)
                ytop += w.get_height()
            elif vpos == _locals.POSITION_SOUTH:
                ybottom -= (w.get_margin()[1] + w.get_height())
                self._pos[w.get_id()] = (self._get_ht(w, align) + w.get_margin()[0], self._height + ybottom)
            dh = ytop - ybottom
            if dh > self._height:
                msg = '{3} sizing ({0}) exceeds {2} height ({1})' \
                      ''.format(dh, self._height, self.get_class_id(), w.get_class_id())
                raise _FrameSizeException(msg)

        # Now center widgets
        available = self._height - (ytop - ybottom)
        if wcenter > available:
            msg = 'cannot place center widgets as required height ({0}) ' \
                  'is greater than available ({1}) in {2}'.format(wcenter, available, self.get_class_id())
            raise _FrameSizeException(msg)
        ycenter = int(self._height / 2 - wcenter / 2)
        for w in self._widgets.values():
            w, align, vpos = w
            if vpos == _locals.POSITION_CENTER:
                ycenter += w.get_margin()[1]
                self._pos[w.get_id()] = (self._get_ht(w, align) + w.get_margin()[0], ycenter)
                ycenter += w.get_height()

    def update_position(self) -> 'Frame':
        """
        Update the position of each widget.

        :return: Self reference
        """
        if len(self._widgets) == 0:
            return self

        # Update position based on orientation
        if self._orientation == _locals.ORIENTATION_HORIZONTAL:
            self._update_position_horizontal()
        elif self._orientation == _locals.ORIENTATION_VERTICAL:
            self._update_position_vertical()

        # Apply position to each widget
        for w in self._widgets.keys():
            tx, ty = self._pos[w]
            widget = self._widgets[w][0]
            if widget.get_menu() is None:  # Widget is only appended to Frame
                widget.set_position(*self.get_position())
                continue
            if self._frame_scrollarea is not None:
                sx, sy = self._frame_scrollarea.get_position()
                # widget._translate_virtual = (tx, ty)  # Store virtual original translation
                tx -= sx
                ty -= sy

            widget._translate = (tx, ty)  # Translate to scrollarea

        # Check if control widget has changed positioning. This fixes centering issues
        if self._control_widget is not None:
            cpos = self._control_widget.get_position()
            if self._control_widget_last_pos != cpos:
                self._control_widget_last_pos = cpos
                if self._recursive_render <= 100:
                    self._menu.render()
                self._recursive_render += 1
            else:
                self._recursive_render = 0

        return self

    def get_widgets(self,
                    unpack_subframes: bool = True,
                    unpack_subframes_include_frame: bool = False
                    ) -> Tuple['Widget', ...]:
        """
        Get widgets as a tuple.

        :param unpack_subframes: If ``True`` add frame widgets instead of frame
        :param unpack_subframes_include_frame: If ``True`` the unpacked frame is also added to the widget list
        :return: Widget tuple
        """
        wtp = []
        for w in self._widgets.values():
            widget = w[0]
            if isinstance(widget, Frame) and unpack_subframes:
                ww = widget.get_widgets(unpack_subframes=unpack_subframes)
                for i in ww:
                    wtp.append(i)
                if unpack_subframes_include_frame:
                    wtp.append(widget)
                continue
            wtp.append(widget)
        return tuple(wtp)

    def unpack(self, widget: 'Widget') -> 'Frame':
        """
        Unpack widget from Frame. If widget does not exist, raises ``ValueError``.
        Unpacked widgets have a floating position and are moved to the last position of the widget list of Menu

        :param widget: Widget to unpack
        :return: Self reference
        """
        assert len(self._widgets) > 0, 'frame is empty'
        wid = widget.get_id()
        if wid not in self._widgets.keys():
            msg = '{0} does not exist in frame'.format(widget.get_class_id())
            raise ValueError(msg)
        assert widget._frame == self, 'widget frame differs from current'
        widget._frame = None
        widget._translate = (0, 0)
        del self._widgets[wid]
        try:
            del self._pos[wid]
        except KeyError:
            pass

        # Move widget to the last position of widget list
        if widget.get_menu() == self.get_menu():
            try:
                self.get_menu().move_widget_index(widget)
            except ValueError:
                pass

        self.force_menu_surface_update()
        if self._control_widget == widget:
            self._control_widget = None
            self._control_widget_last_pos = None
            for widget in self.get_widgets():
                if widget.get_menu() is not None:
                    self._control_widget = widget
                    self._control_widget_last_pos = self._control_widget.get_position()
                    break

        self.update_indices()
        return self

    def pack(self,
             widget: Union['Widget', List['Widget'], Tuple['Widget', ...]],
             alignment: str = _locals.ALIGN_LEFT,
             vertical_position: str = _locals.POSITION_NORTH,
             margin: Vector2NumberType = (0, 0)) -> Union['Widget', List['Widget'], Tuple['Widget', ...]]:
        """
        Packs widget in the frame line. To pack a widget it has to be already
        appended to Menu, and the Menu must be the same as the frame.

        Packing is added to the same line, for example if three LEFT widgets are added:

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

            It is recommended to force menu rendering after packing all widgets.

        :param widget: Widget to be packed
        :param alignment: Widget alignment
        :param vertical_position: Vertical position of the widget within frame. See :py:mod:`pygame_menu.locals`
        :param margin: *(left, top)* margin of added widget in px. It overrides the previous widget margin
        :return: Added widget references
        """
        menu = self.get_menu()
        assert menu is not None, \
            'menu must be set before packing widgets'
        if isinstance(widget, (tuple, list)):
            for w in widget:
                self.pack(widget=w, alignment=alignment, vertical_position=vertical_position)
            return widget
        assert isinstance(widget, Widget)
        assert widget.get_id() not in self._widgets.keys(), \
            'widget already in frame'
        assert widget.get_menu() == menu or widget.get_menu() is None, \
            'widget menu to be added to frame must be in same menu as frame, or it can have any Menu instance'
        assert widget.get_frame() is None, \
            'widget already is in another frame'
        assert_alignment(alignment)
        assert vertical_position in (_locals.POSITION_NORTH, _locals.POSITION_CENTER, _locals.POSITION_SOUTH), \
            'vertical position must be NORTH, CENTER, or SOUTH'
        assert widget._translate[0] == 0 and widget._translate[1] == 0, \
            'widget cannot have a previous translation if appended. Frame overrides translation'
        assert_vector(margin, 2)
        assert widget.configured, 'widget must be configured before packing'

        widget.set_frame(self)
        widget.set_float()
        widget.set_margin(*margin)
        if self._frame_scrollarea is not None:
            widget.set_scrollarea(self._frame_scrollarea)
        self._widgets[widget.get_id()] = (widget, alignment, vertical_position)

        # Sort widgets to keep selection order
        if widget.get_menu() is not None:
            try:
                widget.get_menu().move_widget_index(widget, self, render=False)
            except AssertionError:
                pass
        if self._control_widget is None and widget.get_menu() is not None:
            self._control_widget = widget
            self._control_widget_last_pos = self._control_widget.get_position()

        # Render is mandatory as it modifies row/column layout
        try:
            menu.render()
        except _FrameSizeException:
            self.unpack(widget)
            raise

        self.update_indices()
        return widget

    def contains_widget(self, widget: 'Widget') -> bool:
        """
        Returns true if the frame contains the given widget.

        :param widget: Widget to check
        :return: ``True`` if widget within frame
        """
        return widget.get_frame() == self and widget.get_id() in self._widgets.keys()

    def update_indices(self) -> None:
        """
        Update first and last selectable widget index.

        :return: None
        """
        widgs = self.get_widgets(unpack_subframes=False)
        self.first_index = -1
        self.last_index = -1
        for widget in widgs:
            if (widget.is_selectable or isinstance(widget, Frame)) and widget.get_menu() is not None:
                if isinstance(widget, Frame) and widget.get_indices() == (-1, -1):
                    continue  # Frames with not selectable indices are not counted
                windex = widget.get_col_row_index()[2]
                if self.first_index == -1:
                    self.first_index = windex
                    self.last_index = windex
                else:
                    self.first_index = min(self.first_index, windex)
                    self.last_index = max(self.last_index, windex)


class _FrameSizeException(Exception):
    """
    If widget size is greater than frame raises exception.
    """
    pass
