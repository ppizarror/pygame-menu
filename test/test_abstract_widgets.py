"""
pygame-menu

TEST ABSTRACT WIDGET MANAGER
Test suite for AbstractWidgetManager abstraction contract.
"""

from __future__ import annotations

from typing import Any

import pytest

from pygame_menu.widgets.core.abstract_widget import AbstractWidgetManager


class DummyConcreteWidgetManager(AbstractWidgetManager):
    """
    Minimal valid implementation of AbstractWidgetManager.
    """

    @property
    def _theme(self) -> Any:
        return "theme"

    def _add_submenu(self, menu: Any, hook: Any) -> None:
        return None

    def _filter_widget_attributes(
        self,
        kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        return kwargs

    def _configure_widget(self, widget: Any, **kwargs: Any) -> None:
        return None

    @staticmethod
    def _check_kwargs(kwargs: dict[str, Any]) -> None:
        return None

    def _append_widget(self, widget: Any) -> None:
        return None

    def configure_defaults_widget(self, widget: Any) -> None:
        return None


def test_abstract_widget_manager_cannot_be_instantiated() -> None:
    """
    AbstractWidgetManager must not be directly instantiable.
    """
    with pytest.raises(TypeError):
        AbstractWidgetManager()


def test_concrete_implementation_can_be_instantiated() -> None:
    """
    A fully implemented subclass must be instantiable.
    """
    manager = DummyConcreteWidgetManager()

    assert isinstance(manager, AbstractWidgetManager)


@pytest.mark.parametrize(
    "missing_member",
    [
        "_theme",
        "_add_submenu",
        "_filter_widget_attributes",
        "_configure_widget",
        "_check_kwargs",
        "_append_widget",
        "configure_defaults_widget",
    ],
)
def test_all_abstract_members_are_required(
    missing_member: str,
) -> None:
    """
    Omitting any abstract member must prevent instantiation.
    """
    namespace = {
        "_theme": property(lambda self: None),
        "_add_submenu": lambda self, menu, hook: None,
        "_filter_widget_attributes": lambda self, kwargs: kwargs,
        "_configure_widget": lambda self, widget, **kwargs: None,
        "_check_kwargs": staticmethod(lambda kwargs: None),
        "_append_widget": lambda self, widget: None,
        "configure_defaults_widget": lambda self, widget: None,
    }

    del namespace[missing_member]

    cls = type(
        "IncompleteManager",
        (AbstractWidgetManager,),
        namespace,
    )

    with pytest.raises(TypeError):
        cls()


def test_static_abstract_method_is_enforced() -> None:
    """
    _check_kwargs is an abstract staticmethod and must be implemented.
    """

    class InvalidManager(AbstractWidgetManager):
        @property
        def _theme(self) -> Any:
            return None

        def _add_submenu(self, menu: Any, hook: Any) -> None:
            pass

        def _filter_widget_attributes(
            self,
            kwargs: dict[str, Any],
        ) -> dict[str, Any]:
            return kwargs

        def _configure_widget(self, widget: Any, **kwargs: Any) -> None:
            pass

        def _append_widget(self, widget: Any) -> None:
            pass

        def configure_defaults_widget(self, widget: Any) -> None:
            pass

    with pytest.raises(TypeError):
        InvalidManager()


def test_concrete_subclass_exposes_contract_members() -> None:
    """
    Verify a concrete implementation satisfies the public contract.
    """
    manager = DummyConcreteWidgetManager()

    assert manager._theme == "theme"

    assert callable(manager._add_submenu)
    assert callable(manager._filter_widget_attributes)
    assert callable(manager._configure_widget)
    assert callable(manager._check_kwargs)
    assert callable(manager._append_widget)
    assert callable(manager.configure_defaults_widget)


def test_abstract_methods_registry() -> None:
    """
    Validate the abstract method registry exposed by ABC.
    """
    expected = {
        "_theme",
        "_add_submenu",
        "_filter_widget_attributes",
        "_configure_widget",
        "_check_kwargs",
        "_append_widget",
        "configure_defaults_widget",
    }

    assert AbstractWidgetManager.__abstractmethods__ == expected
