"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - PROGRESSBAR
Test ProgressBar widget.
"""

import pytest

import pygame_menu
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from test._utils import PYGAME_V2, MenuUtils, surface


@pytest.fixture
def menu():
    return MenuUtils.generic_menu()


def test_progressbar_basic(menu):
    pb = pygame_menu.widgets.ProgressBar(
        "progress", progress_text_font=pygame_menu.font.FONT_BEBAS
    )

    menu.add.generic_widget(pb, configure_defaults=True)
    menu.draw(surface)

    with pytest.raises(AssertionError):
        pygame_menu.widgets.ProgressBar("progress", default=-1)

    assert pb.get_size() == (312, 49)
    assert pb._width == 150


@pytest.mark.parametrize(
    "method",
    [
        "rotate",
        "flip",
        "scale",
        "resize",
        "set_max_width",
        "set_max_height",
    ],
)
def test_progressbar_invalid_transforms(menu, method):
    pb = pygame_menu.widgets.ProgressBar("progress")
    with pytest.raises(WidgetTransformationNotImplemented):
        getattr(pb, method)()


def test_progressbar_update(menu):
    pb = pygame_menu.widgets.ProgressBar("progress")
    menu.add.generic_widget(pb, configure_defaults=True)
    assert not pb.update([])


def test_progressbar_value(menu):
    pb = menu.add.progress_bar(
        "progress", default=50, progress_text_align=pygame_menu.locals.ALIGN_LEFT
    )

    with pytest.raises(AssertionError):
        pb.set_value(-1)

    with pytest.raises(AssertionError):
        pb.set_value("a")  # type: ignore

    assert pb.get_value() == 50
    assert not pb.value_changed()

    pb.set_value(75)
    assert pb.get_value() == 75
    assert pb.value_changed()

    pb.reset_value()
    assert pb.get_value() == 50
    assert not pb.value_changed()


def test_progressbar_empty_title(menu):
    pb = menu.add.progress_bar(
        "",
        box_margin=(0, 0),
        padding=0,
        progress_text_align=pygame_menu.locals.ALIGN_RIGHT,
    )

    expected_height = 41 if PYGAME_V2 else 42
    assert pb.get_size() == (150, expected_height)
    assert not pb.is_selected()
