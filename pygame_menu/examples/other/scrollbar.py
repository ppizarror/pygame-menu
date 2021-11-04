"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - USE SCROLLBAR WIDGET
Shows how the ScrollBar can be used on a surface.
"""

__all__ = ['main']

import pygame
import pygame_menu

from pygame_menu.examples import create_example_window
from pygame_menu.utils import make_surface
from pygame_menu.widgets import ScrollBar


def make_world(width: int, height: int) -> 'pygame.Surface':
    """
    Create a test surface.

    :param width: Width in pixels
    :param height: Height in pixels
    :return: World surface
    """
    world = make_surface(width, height)
    world.fill((200, 200, 200))

    color = [70, 20, 20]
    max_x = len(list(range(100, width, 200)))
    max_y = len(list(range(100, height, 200)))
    number_x = 0
    for x in range(100, width, 200):
        number_y = 0
        for y in range(100, height, 200):
            if number_x in (0, max_x - 1) or number_y in (0, max_y - 1):
                # White circles to delimit world boundaries
                # noinspection PyArgumentList
                pygame.draw.circle(world, (255, 255, 255), (x, y), 100, 10)
            else:
                # noinspection PyArgumentList
                pygame.draw.circle(world, color, (x, y), 100, 10)
                if color[0] + 15 < 255:
                    color[0] += 15
                elif color[1] + 15 < 255:
                    color[1] += 15
                else:
                    color[2] += 15
            number_y += 1
        number_x += 1

    return world


def h_changed(value: int) -> None:
    """
    :param value: Value data
    """
    print('Horizontal position changed:', value)


def v_changed(value: int) -> None:
    """
    :param value: Value data
    """
    print('Vertical position changed:', value)


def main(test: bool = False) -> None:
    """
    Main function.

    :param test: Indicate function is being tested
    :return: None
    """
    scr_size = (480, 480)
    screen = create_example_window('Example - Scrollbar', scr_size)
    world = make_world(int(scr_size[0] * 4), scr_size[1] * 3)
    screen.fill((120, 90, 130))

    thick_h = 20
    thick_v = 40

    # Horizontal ScrollBar
    sb_h = ScrollBar(
        length=scr_size[0] - thick_v,
        values_range=(50, world.get_width() - scr_size[0] + thick_v),
        slider_pad=2,
        page_ctrl_thick=thick_h,
        onchange=h_changed
    )
    sb_h.set_shadow(
        color=(0, 0, 0),
        position=pygame_menu.locals.POSITION_SOUTHEAST
    )
    sb_h.set_controls(False)
    sb_h.set_position(0, scr_size[1] - thick_h)
    sb_h.set_page_step(scr_size[0] - thick_v)

    # Vertical ScrollBar
    sb_v = ScrollBar(
        length=scr_size[1] - thick_h,
        values_range=(0, world.get_height() - scr_size[1] + thick_h),
        orientation=pygame_menu.locals.ORIENTATION_VERTICAL,
        slider_pad=6,
        slider_color=(135, 193, 180),
        slider_hover_color=(180, 180, 180),
        page_ctrl_thick=thick_v,
        page_ctrl_color=(253, 246, 220),
        onchange=v_changed
    )
    sb_v.set_shadow(
        color=(52, 54, 56),
        position=pygame_menu.locals.POSITION_NORTHWEST,
        offset=4
    )
    sb_v.set_controls(False)
    sb_v.set_position(scr_size[0] - thick_v, 0)
    sb_v.set_page_step(scr_size[1] - thick_h)
    clock = pygame.time.Clock()

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Clock tick
        clock.tick(60)

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                sb_h.set_value(100)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_v:
                sb_v.set_value(200)

            sb_h.update([event])
            sb_h.draw(screen)
            sb_v.update([event])
            sb_v.draw(screen)

        trunc_world_orig = (sb_h.get_value(), sb_v.get_value())
        trunc_world = (scr_size[0] - thick_v, scr_size[1] - thick_h)

        # noinspection PyTypeChecker
        screen.blit(world, (0, 0), (trunc_world_orig, trunc_world))
        pygame.display.update()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
