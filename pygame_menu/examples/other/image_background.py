"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - IMAGE BACKGROUND
Menu using background image + BaseImage object.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2021 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

__all__ = ['main']

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from typing import Optional

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60
WINDOW_SIZE = (640, 480)

sound: Optional['pygame_menu.sound.Sound'] = None
surface: Optional['pygame.Surface'] = None
main_menu: Optional['pygame_menu.Menu'] = None

# -----------------------------------------------------------------------------
# Load image
# -----------------------------------------------------------------------------
background_image = pygame_menu.BaseImage(
    image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_WALLPAPER
)


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def main_background() -> None:
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.

    :return: None
    """
    background_image.draw(surface)


def main(test: bool = False) -> None:
    """
    Main program.

    :param test: Indicate function is being tested
    :return: None
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface

    # -------------------------------------------------------------------------
    # Create window
    # -------------------------------------------------------------------------
    surface = create_example_window('Example - Image Background', WINDOW_SIZE)
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
    main_menu_theme.set_background_color_opacity(0.5)  # 50% opacity

    main_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        theme=main_menu_theme,
        title='Epic Menu',
        width=WINDOW_SIZE[0] * 0.8
    )

    widget_colors_theme = pygame_menu.themes.THEME_ORANGE.copy()
    widget_colors_theme.widget_margin = (0, 10)
    widget_colors_theme.widget_padding = 0
    widget_colors_theme.widget_selection_effect.margin_xy(10, 5)
    widget_colors_theme.widget_font_size = 20
    widget_colors_theme.set_background_color_opacity(0.5)  # 50% opacity

    widget_colors = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        theme=widget_colors_theme,
        title='Widget backgrounds',
        width=WINDOW_SIZE[0] * 0.8
    )

    button_image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_CARBON_FIBER)

    widget_colors.add.button('Opaque color button',
                             background_color=(100, 100, 100))
    widget_colors.add.button('Transparent color button',
                             background_color=(50, 50, 50, 200), font_size=40)
    widget_colors.add.button('Transparent background inflate to selection effect',
                             background_color=(50, 50, 50, 200),
                             margin=(0, 15)).background_inflate_to_selection_effect()
    widget_colors.add.button('Background inflate + font background color',
                             background_color=(50, 50, 50, 200),
                             font_background_color=(200, 200, 200)
                             ).background_inflate_to_selection_effect()
    widget_colors.add.button('This inflates background to match selection effect',
                             background_color=button_image,
                             font_color=(255, 255, 255), font_size=15
                             ).selection_expand_background = True
    widget_colors.add.button('This is already inflated to match selection effect',
                             background_color=button_image,
                             font_color=(255, 255, 255), font_size=15
                             ).background_inflate_to_selection_effect()

    main_menu.add.button('Test different widget colors', widget_colors)
    main_menu.add.button('Another fancy button', lambda: print('This button has been pressed'))
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Main menu
        main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
