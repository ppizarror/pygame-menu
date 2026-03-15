"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST EXAMPLES
Test example files.
"""

import pygame
import pytest

import pygame_menu.examples.game_selector as game_selector
import pygame_menu.examples.multi_input as multi_input
import pygame_menu.examples.other.calculator as calculator
import pygame_menu.examples.other.dynamic_button_append as dynamic_button
import pygame_menu.examples.other.dynamic_widget_update as dynamic_widget
import pygame_menu.examples.other.image_background as image_background
import pygame_menu.examples.other.maze as maze
import pygame_menu.examples.other.scrollbar as scrollbar
import pygame_menu.examples.other.scrollbar_area as scrollbar_area
import pygame_menu.examples.other.ui_solar_system as ui_solarsystem
import pygame_menu.examples.other.widget_positioning as widget_positioning
import pygame_menu.examples.scroll_menu as scroll_menu
import pygame_menu.examples.simple as simple
import pygame_menu.examples.timer_clock as timer_clock
import pygame_menu.examples.window_resize as window_resize
from test._utils import MenuUtils, PygameEventUtils


def test_example_game_selector():
    game_selector.main(test=True)
    font = MenuUtils.load_font(MenuUtils.random_font(), 5)

    game_selector.play_function(["EASY"], font, test=True)
    pygame.event.post(PygameEventUtils.keydown(pygame.K_ESCAPE, inlist=False))

    game_selector.play_function(["MEDIUM"], font, test=True)
    pygame.event.post(PygameEventUtils.keydown(pygame.K_ESCAPE, inlist=False))

    game_selector.play_function(["HARD"], font, test=True)

    with pytest.raises(ValueError):
        game_selector.play_function(["U"], font, test=True)

    game_selector.change_difficulty(("HARD", 1), "HARD")


def test_example_multi_input():
    multi_input.main(test=True)
    multi_input.check_name_test("name")
    multi_input.update_menu_sound(("sound", None), True)
    multi_input.update_menu_sound(("sound", None), False)

    settings = multi_input.main_menu.get_submenus()[0]
    settings.get_widget("store").apply()

    rslider = settings.get_widget("range_slider")
    assert rslider._onchange is not None
    assert rslider.get_value() == 50

    rslider.set_value(69)
    rslider.change()
    assert settings.get_widget("progress").get_value() == 69

    more_settings = multi_input.main_menu.get_submenus()[1]
    hex_color_widget = more_settings.get_widget("hex_color")
    hex_color_widget.apply()


def test_example_scroll_menu():
    scroll_menu.main(test=True)
    scroll_menu.on_button_click("pygame-menu", "epic")
    scroll_menu.on_button_click("pygame-menu")


def test_example_simple():
    sel = simple.menu.get_widgets()[1]
    sel.change(sel.get_value())

    btn = simple.menu.get_widgets()[2]
    btn.apply()


def test_example_resizable_window():
    window_resize.on_resize()
    assert window_resize.menu.get_window_size() == (600, 600)
    assert window_resize.menu.get_size() == (450, 420)


def test_example_timer_clock():
    pygame.event.post(PygameEventUtils.keydown(pygame.K_ESCAPE, inlist=False))
    timer_clock.main(test=True)

    timer_clock.mainmenu_background()
    timer_clock.reset_timer()
    timer_clock.TestCallClassMethod.update_game_settings()

    color = (-1, -1, -1)
    timer_clock.change_color_bg((color, "random"), color, write_on_console=True)


def test_example_other_calculator():
    app = calculator.main(test=True)

    app.process_events(
        PygameEventUtils.keydown(
            [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_PLUS]
        )
    )
    assert app.prev == "12345"
    assert app.op == "+"
    app.process_events(
        PygameEventUtils.keydown(
            [pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]
        )
    )
    assert app.curr == "67890"

    app.process_events(PygameEventUtils.keydown(pygame.K_EQUALS))
    assert app.op == ""
    assert app.curr == "80235"
    assert app.prev == ""

    app.process_events(PygameEventUtils.keydown([pygame.K_x, pygame.K_2]))
    assert app.op == "x"
    assert app.curr == "2"
    assert app.prev == "80235"

    app.process_events(PygameEventUtils.keydown([pygame.K_x]))
    assert app.op == "x"
    assert app.curr == ""
    assert app.prev == "160470"

    app.process_events(
        PygameEventUtils.keydown([pygame.K_PLUS, pygame.K_3, pygame.K_0])
    )
    assert app.op == "+"
    assert app.curr == "30"
    assert app.prev == "160470"

    app.process_events(PygameEventUtils.keydown(pygame.K_EQUALS))
    assert app.op == ""
    assert app.curr == "160500"
    assert app.prev == ""

    app.process_events(
        PygameEventUtils.keydown([pygame.K_SLASH, pygame.K_5, pygame.K_MINUS])
    )
    assert app.op == "-"
    assert app.curr == ""
    assert app.prev == "32100"

    app.process_events(
        PygameEventUtils.keydown(
            [pygame.K_3, pygame.K_2, pygame.K_1, pygame.K_0, pygame.K_EQUALS]
        )
    )
    assert app.op == ""
    assert app.curr == "28890"
    assert app.prev == ""

    app.process_events(PygameEventUtils.keydown([pygame.K_9, pygame.K_BACKSPACE]))
    assert app.op == ""
    assert app.curr == ""
    assert app.prev == ""

    with pytest.raises(ValueError):
        app._format("n")

    assert app._format("1.2") == "1"
    assert app._format("2.0") == "2"

    app.menu._test_print_widgets()
    b1 = app.menu.get_widgets()[4]
    deco = b1.get_decorator()
    layer = b1.get_attribute("on_layer")

    assert not deco.is_enabled(layer)
    b1.select()
    assert deco.is_enabled(layer)
    b1.select(False)
    assert not deco.is_enabled(layer)


def test_example_other_dynamic_button_append():
    btn = dynamic_button.add_dynamic_button()
    assert btn.get_counter_attribute("count") == 0
    btn.apply()
    assert btn.get_counter_attribute("count") == 1
    dynamic_button.main(test=True)


def test_example_other_dynamic_widget_update():
    app = dynamic_widget.App()
    app.current = 3
    app.animate_quit_button(app.quit_button, app.menu)
    dynamic_widget.main(test=True)
    app.fake_quit()
    app._on_selector_change(3, 3)


def test_example_other_image_background():
    image_background.main(test=True)


def test_example_other_maze():
    app = maze.MazeApp(rows=10)
    btn = app._menu.get_widget("clear")

    app._path_found = True
    btn.apply()
    assert not app._path_found

    app._visualize = False
    gen = app._menu.get_widget("generator")
    sol = app._menu.get_widget("solver")

    for i in range(4):
        gen.set_value(i)
        sol.set_value(i)
        app._run_generator()
        app._run_solver()


def test_example_other_scrollbar():
    pygame.event.post(PygameEventUtils.keydown(pygame.K_v, inlist=False))
    pygame.event.post(PygameEventUtils.keydown(pygame.K_h, inlist=False))

    scrollbar.main(test=True)
    scrollbar.h_changed(1)
    scrollbar.v_changed(1)


def test_example_other_scrollbar_area():
    pygame.event.post(PygameEventUtils.keydown(pygame.K_ESCAPE, inlist=False))
    scrollbar_area.main(test=True)


def test_example_other_ui_solar_system():
    app = ui_solarsystem.main(test=True)

    assert not app.menu._disable_draw
    app.process_events(PygameEventUtils.keydown([pygame.K_p]), app.menu)
    assert app.menu._disable_draw

    app.process_events(
        PygameEventUtils.keydown(
            [pygame.K_p, pygame.K_q, pygame.K_e, pygame.K_s, pygame.K_c]
        ),
        app.menu,
    )
    assert not app.menu._disable_draw


def test_example_other_widget_positioning():
    widget_positioning.menu.render()

    assert widget_positioning.f.is_floating()
    assert widget_positioning.b1.is_floating()
    assert widget_positioning.b2.is_floating()
