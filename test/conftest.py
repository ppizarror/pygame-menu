"""
Pytest configuration for pygame-menu test suite.
Provides fixtures for resetting the pygame surface.
"""

import gc

import pytest

from test._utils import test_reset_surface


@pytest.fixture(autouse=True)
def disable_gc():
    gc.disable()
    yield
    gc.enable()
    gc.collect()


@pytest.fixture(autouse=True)
def pygame_surface():
    """
    Automatically reset the pygame surface before and after each test.
    """
    test_reset_surface()
    yield
    test_reset_surface()
