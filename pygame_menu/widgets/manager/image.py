"""
pygame-menu
https://github.com/ppizarror/pygame-menu

IMAGE MANAGER
Base class for ImageManager.
"""

from __future__ import annotations

__all__ = ["ImageManager"]

from abc import ABC
from io import BytesIO
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pygame

from pygame_menu.baseimage import BaseImage
from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.image import Image

if TYPE_CHECKING:
    from collections.abc import Callable

    import pygame_menu
    from pygame_menu._types import NumberType, Vector2NumberType
    from pygame_menu.widgets.core.widget import Widget


class ImageManager(AbstractWidgetManager, ABC):
    """
    Image manager.
    """

    def image(
        self,
        image_path: str | Path | BaseImage | BytesIO | pygame.Surface,
        angle: NumberType = 0,
        image_id: str = "",
        onselect: Callable[[bool, Widget, pygame_menu.Menu], Any] | None = None,
        scale: Vector2NumberType = (1, 1),
        scale_smooth: bool = True,
        selectable: bool = False,
        **kwargs,
    ) -> Image:
        """
        Add a simple image to the Menu.

        If ``onselect`` is defined, the callback is executed as follows, where
        ``selected`` is a boolean representing the selected status:

        .. code-block:: python

            onselect(selected, widget, menu)

        kwargs (Optional)
            - ``align``                         (str) – Widget `alignment <https://pygame-menu.readthedocs.io/en/latest/_source/themes.html#alignment>`_
            - ``background_color``              (tuple, list, str, int, :py:class:`pygame.Color`, :py:class:`pygame_menu.baseimage.BaseImage`) – Color of the background. ``None`` for no-color
            - ``background_inflate``            (tuple, list) – Inflate background on x-axis and y-axis (x, y) in px
            - ``border_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Widget border color. ``None`` for no-color
            - ``border_inflate``                (tuple, list) – Widget border inflate on x-axis and y-axis (x, y) in px
            - ``border_position``               (str, tuple, list) – Widget border positioning. It can be a single position, or a tuple/list of positions. Only are accepted: north, south, east, and west. See :py:mod:`pygame_menu.locals`
            - ``border_width``                  (int) – Border width in px. If ``0`` disables the border
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect. Applied only if ``selectable`` is ``True``
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param image_path: Path of the image (file), a pygame.Surface, or a BaseImage object. If BaseImage object is provided the angle and scale are ignored
        :param angle: Angle of the image in degrees (clockwise)
        :param image_id: ID of the image
        :param onselect: Callback executed when selecting the widget; only executed if ``selectable`` is ``True``
        :param scale: Scale of the image on x-axis and y-axis (x, y)
        :param scale_smooth: Scale is smoothed
        :param selectable: Image accepts user selection
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.Image`
        """
        assert isinstance(image_path, (str, Path, BaseImage, BytesIO, pygame.Surface))
        assert isinstance(selectable, bool)

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
                "selection_color",
                "selection_effect",
                "border_position",
                "float",
                "float_origin_position",
                "shadow_color",
                "shadow_radius",
                "shadow_type",
                "shadow_width",
            ):
                kwargs.pop(key, None)

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        widget = Image(
            angle=angle,
            image_id=image_id,
            image_path=image_path,
            onselect=onselect,
            scale=scale,
            scale_smooth=scale_smooth,
        )
        widget.is_selectable = selectable

        self._check_kwargs(kwargs)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
