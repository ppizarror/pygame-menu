"""
pygame-menu
https://github.com/ppizarror/pygame-menu

IMAGE
Image widget class, adds a simple image.
"""

__all__ = [
    'Image',
    'ImageManager'
]

from abc import ABC
from io import BytesIO
from pathlib import Path

import pygame
import pygame_menu

from pygame_menu.baseimage import BaseImage
from pygame_menu.utils import assert_vector
from pygame_menu.widgets.core.widget import Widget, AbstractWidgetManager

from pygame_menu._types import Union, NumberType, CallbackType, Tuple2NumberType, \
    Optional, NumberInstance, EventVectorType, Callable, Vector2NumberType, Any


# noinspection PyMissingOrEmptyDocstring
class Image(Widget):
    """
    Image widget.

    .. note::

        Image accepts all transformations.

    :param image_path: Path of the image, BytesIO object, or :py:class:`pygame_menu.baseimage.BaseImage` object. If :py:class:`pygame_menu.baseimage.BaseImage` object is provided drawing mode is not considered
    :param image_id: Image ID
    :param angle: Angle of the image in degrees (clockwise)
    :param onselect: Function when selecting the widget
    :param scale: Scale of the image on x-axis and y-axis (x, y) in px
    :param scale_smooth: Scale is smoothed
    """
    _image: 'BaseImage'

    def __init__(
            self,
            image_path: Union[str, 'BaseImage', 'Path', 'BytesIO'],
            angle: NumberType = 0,
            image_id: str = '',
            onselect: CallbackType = None,
            scale: Tuple2NumberType = (1, 1),
            scale_smooth: bool = True
    ) -> None:
        assert isinstance(image_path, (str, Path, BaseImage, BytesIO))
        assert isinstance(image_id, str)
        assert isinstance(angle, NumberInstance)
        assert isinstance(scale_smooth, bool)
        assert_vector(scale, 2)

        super(Image, self).__init__(
            onselect=onselect,
            widget_id=image_id
        )

        if isinstance(image_path, BaseImage):
            self._image = image_path
        else:
            self._image = BaseImage(image_path)
            self._image.rotate(angle)
            self._image.scale(scale[0], scale[1], smooth=scale_smooth)

    def set_title(self, title: str) -> 'Image':
        return self

    def get_image(self) -> 'BaseImage':
        """
        Gets the :py:class:`pygame_menu.baseimage.BaseImage` object from widget.

        :return: Widget image
        """
        return self._image

    def get_angle(self) -> NumberType:
        """
        Return the image angle.

        :return: Angle in degrees
        """
        return self._image.get_angle()

    def set_image(self, image: 'BaseImage') -> None:
        """
        Set the :py:class:`pygame_menu.baseimage.BaseImage` object from widget.

        :param image: Image object
        :return: None
        """
        self._image = image
        self._surface = None
        self._render()

    def _apply_font(self) -> None:
        pass

    def _update_surface(self) -> 'Image':
        """
        Updates surface and renders.

        :return: Self reference
        """
        self._surface = None
        self._render()
        return self

    def scale(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'Image':
        self._image.scale(width, height, smooth)
        return self._update_surface()

    def resize(self, width: NumberType, height: NumberType, smooth: bool = False) -> 'Image':
        self._image.resize(width, height, smooth)
        self._surface = None
        return self._update_surface()

    def set_max_width(self, width: Optional[NumberType], scale_height: NumberType = False,
                      smooth: bool = True) -> 'Image':
        if width is not None and self._image.get_width() > width:
            sx = width / self._image.get_width()
            height = self._image.get_height()
            if scale_height:
                height *= sx
            self._image.resize(width, height, smooth)
            return self._update_surface()
        return self

    def set_max_height(self, height: Optional[NumberType], scale_width: NumberType = False,
                       smooth: bool = True) -> 'Image':
        if height is not None and self._image.get_height() > height:
            sy = height / self._image.get_height()
            width = self._image.get_width()
            if scale_width:
                width *= sy
            self._image.resize(width, height, smooth)
            return self._update_surface()
        return self

    def rotate(self, angle: NumberType) -> 'Image':
        self._image.rotate(angle)
        return self._update_surface()

    def flip(self, x: bool, y: bool) -> 'Image':
        assert isinstance(x, bool)
        assert isinstance(y, bool)
        self._flip = (x, y)
        if x or y:
            self._image.flip(x, y)
            return self._update_surface()
        return self

    def _draw(self, surface: 'pygame.Surface') -> None:
        surface.blit(self._surface, self._rect.topleft)

    def _render(self) -> Optional[bool]:
        if self._surface is not None:
            return True
        self._surface = self._image.get_surface(new=False)
        self._rect.width, self._rect.height = self._surface.get_size()
        if not self._render_hash_changed(self._visible):
            return True
        self.force_menu_surface_update()

    def update(self, events: EventVectorType) -> bool:
        self.apply_update_callbacks(events)
        for event in events:
            if self._check_mouseover(event):
                break
        return False


class ImageManager(AbstractWidgetManager, ABC):
    """
    Image manager.
    """

    def image(
            self,
            image_path: Union[str, 'Path', 'pygame_menu.BaseImage', 'BytesIO'],
            angle: NumberType = 0,
            image_id: str = '',
            onselect: Optional[Callable[[bool, 'Widget', 'pygame_menu.Menu'], Any]] = None,
            scale: Vector2NumberType = (1, 1),
            scale_smooth: bool = True,
            selectable: bool = False,
            **kwargs
    ) -> 'pygame_menu.widgets.Image':
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
            - ``float``                         (bool) - If ``True`` the widget don't contributes width/height to the Menu widget positioning computation, and don't add one unit to the rows
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
            stored in ``_current`` pointer); for such behaviour apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        :param image_path: Path of the image (file) or a BaseImage object. If BaseImage object is provided the angle and scale are ignored
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
        assert isinstance(selectable, bool)

        # Remove invalid keys from kwargs
        for key in list(kwargs.keys()):
            if key not in ('align', 'background_color', 'background_inflate',
                           'border_color', 'border_inflate', 'border_width',
                           'cursor', 'margin', 'padding', 'selection_color',
                           'selection_effect', 'border_position', 'float',
                           'float_origin_position', 'shadow_color', 'shadow_radius',
                           'shadow_type', 'shadow_width'):
                kwargs.pop(key, None)

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        widget = Image(
            angle=angle,
            image_id=image_id,
            image_path=image_path,
            onselect=onselect,
            scale=scale,
            scale_smooth=scale_smooth
        )
        widget.is_selectable = selectable

        self._check_kwargs(kwargs)
        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
