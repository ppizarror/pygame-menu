"""
pygame-menu
https://github.com/ppizarror/pygame-menu

TEST WIDGETS
Test general widget properties.
"""

__all__ = ['WidgetsTest']

from test._utils import MenuUtils, surface, PygameEventUtils, test_reset_surface, \
    TEST_THEME, PYGAME_V2, BaseTest
import copy

import pygame
import pygame_menu

from pygame_menu.locals import POSITION_SOUTHEAST, POSITION_NORTH, POSITION_SOUTH, \
    POSITION_EAST, POSITION_WEST, POSITION_CENTER, POSITION_NORTHEAST, \
    POSITION_SOUTHWEST, POSITION_NORTHWEST
from pygame_menu.widgets import Label, Button
from pygame_menu.widgets.core.widget import Widget, AbstractWidgetManager


class WidgetsTest(BaseTest):

    def setUp(self) -> None:
        """
        Setup widgets test.
        """
        test_reset_surface()

    # noinspection PyTypeChecker
    def test_abstract_widget_manager(self) -> None:
        """
        Test abstract widget manager.
        """
        wm = AbstractWidgetManager()
        self.assertRaises(NotImplementedError, lambda: wm._theme)
        self.assertRaises(NotImplementedError, lambda: wm._add_submenu(None, None))
        self.assertRaises(NotImplementedError, lambda: wm._filter_widget_attributes({}))
        self.assertRaises(NotImplementedError, lambda: wm._configure_widget(None))
        self.assertRaises(NotImplementedError, lambda: wm._check_kwargs({}))
        self.assertRaises(NotImplementedError, lambda: wm._append_widget(None))
        self.assertRaises(NotImplementedError, lambda: wm.configure_defaults_widget(None))

    def test_abstract_widget(self) -> None:
        """
        Test an abstract widget.
        """
        w = Widget()

        w.readonly = True
        w.change()

        w.lock_position = True
        w.set_position(1, 1)
        self.assertEqual(w.get_position(), (0, 0))

        self.assertRaises(NotImplementedError, lambda: w._render())
        self.assertRaises(NotImplementedError, lambda: w._draw(surface))
        self.assertRaises(NotImplementedError, lambda: w._apply_font())
        self.assertRaises(NotImplementedError, lambda: w.update([]))

        self.assertEqual(w._get_menu_widgets(), [])
        self.assertEqual(w._get_menu_update_widgets(), [])

        w._selected = True
        self.assertGreater(w.get_selected_time(), 0)

    def test_kwargs(self) -> None:
        """
        Test kwargs addition.
        """

        def function_kwargs(*args, **kwargs) -> None:
            """
            Button callback.
            """
            self.assertEqual(len(args), 0)
            kwargs_k = list(kwargs.keys())
            self.assertEqual(kwargs_k[0], 'test')
            self.assertEqual(kwargs_k[1], 'widget')

        menu = MenuUtils.generic_menu()
        self.assertRaises(ValueError, lambda: menu.add.button('btn', function_kwargs, test=True))
        btn = menu.add.button('btn', function_kwargs, test=True, accept_kwargs=True, padding=10)
        self.assertEqual(len(btn._kwargs), 1)
        self.assertRaises(KeyError, lambda: btn.add_self_to_kwargs('test'))
        self.assertEqual(len(btn._kwargs), 1)
        btn.add_self_to_kwargs()
        self.assertEqual(len(btn._kwargs), 2)
        self.assertEqual(btn._kwargs['widget'], btn)
        btn.apply()

    def test_copy(self) -> None:
        """
        Test widget copy.
        """
        widget = pygame_menu.widgets.Widget()
        self.assertRaises(pygame_menu.widgets.core.widget._WidgetCopyException, lambda: copy.copy(widget))
        self.assertRaises(pygame_menu.widgets.core.widget._WidgetCopyException, lambda: copy.deepcopy(widget))

    def test_onselect(self) -> None:
        """
        Test onselect widgets.
        """
        menu = MenuUtils.generic_menu()
        test = [None]

        def on_select(selected, widget, _) -> None:
            """
            Callback.
            """
            if selected:
                test[0] = widget

        # Button
        self.assertIsNone(test[0])
        btn = menu.add.button('nice', onselect=on_select)  # The first to be selected
        self.assertEqual(test[0], btn)

        btn2 = menu.add.button('nice', onselect=on_select)
        self.assertEqual(test[0], btn)
        btn2.is_selectable = False
        btn2.select(update_menu=True)
        self.assertEqual(test[0], btn)
        btn2.is_selectable = True
        btn2.select(update_menu=True)
        self.assertEqual(test[0], btn2)
        btn.scale(1, 1)

        # Color
        color = menu.add.color_input('nice', 'rgb', onselect=on_select)
        color.select(update_menu=True)
        self.assertEqual(test[0], color)

        # Image
        image = menu.add.image(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES, onselect=on_select, font_color=(2, 9))
        image.select(update_menu=True)
        self.assertEqual(test[0], color)
        image.is_selectable = True
        image.select(update_menu=True)
        self.assertEqual(test[0], image)

        # Label
        label = menu.add.label('label', onselect=on_select)
        label.is_selectable = True
        label.select(update_menu=True)
        self.assertEqual(test[0], label)

        # None, it cannot be selected
        none = menu.add.none_widget()
        none.select(update_menu=True)
        self.assertEqual(test[0], label)

        # Selector
        selector = menu.add.selector('nice', ['nice', 'epic'], onselect=on_select)
        selector.select(update_menu=True)
        self.assertEqual(test[0], selector)

        # Textinput
        text = menu.add.text_input('nice', onselect=on_select)
        text.select(update_menu=True)
        self.assertEqual(test[0], text)

        # Vmargin
        vmargin = menu.add.vertical_margin(10)
        vmargin.select(update_menu=True)
        self.assertEqual(test[0], text)

    def test_non_ascii(self) -> None:
        """
        Test non-ascii.
        """
        menu = MenuUtils.generic_menu()
        m = MenuUtils.generic_menu(title=u'Ménu')
        m.clear()
        menu.add.button('0', pygame_menu.events.NONE)
        menu.add.button('Test', pygame_menu.events.NONE)
        menu.add.button(u'Menú', pygame_menu.events.NONE)
        menu.add.color_input(u'Cólor', 'rgb')
        text = menu.add.text_input(u'Téxt')
        menu.add.label(u'Téxt')
        menu.add.selector(u'Sélect'.encode('latin1'), [('a', 'a')])
        menu.enable()
        menu.draw(surface)

        # Text text input
        text.set_value('ą, ę, ś, ć, ż, ź, ó, ł, ń')
        self.assertEqual(text.get_value(), 'ą, ę, ś, ć, ż, ź, ó, ł, ń')
        text.set_value('')
        text.update(PygameEventUtils.key(pygame.K_l, char='ł', keydown=True))
        self.assertEqual(text.get_value(), 'ł')

    def test_background(self) -> None:
        """
        Test widget background.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add.label('Text')

        w.set_background_color((255, 255, 255), (10, 10))
        self.assertEqual(w._background_color, (255, 255, 255, 255))
        w.draw(surface)
        self.assertEqual(w._background_inflate[0], 10)
        self.assertEqual(w._background_inflate[1], 10)
        w.set_background_color(pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_GRAY_LINES))
        w.draw(surface)

        # Test hex
        w.set_background_color('#ff00ff')
        self.assertEqual(w._background_color, (255, 0, 255, 255))
        w.set_background_color('#f0f')
        self.assertEqual(w._background_color, (255, 0, 255, 255))

    def test_max_width_height(self) -> None:
        """
        Test widget max width/height.
        """
        label = Label('my label is really long yeah, it should be scaled in the width')
        label.set_font(pygame_menu.font.FONT_OPEN_SANS, 25, (255, 255, 255), (0, 0, 0),
                       (0, 0, 0), (0, 0, 0), (0, 0, 0))
        label.render()

        # The padding is zero, also the selection box and all transformations
        self.assertEqual(label.get_width(), 686)
        self.assertEqual(label.get_height(), 35)
        self.assertEqual(label.get_size()[0], 686)
        self.assertEqual(label.get_size()[1], 35)

        # Add padding, this will increase the width of the widget
        label.set_padding(58)
        self.assertEqual(label.get_width(), 802)

        # Apply scaling
        label.scale(0.5, 0.5)
        self.assertEqual(label.get_width(), 401)
        label.scale(0.5, 0.5)
        self.assertEqual(label.get_width(), 401)
        self.assertEqual(label.get_padding()[0], 28)
        self.assertEqual(label.get_padding(transformed=False)[0], 58)

        # Set size
        label.resize(450, 100)
        self.assertEqual(label.get_width(), 448)
        self.assertEqual(label.get_height(), 99)

        # Set size back
        label.scale(1, 1)
        label.set_padding(0)
        self.assertEqual(label.get_width(), 686)
        self.assertEqual(label.get_height(), 35)

        # Test max width
        label.scale(2, 2)
        label.set_padding(52)
        label.set_max_width(250)
        self.assertFalse(label._scale[0])  # max width disables scale
        self.assertEqual(label.get_width(), 249)
        self.assertEqual(label.get_height(), 35 + 52 * 2)

        # Apply the same, but this time height is scaled
        label.set_max_width(250, scale_height=True)
        self.assertEqual(label.get_height(), 113)

        # Set max height, this will disable max width
        label.set_max_height(100)
        self.assertIsNone(label._max_width[0])
        self.assertEqual(label.get_height(), 99)

        # Scale, disable both max width and max height
        label.set_max_width(100)
        label.set_max_height(100)
        label.scale(1.5, 1.5)
        self.assertIsNone(label._max_width[0])
        self.assertIsNone(label._max_height[0])
        self.assertTrue(label._scale[0])

        # Set scale back
        label.scale(1, 1)
        label.set_padding(0)
        self.assertEqual(label.get_width(), 686)
        self.assertEqual(label.get_height(), 35)

    def test_visibility(self) -> None:
        """
        Test widget visibility.
        """
        menu = MenuUtils.generic_menu()
        w = menu.add.label('Text')
        last_hash = w._last_render_hash
        w.hide()
        self.assertFalse(w.is_visible())
        self.assertNotEqual(w._last_render_hash, last_hash)
        last_hash = w._last_render_hash
        w.show()
        self.assertTrue(w.is_visible())
        self.assertNotEqual(w._last_render_hash, last_hash)

        w = Button('title')
        menu.add.generic_widget(w)
        w.hide()

    def test_font(self) -> None:
        """
        Test widget font.
        """
        menu = MenuUtils.generic_menu()

        w = menu.add.label('Text')  # type: Label
        self.assertRaises(AssertionError, lambda: w.update_font({}))
        w.update_font({'color': (255, 0, 0)})

        # Default color
        w._selected = False
        self.assertEqual(w.get_font_color_status(), w._font_color)

        # Readonly color
        w.readonly = True
        self.assertEqual(w.get_font_color_status(), w._font_readonly_color)

        # Read only + selected color
        w._selected = True
        self.assertEqual(w.get_font_color_status(), w._font_readonly_selected_color)

        # Selected only color
        w.readonly = False
        self.assertEqual(w.get_font_color_status(), w._font_selected_color)

        # Default color
        w._selected = False
        self.assertEqual(w.get_font_color_status(), w._font_color)

        # Test font shadow
        for pos in [POSITION_NORTHWEST, POSITION_NORTH, POSITION_NORTHEAST, POSITION_EAST,
                    POSITION_SOUTHEAST, POSITION_SOUTH, POSITION_SOUTHWEST, POSITION_WEST,
                    POSITION_CENTER]:
            w.set_font_shadow(position=pos)

    def test_padding(self) -> None:
        """
        Test widget padding.
        """
        menu = MenuUtils.generic_menu()
        self.assertRaises(Exception, lambda: menu.add.button(0, pygame_menu.events.NONE, padding=-1))
        self.assertRaises(Exception, lambda: menu.add.button(0, pygame_menu.events.NONE, padding='a'))
        self.assertRaises(Exception, lambda: menu.add.button(0, pygame_menu.events.NONE, padding=(0, 0, 0, 0, 0)))
        self.assertRaises(Exception, lambda: menu.add.button(0, pygame_menu.events.NONE, padding=(0, 0, -1, 0)))
        self.assertRaises(Exception, lambda: menu.add.button(0, pygame_menu.events.NONE, padding=(0, 0, 'a', 0)))

        w = menu.add.button(0, pygame_menu.events.NONE, padding=25)
        self.assertEqual(w.get_padding(), (25, 25, 25, 25))

        w = menu.add.button(0, pygame_menu.events.NONE, padding=(25, 50, 75, 100))
        self.assertEqual(w.get_padding(), (25, 50, 75, 100))

        w = menu.add.button(0, pygame_menu.events.NONE, padding=(25, 50))
        self.assertEqual(w.get_padding(), (25, 50, 25, 50))

        w = menu.add.button(0, pygame_menu.events.NONE, padding=(25, 75, 50))
        self.assertEqual(w.get_padding(), (25, 75, 50, 75))

    def test_draw_callback(self) -> None:
        """
        Test drawing callback.
        """
        menu = MenuUtils.generic_menu()

        def call(widget, _) -> None:
            """
            Callback.
            """
            widget.set_attribute('attr', True)

        btn = menu.add.button('btn')
        call_id = btn.add_draw_callback(call)
        self.assertFalse(btn.get_attribute('attr', False))
        menu.draw(surface)
        self.assertTrue(btn.get_attribute('attr', False))
        btn.remove_draw_callback(call_id)
        self.assertRaises(IndexError, lambda: btn.remove_draw_callback(call_id))  # Already removed
        menu.disable()

    def test_update_callback(self) -> None:
        """
        Test update callback.
        """

        def update(event, widget, _) -> None:
            """
            Callback.
            """
            assert isinstance(event, list)
            widget.set_attribute('attr', True)

        menu = MenuUtils.generic_menu(theme=TEST_THEME.copy())
        btn = menu.add.button('button', lambda: print('Clicked'))
        call_id = btn.add_update_callback(update)
        self.assertFalse(btn.get_attribute('attr', False))
        click_pos = btn.get_rect(to_real_position=True).center
        deco = menu.get_decorator()
        test_draw_rects = True

        def draw_rect() -> None:
            """
            Draw absolute rect on surface for testing purposes.
            """
            if not test_draw_rects:
                return
            surface.fill((0, 255, 0), btn.get_rect(to_real_position=True))

        deco.add_callable(draw_rect, prev=False, pass_args=False)
        click_pos_absolute = btn.get_rect(to_absolute_position=True).center
        self.assertNotEqual(click_pos, click_pos_absolute)
        self.assertEqual(menu.get_scrollarea()._view_rect, menu.get_scrollarea().get_absolute_view_rect())
        self.assertEqual(btn.get_scrollarea(), menu.get_current().get_scrollarea())
        if PYGAME_V2:
            self.assertEqual(btn.get_rect(), pygame.Rect(253, 153, 94, 41))
            self.assertEqual(btn.get_rect(to_real_position=True), pygame.Rect(253, 308, 94, 41))

        else:
            self.assertEqual(btn.get_rect(), pygame.Rect(253, 152, 94, 42))
            self.assertEqual(btn.get_rect(to_real_position=True), pygame.Rect(253, 307, 94, 42))

        self.assertEqual(len(menu._update_frames), 0)
        self.assertEqual(len(menu.get_current()._update_frames), 0)
        btn.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))  # MOUSEBUTTONUP
        self.assertTrue(btn.get_attribute('attr', False))
        btn.set_attribute('attr', False)
        btn.remove_update_callback(call_id)
        self.assertRaises(IndexError, lambda: btn.remove_update_callback(call_id))
        self.assertFalse(btn.get_attribute('attr', False))
        btn.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))
        self.assertFalse(btn.get_attribute('attr', False))

        def update2(event, widget, _) -> None:
            """
            Callback.
            """
            assert isinstance(event, list)
            widget.set_attribute('epic', 'bass')

        btn.add_update_callback(update2)
        self.assertFalse(btn.has_attribute('epic'))
        btn.draw(surface)
        self.assertFalse(btn.has_attribute('epic'))
        btn.update(PygameEventUtils.mouse_click(click_pos[0], click_pos[1]))
        self.assertTrue(btn.has_attribute('epic'))
        btn.remove_attribute('epic')
        self.assertRaises(IndexError, lambda: btn.remove_attribute('epic'))
        self.assertFalse(btn.has_attribute('epic'))

    def test_border(self) -> None:
        """
        Test widget border.
        """
        menu = MenuUtils.generic_menu()
        self.assertRaises(AssertionError, lambda: menu.add.button('', border_width=-1))
        self.assertRaises(AssertionError, lambda: menu.add.button('', border_width=1.5))
        self.assertRaises(AssertionError, lambda: menu.add.button('', border_width=1, border_color=(0, 0, 0), border_inflate=(-1, - 1)))
        btn = menu.add.button('', border_width=1, border_color=(0, 0, 0), border_inflate=(1, 1))
        self.assertEqual(btn._border_width, 1)
        self.assertEqual(btn._border_color, (0, 0, 0, 255))
        self.assertEqual(btn._border_inflate, (1, 1))
        self.assertEqual(btn._border_position, pygame_menu.widgets.core.widget.WIDGET_BORDER_POSITION_FULL)

        # Test positioning
        btn._draw_border(surface)

        # Change border position
        self.assertRaises(AssertionError, lambda: btn.set_border(1, 'black', (1, 1), POSITION_SOUTHEAST))
        btn.set_border(1, 'black', (1, 1), POSITION_NORTH)
        btn._draw_border(surface)
        btn.set_border(1, 'black', (1, 1), POSITION_SOUTH)
        btn._draw_border(surface)
        btn.set_border(1, 'black', (1, 1), POSITION_EAST)
        btn._draw_border(surface)
        btn.set_border(1, 'black', (1, 1), POSITION_WEST)

        # Invalid
        btn._border_position = [POSITION_SOUTHEAST]
        self.assertRaises(RuntimeError, lambda: btn._draw_border(surface))

        # None border
        btn._border_position = pygame_menu.widgets.core.widget.WIDGET_BORDER_POSITION_NONE
        btn._draw_border(surface)
        btn._border_position = 'invalid'
        self.assertRaises(RuntimeError, lambda: btn._draw_border(surface))

    def test_scale_maxwidth_height(self) -> None:
        """
        Test the interaction between scale, max width and max height.
        """
        menu = MenuUtils.generic_menu()
        btn = menu.add.button('button')

        btn.scale(1, 1)
        btn.scale(2, 3)

        self.assertTrue(btn._scale[0])
        self.assertEqual(btn._scale[1], 2)
        self.assertEqual(btn._scale[2], 3)

        # Now, set max width
        btn.set_max_width(150)
        self.assertFalse(btn._scale[0])

        btn.set_max_height(150)
        self.assertFalse(btn._scale[0])
        self.assertIsNone(btn._max_width[0])

        btn.scale(2, 2)
        self.assertIsNone(btn._max_height[0])
        self.assertTrue(btn._scale[0])
        self.assertEqual(btn._scale[1], 2)
        self.assertEqual(btn._scale[2], 2)

    def test_widget_floating_zero(self) -> None:
        """
        Test widgets with zero position if floated.
        """
        menu = MenuUtils.generic_menu(title='Example menu')
        img = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_PYGAME_MENU)
        img.scale(0.3, 0.3)
        image_widget = menu.add.image(image_path=img.copy())
        image_widget.set_border(1, 'black')
        image_widget.set_float(origin_position=True)
        menu.render()

        # Test position
        self.assertEqual(image_widget.get_position(), (8, 60))

        # Image translate
        image_widget.translate(100, 100)
        self.assertEqual(image_widget.get_position(), (8, 60))

        # Render, then update the position
        menu.render()
        self.assertEqual(image_widget.get_position(), (108, 160))

        image_widget.translate(-50, 0)
        menu.render()
        self.assertEqual(image_widget.get_position(), (-42, 60))

    def test_widget_center_overflow_ignore_scrollbar_thickness(self) -> None:
        """
        Test widget centering if overflow ignores scrollbar thickness.
        """
        theme = TEST_THEME.copy()

        menu = MenuUtils.generic_menu(width=320, theme=theme)
        for i in range(5):
            menu.add.button(f'Option{i + 1}')
            menu.add.button('Quit', pygame_menu.events.EXIT)

        pos_before = menu.get_selected_widget().get_position()
        theme.widget_alignment_ignore_scrollbar_thickness = True
        menu.render()
        pos_after = menu.get_selected_widget().get_position()

        # If we ignore scrollbar thickess in position, the difference
        # should be equal to the half of the scrollbar thickness (because
        # we have centered alignment)
        self.assertEqual(pos_after[0] - pos_before[0], menu._get_scrollbar_thickness()[1] / 2)  # x
        self.assertEqual(pos_after[1], pos_before[1])  # y
