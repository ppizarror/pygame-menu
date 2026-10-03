from __future__ import annotations

__all__ = ["Timer"]

import time

from pygame_menu.widgets.widget.label import Label


class Timer(Label):
    """
    Timer label widget.
    Displays elapsed time formatted dynamically via a title generator.
    """

    _start_time: float | None
    _elapsed: float
    _running: bool
    _started: bool
    _title_format: str

    def __init__(
        self,
        title_format: str = "{0:02d}:{1:02d}",
        label_id: str = "",
        **kwargs,
    ) -> None:
        """
        Initialize a timer label.

        :param title_format: Format string receiving minutes and seconds
        :param label_id: Timer ID
        :param kwargs: Additional label arguments
        """
        assert isinstance(title_format, str)

        super().__init__(
            title="",
            label_id=label_id,
            **kwargs,
        )

        self._start_time = None
        self._elapsed = 0.0
        self._running = False
        self._started = False
        self._title_format = title_format

        self.set_title_generator(self._generate_title)

    def _generate_title(self) -> str:
        """
        Generate the current timer title.

        :return: Formatted elapsed time
        """
        total = int(self.get_elapsed())
        minutes = total // 60
        seconds = total % 60

        return self._title_format.format(minutes, seconds)

    def start(self) -> Timer:
        """
        Start the timer.

        Starting an already started timer has no effect.

        :return: Self reference
        """
        if not self._started:
            self._start_time = time.monotonic()
            self._running = True
            self._started = True

        return self

    def pause(self) -> Timer:
        """
        Pause the timer.

        Pausing an already paused or stopped timer has no effect.

        :return: Self reference
        """
        if self._running and self._start_time is not None:
            self._elapsed += time.monotonic() - self._start_time
            self._start_time = None
            self._running = False

        return self

    def resume(self) -> Timer:
        """
        Resume the timer from pause.

        Resuming a timer that has not been started or is already running
        has no effect.

        :return: Self reference
        """
        if self._started and not self._running:
            self._start_time = time.monotonic()
            self._running = True

        return self

    def reset(self) -> Timer:
        """
        Reset the timer.

        The timer is stopped and its elapsed time is set to zero.

        :return: Self reference
        """
        self._start_time = None
        self._elapsed = 0.0
        self._running = False
        self._started = False

        self._title = self._generate_title()
        self._render()

        return self

    def get_elapsed(self) -> float:
        """
        Return total elapsed time in seconds.

        :return: Elapsed seconds
        """
        if self._running and self._start_time is not None:
            return self._elapsed + (time.monotonic() - self._start_time)

        return self._elapsed

    def set_elapsed(self, seconds: float) -> Timer:
        """
        Set elapsed time.

        If the timer is running, its current timing interval is restarted
        from the supplied elapsed value. The running state is preserved.

        :param seconds: Elapsed time in seconds
        :return: Self reference
        """
        assert seconds >= 0

        self._elapsed = float(seconds)

        if self._running:
            self._start_time = time.monotonic()

        self._title = self._generate_title()
        self._render()

        return self

    def is_running(self) -> bool:
        """
        Return whether the timer is currently running.

        :return: True if running
        """
        return self._running

    def is_paused(self) -> bool:
        """
        Return whether the timer is currently paused.

        A timer is paused after it has been started and is no longer running.

        :return: True if paused
        """
        return self._started and not self._running
