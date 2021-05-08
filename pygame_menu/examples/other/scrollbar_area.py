"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - SCROLL AREA
Shows ScrollArea widget usage.

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
from pygame_menu import locals
from pygame_menu.examples import create_example_window
from pygame_menu._scrollarea import ScrollArea
from pygame_menu.utils import make_surface

import itertools
from typing import Generator

FPS = 30
W_SIZE = 800  # Width of window size
H_SIZE = 600  # Height of window size
COLOR_BACKGROUND = (128, 230, 198)
LEGEND = 'Area {}x{}\nWorld {}x{}\nPress [ESC] to change'

WORLDS = {
    '1': {'pos': (0, 0),
          'win': (W_SIZE, H_SIZE),
          'size': (W_SIZE * 2, H_SIZE * 3)},
    '2': {'pos': (200, 100),
          'win': (W_SIZE // 2, H_SIZE // 2),
          'size': (W_SIZE * 2, H_SIZE * 3)},
    '3': {'pos': (50, 250),
          'win': (W_SIZE // 2, H_SIZE // 2),
          'size': (200, 200)},
    '4': {'pos': (350, 250),
          'win': (W_SIZE // 2, H_SIZE // 2),
          'size': (W_SIZE // 2, H_SIZE // 2)},
    '5': {'pos': (200, 200),
          'win': (W_SIZE // 2, H_SIZE // 2),
          'size': (W_SIZE // 2, H_SIZE // 2 + 10)},
    '6': {'pos': (10, 10),
          'win': (W_SIZE - 300, H_SIZE // 2),
          'size': (W_SIZE - 200, H_SIZE // 2 - 10)}
}


def make_world(width: int, height: int, text: str = '') -> 'pygame.Surface':
    """
    Create a test surface.

    :param width: Width in pixels
    :param height: Height in pixels
    :param text: Text to write
    :return: World surface
    """
    world = make_surface(width, height)
    world.fill((210, 210, 210))
    font = pygame.font.SysFont('arial', 20)

    posy = 60
    for line in text.splitlines():
        text = font.render(str(line), True, (0, 0, 0))
        world.blit(text, (60, posy))
        posy += text.get_height() + 10

    for x in range(0, width, 10):
        if x % 100 == 0 and x != 0:
            pygame.draw.line(world, (255, 0, 0), (x, 0), (x, 20))
            pygame.draw.line(world, (180, 180, 180), (x, 80), (x, height))
            tick = font.render(str(x), True, (255, 0, 0))
            world.blit(tick, (x - tick.get_width() / 2, 25))
        else:
            pygame.draw.line(world, (255, 0, 0), (x, 0), (x, 10))
    for y in range(0, height, 10):
        if y % 100 == 0 and y != 0:
            pygame.draw.line(world, (255, 0, 0), (0, y), (20, y))
            pygame.draw.line(world, (180, 180, 180), (80, y), (width, y))
            tick = font.render(str(y), True, (255, 0, 0))
            world.blit(tick, (25, y - tick.get_height() / 2))
        else:
            pygame.draw.line(world, (255, 0, 0), (0, y), (10, y))

    return world


# noinspection PyProtectedMember
def iter_world(area: 'ScrollArea') -> Generator:
    """
    Iterate through worlds.

    :param area: Scroll area
    :return: None
    """
    for name in itertools.cycle(WORLDS):
        params = WORLDS[name]
        area._rect.width = params['win'][0]
        area._rect.height = params['win'][1]
        text = LEGEND.format(params['win'][0], params['win'][1],
                             params['size'][0], params['size'][1])
        area.set_world(make_world(params['size'][0],
                                  params['size'][1],
                                  text))
        area.set_position(*params['pos'])
        yield params


def main(test: bool = False) -> None:
    """
    Main function.

    :param test: Indicate function is being tested
    :return: None
    """
    screen = create_example_window('Example - Scrolling Area', (W_SIZE, H_SIZE))
    clock = pygame.time.Clock()

    area = ScrollArea(
        W_SIZE, H_SIZE,
        scrollbars=(
            locals.POSITION_SOUTH,
            locals.POSITION_EAST,
            locals.POSITION_WEST,
            locals.POSITION_NORTH
        )
    )

    worlds = iter_world(area)
    next(worlds)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick
        clock.tick(FPS)

        # Paint background
        screen.fill(COLOR_BACKGROUND)

        pygame.draw.rect(
            screen,
            (20, 89, 20),
            area.get_rect().inflate(20, 20)  # Inflate to see area overflow in case of bug
        )

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    next(worlds)

        area.update(events)
        area.draw(screen)

        # Update surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
