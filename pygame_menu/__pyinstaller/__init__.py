"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PYINSTALLER
Module for pyinstaller.
"""

__all__ = ['get_hook_dirs']

import os
from typing import List


def get_hook_dirs() -> List[str]:
    """
    Return hook dirs to PyInstaller.

    :return: Hook dir list
    """
    return [os.path.dirname(__file__)]
