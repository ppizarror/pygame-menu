"""
pygame-menu
https://github.com/ppizarror/pygame-menu

MENU WIDGET MANAGER
Easy widget add/remove to Menus.
"""

from __future__ import annotations

__all__ = ["WidgetManager"]

from typing import Any

import pygame_menu
from pygame_menu._base import Base
from pygame_menu._types import PaddingInstance
from pygame_menu.font import assert_font
from pygame_menu.utils import (
    assert_color,
    assert_cursor,
    assert_position_vector,
    assert_vector,
    warn,
)

# Import widgets
from pygame_menu.widgets.core.widget import Widget, check_widget_mouseleave
from pygame_menu.widgets.widget.button import ButtonManager
from pygame_menu.widgets.widget.colorinput import ColorInputManager
from pygame_menu.widgets.widget.dropselect import DropSelectManager
from pygame_menu.widgets.widget.dropselect_multiple import DropSelectMultipleManager
from pygame_menu.widgets.widget.frame import FrameManager
from pygame_menu.widgets.widget.hmargin import HMarginManager
from pygame_menu.widgets.widget.image import ImageManager
from pygame_menu.widgets.widget.label import LabelManager
from pygame_menu.widgets.widget.menulink import MenuLinkManager
from pygame_menu.widgets.widget.none import NoneWidgetManager
from pygame_menu.widgets.widget.progressbar import ProgressBarManager
from pygame_menu.widgets.widget.rangeslider import RangeSliderManager
from pygame_menu.widgets.widget.selector import SelectorManager
from pygame_menu.widgets.widget.surface import SurfaceWidgetManager
from pygame_menu.widgets.widget.table import TableManager
from pygame_menu.widgets.widget.textinput import TextInputManager
from pygame_menu.widgets.widget.toggleswitch import ToggleSwitchManager
from pygame_menu.widgets.widget.vfill import VFillManager
from pygame_menu.widgets.widget.vmargin import VMarginManager


