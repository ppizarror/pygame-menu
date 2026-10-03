"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PROGRESS BAR MANAGER
Base class for ProgressBarManager.
"""

from __future__ import annotations

__all__ = ["ProgressBarManager"]

from abc import ABC
from typing import TYPE_CHECKING, Any

from pygame_menu.locals import (
    ORIENTATION_HORIZONTAL,
    ORIENTATION_VERTICAL,
)
from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager
from pygame_menu.widgets.widget.progressbar import (
    ProgressBar,
    ProgressBarTextFormatType,
)

if TYPE_CHECKING:
    from pygame_menu._types import (
        CallbackType,
        NumberType,
    )


class ProgressBarManager(AbstractWidgetManager, ABC):
    """
    ProgressBar manager.
    """

    def progress_bar(
        self,
        title: Any,
        default: NumberType = 0,
        min_value: NumberType = 0,
        max_value: NumberType = 100,
        height: int = 20,
        orientation: str = ORIENTATION_HORIZONTAL,
        onselect: CallbackType = None,
        progressbar_id: str = "",
        progress_text_format: ProgressBarTextFormatType = lambda x: str(round(x, 1)),
        selectable: bool = False,
        width: int = 150,
        **kwargs,
    ) -> ProgressBar:
        """
        Add a progress bar, which offers a bar that accepts a percentage from
        ``min_value`` to ``max_value``.

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
            - ``box_background_color``          (tuple, list, str, int, :py:class:`pygame.Color`) – Background color of the box
            - ``box_border_color``              (tuple, list, str, int, :py:class:`pygame.Color`) – Border color of the box
            - ``box_border_width``              (int) - Border width of the box in px
            - ``box_margin``                    (tuple, list) - Box margin on x-axis and y-axis (x, y) respect to the title of the widget in px
            - ``box_progress_color``            (tuple, list, str, int, :py:class:`pygame.Color`) – Box progress color
            - ``box_progress_padding``          (int, float, tuple, list) – Box progress padding
            - ``cursor``                        (int, :py:class:`pygame.cursors.Cursor`, None) – Cursor of the widget if the mouse is placed over
            - ``float``                         (bool) - If ``True`` the widget don't contribute width/height to the Menu widget positioning computation, and don't add one unit to the rows
            - ``float_origin_position``         (bool) - If ``True`` the widget position is set to the top-left position of the Menu if the widget is floating
            - ``font_background_color``         (tuple, list, str, int, :py:class:`pygame.Color`, None) – Widget font background color
            - ``font_color``                    (tuple, list, str, int, :py:class:`pygame.Color`) – Widget font color
            - ``font_name``                     (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Widget font path
            - ``font_shadow_color``             (tuple, list, str, int, :py:class:`pygame.Color`) – Font shadow color
            - ``font_shadow_offset``            (int) – Font shadow offset in px
            - ``font_shadow_position``          (str) – Font shadow position, see locals for position
            - ``font_shadow``                   (bool) – Font shadow is enabled or disabled
            - ``font_size``                     (int) – Font size of the widget
            - ``margin``                        (tuple, list) – Widget (left, bottom) margin in px
            - ``padding``                       (int, float, tuple, list) – Widget padding according to CSS rules. General shape: (top, right, bottom, left)
            - ``progress_text_align``           (str) - Align of the progress text, can be CENTER, LEFT or RIGHT. See :py:mod:`pygame_menu.locals`
            - ``progress_text_enabled``         (bool) - Enables the progress text over box
            - ``progress_text_font_color``      (tuple, list, str, int, :py:class:`pygame.Color`) – Progress font color. If ``None`` uses the same as the widget font
            - ``progress_text_font_hfactor``    (int, float) - Height factor of the font height relative to the widget font height
            - ``progress_text_font``            (str, :py:class:`pathlib.Path`, :py:class:`pygame.font.Font`) – Progress font. If ``None`` uses the same as the widget font
            - ``progress_text_margin``          (tuple, list) - Margin of the progress box on x-axis and y-axis in px
            - ``progress_text_placeholder``     (str) - Placeholder of the progress text, which considers as format the output of ``progress_text_format``. ``"{0} %"`` by default
            - ``readonly_color``                (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode
            - ``readonly_selected_color``       (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget if readonly mode and is selected
            - ``selection_color``               (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the selected widget; only affects the font color
            - ``selection_effect``              (:py:class:`pygame_menu.widgets.core.Selection`) – Widget selection effect
            - ``shadow_color``                  (tuple, list, str, int, :py:class:`pygame.Color`) – Color of the widget shadow
            - ``shadow_radius``                 (int) - Border radius of the shadow
            - ``shadow_type``                   (str) - Shadow type, it can be ``'rectangular'`` or ``'ellipse'``
            - ``shadow_width``                  (int) - Width of the shadow. If ``0`` the shadow is disabled
            - ``tab_size``                      (int) – Width of a tab character

        .. note::

            All theme-related optional kwargs use the default Menu theme if not
            defined.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Be careful with kwargs collision. Consider that all optional documented
            kwargs keys are removed from the object.

        :param title: Title of the progress bar
        :param default: Default value of the progressbar, from ``0`` to ``100``
        :param onselect: Callback executed when selecting the widget
        :param progressbar_id: ID of the progress bar
        :param progress_text_format: Format function of the progress text, which considers as input the progress value (0-100)
        :param selectable: Progress bar accepts user selection
        :param width: Progress bar width in px
        :param kwargs: Optional keyword arguments
        :return: Widget object
        :rtype: :py:class:`pygame_menu.widgets.ProgressBar`
        """
        assert isinstance(selectable, bool)
        assert orientation in (ORIENTATION_HORIZONTAL, ORIENTATION_VERTICAL), (
            "orientation must be ORIENTATION_HORIZONTAL or ORIENTATION_VERTICAL"
        )

        # Filter widget attributes to avoid passing them to the callbacks
        attributes = self._filter_widget_attributes(kwargs)

        box_background_color = kwargs.pop(
            "box_background_color", self._theme.widget_box_background_color
        )
        box_border_color = kwargs.pop(
            "box_border_color", self._theme.widget_box_border_color
        )
        box_border_width = kwargs.pop(
            "box_border_width", self._theme.widget_box_border_width
        )
        box_margin = kwargs.pop("box_margin", self._theme.widget_box_margin)
        box_progress_color = kwargs.pop("box_progress_color", (53, 172, 78))
        progress_text_font_color = kwargs.pop(
            "progress_text_font_color", self._theme.widget_font_color
        )

        widget = ProgressBar(
            title=title,
            progressbar_id=progressbar_id,
            default=default,
            min_value=min_value,
            max_value=max_value,
            width=width,
            height=height,
            orientation=orientation,
            onselect=onselect,
            box_background_color=box_background_color,
            box_border_color=box_border_color,
            box_border_width=box_border_width,
            box_margin=box_margin,
            box_progress_color=box_progress_color,
            progress_text_font_color=progress_text_font_color,
            progress_text_format=progress_text_format,
            **kwargs,
        )
        widget.is_selectable = selectable

        self._configure_widget(widget=widget, **attributes)
        self._append_widget(widget)

        return widget
