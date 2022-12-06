"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - LABEL
Test Label widget.
"""

__all__ = ['LabelWidgetTest']

from test._utils import MenuUtils, surface, BaseTest, PYGAME_V2

from pygame_menu.locals import ALIGN_LEFT
from pygame_menu.widgets import Label


class LabelWidgetTest(BaseTest):

    def test_label(self) -> None:
        """
        Test label widget.
        """
        menu = MenuUtils.generic_menu()

        # noinspection SpellCheckingInspection
        label = menu.add.label('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
                               'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, '
                               'quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. '
                               'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu '
                               'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in '
                               'culpa qui officia deserunt mollit anim id est laborum.',
                               max_char=33,
                               margin=(3, 5),
                               align=ALIGN_LEFT,
                               font_size=3)
        self.assertEqual(len(label), 15)
        w = label[0]
        self.assertFalse(w.is_selectable)
        self.assertEqual(w.get_margin()[0], 3)
        self.assertEqual(w.get_margin()[1], 5)
        self.assertEqual(w.get_alignment(), ALIGN_LEFT)
        self.assertEqual(w.get_font_info()['size'], 3)
        w.draw(surface)
        self.assertFalse(w.update([]))
        # noinspection SpellCheckingInspection
        label_text = ['Lorem ipsum dolor sit amet,', 'consectetur adipiscing elit, sed',
                      'do eiusmod tempor incididunt ut', 'labore et dolore magna aliqua. Ut',
                      'enim ad minim veniam, quis', 'nostrud exercitation ullamco',
                      'laboris nisi ut aliquip ex ea', 'commodo consequat. Duis aute',
                      'irure dolor in reprehenderit in', 'voluptate velit esse cillum',
                      'dolore eu fugiat nulla pariatur.', 'Excepteur sint occaecat cupidatat',
                      'non proident, sunt in culpa qui', 'officia deserunt mollit anim id',
                      'est laborum.']
        for i in range(len(label)):
            self.assertEqual(label[i].get_title(), label_text[i])

        # Split label
        label = menu.add.label('This label should split.\nIn two lines')
        self.assertEqual(label[0].get_title(), 'This label should split.')
        self.assertEqual(label[1].get_title(), 'In two lines')

        # Split label, but also with maxchar enabled
        label = menu.add.label(
            'This label should split, this line is really long so it should split.\nThe second line', max_char=40)
        self.assertEqual(label[0].get_title(), 'This label should split, this line is')
        self.assertEqual(label[1].get_title(), 'really long so it should split.')
        self.assertEqual(label[2].get_title(), 'The second line')

        # Split label with -1 maxchar
        label = menu.add.label(
            'This label should split, this line is really long so it should split.\nThe second line', max_char=-1)
        self.assertEqual(label[0].get_title(), 'This label should split, this line is really')
        self.assertEqual(label[1].get_title(), 'long so it should split.')
        self.assertEqual(label[2].get_title(), 'The second line')

        # Split label with -1 double \n
        label = menu.add.label('a\n\nb\n\nc', max_char=-1)
        self.assertEqual(label[0].get_title(), 'a')
        self.assertEqual(label[1].get_title(), '')
        self.assertEqual(label[2].get_title(), 'b')
        self.assertEqual(label[3].get_title(), '')
        self.assertEqual(label[4].get_title(), 'c')

        # Add underline
        label = menu.add.label('nice')
        self.assertEqual(label._decorator._total_decor(), 0)
        label.add_underline((0, 0, 0), 1, 1, force_render=True)
        self.assertEqual(label._decorator._total_decor(), 1)

        # Test generator
        gen_index = [-1]

        def generator() -> str:
            """
            Label generator.
            """
            s = ('a', 'b', 'c')
            gen_index[0] = (gen_index[0] + 1) % len(s)
            return s[gen_index[0]]

        self.assertNotIn(label, menu._update_widgets)
        label.set_title_generator(generator)
        self.assertIn(label, menu._update_widgets)
        self.assertEqual(label.get_title(), 'nice')
        label._render()
        self.assertEqual(label.get_title(), 'nice')
        label.render()
        self.assertEqual(label.get_title(), 'nice')

        label.update([])
        self.assertEqual(label.get_title(), 'a')
        label.update([])
        self.assertEqual(label.get_title(), 'b')
        label.update([])
        self.assertEqual(label.get_title(), 'c')
        label.update([])
        self.assertEqual(label.get_title(), 'a')

        # Update title with generator, it should raise a warning
        label.set_title('this should be overridden')

        label.set_title('this should be overridden 2')

        label.update([])
        self.assertEqual(label.get_title(), 'b')

        # Remove generator, it also should remove the widget from update
        label.set_title_generator(None)
        self.assertNotIn(label, menu._update_widgets)
        label.update([])
        self.assertEqual(label.get_title(), 'b')
        self.assertIsNone(label._title_generator)

        # Label set to empty
        label_e = menu.add.label('new')
        self.assertRaises(ValueError, lambda: label_e.set_value(''))
        label_e.set_title('')
        label_e.draw(surface)

        # Test underline
        label_u = menu.add.label('underlined', underline=True)
        self.assertIsNotNone(label_u._last_underline[1])

    def test_clock(self) -> None:
        """
        Test clock.
        """
        menu = MenuUtils.generic_menu()
        clock = menu.add.clock()
        self.assertNotEqual(clock.get_title(), '')

        # Check title format
        self.assertRaises(AssertionError, lambda: menu.add.clock(title_format='bad'))
        self.assertIsInstance(clock, Label)

    def test_empty_title(self) -> None:
        """
        Test empty title.
        """
        menu = MenuUtils.generic_menu()
        label = menu.add.label('')
        p = label._padding
        self.assertEqual(label.get_width(), p[1] + p[3])
        self.assertEqual(label.get_height(), p[0] + p[2] + 41 if PYGAME_V2 else 42)

    def test_value(self) -> None:
        """
        Test label value.
        """
        menu = MenuUtils.generic_menu()
        label = menu.add.label('title')
        self.assertRaises(ValueError, lambda: label.get_value())
        self.assertRaises(ValueError, lambda: label.set_value('value'))
        self.assertFalse(label.value_changed())
        label.reset_value()

    def test_wordwrap(self) -> None:
        """
        Tests wordwrap.
        """
        menu = MenuUtils.generic_menu()
        label = menu.add.label('lorem ipsum dolor sit amet this was very important nice a test is required', wordwrap=True)
        self.assertEqual(label.get_width(), 586)
        self.assertRaises(AssertionError, lambda: label.get_overflow_lines())
        self.assertEqual(label._get_max_container_width(), 584)
        self.assertEqual(len(label.get_lines()), 2)
        self.assertEqual(label._get_leading(), 41)
        self.assertEqual(label.get_height(), 90)

        # Test none menu
        label.set_menu(None)
        self.assertEqual(label.get_width(apply_padding=False), 0)
        self.assertEqual(label._get_max_container_width(), 0)
        label._force_render()

        # Test multilines
        s = 'lorem ipsum dolor sit amet this was very important nice a test is required ' \
            'lorem ipsum dolor sit amet this was very important nice a test is required'
        label = menu.add.label(s, wordwrap=True, max_nlines=3)  # Maximum number of lines
        self.assertEqual(len(label.get_lines()), 3)  # The widget needs 4 lines, but maximum is 3
        self.assertEqual(label.get_height(), 131)
        self.assertEqual(label.get_overflow_lines(), ['important nice a test is required'])

        # The sum of lines and overflow should be the same as s
        self.assertEqual(' '.join(label.get_lines() + label.get_overflow_lines()), s)

        label.set_menu(None)
        self.assertEqual(label.get_overflow_lines(), [])
