# coding=utf-8
"""
SELECTOR
Selector class, manage elements and adds entries to menu.

Copyright (C) 2017-2018 Pablo Pizarro @ppizarror

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""


class Selector(object):
    """
    Selector object
    """

    def __init__(self, title, elements, onchange=None, onreturn=None, default=0, **kwargs):
        """
        Constructor.

        :param title: Title of the selector
        :param elements: Elements of the selector
        :param default: Index of default element to display
        :param kwargs: Optional arguments
        :param onchange: Event when changing the selector
        :param onreturn: Event when pressing return button
        :type title: str
        :type elements: list
        :type onchange: function, NoneType
        :type onreturn: function, NoneType
        :type default: int
        """
        self._elements = elements
        self._index = 0
        self._kwargs = kwargs
        self._on_change = onchange
        self._on_return = onreturn
        self._title = title
        self._total_elements = len(elements)

        # Apply default item
        default %= self._total_elements
        for k in range(0, default):
            self.right()

    def update_elements(self, elements):
        """
        Update selector elements.

        :param elements: Elements of the selector
        :return: None
        """
        selected_element = self._elements[self._index]
        self._elements = elements
        self._total_elements = len(elements)
        try:
            self._index = self._elements.index(selected_element)
        except ValueError:
            if self._index >= self._total_elements:
                self._index = self._total_elements - 1

    def apply(self):
        """
        Apply the selected item when return event.

        :return: None
        """
        if self._on_return is not None:
            paramlist = self._elements[self._index]
            paraml = []
            for i in range(1, len(paramlist)):
                paraml.append(paramlist[i])

            if len(self._kwargs) > 0:
                self._on_return(*paraml, **self._kwargs)
            else:
                self._on_return(*paraml)

    def change(self):
        """
        Apply the selected item when changing.

        :return: None
        """
        if self._on_change is not None:
            paramlist = self._elements[self._index]
            paraml = []
            for i in range(1, len(paramlist)):
                paraml.append(paramlist[i])

            if len(self._kwargs) > 0:
                self._on_change(*paraml, **self._kwargs)
            else:
                self._on_change(*paraml)

    def get(self):
        """
        Return element text.

        :return: Element text
        :rtype: str
        """
        return '{0} < {1} >'.format(self._title, self._elements[self._index][0])

    def left(self):
        """
        Move selector to left.

        :return:
        """
        self._index = (self._index - 1) % self._total_elements
        self.change()

    def right(self):
        """
        Move selector to right.

        :return:
        """
        self._index = (self._index + 1) % self._total_elements
        self.change()
