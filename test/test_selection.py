"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET SELECTION.
Test widget selection effects.
"""

import copy

import pytest

from pygame_menu.widgets import Button
from pygame_menu.widgets.core.selection import Selection
from pygame_menu.widgets.selection import (
    HighlightSelection,
    LeftArrowSelection,
    NoneSelection,
    RightArrowSelection,
    SimpleSelection,
)
from pygame_menu.widgets.selection.arrow_selection import ArrowSelection
from test._utils import MenuUtils, surface


@pytest.fixture
def menu():
    m = MenuUtils.generic_menu()
    m.enable()
    return m


def test_copy():
    s = LeftArrowSelection()
    s1 = copy.copy(s)
    s2 = copy.deepcopy(s)
    s3 = s.copy()

    assert s != s1
    assert s != s2
    assert s != s3


def test_abstract_selection_draw_raises():
    w = Button("epic")

    sel = Selection(0, 0, 0, 0)
    with pytest.raises(NotImplementedError):
        sel.draw(surface, w)

    arrow = ArrowSelection(0, 0, 0, 0)
    with pytest.raises(NotImplementedError):
        arrow.draw(surface, w)


def test_arrow_selection(menu):
    w = Button("epic")
    w.set_selection_effect(LeftArrowSelection())
    menu.add.generic_widget(w)
    menu.draw(surface)

    w.set_selection_effect(RightArrowSelection())
    menu.draw(surface)

    arrow = ArrowSelection(0, 0, 0, 0)
    with pytest.raises(NotImplementedError):
        arrow.draw(surface, w)


def test_highlight_selection(menu):
    w = Button("epic")
    border_width = 1
    margin_x = 18
    margin_y = 10

    w.set_selection_effect(
        HighlightSelection(
            border_width=border_width,
            margin_x=margin_x,
            margin_y=margin_y,
        )
    )
    menu.add.generic_widget(w)
    menu.draw(surface)

    sel: HighlightSelection = w.get_selection_effect()  # type: ignore

    assert sel.get_height() == margin_y
    assert sel.get_width() == margin_x

    rect = w.get_rect()
    inflated = sel.inflate(rect)

    assert -inflated.x + rect.x == sel.get_width() / 2
    assert -inflated.y + rect.y == sel.get_height() / 2

    sel.margin_xy(10, 20)
    assert sel.margin_left == 10
    assert sel.margin_right == 10
    assert sel.margin_top == 20
    assert sel.margin_bottom == 20

    sel._border_width = 0
    sel.draw(surface, w)

    sel.set_background_color("red")
    assert sel.get_background_color() == (255, 0, 0, 255)


def test_none_selection(menu):
    w = Button("epic")
    w.set_selection_effect(NoneSelection())
    menu.add.generic_widget(w)
    menu.draw(surface)

    rect = w.get_rect()
    new_rect = w.get_selection_effect().inflate(rect)
    assert rect == new_rect
    assert not w.get_selection_effect().widget_apply_font_color

    last_sel = w.get_selection_effect()
    w.set_selection_effect()
    assert isinstance(w.get_selection_effect(), NoneSelection)
    assert w.get_selection_effect() != last_sel


def test_simple_selection(menu):
    w = Button("epic")
    w.set_selection_effect(SimpleSelection())
    menu.add.generic_widget(w)
    menu.draw(surface)

    rect = w.get_rect()
    new_rect = w.get_selection_effect().inflate(rect)
    assert rect == new_rect
    assert w.get_selection_effect().widget_apply_font_color
