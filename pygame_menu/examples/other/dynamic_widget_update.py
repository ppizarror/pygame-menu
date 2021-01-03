# coding=utf-8
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
import sys

sys.path.insert(0, '../../')

import pygame_menu
import pygame
import os


class App(object):
    """
    The following object creates the whole app.
    """

    def __init__(self):
        """
        Constructor.
        """

        # Start pygame
        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.surface = pygame.display.set_mode((640, 480), flags=pygame.NOFRAME)

        # Load image
        default_image = pygame_menu.baseimage.BaseImage(
            image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU
        ).scale(0.2, 0.2)

        # Set theme
        theme = pygame_menu.themes.THEME_DEFAULT

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

        self.selector_widget = self.menu.add_selector(
            title='Pick one option: ',
            items=[('The first', 1),
                   ('The second', 2),
                   ('The final mode', 3)],
            onchange=self._on_selector_change
        )  # type: pygame_menu.widgets.Selector

        self.image_widget = self.menu.add_image(
            image_path=self.modes[1]['image'],
            padding=(25, 0, 0, 0)  # top, right, bottom, left
        )  # type: pygame_menu.widgets.Image

        self.item_description_widget = self.menu.add_label(title='')  # type: pygame_menu.widgets.Label

        self.quit_button = self.menu.add_button('Quit', pygame_menu.events.EXIT)
        self.quit_button_fake = self.menu.add_button('You cannot quit', self.fake_quit)

        # Update the widgets based on selected value from selector
        # get_value returns selected item tuple and index, so [0][1] means the second object from ('The first', 1) tuple
        self._update_from_selection(self.selector_widget.get_value()[0][1])

    @staticmethod
    def fake_quit():
        """
        Function executed by fake quit button.

        :return: None
        """
        print('I said that you cannot quit')

    def _update_from_selection(self, index):
        """
        Change widgets depending on index.

        :param index: Index
        :type index: int
        :return: None
        """
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

    def _on_selector_change(self, selected, value):
        """
        Function executed if selector changes.

        :param selected: Selector data (tuple) containing text and index
        :type selected: tuple
        :param value: Value from the selected option
        :type value: int
        :return: None
        """
        print('Selected data:', selected)
        self._update_from_selection(value)

    def mainloop(self, test):
        """
        App mainloop.

        :param test: Test status
        :type test: bool
        """
        self.menu.mainloop(self.surface, disable_loop=test)


def main(test=False):
    """
    Main function.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """
    app = App()
    app.mainloop(test)


if __name__ == '__main__':
    main()
