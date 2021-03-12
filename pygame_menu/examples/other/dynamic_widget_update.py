"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - DYNAMIC WIDGET UPDATE
Dynamically updates the widgets based on user events.

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

import math
from typing import Dict, Any


class App(object):
    """
    The following object creates the whole app.
    """
    image_widget: 'pygame_menu.widgets.Image'
    item_description_widget: 'pygame_menu.widgets.Label'
    menu: 'pygame_menu.Menu'
    modes: Dict[int, Dict[str, Any]]
    quit_button: 'pygame_menu.widgets.Button'
    quit_button_fake: 'pygame_menu.widgets.Button'
    selector_widget: 'pygame_menu.widgets.Selector'
    surface: 'pygame.Surface'

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.surface = create_example_window('Example - Dynamic Widget Update',
                                             (640, 480), flags=pygame.NOFRAME)

        # Load image
        default_image = pygame_menu.BaseImage(
            image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU
        ).scale(0.2, 0.2)

        # Set theme
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE_TITLE
        theme.title_close_button_cursor = pygame_menu.locals.CURSOR_HAND
        theme.title_font_color = (35, 35, 35)

        # This dict stores the values of the widgets to be changed dynamically
        self.modes = {
            1: {
                'image': default_image.copy(),
                'label': {
                    'color': theme.widget_font_color,
                    'size': theme.widget_font_size,
                    'text': 'The first one is very epic'
                }
            },
            2: {
                'image': default_image.copy().to_bw(),
                'label': {
                    'color': (0, 0, 0),
                    'size': 20,
                    'text': 'This other one is also epic, but fancy'
                }
            },
            3: {
                'image': default_image.copy().flip(False, True).pick_channels('r'),
                'label': {
                    'color': (255, 0, 0),
                    'size': 45,
                    'text': 'YOU D I E D'
                }
            }
        }

        # Create menus
        self.menu = pygame_menu.Menu(
            height=480,
            onclose=pygame_menu.events.CLOSE,
            theme=theme,
            title='Everything is dynamic now',
            width=640
        )

        self.selector_widget = self.menu.add.selector(
            title='Pick one option: ',
            items=[('The first', 1),
                   ('The second', 2),
                   ('The final mode', 3)],
            onchange=self._on_selector_change
        )

        self.image_widget = self.menu.add.image(
            image_path=self.modes[1]['image'],
            padding=(25, 0, 0, 0)  # top, right, bottom, left
        )

        self.item_description_widget = self.menu.add.label(title='')

        self.quit_button = self.menu.add.button('Quit', pygame_menu.events.EXIT)

        self.quit_button_fake = self.menu.add.button('You cannot quit', self.fake_quit,
                                                     font_color=(255, 255, 255))
        self.quit_button_fake.add_draw_callback(self.animate_quit_button)

        # Update the widgets based on selected value from selector get_value
        # returns selected item tuple and index, so [0][1] means the second object
        # from ('The first', 1) tuple
        self._update_from_selection(int(self.selector_widget.get_value()[0][1]))

    def animate_quit_button(
            self,
            widget: 'pygame_menu.widgets.Widget',
            menu: 'pygame_menu.Menu'
    ) -> None:
        """
        Animate widgets if the last option is selected.

        :param widget: Widget to be updated
        :param menu: Menu
        :return: None
        """
        if self.current == 3:
            t = widget.get_counter_attribute('t', menu.get_clock().get_time() * 0.0075, math.pi)
            widget.set_padding(10 * (1 + math.sin(t)))  # Oscillating padding
            widget.set_background_color((int(125 * (1 + math.sin(t))), 0, 0), None)
            c = int(127 * (1 + math.cos(t)))
            widget.update_font({'color': (c, c, c)})  # Widget font now is in grayscale
            # widget.translate(10 * math.cos(t), 10 * math.sin(t))
            widget.rotate(5 * t)

    @staticmethod
    def fake_quit() -> None:
        """
        Function executed by fake quit button.

        :return: None
        """
        print('I said that you cannot quit')

    def _update_from_selection(self, index: int) -> None:
        """
        Change widgets depending on index.

        :param index: Index
        :return: None
        """
        self.current = index
        self.image_widget.set_image(self.modes[index]['image'])
        self.item_description_widget.set_title(self.modes[index]['label']['text'])
        self.item_description_widget.update_font(
            {'color': self.modes[index]['label']['color'],
             'size': self.modes[index]['label']['size']}
        )
        # Swap buttons using hide/show
        if index == 3:
            self.quit_button.hide()
            self.quit_button_fake.show()
        else:
            self.quit_button.show()
            self.quit_button_fake.hide()

    def _on_selector_change(self, selected: Any, value: int) -> None:
        """
        Function executed if selector changes.

        :param selected: Selector data containing text and index
        :param value: Value from the selected option
        :return: None
        """
        print('Selected data:', selected)
        self._update_from_selection(value)

    def mainloop(self, test: bool) -> None:
        """
        App mainloop.

        :param test: Test status
        """
        self.menu.mainloop(self.surface, disable_loop=test)


def main(test: bool = False) -> 'App':
    """
    Main function.

    :param test: Indicate function is being tested
    :return: App object
    """
    app = App()
    app.mainloop(test)
    return app


if __name__ == '__main__':
    main()
