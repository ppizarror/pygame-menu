"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - SCROLLBAR
Test ScrollBar widget.
"""

import pygame
import pytest

from pygame_menu.locals import (
    ORIENTATION_HORIZONTAL,
    ORIENTATION_VERTICAL,
    POSITION_SOUTHEAST,
)
from pygame_menu.widgets import ScrollBar
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented
from test._utils import WINDOW_SIZE, MenuUtils, PygameEventUtils, surface


@pytest.fixture
def world_surface():
    world = pygame.Surface((WINDOW_SIZE[0] * 2, WINDOW_SIZE[1] * 3))
    world.fill((200, 200, 200))
    for x in range(100, world.get_width(), 200):
        for y in range(100, world.get_height(), 200):
            pygame.draw.circle(world, (225, 34, 43), (x, y), 100, 10)
    return world


@pytest.fixture
def default_scrollbar():
    return ScrollBar(100, (0, 100), "sb", ORIENTATION_VERTICAL)


def test_scrollbar_full_interaction(world_surface):
    screen_size = surface.get_size()
    thick = 80
    length = screen_size[1]
    world_range = (50, world_surface.get_height())
    x, y = screen_size[0] - thick, 0

    sb = ScrollBar(
        length,
        world_range,
        "sb2",
        ORIENTATION_VERTICAL,
        slider_pad=2,
        slider_color=(210, 120, 200),
        page_ctrl_thick=thick,
        page_ctrl_color=(235, 235, 230),
    )

    assert sb.get_thickness() == 80
    assert sb.get_scrollarea() is None

    sb.set_shadow(color=(245, 245, 245), position=POSITION_SOUTHEAST)
    assert not sb._font_shadow

    sb.set_position(x, y)

    assert sb._orientation == 1
    assert sb.get_orientation() == ORIENTATION_VERTICAL
    assert sb.get_minimum() == world_range[0]
    assert sb.get_maximum() == world_range[1]

    sb.set_value(80)
    assert pytest.approx(sb.get_value(), abs=2) == 80

    sb.update(
        PygameEventUtils.mouse_click(
            x + thick / 2, y + 2, evtype=pygame.MOUSEBUTTONDOWN
        )
    )
    assert sb.get_value() == 50
    assert sb.get_value_percentage() == 0

    sb.set_page_step(length)
    assert pytest.approx(sb.get_page_step(), abs=2) == length

    sb.draw(surface)

    # PageDown / PageUp
    sb.update(PygameEventUtils.key(pygame.K_PAGEDOWN, keydown=True))
    assert sb.get_value() == 964
    sb.update(PygameEventUtils.key(pygame.K_PAGEUP, keydown=True))
    assert sb.get_value() == 50

    assert sb._last_mouse_pos == (-1, -1)
    sb.update(PygameEventUtils.enter_window())
    assert sb._last_mouse_pos == (-1, -1)
    sb.update(PygameEventUtils.leave_window())
    assert sb._last_mouse_pos == pygame.mouse.get_pos()

    assert not sb.scrolling
    sb.update(
        PygameEventUtils.middle_rect_click(
            sb.get_slider_rect(), evtype=pygame.MOUSEBUTTONDOWN
        )
    )
    assert sb.scrolling
    sb.update(PygameEventUtils.mouse_click(1, 1))
    assert not sb.scrolling
    assert sb.get_value() == 50

    sb.update(
        PygameEventUtils.middle_rect_click(
            sb.get_rect(to_absolute_position=True), evtype=pygame.MOUSEBUTTONDOWN
        )
    )
    assert sb.get_value() == 964

    sb.update(
        PygameEventUtils.middle_rect_click(
            sb.get_slider_rect(), evtype=pygame.MOUSEBUTTONDOWN
        )
    )
    assert sb.scrolling

    sb.update(
        PygameEventUtils.middle_rect_click(
            sb.get_slider_rect(), button=4, evtype=pygame.MOUSEBUTTONDOWN
        )
    )
    assert sb.get_value() == 875

    sb.update(
        PygameEventUtils.middle_rect_click(
            sb.get_slider_rect(), button=5, evtype=pygame.MOUSEBUTTONDOWN
        )
    )
    assert sb.get_value() == 964
    assert sb.get_value_percentage() == 0.522

    # Mouse motion while scrolling
    sb.update(
        PygameEventUtils.middle_rect_click(
            sb.get_slider_rect(),
            button=5,
            delta=(0, 50),
            rel=(0, 10),
            evtype=pygame.MOUSEMOTION,
        )
    )
    assert sb.get_value_percentage() == 0.547

    sb.update(
        PygameEventUtils.middle_rect_click(
            sb.get_slider_rect(),
            button=5,
            delta=(0, 50),
            rel=(0, -10),
            evtype=pygame.MOUSEMOTION,
        )
    )
    assert sb.get_value_percentage() == 0.522

    sb.update(
        PygameEventUtils.middle_rect_click(
            sb.get_slider_rect(),
            button=5,
            delta=(0, 50),
            rel=(0, 999),
            evtype=pygame.MOUSEMOTION,
        )
    )
    assert sb.get_value_percentage() == 1

    sb.readonly = True
    assert not sb.update([])

    # Ignore events outside region
    sb.update(
        PygameEventUtils.middle_rect_click(
            sb.get_slider_rect(),
            button=5,
            delta=(0, 999),
            rel=(0, -10),
            evtype=pygame.MOUSEMOTION,
        )
    )
    assert sb.get_value_percentage() in (0.976, 1)

    # onreturn removal
    sb = ScrollBar(length, world_range, "sb", ORIENTATION_VERTICAL, onreturn=-1)
    assert sb._onreturn is None
    assert sb._kwargs.get("onreturn", 0)

    # Scaling not supported
    with pytest.raises(WidgetTransformationNotImplemented):
        sb.scale(2, 2)
    assert not sb._scale[0]

    with pytest.raises(WidgetTransformationNotImplemented):
        sb.resize(2, 2)
    assert not sb._scale[0]

    with pytest.raises(WidgetTransformationNotImplemented):
        sb.set_max_width(10)
    assert sb._max_width[0] is None

    with pytest.raises(WidgetTransformationNotImplemented):
        sb.set_max_height(10)
    assert sb._max_height[0] is None

    sb._apply_font()
    sb.set_padding(10)
    assert sb._padding[0] == 0

    with pytest.raises(WidgetTransformationNotImplemented):
        sb.rotate(10)
    assert sb._angle == 0

    with pytest.raises(WidgetTransformationNotImplemented):
        sb.flip(True, True)
    assert not sb._flip[0]
    assert not sb._flip[1]

    sb.set_minimum(0.5 * sb._values_range[1])

    sb._mouseover = True
    sb.hide()


def test_value_behavior():
    menu = MenuUtils.generic_menu()
    sb = menu.get_scrollarea()._scrollbars[0]

    assert sb._default_value == 0
    assert sb.get_value() == 0
    assert not sb.value_changed()

    sb.set_value(1)
    assert sb.get_value() == 1
    assert sb.value_changed()

    sb.reset_value()
    assert sb.get_value() == 0
    assert not sb.value_changed()

    assert sb.is_at_top()
    assert not sb.is_at_bottom()

    sb.set_value(sb.get_maximum())
    assert not sb.is_at_top()
    assert sb.is_at_bottom()

    sb.set_value(0)
    assert sb.is_at_top()
    assert not sb.is_at_bottom()

    sb.set_value(sb.get_maximum())
    sb.bump_to_top()
    assert sb.get_value() == 0

    sb.bump_to_bottom()
    assert sb.get_value() == sb.get_maximum()


def test_set_length(default_scrollbar):
    default_scrollbar.set_length(200)
    assert default_scrollbar._page_ctrl_length == 200


def test_set_page_step(default_scrollbar):
    default_scrollbar.set_page_step(20)
    assert default_scrollbar._page_step == 20


@pytest.mark.parametrize("value", [-10, 110])
def test_set_value_out_of_range(default_scrollbar, value):
    with pytest.raises(AssertionError):
        default_scrollbar.set_value(value)


def test_value_percentage(default_scrollbar):
    default_scrollbar.set_value(50)
    assert pytest.approx(default_scrollbar.get_value_percentage(), abs=0.01) == 0.5


def test_at_top_bottom(default_scrollbar):
    assert default_scrollbar.is_at_top()
    assert not default_scrollbar.is_at_bottom()

    default_scrollbar.set_value(100)
    assert not default_scrollbar.is_at_top()
    assert default_scrollbar.is_at_bottom()


def test_bump_to_top_bottom(default_scrollbar):
    default_scrollbar.set_value(50)
    default_scrollbar.bump_to_top()
    assert default_scrollbar.get_value() == 0

    default_scrollbar.bump_to_bottom()
    assert default_scrollbar.get_value() == 100


def test_scroll_to_widget(default_scrollbar):
    assert default_scrollbar.scroll_to_widget() is default_scrollbar


def test_set_orientation(default_scrollbar):
    default_scrollbar.set_orientation(ORIENTATION_HORIZONTAL)
    assert default_scrollbar.get_orientation() == ORIENTATION_HORIZONTAL


def test_set_maximum_minimum(default_scrollbar):
    default_scrollbar.set_maximum(200)
    assert default_scrollbar.get_maximum() == 200

    default_scrollbar.set_minimum(50)
    assert default_scrollbar.get_minimum() == 50


@pytest.mark.parametrize("length", [0])
def test_set_length_zero(default_scrollbar, length):
    with pytest.raises(AssertionError):
        default_scrollbar.set_length(length)


@pytest.mark.parametrize("step", [0])
def test_set_page_step_zero(default_scrollbar, step):
    with pytest.raises(AssertionError):
        default_scrollbar.set_page_step(step)


def test_minimum_greater_than_maximum(default_scrollbar):
    with pytest.raises(AssertionError):
        default_scrollbar.set_minimum(100)


def test_maximum_less_than_minimum(default_scrollbar):
    with pytest.raises(AssertionError):
        default_scrollbar.set_maximum(0)


def test_percentage_zero(default_scrollbar):
    assert pytest.approx(default_scrollbar.get_value_percentage(), abs=0.01) == 0


def test_percentage_one(default_scrollbar):
    default_scrollbar.set_value(100)
    assert pytest.approx(default_scrollbar.get_value_percentage(), abs=0.01) == 1


def test_scroll_to_widget_invalid(default_scrollbar):
    assert default_scrollbar.scroll_to_widget("invalid") is default_scrollbar


def test_invalid_orientation(default_scrollbar):
    with pytest.raises(AssertionError):
        default_scrollbar.set_orientation("invalid")


@pytest.mark.parametrize(
    "setter", ["_page_ctrl_color", "_slider_color", "_slider_hover_color"]
)
def test_invalid_color_setters(default_scrollbar, setter):
    with pytest.raises(TypeError):
        getattr(default_scrollbar, setter)("invalid_color")


def test_invalid_slider_rect_call(default_scrollbar):
    with pytest.raises(AttributeError):
        default_scrollbar.get_slider_rect().invalid_method()


def test_update_invalid_event(default_scrollbar):
    with pytest.raises(AttributeError):
        default_scrollbar.update("invalid_event")


def test_draw_invalid_surface(default_scrollbar):
    with pytest.raises(AttributeError):
        default_scrollbar.draw("invalid_surface")
