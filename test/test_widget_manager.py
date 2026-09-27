"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET MANAGER
Test WidgetManager class.
"""

from unittest.mock import patch

import pytest

import pygame_menu
from pygame_menu._widgetmanager import WidgetManager
from pygame_menu.widgets import Button, Label


@pytest.fixture
def menu_and_manager():
    """Provide a fresh menu and widget manager for each test."""
    menu = pygame_menu.Menu("Test Menu", 600, 400)
    manager = WidgetManager(menu)
    return menu, manager


def test_initialization(menu_and_manager):
    """Verify that the manager stores its associated menu."""
    menu, _ = menu_and_manager

    manager = WidgetManager(menu=menu, verbose=True)

    assert isinstance(manager, WidgetManager)
    assert manager._menu is menu
    assert manager._verbose is True


def test_initialization_with_verbose_disabled(menu_and_manager):
    """Verify that the verbose option is stored correctly."""
    menu, _ = menu_and_manager

    manager = WidgetManager(menu=menu, verbose=False)

    assert manager._verbose is False


def test_theme_property(menu_and_manager):
    """Verify that the theme property comes from the associated menu."""
    menu, manager = menu_and_manager

    assert manager._theme is menu.get_theme()


def test_filter_widget_attributes_uses_theme_defaults(menu_and_manager):
    """Verify that widget attributes default to theme values."""
    _, manager = menu_and_manager

    attributes = manager._filter_widget_attributes({})

    assert attributes["align"] == manager._theme.widget_alignment
    assert attributes["font_size"] == manager._theme.widget_font_size
    assert attributes["font_name"] == manager._theme.widget_font
    assert attributes["font_color"] == manager._theme.widget_font_color
    assert attributes["float"] is False
    assert attributes["float_origin_position"] is False


def test_filter_widget_attributes_override_values(menu_and_manager):
    """Verify that explicit values override theme defaults."""
    _, manager = menu_and_manager

    attributes = manager._filter_widget_attributes(
        {
            "font_size": 42,
            "align": pygame_menu.locals.ALIGN_RIGHT,
            "float": True,
            "margin": (5, 10),
        }
    )

    assert attributes["font_size"] == 42
    assert attributes["align"] == pygame_menu.locals.ALIGN_RIGHT
    assert attributes["float"] is True
    assert attributes["margin"] == (5, 10)


def test_filter_widget_attributes_consumes_supported_kwargs(menu_and_manager):
    """Verify that supported keyword arguments are removed from the input."""
    _, manager = menu_and_manager
    kwargs = {"font_size": 42, "float": True}

    manager._filter_widget_attributes(kwargs)

    assert kwargs == {}


def test_filter_widget_attributes_normalizes_background_inflate_zero(
    menu_and_manager,
):
    """Verify that zero background inflation becomes a two-item tuple."""
    _, manager = menu_and_manager

    attributes = manager._filter_widget_attributes({"background_inflate": 0})

    assert attributes["background_inflate"] == (0, 0)


def test_filter_widget_attributes_normalizes_border_inflate_zero(
    menu_and_manager,
):
    """Verify that zero border inflation becomes a two-item tuple."""
    _, manager = menu_and_manager

    attributes = manager._filter_widget_attributes({"border_inflate": 0})

    assert attributes["border_inflate"] == (0, 0)


def test_filter_widget_attributes_accepts_valid_inflate_values(menu_and_manager):
    """Verify that valid inflation vectors are preserved."""
    _, manager = menu_and_manager

    attributes = manager._filter_widget_attributes(
        {
            "background_inflate": (2, 3),
            "border_inflate": (4, 5),
        }
    )

    assert attributes["background_inflate"] == (2, 3)
    assert attributes["border_inflate"] == (4, 5)


@pytest.mark.parametrize(
    "option",
    ["align", "font_shadow_position"],
)
def test_filter_widget_attributes_rejects_non_string_options(
    menu_and_manager,
    option,
):
    """Verify that string-based options reject non-string values."""
    _, manager = menu_and_manager

    with pytest.raises(AssertionError):
        manager._filter_widget_attributes({option: 123})


@pytest.mark.parametrize(
    "option",
    ["font_size", "border_width", "font_shadow_offset"],
)
def test_filter_widget_attributes_rejects_invalid_integer_options(
    menu_and_manager,
    option,
):
    """Verify that integer options reject invalid values."""
    _, manager = menu_and_manager

    with pytest.raises(AssertionError):
        manager._filter_widget_attributes({option: "invalid"})


def test_filter_widget_attributes_rejects_non_positive_font_size(
    menu_and_manager,
):
    """Verify that font size must be greater than zero."""
    _, manager = menu_and_manager

    with pytest.raises(AssertionError, match="font size must be greater than zero"):
        manager._filter_widget_attributes({"font_size": 0})


@pytest.mark.parametrize("option", ["background_inflate", "border_inflate"])
def test_filter_widget_attributes_rejects_negative_inflate(
    menu_and_manager,
    option,
):
    """Verify that inflation values cannot be negative."""
    _, manager = menu_and_manager

    with pytest.raises(AssertionError):
        manager._filter_widget_attributes({option: (-1, 0)})


def test_filter_widget_attributes_rejects_negative_border_width(menu_and_manager):
    """Verify that border width cannot be negative."""
    _, manager = menu_and_manager

    with pytest.raises(AssertionError):
        manager._filter_widget_attributes({"border_width": -1})


def test_filter_widget_attributes_selection_effect_none_creates_default(
    menu_and_manager,
):
    """Verify that None creates a default selection effect."""
    _, manager = menu_and_manager

    attributes = manager._filter_widget_attributes({"selection_effect": None})

    assert isinstance(
        attributes["selection_effect"],
        pygame_menu.widgets.core.Selection,
    )


def test_filter_widget_attributes_copies_selection_effect(menu_and_manager):
    """Verify that a supplied selection effect is copied."""
    _, manager = menu_and_manager
    original = manager._theme.widget_selection_effect

    if original is None:
        pytest.skip("The active theme has no selection effect.")

    attributes = manager._filter_widget_attributes({"selection_effect": original})

    assert attributes["selection_effect"] is not original
    assert isinstance(
        attributes["selection_effect"],
        pygame_menu.widgets.core.Selection,
    )


def test_check_kwargs_accepts_empty_kwargs():
    """Verify that empty keyword arguments are accepted."""
    WidgetManager._check_kwargs({})


def test_check_kwargs_rejects_unknown_keyword():
    """Verify that unknown widget keywords raise ValueError."""
    with pytest.raises(
        ValueError,
        match=r"widget addition optional parameter kwargs\.unknown is not valid",
    ):
        WidgetManager._check_kwargs({"unknown": True})


def test_configure_defaults_marks_widget_configured(menu_and_manager):
    """Verify that default configuration marks a widget configured."""
    _, manager = menu_and_manager
    label = Label("Test")

    assert label.configured is False

    manager.configure_defaults_widget(label)

    assert label.configured is True


def test_configure_defaults_applies_menu_controls(menu_and_manager):
    """Verify that default configuration applies menu controls."""
    menu, manager = menu_and_manager
    label = Label("Test")

    with patch.object(label, "set_controls") as set_controls:
        manager.configure_defaults_widget(label)

    set_controls.assert_called_once_with(
        joystick=menu._joystick,
        keyboard=menu._keyboard,
        mouse=menu._mouse,
        touchscreen=menu._touchscreen,
    )


def test_configure_defaults_rejects_invalid_object(menu_and_manager):
    """Verify that default configuration requires a widget instance."""
    _, manager = menu_and_manager

    with pytest.raises(AssertionError):
        manager.configure_defaults_widget(object())


def test_generic_widget_addition(menu_and_manager):
    """Verify that a configured widget is appended to the menu."""
    menu, manager = menu_and_manager
    label = Label("Hello World")

    result = manager.generic_widget(label, configure_defaults=True)

    assert result is label
    assert label in menu._widgets
    assert label.get_menu() is menu
    assert label.configured is True


def test_generic_widget_without_default_configuration(menu_and_manager):
    """Verify that generic_widget can append an unconfigured widget."""
    menu, manager = menu_and_manager
    label = Label("Hello World")

    result = manager.generic_widget(label, configure_defaults=False)

    assert result is label
    assert label in menu._widgets
    assert label.get_menu() is menu


def test_generic_widget_rejects_non_widget(menu_and_manager):
    """Verify that generic_widget requires a widget instance."""
    _, manager = menu_and_manager

    with pytest.raises(AssertionError):
        manager.generic_widget(object())


def test_generic_widget_already_attached_raises(menu_and_manager):
    """Verify that an already attached widget cannot be appended twice."""
    _, manager = menu_and_manager
    label = Label("Label")

    manager.generic_widget(label)

    with pytest.raises(ValueError, match="already appended to another Menu"):
        manager.generic_widget(label)


def test_generic_widget_attached_to_different_menu_raises(menu_and_manager):
    """Verify that widgets from another menu cannot be reused."""
    menu, manager = menu_and_manager
    other_menu = pygame_menu.Menu("Other Menu", 400, 300)
    label = Label("Attached")

    label.set_menu(other_menu)

    with pytest.raises(ValueError, match="already appended to another Menu"):
        manager.generic_widget(label)


def test_append_selectable_widget_updates_index(menu_and_manager):
    """Verify that the first selectable widget becomes selected."""
    menu, manager = menu_and_manager
    button = Button("Play", onreturn=lambda: None)

    manager.generic_widget(button, configure_defaults=True)

    assert menu._index == 0
    assert button.is_selected()


def test_append_non_selectable_widget_does_not_change_index(menu_and_manager):
    """Verify that a non-selectable widget does not change selection."""
    menu, manager = menu_and_manager
    button = Button("Play", onreturn=lambda: None)

    manager.generic_widget(button, configure_defaults=True)
    index_before = menu._index

    label = Label("Label")
    manager.generic_widget(label, configure_defaults=True)

    assert menu._index == index_before
    assert not label.is_selected()


def test_second_selectable_widget_does_not_replace_selection(menu_and_manager):
    """Verify that later selectable widgets do not replace the selection."""
    menu, manager = menu_and_manager

    first = Button("First", onreturn=lambda: None)
    second = Button("Second", onreturn=lambda: None)

    manager.generic_widget(first, configure_defaults=True)
    manager.generic_widget(second, configure_defaults=True)

    assert menu._index == 0
    assert first.is_selected()
    assert not second.is_selected()


def test_append_duplicate_id_raises(menu_and_manager):
    """Verify that duplicate widget identifiers raise IndexError."""
    _, manager = menu_and_manager
    label1 = Label("A", label_id="same")
    label2 = Label("B", label_id="same")

    manager.generic_widget(label1)

    with pytest.raises(IndexError, match=r'widget id "same" already exists'):
        manager.generic_widget(label2)


def test_add_submenu_registers_hook(menu_and_manager):
    """Verify that a submenu hook is registered correctly."""
    menu, manager = menu_and_manager
    submenu = pygame_menu.Menu("Sub", 300, 200)
    button = Button("Settings", onreturn=lambda: None)

    manager._add_submenu(submenu, button)

    assert submenu in menu._submenus
    assert button in menu._submenus[submenu]
    assert button._menu_hook is submenu


def test_add_submenu_registers_multiple_hooks(menu_and_manager):
    """Verify that multiple widgets can hook the same submenu."""
    menu, manager = menu_and_manager
    submenu = pygame_menu.Menu("Sub", 300, 200)
    first = Button("First", onreturn=lambda: None)
    second = Button("Second", onreturn=lambda: None)

    manager._add_submenu(submenu, first)
    manager._add_submenu(submenu, second)

    assert menu._submenus[submenu] == [first, second]


def test_add_submenu_rejects_self_reference(menu_and_manager):
    """Verify that a menu cannot be registered as its own submenu."""
    menu, manager = menu_and_manager
    button = Button("Settings", onreturn=lambda: None)

    with pytest.raises(AssertionError, match="submenu cannot point to menu itself"):
        manager._add_submenu(menu, button)


def test_add_submenu_rejects_duplicate_hook(menu_and_manager):
    """Verify that the same widget cannot hook a submenu twice."""
    _, manager = menu_and_manager
    submenu = pygame_menu.Menu("Sub", 300, 200)
    button = Button("Settings", onreturn=lambda: None)

    manager._add_submenu(submenu, button)

    with pytest.raises(AssertionError, match="already hooks submenu"):
        manager._add_submenu(submenu, button)


def test_add_submenu_rejects_invalid_menu(menu_and_manager):
    """Verify that submenu registration requires a menu instance."""
    _, manager = menu_and_manager
    button = Button("Settings", onreturn=lambda: None)

    with pytest.raises(AssertionError):
        manager._add_submenu(object(), button)


def test_add_submenu_rejects_invalid_hook(menu_and_manager):
    """Verify that submenu registration requires a widget hook."""
    _, manager = menu_and_manager
    submenu = pygame_menu.Menu("Sub", 300, 200)

    with pytest.raises(AssertionError):
        manager._add_submenu(submenu, object())


def test_append_widget_assigns_menu(menu_and_manager):
    """Verify that appending assigns the widget to the current menu."""
    menu, manager = menu_and_manager
    label = Label("Label")

    manager._append_widget(label)

    assert label.get_menu() is menu


def test_append_widget_assigns_scrollarea(menu_and_manager):
    """Verify that appending assigns the menu scroll area."""
    menu, manager = menu_and_manager
    label = Label("Label")

    manager._append_widget(label)

    assert label.get_scrollarea() is menu.get_scrollarea()


def test_append_widget_initializes_widgets_surface(menu_and_manager):
    """Verify that appending invalidates the cached widget surface."""
    menu, manager = menu_and_manager
    menu._widgets_surface = object()
    label = Label("Label")

    manager._append_widget(label)

    assert menu._widgets_surface is not None


def test_append_widget_rolls_back_on_sizing_exception(menu_and_manager):
    """Verify that sizing failures remove the widget from the menu."""
    menu, manager = menu_and_manager
    label = Label("Overflowing Widget")
    initial_widgets = list(menu._widgets)
    initial_index = menu._index

    with patch.object(
        menu,
        "_render",
        side_effect=pygame_menu.menu._MenuSizingException("Sizing failed"),
    ):
        with pytest.raises(pygame_menu.menu._MenuSizingException):
            manager._append_widget(label)

    assert menu._widgets == initial_widgets
    assert menu._index == initial_index
    assert label not in menu._widgets
    assert label.get_menu() is None


def test_append_widget_rolls_back_on_widget_overflow(menu_and_manager):
    """Verify that widget overflow failures remove the widget from the menu."""
    menu, manager = menu_and_manager
    label = Label("Overflowing Widget")
    initial_widgets = list(menu._widgets)
    initial_index = menu._index

    with patch.object(
        menu,
        "_render",
        side_effect=pygame_menu.menu._MenuWidgetOverflow("Overflow"),
    ):
        with pytest.raises(pygame_menu.menu._MenuWidgetOverflow):
            manager._append_widget(label)

    assert menu._widgets == initial_widgets
    assert menu._index == initial_index
    assert label not in menu._widgets
    assert label.get_menu() is None


def test_append_widget_rollback_preserves_widget_count(menu_and_manager):
    """Verify that render failure preserves the widget count."""
    menu, manager = menu_and_manager
    label = Label("Rollback")
    initial_count = len(menu._widgets)

    with patch.object(
        menu,
        "_render",
        side_effect=pygame_menu.menu._MenuSizingException("Failure"),
    ):
        with pytest.raises(pygame_menu.menu._MenuSizingException):
            manager._append_widget(label)

    assert len(menu._widgets) == initial_count


def test_append_widget_rollback_restores_existing_index(menu_and_manager):
    """Verify that render failure preserves an existing selection index."""
    menu, manager = menu_and_manager
    button = Button("Button", onreturn=lambda: None)

    manager.generic_widget(button, configure_defaults=True)
    initial_index = menu._index

    with patch.object(
        menu,
        "_render",
        side_effect=pygame_menu.menu._MenuSizingException("Failure"),
    ):
        with pytest.raises(pygame_menu.menu._MenuSizingException):
            manager._append_widget(Label("Temporary"))

    assert menu._index == initial_index
    assert button.is_selected()


def test_append_widget_calls_render_and_render_menu(menu_and_manager):
    """Verify that appending renders the menu and its widgets."""
    menu, manager = menu_and_manager
    label = Label("Label")

    with (
        patch.object(menu, "_render", wraps=menu._render) as render,
        patch.object(menu, "render", wraps=menu.render) as menu_render,
    ):
        manager._append_widget(label)

    assert render.call_count == 2
    menu_render.assert_called_once_with()


def test_append_widget_calls_widget_append_hook(menu_and_manager):
    """Verify that appending invokes the widget append hook."""
    _, manager = menu_and_manager
    label = Label("Label")

    with patch.object(label, "_append_to_menu") as append_hook:
        manager._append_widget(label)

    append_hook.assert_called_once_with()


def test_generic_widget_warns_for_button_to_menu(menu_and_manager):
    """Verify that button submenu usage emits a warning."""
    _, manager = menu_and_manager
    button = Button("Open", onreturn=lambda: None)
    button.to_menu = True

    with patch("pygame_menu._widgetmanager.warn") as warning:
        manager.generic_widget(button)

    warning.assert_called_once()
    assert (
        "prefer adding submenus using add_button method" in (warning.call_args.args[0])
    )
