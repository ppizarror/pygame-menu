import pygame

from pygameMenu.widgets.core.selection import Selection


class LeftArrowSelection(Selection):
    """
    Widget selection highlight class.

    :param border_width: Border width of the highlight box
    :type border_width: int
    :param margin_x: X margin of selected highlight box
    :type margin_x: int, float
    :param margin_y: X margin of selected highlight box
    :type margin_y: int, float
    """

    def __init__(self,
                 border_width=1,
                 margin_x=16.0,
                 margin_y=8.0):
        margin_x = float(margin_x)
        margin_y = float(margin_y)
        super(LeftArrowSelection, self).__init__(margin_left=margin_x / 2, margin_right=margin_x / 2,
                                                 margin_top=margin_y / 2, margin_bottom=margin_y / 2)
        self.border_width = border_width
        self.margin_x = margin_x
        self.margin_y = margin_y

    def get_margin(self):
        """
        Return top, left, bottom and right margins of the selection.

        :return: Tuple of (t,l,b,r) margins in px
        :rtype: tuple
        """
        return self.margin_top + self.border_width, self.margin_left + self.border_width, \
               self.margin_bottom + self.border_width, self.margin_right + self.border_width

    def draw(self, surface, widget):
        """
        Draw the selection.

        :param surface: Surface to draw
        :type surface: pygame.surface.SurfaceType
        :param widget: Widget object
        :type widget: pygameMenu.widgets.core.widget.Widget
        :return: None
        """
        arrow_size = 10
        pygame.draw.polygon(surface,
                            self.color,
                            [(widget.get_rect().topleft[0] - arrow_size, widget.get_rect().topleft[1]),
                             widget.get_rect().midleft,
                             (widget.get_rect().bottomleft[0] - arrow_size, widget.get_rect().bottomleft[1])])
