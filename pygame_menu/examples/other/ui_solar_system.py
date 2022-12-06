"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - UI SOLAR SYSTEM
Advanced example with a fancy solar system.
"""

__all__ = ['main']

import pygame
import pygame.gfxdraw as gfxdraw
import pygame_menu
from pygame_menu.examples import create_example_window
from pygame_menu.examples._resources import SOLAR_SYSTEM_IMG, NEBULA_IMG

import math
import random
from typing import Dict, Union, Optional, List


class Planet(object):
    """
    Planet object.
    """
    button: Optional['pygame_menu.widgets.Button']
    fontsize: int
    image: 'pygame_menu.BaseImage'
    info: str
    name: str
    period: float
    radius: float
    url: str

    def __init__(
            self,
            image: 'pygame_menu.BaseImage',
            info: str,
            url: str,
            radius: float,
            period: float,
            fontsize: Union[int, float]
    ) -> None:
        """
        Create a planet.

        :param image: Planet image
        :param info: Planet info
        :param url: Info url
        :param radius: Rotation radius
        :param period: Rotation period
        :param fontsize: Button text font size
        """
        self.button = None
        self.fontsize = int(fontsize)
        self.image = image
        self.info = info
        self.name = ''
        self.period = period
        self.radius = radius
        self.url = url


# noinspection SpellCheckingInspection
class SolarSystemApp(object):
    """
    Draws a fancy solar system.
    """
    menu: 'pygame_menu.Menu'
    nebulas: List['pygame_menu.BaseImage']
    planets: Dict[str, 'Planet']
    rotation_velocity: float
    stars: List[List[Union[int, float]]]
    surface: 'pygame.Surface'

    def __init__(self) -> None:
        self.surface = create_example_window('Example - Dynamic Widget Update',
                                             (640, 480), flags=pygame.NOFRAME)

        # Create app theme and menu
        theme = pygame_menu.Theme()

        theme.background_color = (0, 0, 0)
        theme.scrollbar_cursor = pygame_menu.locals.CURSOR_HAND
        theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_TITLE_ONLY
        theme.title_close_button_cursor = pygame_menu.locals.CURSOR_HAND
        theme.title_floating = True
        theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

        # Load the SS image
        base_img = pygame_menu.BaseImage(SOLAR_SYSTEM_IMG, frombase64=True)

        # Create planets
        self.planets = {
            'sun': Planet(
                base_img.copy().crop(1, 1, 237, 238),
                'The Sun is the Solar System\'s star and by far its most massive '
                'component. Its large mass (332,900 Earth masses), which comprises '
                '99.86% of all the mass in the Solar System, produces temperatures '
                'and densities in its core high enough to sustain nuclear fusion '
                'of hydrogen into helium, making it a main-sequence star. This '
                'releases an enormous amount of energy, mostly radiated into space '
                'as electromagnetic radiation peaking in visible light.',
                'https://en.wikipedia.org/wiki/Sun',
                radius=0,
                period=0,
                fontsize=theme.widget_font_size * 1.25
            ),
            'mercury': Planet(
                base_img.copy().crop(239, 16, 50, 50),
                'Mercury (0.4 AU from the Sun) is the closest planet to the Sun '
                'and on average, all seven other planets. The smallest planet in '
                'the Solar System (0.055 Mo), Mercury has no natural satellites. '
                'Besides impact craters, its only known geological features are '
                'lobed ridges or rupes that were probably produced by a period of '
                'contraction early in its history. Mercury\'s very tenuous '
                'atmosphere consists of atoms blasted off its surface by the solar '
                'wind. Its relatively large iron core and thin mantle have not yet '
                'been adequately explained. Hypotheses include that its outer '
                'layers were stripped off by a giant impact, or that it was '
                'prevented from fully accreting by the young Sun\'s energy.',
                'https://en.wikipedia.org/wiki/Mercury_(planet)',
                radius=0.4,
                period=0.24,
                fontsize=theme.widget_font_size * 0.5
            ),
            'venus': Planet(
                base_img.copy().crop(238, 156, 82, 82),
                'Venus (0.7 AU from the Sun) is close in size to Earth (0.815 Mo) '
                'and, like Earth, has a thick silicate mantle around an iron core, '
                'a substantial atmosphere, and evidence of internal geological '
                'activity. It is much drier than Earth, and its atmosphere is '
                'ninety times as dense. Venus has no natural satellites. It is '
                'the hottest planet, with surface temperatures over 400 °C (752 '
                '°F), most likely due to the amount of greenhouse gases in the '
                'atmosphere. No definitive evidence of current geological '
                'activity has been detected on Venus, but it has no magnetic '
                'field that would prevent depletion of its substantial atmosphere, '
                'which suggests that its atmosphere is being replenished by '
                'volcanic eruptions.',
                'https://en.wikipedia.org/wiki/Venus',
                radius=0.7,
                period=0.615,
                fontsize=theme.widget_font_size * 0.6
            ),
            'earth': Planet(
                base_img.copy().crop(441, 148, 89, 89),
                'Earth (1 AU from the Sun) is the largest and densest of the inner '
                'planets, the only one known to have current geological activity, '
                'and the only place where life is known to exist. Its liquid '
                'hydrosphere is unique among the terrestrial planets, and it is '
                'the only planet where plate tectonics has been observed. Earth\'s '
                'atmosphere is radically different from those of the other planets, '
                'having been altered by the presence of life to contain 21% free '
                'oxygen. It has one natural satellite, the Moon, the only large '
                'satellite of a terrestrial planet in the Solar System.',
                'https://en.wikipedia.org/wiki/Earth',
                radius=1,
                period=1,
                fontsize=theme.widget_font_size * 0.85
            ),
            'moon': Planet(
                base_img.copy().crop(247, 86, 64, 64),
                'The Moon is Earth\'s only proper natural satellite. It is one '
                'quarter the diameter of Earth (comparable to the width of '
                'Australia) making it the largest natural satellite in the Solar '
                'System relative to the size of its planet. It is the fifth '
                'largest satellite in the Solar System and is larger than any '
                'dwarf planet. The Moon orbits Earth at an average lunar distance '
                'of 384,400 km (238,900 mi), or 1.28 light-seconds. Its '
                'gravitational influence produces Earth\'s tides and slightly '
                'lengthens Earth\'s day.',
                'https://en.wikipedia.org/wiki/Moon',
                radius=0.35,
                period=0.2,
                fontsize=theme.widget_font_size * 0.5
            ),
            'mars': Planet(
                base_img.copy().crop(535, 170, 69, 69),
                'Mars (1.5 AU from the Sun) is smaller than Earth and Venus (0.107 '
                'Mo). It has an atmosphere of mostly carbon dioxide with a '
                'surface pressure of 6.1 millibars (roughly 0.6% of that of Earth'
                '). Its surface, peppered with vast volcanoes, such as Olympus '
                'Mons, and rift valleys, such as Valles Marineris, shows '
                'geological activity that may have persisted until as recently '
                'as 2 million years ago. Its red colour comes from iron oxide '
                '(rust) in its soil. Mars has two tiny natural satellites (Deimos '
                'and Phobos) thought to be either captured asteroids, or ejected '
                'debris from a massive impact early in Mars\'s history.',
                'https://en.wikipedia.org/wiki/Mars',
                radius=1.25,
                period=1.880,
                fontsize=theme.widget_font_size * 0.95
            ),
            'jupiter': Planet(
                base_img.copy().crop(322, 89, 118, 118),
                'Jupiter (5.2 AU), at 318 Mo, is 2.5 times the mass of all the '
                'other planets put together. It is composed largely of hydrogen '
                'and helium. Jupiter\'s strong internal heat creates semi-permanent '
                'features in its atmosphere, such as cloud bands and the Great '
                'Red Spot. Jupiter has 79 known satellites. The four largest, '
                'Ganymede, Callisto, Io, and Europa, show similarities to the '
                'terrestrial planets, such as volcanism and internal heating. '
                'Ganymede, the largest satellite in the Solar System, is larger '
                'than Mercury.',
                'https://en.wikipedia.org/wiki/Jupiter',
                radius=1.75,
                period=11.862,
                fontsize=theme.widget_font_size * 1.1
            ),
            'uranus': Planet(
                base_img.copy().crop(525, 83, 83, 83),
                'Uranus (19.2 AU), at 14 Mo, is the lightest of the outer '
                'planets. Uniquely among the planets, it orbits the Sun on its '
                'side; its axial tilt is over ninety degrees to the ecliptic. It '
                'has a much colder core than the other giant planets and radiates '
                'very little heat into space. Uranus has 27 known satellites, the '
                'largest ones being Titania, Oberon, Umbriel, Ariel, and Miranda.',
                'https://en.wikipedia.org/wiki/Uranus',
                radius=2,
                period=84.0205,
                fontsize=theme.widget_font_size
            ),
            'neptune': Planet(
                base_img.copy().crop(448, 1, 92, 92),
                'Neptune (30.1 AU), though slightly smaller than Uranus, is more '
                'massive (17 Mo) and hence more dense. It radiates more internal '
                'heat, but not as much as Jupiter or Saturn. Neptune has 14 known '
                'satellites. The largest, Triton, is geologically active, with '
                'geysers of liquid nitrogen. Triton is the only large satellite '
                'with a retrograde orbit. Neptune is accompanied in its orbit by '
                'several minor planets, termed Neptune trojans, that are in 1:1 '
                'resonance with it.',
                'https://en.wikipedia.org/wiki/Neptune',
                radius=2.25,
                period=164.8,
                fontsize=theme.widget_font_size
            ),
        }

        self.menu = pygame_menu.Menu('Solar System', 640, 480,
                                     onclose=pygame_menu.events.EXIT,
                                     theme=theme, mouse_motion_selection=True)

        # Configure planets and add them to the Menu
        for p in self.planets.keys():
            planet: 'Planet' = self.planets[p]

            # Configure planet
            planet.name = str(p).capitalize()

            # Create submenu for given planet
            submenu = pygame_menu.Menu(planet.name + ' Info', 640, 480, theme=theme,
                                       mouse_motion_selection=True, center_content=False)
            submenu_area_deco = submenu.get_scrollarea().get_decorator()
            submenu_area_deco.add_callable(self.draw_universe_background)

            # Add go back button with a background image
            submenu.add.vertical_margin(150)
            go_back = submenu.add.button('Back to Menu', pygame_menu.events.BACK, cursor=pygame_menu.locals.CURSOR_HAND)
            go_back_img = planet.image.copy().resize(150, 150)
            # Get color from figure's center pixel
            go_back_color = go_back_img.get_at((100, 100), ignore_alpha=True)
            go_back.get_decorator().add_baseimage(0, 0, go_back_img, centered=True)
            go_back_selection = pygame_menu.widgets.HighlightSelection(border_width=2)
            go_back.set_selection_effect(go_back_selection.set_color(go_back_color))

            # Description
            submenu.add.vertical_margin(75)
            submenu.add.label('Description', align=pygame_menu.locals.ALIGN_LEFT,
                              font_name=pygame_menu.font.FONT_OPEN_SANS_BOLD,
                              margin=(5, 10))
            label = submenu.add.label(planet.info, max_char=70,
                                      align=pygame_menu.locals.ALIGN_LEFT,
                                      margin=(29, 1), font_size=20,
                                      font_name=pygame_menu.font.FONT_PT_SERIF,
                                      font_color=(255, 255, 255), padding=0)
            for line in label:
                line.set_max_width(565)
            submenu.add.url(planet.url, align=pygame_menu.locals.ALIGN_LEFT,
                            margin=(20, 1), font_size=20,
                            font_name=pygame_menu.font.FONT_PT_SERIF)
            submenu.add.vertical_margin(40)  # Bottom margin

            # Create advanced button
            planet.image.scale(0.35, 0.35)
            button = self.menu.add.button(planet.name, submenu,
                                          font_size=planet.fontsize)
            button.set_cursor(pygame_menu.locals.CURSOR_HAND)
            button.set_float()
            button.get_decorator().add_baseimage(0, 2, planet.image, centered=True)
            button.set_attribute('planet', planet)
            button.add_draw_callback(self.rotate_planet)
            button_selection = pygame_menu.widgets.LeftArrowSelection(arrow_size=(20, 30), blink_ms=1000)
            button.set_selection_effect(button_selection.set_color(go_back_color))

            # Set random times
            button.set_attribute('t', random.random() * 2 * math.pi)

            # Save button reference to object
            planet.button = button

        # Add draw stars as Menu's decoration
        self.menu.get_scrollarea().get_decorator().add_callable(self.draw_universe_background)

        # Set update event
        self.menu.set_onupdate(self.process_events)

        # Initialize stars random colors
        self.stars = []
        for i in range(100):
            self.add_star()

        # Set the nebulas
        nebula = pygame_menu.BaseImage(NEBULA_IMG, frombase64=True,
                                       drawing_mode=pygame_menu.baseimage.IMAGE_MODE_SIMPLE)
        self.nebulas = [
            nebula.copy().set_drawing_offset((150, 400)).scale2x().set_alpha(25),
            nebula.copy().set_drawing_offset((500, 50)).scale(3, 3).rotate(90).set_alpha(50).pick_channels('b'),
            nebula.copy().set_drawing_offset((50, 100)).scale2x().rotate(175).set_alpha(75).pick_channels('r')
        ]
        for nebula in self.nebulas:
            nebula.set_drawing_position(pygame_menu.locals.POSITION_CENTER)
            nebula.checkpoint()  # Because rotation method works from checkpointed surface
            nebula.set_attribute('delta_angle', 0.25 * random.randint(-1, 1) * random.random())

        # Add shooting stars
        self.shooting_stars = []
        for i in range(3):
            self.add_shooting_star()

        # Update values
        self.rotation_velocity = 0.0003

    def add_shooting_star(self) -> None:
        """
        Add a new shooting star to the simulation.
        """
        dx = random.randrange(-25, 25) * random.random()
        dy = random.randrange(-25, 25) * random.random()
        angle = math.atan2(dy, dx)
        self.shooting_stars.append([
            random.randrange(1, self.menu.get_width()),  # x position
            random.randrange(1, self.menu.get_height()),  # y position
            int(dx),
            int(dy),
            angle,
            random.randrange(1, 5),  # speed
            2 * math.pi * random.random()  # initial flickering
        ])

    def add_star(self) -> None:
        """
        Add a new star to the simulation.
        """
        self.stars.append([
            random.randrange(1, self.menu.get_width()),  # x position
            random.randrange(1, self.menu.get_height()),  # y position
            2 * math.pi * random.random()  # initial flickering
        ])

    # noinspection PyUnusedLocal
    def draw_universe_background(self, surface: 'pygame.Surface', *args) -> None:
        """
        Draw stars as background.

        :param surface: Surface to draw
        :param args: Optional arguments
        """
        t = self.menu.get_counter_attribute('t', self.menu.get_clock().get_time() * 0.001)

        # Draw nebulas
        for nebula in self.nebulas:
            nebula.draw(surface)
            nebula.rotate(nebula.get_angle() + nebula.get_attribute('delta_angle'))

        # Draw stars
        for s in self.stars:
            x, y, flicker = s
            c = int(127 * max(0.5, 1 + math.cos(t + flicker)))
            gfxdraw.pixel(surface, x, y, (c, c, c))

        # Draw shooting stars
        for s in self.shooting_stars:
            x, y, dx, dy, theta, speed, flicker = s
            c = int(150 * max(0.1, max(math.sin(0.1 * t + 1.5 * math.pi + flicker),
                                       math.cos(0.1 * t + flicker))))
            x = int(x)
            y = int(y)
            gfxdraw.line(surface, x, y, x + dx, y + dy, (c, c, c))

            # Update velocity + window constraints
            s[0] = (s[0] + speed * math.cos(theta)) % self.menu.get_width()
            s[1] = (s[1] + speed * math.sin(theta)) % self.menu.get_height()

        # This line forces cache update for submenus that call this method
        self.menu.force_surface_cache_update()

    # noinspection PyProtectedMember
    def process_events(self, events: List['pygame.event.Event'], menu: 'pygame_menu.Menu') -> None:
        """
        Process events from user.

        :param events: Events
        :param menu: Menu
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu._disable_draw = not menu._disable_draw
                elif event.key == pygame.K_q:
                    if not menu._disable_draw:
                        self.rotation_velocity += 5e-5
                elif event.key == pygame.K_e:
                    if not menu._disable_draw:
                        self.rotation_velocity = max(0.0, self.rotation_velocity - 5e-5)
                elif event.key == pygame.K_s:
                    if not menu._disable_draw:
                        self.add_star()
                elif event.key == pygame.K_c:
                    if not menu._disable_draw:
                        self.add_shooting_star()

    def rotate_planet(self, widget: 'pygame_menu.widgets.Widget', menu: 'pygame_menu.Menu') -> None:
        """
        Rotate a planet.

        :param widget: Widget to rotate
        :param menu: Widget's menu
        """
        # Get planet from attributes
        planet: 'Planet' = widget.get_attribute('planet')

        # Update time from attribute
        t = widget.get_attribute('t')
        if planet.period != 0:
            t -= menu.get_clock().get_time() * self.rotation_velocity / planet.period
        widget.set_attribute('t', t)
        radius_factor = 110  # Visual only

        x = planet.radius * math.cos(t) * radius_factor
        y = planet.radius * math.sin(t) * radius_factor

        # Compute position based on radius
        if planet.name == 'Moon':
            xc, yc = self.planets['earth'].button.get_attribute('pos')  # Center of earth
            x += xc + 1
            y += yc - 10

        # Visual offset
        if planet.name != 'Sun':
            y += 15

        widget.translate(x, y)
        widget.set_attribute('pos', (x, y))
        widget.force_menu_surface_cache_update()

    def mainloop(self, test: bool) -> None:
        """
        App mainloop.

        :param test: Test status
        """
        print('Press ESC to close the app')
        print('Press P to pause the planets')
        print('Press E to increase the rotation velocity')
        print('Press Q to decrease the rotation velocity')
        print('Press S to add a new star')
        print('Press C to add a new shooting star')
        self.menu.mainloop(self.surface, disable_loop=test)


def main(test: bool = False) -> 'SolarSystemApp':
    """
    Main function.

    :param test: Indicate function is being tested
    :return: App
    """
    app = SolarSystemApp()
    app.mainloop(test)
    return app


if __name__ == '__main__':
    main()
