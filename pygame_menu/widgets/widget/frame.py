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

import warnings

import pygame
import pygame_menu
import pygame_menu.locals as _locals

from pygame_menu._decorator import Decorator
from pygame_menu.utils import assert_alignment, make_surface, assert_vector, assert_orientation
from pygame_menu.widgets.core import Widget

from pygame_menu._types import Optional, NumberType, Dict, Tuple, Union, List, Vector2NumberType, \
    Tuple2IntType, NumberInstance, Any, ColorInputType, EventVectorType


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

    .. note::

        Frames should be appended to Menu scrollable frames if it's scrollable,
        be careful when removing. Check :py:class:`pygame_menu.widgets.DropSelect`
        as a complete example of Frame implementation within another Widgets.

    :param width: Frame width (px)
    :param height: Frame height (px)
    :param orientation: Frame orientation (horizontal or vertical). See :py:mod:`pygame_menu.locals`
    :param frame_id: ID of the frame
    """
    _control_widget: Optional['Widget']
    _control_widget_last_pos: Optional[Vector2NumberType]
    _frame_scrollarea: Optional['pygame_menu.scrollarea.ScrollArea']
    _has_frames: bool  # True if frame has packed other frames
    _height: int
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
        assert width > 0, 'width must be greater than zero ({0} received)'.format(width)
        assert height > 0, 'height must be greater than zero ({0} received)'.format(height)
        assert_orientation(orientation)

        # Internals
        self._control_widget = None
        self._control_widget_last_pos = None  # This checks if menu has updated widget position
        self._frame_scrollarea = None
        self._has_frames = False
        self._height = int(height)
        self._orientation = orientation
        self._pack_margin_warning = True  # Set to False for hiding the pack margin warning
        self._pos = {}
        self._real_rect = pygame.Rect(0, 0, width, height)
        self._recursive_render = 0
        self._relax = False  # If True ignore sizing
        self._widgets = {}
        self._widgets_props = {}
        self._width = int(width)

        # Configure widget publics
        self.first_index = -1
        self.horizontal = orientation == _locals.ORIENTATION_HORIZONTAL
        self.is_scrollable = False
        self.is_selectable = False
        self.last_index = -1

    def get_inner_size(self) -> Tuple2IntType:
        """
        Return Frame inner size (width, height).

        :return: Size tuple in px
        """
        return self._width, self._height

    # noinspection PyProtectedMember
    def _sort_menu_scrollable_frames(self) -> None:
        """
        Sort the menu scrollable frames.

        :return: None
        """
        if self._menu is not None and self.is_scrollable:
            if len(self._menu._scrollable_frames) == 0:
                return
            widgets: List[Tuple[int, 'Widget']] = []
            for w in self._menu._scrollable_frames:
                if isinstance(w, Frame):
                    sa = w.get_scrollarea(inner=True)
                else:
                    sa = w.get_scrollarea()
                widgets.append((-sa.get_depth(), w))
            widgets.sort(key=lambda x: x[0])
            self._menu._scrollable_frames = []
            for w in widgets:
                self._menu._scrollable_frames.append(w[1])

    def on_remove_from_menu(self) -> 'Frame':
        for w in self.get_widgets(unpack_subframes=False):
            self.unpack(w)
        self.update_indices()
        return self

    # noinspection PyProtectedMember
    def set_menu(self, menu: Optional['pygame_menu.Menu']) -> 'Frame':
        # If menu is set, remove from previous scrollable if enabled
        if self._menu is not None and self.is_scrollable:
            scrollable_widgets = self._menu._scrollable_frames
            if self in scrollable_widgets:
                scrollable_widgets.remove(self)

        # Update menu
        super(Frame, self).set_menu(menu)

        # Add self to scrollable
        if self.is_scrollable and self._menu is not None:
            self._menu._scrollable_frames.append(self)
            self._sort_menu_scrollable_frames()

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
        Returns the max size of the frame.

        :return: Max (width, height) in px
        """
        if self._frame_scrollarea is not None:
            return self._frame_scrollarea.get_size(inner=True)
        return self.get_size()

    def make_scrollarea(
            self,
            max_width: Optional[NumberType],
            max_height: Optional[NumberType],
            scrollarea_color: Optional[ColorInputType],
            scrollbar_color: ColorInputType,
            scrollbar_cursor: Optional[Union[int, 'pygame.cursors.Cursor']],
            scrollbar_shadow: bool,
            scrollbar_shadow_color: ColorInputType,
            scrollbar_shadow_offset: int,
            scrollbar_shadow_position: str,
            scrollbar_slider_color: ColorInputType,
            scrollbar_slider_pad: NumberType,
            scrollbar_thick: NumberType,
            scrollbars: Union[str, Tuple[str, ...]],
    ) -> 'Frame':
        """
        Make the scrollarea of the frame.

        :param max_width: Maximum width of the scrollarea (px)
        :param max_height: Maximum height of the scrollarea (px)
        :param scrollarea_color: Scroll area color. If ``None`` area is transparent
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
        assert len(self._widgets.keys()) == 0, 'frame widgets must be empty if creating the scrollarea'
        assert self.configured, 'frame must be configured before adding the scrollarea'
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
            # Configure rect
            self._rect.height = self._height
            self._rect.width = self._width
            self._frame_scrollarea = None

            # If in previous scrollable frames
            if self._menu is not None and self.is_scrollable:
                # noinspection PyProtectedMember
                scrollable_frames = self._menu._scrollable_frames
                if self in scrollable_frames:
                    scrollable_frames.remove(self)

            self.is_scrollable = False
            return self

        # Create area object
        self._frame_scrollarea = pygame_menu.scrollarea.ScrollArea(
            area_color=scrollarea_color,
            area_height=max_height + sx,
            area_width=max_width + sy,
            parent_scrollarea=self._scrollarea,
            scrollbar_color=scrollbar_color,
            scrollbar_cursor=scrollbar_cursor,
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
        self._surface = make_surface(self._width, self._height, alpha=True)

        # Configure area
        self._frame_scrollarea.set_world(self._surface)

        # Configure rect
        self._rect.height = max_height + sx
        self._rect.width = max_width + sy

        return self

    def get_indices(self) -> Tuple[int, int]:
        """
        Return first and last selectable indices tuple.

        :return: First, Last widget selectable indices
        """
        return self.first_index, self.last_index

    def update(self, events: EventVectorType) -> bool:
        if not self.is_scrollable or not self._visible or self.readonly:
            return False
        return self._frame_scrollarea.update(events)

    def select(self, *args, **kwargs) -> 'Frame':
        return self

    def set_selection_effect(self, *args, **kwargs) -> 'Frame':
        pass

    def _apply_font(self) -> None:
        pass

    def _render(self) -> None:
        pass

    def _draw(self, *args, **kwargs) -> None:
        pass

    def scale(self, *args, **kwargs) -> 'Frame':
        return self

    def resize(self, *args, **kwargs) -> 'Frame':
        return self

    def set_max_width(self, *args, **kwargs) -> 'Frame':
        return self

    def set_max_height(self, *args, **kwargs) -> 'Frame':
        return self

    def rotate(self, *args, **kwargs) -> 'Frame':
        return self

    def flip(self, *args, **kwargs) -> 'Frame':
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
            self._frame_scrollarea.set_position(self._rect.x, self._rect.y)
        return self

    def draw(self, surface: 'pygame.Surface') -> 'Frame':
        if not self.is_visible():
            return self

        selected_widget = None

        # Simple case, no scrollarea
        if not self.is_scrollable:
            self.last_surface = surface
            self._draw_background_color(surface)
            self._decorator.draw_prev(surface)
            for widget in self._widgets.values():
                if widget.is_selected():
                    selected_widget = widget
                widget.draw(surface)
            if selected_widget is not None:
                selected_widget.draw_after_if_selected(surface)
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
            for widget in self._widgets.values():
                if widget.is_selected():
                    selected_widget = widget
                widget.draw(self._surface)
            if selected_widget is not None:
                selected_widget.draw_after_if_selected(self._surface)
            self._frame_scrollarea.draw(surface)
            if selected_widget is not None and selected_widget.last_surface != self._surface:  # Draw after was not completed
                selected_widget.draw_after_if_selected(None)
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
        if w > self._width and not self._relax:
            raise _FrameSizeException(
                '{0} width ({1}) is greater than {3} width ({2}), try using '
                'widget.set_max_width(...) for avoiding this issue, or set '
                'the widget as floating'.format(
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
        if h > self._height and not self._relax:
            raise _FrameSizeException(
                '{0} height ({1}) is greater than {3} height ({2}), try using '
                'widget.set_max_height(...) for avoiding this issue, or set '
                'the widget as floating'.format(
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
            align, vpos = self._widgets_props[w.get_id()]
            if not w.is_visible() or w.is_floating():
                continue
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
            if dw > self._width and not self._relax:
                msg = '{3} width ({0}) exceeds {2} width ({1})' \
                      ''.format(dw, self._width, self.get_class_id(), w.get_class_id())
                raise _FrameSizeException(msg)

        # Now center widgets
        available = self._width - (xleft - xright)
        if wcenter > available and not self._relax:
            msg = 'cannot place center widgets as required width ({0}) ' \
                  'is greater than available ({1}) in {2}'.format(wcenter, available, self.get_class_id())
            raise _FrameSizeException(msg)
        xcenter = int(self._width / 2 - wcenter / 2)
        for w in self._widgets.values():
            align, vpos = self._widgets_props[w.get_id()]
            if not w.is_visible() or w.is_floating():
                continue
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
            align, vpos = self._widgets_props[w.get_id()]
            if not w.is_visible() or w.is_floating():
                continue
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
            if dh > self._height and not self._relax:
                msg = '{3} height ({0}) exceeds {2} height ({1})' \
                      ''.format(dh, self._height, self.get_class_id(), w.get_class_id())
                raise _FrameSizeException(msg)

        # Now center widgets
        available = self._height - (ytop - ybottom)
        if wcenter > available and not self._relax:
            msg = 'cannot place center widgets as required height ({0}) ' \
                  'is greater than available ({1}) in {2}'.format(wcenter, available, self.get_class_id())
            raise _FrameSizeException(msg)
        ycenter = int(self._height / 2 - wcenter / 2)
        for w in self._widgets.values():
            align, vpos = self._widgets_props[w.get_id()]
            if not w.is_visible() or w.is_floating():
                continue
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
            widget = self._widgets[w]
            if not widget.is_visible():
                widget.set_position(0, 0)
                continue
            if widget.is_floating():
                tx = 0
                ty = 0
            else:
                tx, ty = self._pos[w]
            if widget.get_menu() is None:  # Widget is only appended to Frame
                fx, fy = self.get_position()
                margin = widget.get_margin()
                padding = widget.get_padding()
                widget.set_position(fx + margin[0] + padding[3], fy + padding[0])
            if self.is_scrollable and isinstance(widget, Frame) and widget.is_scrollable:
                widget.get_scrollarea(inner=True).set_position(tx, ty)
            if self._frame_scrollarea is not None:  # If scrollarea, subtract this position to each widget
                sx, sy = self._frame_scrollarea.get_position()
                tx -= sx
                ty -= sy
            widget._translate_virtual = (tx, ty)  # Translate to scrollarea

        # Check if control widget has changed positioning. This fixes centering issues
        if self._control_widget is not None:
            cpos = self._control_widget.get_position()
            if self._control_widget_last_pos != cpos:
                self._control_widget_last_pos = cpos
                if self._recursive_render <= 100 and self._menu is not None:
                    self._menu.render()
                self._recursive_render += 1
            else:
                self._recursive_render = 0

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
        unpackd = []
        for w in self.get_widgets(unpack_subframes=False):
            self.unpack(w)
            unpackd.append(w)
        return tuple(unpackd)

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

    def get_scrollarea(self, inner: bool = False) -> Optional['pygame_menu.scrollarea.ScrollArea']:
        """
        Return the scrollarea object.

        :param inner: If ``True`` return the inner scrollarea
        :return: ScrollArea object
        """
        if inner:
            return self._frame_scrollarea
        return self._scrollarea

    def set_scrollarea(self, scrollarea: Optional['pygame_menu.scrollarea.ScrollArea']) -> None:
        self._scrollarea = scrollarea
        if self._frame_scrollarea is not None:
            self._frame_scrollarea.set_parent_scrollarea(scrollarea)
        else:
            for w in self.get_widgets(unpack_subframes=False):
                w.set_scrollarea(scrollarea)

    def scrollh(self, value: NumberType) -> 'Frame':
        """
        Scroll to horizontal value if frame is scrollable.

        :param value: Horizontal scroll value, if ``0`` scroll to left; ``1`` scroll to right
        :return: Self reference
        """
        if self._frame_scrollarea is not None:
            self._frame_scrollarea.scroll_to(_locals.ORIENTATION_HORIZONTAL, value)
        return self

    def scrollv(self, value: NumberType) -> 'Frame':
        """
        Scroll to vertical value if frame is scrollable.

        :param value: Vertical scroll value, if ``0`` scroll to top; ``1`` scroll to bottom
        :return: Self reference
        """
        if self._frame_scrollarea is not None:
            self._frame_scrollarea.scroll_to(_locals.ORIENTATION_VERTICAL, value)
        return self

    def get_scroll_value_percentual(self, orientation: str) -> float:
        """
        Get the scroll value in percentage, if ``0`` the scroll is at top/left, ``1`` bottom/right.

        .. note::

            If ScrollArea does not contain such orientation scroll, or frame is not scrollable,
            ``-1`` is returned.

        :param orientation: Orientation. See :py:mod:`pygame_menu.locals`
        :return: Value from ``0`` to ``1``
        """
        if self._frame_scrollarea is not None:
            return self._frame_scrollarea.get_scroll_value_percentual(orientation)
        return -1

    # noinspection PyProtectedMember
    def unpack(self, widget: 'Widget') -> 'Frame':
        """
        Unpack widget from Frame. If widget does not exist, raises ``ValueError``.
        Unpacked widgets adopt a floating position and are moved to the last position of the widget list of Menu

        :param widget: Widget to unpack
        :return: Unpacked widget
        """
        assert widget != self, 'frame cannot unpack itself'
        assert len(self._widgets) > 0, 'frame is empty'
        wid = widget.get_id()
        if wid not in self._widgets.keys():
            msg = '{0} does not exist in {1}'.format(widget.get_class_id(), self.get_class_id())
            raise ValueError(msg)
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
        if widget.get_menu() == self._menu and self._menu is not None:
            self._menu._validate_frame_widgetmove = False
            try:
                self._menu.move_widget_index(widget, render=False)
            except (ValueError, AssertionError):  # Assertion error if moving widget (last) to same position (last)
                pass
            if isinstance(widget, Frame):
                widgets = widget.get_widgets(unpack_subframes_include_frame=True)
                for w in widgets:
                    if w.get_menu() is None:
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
        if self._menu is not None:
            self._menu._render()

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

        return widget

    # noinspection PyProtectedMember
    def pack(
            self,
            widget: Union['Widget', List['Widget'], Tuple['Widget', ...]],
            alignment: str = _locals.ALIGN_LEFT,
            vertical_position: str = _locals.POSITION_NORTH,
            margin: Vector2NumberType = (0, 0)) -> Union['Widget', List['Widget'], Tuple['Widget', ...], Any]:
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
        :param alignment: Widget alignment
        :param vertical_position: Vertical position of the widget within frame. See :py:mod:`pygame_menu.locals`
        :param margin: (left, top) margin of added widget in px. It overrides the previous widget margin
        :return: Added widget references
        """
        assert self._menu is not None, \
            'frame menu must be set before packing widgets'
        if isinstance(widget, (tuple, list)):
            for w in widget:
                self.pack(widget=w, alignment=alignment, vertical_position=vertical_position)
            return widget
        assert isinstance(widget, Widget)
        if isinstance(widget, Frame):
            assert widget.get_menu() is not None, \
                '{0} menu cannot be None'.format(widget.get_class_id())
        assert widget.get_id() not in self._widgets.keys(), \
            '{0} already exists in {1}'.format(widget.get_class_id(), self.get_class_id())
        assert widget.get_menu() == self._menu or widget.get_menu() is None, \
            'widget menu to be added to frame must be in same menu as frame, or it can have any Menu instance'
        assert widget.get_frame() is None, \
            '{0} is already packed in {1}'.format(widget.get_class_id(), widget.get_frame().get_class_id())
        assert_alignment(alignment)
        assert vertical_position in (_locals.POSITION_NORTH, _locals.POSITION_CENTER, _locals.POSITION_SOUTH), \
            'vertical position must be NORTH, CENTER, or SOUTH'
        assert_vector(margin, 2)
        assert widget.configured, 'widget must be configured before packing'

        if widget.get_margin() != (0, 0) and self._pack_margin_warning:
            msg = '{0} margin should be (0, 0) if packed, but received {1}; {2}.pack() does not consider ' \
                  'previous widget margin. Set frame._pack_margin_warning=False to hide this warning' \
                  ''.format(widget.get_class_id(), widget.get_margin(), self.get_class_id())
            warnings.warn(msg)

        if isinstance(widget, Frame):
            widget.update_indices()

        widget.set_frame(self)
        widget.set_margin(*margin)
        if self._frame_scrollarea is not None:
            widget.set_scrollarea(self._frame_scrollarea)
            self._sort_menu_scrollable_frames()
        else:
            widget.set_scrollarea(self._scrollarea)
        self._widgets[widget.get_id()] = widget
        self._widgets_props[widget.get_id()] = (alignment, vertical_position)

        # Sort widgets to keep selection order
        menu_widgets = self._menu._widgets
        if widget.get_menu() is not None and widget in menu_widgets:
            self._menu._validate_frame_widgetmove = False
            widgets_list = list(self._widgets.values())

            # Move frame to last
            if len(self._widgets) > 1:
                wlast = widgets_list[-2]  # -1 is the last added
                for i in range(2, len(self._widgets)):
                    if wlast.get_menu() is None and len(self._widgets) > 2:
                        wlast = widgets_list[-(i + 1)]
                    else:
                        break

                # Check for last if wlast is frame
                while True:
                    if not (isinstance(wlast, Frame) and wlast.get_indices() != (-1, -1)) or wlast.get_menu() is None:
                        break
                    wlast = menu_widgets[wlast.last_index]

                if wlast.get_menu() == self._menu:
                    self._menu.move_widget_index(self, wlast, render=False)

            # Swap
            self._menu.move_widget_index(widget, self, render=False)
            if isinstance(widget, Frame):
                reverse = menu_widgets.index(widget) == len(menu_widgets) - 1
                widgs = widget.get_widgets(unpack_subframes_include_frame=True, reverse=reverse)
                for w in widgs:
                    if w.get_menu() is None:
                        continue
                    self._menu.move_widget_index(w, self, render=False)
                if len(widgs) >= 1:
                    swap_target = widgs[-1]
                    if not reverse:
                        swap_target = widgs[0]
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
        self._menu.move_widget_index(None, update_selected_index=True)

        # Render is mandatory as it modifies row/column layout
        try:
            self.update_position()
            self._menu._render()
        except _FrameSizeException:
            self.unpack(widget)
            raise

        # Request scroll if widget is selected
        if widget.is_selected():
            widget.scroll_to_widget()
            widget.scroll_to_widget()

        return widget

    def contains_widget(self, widget: 'Widget') -> bool:
        """
        Returns true if the frame contains the given widget.

        :param widget: Widget to check
        :return: ``True`` if widget within frame
        """
        return widget.get_frame() == self and widget.get_id() in self._widgets.keys()

    def update_indices(self) -> 'Frame':
        """
        Update first and last selectable widget index.

        :return: Self reference
        """
        if not self._has_frames:  # Public index update only triggered if frame does not contain subframes
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
        if self.get_frame() is not None:
            self.get_frame()._update_indices()


class _FrameSizeException(Exception):
    """
    If widget size is greater than frame raises exception.
    """
    pass
