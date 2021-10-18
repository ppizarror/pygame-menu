"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - WINDOW RESIZE
Resize the menu when the window is resized.

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

import pygame
import pygame_menu

pygame.init()

surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
pygame.display.set_caption("Example resizable window")

menu = pygame_menu.Menu(
    height=100,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Welcome',
    width=100
)


def on_resize() -> None:
    """
    Function checked if the window is resized.
    """
    window_size = surface.get_size()
    new_w, new_h = 0.75 * window_size[0], 0.7 * window_size[1]
    menu.resize(new_w, new_h)
    print(f'New menu size: {menu.get_size()}')


menu.add.label('Resize the window!')
user_name = menu.add.text_input('Name: ', default='John Doe', maxchar=10)
menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)])
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.enable()
on_resize()  # Set initial size

if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.VIDEORESIZE:
                # Update the surface
                surface = pygame.display.set_mode((event.w, event.h),
                                                  pygame.RESIZABLE)
                # Call the menu event
                on_resize()

        # Draw the menu
        surface.fill((25, 0, 50))

        menu.update(events)
        menu.draw(surface)

        pygame.display.flip()
