"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - DYNAMIC BUTTON
Menu with dynamic buttons.
"""

__all__ = ['main']

import pygame_menu
from pygame_menu.examples import create_example_window

from random import randrange

surface = create_example_window('Example - Dynamic Button Append', (600, 400))
menu = pygame_menu.Menu(
    height=300,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Welcome',
    width=400
)


def add_dynamic_button() -> 'pygame_menu.widgets.Button':
    """
    Append a button to the menu on demand.

    :return: Appended button
    """
    print(f'Adding a button dynamically, total: {len(menu.get_widgets()) - 2}')
    btn = menu.add.button(randrange(0, 10))

    def _update_button() -> None:
        count = btn.get_counter_attribute('count', 1, btn.get_title())
        btn.set_title(str(count))

    btn.update_callback(_update_button)
    return btn


menu.add.text_input('Name: ', default='John Doe')
menu.add.button('Play', add_dynamic_button)
menu.add.button('Quit', pygame_menu.events.EXIT)


def main(test: bool = False) -> None:
    """
    Main function.

    :param test: Indicate function is being tested
    :return: None
    """
    menu.mainloop(surface, disable_loop=test)


if __name__ == '__main__':
    main()
