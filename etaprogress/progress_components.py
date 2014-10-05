"""Holds classes for different components of the ProgressBar class and friends.

Holds code for parts of the progress bar such as the spinner and calculating the progress bar itself.
"""

from itertools import cycle


class Spinner(object):
    """Holds logic for 'spinner' character."""

    CHARS_SPINNER = ('/', '-', '\\', '|')

    def __init__(self):
        self._spinner_iter = cycle(self.CHARS_SPINNER)

    @property
    def _spinner(self):
        """Returns the spinner character. Every time this property is called a new character is returned."""
        return next(self._spinner_iter)


class EtaLetters(object):
    """Show the ETA using letters (e.g. '1s' or '5h 22m 2s').

    Instance variables:
    _eta_shortest -- show the shortest possible string length by only showing the biggest unit.
    _eta_leading_zero -- always show a leading zero for the minutes and seconds.
    """

    CHARS_ETA_SECOND = 's'
    CHARS_ETA_MINUTE = 'm'
    CHARS_ETA_HOUR = 'h'
    CHARS_ETA_DAY = 'd'
    CHARS_ETA_WEEK = 'w'

    def __init__(self, shortest=False, leading_zero=False):
        self._eta_shortest = shortest
        self._eta_leading_zero = leading_zero

    def _eta(self, seconds):
        """Returns a string representing a human-readable ETA.

        Positional arguments:
        seconds -- number of seconds left (eta).

        Returns:
        ETA string (e.g. '1h 3s').
        """
        if not seconds:
            return '00s' if self._eta_leading_zero else '0s'

        # Split up seconds into other units.
        values = dict(week=0, day=0, hour=0, minute=0, second=0)
        if seconds >= 604800:
            values['week'] = int(seconds / 604800.0)
            seconds -= values['week'] * 604800
        if seconds >= 86400:
            values['day'] = int(seconds / 86400.0)
            seconds -= values['day'] * 86400
        if seconds >= 3600:
            values['hour'] = int(seconds / 3600.0)
            seconds -= values['hour'] * 3600
        if seconds >= 60:
            values['minute'] = int(seconds / 60.0)
            seconds -= values['minute'] * 60
        values['second'] = seconds

        # Map to characters.
        leading = lambda x: ('{0:02d}' if self._eta_leading_zero else '{0}').format(x)
        mapped = (
            (self.CHARS_ETA_WEEK, str(values['week'] or '')),
            (self.CHARS_ETA_DAY, str(values['day'] or '')),
            (self.CHARS_ETA_HOUR, str(values['hour'] or '')),
            (self.CHARS_ETA_MINUTE, leading(values['minute']) if values['minute'] else ''),
            (self.CHARS_ETA_SECOND, leading(values['second']) if values['second'] else ''),
        )
        trimmed = [(k, v) for k, v in mapped if v]
        formatted = ['{0}{1}'.format(v, k) for k, v in trimmed]

        return formatted[0] if self._eta_shortest else ' '.join(formatted)


class EtaHMS(object):
    """Show the ETA as ss, mm:ss, h:mm:ss, or hh:mm:ss.

    Instance variables:
    _eta_always_show_hours -- don't hide the 0 hours.
    _eta_always_show_minutes -- don't hide the 0 minutes.
    _eta_hours_leading_zero -- show 01:00:00 instead of 1:00:00.
    """

    def __init__(self, always_show_hours=False, always_show_minutes=False, hours_leading_zero=False):
        self._eta_always_show_hours = always_show_hours
        self._eta_always_show_minutes = always_show_minutes
        self._eta_hours_leading_zero = hours_leading_zero

    def _eta(self, seconds):
        """Returns a string representing a human-readable ETA.

        Positional arguments:
        seconds -- number of seconds left (eta).

        Returns:
        ETA string (e.g. '01:59:59').
        """
        values = dict(hour=0, minute=0, second=0)
        if seconds >= 3600 or self._eta_always_show_hours:
            if self._eta_hours_leading_zero:
                template = '{hour:02d}:{minute:02d}:{second:02d}'
            else:
                template = '{hour}:{minute:02d}:{second:02d}'
        elif seconds >= 60 or self._eta_always_show_minutes:
            template = '{minute:02d}:{second:02d}'
        else:
            template = '{second:02d}'

        # Split up seconds into other units.
        if seconds >= 3600:
            values['hour'] = int(seconds / 3600.0)
            seconds -= values['hour'] * 3600
        if seconds >= 60:
            values['minute'] = int(seconds / 60.0)
            seconds -= values['minute'] * 60
        values['second'] = seconds

        return template.format(**values)