# noinspection PyProtectedMember
class WidgetManager(
    Base,
    ButtonManager,
    ColorInputManager,
    DropSelectManager,
    DropSelectMultipleManager,
    FrameManager,
    HMarginManager,
    ImageManager,
    LabelManager,
    MenuLinkManager,
    NoneWidgetManager,
    ProgressBarManager,
    RangeSliderManager,
    SelectorManager,
    SurfaceWidgetManager,
    TableManager,
    TextInputManager,
    ToggleSwitchManager,
    VFillManager,
    VMarginManager,
):
    """
    Add/Remove widgets to the Menu.

    :param menu: The Menu reference
    :param verbose: Enables/disables verbose mode (warnings/errors)
    """

    def __init__(self, menu: pygame_menu.Menu, verbose: bool = True) -> None:
        super().__init__(object_id=menu.get_id() + "+widget-manager", verbose=verbose)
        self._menu = menu

    @property
    def _theme(self) -> pygame_menu.Theme:
        return self._menu.get_theme()

    def _add_submenu(self, menu: pygame_menu.Menu, hook: Widget) -> None:
        assert isinstance(menu, pygame_menu.Menu)
        assert menu != self._menu, "submenu cannot point to menu itself"
        assert isinstance(hook, Widget)
        if menu not in self._menu._submenus.keys():
            self._menu._submenus[menu] = []
        assert hook not in self._menu._submenus[menu], (
            f"widget {hook.get_class_id()} already hooks submenu {menu.get_class_id()}"
        )
        self._menu._submenus[menu].append(hook)
        hook._menu_hook = menu

    @staticmethod
    def _normalize_inflate(value: Any) -> tuple[int, int]:
        """Normalize and validate a widget inflate value."""
        if value == 0:
            value = (0, 0)

        assert_vector(value, 2, int)
        assert value[0] >= 0 and value[1] >= 0, (
            "both inflate components must be equal or greater than zero"
        )
        return value

    def _filter_widget_attributes(
        self,
        kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Extract and validate widget attributes from ``kwargs``.

        Recognized options are removed from ``kwargs``. Any remaining
        entries are treated as unsupported options by the caller.
        """
        attributes: dict[str, Any] = {}
        theme = self._theme

        # align
        align = kwargs.pop("align", theme.widget_alignment)
        assert isinstance(align, str)
        attributes["align"] = align

        # background_color
        background_color = kwargs.pop(
            "background_color",
            theme.widget_background_color,
        )

        background_is_color = background_color is not None and not isinstance(
            background_color, pygame_menu.BaseImage
        )

        if background_is_color:
            background_color = assert_color(background_color)

        attributes["background_color"] = background_color

        # background_inflate
        background_inflate = kwargs.pop(
            "background_inflate",
            theme.widget_background_inflate,
        )
        attributes["background_inflate"] = self._normalize_inflate(background_inflate)

        # border_color
        border_color = kwargs.pop(
            "border_color",
            theme.widget_border_color,
        )
        if border_color is not None:
            border_color = assert_color(border_color)

        attributes["border_color"] = border_color

        # border_inflate
        border_inflate = kwargs.pop(
            "border_inflate",
            theme.widget_border_inflate,
        )
        attributes["border_inflate"] = self._normalize_inflate(border_inflate)

        # border_position
        border_position = kwargs.pop(
            "border_position",
            theme.widget_border_position,
        )
        assert_position_vector(border_position)
        attributes["border_position"] = border_position

        # border_width
        border_width = kwargs.pop(
            "border_width",
            theme.widget_border_width,
        )
        assert isinstance(border_width, int) and border_width >= 0
        attributes["border_width"] = border_width

        # cursor
        cursor = kwargs.pop("cursor", theme.widget_cursor)
        assert_cursor(cursor)
        attributes["cursor"] = cursor

        # floating status
        float_ = kwargs.pop("float", False)
        assert isinstance(float_, bool)
        attributes["float"] = float_

        float_origin_position = kwargs.pop(
            "float_origin_position",
            False,
        )
        assert isinstance(float_origin_position, bool)
        attributes["float_origin_position"] = float_origin_position

        # font_antialias
        attributes["font_antialias"] = theme.widget_font_antialias

        # font_background_color
        font_background_color = kwargs.pop(
            "font_background_color",
            theme.widget_font_background_color,
        )

        if (
            font_background_color is None
            and theme.widget_font_background_color_from_menu
            and not background_is_color
            and not isinstance(theme.background_color, pygame_menu.BaseImage)
        ):
            font_background_color = assert_color(theme.background_color)

        attributes["font_background_color"] = font_background_color

        # font_color
        font_color = kwargs.pop(
            "font_color",
            theme.widget_font_color,
        )
        attributes["font_color"] = assert_color(font_color)

        # font_name
        font_name = kwargs.pop(
            "font_name",
            theme.widget_font,
        )
        assert_font(font_name)
        attributes["font_name"] = font_name

        # font_shadow
        font_shadow = kwargs.pop(
            "font_shadow",
            theme.widget_font_shadow,
        )
        assert isinstance(font_shadow, bool)
        attributes["font_shadow"] = font_shadow

        # font_shadow_color
        font_shadow_color = kwargs.pop(
            "font_shadow_color",
            theme.widget_font_shadow_color,
        )
        attributes["font_shadow_color"] = assert_color(font_shadow_color)

        # font_shadow_offset
        font_shadow_offset = kwargs.pop(
            "font_shadow_offset",
            theme.widget_font_shadow_offset,
        )
        assert isinstance(font_shadow_offset, int)
        attributes["font_shadow_offset"] = font_shadow_offset

        # font_shadow_position
        font_shadow_position = kwargs.pop(
            "font_shadow_position",
            theme.widget_font_shadow_position,
        )
        assert isinstance(font_shadow_position, str)
        attributes["font_shadow_position"] = font_shadow_position

        # font_size
        font_size = kwargs.pop(
            "font_size",
            theme.widget_font_size,
        )
        assert isinstance(font_size, int)
        assert font_size > 0, "font size must be greater than zero"
        attributes["font_size"] = font_size

        # margin
        margin = kwargs.pop(
            "margin",
            theme.widget_margin,
        )
        if margin == 0:
            margin = (0, 0)

        assert_vector(margin, 2)
        attributes["margin"] = margin

        # padding
        padding = kwargs.pop(
            "padding",
            theme.widget_padding,
        )
        assert isinstance(padding, PaddingInstance)
        attributes["padding"] = padding

        # readonly_color
        readonly_color = kwargs.pop(
            "readonly_color",
            theme.readonly_color,
        )
        attributes["readonly_color"] = assert_color(readonly_color)

        # readonly_selected_color
        readonly_selected_color = kwargs.pop(
            "readonly_selected_color",
            theme.readonly_selected_color,
        )
        attributes["readonly_selected_color"] = assert_color(readonly_selected_color)

        # selection_color
        selection_color = kwargs.pop(
            "selection_color",
            theme.selection_color,
        )
        attributes["selection_color"] = assert_color(selection_color)

        # selection_effect
        selection_effect = kwargs.pop(
            "selection_effect",
            theme.widget_selection_effect,
        )

        if selection_effect is None:
            selection_effect = pygame_menu.widgets.NoneSelection()
        else:
            selection_effect = selection_effect.copy()

        assert isinstance(
            selection_effect,
            pygame_menu.widgets.core.Selection,
        )

        selection_effect.set_color(attributes["selection_color"])
        attributes["selection_effect"] = selection_effect

        # shadow
        attributes["shadow_aa"] = kwargs.pop(
            "shadow_aa",
            theme.widget_shadow_aa,
        )
        attributes["shadow_color"] = kwargs.pop(
            "shadow_color",
            theme.widget_shadow_color,
        )
        attributes["shadow_radius"] = kwargs.pop(
            "shadow_radius",
            theme.widget_shadow_radius,
        )
        attributes["shadow_type"] = kwargs.pop(
            "shadow_type",
            theme.widget_shadow_type,
        )
        attributes["shadow_width"] = kwargs.pop(
            "shadow_width",
            theme.widget_shadow_width,
        )

        # tab_size
        attributes["tab_size"] = kwargs.pop(
            "tab_size",
            theme.widget_tab_size,
        )

        return attributes

    def _configure_widget(
        self,
        widget: Widget,
        **kwargs: Any,
    ) -> None:
        assert isinstance(widget, Widget)

        menu = self._menu
        theme = self._theme

        widget._verbose = self._verbose

        # Basic layout
        widget.set_alignment(align=kwargs["align"])

        widget.set_margin(
            x=kwargs["margin"][0],
            y=kwargs["margin"][1],
        )
        widget.set_padding(padding=kwargs["padding"])

        widget.set_float(
            float_status=kwargs["float"],
            origin_position=kwargs["float_origin_position"],
        )

        # Background and border
        widget.set_background_color(
            color=kwargs["background_color"],
            inflate=kwargs["background_inflate"],
        )

        widget.set_border(
            color=kwargs["border_color"],
            inflate=kwargs["border_inflate"],
            position=kwargs["border_position"],
            width=kwargs["border_width"],
        )

        # Input controls
        widget.set_controls(
            joystick=menu._joystick,
            keyboard=menu._keyboard,
            mouse=menu._mouse,
            touchscreen=menu._touchscreen,
        )

        widget.set_cursor(cursor=kwargs["cursor"])
        widget.set_tab_size(tab_size=kwargs["tab_size"])

        # Font
        widget.set_font(
            antialias=kwargs["font_antialias"],
            background_color=kwargs["font_background_color"],
            color=kwargs["font_color"],
            font=kwargs["font_name"],
            font_size=kwargs["font_size"],
            readonly_color=kwargs["readonly_color"],
            readonly_selected_color=kwargs["readonly_selected_color"],
            selected_color=kwargs["selection_color"],
        )

        widget.set_font_shadow(
            color=kwargs["font_shadow_color"],
            enabled=kwargs["font_shadow"],
            offset=kwargs["font_shadow_offset"],
            position=kwargs["font_shadow_position"],
        )

        # Selection and shadow effects
        widget.set_selection_effect(
            selection=kwargs["selection_effect"],
        )

        widget.shadow(
            aa_amount=kwargs["shadow_aa"],
            color=kwargs["shadow_color"],
            corner_radius=kwargs["shadow_radius"],
            shadow_type=kwargs["shadow_type"],
            shadow_width=kwargs["shadow_width"],
        )

        if theme.widget_background_inflate_to_selection:
            widget.background_inflate_to_selection_effect()

        # Final widget state
        widget._update__repr___(self)
        widget._keyboard_ignore_nonphysical = menu._keyboard_ignore_nonphysical
        widget.configured = True
        widget._configure()

    @staticmethod
    def _check_kwargs(kwargs: dict[str, Any]) -> None:
        if not kwargs:
            return

        invalid_keyword = next(iter(kwargs))
        raise ValueError(
            f"widget addition optional parameter kwargs.{invalid_keyword} is not valid"
        )

    def _append_widget(self, widget: Widget) -> None:
        assert isinstance(widget, Widget)

        menu = self._menu

        # Associate the widget with this menu.
        if widget.get_menu() is None:
            widget.set_menu(menu)

        assert widget.get_menu() == menu, (
            "widget cannot have a different instance of menu"
        )

        menu._check_id_duplicated(widget.get_id())

        if widget.get_scrollarea() is None:
            widget.set_scrollarea(menu.get_scrollarea())

        # Widgets are initially unselected.
        widget.select(False)

        # Append the widget to the menu.
        menu._widgets.append(widget)

        # Select the first selectable widget.
        if menu._index < 0 and widget.is_selectable:
            widget.select()
            menu._index = len(menu._widgets) - 1

        # Force menu rendering. This checks for sizing errors and overflow.
        # If the widget is added during execution, it also refreshes the surface.
        menu._widgets_surface = None

        try:
            menu._render()
        except (
            pygame_menu.menu._MenuSizingException,
            pygame_menu.menu._MenuWidgetOverflow,
        ):
            # Restore the menu if rendering fails.
            menu.remove_widget(widget)
            raise

        menu.render()

        # Sort frame widgets because rendering may change frame positions.
        if menu._update_frames:
            menu._update_frames[0]._sort_menu_update_frames()

        # Update widget mouse state.
        check_widget_mouseleave()

        # Notify the widget that it has been appended to the menu.
        widget._append_to_menu()

    def configure_defaults_widget(self, widget: Widget) -> None:
        self._configure_widget(widget, **self._filter_widget_attributes({}))

    def generic_widget(
        self, widget: Widget, configure_defaults: bool = False
    ) -> Widget:
        """
        Add generic widget to the Menu.

        .. note::

            The widget should be fully configured by the user: font, padding, etc.

        .. note::

            This is applied only to the base Menu (not the currently displayed,
            stored in ``_current`` pointer); for such behavior apply to
            :py:meth:`pygame_menu.menu.Menu.get_current` object.

        .. warning::

            Unintended behaviors may happen while using this method, use only with
            caution; specially while creating nested submenus with buttons.

        :param widget: Widget to be added
        :param configure_defaults: Apply defaults widget configuration (for example, theme)
        :return: The added widget object
        :rtype: :py:class:`pygame_menu.widgets.Widget`
        """
        assert isinstance(widget, Widget)
        if widget.get_menu() is not None:
            raise ValueError("widget to be added is already appended to another Menu")

        # Raise warning if adding button with Menu
        if isinstance(widget, pygame_menu.widgets.Button) and widget.to_menu:
            if self._verbose:
                warn(
                    "prefer adding submenus using add_button method instead, "
                    "unintended behaviours may occur"
                )

        # Configure widget
        if configure_defaults:
            self.configure_defaults_widget(widget)
        self._append_widget(widget)

        return widget
