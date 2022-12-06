"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGET - DROPSELECT
Test DropSelect and DropSelectMultiple widgets.
"""

__all__ = ['DropSelectWidgetTest']

from test._utils import MenuUtils, surface, PygameEventUtils, PYGAME_V2, \
    THEME_NON_FIXED_TITLE, BaseTest

import pygame
import pygame_menu
import pygame_menu.controls as ctrl

from pygame_menu.locals import ORIENTATION_VERTICAL, FINGERDOWN
from pygame_menu.widgets import DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA, \
    DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN, DROPSELECT_MULTIPLE_SFORMAT_TOTAL
from pygame_menu.widgets.core.widget import WidgetTransformationNotImplemented


class DropSelectWidgetTest(BaseTest):

    def test_dropselect(self) -> None:
        """
        Test dropselect widget.
        """
        menu = MenuUtils.generic_menu(mouse_motion_selection=True, theme=THEME_NON_FIXED_TITLE)
        items = [('This is a really long selection item', 1), ('epic', 2)]
        for i in range(10):
            items.append((f'item{i + 1}', i + 1))
        # noinspection SpellCheckingInspection
        drop = pygame_menu.widgets.DropSelect('dropsel', items,
                                              selection_option_font_size=int(0.75 * menu._theme.widget_font_size),
                                              placeholder_add_to_selection_box=False,
                                              selection_option_font=menu._theme.widget_font)
        menu.add.generic_widget(drop, configure_defaults=True)
        self.assertEqual(drop._selection_box_width, (207 if PYGAME_V2 else 208))
        self.assertEqual(drop.get_frame_depth(), 0)
        drop.render()
        self.assertTrue(drop._drop_frame.is_scrollable)
        drop_frame = drop._drop_frame

        self.assertIn(drop_frame, menu._update_frames)
        if PYGAME_V2:
            # noinspection SpellCheckingInspection
            self.assertEqual(menu._test_widgets_status(), (
                (('DropSelect-dropsel',
                  (0, 0, 0, 123, 149, 354, 49, 123, 304, 123, 149),
                  (1, 0, 1, 1, 0, 0, 0),
                  ('Frame',
                   (-1, -1, -1, 261, 193, 207, 136, 261, 348, 261, 193),
                   (0, 0, 0, 0, 1, 0, 0),
                   (-1, -1)),
                  ('Button-This is a really long selection item',
                   (-1, -1, -1, 0, -1, 356, 40, 261, 348, 0, 154),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-epic',
                   (-1, -1, -1, 0, 38, 356, 40, 261, 386, 0, 193),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item1',
                   (-1, -1, -1, 0, 77, 356, 40, 261, 425, 0, 232),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item2',
                   (-1, -1, -1, 0, 116, 356, 40, 261, 348, 0, 271),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item3',
                   (-1, -1, -1, 0, 155, 356, 40, 261, 348, 0, 310),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item4',
                   (-1, -1, -1, 0, 194, 356, 40, 261, 348, 0, 349),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item5',
                   (-1, -1, -1, 0, 233, 356, 40, 261, 348, 0, 388),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item6',
                   (-1, -1, -1, 0, 272, 356, 40, 261, 348, 0, 427),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item7',
                   (-1, -1, -1, 0, 311, 356, 40, 261, 348, 0, 466),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item8',
                   (-1, -1, -1, 0, 350, 356, 40, 261, 348, 0, 505),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item9',
                   (-1, -1, -1, 0, 389, 356, 40, 261, 348, 0, 544),
                   (1, 0, 0, 0, 0, 1, 1)),
                  ('Button-item10',
                   (-1, -1, -1, 0, 428, 356, 40, 261, 348, 0, 583),
                   (1, 0, 0, 0, 0, 1, 1))),)
            ))

        self.assertEqual(drop._drop_frame.get_attribute('height'), (135 if PYGAME_V2 else 138))
        self.assertEqual(drop._drop_frame.get_attribute('width'), (187 if PYGAME_V2 else 188))

        # Test events
        self.assertFalse(drop.active)
        self.assertFalse(drop._drop_frame.is_visible())
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertTrue(drop.active)
        self.assertTrue(drop._drop_frame.is_visible())
        self.assertEqual(drop.get_index(), -1)
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        self.assertEqual(drop.get_index(), 0)
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertFalse(drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True, testmode=False)))
        self.assertFalse(drop.active)
        self.assertFalse(drop._drop_frame.is_visible())
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        self.assertEqual(drop.get_index(), 0)
        self.assertFalse(drop.active)
        drop.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))  # Enable
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))
        self.assertFalse(drop.active)
        drop.update(PygameEventUtils.key(pygame.K_TAB, keydown=True))  # Enable
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))  # Not infinite
        self.assertEqual(drop.get_index(), 0)
        scroll_values = [-1, 0, 0, 0.114, 0.228, 0.33, 0.447, 0.561, 0.664, 0.778, 0.895, 0.997]
        for i in range(1, 12):
            drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
            self.assertEqual(drop.get_index(), i)
            if PYGAME_V2:
                self.assertEqual(drop.get_scroll_value_percentage(ORIENTATION_VERTICAL), scroll_values[i])

        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))  # Not infinite
        self.assertEqual(drop.get_index(), 11)  # Not infinite
        if PYGAME_V2:
            self.assertEqual(drop.get_scroll_value_percentage(ORIENTATION_VERTICAL), 0.997)

        # Mouseup over rect returns True updated status
        self.assertTrue(drop.active)
        self.assertTrue(drop.update(PygameEventUtils.middle_rect_click(drop.get_focus_rect(), evtype=pygame.MOUSEBUTTONDOWN)))
        self.assertTrue(drop.active)

        # Touch also does the same trick
        if PYGAME_V2:
            drop._touchscreen_enabled = True
            self.assertTrue(drop.update(PygameEventUtils.middle_rect_click(drop.get_focus_rect(), menu=menu, evtype=FINGERDOWN)))
            self.assertTrue(drop.active)

        # Scroll to bottom and close, then open again, this should scroll to current selected
        drop.scrollh(0)
        drop.scrollv(0)
        self.assertEqual(drop._drop_frame.get_scroll_value_percentage(ORIENTATION_VERTICAL), 0)
        drop._toggle_drop()
        drop._toggle_drop()
        if PYGAME_V2:
            self.assertEqual(drop._drop_frame.get_scroll_value_percentage(ORIENTATION_VERTICAL), 0.997)

        # Click drop box should toggle it
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.middle_rect_click(drop))
        self.assertFalse(drop.active)
        drop.update(PygameEventUtils.middle_rect_click(drop))
        self.assertTrue(drop.active)

        # Click middle option
        drop.update(PygameEventUtils.middle_rect_click(drop.get_focus_rect()))
        self.assertEqual(drop.get_index(), 10)
        self.assertFalse(drop.active)

        # Touch middle
        self.assertTrue(drop._touchscreen_enabled)
        drop.update(PygameEventUtils.middle_rect_click(drop.get_focus_rect(), evtype=pygame.FINGERUP, menu=drop.get_menu()))
        self.assertTrue(drop.active)

        # Test focus
        if not drop.active:
            drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        if PYGAME_V2:
            self.assertEqual(menu._draw_focus_widget(surface, drop),
                             {1: ((0, 0), (600, 0), (600, 307), (0, 307)),
                              2: ((0, 308), (260, 308), (260, 483), (0, 483)),
                              3: ((468, 308), (600, 308), (600, 483), (468, 483)),
                              4: ((0, 484), (600, 484), (600, 600), (0, 600))}
                             )
        else:
            self.assertEqual(menu._draw_focus_widget(surface, drop),
                             {1: ((0, 0), (600, 0), (600, 305), (0, 305)),
                              2: ((0, 306), (259, 306), (259, 489), (0, 489)),
                              3: ((469, 306), (600, 306), (600, 489), (469, 489)),
                              4: ((0, 490), (600, 490), (600, 600), (0, 600))}
                             )

        # Test change items
        drop_frame = drop._drop_frame
        drop._drop_frame = None
        self.assertEqual(drop.get_scroll_value_percentage('any'), -1)
        self.assertRaises(pygame_menu.widgets.widget.dropselect._SelectionDropNotMadeException, lambda: drop._check_drop_made())
        drop._drop_frame = drop_frame
        drop.update_items([])
        drop._make_selection_drop()
        self.assertEqual(drop._drop_frame.get_attribute('height'), 0)
        self.assertEqual(drop._drop_frame.get_attribute('width'), 0)
        self.assertFalse(drop.active)
        drop._toggle_drop()
        self.assertFalse(drop.active)
        fr = drop.get_focus_rect()
        r = drop.get_rect(apply_padding=False, to_real_position=True)
        self.assertEqual(fr.x, r.x)
        self.assertEqual(fr.y, r.y)
        self.assertEqual(fr.width + drop._selection_box_border_width, r.width)
        self.assertEqual(fr.height, r.height)
        self.assertEqual(drop.get_index(), -1)
        self.assertRaises(ValueError, lambda: drop.get_value())
        drop._up()
        self.assertEqual(drop.get_index(), -1)
        drop._down()
        self.assertEqual(drop.get_index(), -1)

        # Check previous frame not in scrollable frames
        self.assertFalse(drop._drop_frame.is_scrollable)
        self.assertNotIn(drop_frame, menu._update_frames)

        # Restore previous values
        drop.update_items(items)
        self.assertEqual(drop.get_index(), -1)

        # Apply transforms
        drop.translate(1, 1)
        self.assertEqual(drop.get_translate(), (1, 1))
        drop.translate(0, 0)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: drop.rotate(10))
        self.assertEqual(drop._angle, 0)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: drop.resize(10, 10))
        self.assertFalse(drop._scale[0])
        self.assertEqual(drop._scale[1], 1)
        self.assertEqual(drop._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: drop.scale(100, 100))
        self.assertFalse(drop._scale[0])
        self.assertEqual(drop._scale[1], 1)
        self.assertEqual(drop._scale[2], 1)

        self.assertRaises(WidgetTransformationNotImplemented, lambda: drop.flip(True, True))
        self.assertFalse(drop._flip[0])
        self.assertFalse(drop._flip[1])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: drop.set_max_width(100))
        self.assertIsNone(drop._max_width[0])

        self.assertRaises(WidgetTransformationNotImplemented, lambda: drop.set_max_height(100))
        self.assertIsNone(drop._max_height[0])
        self.assertFalse(drop.active)

        # Add margin
        vm = menu.add.vertical_margin(500)
        self.assertEqual(vm.get_height(), 500)

        # Add drop from widget manager, this has the placeholder button
        drop2 = menu.add.dropselect('drop2', items, dropselect_id='2', selection_infinite=True,
                                    selection_option_font_size=int(0.75 * menu._theme.widget_font_size))
        self.assertEqual(drop2._tab_size, menu._theme.widget_tab_size)
        for btn in drop2._option_buttons:
            self.assertEqual(btn._tab_size, menu._theme.widget_tab_size)
        self.assertEqual(drop2._drop_frame._tab_size, 4)
        self.assertEqual(drop2.get_id(), '2')
        self.assertEqual(menu.get_scrollarea().get_scroll_value_percentage(ORIENTATION_VERTICAL), 0)
        self.assertTrue(drop._open_bottom)
        self.assertFalse(drop2._open_bottom)

        # Move to bottom
        menu.get_scrollarea().scroll_to(ORIENTATION_VERTICAL, 1)
        menu.render()
        self.assertTrue(drop._open_bottom)
        self.assertFalse(drop2._open_bottom)
        menu.select_widget(drop2)
        drop2._toggle_drop()

        self.assertEqual(drop2.get_position(), ((132, 554) if PYGAME_V2 else (131, 555)))
        self.assertEqual(drop2._drop_frame.get_attribute('height'), 117 if PYGAME_V2 else 120)
        self.assertEqual(drop2._drop_frame.get_attribute('width'), 187 if PYGAME_V2 else 188)

        # Test infinite
        self.assertTrue(drop2.active)
        self.assertEqual(drop2.get_index(), -1)
        drop2._down()
        self.assertEqual(drop2.get_index(), 11)
        drop2.draw(surface)
        drop._index = -1
        drop2._up()
        self.assertEqual(drop2.get_index(), 0)
        drop2._up()
        self.assertEqual(drop2.get_index(), 1)
        drop2._down()
        self.assertEqual(drop2.get_index(), 0)
        drop2._down()
        self.assertEqual(drop2.get_index(), 11)
        drop2._up()
        self.assertEqual(drop2.get_index(), 0)
        drop2.set_value('item6')
        self.assertEqual(drop2.get_index(), 7)

        drop2.readonly = True
        drop2._up()
        self.assertEqual(drop2.get_index(), 7)
        drop2._down()
        self.assertEqual(drop2.get_index(), 7)
        drop2.readonly = False
        menu.render()
        self.assertEqual(drop2.get_scroll_value_percentage(ORIENTATION_VERTICAL), 0.606 if PYGAME_V2 else 0.603)
        drop2.reset_value()
        self.assertTrue(drop2.active)
        self.assertEqual(drop2.get_index(), -1)
        drop2.set_scrollarea(drop2.get_scrollarea())

        if PYGAME_V2:
            self.assertEqual(
                menu._draw_focus_widget(surface, drop2),
                {1: ((0, 0), (600, 0), (600, 338), (0, 338)),
                 2: ((0, 339), (239, 339), (239, 496), (0, 496)),
                 3: ((447, 339), (600, 339), (600, 496), (447, 496)),
                 4: ((0, 497), (600, 497), (600, 600), (0, 600))}
            )

        menu.draw(surface)
        self.assertIsNone(drop2.get_frame())
        self.assertEqual(drop2.last_surface, menu._widgets_surface)  # Outside frame, must be the widgets surface

        # Add drop inside frame
        f = menu.add.frame_v(400, 500, max_height=200, background_color=(0, 0, 255))
        f.pack(drop2)
        self.assertEqual(drop2.get_scrollarea(), f.get_scrollarea(inner=True))
        self.assertEqual(drop2._drop_frame.get_scrollarea(), f.get_scrollarea(inner=True))
        self.assertEqual(drop2.get_scrollarea().get_parent(), menu.get_scrollarea())
        self.assertEqual(drop2._drop_frame.get_scrollarea().get_parent(), menu.get_scrollarea())
        drop2.update_items([('optionA', 1), ('optionB', 2)])

        if PYGAME_V2:
            self.assertEqual(drop2._get_status(), (
                ('DropSelect-drop2',
                 (0, 2, 3, 0, 0, 332, 49, 88, 308, 0, -242),
                 (1, 0, 1, 1, 0, 1, 1),
                 ('Frame',
                  (-1, -1, -1, 116, 44, 207, 100, 204, 352, 116, -198),
                  (0, 0, 0, 0, 0, 1, 1),
                  (-1, -1)),
                 ('Button-optionA',
                  (-1, -1, -1, 116, 77, 207, 34, 204, 385, 116, -165),
                  (1, 0, 0, 0, 0, 1, 2)),
                 ('Button-optionB',
                  (-1, -1, -1, 116, 110, 207, 34, 204, 418, 116, -132),
                  (1, 0, 0, 0, 0, 1, 2)))
            ))

        self.assertEqual(drop2._drop_frame.get_attribute('height'), 100 if PYGAME_V2 else 103)
        self.assertEqual(drop2._drop_frame.get_attribute('width'), 207 if PYGAME_V2 else 208)
        self.assertEqual(drop2.get_scrollarea().get_parent_scroll_value_percentage(ORIENTATION_VERTICAL), (0, 1))
        self.assertTrue(drop2._open_bottom)

        # Test onchange
        test = [-1, False]

        drop2.set_default_value(0)

        def test_change(item, v) -> None:
            """
            Test change.
            """
            assert item[0][1] == v
            test[0] = item[0][0]

        def test_apply(item, v) -> None:
            """
            Test apply.
            """
            assert item[0][1] == v
            test[1] = not test[1]

        drop2.set_onchange(test_change)
        drop2.set_onreturn(test_apply)
        drop2._toggle_drop()
        self.assertEqual(drop2.get_index(), -1)
        self.assertEqual(test[0], -1)
        drop2._up()
        self.assertEqual(test[0], 'optionA')
        drop2._up()
        self.assertEqual(test[0], 'optionB')
        drop2._up()
        self.assertEqual(test[0], 'optionA')
        self.assertFalse(test[1])
        drop2.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))  # Now it's closed
        self.assertTrue(test[1])
        self.assertFalse(drop2.active)
        drop2.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))  # This only opens but not apply
        self.assertTrue(test[1])
        self.assertTrue(drop2.active)
        menu.draw(surface)
        self.assertEqual(drop2.get_frame(), f)
        self.assertEqual(drop2.last_surface, f.get_surface())  # Frame surface as drop is not in middle
        drop2.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))  # Now applies
        self.assertFalse(test[1])
        self.assertFalse(drop2.active)

        # Unpack from frame
        f.unpack(drop2)
        self.assertTrue(drop2.is_floating())
        drop2.set_float(False)
        self.assertEqual(drop2._drop_frame.get_attribute('height'), 100 if PYGAME_V2 else 103)
        self.assertEqual(drop2._drop_frame.get_attribute('width'), 207 if PYGAME_V2 else 208)

        # Test close if mouse clicks outside
        menu.select_widget(drop)
        drop._toggle_drop()
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.mouse_click(0, 0))
        self.assertFalse(drop.active)

        # Set drop in middle
        if PYGAME_V2:
            self.assertEqual(drop._drop_frame.get_position(), (251, 45))
            self.assertEqual(drop.get_focus_rect(), pygame.Rect(121, 160, 337, 41))

        drop._open_middle = True
        menu.render()

        # For this test, hide all widgets except drop
        # for w in menu.get_widgets():
        #     w.hide()
        # drop.show()

        if PYGAME_V2:
            self.assertEqual(drop._drop_frame.get_position(), (196, 105))
            self.assertEqual(drop.get_focus_rect(), pygame.Rect(121, 160, 337, 41))

        scr = drop._drop_frame.get_scrollarea()
        sfr = drop._drop_frame.get_frame()

        # Add drop to frame
        f.pack(drop)
        menu.render()
        self.assertEqual(drop._drop_frame.get_scrollarea(), scr)
        self.assertEqual(drop._drop_frame.get_frame(), sfr)
        if PYGAME_V2:
            self.assertEqual(drop._drop_frame.get_position(), (196, 453))
            self.assertEqual(drop.get_focus_rect(), pygame.Rect(96, 312, 337, 41))

        self.assertFalse(drop.active)
        drop._toggle_drop()
        menu.render()
        menu.draw(surface)
        self.assertEqual(drop.last_surface, menu._widgets_surface)  # Menu surface as drop is in middle
        if PYGAME_V2:
            self.assertEqual(
                menu._draw_focus_widget(surface, drop),
                {1: ((0, 0), (600, 0), (600, 259), (0, 259)),
                 2: ((0, 260), (195, 260), (195, 394), (0, 394)),
                 3: ((403, 260), (600, 260), (600, 394), (403, 394)),
                 4: ((0, 395), (600, 395), (600, 600), (0, 600))}
            )

        drop._toggle_drop()

        drop2._open_middle = True
        menu.render()
        menu.select_widget(drop2)
        drop2._toggle_drop()
        menu.draw(surface)
        self.assertEqual(drop2.last_surface, menu._widgets_surface)
        if PYGAME_V2:
            self.assertEqual(drop2._drop_frame.get_position(), (196, 519))
            self.assertEqual(drop2.get_focus_rect(), pygame.Rect(196, 277, 207, 99))

        # Disable focus
        menu._mouse_motion_selection = False

        # As drop1 is scrollable, remove from menu, this should remove the widget too
        drop_frame = drop._drop_frame
        self.assertIn(drop_frame, menu._update_frames)
        menu.remove_widget(drop)
        self.assertNotIn(drop_frame, menu._update_frames)

        def draw_rect() -> None:
            """
            Draw absolute rect on surface for testing purposes.
            """
            # surface.fill((255, 0, 0), drop2.get_focus_rect())
            # surface.fill((0, 0, 255), drop2.get_scrollarea().get_absolute_view_rect())
            # surface.fill((255, 255, 0), drop2.get_scrollarea().get_absolute_view_rect().clip(drop.get_focus_rect()))
            return

        menu.get_decorator().add_callable(draw_rect, prev=False, pass_args=False)

        # Test active with different menu settings
        menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
        menu_theme.title_fixed = False
        menu_theme.title_offset = (5, -2)
        menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        menu_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS_LIGHT
        menu_theme.widget_font_size = 20

        menu2 = MenuUtils.generic_menu(theme=menu_theme, width=400)
        menu2.add.vertical_margin(1000)

        drop3 = menu2.add.dropselect_multiple(
            title='Pick 3 colors',
            items=[('Black', (0, 0, 0)),
                   ('Blue', (0, 0, 255)),
                   ('Cyan', (0, 255, 255)),
                   ('Fuchsia', (255, 0, 255)),
                   ('Green', (0, 255, 0)),
                   ('Red', (255, 0, 0)),
                   ('White', (255, 255, 255)),
                   ('Yellow', (255, 255, 0))],
            dropselect_multiple_id='pickcolors',
            open_middle=True,
            max_selected=3
        )
        self.assertEqual(drop3.get_focus_rect(), pygame.Rect(108, 468, 320, 28))

        # Translate the menu, this should also modify focus
        menu2.translate(100, 50)
        self.assertEqual(drop3.get_focus_rect(), pygame.Rect(108 + 100, 468 + 50, 320, 28))
        menu2.translate(100, 150)
        self.assertEqual(drop3.get_focus_rect(), pygame.Rect(108 + 100, 468 + 150, 320, 28))
        menu2.translate(0, 0)
        self.assertEqual(drop3.get_focus_rect(), pygame.Rect(108, 468, 320, 28))

        # Test update list
        def remove_selection_item(select: 'pygame_menu.widgets.DropSelect'):
            """
            Update list event.
            """
            if select.get_index() == -1:
                return
            s_val = select.get_value()
            _items = select.get_items()
            _items.pop(_items.index(s_val[0]))
            select.update_items(_items)
            print(f'removed {len(_items)} left')

        menu = MenuUtils.generic_menu()

        select1 = menu.add.dropselect('Subject Id',
                                      items=[('a',), ('b',), ('c',), ('d',), ('e',), ('f',)],
                                      dropselect_id='s0')
        b_sel = menu.add.button('One', remove_selection_item, select1)

        b_sel.apply()
        select1.set_value(0)
        self.assertEqual(select1.get_value(), (('a',), 0))
        b_sel.apply()
        self.assertEqual(select1.get_index(), -1)
        self.assertEqual(select1.get_items(), [('b',), ('c',), ('d',), ('e',), ('f',)])
        b_sel.apply()

        # Update by value
        select1.set_value('b')
        self.assertEqual(select1.get_index(), 0)
        select1.set_value('e')
        self.assertEqual(select1.get_index(), 3)
        self.assertRaises(ValueError, lambda: select1.set_value('unknown'))
        b_sel.apply()  # to -1

        select1.active = True
        select1.show()

        # Test configured
        select1.configured = False
        self.assertRaises(RuntimeError, lambda: select1._make_selection_drop())
        select1.configured = True
        select1.readonly = True
        self.assertFalse(select1.update([]))

        # Test touchscreen support
        if not PYGAME_V2:
            return

        menu = MenuUtils.generic_menu(touchscreen=True)
        sel = menu.add.dropselect('Subject Id', items=[('a',), ('b',), ('c',), ('d',), ('e',), ('f',)], dropselect_id='s0')
        menu.add.button('One', remove_selection_item, sel)

        # Select by touch
        touch_sel = sel.get_rect(to_real_position=True).center
        self.assertEqual(sel.get_index(), -1)
        self.assertFalse(sel.active)

        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1], menu=menu))
        self.assertTrue(sel.active)

        # Touch null option
        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 40, menu=menu))
        self.assertTrue(sel.active)

        # Select option a
        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 80, menu=menu))
        self.assertEqual(sel.get_index(), 0)
        self.assertFalse(sel.active)

        # Touch outside
        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 400, menu=menu))
        self.assertFalse(sel.active)

        # Touch button
        menu.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 40, menu=menu, evtype=FINGERDOWN))
        menu.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 40, menu=menu))

        # Touch again outside
        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 400, menu=menu))
        self.assertFalse(sel.active)

        # Select
        sel.select(update_menu=True)
        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1], menu=menu))
        self.assertTrue(sel.active)

        # Touch but by menu events, unselect current and force selection
        sel.active = False
        menu._widget_selected_update = False
        menu.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1], menu=menu))
        self.assertTrue(sel.active)
        menu.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1], menu=menu))
        self.assertFalse(sel.active)

        # Mouse click
        menu.update(PygameEventUtils.mouse_click(touch_sel[0], touch_sel[1]))
        self.assertTrue(sel.active)
        menu.update(PygameEventUtils.mouse_click(touch_sel[0], touch_sel[1]))
        self.assertFalse(sel.active)
        menu._widget_selected_update = True

        # Update the number of items
        sel.update_items([('a',), ('b',)])
        self.assertFalse(sel.active)
        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1], menu=menu))
        self.assertTrue(sel.active)
        self.assertEqual(sel.get_index(), -1)
        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 80, menu=menu))
        self.assertEqual(sel.get_index(), 0)
        self.assertFalse(sel.active)
        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1], menu=menu))
        self.assertTrue(sel.active)
        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1] + 80, menu=menu, evtype=pygame.FINGERDOWN))
        sel.update(PygameEventUtils.touch_click(touch_sel[0], touch_sel[1], menu=menu))
        self.assertFalse(sel.active)

        # Ignore buttons if not active
        self.assertFalse(sel.update(PygameEventUtils.key(pygame_menu.controls.KEY_MOVE_UP, keydown=True)))

    def test_dropselect_multiple(self) -> None:
        """
        Test dropselect multiple widget.
        """
        theme = pygame_menu.themes.THEME_DEFAULT.copy()
        theme.widget_font_size = 25
        menu = MenuUtils.generic_menu(mouse_motion_selection=True, theme=theme)
        items = [('This is a really long selection item', 1), ('epic', 2)]
        for i in range(10):
            items.append((f'item{i + 1}', i + 1))
        # noinspection SpellCheckingInspection
        drop = pygame_menu.widgets.DropSelectMultiple('dropsel', items, open_middle=True, selection_box_height=5)
        self.assertNotEqual(id(items), id(drop._items))
        menu.add.generic_widget(drop, configure_defaults=True)
        self.assertEqual(drop._selection_box_width, 225)

        # Check drop is empty
        self.assertEqual(drop.get_value(), ([], []))
        self.assertEqual(drop.get_index(), [])
        self.assertEqual(drop._get_current_selected_text(), 'Select an option')

        # Check events
        self.assertFalse(drop.active)
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertTrue(drop.active)
        self.assertEqual(drop._index, -1)
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))  # Index is -1
        self.assertFalse(drop.active)
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        self.assertEqual(drop._index, 0)
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        self.assertEqual(drop._index, 1)

        # Apply on current
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertEqual(drop.get_value(), ([('epic', 2)], [1]))
        self.assertEqual(drop.get_index(), [1])
        self.assertEqual(drop._get_current_selected_text(), '1 selected')
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertEqual(drop.get_value(), ([('epic', 2), ('item2', 2)], [1, 3]))
        self.assertEqual(drop._get_current_selected_text(), '2 selected')

        # Change selection type
        drop._selection_placeholder_format = DROPSELECT_MULTIPLE_SFORMAT_LIST_COMMA
        self.assertEqual(drop._get_current_selected_text(), 'epic,item2 selected')
        drop._selection_placeholder_format = DROPSELECT_MULTIPLE_SFORMAT_LIST_HYPHEN
        self.assertEqual(drop._get_current_selected_text(), 'epic-item2 selected')
        drop._selection_placeholder_format = '+'
        self.assertEqual(drop._get_current_selected_text(), 'epic+item2 selected')

        def format_string_list(items_list) -> str:
            """
            Receives the items list string and returns a function.

            :param items_list: Items list
            :return: Join string
            """
            if len(items_list) == 1:
                return items_list[0]
            elif len(items_list) == 2:
                return items_list[0] + ' and ' + items_list[1]
            return 'overflow'

        drop._selection_placeholder_format = format_string_list
        self.assertEqual(drop._get_current_selected_text(), 'epic and item2 selected')

        # Invalid format
        drop._selection_placeholder_format = 1
        self.assertRaises(ValueError, lambda: drop._get_current_selected_text())
        drop._selection_placeholder_format = lambda: print('nice')
        self.assertRaises(ValueError, lambda: drop._get_current_selected_text())
        drop._selection_placeholder_format = lambda x: 1
        self.assertRaises(AssertionError, lambda: drop._get_current_selected_text())

        # Back to default
        drop._selection_placeholder_format = DROPSELECT_MULTIPLE_SFORMAT_TOTAL

        # Click item 2, this should unselect
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.middle_rect_click(drop._option_buttons[3]))
        self.assertEqual(drop.get_value(), ([('epic', 2)], [1]))
        self.assertEqual(drop._get_current_selected_text(), '1 selected')
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        self.assertEqual(drop._index, 4)
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertEqual(drop.get_value(), ([('epic', 2), ('item3', 3)], [1, 4]))
        self.assertEqual(drop._get_current_selected_text(), '2 selected')

        # Close
        drop.update(PygameEventUtils.key(pygame.K_ESCAPE, keydown=True))
        self.assertFalse(drop.active)
        self.assertEqual(drop.get_value(), ([('epic', 2), ('item3', 3)], [1, 4]))
        self.assertEqual(drop._get_current_selected_text(), '2 selected')

        # Change drop selected text method

        # Set max limit
        drop._max_selected = 3
        self.assertEqual(drop.get_total_selected(), 2)
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertEqual(drop.get_total_selected(), 3)
        self.assertTrue(drop.active)
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_UP, keydown=True))
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))
        self.assertEqual(drop.get_total_selected(), 3)  # Limit reached
        self.assertEqual(drop.get_value(), ([('epic', 2), ('item3', 3), ('item4', 4)], [1, 4, 5]))
        drop.update(PygameEventUtils.key(ctrl.KEY_MOVE_DOWN, keydown=True))
        drop.update(PygameEventUtils.key(ctrl.KEY_APPLY, keydown=True))  # Unselect previous
        self.assertEqual(drop.get_total_selected(), 2)  # Limit reached
        self.assertEqual(drop.get_value(), ([('epic', 2), ('item3', 3)], [1, 4]))

        # Update elements
        drop.update_items([('This is a really long selection item', 1), ('epic', 2)])
        self.assertEqual(drop.get_value(), ([], []))
        self.assertEqual(drop._get_current_selected_text(), 'Select an option')
        drop.set_value(1, process_index=True)
        self.assertEqual(drop.get_value(), ([('epic', 2)], [1]))
        drop.set_value('This is a really long selection item', process_index=True)
        self.assertEqual(drop.get_value(), ([('This is a really long selection item', 1), ('epic', 2)], [0, 1]))
        self.assertEqual(drop._get_current_selected_text(), '2 selected')
        drop.set_default_value(1)
        self.assertEqual(drop.get_value(), ([('epic', 2)], [1]))
        self.assertEqual(drop._get_current_selected_text(), '1 selected')

        # Use manager
        drop2 = menu.add.dropselect_multiple('nice', [('This is a really long selection item', 1), ('epic', 2)],
                                             placeholder_selected='nice {0}', placeholder='epic', max_selected=1)
        self.assertEqual(drop2._selection_box_width, 134)
        self.assertEqual(drop2._get_current_selected_text(), 'epic')
        drop2.set_value('epic', process_index=True)
        self.assertEqual(drop2.get_index(), [1])
        self.assertEqual(drop2._get_current_selected_text(), 'nice 1')
        drop2.set_value(0, process_index=True)
        self.assertEqual(drop2.get_index(), [1])
        self.assertEqual(drop2._get_current_selected_text(), 'nice 1')
        self.assertEqual(drop2._default_value, [])
        self.assertEqual(drop2._index, 0)
        self.assertRaises(ValueError, lambda: drop2.set_value('not epic'))

        # Reset
        drop2.reset_value()
        self.assertEqual(drop2._get_current_selected_text(), 'epic')
        self.assertEqual(drop2._default_value, [])
        self.assertEqual(drop2._index, -1)
        self.assertEqual(drop2.get_index(), [])
        self.assertNotEqual(id(drop2._default_value), id(drop2._selected_indices))

        menu.select_widget(drop2)
        self.assertTrue(drop2.update(PygameEventUtils.key(pygame.K_TAB, keydown=True)))

        # Test hide
        self.assertTrue(drop2._drop_frame.is_visible())
        self.assertTrue(drop2.active)
        drop2.hide()  # Hiding selects the other widget
        self.assertEqual(menu.get_selected_widget(), drop)
        self.assertFalse(drop2._drop_frame.is_visible())
        self.assertFalse(drop2.active)
        drop2.show()
        self.assertFalse(drop2._drop_frame.is_visible())
        self.assertFalse(drop2.active)
        self.assertEqual(menu.get_selected_widget(), drop)
        menu.select_widget(drop2)
        drop2._toggle_drop()
        self.assertTrue(drop2.active)
        self.assertTrue(drop2._drop_frame.is_visible())

        # Test change
        test = [-1]

        def onchange(value) -> None:
            """
            Test onchange.
            """
            test[0] = value[1]

        drop2.set_onchange(onchange)

        # Pick any option
        menu.render()
        self.assertEqual(test, [-1])
        drop2._option_buttons[0].apply()
        self.assertEqual(test[0], [0])
        drop2._option_buttons[0].apply()
        self.assertEqual(test[0], [])
        drop2._option_buttons[0].apply()
        drop2._option_buttons[1].apply()
        self.assertEqual(test[0], [0])  # As max selected is only 1
        drop2._max_selected = 2
        drop2._option_buttons[1].apply()
        self.assertEqual(test[0], [0, 1])

        # Test none drop frame
        drop2._drop_frame = None
        self.assertEqual(drop2.get_scroll_value_percentage('any'), -1)

        # Test format option from manager
        menu._theme.widget_background_inflate_to_selection = True
        menu._theme.widget_background_inflate = 0
        # menu._theme.widget_border_inflate = 0
        menu._theme.widget_margin = 0
        drop2 = menu.add.dropselect_multiple('nice', [('This is a really long selection item', 1), ('epic', 2)],
                                             placeholder_selected='nice {0}', placeholder='epic', max_selected=1,
                                             selection_placeholder_format=lambda x: 'not EPIC')
        self.assertEqual(drop2._get_current_selected_text(), 'epic')
        drop2.set_value('epic', process_index=True)
        self.assertEqual(drop2._get_current_selected_text(), 'nice not EPIC')
        self.assertEqual(drop2.get_margin(), (0, 0))
        self.assertEqual(drop2._background_inflate, (0, 0))
        self.assertEqual(drop2._border_inflate, (0, 0))
        menu._theme.widget_background_inflate_to_selection = False

        # Process index
        drop2._index = -1
        drop2._process_index()

    def test_value(self) -> None:
        """
        Test dropselect value.
        """
        menu = MenuUtils.generic_menu()
        values = [('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd'), ('e', 'e')]

        drop = menu.add.dropselect('title', items=values)
        self.assertRaises(ValueError, lambda: drop.get_value())
        self.assertFalse(drop.value_changed())
        drop.set_value(0)
        self.assertEqual(drop.get_value(), (('a', 'a'), 0))
        self.assertTrue(drop.value_changed())
        drop.reset_value()
        self.assertEqual(drop._default_value, -1)
        self.assertRaises(ValueError, lambda: drop.get_value())

        drop = menu.add.dropselect('title', items=values, default=1)
        self.assertEqual(drop.get_value(), (('b', 'b'), 1))
        self.assertFalse(drop.value_changed())
        drop.set_value(0)
        self.assertEqual(drop.get_value(), (('a', 'a'), 0))
        self.assertTrue(drop.value_changed())
        drop.reset_value()

        drop_m = menu.add.dropselect_multiple('title', values)
        self.assertEqual(drop_m._default_value, [])
        self.assertEqual(drop_m.get_value(), ([], []))
        self.assertFalse(drop_m.value_changed())
        drop_m.set_value(0, process_index=True)
        self.assertEqual(drop_m.get_value(), ([('a', 'a')], [0]))
        self.assertTrue(drop_m.value_changed())
        drop_m.reset_value()
        self.assertEqual(drop_m.get_value(), ([], []))
        self.assertFalse(drop_m.value_changed())

        drop_m = menu.add.dropselect_multiple('title', values, default=[1, 2])
        self.assertTrue(drop_m._selected_indices, [1, 2])
        self.assertFalse(drop_m.value_changed())
        drop_m._selected_indices = [0, 2]
        self.assertTrue(drop_m.value_changed())
        drop_m.reset_value()
        self.assertTrue(drop_m._selected_indices, [1, 2])
        self.assertFalse(drop_m.value_changed())

    def test_empty_title(self) -> None:
        """
        Test empty title.
        """
        menu = MenuUtils.generic_menu()
        values = [('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd'), ('e', 'e')]
        drop = menu.add.dropselect('', items=values)
        self.assertEqual(drop.get_size(), (309, 49))
        drop = menu.add.dropselect_multiple('', items=values)
        self.assertEqual(drop.get_size(), (309, 49))

    def test_frame_support(self) -> None:
        """
        Test drop selects within frames.
        """
        menu = MenuUtils.generic_menu()

        menu.add.dropselect('Subject Id', items=[('a', 'a'), ('b', 'b'), ('c', 'c')], dropselect_id='s0')
        frame_s = menu.add.frame_h(600, 58)
        frame_s.pack(
            menu.add.dropselect('Subject Id', items=[('a', 'a'), ('b', 'b'), ('c', 'c')], dropselect_id='s1', open_middle=True)
        )
        frame_s.pack(menu.add.button('One', lambda: print('1')))
        frame_t = menu.add.frame_h(600, 58)
        frame_t.pack(
            menu.add.dropselect('Subject Id', items=[('a', 'a'), ('b', 'b'), ('c', 'c')], dropselect_id='s2')
        )
        frame_t.pack(menu.add.button('Two', lambda: print('2')))
        menu.add.dropselect('Subject Id', items=[('a', 'a'), ('b', 'b'), ('c', 'c')], dropselect_id='s3')
        menu.add.dropselect('Subject Id', items=[('a', 'a'), ('b', 'b'), ('c', 'c')], dropselect_id='s4', open_middle=True)

        # Test draw surfaces
        menu.draw(surface)
        # noinspection PyTypeChecker
        s0: 'pygame_menu.widgets.DropSelect' = menu.get_widget('s0')
        # noinspection PyTypeChecker
        s1: 'pygame_menu.widgets.DropSelect' = menu.get_widget('s1')
        surf = menu._widgets_surface
        self.assertTrue(s0.is_selected())
        self.assertEqual(s0.last_surface, surf)
        s0.active = True
        menu.render()
        menu.draw(surface)
        self.assertEqual(s0.last_surface, surf)
        s0._selection_effect_draw_post = True
        menu.render()
        menu.draw(surface)
        s0.draw_after_if_selected(surface)

        s1.select(update_menu=True)
        s1.active = True
        menu.draw(surface)
        self.assertEqual(s1.last_surface, surf)
