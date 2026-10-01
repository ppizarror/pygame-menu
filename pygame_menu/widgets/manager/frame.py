"""
pygame-menu
https://github.com/ppizarror/pygame-menu

FRAME MANAGER
Base class for FrameManager.
"""

from __future__ import annotations

__all__ = ["FrameManager"]

from abc import ABC
from typing import TYPE_CHECKING

from pygame_menu.locals import (
    ORIENTATION_HORIZONTAL,
    ORIENTATION_VERTICAL,
)
from pygame_menu.utils import parse_padding
from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.frame import Frame

if TYPE_CHECKING:
    from pygame_menu._types import NumberType


class FrameManager(AbstractWidgetManager, ABC):
    """
    Frame manager.
    """

    def _frame(
        self,
        width: NumberType,
        height: NumberType,
        orientation: str,
        frame_id: str = "",
        **kwargs,
    ) -> Frame:
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
            if key not in (
                "align",
                "background_color",
                "background_inflate",
                "border_color",
                "border_inflate",
                "border_width",
                "cursor",
                "margin",
                "padding",
                "max_height",
                "max_width",
                "scrollbar_color",
                "scrollbar_cursor",
                "scrollbar_shadow_color",
                "scrollbar_shadow_offset",
                "scrollbar_shadow_position",
                "scrollbar_shadow",
                "scrollbar_slider_color",
                "scrollbar_slider_pad",
                "scrollbar_thick",
                "scrollbars",
                "scrollarea_color",
                "border_position",
                "scrollbar_slider_hover_color",
                "tab_size",
                "float",
                "float_origin_position",
            ):
                kwargs.pop(key, None)

        attributes = self._filter_widget_attributes(kwargs)
        pad = parse_padding(attributes["padding"])  # top, right, bottom, left
        pad_h = pad[1] + pad[3]
        pad_v = pad[0] + pad[2]

        assert width > pad_h, (
            f"frame width ({width}) cannot be lower than horizontal padding size ({pad_h})"
        )
        assert height > pad_v, (
            f"frame height ({height}) cannot be lower than vertical padding size ({pad_v})"
        )

        widget = Frame(
            width=width - pad_h,
            height=height - pad_v,
            orientation=orientation,
            frame_id=frame_id,
        )
        self._configure_widget(widget=widget, **attributes)

        widget.make_scrollarea(
            max_height=kwargs.pop("max_height", height) - pad_v,
            max_width=kwargs.pop("max_width", width) - pad_h,
            scrollarea_color=kwargs.pop("scrollarea_color", None),
            scrollbar_color=kwargs.pop("scrollbar_color", self._theme.scrollbar_color),
            scrollbar_cursor=kwargs.pop(
                "scrollbar_cursor", self._theme.scrollbar_cursor
            ),
            scrollbar_shadow=kwargs.pop(
                "scrollbar_shadow", self._theme.scrollbar_shadow
            ),
            scrollbar_shadow_color=kwargs.pop(
                "scrollbar_shadow_color", self._theme.scrollbar_shadow_color
            ),
            scrollbar_shadow_offset=kwargs.pop(
                "scrollbar_shadow_offset", self._theme.scrollbar_shadow_offset
            ),
            scrollbar_shadow_position=kwargs.pop(
                "scrollbar_shadow_position", self._theme.scrollbar_shadow_position
            ),
            scrollbar_slider_color=kwargs.pop(
                "scrollbar_slider_color", self._theme.scrollbar_slider_color
            ),
            scrollbar_slider_hover_color=kwargs.pop(
                "scrollbar_slider_hover_color", self._theme.scrollbar_slider_hover_color
            ),
            scrollbar_slider_pad=kwargs.pop(
                "scrollbar_slider_pad", self._theme.scrollbar_slider_pad
            ),
            scrollbar_thick=kwargs.pop("scrollbar_thick", self._theme.scrollbar_thick),
            scrollbars=get_scrollbars_from_position(
                kwargs.pop("scrollbars", self._theme.scrollarea_position)
            ),
        )

        self._append_widget(widget)
        self._check_kwargs(kwargs)

        return widget

    def frame_h(
        self, width: NumberType, height: NumberType, frame_id: str = "", **kwargs
    ) -> Frame:
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
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
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
            stored in ``_current`` pointer); for such behavior apply to
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
        self, width: NumberType, height: NumberType, frame_id: str = "", **kwargs
    ) -> Frame:
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
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
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
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param width: Frame width in px
        :param height: Frame height in px
        :param frame_id: ID of the vertical frame
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Frame`
        """
        return self._frame(width, height, ORIENTATION_VERTICAL, frame_id, **kwargs)