class Bar(object):
    """Holds logic for a progress bar.

    Instance variables:
    _bar_with_leading -- shows a leading character in the progress bar if True. Disables half unit.
    _bar_undefined_animated -- progress bar will be undefined (no final size) with an animated character(s) every time
        _bar() is called (like wget) if True.
    _bar_undefined_empty -- progress bar will be undefined and always empty with no animation if True.
    _bar_undefined_animated_pos_addend -- offset the animated progress bar character(s) to this on the next iteration
        and the direction of the animated progress bar (1 or -1).
    """

    CHARS_BAR_LEFT_BORDER = '['
    CHARS_BAR_RIGHT_BORDER = ']'
    CHARS_BAR_UNDEFINED_ANIMATED = '?'
    CHAR_BAR_UNIT_LEADING = ' '
    CHAR_BAR_UNIT_FULL = '#'
    CHAR_BAR_UNIT_HALF = ' '
    CHAR_BAR_UNIT_EMPTY = ' '

    def __init__(self, with_leading=False, undefined_animated=False, undefined_empty=False):
        self._bar_with_leading = with_leading
        self._bar_undefined_animated = undefined_animated
        self._bar_undefined_empty = undefined_empty
        self._bar_undefined_animated_pos_addend = (0, 1)

    def _bar(self, width, percent=None):
        """Returns a complete progress bar based on information provided.

        Positional arguments:
        width -- the width of the entire bar (including borders).
        percent -- percentage of the bar (0.0 - 100.0).

        Returns:
        Progress bar string (e.g. '[###     ]').
        """
        inner_width = width - (len(self.CHARS_BAR_LEFT_BORDER) + len(self.CHARS_BAR_RIGHT_BORDER))

        # Handle undefined progress bars.
        if self._bar_undefined_empty:
            inner_bar = self.CHAR_BAR_UNIT_EMPTY * inner_width
            return self.CHARS_BAR_LEFT_BORDER + inner_bar + self.CHARS_BAR_RIGHT_BORDER
        if self._bar_undefined_animated:
            pos, addend = self._bar_undefined_animated_pos_addend
            char_len = len(self.CHARS_BAR_UNDEFINED_ANIMATED)
            if addend > 0 and pos + char_len > inner_width:
                addend = -1
                pos = inner_width - char_len - 1
            elif addend < 0 and pos < 0:
                addend = 1
                pos = 1
            self._bar_undefined_animated_pos_addend = (pos + addend, addend)
            inner_bar = (pos * self.CHAR_BAR_UNIT_EMPTY) + self.CHARS_BAR_UNDEFINED_ANIMATED
            inner_bar = inner_bar.ljust(inner_width, self.CHAR_BAR_UNIT_EMPTY)
            return self.CHARS_BAR_LEFT_BORDER + inner_bar + self.CHARS_BAR_RIGHT_BORDER

        # Handle empty defined progress bars.
        if percent is None or percent < 0 or percent > 100:
            raise ValueError('percent must be from 0 to 100.')
        show_blocks = inner_width * (percent / 100.0)
        show_half = False if self._bar_with_leading else (show_blocks - int(show_blocks)) >= 0.5
        if show_blocks < 0.5 or (not show_half and show_blocks < 1):
            inner_bar = self.CHAR_BAR_UNIT_EMPTY * inner_width
            return self.CHARS_BAR_LEFT_BORDER + inner_bar + self.CHARS_BAR_RIGHT_BORDER

        # Handle defined progress bars with leading character.
        if self._bar_with_leading:
            inner_bar = (self.CHAR_BAR_UNIT_FULL * (int(show_blocks) - 1)) + self.CHAR_BAR_UNIT_LEADING
        else:
            inner_bar = (self.CHAR_BAR_UNIT_FULL * int(show_blocks)) + (self.CHAR_BAR_UNIT_HALF if show_half else '')
        inner_bar = inner_bar.ljust(inner_width, self.CHAR_BAR_UNIT_EMPTY)
        return self.CHARS_BAR_LEFT_BORDER + inner_bar + self.CHARS_BAR_RIGHT_BORDER
