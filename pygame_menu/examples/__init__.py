"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLES
Example file directory.
"""

__all__ = ['create_example_window']

import pygame
import sys

from typing import Tuple

_PYGAME_ICON = [None]


# noinspection PyTypeChecker
def create_example_window(
        title: str,
        window_size: Tuple[int, int],
        pygame_menu_icon: bool = True,
        init_pygame: bool = True,
        center_window: bool = True,
        **kwargs
) -> 'pygame.Surface':
    """
    Set pygame window.

    :param title: Window title
    :param window_size: Window size
    :param pygame_menu_icon: Use pygame menu icon
    :param init_pygame: Init pygame
    :param center_window: Center the window
    :param kwargs: Optional keyword arguments received by display set_mode
    :return: Pygame surface from created display
    """
    assert len(title) > 0, 'title cannot be empty'
    assert len(window_size) == 2, 'window size shape must be (width, height)'
    assert isinstance(window_size[0], int), 'width must be an integer'
    assert isinstance(window_size[1], int), 'height must be an integer'

    from pygame_menu.baseimage import IMAGE_EXAMPLE_PYGAME_MENU, BaseImage
    import os

    if init_pygame:
        pygame.init()
    if center_window:
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    if sys.platform == 'darwin':
        kwargs = {}

    try:
        surface = pygame.display.set_mode(window_size, **kwargs)
    except TypeError:
        surface = pygame.display.set_mode(window_size)
    pygame.display.set_caption(title)

    if pygame_menu_icon:
        # noinspection PyBroadException
        try:
            if _PYGAME_ICON[0] is not None:
                pygame.display.set_icon(_PYGAME_ICON[0])
            else:
                icon = BaseImage(IMAGE_EXAMPLE_PYGAME_MENU).get_surface(new=False)
                pygame.display.set_icon(icon)
                _PYGAME_ICON[0] = icon
        except BaseException:  # lgtm [py/catch-base-exception]
            pass

    return surface
