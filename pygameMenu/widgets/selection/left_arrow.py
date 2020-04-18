import pygame

from pygameMenu.widgets.core.selection import Selection


class LeftArrowSelection(Selection):
    """
    Widget selection left arrow class.
    Creates an arrow to the left of the selected menu item.

    :param arrow_size: size of arrow
    :type arrow_size: int, float
    """

    def __init__(self,
                 arrow_size=15):
        super(LeftArrowSelection, self).__init__(margin_left=0, margin_right=arrow_size,
                                                 margin_top=0, margin_bottom=0)
        self.arrow_size = arrow_size

    def get_margin(self):
        """
        Return top, left, bottom and right margins of the selection.

        :return: Tuple of (t,l,b,r) margins in px
        :rtype: tuple
        """
        return 0, self.arrow_size, 0, 0

    def draw(self, surface, widget):
        """
        Draw the selection.

        :param surface: Surface to draw
        :type surface: pygame.surface.SurfaceType
        :param widget: Widget object
        :type widget: pygameMenu.widgets.core.widget.Widget
        :return: None
        """
        pygame.draw.polygon(surface,
                            self.color,
                            [(widget.get_rect().topleft[0] - self.arrow_size, widget.get_rect().topleft[1]),
                             widget.get_rect().midleft,
                             (widget.get_rect().bottomleft[0] - self.arrow_size, widget.get_rect().bottomleft[1])])
