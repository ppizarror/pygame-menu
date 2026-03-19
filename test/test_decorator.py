"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST DECORATOR
Decorator API.
"""

import copy
import timeit

import pygame
import pytest

from pygame_menu.baseimage import IMAGE_EXAMPLE_PYGAME_MENU, BaseImage
from pygame_menu.font import FONT_8BIT
from pygame_menu.widgets.widget.button import Button
from pygame_menu.widgets.widget.none import NoneWidget
from test._utils import TEST_THEME, MenuUtils, surface

TEST_TIME_DRAW = False


@pytest.mark.skipif(not TEST_TIME_DRAW, reason="Timing test disabled")
def test_time_draw():
    """This test the time that takes to draw the decorator surface with several decorations."""
    widg = NoneWidget()
    deco = widg.get_decorator()
    deco.cache = True

    for _ in range(10000):
        deco.add_pixel(1, 2, (0, 0, 0))

    total_tests = 10
    total = 0
    for i in range(total_tests):
        t = timeit.timeit(lambda: widg.draw(surface), number=1000)
        total += t
    avg = round(total / total_tests, 3)
    print("Average:", avg)


def test_cache():
    """Test cache."""
    widg = NoneWidget()
    deco = widg.get_decorator()
    deco.cache = True

    # Prev
    assert deco._cache_surface["prev"] is None
    assert deco._cache_surface["post"] is None

    f = deco.add_circle(1, 1, 1, (0, 0, 0), True)
    assert deco._cache_surface["prev"] is None
    assert deco._cache_surface["post"] is None

    deco.draw_prev(surface)
    assert deco._cache_surface["prev"] is not None
    assert deco._cache_surface["post"] is None

    prev = deco._cache_surface["prev"]
    deco.add_circle(1, 1, 1, (0, 0, 0), True)
    deco.draw_prev(surface)
    assert deco._cache_surface["prev"] != prev
    assert not deco._cache_needs_update["prev"]
    assert not deco._cache_needs_update["post"]

    deco.add_circle(1, 1, 1, (0, 0, 0), True)
    assert deco._cache_needs_update["prev"]
    deco.draw_prev(surface)
    assert not deco._cache_needs_update["prev"]
    assert deco._total_decor() == 3

    deco.disable(f)
    assert deco._cache_needs_update["prev"]

    deco.remove_all()
    assert deco._total_decor() == 0
    assert not deco._cache_needs_update["prev"]
    deco.draw_prev(surface)

    # Post
    deco.add_circle(1, 1, 1, (0, 0, 0), False, prev=False)
    assert deco._cache_needs_update["post"]
    assert deco._cache_surface["post"] is None

    deco.draw_post(surface)
    assert deco._total_decor() == 1
    assert not deco._cache_needs_update["post"]
    assert deco._cache_surface["post"] is not None

    deco.remove_all()
    assert deco._total_decor() == 0


def test_copy():
    """Test decorator copy."""
    widg = NoneWidget()
    deco = widg.get_decorator()

    with pytest.raises(Exception):
        copy.copy(deco)
    with pytest.raises(Exception):
        copy.deepcopy(deco)


def test_add_remove():
    """Test add remove."""
    widg = NoneWidget()
    deco = widg.get_decorator()

    d = deco._add_none()
    assert len(deco._decor["prev"]) == 1
    assert len(deco._decor["post"]) == 0
    assert len(deco._decor_prev_id) == 1
    assert d in deco._decor_prev_id
    assert deco._total_decor() == 1
    assert isinstance(d, str)

    with pytest.raises(IndexError):
        deco.remove("none")

    deco.remove(d)
    assert len(deco._decor["prev"]) == 0
    assert len(deco._decor_prev_id) == 0

    p = deco.add_pixel(1, 1, (1, 1, 1))
    assert len(deco._coord_cache) == 0
    deco.draw_prev(surface)
    assert len(deco._coord_cache) == 1
    deco.remove(p)
    assert len(deco._coord_cache) == 0


def test_enable_disable():
    """Test enable disable decoration."""
    menu = MenuUtils.generic_menu()
    btn = menu.add.button("Button")
    deco = btn.get_decorator()

    test = [False]

    def fun(surf, obj):
        test[0] = True
        assert isinstance(surf, pygame.Surface)
        assert isinstance(obj, Button)

    call_id = deco.add_callable(fun)
    assert not test[0]
    btn.draw(surface)
    assert test[0]

    with pytest.raises(IndexError):
        deco.is_enabled("unknown")

    assert deco.is_enabled(call_id)

    # Now disable the decoration
    deco.disable(call_id)
    assert not deco.is_enabled(call_id)
    test[0] = False
    btn.draw(surface)
    assert not test[0]

    deco.enable(call_id)
    btn.draw(surface)
    assert test[0]

    deco.remove(call_id)
    assert call_id not in deco._decor_enabled

    # Disable unknown decorations
    with pytest.raises(IndexError):
        deco.disable("unknown")
    with pytest.raises(IndexError):
        deco.enable("unknown")


def test_general():
    """Test all decorators."""
    theme = TEST_THEME.copy()
    theme.widget_selection_effect = None

    menu = MenuUtils.generic_menu(theme=theme)
    btn = menu.add.button("Button")
    deco = btn.get_decorator()

    poly = [(50, 50), (50, 100), (100, 50)]
    color = (1, 1, 1)

    # Polygon
    with pytest.raises(AssertionError):
        deco.add_polygon([(1, 1)], color, True)
    with pytest.raises(AssertionError):
        deco.add_polygon([(1, 1)], color, True, 1)
    with pytest.raises(AssertionError):
        deco.add_polygon([(1, 1)], color, True, gfx=False)
    deco.add_polygon(poly, color, True)
    deco.add_polygon(poly, color, False)
    deco.add_polygon(poly, color, False, gfx=False)
    deco.draw_prev(surface)

    # Circle
    with pytest.raises(AssertionError):
        deco.add_circle(1, 1, 0, color, True)
    with pytest.raises(AssertionError):
        deco.add_circle(1, 1, 0, color, True, gfx=False)
    with pytest.raises(AssertionError):
        deco.add_circle(50, 50, 100, color, True, 1)
    deco.add_circle(1, 1, 100, color, False, 5)
    deco.add_circle(50, 50, 100, color, True)

    # Surface
    img = BaseImage(IMAGE_EXAMPLE_PYGAME_MENU)
    img.scale(0.15, 0.15)
    deco.add_surface(60, 60, img.get_surface(), prev=False)

    # BaseImage
    img_dec = deco.add_baseimage(0, 0, img)
    assert len(deco._coord_cache) == 3
    menu.draw(surface)
    assert len(deco._coord_cache) == 7
    assert deco._coord_cache[img_dec] == (299, 173, ((299, 173),))

    # If widget changes in size, coord cache should change too
    btn.translate(1, 0)
    menu.draw(surface)
    assert deco._coord_cache[img_dec] == (300, 173, ((300, 173),))

    # As some problems occur here, test the position of the widget before padding
    w, h = btn.get_width(), btn.get_height()
    x, y = btn.get_position()
    assert menu.get_width(widget=True) == w
    assert menu.get_height(widget=True) == h

    wo = (menu.get_height(inner=True) - h) / 2
    assert menu._widget_offset[1] == int(wo)
    assert btn.get_rect().center == (int(x + w / 2), int(y + h / 2))

    # If widget changes padding, the center does not change if pad is equal, so the coord cache must be the same
    btn.set_padding(100)
    menu.draw(surface)

    # Test sizing
    assert menu.get_width(widget=True) == w + 200
    assert menu.get_height(widget=True) == h + 200
    wo = (menu.get_height(inner=True) - (h + 200)) / 2
    assert menu._widget_offset[1] == int(wo)
    assert btn.get_rect().x == x - 100
    assert btn.get_rect().y == y - 100
    assert btn.get_rect().center == (int(x + w / 2), int(y + h / 2))

    assert deco._coord_cache[img_dec] == (300, 173, ((300, 173),))

    # Padding left is 0, then widget center changes
    btn.set_padding((100, 100, 100, 0))
    menu.draw(surface)
    assert deco._coord_cache[img_dec] == (300, 173, ((300, 173),))

    btn.set_padding((100, 0, 100, 0))
    menu.draw(surface)
    assert deco._coord_cache[img_dec] == (300, 173, ((300, 173),))

    # Text
    with pytest.raises(ValueError):
        deco.add_text(100, 200, "nice", FONT_8BIT, 0, color)
    deco.add_text(-150, 0, "nice", FONT_8BIT, 20, color, centered=True)
    menu.draw(surface)

    # Ellipse
    with pytest.raises(AssertionError):
        deco.add_ellipse(0, 0, 0, 0, color, True)
    deco.add_ellipse(-250, 0, 110, 150, (255, 0, 0), True)
    deco.add_ellipse(-250, 0, 110, 150, (255, 0, 0), False)

    # Callable
    test = [False]

    def fun(_, __):
        test[0] = True

    deco.add_callable(fun)
    assert not test[0]
    btn.draw(surface)
    assert test[0]

    test[0] = False

    def fun_noargs():
        test[0] = True

    deco.add_callable(fun_noargs, pass_args=False)
    btn.draw(surface)
    assert test[0]

    # Textured polygon
    deco.add_textured_polygon(((10, 10), (100, 100), (120, 10)), img)

    # Arc
    deco.add_arc(0, 0, 50, 0, 100, (0, 255, 0), True)
    deco.add_arc(0, 0, 50, 0, 100, (0, 255, 0), False)

    # Pie
    deco.add_pie(0, 0, 50, 0, 100, (0, 255, 0))

    # Bezier
    deco.add_bezier(((100, 100), (0, 0), (0, -100)), (70, 10, 100), 10)

    # Rect
    deco.add_rect(200, 30, pygame.Rect(0, 0, 100, 300), (0, 0, 100))
    deco.add_rect(0, 30, pygame.Rect(0, 0, 100, 300), (100, 0, 100), width=10)

    # Pixel
    for i in range(5):
        for j in range(5):
            deco.add_pixel(10 * i, 10 * j, color)

    # Line
    deco.add_line((10, 10), (100, 100), (45, 180, 34), 10)
    deco.add_hline(1, 2, 3, color)
    deco.add_vline(1, 2, 3, color)

    # Fill
    deco.add_fill((0, 0, 0))

    menu.draw(surface)
    deco.remove_all()
