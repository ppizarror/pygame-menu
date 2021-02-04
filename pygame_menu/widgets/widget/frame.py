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
import pygame_menu.locals as _locals
from pygame_menu.widgets.core import Widget
from pygame_menu._types import Optional, NumberType, Dict, Tuple, Literal, Union, List, Vector2NumberType
from pygame_menu.utils import assert_alignment, make_surface, assert_vector, assert_orientation

PackPositionTypes = Literal[_locals.POSITION_NORTH, _locals.POSITION_CENTER, _locals.POSITION_SOUTH]
FrameOrientationType = Literal[_locals.ORIENTATION_HORIZONTAL, _locals.ORIENTATION_VERTICAL]


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

        Frame does not accept padding.

    :param width: Frame width
    :param height: Frame height
    :param orientation: Frame orientation. It can be ``ORIENTATION_HORIZONTAL`` or ``ORIENTATION_VERTICAL``
    :param frame_id: ID of the frame
    """
    _control_widget: Optional['Widget']
    _control_widget_last_pos: Optional[Vector2NumberType]
    _height: int
    _orientation: FrameOrientationType
    _pos: Dict[str, Tuple[int, int]]  # Widget positioning
    _recursive_render: int
    _widgets: Dict[str, Tuple['Widget', str, str]]  # widget, alignment, vertical position
    _width: int
    first_index: int  # First selectable widget index
    horizontal: bool
    last_index: int  # Last selectable widget index

    def __init__(self,
                 width: NumberType,
                 height: NumberType,
                 orientation: FrameOrientationType,
                 frame_id: str = ''
                 ) -> None:
        super(Frame, self).__init__(widget_id=frame_id)
        assert isinstance(width, (int, float)) and width > 0
        assert isinstance(height, (int, float)) and height > 0
        assert_orientation(orientation)

        # Internals
        self._control_widget = None
        self._control_widget_last_pos = None  # This checks if menu has updated widget position
        self._height = int(height)
        self._orientation = orientation
        self._pos = {}
        self._recursive_render = 0
        self._widgets = {}
        self._width = int(width)

        # Configure widget publics
        self.first_index = -1
        self.horizontal = orientation == _locals.ORIENTATION_HORIZONTAL
        self.is_selectable = False
        self.last_index = -1

        # Stablish rect and surface
        self._rect.height = self._height
        self._rect.width = self._width
        self._surface = make_surface(width, height, alpha=True)

    def get_indices(self) -> Tuple[int, int]:
        """
        Return first and last indices tuple.

        :return: First, Last widget selectable indices
        """
        return self.first_index, self.last_index

    def update(self, events: Union[List['pygame.event.Event'], Tuple['pygame.event.Event']]) -> bool:
        pass

    def _apply_font(self) -> None:
        pass

    def _render(self) -> None:
        pass

    def _draw(self, surface: 'pygame.Surface') -> None:
        pass

    def scale(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'Widget':
        return self

    def resize(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'Widget':
        return self

    def set_max_width(self, width: Optional[NumberType], scale_height: NumberType = False,
                      smooth: bool = True) -> 'Widget':
        return self

    def set_max_height(self, height: Optional[NumberType], scale_width: NumberType = False,
                       smooth: bool = True) -> 'Widget':
        return self

    def rotate(self, angle: NumberType) -> 'Widget':
        return self

    def flip(self, x: bool, y: bool) -> 'Widget':
        return self

    def draw(self, surface: 'pygame.Surface') -> 'Widget':
        self._draw_background_color(surface)
        self._decorator.draw_prev(surface)
        for widget in self._widgets.values():
            widget[0].draw(surface)
        self._draw_border(surface)
        self._decorator.draw_post(surface)
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
            raise _FrameSizeException('widget<"{0}"> ({1}) is greater than Frame<"{3}"> widget ({2})'.format(
                widget.get_id(), w, self._width, self.get_id()
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
            raise _FrameSizeException('widget<"{0}"> height ({1}) is greater than Frame<"{3}"> height ({2})'.format(
                widget.get_id(), h, self._height, self.get_id()
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
                msg = 'widget<"{3}"> sizing ({0}) exceeds frame<"{2}"> ' \
                      'width ({1})'.format(dw, self._width, self.get_id(), w.get_id())
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

        for w in self._widgets.keys():
            self._widgets[w][0]._translate = self._pos[w]

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
                msg = 'widget<"{3}"> sizing ({0}) exceeds frame<"{2}"> ' \
                      'height ({1})'.format(dh, self._height, self.get_id(), w.get_id())
                raise _FrameSizeException(msg)

        # Now center widgets
        available = self._height - (ytop - ybottom)
        if wcenter > available:
            msg = 'cannot place center widgets as required height ({0}) ' \
                  'is greater than available ({1}) in frame<"{2}">'.format(wcenter, available, self.get_id())
            raise _FrameSizeException(msg)
        ycenter = int(self._height / 2 - wcenter / 2)
        for w in self._widgets.values():
            w, align, vpos = w
            if vpos == _locals.POSITION_CENTER:
                ycenter += w.get_margin()[1]
                self._pos[w.get_id()] = (self._get_ht(w, align) + w.get_margin()[0], ycenter)
                ycenter += w.get_height()

        for w in self._widgets.keys():
            self._widgets[w][0]._translate = self._pos[w]

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

        # Check if control widget has changed positioning. This fixes centering issues
        cpos = self._control_widget.get_position()
        if self._control_widget_last_pos != cpos:
            self._control_widget_last_pos = cpos
            if self._recursive_render <= 100:
                self._menu.render()
            self._recursive_render += 1
        else:
            self._recursive_render = 0

        return self

    def get_widgets(self, unpack_subframes: bool = True) -> Tuple['Widget', ...]:
        """
        Get widgets as a tuple.

        :param unpack_subframes: If ``True`` add frame widgets instead of frame
        :return: Widget tuple
        """
        wtp = []
        for w in self._widgets.values():
            widget = w[0]
            if isinstance(widget, Frame) and unpack_subframes:
                ww = widget.get_widgets(unpack_subframes=unpack_subframes)
                for i in ww:
                    wtp.append(i)
                continue
            wtp.append(widget)
        return tuple(wtp)

    def unpack(self, widget: 'Widget') -> 'Frame':
        """
        Unpack widget from Frame. If widget does not exist, raises ``ValueError``.

        :param widget: Widget to unpack
        :return: Self reference
        """
        assert len(self._widgets) >0, 'frame is empty'
        wid = widget.get_id()
        if wid not in self._widgets.keys():
            msg = 'widget<"{0}"> does not exist in frame'.format(wid)
            raise ValueError(msg)
        assert widget._frame == self, 'widget frame differs from current'
        widget._frame = None
        widget._translate = (0, 0)
        widget.set_float(False)
        del self._widgets[wid]
        del self._pos[wid]
        self.force_menu_surface_update()
        if self._control_widget == widget:
            if len(self._widgets) == 0:
                self._control_widget = None
                self._control_widget_last_pos = None
            else:
                self._control_widget = self.get_widgets()[0]
                self._control_widget_last_pos = self._control_widget.get_position()
        self.update_indices()
        return self

    def pack(self,
             widget: Union['Widget', List['Widget'], Tuple['Widget', ...]],
             alignment: str = _locals.ALIGN_LEFT,
             vertical_position: PackPositionTypes = _locals.POSITION_NORTH,
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
        :param vertical_position: Vertical position of the widget
        :param margin: *(left, top)* margin of added widget in px. It overrides the previous widget margin
        :return: Added widget reference
        """
        menu = self.get_menu()
        assert menu is not None, \
            'menu must be set before packing widgets'
        if isinstance(widget, (list, tuple)):
            for w in widget:
                self.pack(widget=w, alignment=alignment, vertical_position=vertical_position)
            return widget
        assert isinstance(widget, Widget)
        assert widget.get_id() not in self._widgets.keys(), \
            'widget already in frame'
        assert widget.get_menu() == menu, \
            'widget menu to be added to frame must be in same menu as frame'
        assert widget.get_frame() is None, \
            'widget already is in another frame'
        assert_alignment(alignment)
        assert vertical_position in (_locals.POSITION_NORTH, _locals.POSITION_CENTER, _locals.POSITION_SOUTH), \
            'vertical position must be NORTH, CENTER, or SOUTH'
        assert widget._translate[0] == 0 and widget._translate[1] == 0, \
            'widget cannot have a previous translation if appended. Frame overrides translation'
        assert_vector(margin, 2)

        widget.set_frame(self)
        widget.set_float()
        widget.set_margin(*margin)
        self._widgets[widget.get_id()] = (widget, alignment, vertical_position)

        # Notify menu and sort widgets to keep selection order
        # noinspection PyProtectedMember
        menu_widgets = menu._widgets

        frame_index = menu_widgets.index(self)
        widgt_index = menu_widgets.index(widget)
        assert widgt_index > frame_index, 'widget cannot be appended before frame'
        menu_widgets.pop(widgt_index)
        menu_widgets.insert(frame_index, widget)
        if widget.is_selected():
            widget.select(False)
            menu.select_widget(widget)

        if self._control_widget is None:
            self._control_widget = widget
            self._control_widget_last_pos = self._control_widget.get_position()

        # Render is mandatory as it modifies row/column layout
        menu.render()
        self.update_indices()

        return widget

    def update_indices(self) -> None:
        """
        Update first and last selectable widget index.

        :return: None
        """
        widgs = self.get_widgets(unpack_subframes=False)
        self.first_index = -1
        self.last_index = -1
        for widget in widgs:
            if widget.is_selectable or isinstance(widget, Frame):
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
