# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - LONG SCROLLING MENU
Shows scrolling in menu.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2020 Pablo Pizarro R. @ppizarror

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

import os
import sys
import itertools
import pygame
from pygameMenu import locals
from pygameMenu.scrollarea import ScrollArea


FPS = 60.0
W_SIZE = 800  # Width of window size
H_SIZE = 600  # Height of window size
COLOR_BACKGROUND = (128, 230, 198)
LEGEND = "Area {}x{}\nWorld {}x{}\nPress [ESC] to change"

WORLDS = {'1': {'pos': (0, 0),
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
          }


def on_button_click(button_id):
    print('Hello from button {}'.format(button_id))


def paint_background(surface):
    surface.fill(COLOR_BACKGROUND)


def make_world(width, height, text=''):
    """
    :param width: Width in pixels
    :param height: Height in pixels
    :return: World surface
    """
    world = pygame.Surface((width, height))  # lgtm [py/call/wrong-arguments]
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


def iter_world(area):
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


def main(test=False):
    """
    Main function
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    clock = pygame.time.Clock()

    # Create window
    screen = pygame.display.set_mode((W_SIZE, H_SIZE))
    pygame.display.set_caption('Example - Scrolling Area')

    area = ScrollArea(W_SIZE,
                      H_SIZE,
                      # scrollbars=(locals.POSITION_SOUTH,
                      #             locals.POSITION_EAST,
                      #             locals.POSITION_WEST,
                      #             locals.POSITION_NORTH)
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
        paint_background(screen)

        pygame.draw.rect(screen,
                         (20, 89, 20),
                         area.get_rect(), 0)

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
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
