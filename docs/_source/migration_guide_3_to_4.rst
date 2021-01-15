
==========================
Migration Guide - v3 to v4
==========================
    
- Removed ``column_force_fit_text`` from ``Menu`` constructor.
- Renamed widget ``expand_background_inflate_to_selection_effect`` to ``background_inflate_to_selection_effect``.
- Menu Column/Row positioning has changed, now ``column_max_width`` has a different behaviour. For setting the minimum width of columns use ``column_min_width``.
- Widget ``VMargin`` now inherits from ``NoneWidget``.
- Widget ``shadow_offset`` now cannot be ``None``, only ``int`` or ``float`` allowed.
- Renamed ``touchscreen_enabled`` to ``touchscreen`` in ``Menu`` constructor.