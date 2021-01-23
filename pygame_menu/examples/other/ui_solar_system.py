"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - UI SOLAR SYSTEM
Advanced example with a fancy solar system.

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

import math
import sys
from typing import Dict

sys.path.insert(0, '../../')
sys.path.insert(0, '../../../')

import pygame
import pygame_menu

from pygame_menu.examples import create_example_window
from pygame_menu.examples._resources import SOLAR_SYSTEM_IMG


class Planet(object):
    """
    Planet object.
    """
    image: 'pygame_menu.BaseImage'
    info: str
    name: str
    period: float
    radius: float

    def __init__(self, image: 'pygame_menu.BaseImage', info: str, radius: float, period: float) -> None:
        """
        Create a planet.

        :param image: Planet image
        :param info: Planet info
        :param radius: Rotation radius
        :param period: Rotation period
        """
        self.image = image
        self.info = info
        self.radius = radius
        self.period = period
        self.name = ''


class SolarSystemApp(object):
    """
    Draws a fancy solar system.
    """
    menu: 'pygame_menu.Menu'
    surface: 'pygame.Surface'
    planets: Dict[str, 'Planet']

    def __init__(self) -> None:
        """
        Constructor.
        """
        self.surface = create_example_window('Example - Dynamic Widget Update', (640, 480),
                                             flags=pygame.NOFRAME)

        # Load the SS image
        base_img = pygame_menu.BaseImage(SOLAR_SYSTEM_IMG, frombase64=True)

        # Create planets
        self.planets = {
            'sun': Planet(
                base_img.copy().crop(1, 1, 237, 238),
                "The Sun is the Solar System's star and by far its most massive component. Its large mass "
                "(332,900 Earth masses), which comprises 99.86% of all the mass in the Solar System, produces "
                "temperatures and densities in its core high enough to sustain nuclear fusion of hydrogen into "
                "helium, making it a main-sequence star.[56] This releases an enormous amount of energy, "
                "mostly radiated into space as electromagnetic radiation peaking in visible light.",
                radius=0,
                period=0
            ),
            'mercury': Planet(
                base_img.copy().crop(239, 16, 50, 50),
                "Mercury (0.4 AU from the Sun) is the closest planet to the Sun and on average, all seven other "
                "planets. The smallest planet in the Solar System (0.055 M⊕), Mercury has no natural satellites. "
                "Besides impact craters, its only known geological features are lobed ridges or rupes that were "
                "probably produced by a period of contraction early in its history. Mercury's very tenuous atmosphere "
                "consists of atoms blasted off its surface by the solar wind. Its relatively large iron core and thin "
                "mantle have not yet been adequately explained. Hypotheses include that its outer layers were stripped "
                "off by a giant impact, or that it was prevented from fully accreting by the young Sun's energy.",
                radius=0.4,
                period=0.24
            ),
            'venus': Planet(
                base_img.copy().crop(238, 156, 82, 82),
                "Venus (0.7 AU from the Sun) is close in size to Earth (0.815 M⊕) and, like Earth, has a thick "
                "silicate mantle around an iron core, a substantial atmosphere, and evidence of internal geological "
                "activity. It is much drier than Earth, and its atmosphere is ninety times as dense. Venus has no "
                "natural satellites. It is the hottest planet, with surface temperatures over 400 °C (752 °F), most "
                "likely due to the amount of greenhouse gases in the atmosphere. No definitive evidence of current "
                "geological activity has been detected on Venus, but it has no magnetic field that would prevent "
                "depletion of its substantial atmosphere, which suggests that its atmosphere is being replenished "
                "by volcanic eruptions.",
                radius=0.7,
                period=0.615
            )
        }
        earth = base_img.copy().crop(441, 148, 89, 89)
        moon = base_img.copy().crop(247, 86, 64, 64)
        mars = base_img.copy().crop(535, 170, 69, 69)
        jupyter = base_img.copy().crop(322, 89, 118, 118)
        uranus = base_img.copy().crop(525, 83, 83, 83)
        neptune = base_img.copy().crop(448, 1, 92, 92)

        # Create app theme and menu
        theme = pygame_menu.Theme()
        theme.background_color = (0, 0, 0)

        self.menu = pygame_menu.Menu('Solar System', 640, 480, onclose=pygame_menu.events.EXIT,
                                     theme=theme)

        # Configure planets and add them to the Menu
        for p in self.planets.keys():
            # Configure planet
            self.planets[p].name = str(p).capitalize()
            self.planets[p].image.scale(0.75, 0.75)

            # Create advanced button
            button = self.menu.add_button(self.planets[p].name, None)
            button.set_float()
            button.get_decorator().add_baseimage(0, 0, self.planets[p].image, centered=True)
            button.set_attribute('planet', self.planets[p])

            button.add_draw_callback(self.rotate_planet)

        # Force menu render
        self.menu.render()

    def rotate_planet(self, widget: 'pygame_menu.widgets.Widget', menu: 'pygame_menu.Menu') -> None:
        """
        Rotate a planet.

        :param widget: Widget to rotate
        :param menu: Widget's menu
        :return: None
        """
        t = widget.get_attribute('t', default=math.pi)
        t += menu.get_clock().get_time() * 0.0025
        widget.set_attribute('t', t)

        # Compute position based on radius
        planet: 'Planet' = widget.get_attribute('planet')
        x = planet.radius * math.cos(t) * 100
        y = planet.radius * math.sin(t) * 100
        widget.translate(x, y)

        widget.force_menu_surface_cache_update()

    def mainloop(self, test: bool) -> None:
        """
        App mainloop.

        :param test: Test status
        """
        self.menu.mainloop(self.surface, disable_loop=test)


def main(test: bool = False) -> None:
    """
    Main function.

    :param test: Indicate function is being tested
    :return: None
    """
    app = SolarSystemApp()
    app.mainloop(test)


if __name__ == '__main__':
    main()
