"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - MAZE
Maze solver app, an improved version from https://github.com/ChrisKneller/pygame-pathfinder.
License: GNU General Public License v3.0
"""

__all__ = ['MazeApp']

import heapq
import pygame
import pygame_menu
import pygame_menu.utils as ut
import random
import time

from collections import deque
from math import inf
from typing import List, Union, Optional, Tuple, Any, Generator

from pygame_menu.examples import create_example_window

# Define some colors
BACKGROUND = (34, 40, 44)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (186, 127, 50)
DARK_BLUE = (0, 0, 128)
DARK_GREEN = (0, 128, 0)
GREEN = (0, 255, 0)
GREY = (143, 143, 143)
LIGHT_BLUE = (0, 111, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


# noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
class AStarQueue(object):
    """
    A* Queue.
    """

    def __init__(self):
        self.myheap = []

    def show(self):
        return self.myheap

    def push(self, priority, distance, node):
        heapq.heappush(self.myheap, (priority, distance, node))

    def pop(self):
        priority, distance, node = heapq.heappop(self.myheap)
        return priority, distance, node


# noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
class PriorityQueue(object):
    """
    Priority Queue.
    """

    def __init__(self):
        self.myheap = []

    def show(self):
        return self.myheap

    def push(self, priority, node):
        heapq.heappush(self.myheap, (priority, node))

    def pop(self):
        priority, node = heapq.heappop(self.myheap)
        return priority, node


# noinspection PyMissingTypeHints,PyMissingOrEmptyDocstring
class PrioritySet(object):
    """
    Create a priority queue that doesn't add duplicate nodes.
    """

    def __init__(self):
        self.myheap = []
        self.myset = set()

    def show(self):
        return self.myheap

    def push(self, priority, node):
        if node not in self.myset:
            heapq.heappush(self.myheap, (priority, node))
            self.myset.add(node)

    def pop(self):
        priority, node = heapq.heappop(self.myheap)
        self.myset.remove(node)
        return priority, node


# noinspection PyDefaultArgument
class Node(object):
    """
    Make it easier to add different node types.
    """
    nodetypes = ['blank', 'start', 'end', 'wall', 'mud', 'dormant']

    colors = {
        'regular': {'blank': WHITE, 'start': RED, 'end': LIGHT_BLUE, 'wall': BLACK, 'mud': BROWN, 'dormant': GREY},
        'visited': {'blank': GREEN, 'start': RED, 'end': LIGHT_BLUE, 'wall': BLACK, 'mud': DARK_GREEN, 'dormant': GREY},
        'path': {'blank': BLUE, 'start': RED, 'end': LIGHT_BLUE, 'wall': BLACK, 'mud': DARK_BLUE, 'dormant': GREY}
    }

    distance_modifiers = {'blank': 1, 'start': 1, 'end': 1, 'wall': inf, 'mud': 3, 'dormant': inf}

    def __init__(self, nodetype: str, colors: dict = colors, dmf: dict = distance_modifiers) -> None:
        """
        Constructor.

        :param nodetype: Node type
        :param colors: Colors
        :param dmf: Distance modifier
        """
        self.nodetype = nodetype
        self.rcolor = colors['regular'][self.nodetype]
        self.vcolor = colors['visited'][self.nodetype]
        self.pcolor = colors['path'][self.nodetype]
        self.is_visited = True if nodetype == 'start' else True if nodetype == 'end' else False
        self.is_path = True if nodetype == 'start' else True if nodetype == 'end' else False
        self.distance_modifier = dmf[self.nodetype]
        self.color = self.pcolor if self.is_path else self.vcolor if self.is_visited else self.rcolor

    def update(
            self,
            nodetype: Union[bool, str] = False,
            is_visited: Union[bool, str] = 'unchanged',
            is_path: Union[bool, str] = 'unchanged',
            colors: dict = colors,
            dmf: dict = distance_modifiers,
            nodetypes: dict = nodetypes
    ) -> None:
        """
        Update the node.
        """
        if nodetype:
            assert nodetype in nodetypes, f"nodetype must be one of: {nodetypes}"
            if (self.nodetype == ('start' or 'end')) and (nodetype == ('wall' or 'mud')):
                pass
            else:
                self.nodetype = nodetype

        if is_visited != 'unchanged':
            assert type(is_visited) == bool, "'is_visited' must be boolean: True or False"
            self.is_visited = is_visited

        if is_path != 'unchanged':
            assert type(is_path) == bool, "'is_path' must be boolean: True or False"
            self.is_path = is_path

        self.rcolor = colors['regular'][self.nodetype]
        self.vcolor = colors['visited'][self.nodetype]
        self.pcolor = colors['path'][self.nodetype]
        self.distance_modifier = dmf[self.nodetype]
        self.color = self.pcolor if self.is_path else self.vcolor if self.is_visited else self.rcolor


_MazeType = List[List['Node']]
_Point2 = Tuple[int, int]


class MazeApp(object):
    """
    Maze class.
    """

    _algorithms: dict
    _diagonals: bool
    _end_point: _Point2
    _grid: _MazeType
    _height: int
    _margin: int
    _menu: 'pygame_menu.Menu'
    _mouse_drag: bool
    _offset: _Point2
    _rows: int
    _start_point: _Point2
    _visualize: bool
    _width: int

    def __init__(
            self,
            width: int = 8,
            rows: int = 75,
            margin: int = 0
    ) -> None:
        """
        Creates the maze.

        :param width: Width of each cell
        :param rows: Number of rows
        :param margin: Margin between cells
        """
        # Create the maze
        self._height = width  # so they are squares
        self._margin = margin
        self._offset = (25, 25)  # Maze offset within window
        self._width = width

        # Create a 2 dimensional array (a list of lists)
        self._grid = []
        self._rows = rows
        self._screen_width = self._rows * (self._width + self._margin) + self._margin * 2

        # Iterate through every row and column, adding blank nodes
        for row in range(rows):
            self._grid.append([])
            for column in range(rows):
                self._grid[row].append(Node('blank'))

        # Set start and end points for the pathfinder
        self._start_point = (random.randrange(2, rows - 1, 2) - 1, random.randrange(2, rows - 1, 2) - 1)
        self._end_point = (random.randrange(2, rows - 1, 2), random.randrange(2, rows - 1, 2))

        self._diagonals = True
        self._visualize = False

        # Used for handling click & drag
        self._mouse_drag = False
        self._drag_start_point = False
        self._drag_end_point = False

        # Used for deciding what to do in different situations
        self._algorithm_run = False
        self._algorithms = {0: 'dijkstra', 1: 'astar', 2: 'dfs', 3: 'bfs'}
        self._path_found = False

        # Create the window
        self._clock = pygame.time.Clock()
        self._fps = 60
        self._surface = create_example_window('Example - Maze', (900, 650))

        # Setups the menu
        self._setup_menu()

    def _setup_menu(self) -> None:
        """
        Setups the menu.
        """

        # Creates the events
        # noinspection PyUnusedLocal
        def onchange_dropselect(*args) -> None:
            """
            Called if the select is changed.
            """
            b = self._menu.get_widget('run_generator')
            b.readonly = False
            b.is_selectable = True
            b.set_cursor(pygame_menu.locals.CURSOR_HAND)

        def button_onmouseover(w: 'pygame_menu.widgets.Widget', _) -> None:
            """
            Set the background color of buttons if entered.
            """
            if w.readonly:
                return
            w.set_background_color((98, 103, 106))

        def button_onmouseleave(w: 'pygame_menu.widgets.Widget', _) -> None:
            """
            Set the background color of buttons if leaved.
            """
            w.set_background_color((75, 79, 81))

        def button_onmouseover_clear(w: 'pygame_menu.widgets.Widget', _) -> None:
            """
            Set the background color of buttons if entered.
            """
            if w.readonly:
                return
            w.set_background_color((139, 0, 0))

        def button_onmouseleave_clear(w: 'pygame_menu.widgets.Widget', _) -> None:
            """
            Set the background color of buttons if leaved.
            """
            w.set_background_color((205, 92, 92))

        def _visualize(value: bool) -> None:
            """
            Changes visualize.
            """
            self._visualize = value

        def _diagonals(value: bool) -> None:
            """
            Changes diagonals
            """
            self._diagonals = value
            if self._algorithm_run:
                self._path_found = self._update_path()

        theme = pygame_menu.Theme(
            background_color=pygame_menu.themes.TRANSPARENT_COLOR,
            title=False,
            widget_font=pygame_menu.font.FONT_FIRACODE,
            widget_font_color=(255, 255, 255),
            widget_margin=(0, 15),
            widget_selection_effect=pygame_menu.widgets.NoneSelection()
        )
        self._menu = pygame_menu.Menu(
            height=self._screen_width,
            mouse_motion_selection=True,
            position=(645, 25, False),
            theme=theme,
            title='',
            width=240
        )

        self._menu.add.toggle_switch(
            'Visualize',
            self._visualize,
            font_size=20,
            margin=(0, 5),
            onchange=_visualize,
            state_text_font_color=((0, 0, 0), (0, 0, 0)),
            state_text_font_size=15,
            switch_margin=(15, 0),
            width=80
        )
        self._menu.add.toggle_switch(
            'Diagonals',
            self._diagonals,
            font_size=20,
            margin=(0, 30),
            onchange=_diagonals,
            state_text_font_color=((0, 0, 0), (0, 0, 0)),
            switch_margin=(15, 0),
            toggleswitch_id='diagonals',
            width=80
        )

        self._menu.add.label(
            'Maze generator',
            font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
            font_size=22,
            margin=(0, 5)
        ).translate(-12, 0)
        self._menu.add.dropselect(
            title='',
            items=[('Prim', 0),
                   ('Alt Prim', 1),
                   ('Recursive', 2),
                   ('(+) Terrain', 3)],
            dropselect_id='generator',
            font_size=16,
            onchange=onchange_dropselect,
            padding=0,
            placeholder='Select one',
            selection_box_height=5,
            selection_box_inflate=(0, 20),
            selection_box_margin=0,
            selection_box_text_margin=10,
            selection_box_width=200,
            selection_option_font_size=20,
            shadow_width=20
        )
        self._menu.add.vertical_margin(10)
        btn = self._menu.add.button(
            'Run Generator',
            self._run_generator,
            button_id='run_generator',
            font_size=20,
            margin=(0, 30),
            shadow_width=10,
        )
        btn.readonly = True
        btn.is_selectable = False

        self._menu.add.label(
            'Maze Solver',
            font_name=pygame_menu.font.FONT_FIRACODE_BOLD,
            font_size=22,
            margin=(0, 5)
        ).translate(-30, 0)
        self._menu.add.dropselect(
            title='',
            items=[('Dijkstra', 0),
                   ('A*', 1),
                   ('DFS', 2),
                   ('BFS', 3)],
            default=0,
            dropselect_id='solver',
            font_size=16,
            padding=0,
            placeholder='Select one',
            selection_box_height=5,
            selection_box_inflate=(0, 20),
            selection_box_margin=0,
            selection_box_text_margin=10,
            selection_box_width=200,
            selection_option_font_size=20,
            shadow_width=20
        )
        self._menu.add.vertical_margin(10)
        self._menu.add.button(
            'Run Solver',
            self._run_solver,
            button_id='run_solver',
            cursor=pygame_menu.locals.CURSOR_HAND,
            font_size=20,
            margin=(0, 75),
            shadow_width=10,
        )

        # Clears
        btn = self._menu.add.button(
            'Clear',
            self._clear_maze,
            background_color=(205, 92, 92),
            button_id='clear',
            cursor=pygame_menu.locals.CURSOR_HAND,
            font_size=20,
            margin=(0, 30),
            shadow_width=10,
        )
        btn.set_onmouseover(button_onmouseover_clear)
        btn.set_onmouseleave(button_onmouseleave_clear)
        btn.translate(-50, 0)

        # Create about menu
        menu_about = pygame_menu.Menu(
            height=self._screen_width + 20,
            mouse_motion_selection=True,
            position=(645, 8, False),
            theme=theme,
            title='',
            width=240
        )
        menu_about.add.label('pygame-menu\nMaze', font_name=pygame_menu.font.FONT_FIRACODE_BOLD, font_size=25,
                             margin=(0, 5))
        menu_about.add.vertical_margin(10)
        text = 'Left click to create a wall or move the start and end points.\n' \
               'Hold left CTRL and left click to create a sticky mud patch (whi' \
               'ch reduces movement speed to 1/3).\n'
        text += 'The point of these mud patches is to showcase Dijkstra\'s algor' \
                'ithm (first) and A* (second) by adjusting the "distances" betwe' \
                'en the nodes.\n\n'
        text += 'After a pathfinding algorithm has been run you can drag the sta' \
                'rt/end points around and see the visualisation update instantly' \
                ' for the new path using the algorithm that was last run.\n'
        menu_about.add.label(text, font_name=pygame_menu.font.FONT_FIRACODE, font_size=12,
                             margin=(0, 5), max_char=-1, padding=0)
        menu_about.add.label('License: GNU GPL v3.0', margin=(0, 5),
                             font_name=pygame_menu.font.FONT_FIRACODE, font_size=12)
        menu_about.add.url('https://github.com/ChrisKneller/pygame-pathfinder', 'ChrisKneller/pygame-pathfinder',
                           font_name=pygame_menu.font.FONT_FIRACODE, font_size=12,
                           font_color='#00bfff')
        menu_about.add.vertical_margin(20)
        menu_about.add.button(
            'Back',
            pygame_menu.events.BACK,
            button_id='about_back',
            cursor=pygame_menu.locals.CURSOR_HAND,
            font_size=20,
            shadow_width=10
        )

        btn = self._menu.add.button(
            'About',
            menu_about,
            button_id='about',
            float=True,
            font_size=20,
            margin=(0, 75),
            shadow_width=10
        )
        btn.translate(50, 0)

        # Configure buttons
        for btn in self._menu.get_widgets(['run_generator', 'run_solver', 'about', 'about_back']):
            btn.set_onmouseover(button_onmouseover)
            btn.set_onmouseleave(button_onmouseleave)
            if not btn.readonly:
                btn.set_cursor(pygame_menu.locals.CURSOR_HAND)
            btn.set_background_color((75, 79, 81))

    def _clear_maze(self) -> None:
        """
        Clear the maze.
        """
        self._path_found = False
        self._algorithm_run = False
        for row in range(self._rows):
            for column in range(self._rows):
                if (row, column) != self._start_point and (row, column) != self._end_point:
                    self._grid[row][column].update(nodetype='blank', is_visited=False, is_path=False)
        self._clear_visited()

    def _run_generator(self) -> None:
        """
        Run the generator.
        """
        if self._visualize:
            ut.set_pygame_cursor(pygame_menu.locals.CURSOR_NO)
        o_visualize = self._visualize
        gen_type = self._menu.get_widget('generator').get_value()[1]
        if gen_type != 3:
            self._clear_maze()
        if gen_type == 0:
            self._grid = self._prim(start_point=self._start_point)
        elif gen_type == 1:
            self._grid = self._better_prim(start_point=self._start_point)
        elif gen_type == 2:
            pygame.display.flip()
            self._recursive_division()
        elif gen_type == 3:
            self._random_terrain()
        self._visualize = o_visualize
        if self._visualize:
            ut.set_pygame_cursor(pygame_menu.locals.CURSOR_ARROW)

    def _run_solver(self) -> None:
        """
        Run the solver.
        """
        o_visualize = self._visualize
        solver_type = self._menu.get_widget('solver').get_value()[1]
        if self._visualize:
            pygame.display.flip()
        if self._path_found and self._algorithms[solver_type] == self._algorithm_run:
            self._visualize = False
        else:
            self._clear_visited()
            pygame.display.flip()
        if self._visualize:
            ut.set_pygame_cursor(pygame_menu.locals.CURSOR_NO)
        if solver_type == 0:
            self._path_found = self._dijkstra(self._grid, self._start_point, self._end_point)
            self._algorithm_run = 'dijkstra'
        elif solver_type == 1:
            self._path_found = self._dijkstra(self._grid, self._start_point, self._end_point, astar=True)
            self._algorithm_run = 'astar'
        elif solver_type == 2:
            self._path_found = self._xfs(self._grid, self._start_point, self._end_point, x='d')
            self._algorithm_run = 'dfs'
        elif solver_type == 3:
            self._path_found = self._xfs(self._grid, self._start_point, self._end_point, x='b')
            self._algorithm_run = 'bfs'
        self._visualize = o_visualize
        self._grid[self._start_point[0]][self._start_point[1]].update(nodetype='start')
        self._update_path()
        if self._visualize:
            ut.set_pygame_cursor(pygame_menu.locals.CURSOR_ARROW)

    def _check_esc(self) -> None:
        """
        Check if ESC button was pressed.
        """
        if self._visualize:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._visualize = False

    @staticmethod
    def _sleep(ms: float) -> None:
        """
        Sleep time.

        :param ms: Sleep in ms
        """
        time.sleep(ms)

    def _better_prim(self, mazearray: Optional[_MazeType] = None, start_point: Optional[_Point2] = None) -> _MazeType:
        """
        Randomized Prim's algorithm for creating random mazes.
        This version maintains the traditional "maze" look, where a route cannot
        be diagonally connected to another point on the route.

        :param mazearray: Initial maze
        :param start_point: Creates a new starting point
        :return: New maze
        """
        # If a maze isn't input, we just create a grid full of walls
        if not mazearray:
            mazearray: _MazeType = []
            for row in range(self._rows):
                mazearray.append([])
                for column in range(self._rows):
                    if row % 2 != 0 and column % 2 != 0:
                        mazearray[row].append(Node('dormant'))
                    else:
                        mazearray[row].append(Node('wall'))
                    if self._visualize:
                        self._draw_square(mazearray, row, column)

        n = len(mazearray) - 1

        if not start_point:
            start_point = (random.randrange(1, n, 2), random.randrange(1, n, 2))
            mazearray[start_point[0]][start_point[1]].update(nodetype='blank')

        if self._visualize:
            self._draw_square(mazearray, start_point[0], start_point[1])
            pygame.display.flip()

        walls = set()

        starting_walls = self._get_neighbours(start_point, n)

        for wall, ntype in starting_walls:
            if mazearray[wall[0]][wall[1]].nodetype == 'wall':
                walls.add(wall)

        # While there are walls in the list (set):
        # Pick a random wall from the list. If only one of the cells that the wall divides is visited, then:
        # # Make the wall a passage and mark the unvisited cell as part of the maze.
        # # Add the neighboring walls of the cell to the wall list.
        # Remove the wall from the list.
        while len(walls) > 0:
            self._check_esc()
            wall = random.choice(tuple(walls))
            visited = 0
            add_to_maze = []

            for wall_neighbour, ntype in self._get_neighbours(wall, n):
                if mazearray[wall_neighbour[0]][wall_neighbour[1]].nodetype == 'blank':
                    visited += 1

            if visited <= 1:
                mazearray[wall[0]][wall[1]].update(nodetype='blank')

                if self._visualize:
                    self._draw_square(mazearray, wall[0], wall[1])
                    self._update_square(wall[0], wall[1])
                    self._sleep(0.0001)

                # A 'dormant' node (below) is a different type of node I had to create for this algo
                # otherwise the maze generated doesn't look like a traditional maze.
                # Every dormant eventually becomes a blank node, while the regular walls
                # sometimes become a passage between blanks and are sometimes left as walls
                for neighbour, ntype in self._get_neighbours(wall, n):
                    if mazearray[neighbour[0]][neighbour[1]].nodetype == 'dormant':
                        add_to_maze.append((neighbour[0], neighbour[1]))

                if len(add_to_maze) > 0:
                    cell = add_to_maze.pop()
                    mazearray[cell[0]][cell[1]].update(nodetype='blank')

                    if self._visualize:
                        self._draw_square(mazearray, cell[0], cell[1])
                        self._update_square(cell[0], cell[1])
                        self._sleep(0.0001)

                    for cell_neighbour, ntype in self._get_neighbours(cell, n):
                        if mazearray[cell_neighbour[0]][cell_neighbour[1]].nodetype == 'wall':
                            walls.add(cell_neighbour)

            walls.remove(wall)

        # Iterate through each dormant, if so, change to blank
        for row in range(self._rows):
            for column in range(self._rows):
                if mazearray[row][column].nodetype == 'dormant':
                    mazearray[row][column].update(nodetype='blank')

        mazearray[self._end_point[0]][self._end_point[1]].update(nodetype='end')
        mazearray[self._start_point[0]][self._start_point[1]].update(nodetype='start')

        return mazearray

    def _prim(self, mazearray: Optional[_MazeType] = None, start_point: Optional[_Point2] = None) -> _MazeType:
        """
        Randomized Prim's algorithm for creating random mazes.

        :param mazearray: Initial maze
        :param start_point: Creates a new starting point
        :return: New maze
        """
        # If a maze isn't input, we just create a grid full of walls
        if not mazearray:
            mazearray: _MazeType = []
            for row in range(self._rows):
                mazearray.append([])
                for column in range(self._rows):
                    mazearray[row].append(Node('wall'))
                    if self._visualize:
                        self._draw_square(mazearray, row, column)

        n = len(mazearray) - 1

        if not start_point:
            start_point = (random.randrange(0, n, 2), random.randrange(0, n, 2))

        if self._visualize:
            self._draw_square(mazearray, start_point[0], start_point[1])
            pygame.display.flip()

        walls = set([])

        neighbours = self._get_neighbours(start_point, n)

        for neighbour, ntype in neighbours:
            if mazearray[neighbour[0]][neighbour[1]].nodetype == 'wall':
                walls.add(neighbour)

        # While there are walls in the list:
        # Pick a random wall from the list. If only one of the cells that the wall divides is visited, then:
        # Make the wall a passage and mark the unvisited cell as part of the maze.
        # Add the neighboring walls of the cell to the wall list.
        # Remove the wall from the list.
        while len(walls) > 0:
            self._check_esc()
            wall = random.choice(tuple(walls))
            wall_neighbours = self._get_neighbours(wall, n)
            neighbouring_walls = set()
            pcount = 0
            for wall_neighbour, ntype in wall_neighbours:
                if wall_neighbour == (start_point or self._end_point):
                    continue
                if mazearray[wall_neighbour[0]][wall_neighbour[1]].nodetype != 'wall':
                    pcount += 1
                else:
                    neighbouring_walls.add(wall_neighbour)

            if pcount <= 1:
                mazearray[wall[0]][wall[1]].update(nodetype='blank')
                if self._visualize:
                    self._draw_square(mazearray, wall[0], wall[1])
                    self._update_square(wall[0], wall[1])
                    self._sleep(0.000001)

                walls.update(neighbouring_walls)

            walls.remove(wall)

        mazearray[self._end_point[0]][self._end_point[1]].update(nodetype='end')
        mazearray[self._start_point[0]][self._start_point[1]].update(nodetype='start')

        return mazearray

    def _recursive_division(
            self,
            chamber: Optional[Tuple[int, int, int, int]] = None,
            halving=True
    ) -> None:
        """
        Performs recursive division.

        :param chamber: Limits
        :param halving: Divides the recursion area by two
        """

        def _gaps_to_offset() -> List[int]:
            """
            Gaps to offset.
            """
            return [_x for _x in range(2, self._rows, 3)]

        gaps_to_offset = _gaps_to_offset()

        sleep = 0.001
        sleep_walls = 0.001

        # When no "chamber" is input,we are starting with the base grid
        if chamber is None:
            chamber_width = len(self._grid)
            chamber_height = len(self._grid[1])
            chamber_left = 0
            chamber_top = 0
        else:
            chamber_width = chamber[2]
            chamber_height = chamber[3]
            chamber_left = chamber[0]
            chamber_top = chamber[1]

        if halving:
            x_divide = int(chamber_width / 2)
            y_divide = int(chamber_height / 2)
        else:
            x_divide = chamber_width
            y_divide = chamber_height

        if chamber_width < 3:
            pass
        else:
            # draw x wall
            for y in range(chamber_height):
                self._grid[chamber_left + x_divide][chamber_top + y].update(nodetype='wall')
                self._draw_square(self._grid, chamber_left + x_divide, chamber_top + y)
                if self._visualize:
                    self._update_square(chamber_left + x_divide, chamber_top + y)
                    self._sleep(sleep_walls)

        if chamber_height < 3:
            pass
        else:
            # draw y wall
            for x in range(chamber_width):
                self._grid[chamber_left + x][chamber_top + y_divide].update(nodetype='wall')
                self._draw_square(self._grid, chamber_left + x, chamber_top + y_divide)
                if self._visualize:
                    self._update_square(chamber_left + x, chamber_top + y_divide)
                    self._sleep(sleep_walls)

        # Base case: stop dividing
        if chamber_width < 3 and chamber_height < 3:
            return

        # define the 4 new chambers (left, top, width, height)
        top_left = (chamber_left, chamber_top, x_divide, y_divide)
        top_right = (chamber_left + x_divide + 1, chamber_top, chamber_width - x_divide - 1, y_divide)
        bottom_left = (chamber_left, chamber_top + y_divide + 1, x_divide, chamber_height - y_divide - 1)
        bottom_right = (chamber_left + x_divide + 1, chamber_top + y_divide + 1, chamber_width - x_divide - 1,
                        chamber_height - y_divide - 1)

        chambers = (top_left, top_right, bottom_left, bottom_right)

        # define the 4 walls (of a + symbol) (left, top, width, height)
        left = (chamber_left, chamber_top + y_divide, x_divide, 1)
        right = (chamber_left + x_divide + 1, chamber_top + y_divide, chamber_width - x_divide - 1, 1)
        top = (chamber_left + x_divide, chamber_top, 1, y_divide)
        bottom = (chamber_left + x_divide, chamber_top + y_divide + 1, 1, chamber_height - y_divide - 1)

        walls = (left, right, top, bottom)

        gaps = 3
        for wall in random.sample(walls, gaps):
            if wall[3] == 1:
                x = random.randrange(wall[0], wall[0] + wall[2])
                y = wall[1]
                if x in gaps_to_offset and y in gaps_to_offset:
                    if wall[2] == x_divide:
                        x -= 1
                    else:
                        x += 1
                if x >= self._rows:
                    x = self._rows - 1
            else:  # the wall is horizontal
                x = wall[0]
                y = random.randrange(wall[1], wall[1] + wall[3])
                if y in gaps_to_offset and x in gaps_to_offset:
                    if wall[3] == y_divide:
                        y -= 1
                    else:
                        y += 1
                if y >= self._rows:
                    y = self._rows - 1
            self._grid[x][y].update(nodetype='blank')
            self._draw_square(self._grid, x, y)
            if self._visualize:
                self._update_square(x, y)
                self._sleep(sleep)

        # recursively apply the algorithm to all chambers
        for num, chamber in enumerate(chambers):
            self._recursive_division(chamber)
            self._check_esc()

    def _random_terrain(self, num_patches: Optional[int] = None) -> None:
        """
        Add random terrain to the maze.

        :param num_patches: Number of patches
        """
        if not num_patches:
            num_patches: int = random.randrange(int(self._rows / 10), int(self._rows / 4))

        terrain_nodes = set([])

        if self._visualize:
            pygame.display.flip()

        # For each patch we are creating we start with a centre node and branch outwards
        # getting neighbours of neighbours etc. for each node that we consider, there is
        # a variable probability of it becoming a patch of mud
        # As we branch outwards that probability decreases
        for patch in range(num_patches + 1):
            self._check_esc()
            neighbour_cycles = 0
            centre_point = (random.randrange(1, self._rows - 1), random.randrange(1, self._rows - 1))
            patch_type = 'mud'
            terrain_nodes.add(centre_point)

            while len(terrain_nodes) > 0:
                node = terrain_nodes.pop()

                if self._grid[node[0]][node[1]].nodetype != 'start' and self._grid[node[0]][node[1]].nodetype != 'end':
                    self._grid[node[0]][node[1]].update(nodetype=patch_type)
                    self._draw_square(self._grid, node[0], node[1])

                    if self._visualize:
                        self._update_square(node[0], node[1])
                        self._sleep(0.000001)

                neighbour_cycles += 1

                for node, ntype in self._get_neighbours(node):

                    if self._grid[node[0]][node[1]].nodetype == 'mud':
                        continue
                    threshold = 700 - (neighbour_cycles * 10)

                    if random.randrange(1, 101) <= threshold:
                        terrain_nodes.add(node)

    def _update_gui(self, draw_background=True, draw_menu=True, draw_grid=True) -> None:
        """
        Updates the gui.

        :param draw_background: Draw the background
        :param draw_menu: Draw the menu
        :param draw_grid: Draw the grid
        """
        if draw_background:
            # Draw a black background to set everything on
            self._surface.fill(BACKGROUND)

        if draw_grid:
            # Draw the grid
            for row in range(self._rows):
                for column in range(self._rows):
                    self._draw_square(self._grid, row, column)

        if draw_menu:
            self._menu.draw(self._surface)

    def _clear_visited(self) -> None:
        """
        Clear the visited grid.
        """
        excluded_nodetypes = ['start', 'end', 'wall', 'mud']
        for row in range(self._rows):
            for column in range(self._rows):
                if self._grid[row][column].nodetype not in excluded_nodetypes:
                    self._grid[row][column].update(nodetype='blank', is_visited=False, is_path=False)
                else:
                    self._grid[row][column].update(is_visited=False, is_path=False)
        self._update_gui()

    def _update_path(self) -> Union[bool, _MazeType]:
        """
        Updates the path.
        """
        self._clear_visited()
        assert self._algorithm_run in self._algorithms.values(), \
            f'last algorithm used ({self._algorithm_run}) is not in valid algorithms: {self._algorithms.values()}'

        visualize = self._visualize
        self._visualize = False
        if self._algorithm_run == 'dijkstra':
            path_found = self._dijkstra(self._grid, self._start_point, self._end_point)
        elif self._algorithm_run == 'astar':
            path_found = self._dijkstra(self._grid, self._start_point, self._end_point, astar=True)
        elif self._algorithm_run == 'dfs':
            path_found = self._xfs(self._grid, self._start_point, self._end_point, x='d')
        elif self._algorithm_run == 'bfs':
            path_found = self._xfs(self._grid, self._start_point, self._end_point, x='b')
        else:
            path_found = False
        self._visualize = visualize

        return path_found

    def _get_neighbours(
            self,
            node: _Point2,
            max_width: Optional[int] = None
    ) -> Generator[Tuple[_Point2, str], Any, None]:
        """
        Get the neighbours.

        :param node: Node
        :param max_width: Max width
        :return: Neighbours
        """
        if not max_width:
            max_width = self._rows - 1
        if not self._diagonals:
            neighbours = (
                ((min(max_width, node[0] + 1), node[1]), '+'),
                ((max(0, node[0] - 1), node[1]), '+'),
                ((node[0], min(max_width, node[1] + 1)), '+'),
                ((node[0], max(0, node[1] - 1)), '+')
            )
        else:
            neighbours = (
                ((min(max_width, node[0] + 1), node[1]), '+'),
                ((max(0, node[0] - 1), node[1]), '+'),
                ((node[0], min(max_width, node[1] + 1)), '+'),
                ((node[0], max(0, node[1] - 1)), '+'),
                ((min(max_width, node[0] + 1), min(max_width, node[1] + 1)), 'x'),
                ((min(max_width, node[0] + 1), max(0, node[1] - 1)), 'x'),
                ((max(0, node[0] - 1), min(max_width, node[1] + 1)), 'x'),
                ((max(0, node[0] - 1), max(0, node[1] - 1)), 'x')
            )

        # return neighbours
        return (neighbour for neighbour in neighbours if neighbour[0] != node)

    def _draw_square(self, grid: _MazeType, row: int, column: int) -> None:
        """
        Draws a square.

        :param grid: Grid
        :param row: Row number
        :param column: Column number
        """
        pygame.draw.rect(
            self._surface,
            grid[row][column].color,
            [
                (self._margin + self._width) * column + self._margin + self._offset[0],
                (self._margin + self._height) * row + self._margin + self._offset[1],
                self._width,
                self._height
            ]
        )
        pygame.event.pump()

    def _update_square(self, row: int, column: int) -> None:
        """
        Updates the square.

        :param row: Row number
        :param column: Column number
        :return:
        """
        # noinspection PyArgumentList
        pygame.display.update(
            (self._margin + self._width) * column + self._margin + self._offset[0],
            (self._margin + self._height) * row + self._margin + self._offset[1],
            self._width,
            self._height
        )
        pygame.event.pump()

    def _dijkstra(
            self,
            mazearray: _MazeType,
            start_point: _Point2 = (0, 0),
            goal_node: Optional[_Point2] = None,
            astar: bool = False
    ) -> bool:
        """
        Dijkstra's pathfinding algorithm, with the option to switch to A* by
        adding a heuristic of expected distance to end node.

        :param mazearray: Maze
        :param start_point: Starting point
        :param goal_node: Goal
        :param astar: A*
        :return: Finish status
        """
        heuristic = 0
        distance = 0

        # Get the dimensions of the (square) maze
        n = len(mazearray) - 1

        # Create the various data structures with speed in mind
        visited_nodes = set()
        unvisited_nodes = set([(x, y) for x in range(n + 1) for y in range(n + 1)])
        queue = AStarQueue()

        queue.push(distance + heuristic, distance, start_point)
        v_distances = {}

        # If a goal_node is not set, put it in the bottom right (1 square away from either edge)
        if not goal_node:
            goal_node = (n, n)
        priority, current_distance, current_node = queue.pop()
        start = time.perf_counter()

        # Main algorithm loop
        while current_node != goal_node and len(unvisited_nodes) > 0:
            self._check_esc()
            if current_node in visited_nodes:
                if len(queue.show()) == 0:
                    return False
                else:
                    priority, current_distance, current_node = queue.pop()
                    continue

            # Call to check neighbours of the current node
            for neighbour in self._get_neighbours(current_node, n):
                self._neighbours_loop(
                    neighbour,
                    mazearr=mazearray,
                    visited_nodes=visited_nodes,
                    unvisited_nodes=unvisited_nodes,
                    queue=queue,
                    # v_distances=v_distances,
                    # current_node=current_node,
                    current_distance=current_distance,
                    astar=astar
                )

            # When we have checked the current node, add and remove appropriately
            visited_nodes.add(current_node)
            unvisited_nodes.discard(current_node)

            # Add the distance to the visited distances' dictionary (used for traceback)
            v_distances[current_node] = current_distance

            # Pygame part: visited nodes mark visited nodes as green
            if (current_node[0], current_node[1]) != start_point:
                mazearray[current_node[0]][current_node[1]].update(is_visited=True)
                self._draw_square(mazearray, current_node[0], current_node[1])

                # If we want to visualise it (rather than run instantly)
                # then we update the grid with each loop
                if self._visualize:
                    self._update_square(current_node[0], current_node[1])
                    self._sleep(0.000001)

            # If there are no nodes in the queue then we return False (no path)
            if len(queue.show()) == 0:
                return False
            # Otherwise, we take the minimum distance as the new current node
            else:
                priority, current_distance, current_node = queue.pop()

        v_distances[goal_node] = current_distance + (1 if not self._diagonals else 2 ** 0.5)
        visited_nodes.add(goal_node)

        # Draw the path back from goal node to start node
        self._trace_back(goal_node, start_point, v_distances, n, mazearray)

        end = time.perf_counter()
        num_visited = len(visited_nodes)
        time_taken = end - start

        # Print timings
        print(f'Program finished in {time_taken:.4f}s after checking {num_visited}'
              f' nodes ({time_taken / num_visited:.8f} s/node)')

        return False if v_distances[goal_node] == float('inf') else True

    def _neighbours_loop(self, neighbour, mazearr, visited_nodes, unvisited_nodes, queue,  # v_distances, current_node,
                         current_distance, astar=False) -> None:
        """
        Loop through neighbours.
        """
        neighbour, ntype = neighbour
        heuristic = 0

        if astar:
            heuristic += abs(self._end_point[0] - neighbour[0]) + abs(self._end_point[1] - neighbour[1])
            heuristic *= 1  # If this goes above 1 then the shortest path is not guaranteed, but the attempted route becomes more direct

        # If the neighbour has already been visited
        if neighbour in visited_nodes:
            pass
        elif mazearr[neighbour[0]][neighbour[1]].nodetype == 'wall':
            visited_nodes.add(neighbour)
            unvisited_nodes.discard(neighbour)
        else:
            modifier = mazearr[neighbour[0]][neighbour[1]].distance_modifier
            if ntype == '+':
                queue.push(current_distance + (1 * modifier) + heuristic, current_distance + (1 * modifier), neighbour)
            elif ntype == 'x':
                queue.push(current_distance + ((2 ** 0.5) * modifier) + heuristic,
                           current_distance + ((2 ** 0.5) * modifier), neighbour)

    def _trace_back(self, goal_node, start_node, v_distances, n, mazearray) -> None:
        """
        (DIJKSTRA/A*) trace a path back from the end node to the start node after the algorithm has been run.
        """
        # Begin the list of nodes which will represent the path back, starting with the end node
        path = [goal_node]
        current_node = goal_node

        # Set the loop in motion until we get back to the start
        while current_node != start_node:
            # Start an empty priority queue for the current node to check all neighbours
            neighbour_distances = PriorityQueue()

            neighbours = self._get_neighbours(current_node, n)

            # Had some errors during testing, not sure if this is still necessary
            try:
                v_distances[current_node]
            except Exception as e:
                print(e)

            # For each neighbour of the current node, add its location and distance
            # to a priority queue
            for neighbour, ntype in neighbours:
                if neighbour in v_distances:
                    distance = v_distances[neighbour]
                    neighbour_distances.push(distance, neighbour)

            # Pop the lowest value off; that is the next node in our path
            distance, smallest_neighbour = neighbour_distances.pop()
            mazearray[smallest_neighbour[0]][smallest_neighbour[1]].update(is_path=True)

            # Update pygame display
            self._draw_square(mazearray, smallest_neighbour[0], smallest_neighbour[1])

            path.append(smallest_neighbour)
            current_node = smallest_neighbour

        pygame.display.flip()

        mazearray[start_node[0]][start_node[1]].update(is_path=True)

    def _xfs(self, mazearray: _MazeType, start_point: _Point2, goal_node: _Point2, x: str) -> bool:
        """
        This is a function where you choose x='b' or x='d' to run bfs (breadth-first search) or
        dfs (depth-first search) on your chosen mazearray (grid format), with chosen start_point (x,y)
        and chosen goal_node (x,y).

        :param mazearray: Maze array
        :param start_point: Starting point
        :param goal_node: Ending point
        :param x: Type
        :return: False
        """
        assert x == 'b' or x == 'd', "x should equal 'b' or 'd' to make this bfs or dfs"

        # Get the dimensions of the (square) maze
        n = len(mazearray) - 1

        # Create the various data structures with speed in mind
        mydeque = deque()
        mydeque.append(start_point)
        visited_nodes = set([])
        path_dict = {start_point: None}

        # Main algorithm loop
        while len(mydeque) > 0:
            self._check_esc()
            if x == 'd':
                current_node = mydeque.pop()
            elif x == 'b':
                current_node = mydeque.popleft()

            # noinspection PyUnboundLocalVariable
            if current_node == goal_node:
                # Trace back to start using path_dict
                path_node = goal_node
                while True:
                    path_node = path_dict[path_node]
                    mazearray[path_node[0]][path_node[1]].update(is_path=True)
                    self._draw_square(mazearray, path_node[0], path_node[1])
                    if self._visualize:
                        self._update_square(path_node[0], path_node[1])
                    if path_node == start_point:
                        return True

            if mazearray[current_node[0]][current_node[1]].nodetype == 'wall':
                continue

            if current_node not in visited_nodes:
                visited_nodes.add(current_node)
                mazearray[current_node[0]][current_node[1]].update(is_visited=True)
                self._draw_square(mazearray, current_node[0], current_node[1])
                if self._visualize:
                    self._update_square(current_node[0], current_node[1])
                    self._sleep(0.001)

                for neighbour, ntype in self._get_neighbours(current_node, n):
                    mydeque.append(neighbour)
                    # Used for tracing back
                    if neighbour not in visited_nodes:
                        path_dict[neighbour] = current_node

        pygame.display.flip()
        return False

    def _get_pos(self, pos: _Point2) -> _Point2:
        """
        Return the column/row position within maze.

        :param pos: Position
        :return: Position in col/row
        """
        column = (pos[0] - self._offset[0]) // (self._width + self._margin)
        row = (pos[1] - self._offset[1]) // (self._height + self._margin)
        return column, row

    def _pos_in_grid(self, pos: _Point2) -> bool:
        """
        Check if the mouse position is in grid.

        :param pos: Position
        :return: True if inside
        """
        x = pos[0] - self._offset[0]
        y = pos[1] - self._offset[1]
        return 1 <= x <= self._screen_width and 1 <= y <= self._screen_width

    @staticmethod
    def _quit() -> None:
        """
        Quit app.
        """
        pygame.quit()
        exit()

    def mainloop(self, test: bool) -> None:
        """
        Executes the main loop of the app.

        :param test: If True, runs only 1 frame
        """
        print('Press [ESC] to skip process if Visualize is On')
        while True:

            # Application events
            events = pygame.event.get()

            # Update the menu
            self._menu.update(events)

            # If a menu widget disable its active state, disable the events, this is due to
            # user can click outside a dropselection box, and that triggers to disable active
            # state. If so, the event is destroyed, thus avoiding clicking the canvas
            if pygame_menu.events.MENU_LAST_WIDGET_DISABLE_ACTIVE_STATE in self._menu.get_last_update_mode()[0]:
                events = []

            for event in events:
                # User closes
                if event.type == pygame.QUIT:
                    self._quit()

                # Write in the board
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    # Find out which keys have been pressed
                    pressed = pygame.key.get_pressed()

                    # If click is inside grid
                    if self._pos_in_grid(pos):

                        # Change the x/y screen coordinates to grid coordinates
                        column, row = self._get_pos(pos)

                        if (row, column) == self._start_point:
                            self._drag_start_point = True
                        elif (row, column) == self._end_point:
                            self._drag_end_point = True
                        else:
                            cell_updated = self._grid[row][column]
                            if pressed[pygame.K_LCTRL]:
                                update_cell_to = 'mud'
                            else:
                                update_cell_to = 'wall'
                            cell_updated.update(nodetype=update_cell_to)
                            self._mouse_drag = True
                            if self._algorithm_run and cell_updated.is_path:
                                self._path_found = self._update_path()

                # Turn off all mouse drags if mouse Button released
                elif event.type == pygame.MOUSEBUTTONUP:
                    self._mouse_drag = self._drag_end_point = self._drag_start_point = False

                # Moves the mouse
                elif event.type == pygame.MOUSEMOTION:
                    # Boolean values saying whether left, middle and right mouse buttons are currently pressed
                    left, middle, right = pygame.mouse.get_pressed()

                    # Sometimes we get stuck in this loop if the mousebutton is released while not in the pygame screen
                    # This acts to break out of that loop
                    if not left:
                        self._mouse_drag = self._drag_end_point = self._drag_start_point = False
                        continue

                    # User moves the mouse. Get the position
                    pos = pygame.mouse.get_pos()

                    # Change the x/y screen coordinates to grid coordinates
                    column, row = self._get_pos(pos)

                    # Turn mouse_drag off if mouse goes outside of grid
                    if not self._pos_in_grid(pos):
                        self._mouse_drag = False
                        continue

                    try:
                        cell_updated = self._grid[row][column]
                    except IndexError:
                        continue

                    # Add walls or sticky mud patches
                    pressed = pygame.key.get_pressed()
                    if self._mouse_drag:
                        if (row, column) == self._start_point:
                            pass
                        elif (row, column) == self._end_point:
                            pass
                        else:
                            if pressed[pygame.K_LCTRL]:
                                update_cell_to = 'mud'
                            else:
                                update_cell_to = 'wall'
                            cell_updated.update(nodetype=update_cell_to)

                        self._mouse_drag = True
                        if self._algorithm_run:
                            if cell_updated.is_path:
                                self._path_found = self._update_path()

                    # Move the start point
                    elif self._drag_start_point:
                        if self._grid[row][column].nodetype == 'blank':
                            self._grid[self._start_point[0]][self._start_point[1]].update(nodetype='blank',
                                                                                          is_path=False,
                                                                                          is_visited=False)
                            self._start_point = (row, column)
                            self._grid[self._start_point[0]][self._start_point[1]].update(nodetype='start')
                            # If we have already run the algorithm, update it as the point is moved
                            if self._algorithm_run:
                                self._path_found = self._update_path()
                                self._grid[self._start_point[0]][self._start_point[1]].update(nodetype='start')

                    # Move the end point
                    elif self._drag_end_point:
                        if self._grid[row][column].nodetype == 'blank':
                            self._grid[self._end_point[0]][self._end_point[1]].update(nodetype='blank', is_path=False,
                                                                                      is_visited=False)
                            self._end_point = (row, column)
                            self._grid[self._end_point[0]][self._end_point[1]].update(nodetype='end')
                            # If we have already run the algorithm, update it as the point is moved
                            if self._algorithm_run:
                                self._path_found = self._update_path()
                                self._grid[self._end_point[0]][self._end_point[1]].update(nodetype='start')

                    pygame.display.flip()

            # Update the app
            self._update_gui()

            self._grid[self._start_point[0]][self._start_point[1]].update(nodetype='start')
            self._grid[self._end_point[0]][self._end_point[1]].update(nodetype='end')

            # Flip surface
            pygame.display.flip()

            # Update clock
            self._clock.tick(self._fps)

            # At first loop returns
            if test:
                break


def main(test: bool = False) -> 'MazeApp':
    """
    Main function.

    :param test: Indicate function is being tested
    :return: App
    """
    app = MazeApp()
    app.mainloop(test)
    return app


if __name__ == '__main__':
    main()
