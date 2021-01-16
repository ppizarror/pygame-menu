# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - IMAGE BACKGROUND
Menu using background image + BaseImage object.

NOTE: pygame-menu v3 will not provide new widgets or functionalities, consider
upgrading to the latest version.

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

from __future__ import print_function
import sys
import os

sys.path.insert(0, '../../')

import pygame
import pygame_menu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
FPS = 60
WINDOW_SIZE = (640, 480)

# noinspection PyTypeChecker
sound = None  # type: pygame_menu.sound.Sound
# noinspection PyTypeChecker
surface = None  # type: pygame.Surface
# noinspection PyTypeChecker
main_menu = None  # type: pygame_menu.Menu

# -----------------------------------------------------------------------------
# Load image
# -----------------------------------------------------------------------------
background_image = pygame_menu.baseimage.BaseImage(
    image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_WALLPAPER
)


# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------
def main_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.

    :return: None
    """
    background_image.draw(surface)


def main(test=False):
    """
    Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # -------------------------------------------------------------------------
    # Globals
    # -------------------------------------------------------------------------
    global main_menu
    global sound
    global surface

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create pygame screen and objects
    surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Example - Image Background')
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
    widget_colors_theme.widget_font_size = 20
    widget_colors_theme.set_background_color_opacity(0.5)  # 50% opacity

    widget_colors = pygame_menu.Menu(
        height=WINDOW_SIZE[1] * 0.7,
        theme=widget_colors_theme,
        title='Widget backgrounds',
        width=WINDOW_SIZE[0] * 0.8
    )

    button_image = pygame_menu.baseimage.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_CARBON_FIBER)

    widget_colors.add_button('Opaque color button', None,
                             background_color=(100, 100, 100))
    widget_colors.add_button('Transparent color button', None,
                             background_color=(50, 50, 50, 200), font_size=40)
    widget_colors.add_button('Transparent background inflate to selection effect', None,
                             background_color=(50, 50, 50, 200), margin=(0, 15)
                             ).expand_background_inflate_to_selection_effect()
    widget_colors.add_button('Background inflate + font background color', None,
                             background_color=(50, 50, 50, 200), font_background_color=(200, 200, 200)
                             ).expand_background_inflate_to_selection_effect()
    widget_colors.add_button('This inflates background to match selection effect', None,
                             background_color=button_image, font_color=(255, 255, 255), font_size=15
                             ).selection_expand_background = True
    widget_colors.add_button('This is already inflated to match selection effect', None,
                             background_color=button_image, font_color=(255, 255, 255), font_size=15
                             ).expand_background_inflate_to_selection_effect()

    main_menu.add_button('Test different widget colors', widget_colors)
    main_menu.add_button('Another fancy button', lambda: print('This button has been pressed'))
    main_menu.add_button('Quit', pygame_menu.events.EXIT)

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
