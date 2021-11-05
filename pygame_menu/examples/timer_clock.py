"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - TIMER CLOCK
Example file, timer clock with in-menu options.
"""

__all__ = ['main']

import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

import datetime
from random import randrange
from typing import List, Tuple, Optional

# Constants and global variables
ABOUT = [f'pygame-menu {pygame_menu.__version__}',
         f'Author: {pygame_menu.__author__}',
         '',
         f'Email: {pygame_menu.__email__}']
COLOR_BACKGROUND = [128, 0, 128]
FPS = 60
H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
W_SIZE = 800  # Width of window size

surface: Optional['pygame.Surface'] = None
timer: Optional[List[float]] = None


def mainmenu_background() -> None:
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.

    :return: None
    """
    surface.fill((40, 0, 40))


def reset_timer() -> None:
    """
    Reset timer.

    :return: None
    """
    timer[0] = 0


class TestCallClassMethod(object):
    """
    Class call method.
    """

    @staticmethod
    def update_game_settings() -> None:
        """
        Class method.

        :return: None
        """
        print('Update game with new settings')


def change_color_bg(value: Tuple, c: Optional[Tuple] = None, **kwargs) -> None:
    """
    Change background color.

    :param value: Selected option (data, index)
    :param c: Color tuple
    :return: None
    """
    color, _ = value
    if c == (-1, -1, -1):  # If random color
        c = (randrange(0, 255), randrange(0, 255), randrange(0, 255))
    if kwargs['write_on_console']:
        print('New background color: {0} ({1},{2},{3})'.format(color[0], *c))
    COLOR_BACKGROUND[0] = c[0]
    COLOR_BACKGROUND[1] = c[1]
    COLOR_BACKGROUND[2] = c[2]


def main(test: bool = False) -> None:
    """
    Main program.

    :param test: Indicate function is being tested
    :return: None
    """

    # -------------------------------------------------------------------------
    # Init
    # -------------------------------------------------------------------------

    # Write help message on console
    for m in HELP:
        print(m)

    # Create window
    global surface
    surface = create_example_window('Example - Timer Clock', (W_SIZE, H_SIZE))

    # Main timer and game clock
    clock = pygame.time.Clock()
    global timer
    timer = [0]
    dt = 1.0 / FPS
    timer_font = pygame_menu.font.get_font(pygame_menu.font.FONT_NEVIS, 100)
    frame = 0

    # -------------------------------------------------------------------------
    # Create menus: Timer
    # -------------------------------------------------------------------------

    timer_theme = pygame_menu.themes.THEME_DARK.copy()  # Create a new copy
    timer_theme.background_color = (0, 0, 0, 180)  # Enable transparency

    # Timer
    timer_menu = pygame_menu.Menu(
        height=400,
        onclose=pygame_menu.events.RESET,
        theme=timer_theme,
        title='Timer Menu',
        width=600
    )

    # Add widgets
    timer_menu.add.button('Reset timer', reset_timer)

    # Adds a selector (element that can handle functions)
    timer_menu.add.selector(
        title='Change color ',
        items=[('Random', (-1, -1, -1)),  # Values of selector, call to change_color_bg
               ('Default', (128, 0, 128)),
               ('Black', (0, 0, 0)),
               ('Blue', (12, 12, 200))],
        default=1,  # Optional parameter that sets default item of selector
        onchange=change_color_bg,  # Action when changing element with left/right
        onreturn=change_color_bg,  # Action when pressing return on an element
        # All the following kwargs are passed to change_color_bg function
        write_on_console=True
    )
    timer_menu.add.button('Update game object', TestCallClassMethod().update_game_settings)
    timer_menu.add.button('Return to Menu', pygame_menu.events.BACK)
    timer_menu.add.button('Close Menu', pygame_menu.events.CLOSE)

    # -------------------------------------------------------------------------
    # Create menus: Help
    # -------------------------------------------------------------------------
    help_theme = pygame_menu.Theme(
        background_color=(30, 50, 107, 190),  # 75% opacity
        title_background_color=(120, 45, 30, 190),
        title_font=pygame_menu.font.FONT_FRANCHISE,
        title_font_size=60,
        widget_font=pygame_menu.font.FONT_FRANCHISE,
        widget_font_color=(170, 170, 170),
        widget_font_shadow=True,
        widget_font_shadow_position=pygame_menu.locals.POSITION_SOUTHEAST,
        widget_font_size=45
    )

    help_menu = pygame_menu.Menu(
        height=600,  # Fullscreen
        theme=help_theme,
        title='Help',
        width=800
    )
    for m in HELP:
        help_menu.add.label(m, align=pygame_menu.locals.ALIGN_CENTER)
    help_menu.add.vertical_margin(25)
    help_menu.add.button('Return to Menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_DARK.copy()
    about_theme.widget_font = pygame_menu.font.FONT_NEVIS
    about_theme.title_font = pygame_menu.font.FONT_8BIT
    about_theme.title_offset = (5, -2)
    about_theme.widget_offset = (0, 0.14)

    about_menu = pygame_menu.Menu(
        center_content=False,
        height=400,
        mouse_visible=False,
        theme=about_theme,
        title='About',
        width=600
    )
    for m in ABOUT:
        about_menu.add.label(m, margin=(0, 0))
    about_menu.add.label('')
    about_menu.add.button('Return to Menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main menu
    # -------------------------------------------------------------------------
    main_menu = pygame_menu.Menu(
        enabled=False,
        height=400,
        theme=pygame_menu.themes.THEME_DARK,
        title='Main Menu',
        width=600
    )

    main_menu.add.button(timer_menu.get_title(), timer_menu)  # Add timer submenu
    main_menu.add.button(help_menu.get_title(), help_menu)  # Add help submenu
    main_menu.add.button(about_menu.get_title(), about_menu)  # Add about submenu
    main_menu.add.button('Exit', pygame_menu.events.EXIT)  # Add exit function

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick clock
        clock.tick(FPS)
        timer[0] += dt
        frame += 1

        # Title is evaluated at current level as the title of the base pointer
        # object (main_menu) can change if user opens submenus
        current_menu = main_menu.get_current()
        if current_menu.get_title() != 'Main Menu' or not main_menu.is_enabled():
            # Draw timer
            surface.fill(COLOR_BACKGROUND)
            time_string = str(datetime.timedelta(seconds=int(timer[0])))
            time_blit = timer_font.render(time_string, True, (255, 255, 255))
            time_blit_size = time_blit.get_size()
            surface.blit(time_blit, (int(W_SIZE / 2 - time_blit_size[0] / 2),
                                     int(H_SIZE / 2 - time_blit_size[1] / 2)))
        else:
            # Background color if the menu is enabled and timer is hidden
            surface.fill((40, 0, 40))

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and \
                        current_menu.get_title() == 'Main Menu':
                    main_menu.toggle()

        if main_menu.is_enabled():
            main_menu.draw(surface)
            main_menu.update(events)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test and frame == 2:
            break


if __name__ == '__main__':
    main()
