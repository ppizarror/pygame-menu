"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - TABLE
Test Table widget.
"""

__all__ = ['TableWidgetTest']

from test._utils import MenuUtils, surface, PYGAME_V2, BaseTest

import pygame
import pygame_menu


class TableWidgetTest(BaseTest):

    def test_table(self) -> None:
        """
        Test table.
        """
        if not PYGAME_V2:
            return

        menu = MenuUtils.generic_menu()
        btn = menu.add.button('1')
        table = menu.add.table('table', background_color='red')
        self.assertTrue(table.is_rectangular())
        self.assertEqual(table.get_inner_size(), (0, 0))
        self.assertEqual(table.get_size(apply_padding=False), (0, 0))
        self.assertRaises(RuntimeError, lambda: table.pack(btn))

        # Test add rows
        row1 = table.add_row([1, 2, 3], row_background_color='blue', cell_align=pygame_menu.locals.ALIGN_CENTER)
        self.assertTrue(table.is_rectangular())
        self.assertEqual(row1.get_size(), (51, 41))
        self.assertEqual(table.get_size(apply_padding=False), (51, 41))
        row2 = table.add_row([10, 20, 30], row_background_color='green', cell_padding=10)
        self.assertEqual(row1.get_size(), (162, 41))
        self.assertEqual(row2.get_size(), (162, 61))
        self.assertEqual(table.get_size(apply_padding=False), (162, 102))
        table.draw(surface)
        self.assertTrue(table.is_rectangular())

        # Test get cell
        self.assertEqual(table.get_cell(2, 1), row1.get_widgets(unpack_subframes=False)[1])
        self.assertEqual(table.get_cell(1, 2), row2.get_widgets(unpack_subframes=False)[0])
        self.assertRaises(AssertionError, lambda: table.get_cell(0, 0))
        self.assertRaises(AssertionError, lambda: table.get_cell(0, 1))
        self.assertRaises(AssertionError, lambda: table.get_cell(1, 0))
        c1 = table.get_cell(1, 1)
        self.assertEqual(c1, row1.get_widgets(unpack_subframes=False)[0])

        # Test cell properties
        self.assertEqual(c1.get_attribute('align'), pygame_menu.locals.ALIGN_CENTER)
        self.assertEqual(c1.get_attribute('border_color'), (0, 0, 0, 255))
        self.assertEqual(c1.get_attribute('border_position'), pygame_menu.widgets.core.widget.WIDGET_FULL_BORDER)
        self.assertEqual(c1.get_attribute('border_width'), 1)
        self.assertEqual(c1.get_attribute('column'), 1)
        self.assertEqual(c1.get_attribute('padding'), (0, 0, 0, 0))
        self.assertEqual(c1.get_attribute('row'), 1)
        self.assertEqual(c1.get_attribute('table'), table)
        self.assertEqual(c1.get_attribute('vertical_position'), pygame_menu.locals.POSITION_NORTH)

        # Update cell
        c5 = table.update_cell_style(2, 2)
        self.assertIsNone(c5._background_color)
        self.assertEqual(c5.get_attribute('background_color'), (0, 255, 0, 255))

        table.update_cell_style(2, 2, background_color='white')
        self.assertEqual(c5._background_color, (255, 255, 255, 255))

        table.update_cell_style(3, 1, background_color='cyan')
        self.assertEqual(c5.get_padding(), (10, 10, 10, 10))
        table.update_cell_style(2, 2, padding=0)
        self.assertEqual(c5.get_padding(), (0, 0, 20, 0))  # vertical position north
        table.update_cell_style(2, 2, vertical_position=pygame_menu.locals.POSITION_CENTER)
        self.assertEqual(c5.get_padding(), (10, 0, 10, 0))  # vertical position north
        table.update_cell_style(2, 2, vertical_position=pygame_menu.locals.POSITION_SOUTH)
        self.assertEqual(c5.get_padding(), (20, 0, 0, 0))  # vertical position north
        table.update_cell_style(1, 1, font_color='white')
        table.draw(surface)
        self.assertEqual(table.get_size(), (158, 110))
        table.update_cell_style(2, 2, padding=50)
        self.assertEqual(table.get_size(), (258, 190))

        # Test align
        c2 = table.get_cell(2, 1)
        self.assertEqual(c2.get_size(), (134, 41))
        self.assertEqual(c2.get_padding(), (0, 58, 0, 59))
        table.update_cell_style(2, 1, align=pygame_menu.locals.ALIGN_LEFT)
        self.assertEqual(c2.get_size(), (134, 41))
        self.assertEqual(c2.get_padding(), (0, 117, 0, 0))
        table.update_cell_style(2, 1, align=pygame_menu.locals.ALIGN_RIGHT)
        self.assertEqual(c2.get_padding(), (0, 0, 0, 117))
        self.assertEqual(c2.get_attribute('border_width'), 1)
        table.update_cell_style(2, 1, border_width=0)
        self.assertEqual(c2.get_attribute('border_width'), 0)
        table.draw(surface)

        # Test hide
        self.assertTrue(c2.is_visible())
        table.hide()
        table.draw(surface)
        self.assertFalse(c2.is_visible())
        table.show()
        self.assertTrue(c2.is_visible())

        # Add and remove row
        self.assertEqual(table.get_size(), (258, 190))
        row3 = table.add_row([12])
        self.assertFalse(table.is_rectangular())
        self.assertEqual(row1.get_total_packed(), 3)
        self.assertEqual(row3.get_total_packed(), 1)
        self.assertEqual(table.get_size(), (258, 231))
        table.remove_row(row3)
        self.assertEqual(table.get_size(), (258, 190))

        # Add new row with an image
        table.update_cell_style(2, 2, padding=0)
        b_image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU)
        b_image.scale(0.1, 0.1)
        row3 = table.add_row(['image', b_image, 'ez'])
        self.assertIsInstance(row3.get_widgets()[1], pygame_menu.widgets.Image)

        # Remove table from menu
        menu.remove_widget(table)

        # Add sub-table
        menu.add.generic_widget(table)
        table2 = menu.add.table(font_size=10)
        table2row1 = table2.add_row([1, 2])
        table2.add_row([3, 4])

        self.assertIn(btn, menu.get_widgets())

        row4 = table.add_row(['sub-table', table2, btn], cell_align=pygame_menu.locals.ALIGN_CENTER,
                             cell_vertical_position=pygame_menu.locals.POSITION_CENTER)
        table.update_cell_style(2, 4, background_color='white')
        self.assertNotIn(btn, menu.get_widgets())
        self.assertEqual(btn.get_frame(), row4)
        self.assertEqual(table2.get_frame(), row4)
        self.assertEqual(table2.get_frame_depth(), 2)
        self.assertEqual(table2row1.get_widgets()[0].get_frame(), table2row1)
        self.assertEqual(table2row1.get_widgets()[0].get_frame_depth(), 4)

        # Try to add an existing row as a new row
        self.assertRaises(AssertionError, lambda: table.add_row([row1]))
        self.assertRaises(AssertionError, lambda: table.add_row([table2row1.get_widgets()[0]]))

        # Update padding
        self.assertEqual(table.get_size(), (265, 201))
        table.set_padding(0)
        self.assertEqual(table.get_size(), (249, 193))

        # Add surface
        new_surface = pygame.Surface((40, 40))
        new_surface.fill((255, 192, 203))
        inner_surface = pygame.Surface((20, 20))
        inner_surface.fill((75, 0, 130))
        new_surface.blit(inner_surface, (10, 10))
        row5 = table.add_row([new_surface, 'epic', new_surface],
                             cell_border_position=pygame_menu.locals.POSITION_SOUTH)

        self.assertIsInstance(row5.get_widgets()[0], pygame_menu.widgets.SurfaceWidget)
        self.assertIsInstance(row5.get_widgets()[1], pygame_menu.widgets.Label)
        self.assertIsInstance(row5.get_widgets()[2], pygame_menu.widgets.SurfaceWidget)
        self.assertEqual(table.get_size(), (249, 234))

        # Create table with fixed surface for testing sizing
        table3 = menu.add.table(background_color='purple')
        table3._draw_cell_borders(surface)
        self.assertRaises(AssertionError, lambda: table3.remove_row(row1))  # Empty table
        table3.add_row([new_surface])
        self.assertRaises(AssertionError, lambda: table3.remove_row(row1))  # Empty table
        self.assertEqual(table3.get_margin(), (0, 0))
        self.assertEqual(table3.get_size(), (56, 48))
        table3.set_padding(False)
        self.assertEqual(table3.get_size(), (40, 40))

        # Test others
        surf_same_table = pygame.Surface((10, 200))
        surf_same_table.fill((0, 0, 0))
        surf_widget = menu.add.surface(surf_same_table)

        # Create frame
        menu._test_print_widgets()
        frame = menu.add.frame_v(300, 300, background_color='yellow', padding=0)
        frame.pack(surf_widget)
        menu.remove_widget(surf_widget)

        self.assertEqual(table._translate_virtual, (0, 0))
        frame.pack(table, align=pygame_menu.locals.ALIGN_CENTER, vertical_position=pygame_menu.locals.POSITION_CENTER)
        self.assertEqual(table._translate_virtual, (25, 33))

        # Add to scrollable frame
        frame2 = menu.add.frame_v(300, 400, max_height=300, background_color='brown')
        menu.remove_widget(frame)
        frame2.pack(table)

        # Add scrollable frame to table
        menu._test_print_widgets()
        frame3 = menu.add.frame_v(200, 200, max_width=100, max_height=100, background_color='cyan')
        self.assertIn(frame3, menu._update_frames)
        row6 = table.add_row([frame3, table3], cell_border_width=0)
        row6_widgs = row6.get_widgets(unpack_subframes=False)
        self.assertIn(frame3, menu._update_frames)
        self.assertEqual(row6.get_widgets(unpack_subframes=False)[1], table3)
        self.assertEqual(table.get_cell(*table.get_cell_column_row(table3)), table3)

        # Remove row6, this should remove table3 from update frames as well
        table.remove_row(row6)
        self.assertNotIn(frame3, menu._update_frames)

        # Check value
        self.assertRaises(ValueError, lambda: table.get_value())

        # Remove table from scrollable frame
        self.assertEqual(row6.get_total_packed(), 2)
        row7 = table.add_row(row6)
        self.assertNotEqual(row6, row7)
        self.assertEqual(row6_widgs, row7.get_widgets(unpack_subframes=False))
        self.assertEqual(row6.get_total_packed(), 0)
        self.assertIn(frame3, menu._update_frames)

        # Unpack table from frame
        frame2.unpack(table)
        self.assertIn(frame3, menu._update_frames)
        self.assertTrue(table.is_floating())
        table.set_float(False)
        menu._test_print_widgets()

        img = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_METAL)
        img.scale(0.2, 0.2)
        table.add_row(img)

        # Test single position
        table.update_cell_style(1, 1, border_position=pygame_menu.locals.POSITION_SOUTH)

        # Test update using -1 column/row
        self.assertEqual(len(table.update_cell_style(-1, 1)), 3)
        self.assertEqual(len(table.update_cell_style(-1, 7)), 1)
        self.assertEqual(len(table.update_cell_style(1, -1)), 7)
        self.assertEqual(len(table.update_cell_style(-1, -1)), 18)
        self.assertEqual(len(table.update_cell_style(1, [1, -1])), 7)
        self.assertEqual(len(table.update_cell_style(1, [1, 1])), 1)
        self.assertEqual(len(table.update_cell_style([1, -1], [1, -1])), 18)
        self.assertRaises(AssertionError, lambda: self.assertEqual(len(table.update_cell_style([1, 7], [1, -1])), 18))
        self.assertEqual(len(table.update_cell_style([1, 2], 1)), 2)
        self.assertFalse(table.update([]))

    def test_table_update(self) -> None:
        """
        Test table update.
        """
        menu = MenuUtils.generic_menu()
        btn = menu.add.button('click', lambda: print('clicked'))
        sel = menu.add.dropselect('sel', items=[('a', 'a'), ('b', 'b')])
        table = menu.add.table()
        table.add_row([btn, sel])
        menu.render()
        menu.draw(surface)
        self.assertEqual(table._update_widgets, [btn, sel])
        self.assertRaises(AssertionError, lambda: table.add_row([table]))
        f = menu.add.frame_h(100, 100)
        f._relax = True
        f.pack(table)
        self.assertRaises(AssertionError, lambda: table.add_row([f]))

    def test_value(self) -> None:
        """
        Test table value.
        """
        menu = MenuUtils.generic_menu()
        table = menu.add.table()
        self.assertRaises(ValueError, lambda: table.get_value())
        self.assertRaises(ValueError, lambda: table.set_value('value'))
        self.assertFalse(table.value_changed())
        table.reset_value()
