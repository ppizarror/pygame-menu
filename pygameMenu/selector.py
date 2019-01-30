# coding=utf-8
"""
SELECTOR
Selector class, manage elements and adds entries to menu.

The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

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

        # Selection format
        self._sformat = '{0} < {1} >'

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

    def format_selection(self, s):
        """
        Change the selection text.

        :param s: Selection text
        :type s: basestring
        :return:
        """
        self._sformat = s

    def get(self):
        """
        Return element text.

        :return: Element text
        :rtype: str
        """
        return self._sformat.format(self._title, self._elements[self._index][0])

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
