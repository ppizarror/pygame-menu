# coding=utf-8
"""
Dynamic button append and update.
"""

import sys

sys.path.insert(0, '../../')
import pygame_menu
from random import randrange
import pygame
import os

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
surface = pygame.display.set_mode((600, 400))

menu = pygame_menu.Menu(height=300,
                        width=400,
                        theme=pygame_menu.themes.THEME_BLUE,
                        title='Welcome')


def add_dynamic_button():
    """
    Append a button to the menu on demand.
    """
    print('Adding a button dynamically')
    btn = menu.add_button(randrange(0, 10), None)

    def _update_button():
        count = btn.get_attribute('count', int(btn.get_title())) + 1
        btn.set_title(count)
        btn.set_attribute('count', count)

    btn.update_callback(_update_button)


menu.add_text_input('Name: ', default='John Doe')
menu.add_button('Play', add_dynamic_button)
menu.add_button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)
