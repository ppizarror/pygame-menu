==========================
Migration Guide - v3 to v4
==========================

- ``pygame_menu v4`` do not supports python 2.7 to 3.5.
- Added ``__all__`` to module, then some usage cases importing with * may fail.
- Menu Column/Row positioning has changed, now ``column_max_width`` has a different behaviour. For setting the minimum width of columns use ``column_min_width``.
- Menu method ``get_width()`` changes to``get_width(inner=False, widget=False)``.
- Removed ``column_force_fit_text`` from ``Menu`` constructor.
- Removed ``dummy_function`` from ``pygame_menu.utils``.
- Renamed ``touchscreen_enabled`` to ``touchscreen`` in ``Menu`` constructor.
- Renamed ``Widget`` method from ``set_selected(selected=True)`` to ``select(status=True, update_menu=False)``.
- Renamed widget ``expand_background_inflate_to_selection_effect`` to ``background_inflate_to_selection_effect``.
- Widget ``shadow_offset`` now cannot be ``None``, only ``int`` or ``float`` allowed.
- Widget ``VMargin`` now inherits from ``NoneWidget``.