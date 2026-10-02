"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - LABEL
Test Label widget.
"""

from unittest.mock import Mock, patch

import pytest

import pygame_menu.widgets.manager.label as label_module


class TestableLabelManager(label_module.LabelManager):
    __test__ = False  # Prevents pytest from collecting this as a test class

    def _add_submenu(self, *args, **kwargs):
        pass

    def _append_widget(self, *args, **kwargs):
        pass

    def _check_kwargs(self, *args, **kwargs):
        pass

    def _configure_widget(self, *args, **kwargs):
        pass

    def _filter_widget_attributes(self, *args, **kwargs):
        return {"font_color": (255, 255, 255)}

    def configure_defaults_widget(self, *args, **kwargs):
        pass

    @property
    def _theme(self):
        theme = Mock()
        theme.widget_font_color = (255, 255, 255)
        return theme

    @property
    def _menu(self):
        menu = Mock()
        menu.get_width.return_value = 100  # Narrow width to force wrapping easily
        return menu


@pytest.fixture
def manager():
    return object.__new__(TestableLabelManager)


def test_label_basic_creation(manager, monkeypatch):
    widget_mock = Mock(name="Label")
    label_factory = Mock(return_value=widget_mock)

    monkeypatch.setattr(label_module, "Label", label_factory)

    result = manager.label(
        title="Hello World",
        label_id="lbl-1",
        selectable=True,
        align="center",
    )

    assert result is widget_mock
    assert widget_mock.is_selectable is True
    label_factory.assert_called_once_with(
        label_id="lbl-1",
        onselect=None,
        title="Hello World",
        wordwrap=False,
        leading=None,
        max_nlines=None,
    )


def test_label_with_underline(manager, monkeypatch):
    widget_mock = Mock(name="Label")
    label_factory = Mock(return_value=widget_mock)

    monkeypatch.setattr(label_module, "Label", label_factory)

    manager.label(
        title="Underlined",
        underline=True,
        underline_color=(255, 0, 0),
        underline_offset=3,
        underline_width=2,
    )

    widget_mock.add_underline.assert_called_once_with((255, 0, 0), 3, 2)


def test_label_multiline_split(manager, monkeypatch):
    sub1 = Mock(name="Sub1")
    sub2 = Mock(name="Sub2")

    label_factory = Mock(side_effect=[sub1, sub2])
    monkeypatch.setattr(label_module, "Label", label_factory)

    result = manager.label(title="Line1\nLine2", label_id="multi", wordwrap=False)

    assert isinstance(result, list)
    assert result == [sub1, sub2]


def test_label_max_char_wrapping(manager, monkeypatch):
    widget_mock = Mock(name="Label")
    label_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(label_module, "Label", label_factory)

    result = manager.label(title="Long text string here", max_char=5, label_id="wrap")

    assert isinstance(result, list)
    assert len(result) > 1


def test_label_negative_max_char_calculates_width(manager, monkeypatch):
    dummy_widget = Mock(name="DummyLabel")
    dummy_widget.get_width.return_value = (
        200  # Large width so text overflows a small max_char calculation
    )

    # Use a side-effect function to return dummy_widget on first call, and fresh Mocks afterwards
    call_idx = 0

    def label_factory_side_effect(*args, **kwargs):
        nonlocal call_idx
        if call_idx == 0:
            call_idx += 1
            return dummy_widget
        call_idx += 1
        return Mock(name=f"WrappedLabel_{call_idx}")

    monkeypatch.setattr(label_module, "Label", label_factory_side_effect)

    result = manager.label(
        title="This is a very long text that will definitely exceed the calculated width limit",
        max_char=-1,
        label_id="auto",
    )

    assert isinstance(result, list)
    assert len(result) > 0


def test_label_assertions(manager):
    with pytest.raises(AssertionError):
        manager.label(title="Test", label_id=123)

    with pytest.raises(AssertionError):
        manager.label(title="Test", max_char="5")

    with pytest.raises(AssertionError):
        manager.label(title="Test", selectable="yes")

    with pytest.raises(AssertionError):
        manager.label(title="Test", max_char=-2)


def test_clock_label_creation(manager, monkeypatch):
    widget_mock = Mock(name="Label")
    label_factory = Mock(return_value=widget_mock)
    monkeypatch.setattr(label_module, "Label", label_factory)

    with patch("time.strftime", return_value="2026-06-06 12:00:00"):
        clock_lbl = manager.clock(
            clock_format="%Y-%m-%d %H:%M:%S",
            clock_id="my-clock",
            title_format="Time: {0}",
        )

    assert clock_lbl is widget_mock
    widget_mock.set_title_generator.assert_called_once()
    widget_mock.update.assert_called_once_with([])


def test_clock_assertions(manager, monkeypatch):
    widget_mock = Mock(name="Label")
    monkeypatch.setattr(label_module, "Label", Mock(return_value=widget_mock))

    with pytest.raises(AssertionError):
        manager.clock(title_format="Invalid Format")
