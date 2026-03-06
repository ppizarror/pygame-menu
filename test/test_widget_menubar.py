"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - MENUBAR
Test MenuBar widget.
"""

import pygame
import pytest

import pygame_menu
import pygame_menu.controls as ctrl
from pygame_menu.locals import (
    POSITION_EAST,
    POSITION_NORTH,
    POSITION_SOUTH,
    POSITION_SOUTHWEST,
    POSITION_WEST,
)
from pygame_menu.widgets import (
    MENUBAR_STYLE_ADAPTIVE,
    MENUBAR_STYLE_NONE,
    MENUBAR_STYLE_SIMPLE,
    MENUBAR_STYLE_TITLE_ONLY,
    MENUBAR_STYLE_TITLE_ONLY_DIAGONAL,
    MENUBAR_STYLE_UNDERLINE,
    MENUBAR_STYLE_UNDERLINE_TITLE,
    MenuBar,
)
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from test._utils import MenuUtils, PygameEventUtils, surface


@pytest.fixture
def menu():
    return MenuUtils.generic_menu()


@pytest.mark.parametrize(
    "mode",
    [
        MENUBAR_STYLE_ADAPTIVE,
        MENUBAR_STYLE_NONE,
        MENUBAR_STYLE_SIMPLE,
        MENUBAR_STYLE_UNDERLINE,
        MENUBAR_STYLE_UNDERLINE_TITLE,
        MENUBAR_STYLE_TITLE_ONLY,
        MENUBAR_STYLE_TITLE_ONLY_DIAGONAL,
    ],
)
def test_menubar_modes(menu, mode):
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True, mode=mode)
    menu.add.generic_widget(mb)
    menu.draw(surface)


def test_menubar_backbox_border_width(menu):
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)
    mb.set_backbox_border_width(2)

    with pytest.raises(AssertionError):
        mb.set_backbox_border_width(1.5)
    with pytest.raises(AssertionError):
        mb.set_backbox_border_width(0)
    with pytest.raises(AssertionError):
        mb.set_backbox_border_width(-1)

    assert mb._backbox_border_width == 2


def test_menubar_unknown_mode(menu):
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True, mode="unknown")
    with pytest.raises(ValueError):
        mb.set_menu(menu)


def test_menubar_scrollbar_displacements(menu):
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True, mode=MENUBAR_STYLE_ADAPTIVE)

    assert mb.get_scrollbar_style_change(POSITION_SOUTH) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_WEST) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_NORTH) == (0, (0, 0))

    mb.set_menu(menu)
    mb._render()

    assert mb.get_scrollbar_style_change(POSITION_SOUTHWEST) == (0, (0, 0))


def test_menubar_displacements_with_title_only():
    theme = pygame_menu.themes.THEME_DEFAULT.copy()
    theme.title_bar_style = MENUBAR_STYLE_TITLE_ONLY

    menu = MenuUtils.generic_menu(theme=theme, title="my title")
    mb = menu.get_menubar()

    assert mb.get_scrollbar_style_change(POSITION_SOUTH) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_WEST) == (-55, (0, 55))
    assert mb.get_scrollbar_style_change(POSITION_NORTH) == (0, (0, 55))


def test_menubar_displacements_with_close_button():
    theme = pygame_menu.themes.THEME_DEFAULT.copy()
    theme.title_bar_style = MENUBAR_STYLE_TITLE_ONLY
    theme.widget_border_inflate = (0, 0)

    menu = MenuUtils.generic_menu(
        theme=theme,
        title="my title",
        onclose=pygame_menu.events.CLOSE,
        touchscreen=True,
    )

    mb = menu.get_menubar()

    assert mb.get_scrollbar_style_change(POSITION_SOUTH) == (0, (0, 0))
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (-33, (0, 33))
    assert mb.get_scrollbar_style_change(POSITION_WEST) == (-55, (0, 55))
    assert mb.get_scrollbar_style_change(POSITION_NORTH) == (0, (0, 55))

    mb.hide()
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))

    mb.show()
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (-33, (0, 33))

    mb.set_float(True)
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))

    mb.set_float(False)
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (-33, (0, 33))

    mb.fixed = False
    assert mb.get_scrollbar_style_change(POSITION_EAST) == (0, (0, 0))


def test_menubar_events(menu):
    theme = pygame_menu.themes.THEME_DEFAULT.copy()
    theme.title_bar_style = MENUBAR_STYLE_TITLE_ONLY
    menu = MenuUtils.generic_menu(theme=theme, title="my title")
    menu.enable()
    mb = menu.get_menubar()

    assert not mb.update(PygameEventUtils.middle_rect_click(mb._rect))

    assert not mb.update(PygameEventUtils.middle_rect_click(mb._backbox_rect))

    assert not mb.update(
        PygameEventUtils.middle_rect_click(
            mb._backbox_rect, evtype=pygame.FINGERUP, menu=menu
        )
    )

    assert not mb.update(
        PygameEventUtils.middle_rect_click(
            mb._backbox_rect, evtype=pygame.MOUSEBUTTONDOWN
        )
    )

    assert mb.update(PygameEventUtils.joy_button(ctrl.JOY_BUTTON_BACK))

    mb.readonly = True
    assert not mb.update(PygameEventUtils.joy_button(ctrl.JOY_BUTTON_BACK))
    mb.readonly = False


@pytest.mark.parametrize(
    "method,args",
    [
        ("rotate", (10,)),
        ("resize", (10, 10)),
        ("scale", (100, 100)),
        ("flip", (True, True)),
        ("set_max_width", (100,)),
        ("set_max_height", (100,)),
    ],
)
def test_menubar_invalid_transforms(method, args):
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)

    with pytest.raises(WidgetTransformationNotImplemented):
        getattr(mb, method)(*args)


def test_menubar_transform_state():
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.rotate(10)
    assert mb._angle == 0

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.resize(10, 10)
    assert mb._scale[:3] == [False, 1, 1]

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.scale(100, 100)
    assert mb._scale[:3] == [False, 1, 1]

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.flip(True, True)
    assert mb._flip == (False, False)

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.set_max_width(100)
    assert mb._max_width[0] is None

    with pytest.raises(WidgetTransformationNotImplemented):
        mb.set_max_height(100)
    assert mb._max_height[0] is None


def test_menubar_empty_title():
    mb = MenuBar("", 500, (0, 0, 0), back_box=True)
    p = mb._padding

    assert mb.get_width() == p[1] + p[3]
    assert mb.get_height() == p[0] + p[2]


def test_menubar_value_api():
    mb = MenuBar("Menu", 500, (0, 0, 0), back_box=True)

    with pytest.raises(ValueError):
        mb.get_value()

    with pytest.raises(ValueError):
        mb.set_value("value")

    assert not mb.value_changed()
    mb.reset_value()
