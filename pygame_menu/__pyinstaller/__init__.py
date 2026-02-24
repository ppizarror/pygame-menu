"""
pygame-menu
https://github.com/ppizarror/pygame-menu

PYINSTALLER
Module for pyinstaller.
"""

__all__ = ['get_hook_dirs']

from pathlib import Path
from typing import List


def get_hook_dirs() -> List[str]:
    """
    Return hook dirs to PyInstaller.

    :return: Hook dir list
    """
    return [Path(__file__).resolve().parent.as_posix()]
